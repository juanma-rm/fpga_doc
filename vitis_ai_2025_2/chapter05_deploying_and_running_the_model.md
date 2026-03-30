# Chapter 5 — Deploying and Running the Model

This chapter covers all deployment paths for compiled Vitis AI models: the low-level VART runtime (C++/Python), DPU debugging workflows, custom OP registration and deployment, ONNX Runtime via the Vitis AI Execution Provider (VOE), multi-FPGA programming with XRM and AKS, the WeGO whole-graph optimizer for TensorFlow/PyTorch, on-the-fly quantization in WeGO, and AMD ZenDNN CPU acceleration.

---

## Table of Contents

| Item | Description |
|------|-------------|
| [Programming with VART](#programming-with-vart) | C++ DpuRunner and Python Runner classes for DPU inference |
| [DPU Debug with VART](#dpu-debug-with-vart) | Verify DPU inference results against quantizer reference data |
| [Custom OP Workflow](#custom-op-workflow) | Define, quantize, compile, register, and deploy custom operations |
| [Programming with VOE](#programming-with-voe) | ONNX Runtime + Vitis AI Execution Provider for embedded deployment |
| [Multi-FPGA Programming](#multi-fpga-programming) | XRM resource management, AKS pipeline scheduler |
| [Using WeGO](#using-wego) | Whole Graph Optimizer for TF1.x, TF2.x, and PyTorch on data center DPU |
| [On-the-fly Quantization in WeGO](#on-the-fly-quantization-in-wego) | Integrated PTQ quantization within the WeGO flow |
| [Optimize Performance with AMD ZenDNN](#optimize-performance-with-amd-zendnn) | CPU acceleration for DPU-unsupported operators |

---

## Programming with VART

VART (Vitis AI Runtime) provides C++ and Python interfaces for DPU inference using compiled XMODEL files.

### C++ DpuRunner API

| Method | Description |
|--------|-------------|
| `execute_async(inputs, outputs)` | Submit input/output `TensorBuffer*` vectors for execution. Returns `{job_id, status}`. |
| `wait(jobid, timeout)` | Block until `job_id` completes. Pass `-1` for no timeout. |
| `get_tensor_format()` | Returns `TensorFormat::NCHW` or `TensorFormat::NHWC`. |
| `get_input_tensors()` / `get_output_tensors()` | Query shape and name of expected input/output tensors. |
| `create_runner(subgraph, mode)` | Factory: creates `unique_ptr<Runner>` from an XIR subgraph. `mode` is typically `"run"`. |

> **Tip:** For multi-threading, create a separate runner per thread.

### C++ Example

```cpp
auto runner = vart::Runner::create_runner(subgraph, "run");
auto job_data = runner->execute_async(inputs, outputs);
runner->wait(job_data.first, -1);
```

### Python Runner API

```python
class Runner:
    def __init__(self, subgraph, mode)
    def get_input_tensors(self)
    def get_output_tensors(self)
    def get_tensor_format(self)
    def execute_async(self, inputs, outputs)  # inputs/outputs: numpy arrays (C layout)
    def wait(self, job_id)
```

> **Note:** NumPy array buffer pointers are passed to the runtime and may be memory-mapped to FPGA DDR. Reuse the same arrays across calls.

### Python Example

```python
dpu_runner = runner.Runner(subgraph, "run")
jid = dpu_runner.execute_async(fpgaInput, fpgaOutput)
dpu_runner.wait(jid)
```

> For models with multiple subgraphs, see the [PyTorch subgraphs tutorial](https://github.com/Xilinx/Vitis-AI-Tutorials/tree/3.0/Tutorials/pytorch-subgraphs/).

---

## DPU Debug with VART

Four-step workflow to verify DPU inference correctness against quantizer reference results.

### Step 1 — Generate Quantized Model & Reference

**TensorFlow:**
```bash
# Quantize
vai_q_tensorflow quantize \
    --input_frozen_graph ./float/resnet_v1_50_inference.pb \
    --input_fn input_fn.calib_input \
    --output_dir quantize_model \
    --input_nodes input \
    --output_nodes resnet_v1_50/predictions/Reshape_1 \
    --input_shapes ?,224,224,3 \
    --calib_iter 100

# Dump reference data
vai_q_tensorflow dump \
    --input_frozen_graph quantize_model/quantize_eval_model.pb \
    --input_fn input_fn.dump_input \
    --output_dir=dump_gpu
```

**PyTorch:**
```bash
python resnet18_quant.py --quant_mode calib --subset_len 200
# Set deploy_check=True in export_xmodel API
python resnet18_quant.py --quant_mode test --deploy
```

### Step 2 — Compile to DPU XMODEL

```bash
# TensorFlow example (V70)
vai_c_tensorflow --frozen_pb quantize_model/quantize_eval_model.pb \
  --arch /opt/vitis_ai/compiler/arch/DPUCV2DX8G/V70/arch.json \
  --output_dir compile_model \
  --net_name resnet50_tf
```

### Step 3 — Generate DPU Inference Result

```bash
env XLNX_ENABLE_DUMP=1 XLNX_ENABLE_DEBUG_MODE=1 \
    XLNX_GOLDEN_DIR=./dump_gpu/dump_results_0 \
    xdputil run ./compile_model/resnet_v1_50_tf.xmodel \
    ./dump_gpu/dump_results_0/input_aquant.bin \
    2>result.log 1>&2
```

### Step 4 — Crosscheck Results

```bash
# View all layer comparisons
grep --color=always 'XLNX_GOLDEN_DIR.*layer_name' result.log

# View only failed layers
grep --color=always 'XLNX_GOLDEN_DIR.*fail ! layer_name' result.log
```

### Debug Tools

| Tool | Usage |
|------|-------|
| `xdputil xmodel <model> -s <svg>` | Generate SVG visualization of network structure |
| `xdputil run_op <model> <op_name> [-r ref] [-d dump]` | Test a single OP against reference data |
| `xdputil comp_float <golden> <dump> [-t threshold]` | Compare floating-point outputs (default threshold: 0.5%) |
| `xdputil --help` | Full usage information |

> **Note:** Install `graphviz` in the Docker environment: `sudo apt-get install graphviz`

---

## Custom OP Workflow

Starting with Vitis AI 2.5, PyTorch and TensorFlow 2 models with custom operations are supported. The workflow:

1. **Define** the OP as custom (unknown to XIR) and quantize the model
2. **Compile** the quantized model
3. **Register and implement** the custom OP (C++ or Python)
4. **Deploy** with `graph_runner` APIs

### Zero-Copy Support

The runtime optimizes data transfer between DPU and CPU OPs using zero-copy (address sharing):

| Type | Output of OP | Input of OP | Zero-Copy |
|------|-------------|-------------|-----------|
| a | Single DPU OP | Single CPU OP | Yes |
| b | Single CPU OP | Single DPU OP | Yes |
| c | Single CPU OP | Single CPU OP | Yes |
| d | Single DPU OP | Multiple CPU OP | Yes |
| e | Multiple CPU/DPU OPs | Single CPU OP | Yes |

### TensorFlow 2 Custom OP Example

**Quantize:**
```bash
conda activate vitis-ai-tensorflow2
bash 1_run_train.sh
bash 3_run_quantize.sh
```

Key quantization code:
```python
from tensorflow_model_optimization.quantization.keras import vitis_quantize
quant_model = vitis_quantize.VitisQuantizer(
    loaded_model,
    custom_objects={'MyLayer': MyLayer}
).quantize_model(calib_dataset=x_test, add_shape_info=True)
```

> `custom_objects` is a dict of `{"class_name": class}`. `add_shape_info=True` is required for custom layers.

**Compile:**
```bash
vai_c_tensorflow2 -m ./quantized/quantized.h5 \
  -a /opt/vitis_ai/compiler/arch/DPUCZDX8G/ZCU102/arch.json \
  -o ./ -n tf2_custom_op
```

**Register (C++):**
```cpp
#include <vart/op_imp.h>

class MylayerOp {
public:
    MylayerOp(const xir::Op* op1, xir::Attrs* attrs) : op{op1} {}
    int calculate(vart::simple_tensor_buffer_t output,
                  std::vector<vart::simple_tensor_buffer_t<float>> inputs) {
        // Implement custom logic
        return 0;
    }
    const xir::Op* const op;
};
DEF_XIR_OP_IMP(MylayerOp)
```

> **Library naming:** Must be `libvart_op_imp_<OpType>.so`. Copy to `/usr/lib` on target.

**Deploy with GraphRunner:**
```cpp
auto graph = xir::Graph::deserialize(xmodel_file);
auto attrs = xir::Attrs::create();
auto runner = vitis::ai::GraphRunner::create_graph_runner(graph.get(), attrs.get());

auto input_tensor_buffers = runner->get_inputs();
auto output_tensor_buffers = runner->get_outputs();

preprocess(image_file, input_tensor_buffers);
for (auto& input : input_tensor_buffers)
    input->sync_for_write(0, input->get_tensor()->get_data_size() /
                              input->get_tensor()->get_shape()[0]);

auto v = runner->execute_async(input_tensor_buffers, output_tensor_buffers);
runner->wait((int)v.first, -1);

for (auto output : output_tensor_buffers)
    output->sync_for_read(0, output->get_tensor()->get_data_size() /
                              output->get_tensor()->get_shape()[0]);
postprocess(output_tensor_buffers);
```

### PyTorch Custom OP Example

**Register with decorator:**
```python
from pytorch_nndct.utils import register_custom_op

@register_custom_op("PPScatterV2", attrs_list=['ny', 'nx', 'nchannels'])
def PPScatterV2(ctx, voxel_features, coords, ny, nx, nchannels):
    # Custom implementation
    ...
    return batch_canvas
```

**Compile:**
```bash
conda activate vitis-ai-pytorch
vai_c_xir -x VoxelNet_int.xmodel \
  -a /opt/vitis_ai/compiler/arch/DPUCZDX8G/ZCU102/arch.json \
  -o ./ -n pointpillars_custom_op
```

> **Samples:** 50+ common OP implementations at [vai_library/cpu_task/ops](https://github.com/Xilinx/Vitis-AI/tree/v3.5/src/vai_library/cpu_task/ops)

### Profiling Custom OPs

Use the `DEEPHI_PROFILING` environment variable to get per-OP timing breakdown when running models with custom operations:

```bash
env DEEPHI_PROFILING=1 ./sample_pointpillars_graph_runner ./model.xmodel input.bin
```

Example output:
```
CPU_UPDATE_INPUT  : 5us
CPU_UPDATE_OUTPUT : 55us
CPU_SYNC_FOR_READ : 46us
CPU_OP_EXEC       : 32us
CPU_OP_EXEC       : 36us
CPU_OP_EXEC       : 232us
CPU_OP_EXEC       : 26575us
CPU_SYNC_FOR_WRITE: 1us
```

---

## Programming with VOE

Vitis AI Execution Provider (Vitis AI EP) enables ONNX Runtime inference on AMD DPUs. VOE (Vitis AI ONNX Runtime Engine) implements the EP.

### Features

- ONNX Opset 18, ONNX Runtime 1.16.0, ONNX version 1.13
- C++ and Python API (Python 3)
- Supports incorporation of other EPs (e.g., ACL EP)
- Supported target: VEK280 in VAI 3.5

### Runtime Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `config_file` | `""` | Yes | Path to `vaip_config.json` configuration file |
| `cacheDir` | `/tmp/{user}/vaip/.cache/` | No | Cache directory |
| `cacheKey` | `{onnx_model_md5}` | No | Cache key to distinguish models |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `XLNX_ENABLE_CACHE` | `1` | Set to `0` to force recompilation |
| `XLNX_CACHE_DIR` | `/tmp/$USER/vaip/.cache/{md5}` | Custom cache path |

### C++ Deployment

```cpp
#include <experimental_onnxruntime_cxx_api.h>

auto onnx_model_path = "resnet50_pt.onnx";
Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "resnet50_pt");
auto session_options = Ort::SessionOptions();
auto options = std::unordered_map<std::string, std::string>({});
options["config_file"] = "/etc/vaip_config.json";
options["cacheDir"] = "/tmp/my_cache";
options["cacheKey"] = "abcdefg";

session_options.AppendExecutionProvider("VitisAI", options);
auto session = Ort::Experimental::Session(env, model_name, session_options);

// Create input tensors, run inference
auto output_tensors = session.Run(
    session.GetInputNames(), input_tensors, session.GetOutputNames());
```

### Python Deployment

```python
import onnxruntime

session = onnxruntime.InferenceSession(
    '[model_file].onnx',
    providers=["VitisAIExecutionProvider"],
    provider_options=[{"config_file": "/etc/vaip_config.json"}])

input_name = session.get_inputs()[0].name
result = session.run([], {input_name: input_data})
```

### Installation on Target Board

```bash
tar -xzvf vitis_ai_2023.1-r3.5.0.tar.gz -C /
pip3 install voe*.whl
pip3 install onnxruntime_vitisai*.whl
```

> **Note:** With `WITH_XCOMPILER` enabled, the first run compiles the model online, which takes time. Subsequent runs use the cache.

---

## Multi-FPGA Programming

### XRM — Xilinx Resource Manager

XRM manages FPGA resources across multiple Alveo cards on a server. Key features:

- Multi-FPGA heterogeneous support
- C++ API and CLI for resource allocation/release
- Resource allocation at FPGA, compute unit (CU), and service granularity
- Auto-release, multi-client, containerized support
- XCLBIN-to-DSA auto-association

Reference: [XRM GitHub](https://github.com/Xilinx/XRM)

### AKS — AI Kernel Scheduler

AKS automatically pipelines multi-stage deep learning inference graphs: preprocessing (decode, resize, color conversion), CNN inference (DPU kernel), and post-processing (SoftMax, NMS). Provides configurable, plug-and-play kernels.

Reference: [AKS on Vitis AI GitHub](https://github.com/Xilinx/Vitis-AI)

---

## Using WeGO

WeGO (Whole Graph Optimizer) deploys quantized models on data center DPUs by integrating the Vitis AI toolchain into TensorFlow and PyTorch frameworks. It handles graph partitioning, compilation, and runtime dispatch transparently.

> Currently supports data center DPU target `DPUCV2DX8G` on the V70 platform only.

### WeGO-Torch (PyTorch)

```python
import torch
import wego_torch

# Load quantized TorchScript module
mod = torch.jit.load(model_path)

# Compile with WeGO
wego_mod = wego_torch.compile(mod,
    wego_torch.CompileOptions(
        inputs_meta=[wego_torch.InputMeta(torch.float, [1, 3, 224, 224])]
    ))

# Run inference
result = wego_mod(input)
```

#### CompileOptions Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `accuracy_mode` | `AccuracyMode` | `Default` (remove redundant fixneurons for performance) or `ReserveFixNeuron` (keep fixneurons for accuracy) |
| `partition_options` | `PartitionOptions` | Min ops per DPU subgraph, extra acceleratable ops |
| `inputs_meta` | `list[InputMeta]` | Data type and shape per model input |
| `thread_parallel` | `uint32` | Thread parallelism optimization |
| `core_parallel` | `uint32` | Core parallelism optimization |
| `debug_options` | `DebugOptions` | Enable subgraph I/O dumping for accuracy debugging |

#### PartitionOptions

| Parameter | Description |
|-----------|-------------|
| `wego_subgraph_min_ops_number` | Minimum ops for a DPU subgraph to be dispatched to DPU (0 = no limit) |
| `extra_accel_op_list` | Operators to explicitly accelerate: `aten::mul`, `aten::mean`, `aten::linear`, `aten::unsqueeze`, `aten::slice` |

#### InputMeta

| Parameter | Values |
|-----------|--------|
| `dtype` | `torch.float`, `torch.int32`, `torch.bool` |
| `input_shape` | List/tuple of dimensions |

#### Key APIs

| API | Description |
|-----|-------------|
| `wego_torch.compile(module, options)` | Compile quantized TorchScript module → optimized module |
| `wego_torch.get_target_info()` | Returns `TargetInfo` (name, fingerprint, batch) |
| `wego_torch.version()` | Version string |

#### Limitations

- RCNN models with control-flow (dynamic shapes) not supported
- `Tensor[]` input type not supported; replace with explicit `Tensor` inputs
- Batch size at inference must match the batch size used during quantization export
- Only a subset of DPU-supported operators is covered

### WeGO-Torch C++ Classes and APIs

WeGO-Torch also provides a C++ interface for compilation and inference, mirroring the Python API.

#### `wego_torch::core::CompileOptions`

C++ class specifying compilation options, passed as an argument to `wego_torch::core::Compile()`.

| Type | Name | Description |
|------|------|-------------|
| `wego_torch::AccuracyMode` | `accuracy_mode` | `kDefaultRemoveFixNeuron` (remove redundant fixneurons for performance) or `kReserveFixNeuron` (keep all fixneurons for accuracy) |
| `wego_torch::core::PartitionOptions` | `partition_options` | Partition configuration (min ops per DPU subgraph, extra accel ops) |
| `std::vector<InputMeta>` | `inputs_meta` | Input metadata per model input |
| `uint32_t` | `thread_parallel` | Thread parallelism optimization |
| `uint32_t` | `core_parallel` | Core parallelism optimization |
| `wego_torch::core::DebugOptions` | `debug_options` | Debug configuration |

#### `wego_torch::core::PartitionOptions`

| Type | Name | Description |
|------|------|-------------|
| `uint32_t` | `wego_subgraph_min_ops_number` | Minimum operators for a DPU subgraph (0 = no limit). Prevents small subgraphs from being dispatched to DPU where memory transfer overhead would dominate. |
| `std::vector<std::string>` | `extra_accel_op_list` | Operators to explicitly accelerate on DPU: `aten::mul`, `aten::mean`, `aten::linear`, `aten::unsqueeze`, `aten::slice` |

#### `wego_torch::core::DebugOptions`

| Type | Name | Description |
|------|------|-------------|
| `bool` | `accuracy_debug` | Set `true` to dump subgraph inputs/outputs for accuracy debugging (default: `false`) |

#### `wego_torch::InputMeta`

Describes one input tensor's type and shape. WeGO-Torch requires static type and shape for compilation.

| Type | Name | Description |
|------|------|-------------|
| `wego_torch::DataType` | `type_` | `kBool`, `kInt32`, or `kFloat32` |
| `wego_torch::ShapeType` | `input_shape_` | Input tensor dimensions |

#### `wego_torch::TargetInfo`

Wrapper for DPU target information.

| Type | Name | Description |
|------|------|-------------|
| `std::string` | `name` | DPU target name |
| `uint64_t` | `fingerprint` | DPU target fingerprint |
| `bool` | `is_fingerprint_driven` | Whether DPU subgraphs are compiled by fingerprint or target name |
| `uint32_t` | `batch` | Batch size supported by the DPU target |

#### Core C++ APIs

| Function | Signature | Description |
|----------|-----------|-------------|
| `Compile` | `torch::jit::Module Compile(const torch::jit::Module &module, CompileOptions options)` | Compile a quantized TorchScript module into an optimized module |
| `GetTargetInfo` | `TargetInfo GetTargetInfo()` | Query DPU target info (name, fingerprint, batch) |
| `getVersionInfo` | `std::string getVersionInfo()` | Get WeGO-Torch version string |

#### C++ Example

```cpp
#include <wego_torch/core.h>

// Load quantized TorchScript module
auto mod = torch::jit::load(quantized_model_path);

// Configure compilation options
auto options = wego_torch::core::CompileOptions();
options.inputs_meta = {
    wego_torch::InputMeta(wego_torch::DataType::kFloat32, {1, 3, 224, 224})
};

// Compile
auto wego_mod = wego_torch::core::Compile(mod, options);

// Query target info
auto target_info = wego_torch::core::GetTargetInfo();
auto batch = target_info.batch;

// Run inference
auto output = wego_mod.forward({input_tensor});
```

### WeGO-TensorFlow 2.x

```python
from tensorflow.compiler import vitis_vai

target_info = vitis_vai.get_target_info()
batch = target_info.batch

wego_fn = vitis_vai.create_wego_model(
    'quantized.h5',
    feed_dict={},
    accuracy_mode=vitis_vai.enums.AccuracyMode.Default)

result = wego_fn(input_data)
```

| API | Parameters | Return |
|-----|-----------|--------|
| `get_target_info()` | None | `DeviceInfo` (batch, target, fingerprint) |
| `create_wego_model(input_h5, feed_dict, accuracy_mode)` | h5 path, shape dict, accuracy mode | Concrete function with VaiWeGOOps |

### WeGO-TensorFlow 1.x

```python
from tensorflow.contrib import vitis_vai

wego_graph = vitis_vai.create_wego_graph(
    input_graph_def,
    feed_dict={},
    accuracy_mode=vitis_vai.enums.AccuracyMode.Default)
```

| API | Parameters | Return |
|-----|-----------|--------|
| `get_target_info()` | None | `DeviceInfo` (batch, target, fingerprint) |
| `create_wego_graph(graph_def, feed_dict, accuracy_mode)` | GraphDef, shape dict, accuracy mode | New GraphDef with VaiWeGOOps |

### Environment Variable

| Variable | Description |
|----------|-------------|
| `WEGO_ENABLE_AGGRESSIVE_SHAPE_INFERENCE` | Set to `1` when operators need batch size for static shape inference. Sets batch to 1. |

### OnBoard Visualization

Experimental TensorBoard extension for WeGO debugging — visualizes inference flow, graph structure before/after WeGO transformation, and DPU platform info. Available for PyTorch and TensorFlow 2.

---

## On-the-fly Quantization in WeGO

WeGO integrates the Vitis AI quantizer for PTQ directly in the compilation flow, avoiding separate quantization steps.

> **Limitations:** PTQ only (no QAT). CPU-only quantization (no GPU).

### PyTorch

```python
quantized_module = wego_torch.quantize(
    module=float_model,
    input_shapes=[[1, 3, 224, 224]],
    dataloader=calib_loader,
    calibrator=my_calibrator,
    device=torch.device("cpu"),
    output_dir="quantize_result",
    bitwidth=8
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `module` | `torch.nn.Module` | Float model to quantize |
| `input_shapes` | `Sequence[Sequence]` | Input tensor shapes |
| `dataloader` | `Iterable` | Calibration data |
| `calibrator` | `Callable` | `(module, batch_data, batch_index, device) → None`. Called N+1 times (N calibration + 1 export) |
| `export_dataloader` | `Iterable` | Optional; for the export stage. Default: reuses first calibration batch |
| `device` | `torch.device` | CPU only currently |
| `output_dir` | `str` | Working directory (default: `"quantize_result"`) |
| `bitwidth` | `int` | Quantization bits (default: 8) |
| `quant_config_file` | `str` | Optional quantizer config file path |

### TensorFlow 2.x

```python
vitis_vai.quantize(
    input_float=keras_model,
    quantize_strategy='pof2s',
    calib_dataset=calib_data,
    calib_steps=100,
    save_path='./vai_wego/quantized.h5'
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `quantize_strategy` | `'pof2s'` | `pof2s`, `pof2s_tqt`, `fs`, `fsx` |
| `calib_dataset` | — | Representative calibration dataset |
| `calib_steps` | `None` | Steps for calibration |
| `calib_batch_size` | `32` | Batch size (for numpy inputs) |
| `save_path` | `'./vai_wego/quantized.h5'` | Output path |
| `add_shape_info` | `False` | Set `True` for models with custom layers |

### TensorFlow 1.x

```python
vitis_vai.quantize(
    input_frozen_graph="model.pb",
    input_nodes="input",
    input_shapes="?,224,224,3",
    output_nodes="output",
    input_fn="my_input_fn.input_fn",
    method=1,
    calib_iter=100,
    output_dir="./quantize_results"
)
```

| `method` | Description |
|----------|-------------|
| 0 | Non-overflow: no saturation, may be less accurate |
| 1 | Min-diffs: allows saturation for large values, better outlier tolerance (default) |
| 2 | Min-diffs + depthwise strategy |

---

## Optimize Performance with AMD ZenDNN

ZenDNN accelerates CPU-side operations (DPU-unsupported operators) on AMD CPUs.

> ⚠️ Experimental feature. Performance gain not guaranteed.

### Enable in WeGO PyTorch

```python
wego_mod = wego_torch.compile(mod,
    wego_torch.CompileOptions(
        ...,
        optimize_options=wego_torch.OptimizeOptions(zendnn_enable=True)
    ))
```

### Enable in WeGO TensorFlow 2

```bash
export TF_ENABLE_ZENDNN_OPTS=1
```

### ZenDNN Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OMP_DYNAMIC` | — | Must set to `FALSE` when ZenDNN is enabled |
| `OMP_NUM_THREADS` | # physical cores | Tune per inference threads to avoid over-subscription |
| `ZENDNN_GEMM_ALGO` | `3` | GEMM algorithm path: 0–4 |
| `ZENDNN_TENSOR_POOL_LIMIT` | `32` | Tensor pool limit (TF2 only). Try `1` for some models. |
| `ZENDNN_TENSOR_BUF_MAXSIZE_ENABLE` | `0` | `0`: reduced pool, `1`: increased pool |
| `TF_ENABLE_ZENDNN_OPTS` | `0` | Set `1` to enable ZenDNN in TF2 |

### Tuning Guidelines

- Set `OMP_NUM_THREADS ≤ cores / inference_threads` to avoid CPU contention
- Example: 64 cores, 16 threads → `OMP_NUM_THREADS=4`
- Try `ZENDNN_TENSOR_POOL_LIMIT=1` if default causes issues

---

## Best Practices

1. **Create one VART runner per thread** for multi-threaded DPU inference.
2. **Reuse NumPy arrays** in Python — buffer pointers may be memory-mapped to FPGA DDR.
3. **Always run the DPU debug workflow** before production deployment to catch layer-level mismatches.
4. **Name custom OP libraries** as `libvart_op_imp_<OpType>.so` exactly — mismatches prevent runtime linking.
5. **Use `graph_runner` APIs** (not raw VART) when deploying models with custom OPs to benefit from zero-copy optimization.
6. **Cache compiled VOE models** — first compilation is slow; subsequent runs use `cacheDir`/`cacheKey`.
7. **Tune ZenDNN `OMP_NUM_THREADS`** relative to CPU core count and inference thread count.
8. **Use accuracy_mode=ReserveFixNeuron** in WeGO if default mode introduces unacceptable accuracy loss.
9. **Set `deploy_check=True`** in `export_xmodel()` during PyTorch quantization to enable golden result generation.
10. **For VOE deployment**, the input is the quantized ONNX model, not the compiled XMODEL.

---

## Quick Reference

| Deployment Path | Input | API / Tool | Target |
|----------------|-------|------------|--------|
| VART (C++) | Compiled `.xmodel` | `vart::Runner::create_runner()` | Edge + Data Center |
| VART (Python) | Compiled `.xmodel` | `runner.Runner()` | Edge + Data Center |
| Custom OP + GraphRunner | Compiled `.xmodel` + custom `.so` | `GraphRunner::create_graph_runner()` | Edge + Data Center |
| VOE (ONNX Runtime) | Quantized `.onnx` | `onnxruntime.InferenceSession()` with `VitisAIExecutionProvider` | VEK280 (VAI 3.5) |
| WeGO-Torch | Quantized TorchScript | `wego_torch.compile()` | V70 (DPUCV2DX8G) |
| WeGO-TF2 | Quantized `.h5` | `vitis_vai.create_wego_model()` | V70 (DPUCV2DX8G) |
| WeGO-TF1 | Quantized `.pb` | `vitis_vai.create_wego_graph()` | V70 (DPUCV2DX8G) |

### See Also

- [Chapter 1 — Vitis AI Overview](chapter01_vitis_ai_overview.md)
- [Chapter 3 — Quantizing the Model](chapter03_quantizing_the_model.md) — quantization is prerequisite to deployment
- [Chapter 4 — Compiling the Model](chapter04_compiling_the_model.md) — XMODEL compilation for VART
- [Chapter 6 — Profiling the Model](chapter06_profiling_the_model.md) — profile deployed model performance

---

## Source Attribution

- **Document:** UG1414 (v3.5) — Vitis AI User Guide
- **Date:** September 28, 2023
- **Chapter:** Chapter 5 — Deploying and Running the Model (pp. 159–217)
