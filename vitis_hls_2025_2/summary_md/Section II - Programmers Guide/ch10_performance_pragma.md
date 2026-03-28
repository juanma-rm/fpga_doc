# Chapter 10: Top-Level Performance Pragma

> **Source:** Vitis HLS User Guide UG1399 v2025.2, Chapter 10, Pages 260–264

---

## Table of Contents
1. [Overview](#1-overview)
2. [Top-Level vs. Loop-Level Performance Pragma](#2-top-level-vs-loop-level-performance-pragma)
3. [Step-by-Step Methodology](#3-step-by-step-methodology)
4. [Pragma Syntax](#4-pragma-syntax)
5. [Optimization Strategy and Priority](#5-optimization-strategy-and-priority)
6. [Limitations and Precedence Rules](#6-limitations-and-precedence-rules)
7. [Unsupported Libraries and Constructs](#7-unsupported-libraries-and-constructs)
8. [Known Issues](#8-known-issues)
9. [Best Practices](#9-best-practices)

---

## 1. Overview

The **top-level performance pragma** is a high-level throughput constraint that guides synthesis across the entire design hierarchy. Instead of manually tuning each loop and array, the compiler performs a **design-wide throughput analysis** and automatically infers appropriate low-level pragmas (`PIPELINE`, `UNROLL`, `FLATTEN`, `ARRAY_PARTITION`, `RESHAPE`) for individual loops and loop nests.

**Core idea:** Specify *what* throughput you need; the tool determines *how* to achieve it.

---

## 2. Top-Level vs. Loop-Level Performance Pragma

| Feature | Top-Level | Loop-Level |
|---|---|---|
| Scope | Entire design | Single loop or loop nest |
| Usage | Throughput goal for top function | Fine-grained bottleneck refinement |
| Inference | Automatically infers loop-level pragmas | Manually specified or auto-inferred by top-level |
| Low-level pragmas inferred | `PIPELINE`, `UNROLL`, `FLATTEN`, `RESHAPE`, `ARRAY_PARTITION` | Same set |

**Workflow:** Apply top-level → synthesize → identify bottleneck loops → add loop-level targets → iterate.

---

## 3. Step-by-Step Methodology

### Step 1: Calculate the Performance Target

Determine the required **target initiation interval** (`target_ti`) for your application:

$$\text{target\_ti (cycles)} = \frac{f_\text{clk}}{\text{throughput\_goal}}$$

**Example for 60 FPS video processing at 300 MHz:**
$$\text{target\_ti} = \frac{1}{60 \text{ fps}} \approx 16.67 \text{ ms} = 5{,}000{,}000 \text{ cycles at 300 MHz}$$

Units accepted by the pragma:
- Milliseconds: `target_ti = 16.67 ms`
- Clock cycles: `target_ti = 5000000`

### Step 2: Verify Code Structure

Before applying performance pragmas, ensure the code is **structured for dataflow**:
- Re-architect into Load–Compute–Store (LCS) tasks
- Apply `#pragma HLS DATAFLOW` at the appropriate level
- This gives the compiler the concurrent execution foundation it needs to meet throughput goals

### Step 3: Run C-Simulation with Loop Tripcount Profiling

```bash
# Enable tripcount profiling in Vitis HLS project settings
```

- C-simulation automatically captures **actual loop iteration counts**
- The performance pragma algorithm requires accurate trip counts to budget all loops
- Without profiling, dynamic loops default to **1024** iterations — leads to inaccurate estimates for loops with bounds > 1024
- Variable loops: also add `#pragma HLS LOOP_TRIPCOUNT max=N` as backup

### Step 4: Apply the Top-Level Performance Pragma

```cpp
// At the top of the top-level function body:
#pragma HLS performance target_ti = 16.67 ms    // milliseconds
// or:
#pragma HLS performance target_ti = 5000000      // cycles
```

### Step 5: Run C Synthesis and Analyze Results

- Run synthesis in Vitis HLS
- Examine the synthesis report for loops/functions that do **not** meet `target_ti`
- These are bottlenecks requiring loop-level intervention

### Step 6: Add Loop-Level Performance Targets

```cpp
// Target a specific loop's initiation interval:
for (int i = 0; i < N; i++) {
#pragma HLS performance target_ti = 100       // cycles budget for this loop
    // ...
}
```

### Step 7: Iterate Until Converged

- Repeat: synthesize → analyze report → tighten loop-level targets → synthesize
- **Export inferred pragmas** to a user configuration file to lock them in (prevents the tool from re-exploring on each run):

```bash
# Export after convergence to lock in results
# Re-inject into source or directives file for faster subsequent runs
```

---

## 4. Pragma Syntax

```cpp
// Top-level: placed inside the top function body
#pragma HLS performance target_ti = <value> [ms | cycles]

// Loop-level: placed inside the target loop
for (...) {
#pragma HLS performance target_ti = <value>
    // ...
}
```

**`target_ti`** = target transaction interval (= target initiation interval for the function/loop).

---

## 5. Optimization Strategy and Priority

The performance pragma prioritizes:

1. **Timing constraints first** — will NOT sacrifice timing (clock period) to meet throughput
2. **Throughput second** — explores pragmas to approach `target_ti`

**Consequence:** If throughput targets cannot be met while respecting timing, the tool reports the gap. Use classic pragmas (`UNROLL`, `PIPELINE`) for finer control in that case.

**Auto-inferred pragmas include:**
- `PIPELINE` on loops (with inferred II)
- `UNROLL` with inferred factor
- `FLATTEN` for loop nests
- `ARRAY_PARTITION` / `ARRAY_RESHAPE` on local arrays

---

## 6. Limitations and Precedence Rules

When classic pragmas co-exist with performance pragma, precedence rules apply:

| Classic Pragma Present | Effect on Performance Pragma Inference |
|---|---|
| `PIPELINE OFF` on a loop | Performance pragma will NOT auto-infer `PIPELINE` for that loop |
| `UNROLL OFF` on a loop | Performance pragma will NOT auto-infer `UNROLL` for that loop |
| `FLATTEN` on a loop | Performance pragma will NOT infer any additional `FLATTEN` |
| `ARRAY_PARTITION OFF` on array | Performance pragma will NOT auto-infer `ARRAY_PARTITION` for that array |

**Interface port limitation:**
- Arrays at the **top-level function interface** are NOT automatically partitioned
- To enable auto-partition for interface arrays:

```bash
# hls_config.cfg
config_array_partition -throughput_driven=aggressive
```

---

## 7. Unsupported Libraries and Constructs

The performance pragma uses a **code analyzer** for design-wide analysis. Constructs unsupported by the analyzer fall into two categories:

| Behavior | Constructs |
|---|---|
| **Tool exits with warning** | `ap_cint`, `hls::stream_of_blocks`, `hls::task`, `hls::split`/`hls::merge`, `hls::print`, `hls::half`, `ap_utils.h`, `hls_fpo.h`, `ap_float`, RTL blackboxes, `hls::burst_maxi`, `hls::fence`, `hls::directio` |
| **Inaccurate performance models** (pragma continues) | `ap_(u)int` / `ap_(u)fixed`, HLS IP blocks (FFT, FIR, ...), `hls_math.h`, `ap_wait`, `hls::vector`, `ap_axis`/`ap_axiu` |
| **Compiler error** | `std::complex<ap_fixed>` (Windows only), macros with `NON_C99STRING` on large constant `ap_int` arrays |
| **Warning only (deprecated ignoring)** | Deprecated HLS pragmas |
| **Assertion failure** | Function pipeline with sub-loop |

---

## 8. Known Issues

### Long Compile Time

The performance pragma performs comprehensive design-wide analysis — exploring many optimization paths simultaneously. This can lead to significantly longer synthesis times for large designs. If experienced, contact AMD support.

### Aggressive Inferred Performance Targets

The tool may infer very aggressive targets for specific loops (minimal resource goal), leading to **excessive resource consumption** on those loops. If a loop shows high resource utilization after performance pragma inference:
- Use classic `PIPELINE`, `UNROLL`, or `ARRAY_PARTITION` pragmas directly on that loop
- These provide finer-grained resource control than the performance pragma

---

## 9. Best Practices

| Topic | Recommendation |
|---|---|
| **Pre-requisite** | Always structure code as LCS + `DATAFLOW` before adding performance pragma |
| **Trip counts** | Run C-sim with tripcount profiling before synthesis; add `LOOP_TRIPCOUNT max=N` for variable loops |
| **Target units** | Prefer milliseconds for time-based targets (FPS, latency SLAs); avoid guessing cycle counts |
| **Iteration** | Apply top-level first; add loop-level targets only for identified bottlenecks |
| **Locking in** | Export and lock inferred pragmas after convergence to avoid re-exploration |
| **Timing safety** | Never compromise clock period for throughput — the pragma respects this automatically |
| **Resource overrun** | If a loop over-consumes resources after inference, override with explicit `PIPELINE`/`UNROLL` |
| **Unsupported libs** | Review the unsupported construct table before applying the pragma to complex designs |
| **Interface arrays** | Enable `config_array_partition -throughput_driven=aggressive` if interface arrays are bottlenecks |
| **Variable loops** | Provide `LOOP_TRIPCOUNT` for all variable-bound loops; default of 1024 may be wildly inaccurate |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 10: Top-Level Performance Pragma, Pages 260–264.*
