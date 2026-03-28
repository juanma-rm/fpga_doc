# Chapter 9: Best Practices for Designing with M_AXI Interfaces

> **Source:** Vitis HLS User Guide UG1399 v2025.2, Chapter 9, Pages 257–259

---

## Table of Contents
1. [Overview and Goals](#1-overview-and-goals)
2. [Load–Compute–Store (LCS) Pattern](#2-loadcomputestore-lcs-pattern)
3. [Hardware Data Flow Mindset](#3-hardware-data-flow-mindset)
4. [Global Memory Access Strategy](#4-global-memory-access-strategy)
5. [Port Width Maximization](#5-port-width-maximization)
6. [Memory Resource Selection](#6-memory-resource-selection)
7. [Concurrent Port Configuration](#7-concurrent-port-configuration)
8. [Burst Length Configuration](#8-burst-length-configuration)
9. [Outstanding Requests Configuration](#9-outstanding-requests-configuration)
10. [Best Practices Summary](#10-best-practices-summary)

---

## 1. Overview and Goals

When designing a Vitis kernel that accesses external device memory (DDR, HBM, PLRAM), throughput is the primary optimization objective. The compute part and the **data transfer overhead** both contribute to total application latency.

The key design principle: **overlap computation with communication** by structuring the kernel as a pipeline of concurrent producer–consumer tasks.

---

## 2. Load–Compute–Store (LCS) Pattern

Decompose the kernel into three task types:

```
 ┌─────────┐    hls::stream    ┌─────────┐    hls::stream    ┌──────────┐
 │  Load   │ ───────────────►  │ Compute │ ───────────────►  │  Store   │
 │ (m_axi) │                   │ (local) │                   │ (m_axi)  │
 └─────────┘                   └─────────┘                   └──────────┘
```

**Rules for Load/Store tasks:**
- All external I/O through m_axi **must** be in Load and Store tasks only
- Use **multiple Load or Store tasks** if the kernel must read/write from different ports in parallel
- Pass data between tasks via `hls::stream` or internal arrays (not through m_axi)

**Rules for Compute tasks:**
- Only accept scalars, local arrays, streams, or `stream_of_blocks` arguments
- No direct m_axi access
- Can be further split into smaller pipelined sub-tasks (same LCS rules apply recursively)
- Always use **local memory** to buffer data between Load → Compute → Store

**Enabling task-level parallelism:**
- All tasks specified as functions (or top-level loop bodies)
- `#pragma HLS DATAFLOW` enables concurrent execution
- Each task runs in its own pipeline stage, overlapping execution

```cpp
extern "C" void kernel(int *in, int *out, int n) {
#pragma HLS DATAFLOW
    hls::stream<int> load_to_compute("l2c");
    hls::stream<int> compute_to_store("c2s");

    load(in, load_to_compute, n);       // m_axi → internal stream
    compute(load_to_compute, compute_to_store, n);  // pure compute
    store(compute_to_store, out, n);    // internal stream → m_axi
}
```

---

## 3. Hardware Data Flow Mindset

| Aspect | Software Thinking | Hardware Thinking |
|---|---|---|
| Data access model | Algorithm **pulls** data it needs | Data **flows** (pushed) through the algorithm |
| Indexing | Array indices — "where" is data? | Streams — "when" does data arrive? |
| Optimization goal | Minimize cache misses, random access OK | Maximize sequential access, minimize DRAM transactions |

**Practical implication:** If the algorithm naturally accesses data in column-major order but DRAM is row-major, consider transposing the data in software before passing it to the kernel. Eliminating a complex hardware address-translation block simplifies the HLS design significantly.

---

## 4. Global Memory Access Strategy

Global memories have **high latency** and **limited bandwidth**. Key rules:

1. **Access contiguous blocks** — use AXI burst transfers; random or strided access disables burst inference
2. **Sequential access** → larger bursts → higher throughput efficiency
3. **Avoid redundant accesses** — every DRAM read/write consumes bandwidth; cache locally when data is reused
4. **Create internal caching structures** when the sequential order required by the Compute task differs from the DRAM layout order

**Example — caching for reorder:**
```cpp
// Instead of random access to global memory:
// out[i] = in[col_idx[i]];  // breaks burst!

// Pre-load a tile, process locally:
void load_tile(int *in, int tile[TILE_SIZE], int base) {
    for (int i = 0; i < TILE_SIZE; i++) {
#pragma HLS PIPELINE II=1
        tile[i] = in[base + i];   // sequential burst
    }
}
```

---

## 5. Port Width Maximization

**Target: 512-bit (64-byte) port width.** Wider ports maximize DRAM bandwidth utilization.

Practical peak throughput (PCIe-limited):
- Read: ~10–17 GB/s
- Write: ~10–17 GB/s

```cpp
// Use ap_uint<512> or hls::vector to get 512-bit wide interface:
#include "ap_int.h"
typedef ap_uint<512> wide_t;

void kernel(wide_t *in, wide_t *out, int n) {
#pragma HLS INTERFACE mode=m_axi port=in  bundle=gmem0 \
    max_read_burst_length=64 num_read_outstanding=32
#pragma HLS INTERFACE mode=m_axi port=out bundle=gmem1 \
    max_write_burst_length=64 num_write_outstanding=32
    for (int i = 0; i < n; i++) {
#pragma HLS PIPELINE II=1
        out[i] = in[i];   // 512-bit burst read + write
    }
}
```

**Avoid structs on m_axi interfaces** — they inhibit auto port widening and degrade burst performance. Disaggregate struct members into separate primitive arrays if needed.

**Key insight:** One large DRAM transfer >> many small transfers. Minimize the number of distinct AXI transactions.

---

## 6. Memory Resource Selection

| Memory Type | Size | Latency | Notes |
|---|---|---|---|
| PLRAM | Small | Very low | On-chip; fastest; best for small control data |
| HBM | Moderate | Low-moderate | 32 channels; good for medium datasets needing parallelism |
| DDR | Large | High | 4 banks on most FPGAs; high bandwidth but high latency |
| Distributed RAM (LUT) | Very small | 1 cycle | Read-immediate; ideal for small fast buffers / ROMs |
| Block RAM | Medium | 2 cycles | Better than LUTRAM for sizes >128 bits; lower power |
| UltraRAM | Large | ~3 cycles | Best for large on-chip buffers |

**Rule of thumb for on-chip buffers:**
- Use distributed RAM (LUTRAM) for small buffers (≤128-bit capacity) or ROMs
- Use BRAM or URAM for anything larger — better performance and lower power

---

## 7. Concurrent Port Configuration

- If the Load task needs multiple datasets simultaneously, use **multiple m_axi bundles** accessing different memory banks
- Data in the **same bank / same port** is always serialized by an arbiter — parallelism requires physical separation

**Parallelism limits:**
| Memory Type | Max Independent Channels |
|---|---|
| DDR | 4 banks per device |
| HBM | 32 channels per device |

```cpp
// Example: two independent load channels
void load_ab(int *a, int *b, hls::stream<int> &sa, hls::stream<int> &sb, int n) {
#pragma HLS INTERFACE mode=m_axi port=a bundle=gmem0
#pragma HLS INTERFACE mode=m_axi port=b bundle=gmem1
    // gmem0 and gmem1 can run in parallel if mapped to different banks
}
```

---

## 8. Burst Length Configuration

**Target burst length:** 4 KB per transfer

$$\text{burst\_length} = \frac{4096 \text{ bytes}}{\text{port\_width\_bytes}}$$

For a 512-bit (64-byte) port:
$$\text{burst\_length} = \frac{4096}{64} = 64 \text{ transfers}$$

```cpp
#pragma HLS INTERFACE mode=m_axi port=in \
    max_read_burst_length=64 \    // = 4096 / 64 bytes for 512-bit port
    max_write_burst_length=64
```

**Why bursts matter:** Each AXI transaction has an address-phase overhead. Longer bursts amortize this overhead over more data words, improving effective bandwidth and hiding memory latency.

---

## 9. Outstanding Requests Configuration

`num_read_outstanding` / `num_write_outstanding` sets the depth of the request/response pipeline:

- Higher → more requests in flight → better latency hiding at the cost of BRAM (data buffer depth = num_outstanding × burst_length)
- Start with 16–32; increase if the design stalls waiting for memory

$$\text{data FIFO depth (words)} = \text{num\_outstanding} \times \text{max\_burst\_length}$$

For 32 outstanding × 64 burst length with 512-bit (8 bytes) data:
$$8 \text{ bytes/word} \times 32 \times 64 = 16{,}384 \text{ bytes} = 16\text{ KB of BRAM}$$

---

## 10. Best Practices Summary

| Category | Recommendation |
|---|---|
| **Architecture** | Structure all kernels as Load–Compute–Store with `DATAFLOW` |
| **I/O placement** | All m_axi accesses in Load/Store tasks only; Compute is m_axi-free |
| **Port width** | Target 512-bit ports; use `ap_uint<512>` or `hls::vector<T,N>` |
| **Burst access** | Always access m_axi sequentially; avoid random/conditional indexing |
| **Structs** | Avoid structs on m_axi; use primitive arrays or disaggregate |
| **Burst length** | Set `max_burst_length = 4096 / port_width_bytes` (= 64 for 512-bit) |
| **Parallelism** | Use separate `bundle=` per port; map to different DDR banks / HBM channels |
| **Memory banks** | DDR: up to 4 parallel; HBM: up to 32 parallel |
| **Outstanding** | Start with 16–32; balance latency-hiding against BRAM cost |
| **Caching** | Buffer tiles locally when compute order ≠ DRAM storage order |
| **Data layout** | Prefer transposing data in software over building hardware transposers |
| **Latency hiding** | One large transfer >> many small; always fill burst to 4 KB |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 9: Best Practices for Designing with M_AXI Interfaces, Pages 257–259.*
