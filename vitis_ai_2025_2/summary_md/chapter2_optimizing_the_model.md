# Chapter 2: Optimizing the Model

The Vitis AI Optimizer provides the ability to optimize (prune) neural network models, removing redundant kernels to reduce overall computational cost for inference. Pruned models can then be quantized and deployed on AMD FPGA, SoC, or adaptive SoC devices. The Optimizer supports TensorFlow (1.15, 2.x) and PyTorch frameworks.

> **Note:** Vitis AI 2.5 and later releases do not support Caffe and Darknet. Use an earlier release for these frameworks.

---

## Table of Contents

| Section | Description |
|---|---|
| [Overview and Installation](#overview-and-installation) | Optimizer purpose and supported frameworks |
| [Pruning](#pruning) | Pruning concepts: fine-grained, coarse-grained, NAS |
| [TensorFlow 1.15 — vai_p_tensorflow](#tensorflow-115-version---vai_p_tensorflow) | TF1.15 iterative pruning API and workflow |
| [TensorFlow 2.x — vai_p_tensorflow2](#tensorflow-2x-version---vai_p_tensorflow2) | TF2.x iterative pruning API and workflow |
| [PyTorch — vai_p_pytorch](#pytorch-version---vai_p_pytorch) | PyTorch pruning: iterative, one-step, OFA |
| [API Reference](#api-reference) | Complete API for all frameworks |

---

## Overview and Installation

### Supported Frameworks and Tool Names

| Framework | Tool Name |
|---|---|
| TensorFlow 1.15 | `vai_p_tensorflow` |
| TensorFlow 2.x | `vai_p_tensorflow2` |
| PyTorch | `vai_p_pytorch` |

### Supported Frameworks and Features

| Framework | Versions | Iterative | One-Step | OFA |
|---|---|---|---|---|
| PyTorch | 1.4–1.13, 2.0 | Yes | Yes | Yes |
| TensorFlow 1.15 | 1.15 | Yes | No | No |
| TensorFlow 2.x | 2.4–2.12 | Yes | No | No |

---

## Pruning

Neural networks are typically over-parameterized with significant redundancy. **Pruning** eliminates redundant weights while keeping accuracy loss as low as possible. Three pruning categories exist:

### Pruning Methods Supported by DPU

| DPU IP | Fine-Grained | Coarse-Grained | NAS |
|---|---|---|---|
| DPUCZ | No | Yes | Yes |
| DPUCV | No | Yes | Yes |
| DPUCV2 | No | Yes | Yes |
| DPUCA | No | Yes | Yes |

### Fine-Grained Pruning

Sets individual weights with minimal effect on output to zero, producing **sparse matrices**. Requires hardware support for fine-grained sparsity (specialized weight-skipping hardware).

**Vitis AI sparsity pruner** implements N:M sparsity patterns:
- Prunes along input channel dimensions
- For each set of M weights, sets the N smallest to zero
- Typical M values: **4, 8, 16**; N = M/2 → **50% fine-grained sparsity**

**Supported sparsity combinations:**

| Activation Sparsity | Weight Sparsity Options |
|---|---|
| 0 | 0, 0.5, 0.75 |
| 0.5 | 0.75 only |

**Steps:** Generate sparse model → Fine-tune → Export sparse model

### Coarse-Grained Pruning (Channel Pruning)

Prunes entire **channels** (convolution kernels) rather than individual weights. Very hardware-friendly—works with any inference architecture. Lower achievable pruning ratio than fine-grained. Requires **fine-tuning** to recover accuracy.

> ⚠️ Depthwise convolution models (e.g., MobileNet-v2) experience dramatic accuracy drops even at low pruning rates with coarse-grained pruning.

Three coarse-grained pruning methods:

| Method | Workflow |
|---|---|
| **Iterative Pruning** | Analyze → Prune → Fine-tune → Repeat |
| **One-Step Pruning** | Search → Select best subnet → Fine-tune |
| **One-Shot NAS** | Train supernet → Search → Prune → Fine-tune |

### Iterative vs. One-Step Pruning Comparison

| Criteria | Iterative Pruning | One-Step Pruning |
|---|---|---|
| Prerequisites | None | BatchNormalization required |
| Time taken | More | Less |
| Retraining | Required | Required |
| Code organization | Evaluation function | Evaluation + Calibration functions |

### Iterative Pruning

Progressively trims model parameters across multiple iterations. Each iteration: prune → fine-tune → use result as new baseline.

> ⚠️ **IMPORTANT:** Parameters are progressively reduced at each iteration. Pruning with too high a ratio in a single pass causes irrecoverable accuracy loss.

**Four stages:**
1. **Analysis** — Sensitivity analysis to determine optimal pruning strategy
2. **Pruning** — Reduce computations in the input model
3. **Fine-tuning** — Retrain to recover accuracy
4. **Transformation** — Generate a dense model with fewer weights

### Recommendations for Better Pruning Results

1. Use as much data as possible for model analysis (ideally full validation set, minimum half).
2. Experiment with hyperparameters during fine-tuning (learning rate, decay policy); use the best result for the next iteration.
3. Fine-tuning data should be a subset of the original training dataset.
4. If accuracy doesn't improve sufficiently, reduce the pruning rate and re-run.

### Neural Architecture Search (NAS)

NAS discovers efficient network architectures in the design space that balance computational cost and accuracy. Uses a **Supernet** approach where multiple candidate subnetworks are assembled and trained simultaneously.

**Steps:** Train → Search → Prune → Fine-tune (optional)

### One-Step Pruning

Implements the **EagleEye** algorithm with **adaptive batch normalization** to evaluate pruned subnetworks without fine-tuning. Searches for subnetworks meeting the required model size and selects the most promising one.

**Steps:**
1. Search for subnetworks meeting the required pruning ratio
2. Select the best candidate via evaluation component
3. Fine-tune the pruned model

### Once-for-All (OFA)

A compression scheme based on One-Shot NAS. Designs a **once-for-all network** deployable under diverse architectural configurations, amortizing training costs.

**Key features:**
- Reduces model size across **depth, width, kernel size, and image resolution**
- Uses the original model as a **teacher** (knowledge distillation)
- Employs **adaptive soft KDLoss** and the **sandwich rule**
- Reduces training time by **half** compared to original OFA

### Pruning Method Selection (PyTorch)

Decision tree for selecting the right pruning method:

1. **Depthwise convolution layers present?**
   - **Yes** → Use **OFA**
   - **No** → Check for BatchNorm layers
2. **BatchNorm layers present?**
   - **Yes** → Use **One-Step Pruning**
   - **No** → Use **Iterative Pruning**

---

## TensorFlow (1.15) Version - vai_p_tensorflow

Requires creating a TensorFlow session with an initialized graph before pruning. Pruning operates in-place on the graph.

### Workflow

```python
# 1. Prepare baseline model
model = keras.Sequential([
    layers.InputLayer(input_shape=input_shape),
    layers.Conv2D(16, kernel_size=(3, 3), activation="relu"),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(num_classes),
])

# 2. Create TF session
with tf.Session() as sess:
    model, input_shape = mnist_convnet()
    sess.run(tf.global_variables_initializer())

    # 3. Create pruning runner
    from tf1_nndct.optimization.pruning import IterativePruningRunner
    input_specs = {'input_1:0': tf.TensorSpec(shape=(1, 28, 28, 1), dtype=tf.dtypes.float32)}
    pruner = IterativePruningRunner("mnist", sess, input_specs, ["dense/BiasAdd"])

    # 4. Define evaluation function
    def eval_fn(frozen_graph_def: tf.compat.v1.GraphDef) -> float:
        with tf.compat.v1.Session().as_default() as sess:
            tf.import_graph_def(frozen_graph_def, name="")
            # do evaluation here
            return 0.5

    # 5. Run model analysis
    pruner.ana(eval_fn, gpu_ids=['/GPU:0', '/GPU:1'])

    # 6. Prune with target sparsity
    shape_tensors, masks = pruner.prune(sparsity=0.5)

    # 7. Export frozen slim graph
    slim_graph_def = pruner.get_slim_graph_def(shape_tensors, masks)
```

> **Note:** `sparsity` is an approximate target; actual pruning ratio will not exactly equal this value.

---

## TensorFlow (2.x) Version - vai_p_tensorflow2

Supports only Keras models created by the **Functional API** or **Sequential API**. Subclassed models are **not supported**.

### Workflow

```python
# 1. Create model
model = keras.Sequential([
    keras.Input(shape=input_shape),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation="softmax"),
])

# 2. Create pruning runner
from tf_nndct.pruning import IterativePruningRunner
input_spec = tf.TensorSpec((1, *input_shape), tf.float32)
runner = IterativePruningRunner(model, input_spec)

# 3. Define evaluation function
def evaluate(model):
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    score = model.evaluate(x_test, y_test, verbose=0)
    return score[1]

# 4. Run analysis
runner.ana(evaluate)

# 5. Prune (returns sparse model)
sparse_model = runner.prune(ratio=0.2)

# 6. Fine-tune sparse model
sparse_model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
sparse_model.fit(x_train, y_train, batch_size=128, epochs=15, validation_split=0.1)
sparse_model.save_weights("model_sparse_0.2", save_format="tf")
```

> **Note:** When calling `save_weights`, use the `"tf"` format.

### Iterative Pruning Loop

```python
# Load previous checkpoint and increase ratio
model.load_weights("model_sparse_0.2")
runner = IterativePruningRunner(model, input_spec)
sparse_model = runner.prune(ratio=0.5)
# Fine-tune again...
```

### Getting the Final Pruned Model

```python
model.load_weights("model_sparse_0.5")
runner = IterativePruningRunner(model, input_spec)
slim_model = runner.get_slim_model()

# Or specify a particular spec file:
slim_model = runner.get_slim_model(".vai/mnist_ratio_0.5.spec")

# Save for inference or quantization
slim_model.save('/tmp/model')
```

---

## PyTorch Version - vai_p_pytorch

Provides three pruning methods: **Iterative**, **One-Step**, and **OFA**. The tool is a Python package (not an executable).

### Fine-Grained Pruning (PyTorch)

```python
from torchvision.models.resnet import resnet50
from pytorch_nndct import SparsePruner
import torch

# Create model and pruner
model = resnet50(pretrained=True)
inputs = torch.randn([1, 3, 224, 224], dtype=torch.float32)
pruner = SparsePruner(model, inputs)

# Generate sparse model (50% weight sparsity)
sparse_model = pruner.sparse_model(w_sparsity=0.5, a_sparsity=0, block_size=4)

# After retraining, export for inference
model = pruner.export_sparse_model(sparse_model)
```

### Coarse-Grained Iterative Pruning (PyTorch)

```python
from torchvision.models.resnet import resnet18
from pytorch_nndct import get_pruning_runner
import torch

model = resnet18(pretrained=True)
input_signature = torch.randn([1, 3, 224, 224], dtype=torch.float32)
runner = get_pruning_runner(model, input_signature, 'iterative')

# Define evaluation function
def eval_fn(model, dataloader):
    top1 = AverageMeter('Acc@1', ':6.2f')
    model.eval()
    with torch.no_grad():
        for i, (images, targets) in enumerate(dataloader):
            images = images.cuda()
            targets = targets.cuda()
            outputs = model(images)
            acc1, _ = accuracy(outputs, targets, topk=(1, 5))
            top1.update(acc1[0], images.size(0))
    return top1.avg

# Run analysis and prune
runner.ana(eval_fn, args=(val_loader,))
model = runner.prune(removal_ratio=0.2)
```

### One-Step Pruning (PyTorch)

```python
runner = get_pruning_runner(model, input_signature, 'one_step')

# Calibration function for adaptive BN
def calibration_fn(model, dataloader, number_forward=100):
    model.train()
    with torch.no_grad():
        for index, (images, target) in enumerate(dataloader):
            images = images.cuda()
            model(images)
            if index > number_forward:
                break

# Search and prune
runner.search(gpus=['0'], calibration_fn=calibration_fn,
              calib_args=(val_loader,), eval_fn=eval_fn,
              eval_args=(val_loader,), num_subnet=1000, removal_ratio=0.7)
model = runner.prune(removal_ratio=0.7, index=None)
```

**Advantages over iterative pruning:**
- Generated pruned models are typically more accurate
- Simpler workflow (one step, no iterations)
- Retraining a slim model is faster than retraining a sparse model

**Disadvantages:**
- Random generation of pruning strategies is unpredictable
- Subnetwork search must be repeated for each pruning ratio

### Retraining a Model (PyTorch)

```python
optimizer = torch.optim.Adam(model.parameters(), 1e-3, weight_decay=5e-4)
best_acc1 = 0
for epoch in range(args.epoches):
    train(train_loader, model, criterion, optimizer, epoch)
    acc1, acc5 = evaluate(val_loader, model, criterion)
    is_best = acc1 > best_acc1
    best_acc1 = max(acc1, best_acc1)
    if is_best:
        torch.save(model.state_dict(), 'model_pruned.pth')
        if hasattr(model, 'slim_state_dict'):
            torch.save(model.slim_state_dict(), 'model_slim.pth')
```

### Generating Final Pruned Model (PyTorch)

**Using Pruning API:**

```python
runner = get_pruning_runner(model, input_signature, method)
slim_model = runner.prune(removal_ratio=0.2, mode='slim')
slim_model.load_state_dict(torch.load('model_slim.pth'))
```

**Without Pruning API** (useful for quantization):

```python
from pytorch_nndct.utils import slim
model = create_your_baseline_model()
slim_model = slim.load_state_dict(model, torch.load('model_slim.pth'))
```

### Once-for-All (OFA) (PyTorch)

```python
from torchvision.models.mobilenet import mobilenet_v2
from pytorch_nndct import OFAPruner
import torch

# Create model and OFA pruner
model = mobilenet_v2(pretrained=True)
inputs = torch.randn([1, 3, 224, 224], dtype=torch.float32)
pruner = OFAPruner(model, inputs)

# Generate OFA model with pruning ratios
ofa_model = pruner.ofa_model([0.5, 0.75, 1], excludes=None, auto_add_excludes=True)
```

**Training with sandwich rule:**

```python
for i, (images, target) in enumerate(train_loader):
    images = images.cuda(non_blocking=True)
    target = target.cuda(non_blocking=True)
    optimizer.zero_grad()
    teacher_model.train()
    with torch.no_grad():
        soft_logits = teacher_model(images).detach()

    for arch_id in range(4):
        if arch_id == 0:
            model, _ = pruner.sample_subnet(ofa_model, 'max')
        elif arch_id == 1:
            model, _ = pruner.sample_subnet(ofa_model, 'min')
        else:
            model, _ = pruner.sample_subnet(ofa_model, 'random')
        output = model(images)
        loss = kd_loss(output, soft_logits) + cross_entropy_loss(output, target)
        loss.backward()
    torch.nn.utils.clip_grad_value_(ofa_model.parameters(), 1.0)
    optimizer.step()
    lr_scheduler.step()
```

**Evolutionary search for constrained subnetworks:**

```python
pareto_global = pruner.run_evolutionary_search(
    ofa_model, calibration_fn, (train_loader,),
    eval_fn, (val_loader,), 'acc1', 'max',
    min_macs=230, max_macs=250)
pruner.save_subnet_config(pareto_global, 'pareto_global.txt')

# Get static subnet for fine-tuning / quantization
pareto_global = pruner.load_subnet_config('pareto_global.txt')
static_subnet, config, flops, params = pruner.get_static_subnet(
    ofa_model, pareto_global['240']['subnet_setting'])
```

---

## API Reference

### `tf1_nndct.IterativePruningRunner` (TensorFlow 1.15)

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model_name: str`, `sess: SessionInterface`, `input_specs: Mapping[str, TensorSpec]`, `output_node_names: List[str]`, `excludes: List[str]=[]` | Instance |
| `ana` | `eval_fn: Callable[[GraphDef], float]`, `gpu_ids: List[str]=['/GPU:0']`, `checkpoint_interval: int=10` | None |
| `prune` | `sparsity: float=None`, `threshold: float=None`, `max_attemp: int=10` | `(shape_tensors, masks)` |
| `get_slim_graph_def` | `shape_tensors`, `masks` | Frozen slim `GraphDef` |

**Prune modes:** FLOPs-based (`sparsity`) or accuracy-based (`threshold`). `sparsity` takes priority.

### `tf_nndct.IterativePruningRunner` (TensorFlow 2.x)

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model: keras.Model`, `input_specs: TensorSpec` | Instance |
| `ana` | `eval_fn`, `excludes=None`, `forced=False` | None |
| `prune` | `ratio=None`, `threshold=None`, `spec_path=None`, `excludes=None`, `mode='sparse'` | Sparse model |
| `get_slim_model` | `spec_path=None` | Slim model |

### `pytorch_nndct.SparsePruner` (Fine-Grained)

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model: nn.Module`, `inputs: Tensor` | Instance |
| `sparse_model` | `w_sparsity=0.5`, `a_sparsity=0`, `block_size=16`, `excludes=None` | Sparse model |
| `export_sparse_model` | `model` | Inference-ready model |

### `pytorch_nndct.IterativePruningRunner` (Coarse-Grained)

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model: nn.Module`, `inputs: Tensor` | Instance |
| `ana` | `eval_fn`, `args=()`, `gpus=None`, `excludes=None`, `forced=False` | None |
| `prune` | `removal_ratio=None`, `threshold=None`, `spec_path=None`, `excludes=None`, `mode='sparse'` | Pruned model |

### `pytorch_nndct.OneStepPruningRunner`

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model: nn.Module`, `inputs: Tensor` | Instance |
| `search` | `gpus=['0']`, `calibration_fn=None`, `calib_args=()`, `num_subnet=10`, `removal_ratio=0.5`, `excludes=[]`, `eval_fn=None`, `eval_args=()` | None |
| `prune` | `mode='slim'`, `index=None`, `removal_ratio=None`, `pruning_info_path=None` | Slim model |

### `pytorch_nndct.OFAPruner`

| Method | Parameters | Returns |
|---|---|---|
| `__init__` | `model: nn.Module`, `inputs: Tensor` | Instance |
| `ofa_model` | `expand_ratio: list`, `channel_divisible=8`, `excludes=None`, `auto_add_excludes=True`, `save_search_space=False` | OFA model |
| `sample_subnet` | `model`, `mode: ['random','max','min']` | `(subnet, config)` |
| `reset_bn_running_stats_for_calibration` | `model` | None |
| `run_evolutionary_search` | `model`, `calibration_fn`, `calib_args`, `eval_fn`, `eval_args`, `evaluation_metric`, `min_or_max_metric`, `min_macs`, `max_macs`, `macs_step=10`, `parent_popu_size=16`, `iteration=10`, `mutate_size=8`, `mutate_prob=0.2`, `crossover_size=4` | Pareto config |
| `save_subnet_config` | `setting_config`, `file_name` | None |
| `load_subnet_config` | `file_name` | Config dict |
| `get_static_subnet` | `model`, `subnet_setting` | `(subnet, config, flops, params)` |

---

## Best Practices

1. **Select the right pruning method** using the decision tree: OFA for depthwise convolutions, one-step for BatchNorm networks, iterative otherwise.
2. **Use iterative pruning progressively** with modest ratios per step—never prune too aggressively in a single iteration.
3. **Use as much validation data as possible** for model analysis (at least half the validation set).
4. **Experiment with learning rate and decay** during fine-tuning for each pruning iteration.
5. **Save both sparse and slim checkpoints** during retraining to enable flexible model recovery.
6. **Always fine-tune after pruning** to recover accuracy before the next iteration or deployment.
7. **For TF 2.x, save weights in `"tf"` format** when using iterative pruning.
8. **OFA requires longer training** and higher skill but achieves the best compression across all convolution types.

---

## Quick Reference

| Framework | Tool | Methods Available |
|---|---|---|
| TF 1.15 | `vai_p_tensorflow` | Iterative |
| TF 2.x | `vai_p_tensorflow2` | Iterative |
| PyTorch | `vai_p_pytorch` | Iterative, One-Step, OFA, Fine-Grained Sparse |

| Pruning Type | Compression | Hardware Friendly | Best For |
|---|---|---|---|
| Fine-grained | High (N:M sparsity) | Requires specialized HW | Models with sparsity support |
| Coarse-grained (Iterative) | Moderate | Yes (any architecture) | VGGNet, models without BN |
| Coarse-grained (One-Step) | Moderate–High | Yes | Models with BatchNorm |
| OFA | Highest | Yes | MobileNet, depthwise conv models |

---

> **Source:** UG1414 (v3.5) — Vitis AI User Guide, September 28, 2023, Chapter 2: Optimizing the Model (pp. 14–44)
