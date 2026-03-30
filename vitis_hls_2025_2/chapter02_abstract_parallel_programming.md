# Chapter 2 — Abstract Parallel Programming Model for HLS
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [The Abstract Parallel Programming Model](#1-the-abstract-parallel-programming-model)
2. [Channel Semantics: Blocking vs Non-Blocking](#2-channel-semantics-blocking-vs-non-blocking)
3. [Control-Driven vs Data-Driven TLP](#3-control-driven-vs-data-driven-tlp)
4. [Data-Driven TLP — `hls::task`](#4-data-driven-tlp--hlstask)
5. [Control-Driven TLP — Dataflow Pragma](#5-control-driven-tlp--dataflow-pragma)
6. [Dataflow Region Coding Style (WYSIWYG / Canonical)](#6-dataflow-region-coding-style-wysiwyg--canonical)
7. [Advanced Dataflow Features](#7-advanced-dataflow-features)
8. [Configuring Dataflow Memory Channels](#8-configuring-dataflow-memory-channels)
9. [Stream-of-Blocks (`hls::stream_of_blocks`)](#9-stream-of-blocks-hlsstream_of_blocks)
10. [Compiler-Created FIFO Types](#10-compiler-created-fifo-types)
11. [`#pragma HLS stable`](#11-pragma-hls-stable)
12. [Mixing Data-Driven and Control-Driven Models](#12-mixing-data-driven-and-control-driven-models)
13. [Summary: Choosing the Right TLP Model](#13-summary-choosing-the-right-tlp-model)
14. [Best Practices](#14-best-practices)

---

## 1. The Abstract Parallel Programming Model

The fundamental issue with synthesizing general C/C++ software is that **constructs used in good software design** — RTTI, recursion, dynamic memory allocation — **have no direct hardware equivalent**. Even synthesizable code must be structured to help the tool infer parallelism.

The abstract model underlying HLS is:

| Concept | Description |
|---|---|
| **Task** | An executable unit with local storage (block RAM/URAM) and I/O ports |
| **Channel** | A data queue connecting one task's output to another task's input; either FIFO or PIPO |
| **Local data access** | Fast access to private memory inside a task (block RAM/URAM) |
| **Non-local data access** | Data transferred through channels (I/O ports) |
| **Control-driven task** | Waits for a control signal to start/stop execution |
| **Data-driven task** | Reacts to the presence of data on input channels; always running |

**Channel guarantees:**
- Data written by the producer arrives at the consumer **in order** (FIFO).
- **PIPOs** support random access within a block.
- **No data is lost.**

---

## 2. Channel Semantics: Blocking vs Non-Blocking

| Semantic | Empty-read behavior | Full-write behavior | Simulation | Deadlock risk |
|---|---|---|---|---|
| **Blocking** | Reading process **stalls** until data arrives | Writing process **stalls** until space is available | Deterministic; order-independent | Yes (FIFO sizing / cycle of processes) |
| **Non-blocking** | Returns uninitialized or last data; no stall | Data may be **lost** if queue full | Non-deterministic | Lower, but loss possible |

> **Recommendation:** Use **blocking** semantics for deterministic, verifiable designs. Non-blocking requires explicit empty/full checks and makes verification significantly harder.

Both blocking and non-blocking semantics are supported by `hls::stream`.

---

## 3. Control-Driven vs Data-Driven TLP

| Criterion | Control-Driven TLP (Dataflow) | Data-Driven TLP (`hls::task`) |
|---|---|---|
| Execution trigger | Control signal (ap_start) | Presence of data on input stream |
| External memory access | Yes (m_axi, arrays) | Primarily streaming; scalars/arrays via specific support |
| Data pattern | Fixed rates; sequential semantics preserved | Variable/data-dependent rates (dynamic multi-rate) |
| Feedback (cyclic deps) | Limited | Fully supported |
| TLP visibility in C-sim | **Not** observable in C-sim (needs co-sim) | **Observable** in C-sim |
| Typical applications | Memory-mapped accelerators, kernels with DDR access | Always-on stream processors, FFT with compiled config, FIR filters |

---

## 4. Data-Driven TLP — `hls::task`

### The `hls::task` Model

`hls::task` objects are C++ class instances that model **always-running hardware threads**, infinitely calling their assigned task body function. They have **no function call/return latency** — they run as long as data is present.

```cpp
#include "test.h"

void splitter(hls::stream<int> &in, hls::stream<int> &odds_buf,
              hls::stream<int> &evens_buf) {
    int data = in.read();
    if (data % 2 == 0) evens_buf.write(data);
    else                odds_buf.write(data);
}
void odds(hls::stream<int> &in, hls::stream<int> &out) {
    out.write(in.read() + 1);
}
void evens(hls::stream<int> &in, hls::stream<int> &out) {
    out.write(in.read() + 2);
}

void odds_and_evens(hls::stream<int> &in, hls::stream<int> &out1,
                    hls::stream<int> &out2) {
    hls_thread_local hls::stream<int> s1;  // FIFO: t1 → t2
    hls_thread_local hls::stream<int> s2;  // FIFO: t1 → t3
    hls_thread_local hls::task t1(splitter, in, s1, s2);
    hls_thread_local hls::task t2(odds,     s1, out1);
    hls_thread_local hls::task t3(evens,    s2, out2);
}
```

### Key Attributes of `hls::task`

| Attribute | Detail |
|---|---|
| `hls_thread_local` qualifier | **Required** on both tasks and their internal streams — keeps object alive across multiple calls of the instantiating function; matches RTL "always running" behavior |
| Implicit infinite loop | The supplied function is called repeatedly with the same arguments indefinitely |
| Arguments | **Only** `hls::stream` or `hls::stream_of_blocks` arguments are supported |
| Constant values | Must be passed as **template arguments** (not function arguments) |
| Pipelined loops inside task body | Must use **flushing pipeline (FLP)** style to prevent deadlock (`#pragma HLS pipeline II=1 style=flp`) |
| Static binding | A task is statically bound to channels — not a function call; each task is instantiated **once** |

### `hls::stream` Channel Properties

| Property | Detail |
|---|---|
| Template: `hls::stream<type, depth>` | FIFO with given depth; **default depth = 2** |
| Read order | Sequential; once read, data cannot be re-read |
| Access ordering | Accesses to **different** streams may be reordered by the scheduler |
| Scope | Local or global; global streams follow the same global variable rules |

### Deadlock Detection

A **deadlock detector** is automatically instantiated for designs containing `hls::task`. When triggered:
- Stops C simulation.
- Debug with `gdb` by checking which tasks are blocked on empty-channel reads.
- The Vitis HLS GUI visualizes blocked tasks.

**Causes of deadlock:**
1. Unbalanced production/consumption rates creating cycles.
2. Test bench providing insufficient data to drive all expected outputs.

---

## 5. Control-Driven TLP — Dataflow Pragma

### How It Works

`#pragma HLS dataflow` transforms a region of sequential C++ functions/loops into a **task-level pipeline** of concurrent processes. The tool:
1. Scans the function/loop body.
2. Extracts tasks from sub-function calls.
3. Infers communication channels (FIFO or PIPO) from shared C++ variables.
4. Inserts synchronization hardware automatically.

### Diamond Example

```cpp
void diamond(data_t vecIn[N], data_t vecOut[N]) {
    data_t c1[N], c2[N], c3[N], c4[N];
    #pragma HLS dataflow
    funcA(vecIn, c1, c2);   // reads vecIn; writes c1, c2
    funcB(c1, c3);           // reads c1; writes c3
    funcC(c2, c4);           // reads c2; writes c4 (parallel with funcB)
    funcD(c3, c4, vecOut);   // reads c3, c4; writes vecOut
}
```

**Performance impact (3 invocations):**

| Mode | Cycles per invocation | Notes |
|---|---|---|
| Sequential (no dataflow) | 475 | funcA→B→C→D serialized |
| With dataflow + FIFO channels | 275 | funcB and funcC run simultaneously; tasks overlap across invocations |

### Dataflow Achievable Throughput

$$\text{Throughput (PIPO)} \propto \frac{1}{\max(\text{latency of tasks})}$$
$$\text{Throughput (FIFO)} \propto \frac{1}{\min(\text{per-sample throughput of tasks})}$$

### What Dataflow Creates in Hardware

| Channel source | Default implementation | Override |
|---|---|---|
| `scalar` variables | FIFO | Automatic |
| `array` variables (sequential access) | PIPO or FIFO (user choice) | `#pragma HLS stream` |
| `array` variables (random access) | **PIPO only** | Cannot be FIFO |
| `hls::stream` in source | FIFO | Preserves type |
| `hls::stream_of_blocks` | Stream-of-Blocks | Preserves type |

> **Note:** The overlapped execution benefit is **only visible after C/RTL co-simulation** — not observable in pure C simulation.

---

## 6. Dataflow Region Coding Style (WYSIWYG / Canonical)

### Where `#pragma HLS dataflow` Can Be Applied

1. **Inside a function body** (function dataflow region).
2. **Inside a `for` loop** (loop dataflow region), provided:
   - The loop is the **only statement** in its enclosing function body.
   - Loop counter declared in the header (`int` type).
   - Initial value: non-negative integer literal.
   - Exit condition: `<` comparison against a non-negative constant or a scalar function argument.
   - Increment: positive integer constant.
   - No variable declarations outside the loop body.

### Canonical (WYSIWYG) Dataflow Requirements

The **body** of a canonical dataflow region must contain **only**:
- Local variable declarations **without initialization** (channels).
  - Use `__attribute__((no_ctor))` for types with non-empty default constructors.
- Sub-function calls (no type conversions or address computations in arguments).
- `hls::task` instantiations.

**No control structures** (`if`, `while`, nested loops) inside a canonical dataflow region body.

```cpp
// CANONICAL: recommended dataflow function
void dataflow(int Input0, int Input1[], int &Output0, int Output1[]) {
    #pragma HLS dataflow
    int C1[N], C2;                                        // uninitialized channels
    UserDataType C0 __attribute__((no_ctor));             // no default ctor
    func1(Input0, Input1, C0, C1);  // write C0, C1
    func2(C0, C1, C2);              // read C0,C1; write C2
    func3(C2, Output0, Output1);    // read C2; write Output0, Output1
}

// CANONICAL: loop dataflow region
void dataflow(int Input0, int Input1[], int &Output0, int Output1[], int N) {
    for (int i = 2; i < N; i += 2) {   // function body has only this loop
        #pragma HLS dataflow
        int C1[N], C2;
        UserDataType C0 __attribute__((no_ctor));
        func1(Input0, Input1, C0, C1, i);
        func2(C0, C1, C2, i);
        func3(C2, Output0, Output1, i);
    }
}
```

### Non-Canonical Dataflow

Non-canonical regions (containing loops, assignments, conditionals) are grouped into inferred processes by the tool. This is less predictable. Controlled by `syn.dataflow.strict_mode` (warning/error/disabled).

### Nested Dataflow Pitfalls

**Pitfall 1 — Missing `dataflow` pragma in intermediate function:**
```cpp
void proc2(...) {
    // Missing #pragma HLS dataflow here!
    proc1();  // proc1 has dataflow internally
}
void top(...) {
    #pragma HLS dataflow
    proc2(...);  // proc2 is sequential FSM → limits overlap
}
```

**Pitfall 2 — Code before/after a dataflow loop:**
```cpp
void proc2(...) {
    a = x + y;              // sequential FSM (NOT a dataflow process)
    for (int i = 0; i < N; i++) {
        #pragma HLS dataflow
        proc1(a, ...);
    }
}
```

> In both cases `proc2` becomes a sequential FSM: its `ap_ready` and `ap_done` fire simultaneously, eliminating the II < latency throughput benefit.

---

## 7. Advanced Dataflow Features

### Parameterized TLP via Unrolling and Partitioning

Create N identical parallel pipeline stages using a compile-time constant:

```cpp
// N-stage pipeline of worker processes connected by hls::streams
void dut(int in[M], int out[M]) {
    #pragma HLS dataflow
    hls_thread_local hls::stream<int> chan[N+1]; // auto-fully-partitioned
    read_in(in, chan[0]);
    hls_thread_local hls::task t[N];
    for (int i = 0; i < N; i++) {
        #pragma HLS unroll
        #pragma HLS dataflow
        t[i](worker, chan[i], chan[i+1]);
    }
    write_out(chan[N], out);
}

// Same with PIPO-based channels (arrays)
void dut(int in[M], int out[M]) {
    #pragma HLS dataflow
    int chan[N+1][M];
    #pragma HLS array_partition complete dim=1 variable=chan
    read_in(in, chan[0]);
    for (int i = 0; i < N; i++) {
        #pragma HLS unroll
        #pragma HLS dataflow
        worker(chan[i], chan[i+1]);
    }
    write_out(chan[N], out);
}
```

### Feedback Streams (Cyclic Dependencies)

`hls::stream` and `hls::stream_of_blocks` can pass data **backwards** (to lexically earlier processes) to model loop-carried dependencies. Use a guard to skip the first read:

```cpp
void read_and_add(int a[N], hls::stream<int> &b, hls::stream<int> &f, int i) {
    #pragma HLS pipeline II=1 style=flp  // flushing pipeline avoids deadlock
    int t = 0;
    if (i > 0) t = f.read();            // skip on first iteration
    b.write(a[i] + t);
}
void write_and_feedback(hls::stream<int> &a, int b[N], hls::stream<int> &f, int i) {
    #pragma HLS pipeline II=1 style=flp
    int aa = a.read();
    if (i < N-1) f.write(aa);           // feed back current sum
    b[i] = aa;
}
void dut(int a[N], int b[N]) {
    for (int i = 0; i < N; i++) {
        #pragma HLS DATAFLOW
        static hls::stream<int> f;  // feedback stream
        hls::stream<int> c;         // forward stream
        read_and_add(a, c, f, i);
        write_and_feedback(c, b, f, i);
    }
}
```

> **FLP pipelines** (`style=flp`) are **required** for pipelined loops inside feedback dataflow regions to prevent deadlock.

---

## 8. Configuring Dataflow Memory Channels

### FIFO vs PIPO Decision Table

| Array access pattern | Recommended channel | Constraint |
|---|---|---|
| Sequential (elements used in order) | **FIFO** (optional) or PIPO | FIFO: use `#pragma HLS stream variable=A` |
| Random (arbitrary access order) | **PIPO only** | FIFO not legal for random access |
| Need more producer-consumer slack | PIPO with depth > 2 | `#pragma HLS stream type=pipo depth=N` |

**PIPO default size:** 2× the original array size.  
**FIFO default depth:** computed by tool to optimize throughput; can be overridden.

```cpp
void top(...) {
    #pragma HLS dataflow
    int A[1024];
    #pragma HLS stream type=pipo variable=A depth=3  // 3-block PIPO
    producer(A, B, ...);
    middle(B, C, ...);
    consumer(A, C, ...);
}
```

### FIFO Sizing Workflow

| Step | Action |
|---|---|
| 1 | Set FIFO depth = max values transferred (size of array) |
| 2 | Run C/RTL co-simulation; confirm it passes |
| 3 | Reduce depth; re-run co-simulation |
| 4 | If co-sim fails, depth was too small → increase |

**Tools:** Vitis HLS IDE shows a **histogram of FIFO/PIPO usage over time** after co-simulation; also has an automatic FIFO sizing feature.

> **Deadlock note:** Incorrectly sized FIFOs cause stalls/deadlocks that are **only detectable during C/RTL co-simulation or in hardware** — not in C simulation.

### Global Dataflow Config

| Config option | Purpose |
|---|---|
| `syn.dataflow.default_channel` | Set global default: `pingpong` or `fifo` |
| `syn.dataflow.fifo_depth` | Global default FIFO/PIPO depth |
| `syn.dataflow.start_fifo_depth` | Size of auto-generated start propagation FIFOs |
| `syn.dataflow.scalar_fifo_depth` | Size of auto-generated scalar propagation FIFOs |
| `syn.dataflow.strict_mode` | Non-canonical dataflow: `warning` / `error` / `off` |

> Individual `#pragma HLS stream` for a variable **takes precedence** over the global option.

> **Important:** Use `volatile` qualifier on streamed arrays when needed to prevent dead-code-elimination by the C compiler, which could corrupt sequential access order.

---

## 9. Stream-of-Blocks (`hls::stream_of_blocks`)

A `stream_of_blocks` is a hybrid between FIFO streaming and PIPO block transfer. It allows the consumer to start processing a block **as soon as the producer releases it** (at lock release), rather than waiting for the producer function to return.

### Template

```cpp
#include "hls_streamofblocks.h"
hls::stream_of_blocks<block_type, depth> v;
// block_type: element type (array or multidimensional array)
// depth: total number of blocks (default = 2)
```

### Usage (RAII locking)

```cpp
typedef int buf[N];

void producer(hls::stream_of_blocks<buf> &s, ...) {
    for (int i = 0; i < M; i++) {
        hls::write_lock<buf> b(s);  // acquire block
        for (int j = 0; j < N; j++)
            b[f(j)] = ...;          // random-order write allowed
        // b destructor: release block to consumer
    }
}

void consumer(hls::stream_of_blocks<buf> &s, ...) {
    for (int i = 0; i < M; i++) {
        hls::read_lock<buf> b(s);   // acquire next block
        for (int j = 0; j < N; j++)
            ... = b[g(j)];          // random-order read
        // b destructor: release block for reuse by producer
    }
}

void top(...) {
    #pragma HLS dataflow
    hls::stream_of_blocks<buf> s;
    producer(s, ...);
    consumer(s, ...);
}
```

### Comparison: PIPO vs stream_of_blocks

| Property | PIPO | `stream_of_blocks` |
|---|---|---|
| Consumer start trigger | **Producer function returns** | **Producer releases `write_lock`** |
| Storage requirement (depth=2) | $2 \times M \times N$ elements | $2 \times N$ elements |
| Access pattern | Random | Random (within lock) |
| Binding to RAM type | Automatic | `BIND_STORAGE` pragma; default: `RAM_2P` |
| Deadlock risk | None | None (RAII locking) |

> **Note:** The producer's acquired block has **undefined initial state** — the producer must write all locations before the consumer reads them.

---

## 10. Compiler-Created FIFO Types

### Start Propagation FIFOs

Automatically created to propagate `ap_start`/`ap_ready` handshake to internal processes.
- Can become a **performance bottleneck** if undersized.
- Override with `syn.dataflow.start_fifo_depth`.
- Remove for unbounded producer/consumer slack (fully data-driven processes only): 
  ```cpp
  #pragma HLS DATAFLOW disable_start_propagation
  ```

### Scalar Propagation FIFOs

Automatically pass scalar values between processes.
- Can cause **deadlocks or performance issues** if incorrectly sized.
- Override with `syn.dataflow.scalar_fifo_depth`.

---

## 11. `#pragma HLS stable`

Removes task-level synchronizations for marked input/output variables of a dataflow region, when the caller guarantees stable access outside the region's execution window.

```cpp
void dataflow_region(int A[...], ...) {
    #pragma HLS stable variable=A
    #pragma HLS dataflow
    proc1(...);
    proc2(A, ...);  // without stable: proc1 blocked until proc2 is ready
}
```

**Without `stable`:** the dataflow region requires `proc2` to signal readiness before the region can restart, preventing overlapping iterations.

**With `stable`:** the compiler assumes `A` is not modified outside the region during execution — enables overlapping iterations.

---

## 12. Mixing Data-Driven and Control-Driven Models

Use `hls::split` / `hls::merge` channels to combine sequential dataflow functions with parallel `hls::task` workers:

```cpp
void dut(int in[N], int out[N], int n) {
    #pragma HLS dataflow
    hls_thread_local hls::split::round_robin<int, NP> split1;
    hls_thread_local hls::merge::round_robin<int, NP> merge1;

    read_in(in, n, split1.in);                     // control-driven

    hls_thread_local hls::task t[NP];
    for (int i = 0; i < NP; i++) {
        #pragma HLS unroll
        t[i](worker, split1.out[i], merge1.in[i]); // data-driven workers
    }

    write_out(merge1.out, out, n);                 // control-driven
}
```

**Rules for correct ordering:**
- Control-driven processes that **produce** streams for `hls::task` must be declared **before** the tasks.
- Control-driven processes that **consume** streams from `hls::task` must be declared **after** the tasks.
- Each `t[i](...)` call executes exactly once; the loop must be fully unrolled.
- Each task is statically bound to exactly one split output and one merge input.

**Scheduler options for split/merge:**

| Scheduler | Behavior |
|---|---|
| `round_robin` | Assigns data to workers in rotating order; deterministic |
| Load-balancing | Assigns to first available worker; **non-deterministic** simulation |

---

## 13. Summary: Choosing the Right TLP Model

| Use Case | Recommended Model |
|---|---|
| Purely streaming, no external memory (FFT/FIR with compiled config) | Data-driven `hls::task` |
| Memory-mapped kernel accessing DDR/HBM | Control-driven `#pragma HLS dataflow` |
| Dynamic multi-rate or feedback between processes | Data-driven `hls::task` |
| Load balancer with mutable routing table | Control-driven dataflow |
| Mix of memory access + streaming compute | Mixed model (`split`/`merge` + `hls::task` in dataflow) |
| Block-based data with early consumer start | `hls::stream_of_blocks` (hybrid) |

---

## 14. Best Practices

| Practice | Why |
|---|---|
| **Always use `hls_thread_local` on `hls::task` and its streams** | Without it, each function call creates a new state — breaks always-running semantics in C simulation |
| **Use canonical (WYSIWYG) dataflow form** | Direct 1:1 mapping to synthesized processes; predictable structure and performance |
| **Add `#pragma HLS dataflow` to every intermediate function in a nested hierarchy** | Missing pragma converts intermediate functions to sequential FSMs — eliminates TLP benefit |
| **Start with PIPO channels, switch to FIFO only for latency-sensitive paths** | PIPOs never deadlock; FIFOs require careful sizing |
| **Set FIFO depth conservatively then size down** | Start at array size; reduce while co-simulation passes |
| **Run C/RTL co-simulation to verify dataflow** | Overlapped execution is invisible in C simulation |
| **Use `hls::stream_of_blocks` when block boundaries matter for consumer latency** | Releases consumer earlier than PIPO (at lock release vs. function return) |
| **Pass constants to `hls::task` as template arguments** | Function arguments to `hls::task` must be streams; constants must be template params |
| **Use FLP pipelines (`style=flp`) inside tasks with feedback streams** | Standard pipelines cause deadlock when waiting for feedback data |
| **Avoid code before/after a dataflow loop in its enclosing function** | Any sequential code before the loop creates a blocking FSM that limits overlap |

---

### See Also

- [Chapter 28 — HLS Task Library](../section06_vitis_hls_libraries_reference/ch28_hls_task_library.md) — `hls::task` API reference
- [Chapter 24 — HLS Stream Library](../section06_vitis_hls_libraries_reference/ch24_hls_stream_library.md) — `hls::stream` blocking/non-blocking API
- [Chapter 30 — Stream of Blocks](../section06_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md) — `hls::stream_of_blocks` for array-based dataflow
- [Chapter 11 — Optimizing Techniques](ch11_optimizing_techniques.md) — Dataflow limitations, canonical dataflow coding style

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 2: Abstract Parallel Programming Model for HLS, Pages 39–64.*
