# Chapter 23 — HLS Math Library

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 785–795

## Table of Contents

- [Overview](#overview)
- [Accuracy and ULP Differences](#accuracy-and-ulp-differences)
- [C Standard Mode Considerations](#c-standard-mode-considerations)
- [Floating-Point Math Functions](#floating-point-math-functions)
- [Fixed-Point Math Functions](#fixed-point-math-functions)
- [Verification Strategies](#verification-strategies)
  - [Option 1: Standard Library + Accept Differences](#option-1-standard-library--accept-differences)
  - [Option 2: HLS Math Library (Source Modification)](#option-2-hls-math-library-source-modification)
  - [Option 3: HLS Math Library File (No Source Changes)](#option-3-hls-math-library-file-no-source-changes)
- [Common Synthesis Errors](#common-synthesis-errors)

---

## Overview

The AMD Vitis HLS Math Library (`hls_math.h`) provides coverage of math functions matching `<cmath>`, usable in both C simulation and synthesis. All functions are in the `hls` namespace and serve as drop-in replacements for `std` namespace functions.

**Header:**
```cpp
#include "hls_math.h"
```

> **Important:** Using `hls_math.h` in C (non-C++) code is **not supported**.

Precision tiers supported by all functions:
- Half-precision (`half`)
- Single-precision (`float`)
- Double-precision (`double`)

For each function `func`, companion variants are also provided:
- `half_func` — half-precision only
- `funcf` — single-precision only

---

## Accuracy and ULP Differences

HLS math functions are **bit-approximate** implementations. They may not produce bit-identical results to standard C library functions.

| Aspect | Detail |
|---|---|
| Accuracy metric | ULP (Unit of Least Precision) |
| Typical ULP difference | 1–4 ULP from standard C math library |
| Synthesis RTL | Same RTL regardless of which library is used in C code |

**Impact on simulation:**

| Source code uses | C sim vs. C/RTL co-sim |
|---|---|
| Standard C math library (`<cmath>`) | Results may differ (ULP discrepancy) |
| HLS math library (`hls_math.h`) | Results are identical between C sim and RTL co-sim |

The seven functions that may show mode-dependent differences:
`copysign`, `fpclassify`, `isinf`, `isfinite`, `isnan`, `isnormal`, `signbit`

---

## C Standard Mode Considerations

| Mode | Behavior |
|---|---|
| **C90** | Only `isinf`, `isnan`, `copysign` provided; all operate on `double`; `copysign` always returns `double` (may cause unexpected double→float conversion in HW) |
| **C99 (`-std=c99`)** | All seven provided; `isnormal` implemented via `fpclassify`; functions redirect to `__isnan(double/float)` |
| **C++ with `math.h`** | All seven operate on `double`; `copysign` always returns `double` |
| **C++ with `cmath`** | Similar to C99; functions properly overloaded for `float` and `double` |
| **C++ with `cmath` + `namespace std`** | No issues — recommended |

**AMD Recommendations:**
- For C code: compile with `-std=c99`
- For C and C++: compile with `-fno-builtin`

> To apply C compile options in Vitis HLS: use `add_files -cflags` in Tcl, or set via **Edit CFLAGs** in Project Settings.

---

## Floating-Point Math Functions

The following functions are provided for `half`, `float`, and `double` types.

### Trigonometric
`acos` · `acospi` · `asin` · `asinpi` · `atan` · `atan2` · `atan2pi` · `cos` · `cospi` · `sin` · `sincos` · `sinpi` · `tan` · `tanpi`

### Hyperbolic
`acosh` · `asinh` · `atanh` · `cosh` · `sinh` · `tanh`

### Exponential
`exp` · `exp10` · `exp2` · `expm1` · `frexp` · `ldexp` · `modf`

### Logarithmic
`ilogb` · `log` · `log10` · `log1p`

### Power
`cbrt` · `hypot` · `pow` · `rsqrt` · `sqrt`

### Error
`erf` · `erfc`

### Rounding
`ceil` · `floor` · `llrint` · `llround` · `lrint` · `lround` · `nearbyint` · `rint` · `round` · `trunc`

### Remainder
`fmod` · `remainder` · `remquo`

### Floating-Point Manipulation
`copysign` · `nan` · `nextafter` · `nexttoward`

### Difference / Min / Max
`fdim` · `fmax` · `fmin` · `maxmag` · `minmag`

> **Note:** Vitis HLS does not yet support TS 18661-1 sNaN handling in `fmin`/`fmax`, which may lead to differences vs. glibc 2.25+.

### Other
`abs` · `divide` · `fabs` · `fma` · `fract` · `mad` · `recip`

### Classification
`fpclassify` · `isfinite` · `isinf` · `isnan` · `isnormal` · `signbit`

### Comparison
`isgreater` · `isgreaterequal` · `isless` · `islessequal` · `islessgreater` · `isunordered`

### Relational
`all` · `any` · `bitselect` · `isequal` · `isnotequal` · `isordered` · `select`

---

## Fixed-Point Math Functions

Fixed-point implementations provide a slightly less accurate but **smaller and faster** RTL implementation. They support `ap_[u]fixed` and `ap_[u]int` types.

### Supported Bit-Width Ranges

| Type | Constraint |
|---|---|
| `ap_fixed<W,I>` | $I \leq 33$, $W - I \leq 32$ |
| `ap_ufixed<W,I>` | $I \leq 32$, $W - I \leq 32$ |
| `ap_int<I>` | $I \leq 33$ |
| `ap_uint<I>` | $I \leq 32$ |

> **Important:** Fixed-point math functions do **not** support the `Q`, `O`, `N` template parameters of `ap_[u]fixed` (quantization mode, overflow mode, saturation bits). These modes only apply on assignment/initialization, not during computation.

### Available Fixed-Point Functions

| Category | Functions |
|---|---|
| Trigonometric | `cos` · `sin` · `tan` · `acos` · `asin` · `atan` · `atan2` · `sincos` · `cospi` · `sinpi` |
| Hyperbolic | `cosh` · `sinh` · `tanh` · `acosh` · `asinh` · `atanh` |
| Exponential | `exp` · `frexp` · `modf` · `exp2` · `expm1` |
| Logarithmic | `log` · `log10` · `ilogb` · `log1p` |
| Power | `pow` · `sqrt` · `rsqrt` · `cbrt` · `hypot` |
| Error | `erf` · `erfc` |
| Rounding | `ceil` · `floor` · `trunc` · `round` · `rint` · `nearbyint` |
| Floating-Point | `nextafter` · `nexttoward` |
| Difference/Min/Max | `fdim` · `fmax` · `fmin` · `maxmag` · `minmag` |
| Other | `fabs` · `recip` · `abs` · `fract` · `divide` |
| Classification | `signbit` |
| Comparison | `isgreater` · `isgreaterequal` · `isless` · `islessequal` · `islessgreater` |
| Relational | `isequal` · `isnotequal` · `any` · `all` · `bitselect` |

### Fixed-Point Usage Methodology

1. Determine if the required math function has a fixed-point implementation.
2. Replace `float`/`double` types with `ap_fixed` in the source.
3. Run C simulation to validate precision is still acceptable (C sim uses the same bit-accurate types as RTL).
4. Synthesize.

**Example:**
```cpp
#include "hls_math.h"
#include "ap_fixed.h"

ap_fixed<26,6> my_input, my_output;
my_input  = 24.675;
my_output = sin(my_input);   // selects fixed-point sin implementation
```

---

## Verification Strategies

### Option 1: Standard Library + Accept Differences

Use standard C math libraries (`<cmath>`) in source. C/RTL co-simulation results may differ from C simulation due to ULP discrepancies. Use a "smart" test bench that validates the error is within an acceptable tolerance.

```cpp
#include <cmath>
// ...
data_t cpp_math(data_t angle) {
    data_t s = sinf(angle);
    data_t c = cosf(angle);
    return sqrtf(s*s + c*c);
}
```

**Test bench tolerance checking pattern:**
```cpp
diff = (exp_output > output) ? exp_output - output : output - exp_output;
if (diff > 0.0000005) {
    printf("Difference %.10f exceeds tolerance at angle %.10f\n", diff, angle);
    retval = 1;
}
```

If tolerance is tightened to `0.00000005`, the benchmark will flag typical RTL differences such as:
```
Difference 0.0000000596 at angle 1.1100001335
```

---

### Option 2: HLS Math Library (Source Modification)

Replace standard math calls with `hls::` prefixed equivalents. C simulation and C/RTL co-simulation will produce **identical** results. Note: results may differ from the standard C library.

> Available in **C++ only**.

```cpp
#include <cmath>
#include "hls_math.h"
// ...
data_t cpp_math(data_t angle) {
    data_t s = hls::sinf(angle);
    data_t c = hls::cosf(angle);
    return hls::sqrtf(s*s + c*c);
}
```

---

### Option 3: HLS Math Library File (No Source Changes)

Add the file `lib_hlsm.cpp` (from the `src/` directory in the Vitis HLS installation) as a design file. This causes Vitis HLS to use the HLS math library for C simulation without modifying source code.

> Available in **C++ only**.

Still validate with a smart test bench — C simulation results with `lib_hlsm.cpp` will differ from results without it.

---

## Common Synthesis Errors

### C++ `cmath.h`

When `cmath` is used, single-precision functions (`sinf`, `cosf`) are synthesized to 32-bit hardware. Standard overloaded functions (`sin`, `cos`) work correctly for both `float` and `double`.

### C `math.h`

Single-precision functions (`sinf`, `cosf`) produce 32-bit hardware. Generic calls (`sin`, `cos`) default to `double` operands and produce **64-bit double-precision** hardware — verify this is intended.

### C to C++ Conversion Pitfall

When converting C code to C++, always ensure the modified code compiles before synthesizing. For example, `sqrtf()` from `math.h` requires an explicit `extern "C"` declaration in C++:

```cpp
#include <math.h>
extern "C" float sqrtf(float);
```

> To avoid unnecessary type-conversion hardware, follow the float/double mixing guidelines in the data types chapter.

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 23, pages 785–795*
