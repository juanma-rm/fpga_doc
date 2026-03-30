# Chapter 29 — HLS Split/Merge Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 829–833

## Table of Contents

- [Overview](#overview)
- [Specification Syntax](#specification-syntax)
- [Template Parameters](#template-parameters)
- [Scheduler Types](#scheduler-types)
- [Interface — Connecting to Processes](#interface--connecting-to-processes)
- [Example — Round-Robin with hls::task Workers](#example--round-robin-with-hlstask-workers)
- [Typical Use Case — Multi-Engine DDR/HBM Fanout](#typical-use-case--multi-engine-ddrhbm-fanout)
- [Best Practices](#best-practices)

---

## Overview

The `hls::split` and `hls::merge` templates implement **one-to-many** and **many-to-one** distribution channels for use in dataflow and task regions.

| Template | Direction | Use |
|---|---|---|
| `hls::split` | 1 input → N outputs | Fan out stream to N parallel workers |
| `hls::merge` | N inputs → 1 output | Collect results from N parallel workers |

**Header:**
```cpp
#include "hls_np_channel.h"
```

---

## Specification Syntax

```cpp
hls::split::round_robin  <DATATYPE, NUM_PORTS[, DEPTH[, N_PORT_DEPTH]]> name;
hls::split::load_balancing<DATATYPE, NUM_PORTS[, DEPTH[, N_PORT_DEPTH]]> name;

hls::merge::round_robin  <DATATYPE, NUM_PORTS[, DEPTH]> name;
hls::merge::load_balancing<DATATYPE, NUM_PORTS[, DEPTH]> name;
```

---

## Template Parameters

| Parameter | Description | Default |
|---|---|---|
| `DATATYPE` | Element type — same restrictions as `hls::stream` | required |
| `NUM_PORTS` | Number of output ports (split) or input ports (merge) | required |
| `DEPTH` | Main FIFO buffer depth | 2 |
| `N_PORT_DEPTH` | Per-output FIFO depth after split (split only) | — |

> `N_PORT_DEPTH` requires `DEPTH` to be specified first — both must be provided together.

---

## Scheduler Types

### Round-Robin

- Distributes tokens to output ports in a fixed rotating order.
- Deterministic — the i-th token always goes to port `(i % NUM_PORTS)`.
- Ideal when all workers process equal-size chunks.

### Load-Balancing

- Distributes tokens to whichever output port is available first.
- **Non-deterministic** — output order may vary between simulation runs.
- Test benches must be written to be order-agnostic (do not assume output ordering).
- Better throughput when tasks have variable processing time.

---

## Interface — Connecting to Processes

Split and merge channels expose `hls::stream`-compatible endpoints:

| Access | Type |
|---|---|
| `split_name.in` | `hls::stream&` — single input to the splitter |
| `split_name.out[i]` | `hls::stream&` — i-th output of the splitter |
| `merge_name.in[i]` | `hls::stream&` — i-th input to the merger |
| `merge_name.out` | `hls::stream&` — single output of the merger |

These can be passed directly to any process that accepts an `hls::stream` reference.

---

## Example — Round-Robin with hls::task Workers

```cpp
#include "hls_np_channel.h"
#include "hls_task.h"

const int NP = 4;

// Single worker: process one input value
void worker(hls::stream<int> &in, hls::stream<int> &out) {
    out.write(in.read() * 2);   // task body — implicit infinite loop
}

void top(int *input, int *output, int n) {
#pragma HLS dataflow

    hls::split::round_robin<int, NP> split1;
    hls::merge::round_robin<int, NP> merge1;

    // I/O processes (CDTLP side)
    read_in(input, n, split1.in);

    // NP parallel task instances (DTLP side)
    hls_thread_local hls::task t[NP];
    for (int i = 0; i < NP; i++) {
        t[i](worker, split1.out[i], merge1.in[i]);
    }

    write_out(merge1.out, output, n);
}
```

---

## Typical Use Case — Multi-Engine DDR/HBM Fanout

The primary motivation for `split`/`merge` is maximizing DDR or HBM bandwidth with multiple compute engines:

```
Producer (M_AXI burst read)
        ↓
    hls::split
   /    |    \
 Eng0  Eng1  Eng2     ← parallel hls::task workers
   \    |    /
    hls::merge
        ↓
Consumer (M_AXI burst write)
```

Steps:
1. Producer reads a burst from AXI master into a stream → feeds `split1.in`.
2. Split distributes packets across N worker engines.
3. Workers compute independently and push results to `merge1.in[i]`.
4. Merge collects results and feeds the consumer.
5. Consumer writes results back to AXI master.

This pattern allows a single M_AXI read/write port to feed multiple compute engines, maximizing utilization.

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Use round-robin when all workers execute the same number of cycles | Deterministic, simpler to debug |
| Use load-balancing for variable-latency workers | Better throughput; avoid pipeline stalls |
| Write test benches order-agnostic for load-balancing | Output order is non-deterministic |
| Specify `N_PORT_DEPTH` for burst-heavy workloads | Avoids output-side backpressure stalling the split arbitration |
| Pair split/merge with `hls::task` workers | Natural fit: workers run indefinitely, driven by split output streams |

---

### See Also

- [Chapter 24 — HLS Stream Library](ch24_hls_stream_library.md) — `hls::stream` fundamentals
- [Chapter 28 — HLS Task Library](ch28_hls_task_library.md) — Combining split/merge with `hls::task`
- [Chapter 2 — Abstract Parallel Programming](../section02_hls_programmers_guide/ch02_abstract_parallel_programming.md) — Parallel dataflow patterns

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 29, pages 829–833*
