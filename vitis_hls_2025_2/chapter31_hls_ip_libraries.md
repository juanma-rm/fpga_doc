# Chapter 31 — HLS IP Libraries

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 843–870

## Table of Contents

- [Overview](#overview)
- [DSP Intrinsics (`hls_dsp_builtins.h`)](#dsp-intrinsics-hls_dsp_builtinsh)
  - [Port Data Types by Platform](#port-data-types-by-platform)
  - [Core Functions](#core-functions)
  - [Register Flags](#register-flags)
  - [Unsigned Input Handling](#unsigned-input-handling)
  - [Accumulator Class](#accumulator-class)
  - [Cascade Class](#cascade-class)
  - [DSP Complex Intrinsics (dspcplx — Versal only)](#dsp-complex-intrinsics-dspcplx--versal-only)
- [FFT IP Library (`hls_fft.h`)](#fft-ip-library-hls_ffth)
  - [Configuration Structure](#configuration-structure)
  - [Runtime Arguments](#runtime-arguments)
  - [Key Configuration Parameters](#key-configuration-parameters)
  - [SSR Restrictions](#ssr-restrictions)
  - [Usage Notes](#fft-usage-notes)
- [FIR IP Library (`hls_fir.h`)](#fir-ip-library-hls_firh)
  - [Configuration Structure](#fir-configuration-structure)
  - [Key Configuration Parameters](#fir-key-configuration-parameters)
  - [Usage Notes](#fir-usage-notes)
- [DDS IP Library (`hls_dds.h`)](#dds-ip-library-hls_ddsh)
  - [Configuration Structure](#dds-configuration-structure)
  - [Key Configuration Parameters](#dds-key-configuration-parameters)
- [SRL Shift Register (`ap_shift_reg.h`)](#srl-shift-register-ap_shift_regh)
  - [Methods](#srl-methods)
  - [Example](#srl-example)
- [Best Practices](#best-practices)

---

## Overview

Chapter 31 covers five IP libraries that map directly to Xilinx DSP primitives and DSP-based IP cores:

| Library | Header | Purpose |
|---|---|---|
| DSP Intrinsics | `hls_dsp_builtins.h` | Direct mapping to DSP48/DSP58 slices |
| FFT | `hls_fft.h` | Xilinx FFT IP wrapper |
| FIR | `hls_fir.h` | Xilinx FIR Compiler IP wrapper |
| DDS | `hls_dds.h` | Xilinx DDS Compiler IP wrapper |
| SRL Shift Register | `ap_shift_reg.h` | Direct mapping to SRL shift-register primitive |

---

## DSP Intrinsics (`hls_dsp_builtins.h`)

Direct intrinsics for explicitly targeting DSP48E1, DSP48E2, DSP58, and Versal complex DSP slices.

**Namespaces:**
```cpp
hls::dsp48e1::   // 7-series DSPs
hls::dsp48e2::   // UltraScale/UltraScale+ DSPs
hls::dsp58::     // Versal DSPs
hls::dspcplx::   // Versal complex DSP
```

### Port Data Types by Platform

| Type | DSP48E1 | DSP48E2 | DSP58 |
|---|---|---|---|
| A_t | `ap_int<25>` | `ap_int<27>` | `ap_int<27>` |
| B_t | `ap_int<18>` | `ap_int<18>` | `ap_int<24>` |
| C_t | `ap_int<48>` | `ap_int<48>` | `ap_int<58>` |
| D_t | `ap_int<25>` | `ap_int<27>` | `ap_int<27>` |
| P_t | `ap_int<48>` | `ap_int<48>` | `ap_int<58>` |

### Core Functions

All functions are templated on a `flags` bitmask of type `int64_t` specifying which pipeline registers to insert.

```cpp
// using dsp48e2 as example
using namespace hls::dsp48e2;

P_t mul_add    (A_t a, B_t b, C_t c, int64_t flags = 0);  // P = A×B + C
P_t mul_sub    (A_t a, B_t b, C_t c, int64_t flags = 0);  // P = A×B − C
P_t add_mul_add(A_t a, D_t d, B_t b, C_t c, int64_t flags = 0);  // P = (A+D)×B + C
P_t sub_mul_add(A_t a, D_t d, B_t b, C_t c, int64_t flags = 0);  // P = (A−D)×B + C
// reverse-subtract variants also available
```

### Register Flags

Combine flags with bitwise OR to enable pipeline registers at specific stages.

| Flag Constant | Register Location |
|---|---|
| `REG_A1` | A input register stage 1 |
| `REG_A2` | A input register stage 2 |
| `REG_B1` | B input register stage 1 |
| `REG_B2` | B input register stage 2 |
| `REG_C`  | C input register |
| `REG_D`  | D input register |
| `REG_AD` | A+D pre-adder register |
| `REG_M`  | Multiplier output register |
| `REG_P`  | P output register |

Example — full pipeline (maximum registered stages):
```cpp
constexpr int64_t FULL = hls::dsp48e2::REG_A1 | hls::dsp48e2::REG_A2 |
                         hls::dsp48e2::REG_B1 | hls::dsp48e2::REG_B2 |
                         hls::dsp48e2::REG_C  | hls::dsp48e2::REG_M  |
                         hls::dsp48e2::REG_P;
auto result = hls::dsp48e2::mul_add(a, b, c, FULL);
```

### Unsigned Input Handling

DSP slices have a **signed multiplier**. For unsigned operands:
- Use a type that is **1 bit smaller** than the unsigned width.
- Ensure the MSB is always 0 (guarantees the signed interpretation is positive).

```cpp
// For 18-bit unsigned B input on dsp48e2:
ap_uint<17> b_unsigned = ...;       // reduce to 17 bits
ap_int <18> b_signed   = b_unsigned; // sign bit is always 0
hls::dsp48e2::mul_add(a, b_signed, c);
```

### Accumulator Class

`hls::dsp(48e1|48e2|58)::acc<flags>` provides a stateful accumulation object with a reset signal:

```cpp
hls::dsp48e2::acc<flags> acc_obj;

// Inside a loop:
bool reset = (i == 0);                     // reset P to 0 on first iteration
P_t sum = acc_obj.mul_acc(a, b, reset);    // P += A×B; if reset: P = 0

// With pre-adder:
P_t sum = acc_obj.add_mul_acc(a, d, b, reset);  // P += (A+D)×B
```

| Method | Operation |
|---|---|
| `mul_acc(a, b, init)` | If `init`: P=A×B; else P+=A×B |
| `add_mul_acc(a, d, b, init)` | If `init`: P=(A+D)×B; else P+=(A+D)×B |

### Cascade Class

`hls::dsp(48e1|48e2|58)::cascade<flags>` connects multiple DSP slices in hardware cascade chains (routed via dedicated cascade routing, not fabric LUTs).

```cpp
hls::dsp48e2::cascade<flags> casc_array[4];
#pragma HLS ARRAY_PARTITION variable=casc_array complete  // must be fully partitioned

typedef hls::dsp48e2::cascade<flags>::R_t R_t;   // contains {acout, bcout, pcout}

R_t r1 = casc_array[0].mul_add(a[0], b[0], c[0]);
R_t r2 = casc_array[1].mul_add(r1.acout, r1.bcout, r1.pcout);
// ...
```

**Cascade restrictions:**
- Array of cascades must be fully partitioned (`ARRAY_PARTITION complete`)
- Requires `REG_A1`, `REG_A2`, `REG_B1`, `REG_B2`, `REG_P` flags
- Flags `REG_AD`, `REG_D`, `REG_C` cannot be used with cascade
- Vivado selects cascade connections at placement time

### DSP Complex Intrinsics (dspcplx — Versal only)

Targets Versal's native complex DSP58 support for 18×18 complex multiplication using **2 DSP58s instead of 3**.

```cpp
using namespace hls::dspcplx;
typedef std::complex<ap_int<18>> A_t;  // A = B = 18-bit complex
typedef std::complex<ap_int<58>> C_t;  // C = 58-bit complex
typedef std::complex<ap_int<58>> P_t;  // P = 58-bit complex

P_t p = hls::dspcplx::mul_add(a, b, c, flags);   // P = A×B + C (complex)
```

**Pipeline configuration options:**

| Constant | Description |
|---|---|
| `NO_PIPELINE`       | No registers between stages |
| `BALANCED_PIPELINE` | Balanced latency pipelining |
| `FULL_PIPELINE`     | Maximum latency, highest throughput |

---

## FFT IP Library (`hls_fft.h`)

Wrapper around the Xilinx FFT IP core with streaming and array interfaces.

**Header:**
```cpp
#include "hls_fft.h"
```

### Configuration Structure

Derive from `hls::ip_fft::params_t` to override defaults:

```cpp
struct my_fft_config : hls::ip_fft::params_t {
    static const unsigned input_width          = 16;
    static const unsigned output_width         = 16;
    static const unsigned config_width         = 16;
    static const unsigned log2_transform_length = 10;  // 1024-point FFT
    static const bool     has_nfft             = false;
    static const unsigned channels             = 1;
    static const unsigned output_ordering      = hls::ip_fft::natural_order;
    static const unsigned scaling_options      = hls::ip_fft::block_floating_point;
    static const unsigned rounding_modes       = hls::ip_fft::truncation;
    static const unsigned super_sample_rate    = hls::ip_fft::ssr_1;
    static const bool     use_native_float     = false;   // Versal floating-point
};
```

### Runtime Arguments

| Argument | Type | Direction | Description |
|---|---|---|---|
| `fwd_inv` | bool | in | `true` = forward FFT, `false` = inverse IFFT |
| `scale_sch` | ap_uint<log2(N)*2> | in | Scaling schedule (one bit per stage) |
| `cp_len`  | ap_uint<log2(N)> | in | Cyclic prefix insertion length (OFDM) |
| `ovflo`   | bool | out | Overflow flag |
| `blk_exp` | ap_uint<5> | out | Block exponent (block floating-point mode) |

### Key Configuration Parameters

| Parameter | Default | Range / Options |
|---|---|---|
| `input_width` | 16 | 8–32 |
| `output_width` | — | Derived from input_width and transform length |
| `log2_transform_length` | 10 | 3–16 (supports 8 to 65536 points) |
| `channels` | 1 | 1–12 |
| `output_ordering` | `natural_order` | `natural_order`, `bit_reversed_order` |
| `scaling_options` | `block_floating_point` | `block_floating_point`, `scaled`, `unscaled` |
| `rounding_modes` | `truncation` | `truncation`, `rounding` |
| `super_sample_rate` | `ssr_1` | `ssr_1` to `ssr_64` |
| `use_native_float` | `false` | Versal floating-point (overrides widths) |

### SSR Restrictions

When `super_sample_rate > ssr_1`:

| Feature | Supported with SSR>1 |
|---|---|
| Dynamic configuration | No |
| Cyclic prefix | No |
| Overflow output | No |
| Inverse FFT (dynamic) | No (use `systolicfft_inv` static config) |

### FFT Usage Notes

- Interfaces: supports both `hls::stream` and fixed-size arrays.
- Supports single-channel and multi-channel configurations.
- Use `#pragma HLS DATAFLOW` at the top level to pipeline multiple FFT calls — **do not** use a pipelined loop.
- Multi-channel FFT interleaves channels in time on the single stream interface.

---

## FIR IP Library (`hls_fir.h`)

Wrapper around the Xilinx FIR Compiler IP core.

**Header:**
```cpp
#include "hls_fir.h"
```

**Usage:**
```cpp
hls::FIR<my_fir_config> fir_inst;
fir_inst.run(fir_in, fir_out);          // without runtime config
fir_inst.run(fir_in, fir_out, &config); // with runtime coefficient reload
```

### FIR Configuration Structure

Derive from `hls::ip_fir::params_t`:

```cpp
struct my_fir_config : hls::ip_fir::params_t {
    static const unsigned data_width   = 16;
    static const unsigned coeff_width  = 16;
    static const unsigned output_rounding_mode = hls::ip_fir::truncate_lsbs;
    static const unsigned filter_type  = hls::ip_fir::single_rate;
    static const unsigned interp_rate  = 1;
    static const unsigned decim_rate   = 1;
    static const unsigned num_coeffs   = 21;
    static const unsigned filter_arch  = hls::ip_fir::systolic_multiply_accumulate;
    // Coefficients MUST always be specified — no defaults!
    static const double   coeff_vec[num_coeffs];
};
const double my_fir_config::coeff_vec[] = { /* your taps */ };
```

### FIR Key Configuration Parameters

| Parameter | Default | Notes |
|---|---|---|
| `data_width` | 16 | Must be a multiple of 8 (AXI-S interface) |
| `coeff_width` | 16 | Must be a multiple of 8 |
| `num_coeffs` | 21 | Total number of filter taps |
| `filter_type` | `single_rate` | `single_rate`, `interpolation`, `decimation`, `hilbert` |
| `interp_rate` | 1 | Interpolation factor (for `interpolation` filter type) |
| `decim_rate` | 1 | Decimation factor (for `decimation` filter type) |
| `filter_arch` | `systolic_multiply_accumulate` | `systolic_multiply_accumulate`, `transpose_multiply_accumulate` |
| `coeff_vec[]` | *none* | **MUST be specified** — no default coefficients |

### FIR Usage Notes

- `fir_in` and `fir_out` must be `ap_fifo` interfaces, or local arrays/streams — **not** direct `m_axi` connections.
- Data widths (data and coeff) must be multiples of 8 due to the internal AXI-S binding.
- Output array length must match: `input_length × interp_rate / decim_rate` when using rate-change filters.
- SSR=1 only (single-lane input/output).

---

## DDS IP Library (`hls_dds.h`)

Wrapper around the Xilinx DDS Compiler IP core (sine/cosine wave generation).

**Header:**
```cpp
#include "hls_dds.h"
```

**Usage:**
```cpp
hls::DDS<my_dds_config> dds_inst;
dds_inst.run(data_channel, phase_channel);
```

### DDS Configuration Structure

Derive from `hls::ip_dds::params_t`:

```cpp
struct my_dds_config : hls::ip_dds::params_t {
    static const double   DDS_Clock_Rate  = 20.0;  // MHz
    static const unsigned Channels        = 1;
    static const unsigned Mode            = hls::ip_dds::STANDARD;
    static const unsigned Phase_Width     = 16;    // must be multiple of 8
    static const unsigned Output_Width    = 16;    // must be multiple of 8
    static const unsigned Phase_Increment = hls::ip_dds::FIXED;
    static const unsigned Phase_Offset    = hls::ip_dds::NONE;
    static const unsigned Output_Selection = hls::ip_dds::SINE;
    static const unsigned Noise_Shaping   = hls::ip_dds::NONE;
};
```

### DDS Key Configuration Parameters

| Parameter | Default | Options / Range |
|---|---|---|
| `DDS_Clock_Rate` | 20.0 | Clock frequency in MHz |
| `Channels` | 1 | 1–16 |
| `Mode` | `STANDARD` | `STANDARD`, `RASTERIZED` |
| `Phase_Width` | 16 | Multiples of 8 |
| `Output_Width` | 16 | Multiples of 8 |
| `Phase_Increment` | `FIXED` | `FIXED` only (programmable not supported in HLS wrapper) |
| `Phase_Offset` | `NONE` | `NONE`, `FIXED` |
| `Output_Selection` | `SINE` | `SINE`, `COSINE`, `SIN_AND_COS` |
| `Noise_Shaping` | `NONE` | `NONE`, `PHASE_DITHER`, `TAYLOR_SERIES`, `AUTO` |

---

## SRL Shift Register (`ap_shift_reg.h`)

Maps a shift register directly to AMD's SRL (Shift Register LUT) primitive — avoids inference of flip-flop chains and enables efficient deep shift registers on FPGA.

**Header:**
```cpp
#include "ap_shift_reg.h"
```

**Declaration:**
```cpp
static ap_shift_reg<data_type, depth> shift_reg_name;
```

> Must be declared `static` — the underlying hardware is persistent.

### SRL Methods

| Method | Description |
|---|---|
| `read(pos)` | Read value at shift position `pos` without shifting |
| `shift(new_val, pos)` | Read `pos`, then shift all values up by one position (pos 0 ← `new_val`); returns old value at `pos` |
| `shift(new_val, pos, enable)` | Same as above, but only shifts when `enable` is true; returns old value at `pos` |

### SRL Example

```cpp
#include "ap_shift_reg.h"

typedef ap_shift_reg<int, 4> SR_t;   // 4-deep integer shift register

int delay_line(int in_val) {
    static SR_t sr;
    return sr.shift(in_val, 3);      // insert in_val, return value 3-delays ago
}
```

Pipeline-safe usage — the enable signal allows use inside conditional pipelines:
```cpp
static ap_shift_reg<bool, 8> valid_sr;
valid_sr.shift(new_valid, 7, pipeline_enable);
```

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Use `flags` bitmask to control DSP pipeline registers | Allows HLS to map exactly the required register stages to DSP registers (not fabric FFs) |
| For unsigned DSP inputs, use 1-bit-smaller unsigned types, cast to signed | DSP multipliers are signed — excess bits cause wrong results |
| Fully partition arrays of cascade objects | Vivado needs each cascade element independently — partial partition causes failures |
| Never share FIR/FFT/DDS instances across dataflow processes | Each IP instance maps to a single hardware block; concurrent access causes conflicts |
| Use `DATAFLOW` with FIR/FFT, not pipelined loops | IP cores have deep pipeline latency; DATAFLOW allows multiple calls in flight |
| Declare SRL shift registers as `static` | Non-static declaration would create new shift registers every call (functionally wrong) |
| Specify FIR coefficients explicitly | `hls::ip_fir::params_t` has no default coefficient array — missing coefficients cause compile errors |
| Set data/coeff widths to multiples of 8 for FIR/DDS | Internal AXI-S binding requires byte-aligned widths |

---

### See Also

- [Chapter 23 — HLS Math Library](ch23_hls_math_library.md) — Math functions (some share DSP IP)
- [Chapter 11 — Optimizing Techniques](../section2_hls_programmers_guide/ch11_optimizing_techniques.md) — Expression balancing and DSP matching
- [Chapter 17 — HLS Pragmas](../section4_vitis_hls_command_reference/ch17_hls_pragmas.md) — `BIND_OP`, `BIND_STORAGE` pragmas

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 31, pages 843–870*
