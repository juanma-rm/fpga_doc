# Chapter 3: Quantizing the Model

The Vitis AI Quantizer converts 32-bit floating-point weights and activations to fixed-point formats (INT8) to reduce computational complexity, memory bandwidth, and power consumption while preserving prediction accuracy. It supports TensorFlow 1.x, TensorFlow 2.x, PyTorch, and ONNX Runtime frameworks.

> **Note:** Vitis AI only performs signed quantization. It is highly recommended to apply standardization (zero mean, unit variance) so the DPU sees values within [-1.0, +1.0]. Using unsigned inputs [0.0, 1.0] results in loss of dynamic range.

---

## Table of Contents

| Section | Description |
|---|---|
| [Overview](#overview) | Quantization concepts and flow |
| [TF 1.x — vai_q_tensorflow](#tensorflow-1x-version-vai_q_tensorflow) | PTQ, QAT, dump, supported operations |
| [TF 2.x — vai_q_tensorflow2](#tensorflow-2x-version-vai_q_tensorflow2) | PTQ, QAT, inspector, custom layers, quantize strategies |
| [PyTorch — vai_q_pytorch](#pytorch-version-vai_q_pytorch) | PTQ, QAT, fast fine-tuning, inspector, BFP |
| [ONNX Runtime — vai_q_onnx](#onnx-runtime-version-vai_q_onnx) | PTQ for ONNX models |

---

## Overview

### Supported Frameworks and Features

| Framework | Versions | PTQ | QAT | Fast Fine-Tuning | Inspector |
|---|---|---|---|---|---|
| TensorFlow 1.x | 1.15 | Yes | Yes | Yes | No |
| TensorFlow 2.x | 2.3–2.12 | Yes | Yes | Yes | Yes |
| PyTorch | 1.2–1.13, 2.0 | Yes | Yes | Yes | Yes |
| ONNX Runtime | — | Yes | No | No | No |

### Quantization Methods

| Method | Description | Dataset | Duration |
|---|---|---|---|
| **Post-Training Quantization (PTQ)** | Calibrates with unlabeled images to find activation distributions | 100–1000 unlabeled images | Seconds to minutes |
| **Fast Fine-Tuning (AdaQuant)** | Calibrates activations + fine-tunes weights layer-by-layer | Small unlabeled dataset | Longer than PTQ, shorter than QAT |
| **Quantization Aware Training (QAT)** | Models quantization error in forward/backward passes during training | Full training dataset with labels | Minutes to hours |

> **Note:** Fast fine-tuning may produce different results each run. Use small learning rates for QAT.

### Quantizer Flow

1. **Input:** Float model + calibration dataset (100–1000 images)
2. **Pre-processing:** Fold batch-norms, remove inference-irrelevant nodes
3. **Inspect** (optional): Partition analysis showing DPU/CPU device assignments
4. **Quantize:** Weights/biases and activations to given bit width
5. **Output:** DPU-deployable model (deploy_model.pb / .xmodel / .h5)

### Key Concepts

- **fix_point parameter:** Number of fractional bits. For 8-bit signed with fix_point=7: Q0.7 (1 sign bit, 0 integer bits, 7 fractional bits). Convert: `float_value = int_value × 2^(-fix_point)`
- **Cross-Layer Equalization (CLE):** Improves calibration, especially for depthwise convolution networks
- **Quantization methods:**
  - **0 (Non-overflow):** No saturation; sensitive to outliers
  - **1 (Min-diffs):** Allows saturation; more robust to outliers
  - **2 (Min-diffs + depthwise):** Special strategy for depthwise weights

---

## TensorFlow 1.x Version (vai_q_tensorflow)

### Installation

```bash
# Docker
conda activate vitis-ai-tensorflow

# From source
sh build.sh
```

### Input Files

| File | Description |
|---|---|
| `frozen_graph.pb` | Floating-point frozen inference graph (not training graph) |
| Calibration dataset | 100–1000 images |
| `input_fn` | Python function for data pre-processing |

### Generating the Frozen Graph

```bash
freeze_graph \
    --input_graph /tmp/inception_v1_inf_graph.pb \
    --input_checkpoint /tmp/checkpoints/model.ckpt-1000 \
    --input_binary true \
    --output_graph /tmp/frozen_graph.pb \
    --output_node_names InceptionV1/Predictions/Reshape_1
```

> ⚠️ Ensure dropout and batch norm are in inference phase (e.g., `is_training=false`). For tf.keras, call `tf.keras.backend.set_learning_phase(0)` before building the graph.

### Inspect Model

```bash
vai_q_tensorflow inspect --input_frozen_graph=/tmp/inception_v1_inf_graph.pb
```

### Input Function Example

```python
# my_input_fn.py
def calib_input(iter):
    image = load_image(iter)
    preprocessed_image = do_preprocess(image)
    return {"placeholder_name": preprocessed_image}
```

### Post-Training Quantization

```bash
vai_q_tensorflow quantize \
    --input_frozen_graph frozen_graph.pb \
    --input_nodes ${input_nodes} \
    --input_shapes ${input_shapes} \
    --output_nodes ${output_nodes} \
    --input_fn my_input_fn.calib_input \
    [options]
```

### Output Files

| File | Description |
|---|---|
| `deploy_model.pb` | For Vitis AI compiler (DPUCZDX8G) |
| `quantize_eval_model.pb` | For evaluation and compiler input (DPUCAHX8H, DPUCADF8H) |

### Export to ONNX

```bash
vai_q_tensorflow quantize \
    --input_frozen_graph frozen_graph.pb \
    --input_nodes ${input_nodes} \
    --input_shapes ${input_shapes} \
    --output_nodes ${output_nodes} \
    --input_fn input_fn \
    --output_format onnx
```

### Dump Simulation Results

```bash
vai_q_tensorflow dump \
    --input_frozen_graph quantize_results/quantize_eval_model.pb \
    --input_fn dump_input_fn \
    --max_dump_batches 1 \
    --dump_float 0 \
    --output_dir quantize_results
```

### Quantization Aware Training (TF 1.x)

```python
# train.py
model = model_fn(is_training=True)

import vai_q_tensorflow
q_config = vai_q_tensorflow.QuantizeConfig(
    input_nodes=['net_in'],
    output_nodes=['net_out'],
    input_shapes=[[-1, 224, 224, 3]])

vai_q_tensorflow.CreateQuantizeTrainingGraph(config=q_config)

optimizer = tf.train.GradientDescentOptimizer()
# Start training...
```

```python
# eval.py
model = model_fn(is_training=False)

vai_q_tensorflow.CreateQuantizeEvaluationGraph(config=q_config)
vai_q_tensorflow.CreateQuantizeDeployGraph(
    checkpoint="path_to_checkpoint", config=q_config)
# Start evaluation...
```

> ⚠️ `CreateQuantizeTrainingGraph` and `CreateQuantizeEvaluationGraph` modify the default graph in-place. They must be called on different graph phases — never call Evaluation right after Training.

### QAT Tips

- For Keras: Set `backend.set_learning_phase(1)` before train graph, `set_learning_phase(0)` before eval graph
- **Disable dropout** before QAT — the tool does not support finetuning with dropouts
- Tune optimizer type and learning rate curve carefully

### Float16/BFloat16 Conversion

```bash
vai_q_tensorflow quantize \
    --input_frozen_graph frozen_graph.pb \
    --input_nodes ${input_nodes} \
    --input_shapes ${input_shapes} \
    --output_nodes ${output_nodes} \
    --input_fn input_fn \
    --convert_datatype 1  # 1=fp16, 2=double, 3=bf16, 4=fp32
```

### vai_q_tensorflow Options

| Option | Type | Default | Description |
|---|---|---|---|
| `--input_frozen_graph` | String | — | Frozen inference GraphDef file |
| `--input_nodes` | String | — | Input node names (comma separated) |
| `--output_nodes` | String | — | Output node names (comma separated) |
| `--input_shapes` | String | — | Shape list, 4-dim per node |
| `--input_fn` | String | — | `module_name.input_fn_name` |
| `--weight_bit` | Int | 8 | Bit width for weights/bias |
| `--activation_bit` | Int | 8 | Bit width for activations |
| `--method` | Int | 1 | 0=non-overflow, 1=min-diffs, 2=min-diffs+depthwise |
| `--calib_iter` | Int | 100 | Calibration iterations |
| `--ignore_nodes` | String | — | Nodes to skip during quantization |
| `--align_concat` | Int | 0 | 0=all, 1=output only, 2=disable |
| `--simulate_dpu` | Int | 1 | Enable DPU simulation |
| `--adjust_shift_bias` | Int | 1 | 0=disable, 1=static, 2=dynamic |
| `--adjust_shift_cut` | Int | 1 | 0=disable, 1=static |
| `--do_cle` | Int | 0 | Enable cross-layer equalization |
| `--replace_relu6` | Int | 1 | Replace ReLU6 with ReLU (with CLE) |
| `--replace_sigmoid` | Int | 0 | Replace sigmoid with hard-sigmoid |
| `--convert_datatype` | Int | 0 | 1=fp16,2=double,3=bf16,4=fp32 |
| `--output_format` | String | pb | pb or onnx |
| `--output_dir` | String | ./quantize_results | Output directory |
| `--gpu` | String | — | GPU device IDs |

### Supported Operations (TF 1.x)

| Type | Operations |
|---|---|
| Convolution | Conv2D, DepthwiseConv2dNative, Conv2DTranspose, SeparableConv2D |
| Fully Connected | MatMul, Dense |
| Pooling | AvgPool, MaxPool, Mean |
| Activation | ReLU, ReLU6, Sigmoid, Swish, Hard-sigmoid, Hard-swish, LeakyReLU |
| BatchNorm | FusedBatchNorm (Conv2D/DepthwiseConv2D/Dense + BN only) |
| Upsampling | ResizeBilinear, ResizeNearestNeighbor |
| Other | Concat, Pad, Squeeze, Reshape, Transpose, Softmax |

---

## TensorFlow 2.x Version (vai_q_tensorflow2)

### Installation

```bash
# Docker
conda activate vitis-ai-tensorflow2

# From source (wheel)
sh build.sh
pip install pkgs/*.whl

# From source (conda)
conda build vai_q_tensorflow2_gpu_feedstock --output-folder ./conda_pkg/
conda install --use-local ./conda_pkg/linux-64/*.tar.bz2
```

### Float Model Inspection

```python
from tensorflow_model_optimization.quantization.keras import vitis_inspect

inspector = vitis_inspect.VitisInspector(target="DPUCADF8H_ISA0")
inspector.inspect_model(model,
                        plot=True, plot_file="model.svg",
                        dump_results=True,
                        dump_results_file="inspect_results.txt",
                        verbose=0)
```

### Post-Training Quantization

```python
from tensorflow_model_optimization.quantization.keras import vitis_quantize

model = tf.keras.models.load_model('float_model.h5')
quantizer = vitis_quantize.VitisQuantizer(model)
quantized_model = quantizer.quantize_model(
    calib_dataset=calib_dataset,
    calib_steps=100,
    calib_batch_size=10)
quantized_model.save('quantized_model.h5')
```

### Fast Fine-Tuning

```python
quantized_model = quantizer.quantize_model(
    calib_dataset=calib_dataset,
    calib_steps=None,
    calib_batch_size=None,
    include_fast_ft=True,
    fast_ft_epochs=10)
```

### Export to ONNX

```python
quantized_model = quantizer.quantize_model(
    calib_dataset=calib_dataset,
    output_format='onnx',
    onnx_opset_version=11,
    output_dir='./quantize_results')
```

### Quantization Aware Training (TF 2.x)

```python
from tensorflow_model_optimization.quantization.keras import vitis_quantize

model = tf.keras.models.load_model('float_model.h5')
quantizer = vitis_quantize.VitisQuantizer(model)

# Get QAT model with PTQ initialization
qat_model = quantizer.get_qat_model(
    init_quant=True,
    calib_dataset=calib_dataset)

# Compile and train
qat_model.compile(optimizer=RMSprop(learning_rate=lr_schedule),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=[keras.metrics.SparseTopKCategoricalAccuracy()])
qat_model.fit(train_dataset)
qat_model.save('trained_model.h5')

# Convert to deployable model
quantized_model = quantizer.get_deploy_model(qat_model)
quantized_model.save('quantized_model.h5')
```

> **Note:** `pof2s_tqt` strategy should only be used in QAT with `init_quant=True` for best performance.

### Quantize Strategies

| Strategy | Description | Target |
|---|---|---|
| `pof2s` | Power-of-2 scale (default) | DPU |
| `pof2s_tqt` | Trained thresholds, QAT only | DPU |
| `fs` | Float scale, Conv/Dense inputs+weights | CPU/GPU |
| `fsx` | Float scale, more layer types | CPU/GPU |

> ⚠️ `fs` and `fsx` strategies cannot be deployed to DPU (no floating-point support).

### Custom Quantize Strategy

```python
quantizer = vitis_quantize.VitisQuantizer(model)
quantizer.dump_quantize_strategy(dump_file='my_strategy.json', verbose=2)
# Edit my_strategy.json...
quantizer.set_quantize_strategy(new_quantize_strategy='my_strategy.json')
quantized_model = quantizer.quantize_model(calib_dataset)
```

### Quantize Strategy Configuration (JSON)

```json
{
  "layer_type": "tensorflow.keras.layers.Conv2D",
  "quantizable_weights": ["kernel"],
  "weight_quantizers": [
    {"quantizer_type": "Pof2SQuantizer",
     "quantizer_params": {"bit_width": 8, "method": 0, "round_mode": 1,
                           "symmetry": true, "per_channel": true}}
  ],
  "quantizable_activations": ["activation"],
  "activation_quantizers": [
    {"quantizer_type": "FSQuantizer",
     "quantizer_params": {"bit_width": 8, "method": 2,
                           "method_percentile": 99.9999}}
  ]
}
```

### Custom Layer Quantization

```python
quantizer = vitis_quantize.VitisQuantizer(
    float_model,
    custom_objects={'MyCustomLayer': MyCustomLayer})
quantized_model = quantizer.quantize_model(
    calib_dataset=calib_dataset,
    add_shape_info=True)
```

### Float16/BFloat16 Conversion

```python
quantized_model = quantizer.quantize_model(convert_datatype='float16')
```

### Key kwargs for `quantize_model()`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input_layers` | list(str) | [] | Start layers for quantization |
| `output_layers` | list(str) | [] | End layers for quantization |
| `ignore_layers` | list(str) | [] | Layers to skip |
| `weight_bit` | int | 8 | Weight bit width |
| `activation_bit` | int | 8 | Activation bit width |
| `bias_bit` | int | 8 | Bias bit width |
| `weight_method` | int | 1 | 0=NonOverflow, 1=MinMSE, 2=MinKL, 3=Percentile |
| `activation_method` | int | 1 | Same options as weight_method |
| `weight_per_channel` | bool | False | Per-channel weight quantization |
| `include_fast_ft` | bool | False | Enable fast fine-tuning |
| `fast_ft_epochs` | int | — | Epochs per layer for fast fine-tuning |
| `fold_conv_bn` | bool | — | Fold BN into preceding Conv |
| `include_cle` | bool | — | Cross-layer equalization |
| `output_format` | str | '' | '', 'h5', 'tf', 'onnx' |

### Supported Layers (TF 2.x)

| Category | Layers | Notes |
|---|---|---|
| Core | InputLayer, Dense, Activation | relu/linear quantized; sigmoid→hard-sigmoid |
| Convolution | Conv2D, DepthwiseConv2D, Conv2DTranspose, SeparableConv2D | — |
| Pooling | AveragePooling2D, MaxPooling2D, GlobalAveragePooling | — |
| Normalization | BatchNormalization | Fused with prev conv; otherwise → depthwise conv |
| Reshaping | Reshape, Flatten, UpSampling2D, ZeroPadding2D | — |
| Merging | Concatenate, Add, Multiply | — |
| Activation | ReLU, Softmax, LeakyReLU (alpha=0.1 only), PReLU | — |

---

## PyTorch Version (vai_q_pytorch)

### Installation

```bash
# Docker
conda activate vitis-ai-pytorch

# From source
export CUDA_HOME=/usr/local/cuda  # GPU; unset for CPU
pip install torch==1.7.1 torchvision==0.8.2
pip install -r requirements.txt
cd pytorch_binding && python setup.py install
python -c "import pytorch_nndct"
```

### Float Model Inspection

```python
from pytorch_nndct.apis import Inspector

inspector = Inspector("DPUCAHX8L_ISA0_SP")  # or fingerprint
input = torch.randn([batch_size, 3, 224, 224])
inspector.inspect(model, input)
```

Output files in `./quantize_result/`:
- `inspect_{target}.txt` — Target info and operation details
- `inspect_{target}.svg` — Visualization
- `inspect_{target}.gv` — Dot source

### Model Requirements

1. Model must contain **only the `forward` method** — move pre/post-processing outside
2. Float model must pass **JIT trace test** (`torch.jit.trace`)

### Post-Training Quantization

```python
from pytorch_nndct.apis import torch_quantizer, dump_xmodel

input = torch.randn([batch_size, 3, 224, 224])
quantizer = torch_quantizer('calib', model, (input))
quant_model = quantizer.quant_model

# Forward for calibration
acc1, acc5, loss = evaluate(quant_model, val_loader, loss_fn)
quantizer.export_quant_config()
```

```bash
# Calibration
python resnet18_quant.py --quant_mode calib --subset_len 200

# Evaluate quantized model
python resnet18_quant.py --quant_mode test

# Deploy (batch_size=1 required)
python resnet18_quant.py --quant_mode test --subset_len 1 --batch_size=1 --deploy
```

Output files:
- `ResNet.py` — Converted model format
- `Quant_info.json` — Quantization steps
- `ResNet_int.xmodel` — XIR format for compiler
- `ResNet_int.onnx` — ONNX format
- `ResNet_int.pt` — TorchScript format

### Hardware-Aware Quantization

```bash
python resnet18_quant.py --quant_mode calib --target DPUCAHX8L_ISA0_SP
python resnet18_quant.py --quant_mode test --target DPUCAHX8L_ISA0_SP
```

### Module Partial Quantization

```python
from pytorch_nndct.nn import QuantStub, DeQuantStub

class WholeModule(torch.nn.Module):
    def __init__(self):
        self.subm0 = ...
        self.subm1 = ...
        self.quant = QuantStub()
        self.dequant = DeQuantStub()

    def forward(self, input):
        input = self.quant(input)       # start quantization
        output0 = self.subm0(input)
        output0 = self.dequant(output0) # end quantization
        output1 = self.subm1(output0)   # NOT quantized
        output1 = self.quant(output1)   # restart quantization
        output2 = self.subm2(output1)
        output2 = self.dequant(output2) # end quantization
        return output2
```

### Register Custom Operations

```python
from pytorch_nndct.utils import register_custom_op

@register_custom_op(op_type="MyOp", attrs_list=["scale_1", "scale_2"])
def custom_op(ctx, x, y, scale_1, scale_2):
    return scale_1 * x + scale_2 * y
```

### Fast Fine-Tuning

```python
if quant_mode == 'calib':
    quantizer.fast_finetune(evaluate, (quant_model, ft_loader, loss_fn))
elif quant_mode == 'test':
    quantizer.load_ft_param()
```

```bash
python resnet18_quant.py --quant_mode calib --fast_finetune
python resnet18_quant.py --quant_mode test --fast_finetune
```

### Quantization Aware Training (PyTorch)

**Model requirements for QAT:**

| Operation | Replacement |
|---|---|
| `+` | `pytorch_nndct.nn.modules.functional.Add` |
| `-` | `pytorch_nndct.nn.modules.functional.Sub` |
| `torch.add` | `pytorch_nndct.nn.modules.functional.Add` |
| `torch.sub` | `pytorch_nndct.nn.modules.functional.Sub` |

> ⚠️ A module to be quantized **cannot be called multiple times** in the forward pass.

**QAT Workflow:**

```python
from pytorch_nndct import QatProcessor

input = torch.randn([batch_size, 3, 224, 224])
qat_processor = QatProcessor(model, input, bitwidth=8)
quantized_model = qat_processor.trainable_model()

# Use separate LR for quantizer and network parameters
param_groups = [
    {'params': quantized_model.quantizer_parameters(), 'lr': 1e-2, 'name': 'quantizer'},
    {'params': quantized_model.non_quantizer_parameters(), 'lr': 1e-5, 'name': 'weight'}
]
optimizer = torch.optim.Adam(param_groups)

# Train...
# Get deployable model
deployable_model = qat_processor.to_deployable(quantized_model, output_dir)

# Export XMODEL (batch_size=1 required, CPU mode)
deployable_model.cpu()
for images, _ in subset_loader:
    deployable_model(images)
qat_processor.export_xmodel(output_dir)
```

> ⚠️ Avoid `torch.optim.SGD` for QAT — use `Adam` or `RMSprop`.

### Quantization Strategy Configuration (PyTorch)

```python
config_file = "./pytorch_quantize_config.json"
quantizer = torch_quantizer(quant_mode=quant_mode, module=model,
                            input_args=(input), device=device,
                            quant_config_file=config_file)
```

**Configuration hierarchy:** Default → Model config → Layer config (most specific wins)

**Key configuration parameters:**

| Parameter | Scope | Options | Default |
|---|---|---|---|
| `target_device` | Global | DPU, CPU, GPU | DPU |
| `data_type` | Tensor | int, bfloat16, float16, float32 | int |
| `bit_width` | Tensor | integer (for int type) | 8 |
| `method` | Tensor | maxmin, percentile, entropy, mse, diffs | diffs |
| `round_mode` | Tensor | half_even, half_up, half_down, std_round | std_round |
| `symmetry` | Tensor | true/false | true |
| `per_channel` | Tensor | true/false | false |
| `scale_type` | Tensor | float, poweroftwo | poweroftwo |

**DPU deployment restrictions:**

```
method: diffs or maxmin
round_mode: std_round (weights/bias/input), half_up (activation)
symmetry: true
per_channel: false
signed: true
narrow_range: true
scale_type: poweroftwo
calib_statistic_method: modal
```

### Block Floating Point (BFP)

```python
from pytorch_nndct import bfp
quantized_model = bfp.quantize_model(model, inputs, dtype='mx6')
```

> **Note:** BFP is experimental — quantized models cannot yet be deployed to hardware.

### vai_q_pytorch API Reference

#### `torch_quantizer`

```python
torch_quantizer(quant_mode, module, input_args, state_dict_file=None,
                output_dir="quantize_result", bitwidth=8,
                device=torch.device("cuda"), quant_config_file=None,
                target=None)
```

| Method | Description |
|---|---|
| `export_quant_config()` | Export quantization step information |
| `export_xmodel(output_dir, deploy_check)` | Export XMODEL for DPU |
| `export_onnx_model(output_dir, verbose, dynamic_batch, opset_version, native_onnx, dump_layers, check_model, opt_graph)` | Export ONNX model |
| `export_torch_script(output_dir, verbose)` | Export TorchScript model |
| `fast_finetune(eval_fn, args)` | Run fast fine-tuning |
| `load_ft_param()` | Load fast fine-tuned parameters |

#### `Inspector`

```python
Inspector(name_or_fingerprint)
inspector.inspect(module, input_args, device, output_dir, verbose_level, image_format)
```

#### `QatProcessor`

```python
QatProcessor(model, inputs, bitwidth=8)
qat_processor.trainable_model()
qat_processor.to_deployable(quantized_model, output_dir)
qat_processor.export_xmodel(output_dir)
```

---

## ONNX Runtime Version (vai_q_onnx)

### Installation

```bash
sh build.sh
pip install pkgs/*.whl
```

### Pre-Processing (Optional)

```python
from onnxruntime.quantization import shape_inference

shape_inference.quant_pre_process(
    input_model_path='model.onnx',
    output_model_path='model_preprocessed.onnx',
    skip_optimization=False,
    skip_onnx_shape=False,
    skip_symbolic_shape=False)
```

> **Note:** ONNX Runtime cannot output optimized models > 2 GB. Skip optimization for large models.

### Post-Training Quantization

```python
import vai_q_onnx

vai_q_onnx.quantize_static(
    model_input='model.onnx',
    model_output='quantized_model.onnx',
    calibration_data_reader=calibration_data_reader,
    quant_format=vai_q_onnx.VitisQuantFormat.FixNeuron,
    calibrate_method=vai_q_onnx.PowerOfTwoMethod.MinMSE,
    input_nodes=[],
    output_nodes=[])
```

### Quant Formats

| Format | Description |
|---|---|
| `QOperator` | Quantized operators directly |
| `QDQ` | QuantizeLinear/DeQuantizeLinear (8-bit only) |
| `VitisQuantFormat.QDQ` | VAI variants, more bit-widths |
| `VitisQuantFormat.FixNeuron` | FixNeuron composition (default) |

### Calibration Methods (DPU)

| Method | Description |
|---|---|
| `PowerOfTwoMethod.MinMSE` | Minimum MSE (default) |
| `PowerOfTwoMethod.NonOverflow` | No saturation |

### Dump Simulation Results

```python
vai_q_onnx.dump_model(
    model='quantized_model.onnx',
    dump_data_reader=dump_reader,
    output_dir='./dump_results',
    dump_float=False)
```

### Supported Operations (ONNX)

Conv, ConvTranspose, Gemm, BatchNorm (fused with Conv), Add, Concat, Relu, Reshape, Transpose, Squeeze, Resize, MaxPool, GlobalAveragePool, AveragePool, MatMul, Mul, Sigmoid, Softmax

### Key extra_options for `quantize_static()`

| Option | Default | Description |
|---|---|---|
| `ActivationSymmetric` | False | Must be True for PowerOfTwo |
| `WeightSymmetric` | True | Must be True for PowerOfTwo |
| `AddQDQPairToWeight` | False | Must be True for PowerOfTwo |
| `MatMulConstBOnly` | False | Only quantize MatMul with const B |
| `ForceQuantizeNoInputCheck` | False | Force quantize latent operators |

---

## Best Practices

1. **Start with PTQ** — it's fast and sufficient for most models. Try fast fine-tuning if accuracy drops. Use QAT only as a last resort.
2. **Use 100–1000 calibration images** — more is rarely better. Ensure they represent the actual data distribution.
3. **Inspect the model first** (TF2/PyTorch) to understand DPU/CPU partitioning before quantizing.
4. **Standardize inputs** to [-1.0, +1.0] range for optimal DPU dynamic range utilization.
5. **Set input/output nodes correctly** — exclude pre/post-processing subgraphs from quantization.
6. **For DPU deployment:** use power-of-2 scale, symmetric, per-tensor, signed quantization.
7. **Compare simulation results** using dump APIs to cross-check CPU/GPU vs. DPU outputs.
8. **Use batch_size=1** when exporting XMODEL for compilation.
9. **Disable dropout** before QAT in TF 1.x; use `remove_dropout` option in TF 2.x.
10. **For QAT:** Use small learning rates, Adam/RMSprop optimizer, and separate LR for quantizer vs. network parameters.

---

## Quick Reference

| Framework | Tool | PTQ Command / API | QAT Support | Output Formats |
|---|---|---|---|---|
| TF 1.x | `vai_q_tensorflow` | CLI: `vai_q_tensorflow quantize` | Yes (API) | .pb, .onnx |
| TF 2.x | `vai_q_tensorflow2` | API: `VitisQuantizer.quantize_model()` | Yes (API) | .h5, .tf, .onnx |
| PyTorch | `vai_q_pytorch` | API: `torch_quantizer()` | Yes (QatProcessor) | .xmodel, .onnx, .pt |
| ONNX RT | `vai_q_onnx` | API: `vai_q_onnx.quantize_static()` | No | .onnx |

---

> **Source:** UG1414 (v3.5) — Vitis AI User Guide, September 28, 2023, Chapter 3: Quantizing the Model (pp. 45–129)
