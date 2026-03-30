# Chapter 4 — Compiling the Model

The Vitis AI Compiler (VAI_C) maps quantized neural-network models onto optimized DPU instruction sequences. This chapter covers the XIR-based intermediate representation, compilation flows for TensorFlow / TensorFlow 2.x / PyTorch, plugin-based custom accelerator integration, supported operators per DPU architecture, and the VAI_C command-line interface.

---

## Table of Contents

| Item | Description |
|------|-------------|
| [Vitis AI Compiler](#vitis-ai-compiler) | Unified compiler framework — parsing, IR, fusion, scheduling, code generation |
| [XIR — Intermediate Representation](#xir--intermediate-representation) | Graph-based IR: Op, Tensor, Graph, Subgraph libraries; XMODEL serialization |
| [Compiling for DPU](#compiling-for-dpu) | XIR-based compilation for TensorFlow, TensorFlow 2.x, and PyTorch targets |
| [Compiling for Customized Accelerator](#compiling-for-customized-accelerator) | Plugin pipeline for custom IPs — partition, compile, build, and use plugins |
| [Supported Operators & DPU Limitations](#supported-operators--dpu-limitations) | Per-DPU operator tables with kernel size, stride, dilation, activation constraints |
| [Operators Supported by TensorFlow](#operators-supported-by-tensorflow) | TF → XIR → DPU operator mapping |
| [Operators Supported by PyTorch](#operators-supported-by-pytorch) | PyTorch → XIR → DPU operator mapping |
| [VAI_C Usage](#vai_c-usage) | Command-line options for `vai_c_caffe`, `vai_c_tensorflow`, `vai_c_tensorflow2`, `vai_c_xir` |

---

## Vitis AI Compiler

VAI_C is a unified interface for a family of compilers that optimize neural-network computations for different DPU architectures. The workflow is:

1. **Parse** the quantized input model topology
2. **Construct** an internal computation graph as an XIR intermediate representation
3. **Optimize** — node fusion (e.g., batch-norm into convolution), instruction scheduling (parallelism, data reuse)
4. **Generate** a compiled XMODEL targeting the specific DPU microarchitecture

### Supported DPUs

| DPU Name | Hardware Platform |
|----------|-------------------|
| `DPUCZDX8G` | AMD Zynq™ UltraScale+™ MPSoC |
| `DPUCVDX8G` | AMD Versal™ adaptive SoC VCK190, Versal AI Core Series |
| `DPUCVDX8H` | Versal adaptive SoC VCK5000 evaluation kit |
| `DPUCV2DX8G` | Versal adaptive SoC VEK280, Versal AI Edge, V70 evaluation kit, Alveo V70 |

---

## XIR — Intermediate Representation

AMD Intermediate Representation (XIR) is a graph-based IR designed for compilation and deployment of DPU on FPGA. It is the foundation for the Vitis AI quantizer, compiler, runtime, and other tools.

### Core Libraries

| Library | Purpose |
|---------|---------|
| **Op** | Well-defined operator set covering TensorFlow, PyTorch, Caffe, and all built-in DPU operators. Supports dynamic extension. |
| **Tensor** | Multi-dimensional data descriptor (shape + data type). Does not hold actual data — describes the data block only. Supported types: float, half, int32, int16, XINT8, ternary, binary. |
| **Graph** | Container maintaining Ops as vertices with producer-consumer edges. Key APIs: `serialize`, `deserialize`, `topological_sort`. |
| **Subgraph** | Tree-like hierarchy dividing ops into non-overlapping sets. The root is the entire op set; nested subgraphs must be children of outer ones. Supports topo-sort and isomorphism. |

### Formats

- **In-memory:** Graph object (via XIR library)
- **File format:** `.xmodel` — serialized/deserialized via `xir::Graph::serialize` / `xir::Graph::deserialize`

### PyXIR

XIR offers Python APIs (PyXIR) for full access to XIR within Python, enabling co-development and integration with existing XIR-based tools without cross-language bridging.

### Key APIs

```cpp
// Graph
xir::Graph::serialize(const std::string& path);
xir::Graph::deserialize(const std::string& path);
xir::Graph::topological_sort();

// Op — set/get extrinsic attributes
xir::Op::set_attr(const std::string& key, const T& value);

// Each Op has exactly one output Tensor but may have multiple fanout Ops
```

---

## Compiling for DPU

The XIR-based compiler accepts quantized models from TensorFlow 1.x, TensorFlow 2.x, or PyTorch. The flow is:

1. **Transform** input model into XIR format (eliminate framework-specific differences)
2. **Optimize** graph and break into subgraphs (DPU-capable vs. CPU fallback)
3. **Apply** architecture-aware optimizations per subgraph
4. **Generate** instruction stream for DPU subgraphs
5. **Serialize** optimized graph into compiled `.xmodel` file for VART

> Architecture files (`arch.json`) for pre-built DPU platforms are located at `/opt/vitis_ai/compiler/arch` inside the Vitis AI Docker container.

### TensorFlow 1.x

Input: `quantize_eval_model.pb` from `vai_q_tensorflow`.

```bash
vai_c_tensorflow \
  -f /PATH/TO/quantize_eval_model.pb \
  -a /PATH/TO/arch.json \
  -o /OUTPUTPATH \
  -n netname
```

> If the model lacks input tensor shape info, specify it manually:
> `--options '{"input_shape": "1,224,224,3"}'`

### TensorFlow 2.x

Input: quantized `.h5` file from `vai_q_tensorflow2`. Only Keras functional APIs are supported.

```bash
vai_c_tensorflow2 \
  -m /PATH/TO/quantized.h5 \
  -a /PATH/TO/arch.json \
  -o /OUTPUTPATH \
  -n netname
```

### PyTorch

Input: quantized `.xmodel` from NNDCT quantizer (XIR format directly).

```bash
vai_c_xir \
  -x /PATH/TO/quantized.xmodel \
  -a /PATH/TO/arch.json \
  -o /OUTPUTPATH \
  -n netname
```

---

## Compiling for Customized Accelerator

When a model contains operations that the DPU cannot support, those subgraphs are mapped to the CPU by default. To accelerate them with custom FPGA IPs, use the **Plugin** pipeline.

### Plugin Architecture

Plugins execute sequentially before the compiler compiles for DPU. The flow:

1. A child subgraph is created for each operator
2. The plugin picks operators to accelerate
3. It merges them into larger device-level subgraphs
4. Maps them to the custom IP
5. Attaches runtime information (instructions) on the subgraphs

### Implementing a Plugin

**Step 1 — Implement `Plugin::partition()`**

```cpp
std::set<xir::Subgraph*> partition(xir::Graph* graph);
```

Helper functions for picking subgraphs:

| Function | Returns |
|----------|---------|
| `filter_by_name(graph, name)` | Subgraph with a specific name |
| `filter_by_type(graph, type)` | Subgraphs with a specific type |
| `filter_by_template(graph, temp)` | Subgraphs matching a specific structure template |
| `filter(graph, func)` | Subgraphs matching a custom predicate (useful for finding all uncompiled subgraphs) |

Use `merge_subgraph()` to combine child subgraphs at the same level. If the list cannot be merged into one, it merges as far as possible.

**Step 2 — Set name, device, and runner** for the subgraphs returned by `partition()`.

**Step 3 — Implement `Plugin::compile(xir::Subgraph*)`**

Called for every subgraph returned by `partition()`. Attach information on subgraphs for runtime (`VART::Runner`).

### Building the Plugin

```cpp
extern "C" plugin* get_plugin() { return new YOURPLUGIN(); }
```

Build the implementation into a shared library (`.so`).

### Using the Plugin

```bash
vai_c_xir ... --options '{"plugins": "plugin0,plugin1"}'
```

Plugins execute sequentially in the order specified. DPU and CPU compilation runs after all plugins complete.

> **Samples:** [Vitis-AI/src/vai_runtime/plugin-samples](https://github.com/Xilinx/Vitis-AI/tree/v3.5/src/vai_runtime/plugin-samples)

---

## Supported Operators & DPU Limitations

Operator support depends on the DPU type, ISA version, and configuration. When operation parameters exceed DPU limitations, the operator falls back to CPU. Configuration details are in the product guides:

| DPU | Product Guide |
|-----|---------------|
| DPUCZDX8G | PG338 |
| DPUCAHX8H | PG367 |
| DPUCVDX8G | PG389 |
| DPUCVDX8H | PG403 |
| DPUCV2DX8G | PG425 |

### DPU Intrinsic Parameters

| DPU Configuration | channel_parallel | bank_depth | bank_num |
|-------------------|-----------------|------------|----------|
| DPUCZDX8G_ISA1_B4096 (ZCU102/104) | 16 | 2048 | 8 |
| DPUCAHX8L_ISA0 (U50/U50LV/U280) | 32 | 4096 | — |
| DPUCVDX8G_ISA3_C32B3 (VCK190) | 16 | 8192 | 8 |
| DPUCAHX8H_ISA2_DWC (U50/U55C/U50LV/U280) | 16 | 2048 | — |
| DPUCADF8H_ISA0 (U200/U250) | 16 | 8192 | — |
| DPUCVDX8H_ISA1_F2W4_4PE (VCK5000) | 64 | 2048 | — |
| DPUCV2DX8G_ISA1_C20B1 (VEK280/V70) | 32 | 65528 | 1 |

### conv2d Limits

| Parameter | DPUCZDX8G | DPUCAHX8L | DPUCVDX8G | DPUCAHX8H | DPUCADF8H | DPUCVDX8H | DPUCV2DX8G |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------|
| Kernel size | w,h: [1,16] | w,h: [1,16] | w,h: [1,16] | w*h*ceil(ic/2048)≤64 | w,h: [1,16] | w,h: [1,16] | w,h: [1,16]; 256*h*w≤13760 |
| Strides | w,h: [1,8] | w,h: [1,4] | w,h: [1,8] | w,h: [1,4] | w,h: [1,8] | w,h: [1,4] | w,h: [1,8] |
| Dilation | dilation * input_channel ≤ 256 * channel_parallel | | | | | | |
| In Size | kw*kh*ceil(ic/cp) ≤ bank_depth | | | kw*kh*ceil(ic/cp)*ceil(cp/4)+4 ≤ bank_depth | ic ≤ 256*cp | ic ≤ 256*cp | ic ≤ 256*cp |
| Out Size | output_channel ≤ 256 * channel_parallel | | | | | | |
| Activations | ReLU, LeakyReLU, ReLU6, Hard-Swish, Hard-Sigmoid | ReLU, ReLU6 | ReLU, LeakyReLU, ReLU6, Hard-Swish, Hard-Sigmoid | ReLU, LeakyReLU, ReLU6 | ReLU, LeakyReLU | ReLU, LeakyReLU, ReLU6, Hard-Swish, Hard-Sigmoid | ReLU, LeakyReLU, ReLU6, Hard-Swish, Hard-Sigmoid |

### depthwise-conv2d Limits

| Parameter | DPUCZDX8G | DPUCAHX8L | DPUCVDX8G | DPUCAHX8H | DPUCADF8H | DPUCVDX8H | DPUCV2DX8G |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------|
| Kernel size | w,h: [1,256] | w,h: [3] | w,h: [1,256] | w,h: {1,2,3,5,7} | Not supported | w,h: [1,8] | w,h: [1,256]; h*w≤431 |
| Strides | w,h: [1,256] | w,h: [1,2] | w,h: [1,256] | w,h: [1,4] | — | w,h: [1,4] | w,h: [1,256] |
| Activations | ReLU, ReLU6, LeakyReLU, Hard-Swish, Hard-Sigmoid | ReLU, ReLU6 | ReLU, ReLU6, LeakyReLU, Hard-Swish, Hard-Sigmoid | ReLU, ReLU6 | — | ReLU, ReLU6 | ReLU, ReLU6, LeakyReLU, Hard-Swish, Hard-Sigmoid |

### Other Supported Operations (Summary)

| Operation | Key Constraints |
|-----------|----------------|
| **transposed-conv2d** | Kernel size: kw/sw, kh/sh: [1,16]. Activations vary per DPU. |
| **depthwise-transposed-conv2d** | Kernel size varies. Not supported on DPUCADF8H. |
| **max-pooling** | Kernel w,h up to [1,256] on most DPUs. Activation support varies. |
| **average-pooling** | Similar to max-pooling. Some DPUs require w==h. |
| **eltwise** | Types: sum, prod (some DPUs sum only). Input: ic ≤ 256 * cp. |
| **concat** | Network-specific limitation (feature map size, quantization, compiler optimizations). |
| **reorg** | stride² * ic ≤ 256 * cp (reverse=false); ic ≤ 256 * cp (reverse=true). |
| **pad** | Mode: SYMMETRIC supported. CONSTANT pad(value=0) fused into adjacent ops. |
| **global pooling** | Processed as general pooling with kernel = input tensor size. |
| **InnerProduct / FC / MatMul** | Transformed into conv2d. |
| **resize** | NEAREST: scale constraints on bank_depth. BILINEAR: transformed to pad + dw-transposed-conv2d. TRILINEAR (VCK190 only): pad + transposed-conv3d. |
| **conv3d** | VCK190 (DPUCVDX8G) only. w,h,d: [1,16]. |
| **depthwise-conv3d** | VCK190 only. w,h: [1,256], d: [1,16]. |
| **transposed-conv3d** | VCK190 only. |
| **depthwise-transposed-conv3d** | VCK190 only. |
| **argmax** | DPUCZDX8G, DPUCVDX8G, DPUCV2DX8G only. ic ≤ 128. |
| **reduction_max** | Same DPUs as argmax. ic < 2¹². |
| **cost_volume** | DPUCZDX8G and DPUCVDX8G only. |
| **strided_slice** | stride_batch=1, stride_channel=1. |
| **correlation1d/2d_elemwise** | DPUCZDX8G and DPUCVDX8G only. |

---

## Operators Supported by TensorFlow

TensorFlow operators are parsed, transformed to XIR, then mapped to DPU or CPU. Key mappings:

| TensorFlow OP | XIR OP | DPU Implementation |
|---------------|--------|-------------------|
| `placeholder` / `inputlayer` | `data` | Memory allocation for input |
| `conv2d` | `conv2d` | Convolution Engine |
| `depthwiseconv2dnative` | `depthwise-conv2d` | Depthwise-Convolution Engine |
| `conv2dbackpropinput` / `conv2dtranspose` | `transposed-conv2d` | Convolution Engine |
| `spacetobatchnd + conv2d + batchtospacend` | `conv2d` (dilated) | Convolution Engine (when AMD requirements met) |
| `matmul` / `dense` | `conv2d` / `matmul` | Convolution Engine (when equivalent conv2d is feasible) |
| `maxpool` / `maxpooling2d` / `globalmaxpool2d` | `maxpool2d` | Pooling Engine |
| `avgpool` / `averagepooling2d` / `globalaveragepooling2d` | `avgpool2d` | Pooling Engine |
| `mean` | `avgpool` / `reduction_mean` | Mapped to avgpool when equivalent and meets HW requirements |
| `relu`, `relu6`, `leakyrelu` | `relu`, `relu6`, `leaky_relu` | Fused into adjacent operations (e.g., convolution) |
| `fixneuron` / `quantizelayer` | `fix` | Split into float2fix/fix2float, fused with adjacent ops |
| `add`, `addv2` | `add` | Element-wise → DPU Add Engine; channel-wise → fused with conv |
| `mul` | `mul` | Constant input → DW-Conv Engine; same-shape → Misc Engine; otherwise CPU |
| `concatv2` / `concatenate` | `concat` | Optimized on-chip memory allocation |
| `pad` / `zeropadding2d` | `pad` | CONSTANT(0) fused into adjacent ops; SYMMETRIC → DPU; REFLECT → CPU |
| `resizebilinear` | `resize` (BILINEAR) | DPU for align_corners=false, size=2,4,8; half_pixel_centers=true, size=2,4 |
| `resizenearestneighbor` | `resize` (NEAREST) | DPU when size is integer |
| `reshape`, `transpose`, `squeeze` | `reshape`, `transpose`, `squeeze` | Transformed to reshape or mapped to CPU |
| `softmax`, `sigmoid`, `exp` | `softmax`, `sigmoid`, `exp` | CPU only |
| `square + rsqrt + maximum` | `l2_normalize` | Fused into l2_normalize in XIR |

> **Note:** Operators marked with `*` are TensorFlow 2.x versions. All operators have CPU implementations.

---

## Operators Supported by PyTorch

| PyTorch API | XIR OP | DPU Implementation |
|-------------|--------|-------------------|
| `Conv2d` | `conv2d` (groups=1) / `depthwise-conv2d` (groups=ic) | Conv Engine or DW-Conv Engine. groups ≠ 1 and ≠ ic → CPU |
| `ConvTranspose2d` | `transposed-conv2d` / `depthwise-transposed-conv2d` | Conv or DW-Conv Engine. output_padding ≠ 0 → CPU |
| `matmul` | `conv2d` / `matmul` | Transformed to conv2d; falls back to CPU if transformation fails |
| `MaxPool2d` / `AdaptiveMaxPool2d` | `maxpool2d` | Pooling Engine |
| `AvgPool2d` / `AdaptiveAvgPool2d` | `avgpool2d` | Pooling Engine |
| `ReLU`, `LeakyReLU`, `ReLU6` | `relu`, `leakyrelu`, `relu6` | Fused into adjacent operations |
| `Hardtanh(0,6)` → `relu6` | `relu6` | Fused |
| `Hardsigmoid`, `Hardswish` | `hard-sigmoid`, `hardswish` | Fused |
| `ConstantPad2d` / `ZeroPad2d` | `pad` (CONSTANT) | Fused into adjacent ops or DPU when dim=4 |
| `add`, `sub`/`rsub`, `mul`, `neg` | `add`, `sub`, `mul`, `neg` | Element-wise add → DPU Add Engine; mul with constant → DW-Conv Engine |
| `sum`, `max`, `mean` | `reduction_sum`, `reduction_max`, `reduction_mean` | DPU or CPU depending on context |
| `interpolate` / `upsample` | `resize` | Same BILINEAR/NEAREST rules as TensorFlow |
| `transpose`, `permute`, `view`/`reshape`, `flatten`, `squeeze` | `transpose`, `reshape`, `flatten`, `squeeze` | Fused into load/save instructions or CPU |
| `cat` | `concat` | Optimized on-chip memory strategies |
| `aten::slice` | `strided_slice` | Removed if shape-related; otherwise CPU |
| `BatchNorm2d` | `depthwise-conv2d` / `scale` | Transformed to dw-conv if quantized equivalent exists; otherwise CPU |
| `softmax`, `Tanh`, `Sigmoid` | `softmax`, `tanh`, `sigmoid` | CPU only |
| `PixelShuffle` | `pixel_shuffle` (upscale=True) | Transformed to tile if convolution is input |
| `PixelUnshuffle` | `pixel_shuffle` (upscale=False) | Transformed to tile if convolution is input |

> **Note:** Python-syntax tensor slicing in PyTorch is transformed into `aten::slice`.

---

## VAI_C Usage

The compilers are: `vai_c_caffe`, `vai_c_tensorflow`, `vai_c_tensorflow2`, and `vai_c_xir`.

### Common Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--arch` | DPU architecture config file (JSON). For pre-built DPUs: `/opt/vitis_ai/compiler/arch`. Content: `{"target": "DPUCZDX8G_ISA0_B4096"}` or `{"fingerprint":"0x..."}`. The 64-bit fingerprint identifies the DPU: 1 byte DPU type, 1 byte ISA version, 6 bytes configuration. | Required |
| `--output_dir` / `-o` | Output directory for compiled models | Required |
| `--net_name` / `-n` | Name of the DPU kernel for the compiled network | Required |
| `--options` | Extra options as JSON key:value pairs. Highest priority — overrides other values. | — |

### Compiler-Specific Input Options

| Compiler | Input Flag | Input Format |
|----------|-----------|--------------|
| `vai_c_tensorflow` | `-f` | `.pb` file (quantize_eval_model.pb) |
| `vai_c_tensorflow2` | `-m` | `.h5` file (Keras functional API only) |
| `vai_c_xir` | `-x` | `.xmodel` file (from PyTorch NNDCT quantizer) |

### Extra Options (`--options`)

| Option Key | Value | Purpose |
|------------|-------|---------|
| `input_shape` | `"1,224,224,3"` | Specify input tensor shape manually |
| `plugins` | `"plugin0,plugin1"` | Custom accelerator plugin libraries |
| `output_ops` | `"op_name0,op_name1"` | Specify output operations |
| `prefetch` | `"true"` | Enable cross-layer prefetch |
| `hd_opt` | `"true"` | Enable special optimization for HD input |

### Usage Examples

```bash
# TensorFlow 1.x with input shape
vai_c_tensorflow \
  -f /PATH/TO/quantize_eval_model.pb \
  -a /PATH/TO/arch.json \
  -o /output \
  -n resnet50 \
  --options '{"input_shape": "1,224,224,3"}'

# TensorFlow 2.x
vai_c_tensorflow2 \
  -m /PATH/TO/quantized.h5 \
  -a /PATH/TO/arch.json \
  -o /output \
  -n resnet50

# PyTorch (via XIR)
vai_c_xir \
  -x /PATH/TO/quantized.xmodel \
  -a /PATH/TO/arch.json \
  -o /output \
  -n resnet50

# With custom plugins
vai_c_xir \
  -x /PATH/TO/quantized.xmodel \
  -a /PATH/TO/arch.json \
  -o /output \
  -n resnet50 \
  --options '{"plugins": "my_accel_plugin"}'
```

---

## Best Practices

1. **Always use the correct `arch.json`** for your target DPU — mismatches cause runtime failures (fingerprint verification).
2. **Check operator support** before compiling — use the Inspector tool ([Chapter 3](chapter03_quantizing_the_model.md)) to identify unsupported operators early.
3. **Specify `input_shape` explicitly** for TensorFlow models that lack shape information in the graph.
4. **Use `--options '{"prefetch": "true"}'`** to enable cross-layer prefetch for better throughput on supported architectures.
5. **Use `--options '{"hd_opt": "true"}'`** when working with high-definition input for optimized memory handling.
6. **Design custom plugins** for CPU-fallback operations that are performance-critical — leverage FPGA IPs via the Plugin pipeline.
7. **Review DPU constraints** (kernel size, stride, dilation, channel limits) to structure your model for maximum DPU coverage.
8. **Test with the compiler first** to see which operators fall back to CPU — the compiler reports this information.

---

## Quick Reference

| Task | Command |
|------|---------|
| Compile TF 1.x model | `vai_c_tensorflow -f model.pb -a arch.json -o out -n net` |
| Compile TF 2.x model | `vai_c_tensorflow2 -m model.h5 -a arch.json -o out -n net` |
| Compile PyTorch model | `vai_c_xir -x model.xmodel -a arch.json -o out -n net` |
| Set input shape | `--options '{"input_shape": "1,224,224,3"}'` |
| Use custom plugin | `--options '{"plugins": "libmyplugin"}'` |
| Enable prefetch | `--options '{"prefetch": "true"}'` |
| HD input optimization | `--options '{"hd_opt": "true"}'` |
| Find arch.json files | `/opt/vitis_ai/compiler/arch` (inside Docker) |

### See Also

- [Chapter 1 — Vitis AI Overview](chapter01_vitis_ai_overview.md)
- [Chapter 2 — Optimizing the Model](chapter02_optimizing_the_model.md) — pruning before compilation
- [Chapter 3 — Quantizing the Model](chapter03_quantizing_the_model.md) — quantization is prerequisite to compilation
- [Chapter 5 — Deploying and Running the Model](chapter05_deploying_and_running_the_model.md) — VART runtime uses compiled XMODEL
- [Chapter 6 — Profiling the Model](chapter06_profiling_the_model.md) — profile compiled model performance

---

## Source Attribution

- **Document:** UG1414 (v3.5) — Vitis AI User Guide
- **Date:** September 28, 2023
- **Chapter:** Chapter 4 — Compiling the Model (pp. 130–158)
