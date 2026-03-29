# Chapter 25 — HLS Direct I/O

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 808–814

## Table of Contents

- [Overview](#overview)
- [Features of hls::direct_io](#features-of-hlsdirect_io)
- [Using Direct I/O Streams](#using-direct-io-streams)
  - [Declaration](#declaration)
  - [Type Support](#type-support)
- [Protocol Options](#protocol-options)
  - [AP_HS — Two-way Handshake](#ap_hs--two-way-handshake)
  - [AP_VLD — Valid Only](#ap_vld--valid-only)
  - [AP_ACK — Acknowledge Only](#ap_ack--acknowledge-only)
  - [AP_NONE — No Handshake](#ap_none--no-handshake)
- [Mapping Direct I/O to SAXI Lite](#mapping-direct-io-to-saxi-lite)
- [Blocking/Non-Blocking API](#blockingnon-blocking-api)
  - [Blocking Writes](#blocking-writes)
  - [Blocking Reads](#blocking-reads)
  - [Non-Blocking Write](#non-blocking-write)
  - [Non-Blocking Read](#non-blocking-read)
- [Direct I/O vs HLS Stream Comparison](#direct-io-vs-hls-stream-comparison)

---

## Overview

**Continuously running kernels** are hardware kernels that run indefinitely until a reset event — unlike traditional SW acceleration kernels that are called, execute, and return.

A key challenge with continuously running kernels: since they never stop, kernel arguments (scalars and memory offsets) cannot be modified via the normal invocation mechanism. **Direct I/O** (`hls::direct_io`) solves this by providing a wire-based mechanism to update kernel arguments dynamically during execution.

**Header:**
```cpp
#include "hls_directio.h"
```

---

## Features of hls::direct_io

| Feature | Detail |
|---|---|
| Scope | Top-level functions only |
| Supported protocols | `ap_none`, `ap_ack`, `ap_vld`, `ap_hs` |
| API style | Blocking and non-blocking (similar to `hls::stream`) |
| RTL implementation | **Wire-based** (not synthesized as FIFO) |
| Dataflow | Coded like HLS Streams but implemented as wires with protocol signals |

---

## Using Direct I/O Streams

### Declaration

```cpp
#include "hls_directio.h"

// Declare two Direct I/O stream variables using ap_vld protocol
hls::ap_vld<int> &reset_value,
hls::ap_vld<int> &reset_myCounter
```

### Type Support

The type `T` in `hls::ap_vld<T>` (and other protocols) may be:
- Any C++ native data type
- Vitis HLS arbitrary precision types (`ap_int<>`, `ap_ufixed<>`, etc.)
- User-defined structs containing the above

---

## Protocol Options

### AP_HS — Two-way Handshake

Full industry-standard valid/acknowledge handshake.

| Signal | Method | Description |
|---|---|---|
| Data | `<var>.read()` | Read data value |
| Valid | `<var>.valid()` | Returns `true` when data is ready for reading |
| Acknowledge | `<var>.ready()` | Returns `true` after data has been consumed |

---

### AP_VLD — Valid Only

Simplified version of `ap_hs` — valid signal only, no acknowledge.

| Signal | Method | Description |
|---|---|---|
| Data | `<var>.read()` | Read data value |
| Valid | `<var>.valid()` | Returns `true` when data is valid and can be read |

**Example kernel using `ap_vld`:**
```cpp
void krnl_stream_vdatamover(hls::stream<pkt> &in,
                             hls::stream<pkt> &out,
                             int              mem[DATA],
                             hls::ap_vld<int> &reset_value,
                             hls::ap_vld<int> &reset_myCounter)
{
    for (int i = 0; i < DATA; i++) {
        if (reset_myCounter.valid()) {
            int reset = reset_myCounter.read();
            // use reset ...
        }
    }
}
```

---

### AP_ACK — Acknowledge Only

Subset of `ap_hs` — acknowledge signal only.

| Signal | Method | Description |
|---|---|---|
| Data | `<var>.read()` | Read data value |
| Acknowledge | `<var>.ready()` | Indicates data has been consumed |

---

### AP_NONE — No Handshake

Simplest protocol — data port only, no control signals.

> **Note:** `AP_NONE` does **not** support non-blocking APIs.

```cpp
typedef hls::ap_none<int> mystream_in;
typedef hls::ap_none<int> mystream_out;
typedef hls::ap_none<int> stream_vld_in;
typedef hls::ap_none<int> stream_vld_out;

void addInputs(mystream_in     &in,
               mystream_in     &dinB,
               stream_vld_in   &vldIn,
               mystream_out    &dout_Y,
               stream_vld_out  &vldOut)
{
#pragma HLS pipeline II=1
    int var = vldIn.read();
    if (var == 0) {
        vldOut.write(var);
        return;
    }
    int tmp1 = in.read();       // Blocking read
    int tmp2 = dinB.read();     // Blocking read
    int out  = tmp1 + tmp2;
    dout_Y.write(out);
    vldOut.write(1);
}
```

---

## Mapping Direct I/O to SAXI Lite

Vitis HLS can map Direct I/O streams onto an S_AXI_LITE interface, enabling a processor to write directly to the continuously running kernel's input arguments.

**Procedure:**
1. Choose the port protocol (`ap_none`, `ap_vld`, etc.).
2. Add the `s_axilite` interface pragma to the Direct I/O port.
3. Use the `.read()` / `.write()` methods as usual.

**Example:**
```cpp
void sub_task1(hls::stream<int> &in, hls::stream<int> &out) {
    int c = in.read();
    out.write(c + 2);
}

void sub_task2(hls::stream<int> &in, hls::stream<int> &out) {
    int c = in.read();
    out.write(c - 2);
}

void task2(hls::stream<int> &in, hls::stream<int> &out, hls::ap_none<int> &n) {
    int c   = in.read();
    int var = n.read();
    out.write(c + var);
}

void test(hls::stream<int> &in, hls::stream<int> &out, hls::ap_none<int> &bias) {
#pragma HLS interface s_axilite port=bias
    HLS_TASK_STREAM<int> s1;
    HLS_TASK_STREAM<int> s2;
    HLS_TASK t (task2,    s2,  out, bias);
    HLS_TASK t1(sub_task1, in,  s1);
    HLS_TASK t2(sub_task2, s1,  s2);
}
```

---

## Blocking/Non-Blocking API

### Blocking Writes

The `.write()` method stalls until the Direct I/O channel can accept data.

```cpp
// Method 1: explicit write()
// usage: void write(const T &din)
reset_value.write(counter);

// Method 2: << operator
reset_value << counter;
```

### Blocking Reads

The `.read()` method stalls until fresh data is available.

```cpp
// Method 1: explicit read()
// usage: void read(const T &dout) — for ap_hs
void krnl_stream_vdatamover(..., hls::ap_hs<int> &reset_myCounter) {
    int reset = reset_myCounter.read();
}

// Method 2: >> operator
reset_myCounter >> reset;
```

---

### Non-Blocking Write

Supported for `ap_hs` and `ap_vld` only. Returns `true` if successful.

```cpp
// usage: bool write_nb(const T_ &din)
int counter = 1;
reset_value.write_nb(counter);

// << operator variant
reset_value << counter;
```

### Non-Blocking Read

Supported for `ap_hs` and `ap_vld` only. Returns `true` if successful.

```cpp
// usage: bool read_nb(__STREAM_T__& dout)
hls::ap_vld<int> &reset_myCounter;
int reset = 1;
reset_myCounter.read_nb(reset);

// >> operator variant
reset_myCounter >> reset;
```

---

## Direct I/O vs HLS Stream Comparison

| Feature | `hls::stream<T>` | `hls::direct_io` (`ap_vld<T>`, etc.) |
|---|---|---|
| Use case | Data streaming between tasks | Dynamic argument updates to continuously running kernels |
| RTL implementation | FIFO | Wire with protocol handshake |
| Scope | Top-level and internal | Top-level only |
| Protocols | N/A (always FIFO) | `ap_hs`, `ap_vld`, `ap_ack`, `ap_none` |
| SAXI Lite mapping | No | Yes |
| Non-blocking | Both read and write | Read and write for `ap_hs`/`ap_vld`; not for `ap_none` |
| C simulation depth | Infinite queue | Wire (immediate) |
| Design flow | Dataflow pipelines | Continuously running kernels |

---

## Best Practices

| Practice | Rationale |
|---|---|
| **Use `direct_io` only for continuously running (`ap_ctrl_none`) kernels** | Direct I/O models wire-level signaling; it is not suitable for start/stop kernels with control handshakes |
| **Choose `ap_vld` for producer-driven updates, `ap_hs` for handshake-synchronized** | `ap_vld` is simplest when the consumer can tolerate stale data; `ap_hs` guarantees the consumer reads each value |
| **Map `direct_io` ports to `s_axilite` for host-accessible dynamic parameters** | Allows runtime tuning (e.g., threshold, gain) without restarting the kernel |
| **Use `hls::stream` (not `direct_io`) for data pipelines and dataflow regions** | Streams provide FIFO buffering and work inside dataflow; direct I/O does not |
| **Keep `direct_io` at the top-level function interface only** | Internal use is not supported; use `hls::stream` for inter-task communication |

---

### See Also

- [Chapter 24 — HLS Stream Library](ch24_hls_stream_library.md) — FIFO-based streaming alternative
- [Chapter 28 — HLS Task Library](ch28_hls_task_library.md) — Data-driven tasks that pair well with direct I/O
- [Chapter 8 — Interfaces](../section2_hls_programmers_guide/ch08_interfaces.md) — Interface protocols and block-level control

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 25, pages 808–814*
