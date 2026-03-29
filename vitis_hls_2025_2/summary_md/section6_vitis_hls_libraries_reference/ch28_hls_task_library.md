# Chapter 28 — HLS Task Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 821–828

## Table of Contents

- [Overview](#overview)
- [Basic Example — Data-Driven TLP](#basic-example--data-driven-tlp)
- [Restrictions on hls::task](#restrictions-on-hlstask)
- [Support of Scalars / Memory Interfaces in DTLP](#support-of-scalars--memory-interfaces-in-dtlp)
  - [Control-Driven TLP (CDTLP)](#control-driven-tlp-cdtlp)
  - [Data-Driven TLP (DTLP)](#data-driven-tlp-dtlp)
  - [Stable Memory Interface Example](#stable-memory-interface-example)
- [Tasks and Channels — Explicit Programming Model](#tasks-and-channels--explicit-programming-model)
  - [Task Nesting](#task-nesting)
- [Use of Flushing Pipelines](#use-of-flushing-pipelines)
- [Simulation and Co-Simulation](#simulation-and-co-simulation)
- [Tasks and Dataflow — Mixed Regions](#tasks-and-dataflow--mixed-regions)
- [Task-Level Parallelism Hierarchy Rules](#task-level-parallelism-hierarchy-rules)
- [Best Practices](#best-practices)

---

## Overview

The `hls::task` library enables **data-driven task-level parallelism (DTLP)**: static instantiation of tasks that run continuously whenever data is present on their input streams, with no synchronization or function-call overhead.

**Header:**
```cpp
#include "hls_task.h"
```

> **Key difference vs DATAFLOW:** In `#pragma HLS dataflow`, Vitis HLS identifies tasks and manages parallelism automatically. With `hls::task`, you explicitly instantiate tasks and channels — giving you full control and concurrent C simulation semantics.

> **Important:** Including `hls_task.h` makes all `hls::stream` reads **blocking** in C simulation. Reading an empty stream will cause a deadlock error, not a warning.

---

## Basic Example — Data-Driven TLP

```cpp
#include "hls_task.h"

void odds_and_evens(hls::stream<int> &in,
                    hls::stream<int> &out1,
                    hls::stream<int> &out2)
{
    // Thread-local channels (persistent across calls)
    hls_thread_local hls::stream<int> s1;  // connects t1 → t2
    hls_thread_local hls::stream<int> s2;  // connects t1 → t3

    // Tasks run infinitely; no while(1) needed in task bodies
    hls_thread_local hls::task t1(splitter, in, s1, s2);
    hls_thread_local hls::task t2(odds,     s1, out1);
    hls_thread_local hls::task t3(evens,    s2, out2);
}
```

- `hls_thread_local`: keeps the variable (and underlying thread) alive across multiple calls of the enclosing function.
- Task bodies (`splitter`, `odds`, `evens`) have an implicit infinite loop — they run whenever data is available.
- No synchronization is needed between tasks.

---

## Restrictions on hls::task

| Restriction | Details |
|---|---|
| Streaming I/O only | Tasks can only read/write `hls::stream` or `hls::stream_of_blocks` — no direct memory access |
| Scalars/pointers require STABLE | Non-stream arguments can be passed if declared `stable` via `#pragma HLS stable` |
| m_axi offset constraint | Top pointers with `m_axi` interface can only be passed with `offset=off` |
| Unsynchronized non-stream ports | Scalars/arrays are read at unknown intervals; code must not depend on timing |
| Must be in a parallel context | Cannot be nested directly in a sequential context — must be inside a DATAFLOW region or another `hls::task` |
| No nested sequential inside data-driven | A sequential region can only be inside the body of a control-driven or data-driven TASK |

### Task/Region Nesting Table

| Region type | Where it can be placed |
|---|---|
| Control-driven TLP | Top, inside another control-driven, or inside sequential region |
| Data-driven TLP | Top, inside another data-driven, or nested between control-driven tasks |
| Control-driven | **Cannot** be directly inside a pipeline or directly inside data-driven |
| Data-driven | **Cannot** be directly inside sequential, pipeline, or control-driven |
| Sequential / pipeline | Can only be inside the body of a control-driven or data-driven TASK |

---

## Support of Scalars / Memory Interfaces in DTLP

### Control-Driven TLP (CDTLP)

Follows standard C semantics: function parameters must be available before the function is called and remain constant until it completes. Non-stream I/O is treated predictably.

### Data-Driven TLP (DTLP)

Kernels run continuously from FPGA power-on. There are no function start/end synchronization points. Two behaviors for non-stream I/O:

| Case | Behavior | Mechanism |
|---|---|---|
| (a) Can change at any time | Kernel reads updated value at some future point | Use `hls::direct_io` (see Ch. 25) |
| (b) Never changes during execution | Treated as stable — compiler assumes constant value | Mark as `#pragma HLS stable` |

### Stable Memory Interface Example

```cpp
void stable_pointer(int* mem,
                    hls::stream<int>& in,
                    hls::stream<int>& out)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE mode=s_axilite port=mem offset=30
#pragma HLS INTERFACE mode=m_axi bundle=gmem depth=256 port=mem
#pragma HLS stable variable=mem    // <-- mark as stable

    hls_thread_local hls::stream<int> int_fifo("int_fifo");
#pragma HLS STREAM depth=512 type=fifo variable=int_fifo
    hls_thread_local hls::stream<int> int_fifo2("int_fifo2");
#pragma HLS STREAM depth=512 type=fifo variable=int_fifo2

    hls_thread_local hls::task t1(process_23, in, int_fifo);
    hls_thread_local hls::task t2(process_11, int_fifo, int_fifo2);
    hls_thread_local hls::task t3(write_process, int_fifo2, out, mem);
}
```

> For C/RTL co-simulation with `hls::task` and M_AXI interfaces, enable via:
> `cosim.enable_tasks_with_m_axi`

---

## Tasks and Channels — Explicit Programming Model

Unlike DATAFLOW, with `hls::task` you explicitly create channels and wire tasks together:

```cpp
void func1(hls::stream<int> &in, hls::stream<int> &out1, hls::stream<int> &out2) {
    int data = in.read();
    if (data >= 10) out1.write(data);
    else            out2.write(data);
}
void func2(hls::stream<int> &in, hls::stream<int> &out) { out.write(in.read() + 1); }
void func3(hls::stream<int> &in, hls::stream<int> &out) { out.write(in.read() + 2); }

void top_func(hls::stream<int> &in, hls::stream<int> &out1, hls::stream<int> &out2) {
    hls_thread_local hls::stream<int> s1;   // channel: t1 → t2
    hls_thread_local hls::stream<int> s2;   // channel: t1 → t3

    hls_thread_local hls::task t1(func1, in, s1, s2);
    hls_thread_local hls::task t2(func2, s1, out1);
    hls_thread_local hls::task t3(func3, s2, out2);
}
```

Both the `hls::task` objects and the channels connecting them **must** be `hls_thread_local`.

### Task Nesting

Tasks can contain other tasks — forming hierarchical data-driven networks:

```cpp
void task1(hls::stream<int> &in, hls::stream<int> &out) {
    hls_thread_local hls::stream<int> s1;
    hls_thread_local hls::task t1(func2, in, s1);
    hls_thread_local hls::task t2(func3, s1, out);
}

void task2(hls::stream<int> &in1, hls::stream<int> &in2,
           hls::stream<int> &out1, hls::stream<int> &out2) {
    hls_thread_local hls::task tA(task1, in1, out1);  // independent instance
    hls_thread_local hls::task tB(task1, in2, out2);  // independent instance
}
```

`hls_thread_local` ensures each instance of `tA`/`tB` (and their internal `t1`/`t2`) contains independently executing threads.

---

## Use of Flushing Pipelines

`hls::task` designs must use **flushing pipelines** (`flp`) or **free-running pipelines** (`frp`). Non-flushing pipelines introduce dependencies between executions that can cause unexpected deadlocks.

Default flushing behavior in `hls::task` can be configured with:
```
syn.compile.pipeline_flush_in_task
```

---

## Simulation and Co-Simulation

C simulation semantics for tasks match C/RTL co-simulation — reading from an empty stream is always an error:

| Condition | Error Message |
|---|---|
| Design with `hls::task`, deadlock | `ERROR [HLS SIM]: deadlock detected when simulating hls::tasks. Execute C-simulation in debug mode...` |
| Design without `hls::task`, empty stream read | `ERROR [HLS SIM]: an hls::stream is read while empty...` |

> **To convert error to warning:** add `-DHLS_STREAM_READ_EMPTY_RETURNS_GARBAGE` to `-cflags`. This allows empty reads to return the default value for the data type.

---

## Tasks and Dataflow — Mixed Regions

`hls::task` can coexist with standard DATAFLOW processes in the same top-level function. I/O processes (accessing M_AXI, scalars, PIPOs) use DATAFLOW; data transformation uses tasks:

```cpp
#include "hls_task.h"

// I/O dataflow processes
void read_in(int* in, int n, hls::stream<int> &s1) {
    for (int i = 0; i < n; i++) s1.write(in[i]);
}
void write_out(int* out, int n, hls::stream<int> &s2) {
    for (int i = 0; i < n; i++) out[i] = s2.read();
}

// Task bodies (no while(1) needed)
void func1(hls::stream<int> &s1, hls::stream<int> &s3) {
    s3.write(... + s1.read());
}
void func2(hls::stream<int> &s3, hls::stream<int> &s2) {
    s2.write(... * s3.read());
}

void top_func(int *in, int *out, int n) {
#pragma HLS dataflow
    hls_thread_local hls::stream<int> sk1, sk2, sk3;

    read_in(in, n, sk1);                            // I/O process — order matters
    hls_thread_local hls::task t2(func2, sk3, sk2); // task — order doesn't matter
    hls_thread_local hls::task t1(func1, sk1, sk3); // task — order doesn't matter
    write_out(out, n, sk2);                         // I/O process — order matters
}
```

Vitis HLS automatically splits this into two internal dataflow regions:
1. `ap_ctrl_chain` region — sequential functions (`read_in`, `write_out`) + call to ap_ctrl_none region below.
2. `ap_ctrl_none` region — tasks and channels.

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Declare tasks and channels as `hls_thread_local` | Keeps objects and threads alive across top-level calls |
| Use only streaming I/O in task bodies | Tasks are data-driven; non-stream access requires `STABLE` |
| Use flushing or free-running pipelines inside tasks | Non-flushing pipelines can deadlock across task iterations |
| Place I/O dataflow processes before task declarations | Ensures proper ordering in the mixed DATAFLOW+TASK model |
| Use `cosim.enable_tasks_with_m_axi` for co-simulation | Required for C/RTL co-simulation with M_AXI interfaces |
| Pass scalars/arrays via `#pragma HLS stable` only | These are read at arbitrary times — do not depend on timing |

---

### See Also

- [Chapter 2 — Abstract Parallel Programming](../section2_hls_programmers_guide/ch02_abstract_parallel_programming.md) — Control-driven vs data-driven TLP
- [Chapter 24 — HLS Stream Library](ch24_hls_stream_library.md) — `hls::stream` API used with tasks
- [Chapter 11 — Optimizing Techniques](../section2_hls_programmers_guide/ch11_optimizing_techniques.md) — Dataflow canonical coding, deadlock avoidance

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 28, pages 821–828*
