# Chapter 6 — Profiling the Model

The Vitis AI Profiler is an application-level tool for profiling and visualizing AI inference pipelines based on VART. It requires no code changes or recompilation, and combines CPU and DPU execution states into a unified view using Vitis Analyzer.

---

## Table of Contents

| Item | Description |
|------|-------------|
| [Vitis AI Profiler Architecture](#vitis-ai-profiler-architecture) | Components: vaitrace, VART, XRT, Vitis Analyzer |
| [GUI Overview](#gui-overview) | DPU Summary, Throughput/DDR rates, Timeline Trace |
| [System Requirements](#system-requirements) | Hardware and software requirements |
| [Installing the Profiler](#installing-the-profiler) | PetaLinux kernel configuration and vaitrace installation |
| [Starting a Trace](#starting-a-trace) | Tracing C++ and Python VART programs |
| [vaitrace Usage](#vaitrace-usage) | Command-line arguments and configuration file |
| [Text Summary](#text-summary) | ASCII table output with DPU performance metrics |

---

## Vitis AI Profiler Architecture

The profiler consists of:

1. **vaitrace (VAITracer)** — Runs on the target device, instruments the AI program via VART and XRT
2. **Vitis Analyzer** — Runs on PC/server, opens `.csv` and `run_summary` files for visualization

Supported targets:
- AMD Zynq UltraScale+ MPSoC
- AMD Versal adaptive SoC
- Alveo HBM platforms

### Key Capabilities

- **No code changes required** — just prefix the command with `vaitrace`
- **Visualize system bottlenecks** — CPU vs. DPU execution overlap
- **DPU summary** — run count, min/avg/max execution times per kernel
- **Throughput graphs** — FPS and DDR read/write transfer rates (Mbps)
- **Timeline trace** — timed events from VART, HAL APIs, and DPUs

---

## GUI Overview

The Vitis Analyzer (2020.2+) displays three main views:

| View | Content |
|------|---------|
| **DPU Summary** | Table: number of runs, min/avg/max times (ms) per kernel |
| **DPU Throughput & DDR Transfer Rates** | Line graphs of FPS and read/write bandwidth (Mbps) |
| **Timeline Trace** | Timed events from VART, HAL APIs, and DPU instances |

---

## System Requirements

### Hardware

| Platform | DPU |
|----------|-----|
| AMD Zynq UltraScale+ MPSoC | DPUCZDX8G |
| AMD Versal adaptive SoC | DPUCVDX8G / DPUCVDX8H |

### Software

- VART v1.2 or later

---

## Installing the Profiler

### PetaLinux Kernel Configuration

```bash
petalinux-config -c kernel
```

Enable:
- `General architecture-dependent options` → `[*] Kprobes`
- `Kernel hacking` → `[*] Tracers`
- `Kernel hacking` → `Tracers`:
  - `[*] Kernel Function Tracer`
  - `[*] Enable kprobes-based dynamic events`
  - `[*] Enable uprobes-based dynamic events`

### Root Filesystem Configuration

```bash
petalinux-config -c rootfs
```

Enable: `Petalinux Package Groups` → `packagegroup-petalinux-self-hosted` → `[*] packagegroup-petalinux-self-hosted`

Then build:

```bash
petalinux-build
```

### Profiler Binary

`vaitrace` is integrated into the VART runtime. If VART is installed, `vaitrace` is located at `/usr/bin/vaitrace`.

---

## Starting a Trace

### C++ Programs

Prefix the program command with `vaitrace`:

```bash
cd ~/Vitis_AI/examples/vai_runtime/resnet50
vaitrace ./resnet50 /usr/share/vitis_ai_library/models/resnet50/resnet50.xmodel
```

### Python Programs

Use the `-m vaitrace_py` module flag:

```bash
cd ~/Vitis_AI/examples/vai_runtime/resnet50_mt_py
python3 -m vaitrace_py ./resnet50.py 2 /usr/share/vitis_ai_library/models/resnet50/resnet50.xmodel
```

### Viewing Results

1. Copy all `.csv` files and `xclbin.ex.run_summary` to your host system
2. Open with Vitis Analyzer:
   - **CLI:** `vitis_analyzer xclbin.ex.run_summary`
   - **GUI:** File → Open Summary → select the `run_summary` file

---

## vaitrace Usage

### Command Line

```
vaitrace [-h] [-c CONFIG] [-d] [-o TRACESAVETO] [-t TIMEOUT] [-v]
         [-b] [-p] [--va] [--xat] [--txt_summary] [--fine_grained]
         cmd
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `cmd` | Executable AI program with its arguments | Required |
| `-t TIMEOUT` | Tracing time in seconds from program launch | 30 |
| `-c CONFIG` | JSON configuration file path | — |
| `-o TRACESAVETO` | Report output location (text summary mode only) | STDOUT |
| `--va` | Generate trace data for Vitis Analyzer | Enabled by default |
| `--txt_summary` / `--txt` | Output ASCII text summary (incompatible with `--va`) | — |
| `--fine_grained` | Fine-grained mode (mass trace data, limited to 10s) | — |
| `-d` | Enable debug mode | — |
| `-v` | Show version | — |
| `-b` | Bypass vaitrace (just run the command) | — |
| `-p` | Trace Python application | — |
| `--xat` | Save raw data for debug | — |

> `--va` and `--txt_summary` are mutually exclusive.

### Configuration File

Use `-c trace_cfg.json` for persistent trace options. **Priority:** Configuration File > Command Line > Default.

```json
{
    "trace": {
        "enable_trace_list": ["vitis-ai-library", "vart", "custom"]
    },
    "trace_custom": []
}
```

| Key | Type | Description |
|-----|------|-------------|
| `trace.enable_trace_list` | list | Built-in trace functions: `"vitis-ai-library"`, `"vart"`, `"opencv"`, `"custom"` |
| `trace_custom` | list | User-implemented functions to trace (supports namespaces) |

---

## Text Summary

When using `--txt` or `--txt_summary`, vaitrace prints an ASCII table with per-subgraph DPU performance metrics:

| Field | Unit | Description |
|-------|------|-------------|
| **DPU Id** | — | Name of the DPU instance |
| **Bat** | — | Batch size of the DPU instance |
| **SubGraph** | — | Name of subgraph in the XMODEL |
| **WL (Workload)** | GOP | Computation workload (MAC = 2 operations) |
| **RT (Runtime)** | ms | Subgraph execution time |
| **Perf** | GOP/s | DPU performance |
| **LdFM** | MB | External memory load size — feature map |
| **LdWB** | MB | External memory load size — weights and bias |
| **StFM** | MB | External memory store size — feature map |
| **AvgBw** | — | Average DDR bandwidth = (total load + total store) / runtime |

---

## Best Practices

1. **Start with `--txt_summary`** for quick performance overview before switching to Vitis Analyzer for detailed analysis.
2. **Use `-t` to control trace duration** — longer traces generate more data but give more representative results.
3. **Use fine-grained mode** (`--fine_grained`) only when you need per-instruction-level detail — it generates massive trace data.
4. **Configure PetaLinux kernel** with Kprobes and Tracers enabled before attempting to use vaitrace on Zynq platforms.
5. **Use the configuration file** (`-c`) for reproducible profiling setups across multiple runs.
6. **Check AvgBw** to identify memory-bound vs. compute-bound subgraphs.
7. **Profile with `DEEPHI_PROFILING=1`** for custom OP profiling (see [Chapter 5](chapter5_deploying_and_running_the_model.md)).

---

## Quick Reference

| Task | Command |
|------|---------|
| Trace C++ program | `vaitrace ./program model.xmodel` |
| Trace Python program | `python3 -m vaitrace_py ./script.py model.xmodel` |
| Text summary | `vaitrace --txt_summary ./program model.xmodel` |
| With timeout | `vaitrace -t 60 ./program model.xmodel` |
| With config file | `vaitrace -c trace_cfg.json ./program model.xmodel` |
| Fine-grained trace | `vaitrace --fine_grained ./program model.xmodel` |
| Open in Vitis Analyzer | `vitis_analyzer xclbin.ex.run_summary` |

### See Also

- [Chapter 1 — Vitis AI Overview](chapter1_vitis_ai_overview.md) — Profiler in the Vitis AI tool chain
- [Chapter 4 — Compiling the Model](chapter4_compiling_the_model.md) — compiled XMODEL is what gets profiled
- [Chapter 5 — Deploying and Running the Model](chapter5_deploying_and_running_the_model.md) — VART runtime and custom OP profiling
- [DPU Profiling Examples on GitHub](https://github.com/Xilinx/Vitis-AI)

---

## Source Attribution

- **Document:** UG1414 (v3.5) — Vitis AI User Guide
- **Date:** September 28, 2023
- **Chapter:** Chapter 6 — Profiling the Model (pp. 218–225)
