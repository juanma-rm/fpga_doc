# Chapter 6 — Data Types
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Standard C/C++ Types](#1-standard-cc-types)
2. [Floats and Doubles](#2-floats-and-doubles)
3. [Composite Data Types](#3-composite-data-types)
4. [Type Qualifiers](#4-type-qualifiers)
5. [Arbitrary Precision Integer Types (`ap_int`)](#5-arbitrary-precision-integer-types-ap_int)
6. [Arbitrary Precision Fixed-Point Types (`ap_fixed`)](#6-arbitrary-precision-fixed-point-types-ap_fixed)
7. [Arbitrary Precision Floating-Point Library (`ap_float`)](#7-arbitrary-precision-floating-point-library-ap_float)
8. [Global Variables](#8-global-variables)
9. [Pointers](#9-pointers)
10. [Best Practices](#10-best-practices)

---

## 1. Standard C/C++ Types

Vitis HLS supports synthesis of all standard C/C++ types:

| Type | Width | Notes |
|---|---|---|
| `char` / `unsigned char` | 8 bits | Smallest standard type |
| `short` / `unsigned short` | 16 bits | |
| `int` / `unsigned int` | 32 bits | Use over `long` for portability |
| `long` / `unsigned long` | **64-bit on Linux**, 32-bit on Windows | Avoid for portable code |
| `long long` / `unsigned long long` | 64 bits | Use for 64-bit data |
| `int8_t`…`int64_t` / `uint8_t`…`uint64_t` | Exact | From `stdint.h` — recommended |
| `float` | 32-bit IEEE-754 | 24-bit fraction, 8-bit exponent |
| `double` | 64-bit IEEE-754 | 53-bit fraction, 11-bit exponent |

> **Warning:** `std::complex<long double>` is NOT supported.

> **`long` portability note:** On 64-bit Linux, `long` = 64 bits; on Windows, `long` = 32 bits. Use `int32_t`/`int64_t` for platform-safe code.

### Operator Sizing Rule

HLS uses the **smallest operator** that fits the result:
- `char * short` → 24-bit multiplier (8+16), result sign-extended to output width
- `unsigned char + short` → If output is `uint8`, HLS uses an 8-bit adder (lower 8 bits only)

### Define All Types in One Header

```cpp
// types.h — change once, affects entire project
typedef ap_int<10> din_t;   // refined from int → 10-bit
typedef ap_int<18> dout_t;
```

---

## 2. Floats and Doubles

### IEEE-754 Partial Compliance

Both `float` and `double` are synthesized using AMD IP catalog cores (PG060) with partial IEEE-754 compliance.

### Type Mixing Rules

> Always use `sqrtf()` (float) instead of `sqrt()` (double) when the operand is `float`:

```cpp
// Wasteful — uses two type converters
float var_f = sqrt(foo_f);   // foo_f is float, sqrt takes double

// Efficient — no converters needed
float var_f = sqrtf(foo_f);
```

The hardware path for the wasteful version:
```
float → Float-to-Double converter → Double sqrt → Double-to-Float converter → float
```

### Operation Order Preserved

HLS **maintains C++ operation order** for float/double to ensure bit-exact simulation match. This can limit parallel optimizations (e.g., loop unrolling may not gain parallelism for float accumulations).

Override: `config_compile -unsafe_math_optimizations` (disables order preservation).

### Floating-Point Accumulator and MAC

Configurable via `syn.op`:

```
syn.op=op:fmacc precision:high          # high-precision fused multiply-add (Versal only)
syn.op=op:fmacc precision:standard      # standard — II=1 on Versal, II=3-5 on others
syn.op=op:fmacc precision:low           # low — always II=1, integer accumulator + scalers
```

| Precision Mode | Device | II | Notes |
|---|---|---|---|
| `low` | Non-Versal | 1 | Integer accumulator; may cause cosim mismatch |
| `standard` | Versal | 1 | True float accumulator |
| `standard` | Non-Versal | 3–5 | More resources |
| `high` | Versal only | 1 | Extra precision bit; single rounding; may cause cosim mismatch |

---

## 3. Composite Data Types

### Structs

| Context | Default Behavior |
|---|---|
| Internal variables (not on interface) | **Disaggregated** — split into individual elements |
| Top-level function arguments (on interface) | **Aggregated** — combined into single wide vector |

**AGGREGATE pragma** — pack all struct fields into one wide vector (can also apply to internal variables):
```cpp
struct data_t {
    unsigned short varA;    // 16 bits
    unsigned char  varB[4]; // 4 × 8 = 32 bits
};
// Aggregated result: 48-bit single port (LSB=varA, then varB[0]..varB[3])
```

Key rules:
- Elements placed in struct-declaration order; first element at LSB.
- Arrays in the struct are fully partitioned into scalars and placed in order.
- Default: **4-byte alignment** (Vitis kernel flow): padding inserted between fields to align on 32-bit boundaries.
- **1-byte alignment** (Vivado IP flow) — or use `compact=bit` option of `AGGREGATE` pragma (not for AXI ports).

**DISAGGREGATE pragma** — force split of interface struct into individual ports (Vivado IP flow only; not supported in Vitis kernel flow).

#### Struct Padding and Alignment Examples

```cpp
// 4-byte aligned (default Vitis): size = 96 bits (short+4pad+int+short+2pad)
struct data_t { short varA; int varB; short varC; };

// Reordered — no padding needed: size = 64 bits
struct data_t { short varA; short varC; int varB; };

// Explicit alignment: __attribute__((aligned(2))) → align to 2-byte boundary
// Packing: __attribute__((packed)) → actual field sizes, no padding (72 bits for a+b+c+d)
```

> Use compiler flag `-Wpadded` to get warnings when HLS inserts padding.

#### Structs with `hls::stream` Members

Automatically **disaggregated** regardless of settings. Not supported in the Vitis kernel flow as a top-level argument — must manually separate stream and non-stream fields.

### Enumerated Types

Synthesizable. On the top-level interface, enums are 32-bit values (matching C/C++ default). Internally, HLS optimizes them to the minimum required bit width.

### Unions

Supported with restrictions:

| Restriction | Detail |
|---|---|
| Not on top-level interface | Unions cannot be used as top-level function arguments |
| No pointer reinterpretation | Cannot hold pointers to different types |
| No loop-indexed member access | e.g., `intfp.intval.a + B[i]` inside a loop — must unroll manually |
| No general type casting | Native C types supported; user-defined types not |

**Bit-reinterpretation pattern (float ↔ uint):**
```cpp
union { unsigned int as_uint32; float as_floatingpoint; } converter;
converter.as_uint32 = raw_bits;
float result = converter.as_floatingpoint;
```

For `half` type (it's a class, not a POD — unions don't work):
```cpp
half value = static_cast<half>(short_bits);
```

### C++ Classes and Templates

```cpp
// Class cannot be the top-level. Instantiate it in a top-level function:
data_t cpp_FIR(data_t x) {
    static CFir<coef_t, data_t, acc_t> fir1;  // class instance
    return fir1(x);   // call overloaded operator()
}
```

> Do **not** use global variables in classes — can prevent optimization (e.g., variable loop bounds with global index).

**Templates:**
- Fully supported for synthesis; top-level function **cannot** be a template.
- Different template argument values create **unique, independently optimized instances**.
- `static` variables in template functions are **duplicated per unique template instantiation**.
- Templates can implement **tail recursion** (synthesis-safe alternative to runtime recursion).

---

## 4. Type Qualifiers

### `volatile`

| With `volatile` | Without `volatile` |
|---|---|
| All accesses preserved; no burst, no port widening | HLS may merge/reduce accesses |
| Each pointer dereference → separate RTL transaction | Multiple reads may collapse to one |

> `volatile` on `ap_*` types is not supported for arithmetic. Assign to a non-volatile first.

### `static`

- Static variables hold value between function calls → implemented as **registers** in RTL.
- Initialization value from C++ is preserved in RTL and FPGA bitstream.
- Not re-initialized on every hardware reset (only at power-on / configuration).

### `const`

- Read-only variables → propagated as constants in RTL (hardware removed).
- `const` arrays → inferred as **ROMs** in RTL (initialized in bitstream, never reset needed).

### ROM Optimization Example

Even without `static` or `const`, HLS may infer a ROM if all writes happen before all reads:

```cpp
din1_t lookup_table[256];
for (i = 0; i < 256; i++)
    lookup_table[i] = 256 * (i - 128);  // only write once, no interleaving
return inval * lookup_table[idx];       // only reads after all writes
```

---

## 5. Arbitrary Precision Integer Types (`ap_int`)

### Include and Syntax

```cpp
#include "ap_int.h"

ap_int<9>   var1;    // 9-bit signed
ap_uint<10> var2;    // 10-bit unsigned
```

Range: 1 to 1024 bits (default). Extend to 4096 bits:
```cpp
#define AP_INT_MAX_W 4096   // MUST be before #include
#include "ap_int.h"
ap_int<4096> very_wide_var;
```

> **Important:** `ap_int`/`ap_uint` arrays are **not automatically zero-initialized** — initialize manually.

### Hardware Impact Example

| Type Scheme | Latency | LUT | FF |
|---|---|---|---|
| Standard C++ (`int`, `long long`, etc.) | 66 cycles | 17,169 | 17,927 |
| Exact-width AP types (`ap_int<6>`, `ap_int<18>`, etc.) | 35 cycles | 4,573 | 4,770 |

> **75% area reduction** by using exact bit-widths. Division/modulo are the dominant latency contributors; smaller widths directly reduce their latency.

### AP Integer Operations

Full C++ arithmetic operators: `+`, `-`, `*`, `/`, `%`, `<<`, `>>`, bitwise, comparison.
- Bit-width of results is automatically tracked.
- Propagate correct widths from inputs to avoid unintended truncation.

### Numeric Limits

```cpp
using data_u_t = ap_uint<5>;
data_u_t max = std::numeric_limits<data_u_t>::max();  // 31

using data_f_t = ap_ufixed<5, 3>;
data_f_t min = std::numeric_limits<data_f_t>::min();
```

---

## 6. Arbitrary Precision Fixed-Point Types (`ap_fixed`)

```cpp
#include "ap_fixed.h"

// ap_fixed<W, I, Q, O, N>
// W = total bits; I = integer bits (including sign); Q = quantization; O = overflow; N = sat bits
ap_fixed<18, 6, AP_RND> t1 = 1.5;   // 18 total bits, 6 integer bits, round-to-+inf mode
ap_fixed<18, 6, AP_RND> t2 = -1.5;
```

### ap_fixed Parameter Reference

| Parameter | Description | Default |
|---|---|---|
| `W` | Total word length in bits | — |
| `I` | Integer bits left of binary point (includes sign bit) | — |
| `Q` — Quantization | `AP_RND` (→+∞), `AP_RND_ZERO`, `AP_RND_MIN_INF` (→-∞), `AP_RND_INF`, `AP_RND_CONV` (convergent), `AP_TRN` (→-∞ truncate, default), `AP_TRN_ZERO` | `AP_TRN` |
| `O` — Overflow | `AP_SAT` (saturate), `AP_SAT_ZERO`, `AP_SAT_SYM`, `AP_WRAP` (default), `AP_WRAP_SM` | `AP_WRAP` |
| `N` | Saturation bits (used with wrap overflow modes) | 0 |

> `AP_SAT*` modes can add **up to 20% extra LUT** for saturation logic.
>
> `hls_math` fixed-point functions do **not** use Q, O, N modes during computation — only on assignment.

### Negative `I` Example

```cpp
ap_fixed<2,  0> a = -0.5;    // can be -0.5 or 0 only
ap_ufixed<1, 0> x = 0.5;     // can be 0 or 0.5
ap_ufixed<1,-1> y = 0.25;    // can be 0 or 0.25
```

Binary-point alignment is **automatic** when mixing widths.

> **ROM synthesis note:** Using `ap_fixed` for ROM arrays can be slow. Prefer `int` for ROM arrays: change `static ap_fixed<32,0> a[32][depth]` → `static int a[32][depth]`.

---

## 7. Arbitrary Precision Floating-Point Library (`ap_float`)

### Overview

`ap_float<W, E>` — arbitrary-precision floating-point with configurable total width and exponent width.

```cpp
#include "ap_float.h"
```

| C++ type | `ap_float<W,E>` equivalent |
|---|---|
| `float` | `ap_float<32, 8>` |
| `double` | `ap_float<64, 11>` |
| `half` | `ap_float<16, 5>` |
| `bfloat16` | `ap_float<16, 8>` |
| `tf32` (TensorFloat-32) | `ap_float<19, 8>` |

### Constraints

| Limit | Value |
|---|---|
| Max total width W | 80 bits |
| Exponent width E | 4 to 16 bits |
| Mantissa bits | 4 to 64 bits |
| Sub-normals | Not supported — rounded to 0 |
| Rounding mode | Round to Nearest (Ties to Even) only |
| NaN support | Quiet NaNs only (no Signaling NaN) |

### Supported Operations

`+`, `-`, `*`, `/`, `+=`, `-=`, `*=`, `/=`, `<`, `>`, `==`, `hls::sqrt`, `hls::fma`, `hls::abs`

> **No implicit conversion from `ap_float<>` to `float`** — must cast explicitly: `(float)my_ap_float_var`

```cpp
typedef ap_float<18, 6> my_float;

float apf_example(float f_in) {
    my_float pi = M_PI;         // implicit float → ap_float: OK
    my_float r  = f_in;
    my_float area = pi * r * r;
    if (area > 1.0f) area = 1.0f;
    return (float)area;         // explicit ap_float → float required
}
```

### Handling Unsupported Functions

```cpp
ap_float<16,8> k;
// ... = hls::log(k);             // ERROR: no matching function

// Workarounds:
... = hls::log((float)k);
... = hls::log((ap_fixed<20,5>)k);
... = hls::log((int)k);
```

### Accumulation with `ap_float_acc<>`

```cpp
using apf_t = ap_float<18, 5>;
using acc_t = ap_fixed<32, 16>;

ap_float_acc<apf_t, acc_t> acc;   // internal fixed-point accumulator → II=1 in loop

for (unsigned i = 0; i < n; i++) {
    apf_t val = ...;
    result = acc.accumulate(val, i == n-1);  // last=true clears accumulator
}
```

> **Restrictions:** `ap_float_acc<>` arrays must be fully partitioned. Cannot cross function hierarchy; must be declared in the same function as `accumulate()` calls.

---

## 8. Global Variables

Global variables are fully synthesizable, but:

- **Cannot be inferred as RTL ports** automatically.
- Must be **explicitly listed as arguments** of the top-level function if external access is needed.
- AMD does **not recommend** using global variables in classes — can prevent pipelining and loop unrolling (variable loop bound issue).

```cpp
// Global arrays must appear in the argument list of the top-level function:
void top(const int idx, const int Ain[N], int Aout[Nhalf]) { ... }
```

---

## 9. Pointers

### Supported Pointer Patterns

| Pattern | Synthesis Support |
|---|---|
| Basic pointer (read or write once) | ✅ → wire or handshake interface |
| Pointer to multiple objects (branch-select) | ✅ |
| Pointer arithmetic (sequential from index 0) | ✅ |
| Pointer arithmetic (non-sequential, out-of-order) | ❌ wire/handshake/FIFO fail; needs `ap_memory` (array on interface) |
| Pointer to pointer (`**ptr`) | ✅ internally; ❌ on top-level interface |
| Array of pointers (pointing to scalars/arrays) | ✅ |
| Array of pointers (pointing to pointers) | ❌ |
| Pointer casting (native C/C++ types) | ✅ |
| Pointer casting (custom/user types) | ❌ |

### Multi-Access Pointers (Interface)

Reading or writing an interface pointer **more than once** creates unexpected RTL. Prefer `hls::stream` for streaming read/write semantics:

```cpp
// BAD: pointer read 4 times, write twice → synthesis issue
void pointer_stream_bad(dout_t *d_o, din_t *d_i) {
    din_t acc = *d_i + *d_i;  // 2 reads → only 1 RTL read
    *d_o = acc;
    acc += *d_i + *d_i;       // 2 more reads → 1 RTL read
    *d_o = acc;               // 2nd write missed in RTL
}

// GOOD: use hls::stream for multiple sequential reads/writes
```

### Pointer Arithmetic on Interface

Sequential pointer arithmetic from index 0 → synthesizable as `ap_memory` (BRAM interface):
```cpp
// Requires ap_memory interface; wire/handshake/FIFO cannot handle non-zero start index
void array_arith(dio_t d[5]) {
    for (int i = 0; i < 4; i++) {
        acc += d[i+1];   // non-zero start index
        d[i] = acc;
    }
}
```

---

## 10. Best Practices

| Practice | Rationale |
|---|---|
| **Use `int32_t`/`int64_t` instead of `long`** | Portable across OS/compiler differences |
| **Define all types in a single header file** | Single point of change for refinement |
| **Use `ap_int<N>` / `ap_uint<N>` for exact hardware widths** | Reduces operator size → smaller, faster RTL (75%+ area savings typical) |
| **Use `ap_fixed<W,I>` for DSP-style fractional math** | Bit-accurate fixed-point sim matches RTL without float overhead |
| **Prefer `sqrtf()` over `sqrt()` for float operands** | Avoids double ↔ float conversion units in hardware |
| **Use `ap_float<W,E>` for custom float formats** | Enables bfloat16, tf32, etc. without changing data flow code |
| **Do not use `ap_int` in arithmetic inside `volatile` expressions** | Not supported; assign to non-volatile first |
| **Avoid global variables in classes** | Prevents loop unrolling and pipelining (variable loop bound) |
| **Use pointer arithmetic only sequentially from index 0** | Non-sequential pointer arithmetic requires `ap_memory` interface |
| **Use `hls::stream` instead of multi-access interface pointers** | Multi-read/write pointers on interface do not match expected RTL semantics |
| **Keep `const` qualifier on read-only arrays for ROM inference** | Ensures array synthesizes as ROM (embedded in bitstream, zero runtime overhead) |
| **Avoid `std::complex<long double>`** | Not supported |
| **Do not use `-m32` build flag** | Library dependencies require 64-bit builds only |

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 6: Data Types, Pages 104–150.*
