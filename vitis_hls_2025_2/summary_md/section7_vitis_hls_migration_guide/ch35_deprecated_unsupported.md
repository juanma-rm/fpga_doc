# Chapter 35 — Deprecated and Unsupported Features

> UG1399 (v2025.2) · Section VII: Vitis HLS Migration Guide · Pages 882–886

## Table of Contents

- [Notation](#notation)
- [Deprecated and Unsupported Tcl / Pragma Commands](#deprecated-and-unsupported-tcl--pragma-commands)
- [Deprecated Libraries](#deprecated-libraries)
  - [Linear Algebra Library](#linear-algebra-library)
  - [DSP Library](#dsp-library)

---

## Notation

| Status | Meaning |
|---|---|
| **Deprecated** | Still accepted; a warning is issued advising discontinuance in a future release |
| **Unsupported** | Vitis HLS errors out with a descriptive message |
| `*` | All options of the command are affected |

---

## Deprecated and Unsupported Tcl / Pragma Commands

| Type | Command | Option | Status | Details / Replacement |
|---|---|---|---|---|
| config | `config_interface` | `-m_axi_max_data_size` | Deprecated | — |
| config | `config_interface` | `-m_axi_min_data_size` | Deprecated | — |
| config | `config_interface` | `-m_axi_alignment_byte_size` | Deprecated | — |
| config | `config_interface` | `-m_axi_offset=slave` | Unsupported | Use `-m_axi_offset=direct` + `-default_slave_interface=s_axilite` |
| config | `config_interface` | `-expose_global` | Unsupported | Global variables cannot be exposed as top-level ports in Vitis HLS |
| config | `config_interface` | `-trim_dangling_port` | Unsupported | — |
| config | `config_array_partition` | `-auto_promotion_threshold` | Deprecated | — |
| config | `config_array_partition` | `-auto_partition_threshold` | Deprecated | Renamed to `-complete_threshold` |
| config | `config_array_partition` | `-scalarize_all` | Unsupported | — |
| config | `config_array_partition` | `-throughput_driven` | Unsupported | — |
| config | `config_array_partition` | `-maximum_size` | Unsupported | — |
| config | `config_array_partition` | `-include_extern_globals` | Unsupported | — |
| config | `config_array_partition` | `-include_ports` | Unsupported | — |
| config | `config_schedule` | All options except `-enable_dsp_fill_reg` | Deprecated | — |
| config | `config_bind` | `*` | Deprecated | — |
| config | `config_rtl` | `-encoding` | Deprecated | FSM encoding is now always one-hot |
| config | `config_sdx` | `*` | Deprecated | Replaced by `open_solution -flow_target [vitis\|vivado]` |
| config | `config_flow` | `*` | Deprecated | — |
| config | `config_dataflow` | `-disable_start_propagation` | Deprecated | — |
| config | `config_rtl` | `-auto_prefix` | Deprecated | Replaced by `config_rtl -module_prefix` |
| config | `config_rtl` | `-prefix` | Deprecated | Replaced by `config_rtl -module_prefix` |
| config | `config_rtl` | `-m_axi_conservative_mode` | Deprecated | Use `config_interface -m_axi_conservative_mode` |
| directive/pragma | `set_directive_pipeline` | `-enable_flush` | Deprecated | — |
| directive/pragma | `CLOCK` | `*` | Unsupported | — |
| directive/pragma | `DATA_PACK` | `*` | Unsupported | Use `AGGREGATE` pragma/directive; use `__attribute__(packed(X))` if needed |
| directive/pragma | `INLINE` | `-region` | Deprecated | — |
| directive/pragma | `INTERFACE` | `-mode ap_bus` | Unsupported | Use `m_axi` interface instead |
| directive/pragma | `INTERFACE` | `-mode ap_stable` | Deprecated | Use `STABLE` pragma or directive instead |
| directive/pragma | `ARRAY_MAP` | `*` | Unsupported | — |
| directive/pragma | `RESOURCE` | `*` | Deprecated | Replaced by `BIND_OP` and `BIND_STORAGE` pragmas/directives; use `INTERFACE` pragma with `storage_type` for top-level arguments |
| directive/pragma | `SHARED` | `*` | Deprecated | Moved to `type=shared` option on `STREAM` pragma/directive |
| directive/pragma | `STREAM` | `-dim` | Unsupported | — |
| directive/pragma | `STREAM` | `-off` | Deprecated | `STREAM -off` → use `STREAM type=pipo` |
| project | `csim_design` | `-clang_sanitizer` | Renamed/Added | — |
| project | `export_design` | `-use_netlist` | Deprecated | Use `export_design -format ip_catalog` |
| project | `export_design` | `-xo` | Deprecated | Use `export_design -format xo` |
| project | `add_files` | SystemC files | Unsupported | SystemC is not supported by Vitis HLS |
| config | `config_export` | `-disable_deadlock_detection` | Deprecated | Replaced by `config_export -deadlock_detection_sim` |

---

## Deprecated Libraries

### Linear Algebra Library

The `hls_linear_algebra.h` monolithic library is deprecated. Use individual function headers from the `hls/linear_algebra/` directory, or the **Vitis Solver** library for float/double precision.

| Deprecated API | Input Type | Vitis Solver Replacement |
|---|---|---|
| `cholesky` | `float`, `ap_fixed`, `x_complex<float>`, `x_complex<ap_fixed>` | `potrf` (`float`, `double`) |
| `cholesky_inverse` | `float`, `ap_fixed`, `x_complex<float>`, `x_complex<ap_fixed>` | `pomatrixinverse` (`float`, `double`) |
| `matrix_multiply` | `float`, `ap_fixed`, `x_complex<float>`, `x_complex<ap_fixed>` | No direct replacement |
| `qrf` | `float`, `x_complex<float>` | `geqrf` (`float`, `double`) |
| `qr_inverse` | `float`, `x_complex<float>` | No direct replacement |
| `svd` | `float`, `x_complex<float>` | `gesvdj` (`float`, `double`) |

**New header structure:**
```
hls/linear_algebra/
├── hls_back_substitute.h
├── hls_cholesky.h
├── hls_cholesky_inverse.h
├── hls_matrix_multiply.h
├── hls_qr_inverse.h
├── hls_qrf.h
├── hls_svd.h
└── utils/
    ├── std_complex_utils.h
    ├── x_hls_complex.h
    ├── x_hls_matrix_tb_utils.h
    └── x_hls_matrix_utils.h
```

### DSP Library

The `hls_dsp.h` monolithic library is deprecated. Use the **HLS Math library** for standard math functions.

| Deprecated API | Input/Output | Replacement |
|---|---|---|
| `atan2` | `std::complex<ap_fixed>` → `ap_ufixed` | HLS Math `atan2` (`ap_fixed`, `float`, `double`) |
| `sqrt` | unsigned binary fraction → unsigned int | HLS Math `sqrt` (`ap_fixed`, `float`, `double`) |
| `awgn` (Additive White Gaussian Noise) | `ap_ufixed` → `ap_int` | No direct HLS Math replacement |
| `cmpy` (complex multiply) | `std::complex<ap_fixed>` → `std::complex<ap_fixed>` | HLS Math or DSP intrinsics |
| `convolution_encoder` | `ap_uint` → `ap_uint` | No direct replacement |
| `viterbi_decoder` | `ap_uint` → `ap_uint` | No direct replacement |
| `nco` (Numerically-Controlled Oscillator) | `ap_uint` → `std::complex<ap_int>` | Use DDS IP Library (`hls_dds.h`) |

**New individual DSP headers:**
```
hls/dsp/
├── hls_atan2_cordic.h
├── hls_awgn.h
├── hls_cmpy.h
├── hls_convolution_encoder.h
├── hls_nco.h
├── hls_qam_demod.h
├── hls_qam_mod.h
├── hls_sqrt_cordic.h
├── hls_viterbi_decoder.h
└── utils/
    ├── hls_cordic.h
    ├── hls_cordic_functions.h
    └── hls_dsp_common_utils.h
```

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 35, pages 882–886*
