# Chapter 1 — Design Principles
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Introduction & Motivation](#1-introduction--motivation)
2. [Throughput and Performance](#2-throughput-and-performance)
3. [Architecture Matters: CPU vs FPGA](#3-architecture-matters-cpu-vs-fpga)
4. [Three Paradigms for Programmable Logic](#4-three-paradigms-for-programmable-logic)
   - [Producer-Consumer Paradigm](#41-producer-consumer-paradigm)
   - [Streaming Data Paradigm](#42-streaming-data-paradigm)
   - [Pipelining Paradigm](#43-pipelining-paradigm)
5. [Combining the Three Paradigms](#5-combining-the-three-paradigms)
6. [Conclusion — A Prescription for Performance](#6-conclusion--a-prescription-for-performance)
7. [Best Practices](#7-best-practices)

---

## 1. Introduction & Motivation

This chapter is **tool-agnostic** — the concepts apply to most HLS flows, not just Vitis HLS specifically. Its goal is to bridge the mental gap between writing sequential software and writing software that can be **efficiently converted into hardware** by an HLS tool.

Two entry points for the reader:
- **Productivity-focused:** leverage C/C++ to avoid writing RTL.
- **Performance-focused:** accelerate a C/C++ algorithm onto custom hardware in programmable logic at higher throughput and lower power than CPU/GPU.

The core challenge is that **software written for CPUs and software written for FPGAs are fundamentally different**. Good hardware performance requires architectural thinking from the start.

---

## 2. Throughput and Performance

| Term | Definition |
|---|---|
| **Throughput** | Number of results produced per unit of time (e.g., samples/second, iterations/cycle) |
| **Memory bandwidth** | A specific form of throughput for memory systems |
| **Performance** | Higher throughput combined with lower power consumption |
| **Latency** | Total time for one item to pass through the entire system |
| **Initiation Interval (II)** | Time between producing successive outputs after the pipeline is full |

> **Key distinction:** reducing II improves throughput (total latency for many items) but does **not** reduce iteration latency (time for the first item).

$$\text{Total Latency} = \text{Iteration Latency} + II \times (N - 1)$$

where $N$ is the number of items processed.

---

## 3. Architecture Matters: CPU vs FPGA

### Traditional CPU Limitations

- The **von Neumann architecture** (7+ decades old) executes programs sequentially with a shared memory model.
- Multi-threading and multi-core CPUs provide parallelism but constrained by:
  - Fixed instruction set architecture.
  - Cache hierarchy and memory bandwidth bottlenecks.
  - Power consumption grows with frequency scaling.

### Why FPGAs Excel

| Capability | CPU | FPGA |
|---|---|---|
| Architecture | Fixed; general-purpose | Reconfigurable; custom macro-architecture |
| Parallelism | Thread/core-based; shared memory | Spatial mapping; custom datapaths |
| Granularity | Fixed ALUs, registers | From logic gates to full DSP blocks |
| Memory access | Cache-dependent | Custom memory hierarchy; burst-friendly |
| Power | High at high frequencies | Lower per operation |
| Producer-consumer overhead | Requires semaphores/mutexes | FIFO/PIPO — near-zero overhead |

- FPGAs allow **spatial mapping** of computation onto the device — different operations execute in dedicated hardware simultaneously.
- Modern FPGA devices also contain hardened **Arm processor cores** and IP blocks (DSP, memory controllers) usable without consuming programmable fabric.
- **Kernels** — composable units of logic — can be strategically placed to create application-specific macro-architectures.

---

## 4. Three Paradigms for Programmable Logic

HLS tools translate C/C++ into RTL by applying three fundamental architectural paradigms. Mastering these is the key to writing code that synthesizes into high-performance hardware.

### 4.1 Producer-Consumer Paradigm

**Core idea:** Decompose sequential processing into independent tasks where one task (the **producer**) generates data that another task (the **consumer**) processes — and allow them to run **concurrently**.

**Classic example:**

| Task | Role | Latency |
|---|---|---|
| Import Data | Source | 1s/item |
| Process Data | Producer | 2s/item |
| Write Output | Consumer | 1s/item |
| Export Data | Sink | 1s/item |

Sequential total for 100 items: **300 seconds**.  
With producer-consumer overlap: significantly reduced because Write Output starts as soon as the first item is processed.

**Communication channels between producer and consumer:**

| Channel Type | Properties | Use Case |
|---|---|---|
| **FIFO** (First-In-First-Out) | Queue; producer writes, consumer reads; consumer can start as soon as first item arrives | Streaming, varying rates |
| **PIPO** (Ping-Pong Buffer) | Double buffer; producer fills one half while consumer reads the other; automatic rate matching | Block transfers; deadlock-free |

Key properties of FIFO/PIPO channels:
- **No semaphores, mutexes, or monitors needed** — eliminates non-deterministic race conditions.
- Encapsulates synchronization into the channel itself — the rest of the design is **purely functional**.
- The result is a **dataflow network**: a stream of data enters, is processed, and exits.

> **Important design rule:** Encapsulate all memory reads as the **first** task and all memory writes as the **last** task. Reading or writing I/O in the middle of a compute step limits concurrency.

### 4.2 Streaming Data Paradigm

**A stream** is an unbounded, continuously updating data sequence — unknown or unlimited size — flowing **unidirectionally** from a source (producer) to a destination (consumer).

**Why streaming matters in hardware:**

| Software | Hardware |
|---|---|
| Random memory access is nearly free (cached) | Sequential access patterns map to streams efficiently |
| Synchronization managed by OS primitives | Synchronization implicit in FIFO/PIPO channels |
| Parallelism via threads; shared memory model | Parallelism via independent tasks with stream channels |

**FIFO deadlock risk:** In designs with multiple producers and consumers, improperly sized FIFOs can cause deadlock (both sides stall waiting for the other). PIPO avoids this via automatic rate matching.

**Streaming dataflow network example:**

```
Task 1 (random) ──► FIFO ──┐
                             ├──► Task 3 (sum) ──► FIFO ──► Task 4 (print)
Task 2 (random) ──► FIFO ──┘
```

- FIFOs abstract away the parallel behavior — the programmer only reasons about what each task does when it is active.
- The paradigm can be applied **hierarchically**: a streaming network of streaming networks.

> **Block size trade-off:** A block of data can be one value or $N$ values. Larger blocks increase throughput but require more memory resources.

### 4.3 Pipelining Paradigm

**Pipelining** overlaps the execution of multiple instances of a sequential workflow by using dedicated, reusable hardware stages.

**Car factory analogy:**

| Stage | Time |
|---|---|
| A: Install engine | 20 min |
| B: Install doors | 20 min |
| C: Install wheels | 20 min |

| Execution Mode | 3 cars | Throughput |
|---|---|---|
| Sequential (one station) | 180 min | 1 car / 60 min |
| Pipelined (3 stations) | 100 min | 1 car / 20 min |

- **Iteration latency = 60 min** (time for the first car).
- **II = 20 min** (time between successive outputs once pipeline is full).
- **Total latency** = 60 + 20 × 2 = 100 min.

**Pipelining applies at multiple abstraction levels:**

| Level | Applies To | Mechanism |
|---|---|---|
| **Instruction-level (ILP)** | Operations within a loop body | `#pragma HLS PIPELINE` |
| **Loop-level** | Loop iterations | `#pragma HLS PIPELINE` on loop |
| **Task-level** | Functions in a dataflow network | `#pragma HLS DATAFLOW` |

> **Bottleneck rule:** Pipeline throughput is bounded by its **slowest stage**. Balance stage latencies to achieve II = 1.

> **Static vs. dynamic:** Low-level instruction pipelining is a **static** optimization — it requires known stage latencies. It **cannot** be applied to dataflow networks with data-dependent latencies.

---

## 5. Combining the Three Paradigms

### Functions and Loops as Hardware Units

- Each **function** synthesizes into a dedicated hardware component (like a class with hardware instances).
- **Inlining** small functions merges their logic into the caller — can improve resource sharing but increases control complexity.
- **Loops** are the primary target of pipeline and unroll optimizations.

### The Diamond Pattern: Three Execution Modes

Consider four functions A, B, C, D where A fans out to B and C (independent), and D joins their outputs:

```cpp
void diamond(data_t vecIn[N], data_t vecOut[N]) {
    data_t c1[N], c2[N], c3[N], c4[N];
    #pragma HLS dataflow
    A(vecIn, c1, c2);
    B(c1, c3);
    C(c2, c4);
    D(c3, c4, vecOut);
}
```

**Execution mode comparison for 2 runs:**

| Mode | Concurrency | Channel Type | Property |
|---|---|---|---|
| **Sequential** | None; A→B→C→D serialized | N/A | Baseline; black-circle sync between all tasks |
| **Task Parallel within a run** | B ∥ C (fork-join) | Arrays / PIPOs | Expressed as (A; (B ∥ C); D) per run; runs still serialized |
| **Task Parallel + Pipelined across runs** | B ∥ C within each run; run 2 starts while run 1 B/C execute | **PIPOs** | Throughput ∝ max(latency of A,B,C,D); requires double-buffering |
| **Full pipeline with intra-run overlap** | B and C start before A completes; D starts before B/C complete | **FIFOs** | Best throughput; risk of deadlock if FIFOs incorrectly sized |

**Series-parallel task graphs** — any DAG of dependent tasks can be expressed with nested fork-join synchronization.

**Performance formula:**
$$\text{Throughput} \propto \frac{1}{\max(\text{task latencies})} \quad \text{(pipelined, PIPO)}$$
$$\text{Throughput} \propto \frac{1}{\min(\text{task throughputs})} \quad \text{(fully streamed, FIFO)}$$

---

## 6. Conclusion — A Prescription for Performance

The unifying principle: **state and sequential logic are compartmentalized in modular tasks; tasks communicate via streams**.

Benefits of streaming-based design:
1. Enables both task-level and instruction-level pipelining.
2. Eliminates locks, race conditions, and non-deterministic parallel programming.
3. Simpler code with cleaner interfaces.
4. Allows tools (compiler, scheduler) to identify and exploit parallelism automatically.

### Performance Checklist

| Priority | Action |
|---|---|
| 1 | Accept that **software for FPGAs ≠ software for CPUs** — do not optimize portability at the expense of performance |
| 2 | Establish a **functional verification flow** from day one (reference model, golden vectors) |
| 3 | Focus on **macro-architecture first** — identify producers, consumers, and communication channels before writing code |
| 4 | Draw an **activity timeline** — horizontal axis = time, each function plotted across multiple iterations — before coding anything |
| 5 | Begin coding **only after** macro-architecture and activity timeline are established |
| 6 | Put sequential code blocks that need to run concurrently into **dedicated functions** (HLS infers TLP from function calls, not raw loop bodies) |
| 7 | Decompose into **small modular components** communicating via streams |
| 8 | Avoid **wide communication channels** — decompose into multiple narrower channels |
| 9 | Aim for **one loop nest per function** with fixed or annotated bounds — this simplifies throughput measurement and optimization |
| 10 | Study the **critical path** (e.g., A→B→D or A→C→D) and identify bottleneck tasks |
| 11 | Choose FIFO vs PIPO **deliberately**: PIPO = deadlock-free; FIFO = earlier overlap, requires careful sizing |
| 12 | Use **HLS compiler reports and GUIs** to verify achieved parallelism matches expected activity timeline |
| 13 | Learn synthesizable C/C++ coding styles (see Chapter 7) |

---

## 7. Best Practices

| Practice | Rationale |
|---|---|
| **Split load/compute/store into separate functions** | Enables maximal overlap of I/O with computation; isolates memory access for burst inference |
| **Keep functions small with simple control flow** | Large functions with complex control paths are harder for HLS schedulers to optimize |
| **Use streams (hls::stream) for inter-task communication** | Native FIFO semantics; consumer starts as soon as first element is produced |
| **Use PIPOs for block-level communication** | Automatic rate matching; eliminates deadlock risk; simpler to size than FIFOs |
| **Annotate variable loop bounds with LOOP_TRIPCOUNT** | Required for accurate latency and throughput estimates in HLS reports |
| **Never place I/O accesses in the middle of computation** | Breaks producer-consumer overlap; reduces available concurrency |
| **Replicate small modular tasks to increase parallelism** | Modular components can be instantiated multiple times; wide monolithic functions cannot |
| **Profile the slowest stage (bottleneck) first** | Pipelining throughput is limited by the slowest stage — optimization effort should target it |
| **Verify streaming designs with simulation waveforms** | Misaligned producer/consumer rates show up as FIFO stalls in RTL simulation |

---

### See Also

- [Chapter 2 — Abstract Parallel Programming](ch02_abstract_parallel_programming.md) — Dataflow, `hls::task`, control/data-driven TLP
- [Chapter 3 — Loops Primer](ch03_loops_primer.md) — Pipelining, unrolling, loop optimization
- [Section I — Introduction](../section1_introduction/section_intro.md) — HLS overview, refactoring patterns, load-compute-store

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 1: Design Principles, Pages 24–38.*
