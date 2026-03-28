# Chapter 21 — Arbitrary Precision Data Types Library
**Source:** AMD Vitis HLS User Guide UG1399 (v2025.2) · Pages 730–782

---

## Table of Contents
1. [Overview & Motivation](#overview)
2. [ap\_\[u\]int — Arbitrary Precision Integers](#ap_uint)
   - [Configuration & Limits](#ap_int_config)
   - [Initialization & Assignment](#ap_int_init)
   - [Console I/O](#ap_int_io)
   - [Arithmetic Operators & Bit-Growth](#ap_int_arith)
   - [Bitwise & Logical Operators](#ap_int_bitwise)
   - [Shift Operators](#ap_int_shift)
   - [Bit-Level Methods](#ap_int_bitmethods)
   - [Explicit Conversion Methods](#ap_int_conv)
   - [Compile-Time Attributes](#ap_int_static)
3. [ap\_\[u\]fixed — Arbitrary Precision Fixed-Point](#ap_ufixed)
   - [Representation & Template Parameters](#fixed_repr)
   - [Quantization Modes (Q)](#fixed_quant)
   - [Overflow Modes (O, N)](#fixed_overflow)
   - [Initialization & Assignment](#fixed_init)
   - [Console I/O](#fixed_io)
   - [Arithmetic Operators & Bit-Growth](#fixed_arith)
   - [Bit-Level & Class Methods](#fixed_methods)
   - [Explicit Conversion Methods](#fixed_conv)
   - [Compile-Time Attributes](#fixed_static)
4. [Best Practices](#best_practices)

---

## 1. Overview & Motivation <a name="overview"></a>

**The Problem:** Native C data types exist only on 8-bit boundaries (8, 16, 32, 64 bits). RTL hardware buses support arbitrary widths. A design requiring a **17-bit multiplier** must otherwise be implemented with a 32-bit type, wasting DSP resources and increasing area/power.

**The Solution:** Vitis HLS provides two header-only C++ template libraries for arbitrary bit-width types.

| Language | Type Family | Header Required |
|:---:|:---:|:---:|
| C++ | `ap_[u]int<W>` — Integer, **1–1024 bits** (extendable to 4 K) | `#include "ap_int.h"` |
| C++ | `ap_[u]fixed<W,I,Q,O,N>` — Fixed-point | `#include "ap_fixed.h"` |

**Key Benefits:**
- **Hardware efficiency:** Exact bit-widths map directly to RTL, avoiding over-sized operators.
- **Bit-accurate simulation:** C++ simulation with AP types matches the synthesised RTL behaviour precisely, allowing fast algorithmic validation before synthesis.
- **Standalone availability:** The package `xilinx_hls_lib_<release>.tgz` in `$HLS_ROOT/include` can be used independently in any C++ project.

---

## 2. ap\_\[u\]int — Arbitrary Precision Integers <a name="ap_uint"></a>

### 2.1 Configuration & Limits <a name="ap_int_config"></a>

| Parameter / Macro | Default | Max | Notes |
|:---|:---:|:---:|:---|
| Bit-width `W` | — | **1024** | Default cap |
| `AP_INT_MAX_W` | 1024 | **4096** | Must be `#define`d **before** `#include "ap_int.h"` |

```cpp
#define AP_INT_MAX_W 4096   // MUST come before the include
#include "ap_int.h"

ap_int<4096>  very_wide_var;  // 4 K-bit signed integer
```

> **CAUTION:** Setting `AP_INT_MAX_W` extremely high significantly increases software compile and simulation times.

Signed vs. unsigned classes:

```cpp
ap_int<9>    var1;    // 9-bit signed
ap_uint<10>  var2;    // 10-bit unsigned
```

> **IMPORTANT:** Arrays of AP types are **not** automatically zero-initialised. Since Vitis HLS 2023.2, `= {0}` or `= {}` initialises the **entire** array (previous releases only initialised the first element). Beware: array initialisation may create additional write accesses that interfere with dataflow checks.

---

### 2.2 Initialization & Assignment <a name="ap_int_init"></a>

Standard C++ integer literals (up to 64-bit) can be used directly. For values **wider than 64 bits**, a **string constructor** is mandatory.

```cpp
// ── Integer literal assignment ──────────────────────────────────────────
ap_int<42>  a(-1424692392255LL);   // signed, decimal
ap_uint<24> b = 0x1A2B3C;         // hex literal

// ── String constructor for > 64-bit ─────────────────────────────────────
ap_uint<96> wide("76543210fedcba9876543210", 16);   // hex string
ap_uint<96> wide2 = ap_int<96>("0123456789abcdef01234567", 16);

// ── Radix-prefixed string formats ────────────────────────────────────────
ap_int<6>  x("0b101010", 2);   // binary  → 42
ap_int<6>  y("0o40",     8);   // octal   → 32
ap_int<6>  z("0x2A",    16);   // hex     → 42
// ap_int<6> err("0b42", 2);   // COMPILE-TIME ERROR – invalid binary digit
```

| Radix Prefix | Format |
|:---:|:---|
| `0b` | Binary |
| `0o` | Octal |
| `0x` | Hexadecimal |
| *(none)* | Hexadecimal (default for strings) |

> **Rule:** If `W > 53` bits, always use a string initialiser to guarantee all bits are set correctly.

---

### 2.3 Console I/O <a name="ap_int_io"></a>

**Preferred — C++ stream (all widths):**
```cpp
#include <iostream>
ap_uint<72> Val("10fedcba9876543210");
std::cout << Val        << std::endl;   // decimal: "313512663723845890576"
std::cout << std::hex   << Val << std::endl;   // hex
std::cout << std::oct   << Val << std::endl;   // octal
```

**Alternative — C `printf` via `to_string()`:**
```cpp
#include <cstdio>
ap_int<72> Val("80fedcba9876543210");
printf("%s\n",  Val.to_string().c_str());         // hex (default)
printf("%s\n",  Val.to_string(10).c_str());       // decimal
printf("%s\n",  Val.to_string(8).c_str());        // octal
printf("%s\n",  Val.to_string(16, true).c_str()); // hex, signed
```

`to_string()` optional arguments:

| Arg 1 (radix) | Default |
|:---:|:---:|
| `2` (binary) | **Yes** (default for `ap_int`) |
| `8`, `10`, `16` | — |

| Arg 2 (signed print) | Default |
|:---:|:---:|
| `false` = unsigned | **Yes** |
| `true` = signed | — |

> **Note:** For `ap_[u]fixed`, the `to_string()` default radix is **16 (hex)**.

---

### 2.4 Arithmetic Operators & Bit-Growth <a name="ap_int_arith"></a>

When two `ap_[u]int` values participate in arithmetic, the result width is determined automatically **before** assignment. Truncation or sign-extension then applies at the assignment target.

| Operator | Result Width | Result Sign |
|:---:|:---|:---|
| `+` (add) | `max(W_a, W_b) + 1`; `+2` if wider is unsigned and narrower is signed | Signed if either operand is signed |
| `-` (sub) | `max(W_a, W_b) + 1`; `+2` if wider is unsigned and narrower is signed | Always **signed** |
| `*` (mul) | `W_a + W_b` | Signed if either operand is signed |
| `/` (div) | `W_dividend` if divisor is unsigned; `W_dividend + 1` otherwise | Signed if either is signed |
| `%` (mod) | `min(W_a, W_b)` (same sign); `W_divisor + 1` if signs differ | Same as dividend |

> **IMPORTANT:** The `%` operator synthesises AMD LogiCORE divider cores in RTL. Use sparingly in hardware-critical paths.

Mixed-type widths assumed for C++ built-ins: `char`=8, `short`=16, `int`=32, `long`=32, `long long`=64.

```cpp
ap_uint<71> Rslt;
ap_uint<42> Val1 = 5;
ap_int<23>  Val2 = -8;

Rslt = Val1 + Val2;  // 43-bit result, sign-extended to 71 bits → -3
Rslt = Val1 * Val2;  // 65-bit result, sign-extended → -40
Rslt = 50   / Val2;  // 33-bit quotient → -6
Rslt = 50   % Val2;  // 23-bit remainder → +2
```

**Zero/Sign-Extension on narrow→wide assignment:**
```cpp
ap_uint<10> Result;
ap_int<7>   Val1 = 0x7f;   // signed
ap_uint<6>  Val2 = 0x3f;   // unsigned

Result = Val1;              // 0x3ff — sign-extended
Result = Val2;              // 0x03f — zero-padded
Result = ap_uint<7>(Val1);  // 0x07f — explicit zero-pad
Result = ap_int<6>(Val2);   // 0x3ff — explicit sign-extend
```

> **CAUTION:** Implicit conversion of `ap_[u]int` wider than 64 bits to a C++ built-in (`bool`, `int`, etc.) **truncates** to 64 bits silently. Always use explicit conversion methods (`to_int()`, `to_bool()`, etc.).

---

### 2.5 Bitwise & Logical Operators <a name="ap_int_bitwise"></a>

| Operator | Result Width | Result Sign |
|:---:|:---|:---|
| `\|`, `&`, `^` | `max(W_a, W_b)` | Unsigned iff **both** unsigned |
| `~` (bitwise NOT) | Same as operand | Same as operand |
| `!` (logical NOT) | `bool` | Returns `true` iff operand == 0 |
| `-` (unary neg) | Same `W` if signed; `W+1` if unsigned | Always signed |

**Compound assignment** (`+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `|=`, `^=`) is supported — rules from the base operator apply, result is then assigned back.

**Ternary operator:** Both branches must have the **same type**; cast explicitly:
```cpp
// Cast int to ap_int before using in ternary
ap_int<32> testc(int a, ap_int<32> b, bool d) {
    return d ? ap_int<32>(a) : b;
}
```

---

### 2.6 Shift Operators <a name="ap_int_shift"></a>

Each shift comes in **unsigned RHS** and **signed RHS** variants.

| Variant | Behaviour |
|:---|:---|
| `>> ap_uint<W2>` | Logical/arithmetic right-shift by positive amount |
| `>> ap_int<W2>` | If RHS is negative, shifts **left** instead |
| `<< ap_uint<W2>` | Logical left-shift |
| `<< ap_int<W2>` | If RHS is negative, shifts **right** instead |

- Result width = **same width as LHS operand** (no auto-widening).
- Shift-right on a **signed** type copies the sign bit (arithmetic shift).

```cpp
ap_uint<13> Rslt;
ap_uint<7>  Val1 = 0x41;

Rslt = Val1 << 6;              // 0x0040 — MSB of Val1 LOST!
Rslt = ap_uint<13>(Val1) << 6; // 0x1040 — cast prevents loss

ap_int<7>   Val2 = -63;
Rslt = Val2 >> 4;              // 0x1ffc — sign maintained
```

> **CAUTION:** When assigning a shift-left result into a wider destination, bits may be lost. **Explicitly cast the LHS to the destination width first.**

---

### 2.7 Bit-Level Methods <a name="ap_int_bitmethods"></a>

#### Concatenation
```cpp
ap_uint<10> Rslt;
ap_int<3>   Val1 = -3;
ap_int<7>   Val2 = 54;

Rslt = (Val2, Val1);       // comma operator: Val2 in MSBs → 0x1B5
Rslt = Val1.concat(Val2);  // concat: Val1 in MSBs, Val2 in LSBs → 0x2B6
(Val1, Val2) = 0xAB;       // decompose: Val1=1, Val2=43
```

#### Bit & Range Selection
```cpp
ap_uint<8> Val1 = 0x5f;
ap_uint<8> Val2 = 0xaa;
ap_uint<4> Rslt;

Rslt      = Val1.range(3, 0);  // Yields 0xF (bits 3..0)
Val1(3,0) = Val2(3, 0);        // Write range: Val1 → 0x5A
Rslt      = Val1.range(4, 7);  // Lo > Hi → bits returned REVERSED (0xA)
```

#### Bit Reduction Methods

| Method | Operation | Returns `true` when... |
|:---|:---|:---|
| `and_reduce()` | AND of all bits | All bits are 1 |
| `or_reduce()` | OR of all bits | At least one bit is 1 |
| `xor_reduce()` | XOR of all bits | Odd count of 1-bits |
| `nand_reduce()` | NAND of all bits | Not all bits are 1 |
| `nor_reduce()` | NOR of all bits | All bits are 0 |
| `xnor_reduce()` | XNOR of all bits | Even count of 1-bits |

```cpp
ap_uint<8> Val = 0xaa;   // 10101010
Val.and_reduce();   // false (not all 1)
Val.or_reduce();    // true
Val.xor_reduce();   // false (4 ones → even)
Val.xnor_reduce();  // true
```

#### Bit Manipulation Utilities

| Method | Signature | Description |
|:---|:---|:---|
| `length()` | `int length()` | Total bit-width |
| `reverse()` | `void reverse()` | Reverse bit order (LSB↔MSB) |
| `test(i)` | `bool test(unsigned i)` | Is bit `i` set? |
| `set(i, v)` | `void set(unsigned i, bool v)` | Set bit `i` to `v` |
| `set(i)` | `void set(unsigned i)` | Force bit `i` to 1 |
| `clear(i)` | `void clear(unsigned i)` | Force bit `i` to 0 |
| `invert(i)` | `void invert(unsigned i)` | Toggle bit `i` |
| `rrotate(n)` | `void rrotate(unsigned n)` | Rotate right by `n` |
| `lrotate(n)` | `void lrotate(unsigned n)` | Rotate left by `n` |
| `b_not()` | `void b_not()` | Bitwise NOT in-place |
| `sign()` | `bool sign()` | Returns `true` if negative |

```cpp
ap_uint<8> Val = 0x12;   // 0001 0010
Val.reverse();   // 0x48  (0100 1000)
Val.set(7);      // 0xC8  (1100 1000)
Val.clear(1);    // 0xC8→bit1 cleared
Val.invert(4);   // toggle bit 4
Val.rrotate(3);  // rotate right 3
Val.lrotate(6);  // rotate left 6
Val.b_not();     // bitwise NOT
```

---

### 2.8 Explicit Conversion Methods <a name="ap_int_conv"></a>

| Method | Return Type | Notes |
|:---|:---:|:---|
| `to_int()` | `int` (32-bit) | Truncates if value > 32-bit |
| `to_uint()` | `unsigned int` | Truncates if value > 32-bit |
| `to_int64()` | `long long` (64-bit) | Truncates if value > 64-bit |
| `to_uint64()` | `unsigned long long` | Truncates if value > 64-bit |
| `to_double()` | `double` | May lose precision for `W > 53` bits |

> **RECOMMENDED:** Always use explicit member functions (`to_int()`, `to_double()`, etc.) rather than C-style casts.

> **WARNING:** `sizeof(ap_int<N>)` returns the **object storage size**, not the logical bit-width. Use `.length()` or `::width` instead.

```
sizeof(ap_int<127>) = 16 bytes
sizeof(ap_int<128>) = 16 bytes
sizeof(ap_int<129>) = 24 bytes  ← jumps at storage boundary
```

---

### 2.9 Compile-Time Attributes <a name="ap_int_static"></a>

```cpp
static const int width = _AP_W;   // accessible as MyType::width
```

**Use-case — automatic bit-growth for downstream variable:**
```cpp
#define INPUT_DATA_WIDTH 8
typedef ap_int<INPUT_DATA_WIDTH> data_t;

data_t Val1, Val2;
ap_int<data_t::width + 1> Res = Val1 + Val2;  // Res is 9-bit, auto-adapts
```

---
---

## 3. ap\_\[u\]fixed — Arbitrary Precision Fixed-Point <a name="ap_ufixed"></a>

### 3.1 Representation & Template Parameters <a name="fixed_repr"></a>

A fixed-point value with **W** total bits and **I** integer bits is laid out as:

$$\text{Bit positions: } \underbrace{[I{-}1 \ldots 1\ \ 0]}_{\text{integer part}} \underbrace{[-1 \ldots -(W-I)]}_{\text{fractional part}}$$

The relationship between bit positions and value:

$$V = \sum_{k=-(W-I)}^{I-1} b_k \cdot 2^k$$

where $W = I + B$ and $B$ = fractional bits.

```
  MSB                        Binary point                  LSB
  [I-1] ... [1] [0]    .    [-1] ... [-(W-I)]
  ← integer part →           ← fractional part →
```

**Template syntax:**
```cpp
ap_[u]fixed<int W,          // Total word width
            int I,          // Integer bits (including sign)
            ap_q_mode Q,    // Quantization mode (default: AP_TRN)
            ap_o_mode O,    // Overflow mode    (default: AP_WRAP)
            ap_sat_bits N>; // Saturation bits for wrap (default: 0)
```

| Parameter | Description | Default |
|:---:|:---|:---:|
| **W** | Total word length in bits | — |
| **I** | Integer bits left of binary point (incl. sign bit). Negative `I` → implicit sign/zero bits to the right of the binary point. | — |
| **Q** | Quantization mode | `AP_TRN` |
| **O** | Overflow mode | `AP_WRAP` |
| **N** | Number of saturation bits (only relevant for `AP_WRAP` and `AP_WRAP_SM`) | `0` |

**Negative `I` examples:**
```cpp
ap_fixed<2,  0>  a = -0.5;   // range: {-0.5, 0, 0.5}
ap_ufixed<1, 0>  x = 0.5;    // 1-bit: {0, 0.5}
ap_ufixed<1,-1>  y = 0.25;   // 1-bit: {0, 0.25}
ap_fixed<1,-7>   z = 1.0/256;// 1-bit: represents 2^-8
```

> **NOTE:** `AP_SAT*` overflow modes can increase LUT usage by up to **20%** due to saturation logic. `hls_math` library functions do **not** support Q, O, N parameters — these modes only take effect at assignment/initialisation, not during intermediate calculations.

---

### 3.2 Quantization Modes (Q) <a name="fixed_quant"></a>

The **quantization mode** governs what happens when the result has more fractional precision than the destination type can hold.

| Mode | Short Description | `1.25` → `ap_fixed<3,2, MODE, AP_SAT>` | `-1.25` → same |
|:---|:---|:---:|:---:|
| **`AP_TRN`** *(default)* | Truncate towards −∞ | `1.0` | `-1.5` |
| **`AP_TRN_ZERO`** | Truncate towards zero | `1.0` | `-1.0` |
| **`AP_RND`** | Round to nearest, ties → +∞ | `1.5` | `-1.0` |
| **`AP_RND_ZERO`** | Round to nearest, ties → zero | `1.0` | `-1.0` |
| **`AP_RND_MIN_INF`** | Round to nearest, ties → −∞ | `1.0` | `-1.5` |
| **`AP_RND_INF`** | Round to nearest, ties away from zero | `1.5` | `-1.5` |
| **`AP_RND_CONV`** | Convergent (banker's) rounding — ties → even LSB | *see below* | — |

**AP_RND_CONV detail** — "Ties to even" means when a truncated value is exactly at the midpoint of two representable values, the LSB of the result is forced to 0:
```cpp
ap_fixed<8,3> p2 = 1.625;            // => tie with LSB-to-be = 0
ap_fixed<5,3,AP_RND_CONV> r = p2;    // 1.5 (LSB already 0, truncate)

ap_fixed<8,3> p3 = 1.375;            // => tie with LSB-to-be = 1
ap_fixed<5,3,AP_RND_CONV> r3 = p3;   // 1.5 (round up to make LSB = 0)
```

---

### 3.3 Overflow Modes (O, N) <a name="fixed_overflow"></a>

The **overflow mode** governs what happens when a result exceeds the representable range of the destination type.

| Mode | Short Description | Signed: `19.0` | Signed: `-19.0` |
|:---|:---|:---:|:---:|
| **`AP_WRAP`** *(default)* | Modular wrap-around | (wraps) | (wraps) |
| **`AP_WRAP_SM`** | Sign-magnitude wrap | `-4.0` | `2.0` |
| **`AP_SAT`** | Saturate to max/min | `7.0` | `-8.0` |
| **`AP_SAT_ZERO`** | Saturate to zero on any overflow | `0.0` | `0.0` |
| **`AP_SAT_SYM`** | Symmetric saturation (`-max` for signed neg.) | `7.0` | `-7.0` |

**`AP_WRAP` with the `N` parameter:**
- `N = 0` (default): All MSBs outside range are deleted; wraps as standard modular arithmetic.
- `N > 0`: The top `N` MSBs are saturated/forced to 1; the sign bit is preserved; remaining bits are copied from the LSB side.

**`AP_WRAP_SM` with `N > 0`:** Uses sign-magnitude saturation; `N` MSBs saturated to 1; positive stays positive, negative stays negative.

```cpp
// AP_SAT_SYM — negative max (not -8) for signed 4-bit
ap_fixed<4,4, AP_RND, AP_SAT_SYM> sf = -19.0;  // Yields -7.0 (not -8.0)
// AP_SAT (unsigned)
ap_ufixed<4,4, AP_RND, AP_SAT>    uf =  19.0;  // Yields 15.0
ap_ufixed<4,4, AP_RND, AP_SAT>    uf = -19.0;  // Yields  0.0
```

---

### 3.4 Initialization & Assignment <a name="fixed_init"></a>

**From floating-point literals** (precision limited to `float`/`double` width):
```cpp
#include "ap_fixed.h"
ap_ufixed<30,15>  a = 3.1415;           // init from double literal
ap_fixed<42,23>   b = -1158.987;
ap_fixed<36,30>   c = -0x123.456p-1;   // hex float literal
```

**From strings** (full precision for any width):
```cpp
// "dot" format: explicit binary point in string
ap_ufixed<2,0>  x = "0b0.01";         // 0.25
// "scientific" format: value × 2^exponent
ap_ufixed<2,0>  y = "0b01p-2";        // 0.25
ap_ufixed<2,0>  z = "0x4p-4";         // 0.25
// Pi with 60 fractional bits (requires string)
ap_ufixed<62,2> pi = "0b11.001001000011111101101010100010001000010110100011000010001101";
```

**`std::complex` arrays — must cast explicitly:**
```cpp
typedef ap_fixed<DIN_W, 1, AP_TRN, AP_SAT> coeff_t;

// WRONG — does NOT compile or work correctly:
// std::complex<coeff_t> rom[] = {{ 1, -0 }, { 0.9, -0.006 }};

// CORRECT — cast to std::complex<coeff_t>:
std::complex<coeff_t> rom[] = {
    std::complex<coeff_t>(1, -0),
    std::complex<coeff_t>(0.9, -0.006)
};
```

**Literal operators in expressions must be cast:**
```cpp
din1_t in1 = 0.25;
in1 = in1 + din1_t(0.25);   // CORRECT: literal cast to ap_fixed
// in1 = in1 + 0.25;         // WRONG: compiler sees 0.25 as double
```

---

### 3.5 Console I/O <a name="fixed_io"></a>

**C++ stream (preferred):**
```cpp
#include <iostream>
ap_fixed<6,3, AP_RND, AP_WRAP> Val = 3.25;
std::cout << Val         << std::endl;   // 3.25
std::cout << std::hex    << Val << std::endl;
std::cout << std::oct    << Val << std::endl;
```

**C `printf` via `to_string()`:**
```cpp
ap_fixed<6,3, AP_RND, AP_WRAP> Val = 3.25;
printf("%s\n",  Val.to_string().c_str());      // "0b011.010" (binary default for ap_fixed)
printf("%s\n",  Val.to_string(10).c_str());    // "3.25"
```

`to_string()` for `ap_[u]fixed`: default radix = **16** (hexadecimal).

**Formatting manipulators for `ap_[u]fixed`:**

| Manipulator | Purpose |
|:---|:---|
| `setprecision(n)` | Max meaningful decimal digits (default = 6) |
| `setw(w)` | Minimum field width |
| `setfill(c)` | Fill character when width > content |

```cpp
ap_fixed<64,32> f = 3.14159;
std::cout << std::setprecision(5) << f;  // 3.1416
std::cout << std::setprecision(9) << f;  // 3.14159

ap_fixed<65,32> aa = 123456;
std::cout << std::setprecision(5) << std::setw(13) << std::setfill('T') << aa;
// Output: "TTT1.2346e+05"
```

---

### 3.6 Arithmetic Operators & Bit-Growth <a name="fixed_arith"></a>

The result type `RType` is automatically determined to preserve full precision:

| Operator | Integer bits of result | Fractional bits of result |
|:---:|:---|:---|
| `+`, `-` | `max(I_a, I_b) + 1` | `max(F_a, F_b)` |
| `*` | `I_a + I_b` | `F_a + F_b` |
| `/` | `I_dividend + F_divisor` | `F_dividend` |
| `\|`, `&`, `^` | `max(I_a, I_b)` | `max(F_a, F_b)` |

$\text{Example for multiplication: } \text{ap\_fixed}<5,2> \times \text{ap\_fixed}<75,62> \Rightarrow \text{ap\_fixed}<80,64>$

```cpp
ap_fixed<76,63>  R_add;
ap_fixed<5,2>    Val1 = 1.125;
ap_fixed<75,62>  Val2 = 6721.356;

R_add = Val1 + Val2;  // Result: ap_fixed<76,63> → 6722.481
                      // (max I + 1 = 63, max F = 13)

ap_fixed<80,64>  R_mul;
R_mul = Val1 * Val2;  // I: 2+62=64, F: 3+13=16 → ap_fixed<80,64>

ap_fixed<84,66>  R_div;
R_div = Val2 / Val1;  // I: 62+3=65? actually I_dvd + F_dvsr = 62+3=65
                      // → careful: spec says I_result = I_dvd + F_dvsr
```

> **NOTE:** Shift operators do **not** apply quantization or overflow modes — the result type has the **same width** as the shifted variable; bits shifted out are simply lost. Cast to a wider type before shifting if precision must be preserved.

```cpp
ap_fixed<8,5> Val = 5.375;
ap_uint<4>    sh  = 2;
// Without cast — bits lost:
ap_fixed<25,15> R  = Val << sh;               // -10.5 (high bits shifted away)
// With cast — precision preserved:
ap_fixed<25,15> R2 = ap_fixed<10,7>(Val) << sh; // 21.5
```

---

### 3.7 Bit-Level & Class Methods <a name="fixed_methods"></a>

| Method | Signature | Description |
|:---|:---|:---|
| `length()` | `int length()` | Returns total bit width W |
| `[]` (bit select) | `af_bit_ref operator[](int bit)` | Read/write a single bit by index (LSB=0) |
| `range(Hi, Lo)` | `af_range_ref range(unsigned Hi, unsigned Lo)` | Read/write a range of bits; `Lo > Hi` reverses |
| `range()` | `af_range_ref range()` | All bits (equivalent to `range(W-1, 0)`) |

```cpp
ap_ufixed<4,2>  Value = 1.25;   // binary: 01.01
ap_uint<4>      Result;
ap_uint<8>      Repl = 0xAA;

Result       = Value.range(3,0);   // 0x5 (all 4 bits)
Value(3,0)   = Repl(3,0);          // overwrite bits 3..0 → -1.5
Result       = Value.range(0,3);   // reversed order → 0xA

Value[2] = 1;   // set bit 2 to 1
Value[3] = 0;   // clear bit 3
```

---

### 3.8 Explicit Conversion Methods <a name="fixed_conv"></a>

| Method | Return Type | Behaviour |
|:---|:---:|:---|
| `to_double()` | `double` | IEEE 754 double |
| `to_float()` | `float` | IEEE 754 single |
| `to_half()` | `half` | HLS 16-bit half precision |
| `to_ap_int()` | `ap_int<I>` | Integer bits only; fraction **truncated** |
| `to_int()` | `int` | 32-bit; truncates |
| `to_uint()` | `unsigned int` | 32-bit unsigned; truncates |
| `to_int64()` | `ap_slong` | 64-bit signed |
| `to_uint64()` | `ap_ulong` | 64-bit unsigned |

```cpp
ap_ufixed<256,77> x = 333.789;
double  d  = x.to_double();   // 333.789
float   f  = x.to_float();    // 333.789
half    h  = x.to_half();     // 333.789 (limited precision)
ap_uint<77> ai = x.to_ap_int(); // 333 (fraction truncated)
unsigned int ui = x.to_uint();  // 333
```

> **RECOMMENDED:** Prefer explicit member conversion functions over C-style casts.

---

### 3.9 Compile-Time Attributes <a name="fixed_static"></a>

`ap_[u]fixed` exposes four `static const` members accessible at compile time:

```cpp
static const int       width  = _AP_W;   // total bits W
static const int       iwidth = _AP_I;   // integer bits I
static const ap_q_mode qmode  = _AP_Q;   // quantization mode
static const ap_o_mode omode  = _AP_O;   // overflow mode
```

**Use-case — type-safe, auto-sized result with inherited modes:**
```cpp
#define INPUT_DATA_WIDTH 12
#define IN_INTG_WIDTH    6
#define IN_QMODE         AP_RND_ZERO
#define IN_OMODE         AP_WRAP

typedef ap_fixed<INPUT_DATA_WIDTH, IN_INTG_WIDTH, IN_QMODE, IN_OMODE> data_t;

data_t Val1, Val2;

// Res is 1 integer bit wider, inheriting Q/O modes — all computed at compile time
ap_fixed<data_t::width  + 1,
         data_t::iwidth + 1,
         data_t::qmode,
         data_t::omode>  Res = Val1 + Val2;
```

Changing `INPUT_DATA_WIDTH` or `IN_INTG_WIDTH` automatically propagates to `Res` without any manual updates.

---
---

## 4. Best Practices <a name="best_practices"></a>

### Hardware Efficiency

| Recommendation | Rationale |
|:---|:---|
| Always use the **exact bit-width** required — no rounding up to 8/16/32 | Prevents synthesising unnecessarily large operators (e.g., using a 32-bit DSP for a 17-bit multiply). |
| Prefer `ap_[u]fixed` over `float`/`double` in inner loops | Fixed-point maps directly to shift-add networks; floating point requires more complex, higher-latency hardware. |
| Prefer `AP_TRN` + `AP_WRAP` (defaults) in non-critical paths | Avoids extra saturation/rounding logic. Reserve `AP_SAT*` modes only where overflow protection is architecturally required — they can add up to **20% LUT overhead**. |
| Use `AP_RND_CONV` for DSP filters requiring minimum bias | Banker's rounding eliminates systematic truncation bias, important in accumulation-heavy designs like FIR filters. |
| Restrict the result width of arithmetic rather than the operand widths | Assign to a correctly-sized destination type; the compiler can elide redundant bits faster when they are never computed. When using power/sqrt functions, size the stored result: `ap_ufixed<16,7> y = hls::rsqrt<16,6>(x+x);` |

### Avoiding Common Pitfalls

| Pitfall | Fix |
|:---|:---|
| Array of AP types not initialised | Since 2023.2, use `= {}` or `= {0}` to zero-initialise. For older flows, explicitly initialise in a loop. |
| `sizeof()` returning wrong size | `sizeof(ap_int<N>)` returns storage bytes. Use `.length()` or `::width` for the logical bit-width. |
| Implicit truncation of `ap_int>64` to `bool` | Use `.to_bool()` or `.to_int()` explicitly — implicit conversion silently truncates to 64 bits. |
| String initialiser interpreted as wrong radix | Specify radix explicitly: `ap_int<6>("2A", 16)` — don't rely on auto-detection. Values `> 53` bits **require** a string (not a floating-point literal). |
| Shift-left losing bits into a wider variable | Always **cast** the value to the destination width before shifting: `ap_uint<13>(Val1) << 6`. |
| Mixing `ap_[u]fixed` with raw `0.25` literal in expressions | Cast literals to the AP type: `in1 + din1_t(0.25)` — the compiler cannot find a matching operator otherwise. |
| Using `std::complex<coeff_t>` array initialisation without cast | Wrap each element in `std::complex<coeff_t>(real, imag)`. |
| C-style cast instead of member conversion | Always use `.to_int()`, `.to_double()`, etc. C-style casts on AP types produce undefined or unexpected values. |

### Coding Style

```cpp
// ── GOOD: use typedef to centralise type definition ──────────────────────
#define W  18
#define I   6
typedef ap_fixed<W, I, AP_RND, AP_SAT> pixel_t;

// Downstream types automatically adapt via ::width / ::iwidth
typedef ap_fixed<pixel_t::width + 1,
                 pixel_t::iwidth + 1,
                 pixel_t::qmode,
                 pixel_t::omode>  accum_t;

// ── GOOD: use static ::width for compile-time portability ────────────────
ap_int<data_t::width + 1> Res = Val1 + Val2;   // correct bit-growth

// ── GOOD: use explicit conversions ───────────────────────────────────────
ap_ufixed<256, 77> x = 999.5;
printf("Integer part: %u\n", x.to_uint());      // not (unsigned int)(x)

// ── GOOD: string init for high-precision constants ───────────────────────
ap_ufixed<62, 2> pi = "0b11.001001000011111101101010100010001000010110100011000010001101";
```

### Quick Reference — Choosing Q/O Modes

| Use Case | Recommended Q | Recommended O |
|:---|:---:|:---:|
| Default / max HW efficiency | `AP_TRN` | `AP_WRAP` |
| Audio/Video DSP (bias-free rounding) | `AP_RND_CONV` | `AP_SAT` |
| Safety-critical accumulator | `AP_RND` | `AP_SAT` |
| Neural network quantisation (round-to-zero) | `AP_RND_ZERO` | `AP_SAT` |
| CORDIC / iterative algorithm | `AP_TRN` | `AP_WRAP` |
| Signed ↔ unsigned boundary crossing | `AP_TRN_ZERO` | `AP_SAT_SYM` |

---

*Summary generated from Vitis HLS UG1399 v2025.2 — Chapter 21, Pages 730–782.*
