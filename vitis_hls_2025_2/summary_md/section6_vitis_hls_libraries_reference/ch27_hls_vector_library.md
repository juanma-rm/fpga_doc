# Chapter 27 — HLS Vector Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 818–820

## Table of Contents

- [Overview](#overview)
- [Memory Layout and Alignment](#memory-layout-and-alignment)
- [Initialization](#initialization)
- [Requirements and Dependencies](#requirements-and-dependencies)
- [Supported Operations](#supported-operations)
  - [Element Access](#element-access)
  - [Arithmetic Operations](#arithmetic-operations)
  - [Comparison Operations](#comparison-operations)

---

## Overview

`hls::vector<T, N>` is a SIMD-style vector data type for easily modeling and synthesizing parallel element-wise operations on N values of type T.

**Header:**
```cpp
#include "hls_vector.h"
```

**Declaration:**
```cpp
hls::vector<T, N> aVec;
```

- `T`: primitive or user-defined type that supports arithmetic/logic operations.
- `N`: integer > 0, the number of elements.

> **Performance Tip:** Best hardware performance is achieved when both the bit-width of `T` and `N` are integer powers of 2.

> **Examples in GitHub:** `Vitis-HLS-Introductory-Examples/Modeling`

---

## Memory Layout and Alignment

For `hls::vector<T,N>`, storage is:
- **Contiguous**: `sizeof(T) * N` bytes total.
- **Aligned**: to the greatest power of 2 that is ≥ `sizeof(T) * N`.

When both `sizeof(T)` and `N` are powers of 2, the vector is aligned to its exact total size — matching typical architecture vector conventions.

> **Allocation note:** If `sizeof(T)*N` is a power of 2, allocated size = `sizeof(T)*N` exactly. Otherwise it is rounded up for alignment.

**Alignment examples:**
```cpp
hls::vector<char, 8> char8Vec;   // aligned on 8-byte boundary
hls::vector<int,  8> int8Vec;    // aligned on 32-byte boundary
```

The alignment formula used internally:
```cpp
constexpr size_t gp2(size_t N) {
    return (N > 0 && N % 2 == 0) ? 2 * gp2(N / 2) : 1;
}
template<typename T, size_t N>
class alignas(gp2(sizeof(T) * N)) vector { std::array<T, N> data; };
```

---

## Initialization

### Scalar and initializer list:
```cpp
hls::vector<int, 4> x;            // uninitialized
hls::vector<int, 4> y = 10;       // all elements set to 10
hls::vector<int, 4> z = {0,1,2,3};// initializer list (must have exactly N elements)
```

### `iota` — arithmetic sequence initialization:
Similar to `std::iota`, starts from `start` and increments by index.
```cpp
auto vec = hls::vector<int, 8>::iota(-4);
// Equivalent to: hls::vector<int,8> vec = {-4, -3, -2, -1, 0, 1, 2, 3};
```

### Lambda initialization:
```cpp
hls::vector<int, 8> vec([](size_t i) { return i * i; });
// Equivalent to: hls::vector<int,8> vec = {0, 1, 4, 9, 16, 25, 36, 49};
```

---

## Requirements and Dependencies

- **C++ standard:** C++14 or later required.
- **Standard library dependencies:**

| Header | Used For |
|---|---|
| `<array>` | `std::array<T,N>` internal storage |
| `<cassert>` | `assert` |
| `<initializer_list>` | `std::initializer_list<T>` constructor |

---

## Supported Operations

### Element Access

```cpp
x[i] = value;    // write element at index i
value = x[i];    // read element at index i
```

### Arithmetic Operations

All operations are defined recursively, relying on the corresponding operation on type `T`. Both in-place and expression forms are provided, along with reduction (left fold) where associative.

| Operation | In-Place | Expression | Reduction |
|---|---|---|---|
| Addition | `+=` | `+` | `reduce_add` |
| Subtraction | `-=` | `-` | non-associative |
| Multiplication | `*=` | `*` | `reduce_mult` |
| Division | `/=` | `/` | non-associative |
| Remainder | `%=` | `%` | non-associative |
| Bitwise AND | `&=` | `&` | `reduce_and` |
| Bitwise OR | `\|=` | `\|` | `reduce_or` |
| Bitwise XOR | `^=` | `^` | `reduce_xor` |
| Shift Left | `<<=` | `<<` | non-associative |
| Shift Right | `>>=` | `>>` | non-associative |
| Pre-increment | `++x` | — | unary |
| Pre-decrement | `--x` | — | unary |
| Post-increment | `x++` | — | unary |
| Post-decrement | `x--` | — | unary |

### Comparison Operations

Lexicographic order on vectors, returning `bool`:

| Operation | Expression |
|---|---|
| Less than | `<` |
| Less or equal | `<=` |
| Equal | `==` |
| Different | `!=` |
| Greater or equal | `>=` |
| Greater than | `>` |

---

## Best Practices

| Practice | Rationale |
|---|---|
| **Use power-of-2 for both element bit-width and vector size `N`** | Ensures optimal memory alignment and maximum hardware efficiency |
| **Prefer `hls::vector` over manual loop unrolling for SIMD** | The compiler maps vector operations to parallel hardware automatically; cleaner code, same result |
| **Use `reduce()` for sum/min/max reductions** | Generates a balanced tree of operations rather than a sequential chain |
| **Compile with C++14 or later** | `hls::vector` requires C++14; set `syn.compile.cflags=-std=c++14` |
| **Combine vectors with `hls::stream` for throughput** | Streaming vector words through a dataflow pipeline achieves maximum bandwidth |

---

### See Also

- [Chapter 6 — Data Types (Vector Data Types)](../section2_hls_programmers_guide/ch06_data_types.md#10-vector-data-types) — Overview and usage context
- [Chapter 4 — Arrays Primer](../section2_hls_programmers_guide/ch04_arrays_primer.md) — Array partitioning for parallel access
- [Chapter 24 — HLS Stream Library](ch24_hls_stream_library.md) — Streaming vector data between tasks

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 27, pages 818–820*
