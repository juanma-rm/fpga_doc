# Chapter 20 — C/C++ Builtin Functions

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Page 729

## Overview

Vitis HLS supports the following GCC C/C++ builtin functions for counting zero bits. These are synthesizable and map efficiently to hardware.

## Supported Builtins

### `__builtin_clz` — Count Leading Zeros

```c
int __builtin_clz(unsigned int x);
```

Returns the number of leading 0-bits in `x`, starting from the most significant bit position.

> **Note:** Result is undefined if `x == 0`.

**Hardware mapping:** Synthesizes to a priority encoder counting high-order zeros — efficient in both LUT and DSP implementations.

---

### `__builtin_ctz` — Count Trailing Zeros

```c
int __builtin_ctz(unsigned int x);
```

Returns the number of trailing 0-bits in `x`, starting from the least significant bit position.

> **Note:** Result is undefined if `x == 0`.

---

## Example

The following function returns the sum of the number of leading zeros in `in0` and the trailing zeros in `in1`:

```c
int foo(int in0, int in1) {
    int ldz0 = __builtin_clz(in0);
    int ldz1 = __builtin_ctz(in1);
    return (ldz0 + ldz1);
}
```

## Quick Reference

| Builtin | Counts | Undefined when |
|---|---|---|
| `__builtin_clz(x)` | Leading zeros (from MSB) | `x == 0` |
| `__builtin_ctz(x)` | Trailing zeros (from LSB) | `x == 0` |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 20, page 729*
