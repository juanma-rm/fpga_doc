# Chapter 1: Vitis AI Overview

The AMD Vitis AI development environment accelerates AI inference on AMD hardware platforms, including edge devices and AMD Versal accelerator cards. It provides optimized IP cores, tools, libraries, models, and example designs that abstract FPGA complexity and enable developers to build deep-learning inference applications without extensive FPGA knowledge.

> **Note:** Caffe support has been deprecated for releases ≥ 2.5. For Caffe support, see the Vitis AI 2.0 User Guide.

---

## Table of Contents

| Section | Description |
|---|---|
| [Navigating Content by Design Process](#navigating-content-by-design-process) | How documentation maps to the ML design flow |
| [Features](#features) | Key capabilities of Vitis AI |
| [Vitis AI Tools Overview](#vitis-ai-tools-overview) | Summary of all tools in the framework |
| [Vitis AI Containers](#vitis-ai-containers) | Docker-based distribution of AI software |
| [Minimum System Requirements](#minimum-system-requirements) | Hardware/software prerequisites |

---

## Navigating Content by Design Process

AMD documentation is organized around a standard **Machine Learning and Data Science** design process: importing a model from PyTorch, TensorFlow, or another framework into Vitis AI, then optimizing and evaluating its effectiveness. The end-to-end flow maps directly to this guide's chapters:

1. **Optimize** — [Chapter 2: Optimizing the Model](chapter2_optimizing_the_model.md)
2. **Quantize** — [Chapter 3: Quantizing the Model](chapter3_quantizing_the_model.md)
3. **Compile** — [Chapter 4: Compiling the Model](chapter4_compiling_the_model.md)
4. **Deploy & Run** — [Chapter 5: Deploying and Running the Model](chapter5_deploying_and_running_the_model.md)
5. **Profile** — [Chapter 6: Profiling the Model](chapter6_profiling_the_model.md)

---

## Features

Vitis AI includes the following capabilities:

- **Framework support** — Supports mainstream frameworks (PyTorch, TensorFlow 1.x/2.x, ONNX) and the latest models for diverse deep-learning tasks.
- **Pre-optimized models** — Provides a comprehensive set of pre-optimized models ready to deploy on AMD devices via the Model Zoo.
- **Quantization** — A powerful quantizer supporting model quantization, calibration, and fine-tuning (FP32 → INT8).
- **Pruning** — An optional AI Optimizer that can prune a model by up to **90%** with tolerable accuracy loss.
- **Profiling** — Layer-by-layer analysis to help identify bottlenecks.
- **Unified APIs** — High-level C++ and Python APIs for maximum portability from Edge to Data Center.
- **Scalable IP** — Customizable, efficient DPU IP cores optimized for throughput, latency, and power.

---

## Vitis AI Tools Overview

### Vitis AI Model Zoo

A curated collection of finely tuned deep learning models designed to accelerate AI inference deployment on AMD platforms. Covers applications including ADAS/AD, video surveillance, robotics, and data centers.

- Source: [Vitis AI Model Zoo on GitHub](https://github.com/Xilinx/Vitis-AI/tree/master/model_zoo)

### Vitis AI Optimizer

Applies world-leading model compression technology to achieve **5× to 50× reduction** in model complexity with minimal accuracy degradation. Supports pruning across TensorFlow (1.15, 2.x) and PyTorch frameworks.

- See: [Chapter 2: Optimizing the Model](chapter2_optimizing_the_model.md)

### Vitis AI Quantizer

Converts 32-bit floating-point weights and activations to fixed-point formats (e.g., **INT8**), significantly reducing computational complexity while preserving prediction accuracy. The resulting fixed-point model requires less memory bandwidth, enabling faster speed and improved power efficiency.

- See: [Chapter 3: Quantizing the Model](chapter3_quantizing_the_model.md)

### Vitis AI Compiler

Maps the AI model to a highly efficient instruction set and dataflow model. Performs sophisticated optimizations including:

- **Layer fusion**
- **Instruction scheduling**
- **On-chip memory reuse**

- See: [Chapter 4: Compiling the Model](chapter4_compiling_the_model.md)

### Vitis AI Profiler

Analyzes and visualizes AI applications to identify bottlenecks and optimally allocate computing resources across CPU, DPU, and memory. Key characteristics:

- **No code changes required**
- Traces function calls and runtime
- Collects hardware utilization metrics (CPU, DPU, memory)

- See: [Chapter 6: Profiling the Model](chapter6_profiling_the_model.md)

### Vitis AI Library

A collection of high-level libraries and APIs for efficient AI inference with DPUs. Built upon the Vitis AI Runtime with unified APIs and integrates with Xilinx Runtime (XRT).

**Library architecture stack** (top to bottom):

| Layer | Components |
|---|---|
| Demo & Samples | Application examples |
| Algorithm Libraries | classification, SSD, face, segmentation, YOLO, roadline |
| Base Libraries | `cpu_task`, `dpu_task`, `xnnpp` |
| Vitis Runtime Unified APIs | High-level inference API |
| Vitis Runtime Implementation | Backend implementation |
| XRT | Required for Vitis designs only |
| DPU | Deep Learning Processing Unit |

- Reference: Vitis AI Library User Guide (UG1354)

### Vitis AI Runtime (VART)

Provides a unified high-level runtime API for seamless Data Center-to-Edge deployments. Uses **XIR** (AMD Intermediate Representation) internally to represent neural network operators.

**Key features:**

- Asynchronous job submission to the accelerator
- Asynchronous job collection from the accelerator
- C++ and Python implementations
- Multi-threading and multi-process execution support

- See: [Chapter 5: Deploying and Running the Model](chapter5_deploying_and_running_the_model.md)

---

## Vitis AI Containers

The Vitis AI 3.5 release uses **Docker containers** to distribute AI software. The release consists of:

- **Tools Container** — distributed through Docker Hub
- **Examples** — on the public GitHub repository
- **Vitis AI Model Zoo**

### Tools Container Contents

| Component | Details |
|---|---|
| Distribution | Docker Hub |
| Unified Compiler Flow | DPUCZDX8G (Edge), DPUCVDX8G (Edge), DPUCV2DX8G (Edge & Data Center) |
| Conda Environments | `vitis-ai-tensorflow`, `vitis-ai-tensorflow2`, `vitis-ai-pytorch` |
| WeGO Workflow | `vitis-ai-wego-torch` (PyTorch) |
| Versal Runtime Tools | Included |

### Conda Activation Commands

```bash
conda activate vitis-ai-tensorflow     # TensorFlow 1.x flows
conda activate vitis-ai-tensorflow2    # TensorFlow 2.x flows
conda activate vitis-ai-pytorch        # PyTorch flows
conda activate vitis-ai-wego-torch     # WeGO workflow (PyTorch)
```

---

## Minimum System Requirements

Refer to the official system requirements page:
https://xilinx.github.io/Vitis-AI/3.5/html/docs/reference/system_requirements.html

---

## Best Practices

1. **Start with pre-optimized models** from the Model Zoo before training custom models to accelerate your development cycle.
2. **Follow the sequential design flow**: Optimize → Quantize → Compile → Deploy → Profile.
3. **Use Docker containers** for a consistent and reproducible development environment.
4. **Select the correct conda environment** matching your framework before running any tools.
5. **Profile early and often** to identify bottlenecks between CPU and DPU execution.

---

## Quick Reference

| Tool | Purpose | Key Benefit |
|---|---|---|
| Model Zoo | Pre-trained models | Accelerated deployment |
| Optimizer | Model pruning | Up to 50× complexity reduction |
| Quantizer | FP32 → INT8 conversion | Less bandwidth, faster inference |
| Compiler | Model-to-instruction mapping | Layer fusion, memory optimization |
| Profiler | Performance analysis | No-code-change bottleneck detection |
| Library | High-level inference APIs | Simplified DPU programming |
| Runtime (VART) | Unified runtime API | Edge-to-Data-Center portability |

---

> **Source:** UG1414 (v3.5) — Vitis AI User Guide, September 28, 2023, Chapter 1: Vitis AI Overview (pp. 4–13)
