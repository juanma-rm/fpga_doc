# Chapter 30 — HLS Stream of Blocks Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 834–842

## Table of Contents

- [Overview](#overview)
- [The Problem with PIPOs](#the-problem-with-pipos)
- [Template Declaration](#template-declaration)
- [RAII Locking — write_lock and read_lock](#raii-locking--write_lock-and-read_lock)
- [Comparison: PIPO vs stream_of_blocks](#comparison-pipo-vs-stream_of_blocks)
- [Feedback Loop Example](#feedback-loop-example)
- [Status Methods](#status-methods)
- [RTL Interface — Handshake Signals](#rtl-interface--handshake-signals)
- [BIND_STORAGE Pragma](#bind_storage-pragma)
- [Limitations](#limitations)
- [Best Practices](#best-practices)

---

## Overview

`hls::stream_of_blocks` is a dataflow channel that enables **producer/consumer overlap at sub-function granularity** through RAII-style locks. It eliminates the "return-before-start" constraint of PIPOs (ping-pong buffers).

**Header:**
```cpp
#include "hls_streamofblocks.h"
```

**Template:**
```cpp
hls::stream_of_blocks<block_type[, depth]> channel_name;
```

---

## The Problem with PIPOs

With standard PIPO (producer fills array, dataflow swaps buffer, consumer drains), the consumer **cannot start until the producer's function returns**. There is no way to overlap execution at the element level.

`stream_of_blocks` solves this:
- The producer acquires a `write_lock`, writes random-access to the block, then **releases the lock when the `write_lock` object goes out of scope** (destructor).
- The consumer can immediately acquire the block (via `read_lock`) as soon as the producer releases it — **without waiting for the producer function to return**.

---

## Template Declaration

```cpp
hls::stream_of_blocks<buf, depth> s;
```

| Parameter | Description | Default |
|---|---|---|
| `block_type` | Type of the block — typically a fixed-size array type | required |
| `depth` | Total number of blocks (includes producer-held + consumer-held) | 2 |

Example:
```cpp
typedef int block_t[N];                          // block = array of N ints
hls::stream_of_blocks<block_t, 2> s;             // 2 blocks in flight
```

---

## RAII Locking — write_lock and read_lock

Both locks follow RAII semantics: the resource is acquired at construction and released at destruction (scope exit).

### Producer (write_lock)

```cpp
// Producer function
void producer(hls::stream_of_blocks<buf> &s, ...) {
    for (...) {
        hls::write_lock<buf> block(s);    // acquire block — constructor
        // Random-access write to block
        block[f(j)] = compute_value();
    }
    // block released at end of scope — consumer can now acquire it
}
```

### Consumer (read_lock)

```cpp
// Consumer function
void consumer(hls::stream_of_blocks<buf> &s, ...) {
    for (...) {
        hls::read_lock<buf> block(s);     // acquire block — constructor
        // Random-access read from block
        result = process(block[g(j)]);
    }
    // block released at end of scope
}
```

### Top-Level (Dataflow)

```cpp
void top(int M, int N, hls::stream<int> &in, hls::stream<int> &out) {
#pragma HLS dataflow
    hls::stream_of_blocks<int[N]> channel;  // shared channel

    producer(channel, M, N, in);
    consumer(channel, M, N, out);
}
```

---

## Comparison: PIPO vs stream_of_blocks

| Feature | PIPO (array) | stream_of_blocks |
|---|---|---|
| Consumer start point | After producer function returns | After write_lock released (scope exit) |
| Memory usage | 2 × M × N elements | 2 × N elements (depth=2) |
| Random access | Yes | Yes (via lock object) |
| Feedback flow support | No (producer always before consumer) | Yes |
| Dataflow required | Yes | Yes |
| Multiple producers | Possible | No — single producer only |
| Multiple consumers | Possible | No — single consumer only |

---

## Feedback Loop Example

`stream_of_blocks` supports **feedback flows** where the consumer runs before the producer in call order — something impossible with standard PIPOs:

```cpp
void top(...) {
#pragma HLS dataflow
    hls::stream_of_blocks<int[N]> feedback;

    consumer(feedback, ...);   // consumer declared first
    producer(feedback, ...);   // producer declared after
}
```

In this model, the consumer reads the previous iteration's block while the producer writes the next one, achieving a true feedback channel with concurrent execution.

---

## Status Methods

| Method | Returns | Description |
|---|---|---|
| `.empty()` | `bool` | True if no block is available for reading; consumer check before acquiring `read_lock` |
| `.full()` | `bool` | True if no block is available for writing; producer check before acquiring `write_lock` |

Use these to avoid stalling lock acquisition when the pipeline needs backpressure hints.

---

## RTL Interface — Handshake Signals

`stream_of_blocks` generates different handshake signals than PIPOs:

| Signal | PIPO | stream_of_blocks |
|---|---|---|
| Consumer ready to read | `ap_start` / `ap_ready` | `read_n` / `empty_n` |
| Consumer done reading | `ap_done` / `ap_continue` | `read_n` / `empty_n` |
| Producer ready to write | `ap_start` / `ap_ready` | `write_n` / `full_n` |
| Producer done writing | `ap_done` / `ap_continue` | `write_n` / `full_n` |

---

## BIND_STORAGE Pragma

By default, `stream_of_blocks` maps storage to 2-port block RAM (`RAM_2P`). Override with:

```cpp
#pragma HLS BIND_STORAGE variable=channel type=RAM_2P impl=BRAM
```

---

## Limitations

| Limitation | Details |
|---|---|
| Single producer and single consumer | Two separate processes; cannot share one lock between multiple producers or consumers |
| Dataflow context required | Cannot be used in sequential regions |
| No nested locks | Cannot hold two `read_lock` or `write_lock` objects in the same scope simultaneously |
| Sequential locks in IF/ELSE ok | Mutually exclusive locks (in branches) and sequential locks (one lock, then another after release) are supported |
| Explicit release not recommended | Use scope-based RAII; avoid explicit `.release()` calls unless `#define EXPLICIT_ACQUIRE_RELEASE` is set |

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Prefer `stream_of_blocks` over PIPO when producer and consumer touch different rows of a 2D array | Reduces memory from 2×M×N to 2×N elements |
| Use `depth > 2` when the producer/consumer runtime imbalance is large | Deeper queue avoids stalling; each extra level costs one additional block of storage |
| Check `.empty()` / `.full()` before acquiring lock in latency-sensitive code | Avoids stalling the caller when blocks are not ready |
| Declare `stream_of_blocks` at the dataflow top level, not inside functions | Dataflow channels must be at the scope visible to both producer and consumer |
| Use feedback ordering (consumer declared before producer) only when required | Makes intent explicit; tool enforces correct direction automatically |

---

### See Also

- [Chapter 24 — HLS Stream Library](ch24_hls_stream_library.md) — Scalar-element `hls::stream` API
- [Chapter 4 — Arrays Primer](../section2_hls_programmers_guide/ch04_arrays_primer.md) — Array partitioning and access patterns
- [Chapter 2 — Abstract Parallel Programming](../section2_hls_programmers_guide/ch02_abstract_parallel_programming.md) — Dataflow with array channels

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 30, pages 834–842*
