# Section I — Introduction to Vitis HLS
**UG1399 v2025.2 · Vitis HLS User Guide**

---

## Table of Contents
0. [Navigating Content by Design Process](#navigating-content-by-design-process)
1. [What is High-Level Synthesis?](#1-what-is-high-level-synthesis)
2. [Supported Operating Systems & Licensing](#2-supported-operating-systems--licensing)
3. [Changed Behavior in v2025.2](#3-changed-behavior-in-v20252)
4. [Benefits of HLS](#4-benefits-of-hls)
5. [Introduction to Vitis HLS Components](#5-introduction-to-vitis-hls-components)
6. [Key Synthesis Concepts](#6-key-synthesis-concepts)
7. [Refactoring C++ Source Code for HLS](#7-refactoring-c-source-code-for-hls)
8. [Re-Architecting the Hardware Module](#8-re-architecting-the-hardware-module)
9. [Best Practices](#9-best-practices)
10. [Tutorials and Examples](#10-tutorials-and-examples)

---

## Navigating Content by Design Process

AMD documentation is organized around standard design processes accessible via the **Design Hubs** page and the **Design Flow Assistant**. This document covers the following design processes:

| Design Process | Topics in This Document |
|---|---|
| **Hardware, IP, and Platform Development** | Launching the Vitis Unified IDE, Running C Simulation, Running C Synthesis, Running C/RTL Co-Simulation |

---

## 1. What is High-Level Synthesis?

**High-Level Synthesis (HLS)** is an automated design process that takes an **abstract behavioral specification** of a digital system written in C/C++ and generates a **Register-Transfer Level (RTL)** structure that realizes the same behavior.

### Typical HLS Design Flow

```
C/C++ Algorithm
      │
      ▼
C-Simulation  ──►  Functional Verification (behavioral level)
      │
      ▼
C-Synthesis   ──►  RTL Generation (v++ compiler)
      │
      ▼
C/RTL Co-Sim  ──►  RTL Verification with original C testbench
      │
      ▼
Package/Export──►  Vivado IP  or  Vitis Kernel (.xo)
```

### The Core "Why"

| Traditional RTL | HLS Approach |
|---|---|
| Designer specifies both macro- and micro-architecture | Designer specifies only the **macro-architecture** |
| State machine, datapath, pipelines — all manual | State machine, pipelines, datapaths inferred by the tool |
| Tied to a specific clock period / technology node | Technology-agnostic; re-target by changing constraints |
| Changing a derivative product requires a new RTL project | Constraints change; source code stays the same |

> **Key insight:** HLS requires the designer to think carefully about **design intent** (how the algorithm interacts with the outside world) while leaving micro-architecture decisions — state machines, register pipelines, datapaths — to the compiler.

---

## 2. Supported Operating Systems & Licensing

### Supported OS (x86 / x86-64)

| Platform | Versions |
|---|---|
| Red Hat / CentOS | 7.9, 8.5, 8.6, 8.7, 8.8, 9.0, 9.1, 9.2, 9.3 |
| Ubuntu LTS | 20.04.4/5/6, 22.04, 22.04.1/2/3 |
| Amazon Linux 2 | AL2 LTS |
| Windows 10 (64-bit) | 21H2, 22H2 |
| Windows 11 (64-bit) | 21H2, 22H2 |
| Windows Server | 2022 |

> **Note (Ubuntu 20.04):** May require `libtinfo.so.5` — see AMD AR #76616.

### Licensing

The **Vitis HLS License** is required to access reporting features such as the **Code Analyzer** and the **Dataflow viewer** inside the Vitis unified IDE.

**License acquisition steps:**
1. Go to `https://www.xilinx.com/getlicense` and sign in with your AMD account.
2. Navigate to the **Product Licensing** page and select an account.
3. Under **Create New Licenses**, enable the *Vitis HLS License* checkbox.
4. Select **Generate Floating License** (specify requested seats) or **Generate Node-Locked License** (seats = 1).
5. Specify a host under **System Information**. Supported host types:

| Host Type | Notes |
|---|---|
| Dongle Flex ID | Hardware dongle |
| Disk Serial Number | Windows: `vol c:` in cmd prompt |
| Ethernet MAC | Windows: `ipconfig /all` → Physical Address |
| Solaris hostid | Solaris systems |

6. Review and submit — a license file is delivered by email.

For usage of the `.lic` file, refer to *Vivado Design Suite User Guide: Release Notes, Installation, and Licensing (UG973)*.

---

## 3. Changed Behavior in v2025.2

### Vitis Unified IDE

| Change | Details |
|---|---|
| Workspace metadata reorganization | New file `_ide/.wsdata/version.ini` labels workspace version. Opening older workspaces prompts an update. Files that can be regenerated are separated into `.wsdata` for easier source control integration. |
| Python journal renamed | `builder.py` (previously in `logs/`) → `workspace_journal.py` (moved to `_ide/`). Accessible from menu: **Vitis → Workspace Journal**. |
| Build settings | Application component source compilation settings now managed in `UserConfig.cmake` instead of being auto-configured by the IDE. |
| Process name | Changed from `Vitisng-ide` to `Vitis-ide`. |
| Explorer view | User-managed flow extended to **Vitis Explorer** view, providing consistent flow window support for both GUI-managed and user-managed flows. |

### Vitis Accelerated Software Development

| Change | Details |
|---|---|
| VCK190 Base Platform | Now initiates designs using the **Vivado Customizable Example Design (CED)** Vitis Extensible Platform, rather than building from scratch. Aligns Vitis platform configuration with both CED and Vitis Base Platforms. |

---

## 4. Benefits of HLS

### Improve Productivity

- **Fewer lines of code** are needed as input compared to raw RTL.
- Designers focus on **algorithmic intent** rather than mechanical implementation.
- C/C++ testbenches can be written at a high level and **reused directly** to verify generated RTL — reducing overall verification effort.
- Faster design iteration remains within the C/C++ domain before committing to RTL.

**Productivity benefits summary:**

| Benefit | How HLS Delivers It |
|---|---|
| Algorithm development | Work at C-level, abstract from hardware details |
| Rapid validation | C-simulation validates logic before RTL exists |
| Design space exploration | Multiple RTL implementations from one C source + pragma variants |

### Enable Re-Use

- HLS designs are **technology-node-agnostic** and **clock-period-agnostic**.
- Changing clock speed or target device requires only constraint updates — **no source code changes**.
- Compare to RTL: any derivative product change, however small, forces a new project.
- HLS allows the tool to automatically regenerate optimized RTL when constraints change.

---

## 5. Introduction to Vitis HLS Components

An **HLS component** is a C/C++ function synthesized into RTL code targeting the **Programmable Logic (PL)** region of:
- AMD Versal™ Adaptive SoC
- AMD Zynq™ MPSoC
- AMD FPGA devices

### Output Targets

| Target | Usage Context | Notes |
|---|---|---|
| **Vivado IP** | Hardware designs in Vivado Design Suite; embedded software with provided drivers | Fewer restrictions; greater flexibility |
| **Vitis Kernel (`.xo`)** | Vitis application acceleration flow; AI Engine graph applications; Data Center acceleration | Specific interface requirements apply |

### HLS Component Development Flow

| Step | Tool / Action | Purpose |
|---|---|---|
| 1 | Architect algorithm | Apply Design Principles for FPGA |
| 2 | **C-Simulation** | Verify C/C++ functionality with testbench |
| 3 | **Code Analyzer** | Analyze performance, parallelism, and HLS legality |
| 4 | **C-Synthesis** (`v++`) | Generate RTL |
| 5 | **C/RTL Co-Simulation** | Verify RTL functionally against C testbench |
| 6 | **Package** | Review HLS synthesis + implementation timing reports |
| 7 | Iterate | Re-run steps until performance goals are met |

---

## 6. Key Synthesis Concepts

### Hardware Interfaces

- Top-level function **arguments** are synthesized into **interfaces and ports** that define the communication protocol between the HLS component and external components.
- The `v++` compiler assigns interface protocols automatically using industry standards.
- Default protocols differ depending on target: **Vivado IP** vs. **Vitis kernel**.
- Overridden using the `INTERFACE` pragma or directive.

### Controlling Execution (Block-Level Control)

- The **execution mode** of an HLS component is set by the **block-level control protocol**.
- Options include:
  - Control signals to **start/stop** execution explicitly.
  - **Data-driven** execution — component activates when data is available.
- See *Execution Modes of HLS Designs* for details.

### Task-Level Parallelism (TLP)

Two methods to express TLP:

| Method | Description |
|---|---|
| `#pragma HLS DATAFLOW` | Compiler infers task-level parallelism across pipelined functions/loops automatically |
| `hls::task` object | Explicit parallel programming model for finer control |

> **Rule of thumb:** Sequential functions → made concurrent. Sequential loops → pipelined.

### Memory Architecture

| Concept | Detail |
|---|---|
| Local memory | Synthesized from C++ arrays; fast access (1+ cycles) |
| Global memory | DDR / HBM; high latency (many cycles) |
| Dynamic allocation | **Not synthesizable** — exact memory requirements must be known statically |
| Burst access | Hides memory latency; improves bandwidth via `BURST` pragma or auto-detection |
| Access coalescing | Combines multiple accesses into one by expanding data width |

- Memory is **fixed in the CPU** but the developer can design custom memory architecture on PL to optimize access patterns.
- **Burst access** and **coalescing** are the primary techniques for global memory bandwidth optimization.

### Micro-Level Optimization

| Pragma | Purpose |
|---|---|
| `PIPELINE` | Pipeline a loop or function, initiating new iterations before prior ones complete |
| `UNROLL` | Replicate loop body hardware to execute multiple iterations in parallel |
| `ARRAY_PARTITION` | Partition arrays into smaller memories or registers for parallel access |
| `PERFORMANCE` | High-level goal: specify a single target initiation interval (TI); tool infers required sub-pragmas automatically |

> The `PERFORMANCE` pragma reduces pragma verbosity and is the preferred approach for loop optimization — fewer pragmas needed for good **Quality of Results (QoR)**.

---

## 7. Refactoring C++ Source Code for HLS

### The Sequential Baseline (Before Refactoring)

```cpp
#include <vector>
#include <iostream>
#include <ap_int.h>
#include "hls_vector.h"

#define totalNumWords 512
unsigned char data_t;

void compute(data_t in[totalNumWords], data_t Out[totalNumWords]) {
    data_t tmp1[totalNumWords], tmp2[totalNumWords];
    A: for (int i = 0; i < totalNumWords; ++i) {
        tmp1[i] = in[i] * 3;
        tmp2[i] = in[i] * 3;
    }
    B: for (int i = 0; i < totalNumWords; ++i) {
        tmp1[i] = tmp1[i] + 25;
    }
    C: for (int i = 0; i < totalNumWords; ++i) {
        tmp2[i] = tmp2[i] * 2;
    }
    D: for (int i = 0; i < totalNumWords; ++i) {
        out[i] = tmp1[i] + tmp2[i] * 2;
    }
}
```

**Problem:** This code runs **sequentially** on an FPGA — no performance gain over a CPU.

### What Limits Performance

| Limitation | Explanation |
|---|---|
| No task-level parallelism | All four loops run one after another |
| No data streaming | The compute function waits for all data before starting |
| No instruction-level parallelism | Operations are performed word-by-word instead of on vectors |
| No loop pipelining | Each loop iteration waits for the previous to finish |

### Required Transformations

To achieve performance on an FPGA, the algorithm must expose:

1. **Task-level parallelism** — the compute function can start before all data is transferred (streaming).
2. **Overlapping execution** — loop iterations can begin before prior ones complete (pipelining).
3. **Instruction-level parallelism** — process multiple words (e.g., 16 words at once) in a single clock cycle using `hls::vector`.

---

## 8. Re-Architecting the Hardware Module

### Architecture Pattern: Load–Compute–Store

The key refactoring pattern for HLS is to decompose a monolithic function into sub-functions following this shape:

```
Load → Compute_A → Compute_B ──┐
                  └→ Compute_C ──→ Compute_D → Store
```

This is the **diamond** dataflow pattern. Data flows between functions via `hls::stream` FIFOs.

### Refactored Diamond Example (`using_fifos`)

```cpp
#include "diamond.h"
#define NUM_WORDS 16

extern "C" {
void diamond(vecOf16Words* vecIn, vecOf16Words* vecOut, int size) {
    hls::stream<vecOf16Words> c0, c1, c2, c3, c4, c5;
    assert(size % 16 == 0);

    #pragma HLS dataflow          // << enables task-level parallelism
    load(vecIn, c0, size);
    compute_A(c0, c1, c2, size);
    compute_B(c1, c3, size);
    compute_C(c2, c4, size);
    compute_D(c3, c4, c5, size);
    store(c5, vecOut, size);
}
}

void load(vecOf16Words* in, hls::stream<vecOf16Words>& out, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        out.write(in[i]);
    }
}

void compute_A(hls::stream<vecOf16Words>& in,
               hls::stream<vecOf16Words>& out1,
               hls::stream<vecOf16Words>& out2, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        vecOf16Words t = in.read();
        out1.write(t * 3);       // broadcast to both paths
        out2.write(t * 3);
    }
}

void compute_B(hls::stream<vecOf16Words>& in,
               hls::stream<vecOf16Words>& out, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        out.write(in.read() + 25);
    }
}

void compute_C(hls::stream<vecOf16Words>& in,
               hls::stream<vecOf16Words>& out, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        out.write(in.read() * 2);
    }
}

void compute_D(hls::stream<vecOf16Words>& in1,
               hls::stream<vecOf16Words>& in2,
               hls::stream<vecOf16Words>& out, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        out.write(in1.read() + in2.read());
    }
}

void store(hls::stream<vecOf16Words>& in, vecOf16Words* out, int size) {
    Loop0:
    for (int i = 0; i < size; i++) {
        #pragma HLS PERFORMANCE target_ti=32
        #pragma HLS LOOP_TRIPCOUNT max=32
        out[i] = in.read();
    }
}
```

### Key Design Elements in the Diamond Example

| Element | Role |
|---|---|
| `hls::stream<T>` | FIFO channel between tasks; decouples producers from consumers |
| `#pragma HLS dataflow` | Instructs the compiler to run all called functions **concurrently** as a pipeline |
| `vecOf16Words` | Represents 16 × 32-bit words (512 bits) — **instruction-level parallelism** via vector width |
| `#pragma HLS PERFORMANCE target_ti=32` | Sets a target initiation interval; tool infers loop pipeline depth automatically |
| `#pragma HLS LOOP_TRIPCOUNT max=32` | Provides loop trip count for latency estimation (not a functional constraint) |
| `load` / `store` functions | Isolate memory access from compute; enable burst inference and bandwidth optimization |
| `assert(size % 16 == 0)` | Enforces alignment constraint required for vectorized 512-bit memory accesses |

### Parallelism Levels Achieved

| Level | Mechanism | Example |
|---|---|---|
| Task-level | `#pragma HLS dataflow` + `hls::stream` | `compute_B` and `compute_C` run simultaneously |
| Loop-level | `#pragma HLS PERFORMANCE` / `PIPELINE` | Each loop starts a new iteration every `target_ti` cycles |
| Instruction-level | `hls::vector` / wide data types (`vecOf16Words`) | 16 words processed per loop iteration in parallel |

---

## 9. Best Practices

### Architecture
- **Think load–compute–store:** Decompose any top-level function into separate load, compute, and store sub-functions. This isolates memory accesses, enables burst inference, and establishes clean dataflow boundaries.
- **Push loops into functions:** To apply `#pragma HLS dataflow`, loops must be encapsulated in separate functions. Sequential loops become pipelined stages when separated this way.
- **Design with streaming in mind:** Use `hls::stream<T>` for inter-function communication within a dataflow region. Avoid shared arrays between dataflow tasks — these create dependencies that break parallelism.

### Performance
- **Use `PERFORMANCE` over raw `PIPELINE`/`UNROLL` combos:** The `PERFORMANCE` pragma with a single `target_ti` goal lets the tool automatically infer the required pipeline and unroll factors, reducing pragma complexity and improving QoR maintainability.
- **Prefer wide data types for instruction-level parallelism:** Use `hls::vector` or `ap_uint<N>` wide-width types to process multiple data elements per clock cycle rather than scalar loops.
- **Specify `LOOP_TRIPCOUNT` for all loops with non-constant bounds:** The tool requires this for accurate latency/throughput estimation in reports. It has no effect on synthesized logic.

### Memory
- **Avoid dynamic memory allocation (`new`/`malloc`):** These cannot be synthesized. Declare all arrays as fixed-size at compile time.
- **Minimize global memory accesses:** Every DDR/HBM access incurs significant latency. Buffer data locally, and structure access patterns to allow the tool to infer burst transfers.
- **Use `assert` for alignment constraints:** When using vector types with wide AXI ports, `assert(size % N == 0)` communicates alignment requirements to the tool and guards against runtime misuse.

### Interfaces & Integration
- **Understand Vivado IP vs. Vitis Kernel trade-offs early:** Vitis kernels require specific `extern "C"` linkage, specific argument types for AXI interfaces, and have tighter restrictions. Choose the target output format before writing interface code.
- **Let the compiler handle default interfaces first:** Only apply `INTERFACE` pragmas when the default protocol is incorrect for your use case.

### Verification
- **Write the C testbench before synthesis:** The same testbench used for C-simulation should be reused in C/RTL Co-simulation. This guarantees that the synthesized RTL matches the original behavioral intent.
- **Iterate within C/C++ before committing to synthesis:** Fixing algorithmic bugs at the C level is orders of magnitude faster than debugging synthesized RTL.

---

## 10. Tutorials and Examples

| Resource | Location | Content |
|---|---|---|
| **Vitis HLS Introductory Examples** | `github.com/Xilinx/Vitis-HLS-Introductory-Examples` | Small code examples: design patterns, coding guidelines, optimization techniques. Each includes `README`, `hls_config.cfg`, `run_hls.tcl`. |
| **Vitis Accel Examples Repository** | `github.com/Xilinx/Vitis_Accel_Examples` | Host + kernel programming examples for the Vitis acceleration flow. Kernel code is directly compilable as HLS components. |
| **Vitis Application Acceleration Tutorials** | `github.com/Xilinx/Vitis-Tutorials` | Step-by-step tutorials covering tool flow and application development, including using the Vitis unified IDE for bottom-up HLS component design. |

---

### See Also

- [Chapter 1 — Design Principles](../section02_hls_programmers_guide/ch01_design_principles.md) — Core HLS design guidelines
- [Chapter 12 — Launching Vitis IDE](../section03_vitis_hls_flow_steps/ch12_launching_vitis_ide.md) — Getting started with IDE flow
- [Appendix C — Resources](../appendices/appendix_c_resources.md) — External documentation links

---

*UG1399 (v2025.2) · January 22, 2026 · AMD Vitis HLS User Guide*
