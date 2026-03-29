# Chapter 24 — HLS Stream Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 796–807

## Table of Contents

- [Overview](#overview)
- [C Modeling and RTL Implementation](#c-modeling-and-rtl-implementation)
- [Using HLS Streams](#using-hls-streams)
  - [Declaration](#declaration)
  - [Stream Naming](#stream-naming)
  - [Passing Streams Between Functions](#passing-streams-between-functions)
- [Blocking API](#blocking-api)
  - [Blocking Write](#blocking-write)
  - [Blocking Read](#blocking-read)
  - [Deterministic Behavior](#deterministic-behavior)
- [Non-Blocking API](#non-blocking-api)
  - [Non-Blocking Write](#non-blocking-write)
  - [Non-Blocking Read](#non-blocking-read)
- [Status Query Methods](#status-query-methods)
  - [capacity()](#capacity)
  - [empty()](#empty)
  - [full()](#full)
  - [size()](#size)
- [Controlling the RTL FIFO Depth](#controlling-the-rtl-fifo-depth)
- [Best Practices](#best-practices)

---

## Overview

`hls::stream<>` is a C++ template class for modeling streaming data in Vitis HLS. Streaming transfers data samples sequentially from first to last, requiring no address management.

**Header:**
```cpp
#include "hls_stream.h"
```

> **Important:** `hls::stream` is **only** available in C++ designs.

### Key Attributes

| Attribute | Description |
|---|---|
| Infinite FIFO in C | No depth specification required during C code simulation |
| Sequential access | Data is consumed on read — cannot be re-read |
| Top-level interface | `ap_fifo` (Vivado IP flow) or `axis` (Vitis kernel flow) by default |
| Internal FIFO depth | Default depth = 2; adjustable with `STREAM` pragma/directive |
| Definition scope | Local or global; global streams follow global variable rules |

---

## C Modeling and RTL Implementation

In C simulation (`csim`), streams behave as infinite queues. In RTL, they map to FIFOs.

| Context | Default implementation | Default depth |
|---|---|---|
| Top-level argument (Vivado IP flow) | `ap_fifo` interface | N/A (interface ports) |
| Top-level argument (Vitis kernel flow) | `axis` (AXI4-Stream) | N/A |
| Internal stream (inside design function) | FIFO | 2 |

**Non-DATAFLOW vs DATAFLOW:**

| Region | Behavior | Risk |
|---|---|---|
| Non-DATAFLOW | Tasks run sequentially; producer fills FIFO before consumer starts | FIFO underrun/deadlock if depth < produced samples |
| DATAFLOW | Tasks run concurrently; streams flow between overlapping tasks | FIFO depth = 2 is usually sufficient |

When an internal stream with default depth is used outside a DATAFLOW region, Vitis HLS emits:
```
ERROR: [XFORM 203-733] An internal stream xxxx with default size is used in a
non-dataflow region, which may result in deadlock. Please consider to resize
the stream using the directive 'set_directive_stream' or the 'HLS stream' pragma.
```

**Rule:** Each `hls::stream<>` object must be written by exactly one process and read by exactly one process.

---

## Using HLS Streams

### Declaration

Two declaration forms:

```cpp
#include "ap_int.h"
#include "hls_stream.h"

typedef ap_uint<128> uint128_t;

// Form 1: type only — FIFO depth = 2 in RTL
hls::stream<uint128_t> my_wide_stream;

// Form 2: type + depth — explicit FIFO depth for RTL co-sim
hls::stream<uint128_t, 16> my_buffered_stream;
```

The type `T` in `hls::stream<T>` may be:
- Any C++ native data type
- Vitis HLS arbitrary precision types (`ap_int<>`, `ap_ufixed<>`, etc.)
- User-defined structs containing the above

> **Note:** General user-defined **classes** with member functions should not be used as the stream type.

**Namespace shorthand:**
```cpp
#include <hls_stream.h>
using namespace hls;
stream<uint128_t> my_wide_stream;   // hls:: prefix no longer needed
```

### Stream Naming

Streams can be optionally named for improved diagnostic messages:

```cpp
hls::stream<uint8_t> bytestr_in1;                     // unnamed
hls::stream<uint8_t> bytestr_in2("input_stream2");    // named
```

Unnamed streams produce anonymous warnings; named streams produce readable ones:
```
WARNING: Hls::stream 'hls::stream<unsigned char>.1' contains leftover data...
WARNING: Hls::stream 'input_stream2' contains leftover data...
```

### Passing Streams Between Functions

Streams **must always** be passed by reference:

```cpp
void stream_function(
    hls::stream<uint8_t> &strm_out,
    hls::stream<uint8_t> &strm_in,
    uint16_t              strm_len
);
```

---

## Blocking API

The blocking API stalls until data is available (read) or space is available (write). It is fully deterministic when used correctly.

> **Caution:** Blocking mode can deadlock if streams are insufficiently sized.

### Blocking Write

```cpp
hls::stream<int> my_stream;
int src_var = 42;

// Method 1: explicit write
my_stream.write(src_var);

// Method 2: << operator (stream insertion style)
my_stream << src_var;
```

### Blocking Read

```cpp
hls::stream<int> my_stream;
int dst_var;

// Method 1: read into variable
my_stream.read(dst_var);

// Method 2: assignment (reads and returns value)
dst_var = my_stream.read();

// Method 3: >> operator (stream extraction style)
my_stream >> dst_var;
```

### Deterministic Behavior

Blocking API is deterministic only in specific usage patterns:

**Case 1 — Simple read/write:**
```cpp
int data = in.read();
if (data >= 10)
    out1.write(data);
else
    out2.write(data);
```

**Case 2 — Full/empty checks with no side effects:**
```cpp
#pragma HLS dataflow
void p1(hls::stream<...> &s1, ...) {
    if (s1.empty()) return;
    ... = s1.read();
}
void p2(hls::stream<...> &s2, ...) {
    if (s2.full()) return;
    s2.write(...);
}
```

**Non-deterministic anti-pattern** (avoid):
```cpp
// BAD: C-sim will always drain; hardware may exit early on bubble
while (!s.empty()) {
    s.read();
}

// GOOD: use tlast side-channel signal
while (!tlast) {
    s1.read();
}
```

---

## Non-Blocking API

Non-blocking methods return `bool` (true = success, false = failure). They do **not** stall on empty/full conditions.

> **Important:** Only `ap_fifo` protocol fully supports non-blocking. AXI4-Stream (`axis`) only supports non-blocking reads.

> **Warning:** Non-blocking behavior may be non-deterministic between C simulation (infinite FIFO) and RTL simulation (bounded FIFO). Requires a comprehensive RTL test bench.

> **Important:** If `ap_ctrl_none` is used and any stream employs non-blocking behavior, C/RTL co-simulation is not guaranteed to complete.

### Non-Blocking Write

```cpp
hls::stream<int> my_stream;
int src_var = 42;

// Returns true if write succeeded
if (my_stream.write_nb(src_var)) {
    // normal path
} else {
    // FIFO was full — write did not occur
    return;
}
```

Non-blocking write with manual full check:
```cpp
bool stream_full = my_stream.full();
if (!stream_full)
    my_stream.write_nb(src_var);
```

### Non-Blocking Read

```cpp
hls::stream<int> my_stream;
int dst_var;

// Returns true if read succeeded
if (my_stream.read_nb(dst_var)) {
    // normal path
} else {
    // FIFO was empty — read did not occur
    return;
}
```

Non-blocking read in a loop:
```cpp
READ_ONLY_LOOP:
while (check != 0) {
    if (!addr_strm.empty()) {
        addr_strm.read_nb(addr_for_HBM);
        hbm[addr_for_HBM] = some_data;
    }
    check = (check << 1);
}
```

---

## Status Query Methods

### capacity()

```cpp
unsigned int hls::stream<T>::capacity();
```

Returns the maximum number of elements the stream can hold (total FIFO depth).

- In C simulation: returns `MAXINT` (theoretical infinite capacity).
- In synthesis / RTL co-simulation: returns the computed FIFO depth.

**Usage — write only when enough space exists:**
```cpp
if ((my_stream.capacity() - my_stream.size()) >= N) {
    for (int i = 0; i < N; i++)
        my_stream.write(...);   // guaranteed non-blocking
}
```

---

### empty()

```cpp
bool hls::stream<T>::empty();
```

Returns `true` if the stream contains no elements.

```cpp
bool stream_empty = my_stream.empty();
```

> `empty()` applies to **input** FIFOs only (cannot be applied to output FIFOs).

---

### full()

```cpp
bool hls::stream<T>::full();
```

Returns `true` if and only if the stream is at capacity.

```cpp
bool stream_full = my_stream.full();
```

> `full()` applies to **output** FIFOs only (cannot be applied to input FIFOs).

> **Note:** You cannot use `full()` to check if an input FIFO is full — use `size()` for that.

---

### size()

```cpp
unsigned int hls::stream<T>::size();
```

Returns the current number of elements in the stream. Works on both input and output FIFOs.

```cpp
if (my_stream.size() > 0) {
    my_stream.read(var);
}
```

**Advanced flow control using size() + capacity():**

```cpp
// Read burst of N — only if N elements are available
if (instream.size() > N)
    for (int i = 0; i < N; i++)
        ... = instream.read();   // will not block

// Read only when stream is completely full
if (instream.size() == instream.capacity())
    ... = instream.read();
```

---

## Controlling the RTL FIFO Depth

For most streaming designs, the default depth of 2 is sufficient. For **multirate designs** where producer/consumer imbalance requires deeper FIFOs, use the `STREAM` pragma:

```cpp
#pragma HLS stream variable=my_stream depth=16
```

Or via directive in Tcl:
```tcl
set_directive_stream -depth 16 "my_function" my_stream
```

Because stream variables do not appear in the GUI directives pane, right-click the **function** containing the stream declaration, select the STREAM directive, and manually populate the variable name.

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Always pass streams by reference (`&`) | Streams cannot be copied — reference is mandatory |
| Prefer DATAFLOW regions for stream-connected tasks | Enables concurrent task execution; default depth of 2 is sufficient |
| In non-DATAFLOW regions, size FIFOs to hold all producer output | Otherwise deadlock occurs at RTL co-simulation |
| Use blocking API for deterministic behavior | Non-blocking requires RTL test bench for full verification |
| Use `size()` for both input and output FIFO queries | `empty()` is input-only; `full()` is output-only |
| Name streams for readable warning messages | Unnamed streams produce cryptic identifiers in warnings |
| Use `tlast` side-channel to terminate variable-length loops | `while (!stream.empty())` is non-deterministic in hardware |
| Avoid non-blocking with `ap_ctrl_none` | RTL co-simulation may not complete |
| Only AXI4-Stream supports non-blocking reads (not writes) | `ap_fifo` supports both; plan accordingly |

---

### See Also

- [Chapter 2 — Abstract Parallel Programming](../section2_hls_programmers_guide/ch02_abstract_parallel_programming.md) — Dataflow channels and streaming
- [Chapter 28 — HLS Task Library](ch28_hls_task_library.md) — `hls::task` with stream connections
- [Chapter 30 — Stream of Blocks](ch30_hls_stream_of_blocks.md) — Array-based dataflow via `hls::stream_of_blocks`
- [Chapter 29 — HLS Split/Merge](ch29_hls_split_merge.md) — Round-robin stream split/merge

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 24, pages 796–807*
