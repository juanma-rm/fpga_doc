# Chapter 36 — Unsupported Features

> UG1399 (v2025.2) · Section VII: Vitis HLS Migration Guide · Pages 887–888

## Table of Contents

- [Overview](#overview)
- [Unsupported Pragma Usage](#unsupported-pragma-usage)
- [Unsupported Top-Level Function Argument Types](#unsupported-top-level-function-argument-types)
- [HLS Video Library](#hls-video-library)
- [C Arbitrary Precision Types](#c-arbitrary-precision-types)
- [Unsupported C Constructs](#unsupported-c-constructs)

---

## Overview

The features listed in this chapter are **not supported in Vitis HLS**. Unlike deprecated features (which generate warnings), unsupported features cause Vitis HLS to **issue a warning or error** and will not synthesize correctly.

> **Note:** The `INTERFACE` pragma is only supported at the top-level function. Using `#pragma HLS INTERFACE` inside sub-functions is **not supported**.

---

## Unsupported Pragma Usage

### DEPENDENCE on Bundled M_AXI Ports

Using `#pragma HLS DEPENDENCE` on an argument that is also bundled into an `m_axi` interface with two or more ports is not supported:

```cpp
// NOT SUPPORTED:
void top(int *a, int *b) {
    // Both a and b are bundled to the same m_axi port gmem
    #pragma HLS INTERFACE m_axi port=a offset=slave bundle=gmem
    #pragma HLS INTERFACE m_axi port=b offset=slave bundle=gmem
    #pragma HLS DEPENDENCE variable=a false  // <-- ERROR: can't combine with multi-port bundle
}
```

### INTERFACE ap_bus Mode

The `ap_bus` mode on the `INTERFACE` pragma (supported in Vivado HLS) is **not supported**. Use `m_axi` instead:

```cpp
// NOT SUPPORTED:
#pragma HLS INTERFACE ap_bus port=my_port

// USE INSTEAD:
#pragma HLS INTERFACE m_axi port=my_port
```

---

## Unsupported Top-Level Function Argument Types

The following C/C++ data types are **not supported** as top-level function arguments (interface ports):

| Type | Notes |
|---|---|
| `enum` | Any use of enum — struct containing enum, array pointer of enum |
| `ap_int<N>` / `ap_uint<N>` | Supported only for N = 1–32768 |
| `_Complex` | C complex type — use `std::complex<>` instead |
| `_Half` / `__fp16` | 16-bit floating-point C extensions |

---

## HLS Video Library

The `hls_video.h` library (video utilities and functions) is **deprecated** and replaced by the **Vitis Vision Library**:

- See: *Migrating HLS Video Library to Vitis Vision* on GitHub.
- Vitis Vision Library: [https://github.com/Xilinx/Vitis_Libraries/tree/main/vision](https://github.com/Xilinx/Vitis_Libraries/tree/main/vision)

---

## C Arbitrary Precision Types

| Feature | Status |
|---|---|
| C arbitrary precision types (`_ap_int`, `_ap_uint`) | **Not supported** — use C++ types (`ap_int<N>`, `ap_uint<N>`) |
| Maximum precision width | **4096 bits** (vs 32K bits in Vivado HLS) |

> The C++ arbitrary precision types (`ap_int<N>`, `ap_uint<N>`) are fully supported in Vitis HLS up to 4096 bits.

---

## Unsupported C Constructs

| Construct | Status |
|---|---|
| Pointer casts | Not supported |
| Virtual functions | Not supported |

---

### See Also

- [Chapter 35 — Deprecated Features](ch35_deprecated_unsupported.md) — Deprecated (not yet removed) items
- [Chapter 7 — Unsupported Constructs](../section2_hls_programmers_guide/ch07_unsupported_constructs.md) — Unsupported C/C++ constructs

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 36, pages 887–888*
