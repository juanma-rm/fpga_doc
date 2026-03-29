# Chapter 26 — HLS Fence Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 815–817

## Table of Contents

- [Overview](#overview)
- [Full Fence vs. Half Fence](#full-fence-vs-half-fence)
- [Practical Examples](#practical-examples)
  - [Avoiding Deadlocks in Dataflow](#avoiding-deadlocks-in-dataflow)
  - [Configuring the Vivado LogiCORE FFT](#configuring-the-vivado-logicore-fft)
- [Known Limitations](#known-limitations)

---

## Overview

The Vitis HLS compiler may reorder unrelated memory accesses to improve performance. While it always preserves `control dependences` and `data dependences` to maintain sequential program semantics, there are cases where the user needs to additionally enforce a scheduling order between logically independent accesses.

`hls::fence` guarantees that two or more accesses to **streams**, **arrays**, and **scalar function arguments passed by reference** are scheduled in the sequential order implied by the source code.

**Header:**
```cpp
#include "hls_fence.h"
```

> **Tip:** An example is available in `Vitis-HLS-Introductory-Examples/Interface/Memory/aliasing_axi_master_ports` on GitHub.

---

## Full Fence vs. Half Fence

### Full Fence

```cpp
hls::fence(obj_1, obj_2, ..., obj_n);
```

Constrains the scheduling of all accesses to `obj_1 … obj_n`:
- Any access that is **before** the fence in sequential order remains scheduled **before** the fence.
- Any access that is **after** the fence in sequential order remains scheduled **after** the fence.

### Half Fence

```cpp
hls::fence({obj_1, obj_2, ..., obj_n}, {obj'_1, obj'_2, ..., obj'_p});
```

Less restrictive — useful in pipeline loops:
- Objects in the **first** set (left braces): may be scheduled *earlier* than the fence, but cannot be moved *after* it if they were before it in sequential order.
- Objects in the **second** set (right braces): may be scheduled *later* than the fence, but cannot be moved *before* it if they were after it in sequential order.

> **Equivalence:** `hls::fence(a, b)` is equivalent to `hls::fence({a, b}, {a, b})`.

| Type | Syntax | Restriction |
|---|---|---|
| Full fence | `hls::fence(a, b, ...)` | Strict before/after ordering for all listed objects |
| Half fence | `hls::fence({a,...}, {b,...})` | Asymmetric: left set → must not move after; right set → must not move before |

---

## Practical Examples

### Avoiding Deadlocks in Dataflow

**Problem:** A `Consumer` process needs `strm1` (the loop bound) before reading `strm2`. If the compiler reorders the `Producer` to write `strm1` after the loop, the consumer cannot start, and a deadlock occurs — because a stream of depth `bound` would be needed to buffer all `strm2` elements.

**Without fence (potentially unsafe):**
```cpp
void Producer(...) {
    int bound = ...;
    strm1.write(bound);        // HLS may move this AFTER the loop
    for (int i = 0; i < bound; i++) {
        strm2.write(...);
    }
}
```

**With fence (safe):**
```cpp
void Producer(...) {
    int bound = ...;
    strm1.write(bound);
    hls::fence({strm1}, {strm2});   // strm1 write must precede strm2 writes
    for (int i = 0; i < bound; i++) {
        strm2.write(...);
    }
}

void Consumer(...) {
    int bound = strm1.read();       // safe: bound is available before strm2
    for (int i = 0; i < bound; i++) {
        ... = strm2.read();
    }
}
```

---

### Configuring the Vivado LogiCORE FFT

**Problem:** The FFT configuration must be captured **before** processing begins. Without a fence, the compiler may schedule the data loop before the config write.

**Without fence (potentially unsafe):**
```cpp
void inputdatamover(..., config_t *fft_config, cmpxDataIn in[], cmpxDataIn xn[]) {
    config_t fft_config_tmp;
    fft_config_tmp.setDir(...);
    fft_config_tmp.setSch(...);
    *fft_config = fft_config_tmp;   // may be reordered after the loop
    for (int i = 0; i < FFT_LENGTH; i++) {
#pragma HLS pipeline rewind
        xn[i] = in[i];
    }
}
```

**With fence (safe):**
```cpp
void inputdatamover(..., config_t *fft_config, cmpxDataIn in[], cmpxDataIn xn[]) {
    config_t fft_config_tmp;
    fft_config_tmp.setDir(...);
    fft_config_tmp.setSch(...);
    *fft_config = fft_config_tmp;
    hls::fence({fft_config}, {xn});   // config write must precede data writes
    for (int i = 0; i < FFT_LENGTH; i++) {
#pragma HLS pipeline rewind style=flp
        xn[i] = in[i];
    }
}
```

---

## Known Limitations

| Limitation | Detail |
|---|---|
| No implicit global barrier | The fence only constrains the variables explicitly listed as arguments. All relevant objects must be specified. |
| Incompatible with DATAFLOW regions | Fences can be applied in a **pipeline or sequential** scheduling region only — not inside a dataflow region. |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 26, pages 815–817*
