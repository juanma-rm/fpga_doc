# Chapter 34 — Migrating from Vivado HLS to Vitis HLS

> UG1399 (v2025.2) · Section VII: Vitis HLS Migration Guide · Pages 875–881

## Table of Contents

- [Overview](#overview)
- [Tool-Specific Macro](#tool-specific-macro)
- [Default Control Settings](#default-control-settings)
  - [Vivado IP Development Flow Defaults](#vivado-ip-development-flow-defaults)
  - [Vitis Application Acceleration Flow Defaults](#vitis-application-acceleration-flow-defaults)
- [Interface Differences](#interface-differences)
  - [AXI Bundle Rules](#axi-bundle-rules)
  - [Memory Storage Type on Interface](#memory-storage-type-on-interface)
  - [AXI4-Stream Side-Channels](#axi4-stream-side-channels)
- [Memory Model Changes](#memory-model-changes)
- [Unconnected Ports](#unconnected-ports)
- [Global Variables on the Interface](#global-variables-on-the-interface)
- [Module Naming Changes](#module-naming-changes)
  - [Auto-Prefix Behavior](#auto-prefix-behavior)
  - [Memory Module and RTL File Names](#memory-module-and-rtl-file-names)
- [Function Inlining Changes](#function-inlining-changes)
- [Dataflow: std::complex Support](#dataflow-stdcomplex-support)
- [Best Practices](#best-practices)

---

## Overview

AMD Vivado HLS last official release was 2020.1. AMD Vitis HLS is the next-generation HLS solution with an updated LLVM-based compiler supporting **C/C++11/14**. New features include:

- Stricter **syntax checking** — errors on unconnected ports.
- **Pragma Conflict Checker** — warnings/errors for pragma conflicts or typos.
- Better diagnostic messages when user pragmas are ignored.

When migrating from Vivado HLS to Vitis HLS, review the following areas before comparing QoR numbers: default settings, interface behavior, memory model, and inlining.

---

## Tool-Specific Macro

To differentiate code between Vivado HLS and Vitis HLS in shared source files, use the predefined macro:

```cpp
#if defined(__VITIS_HLS__)
    // Vitis HLS-specific code here
#endif
```

---

## Default Control Settings

### Vivado IP Development Flow Defaults

Target: `open_solution -flow_target vivado`

| Setting | Vivado HLS | Vitis HLS |
|---|---|---|
| `config_compile -pipeline_loops` | 0 | 64 |
| `config_export -vivado_optimization_level` | 2 | 0 |
| `set_clock_uncertainty` | 12.5% | 27% |
| `config_interface -m_axi_alignment_byte_size` | N/A | 0 |
| `config_interface -m_axi_max_widen_bitwidth` | N/A | 0 |
| `config_export -vivado_phys_opt` | place | none |
| `config_interface -m_axi_addr64` | false | true |
| `config_schedule -enable_dsp_full_reg` | false | true |
| `config_rtl -module_auto_prefix` | false | true |
| Interface pragma defaults | ip mode | ip mode |

### Vitis Application Acceleration Flow Defaults

Target: `open_solution -flow_target vitis`

| Setting | `flow_target=vitis` | `flow_target=vivado` |
|---|---|---|
| `config_compile -pipeline_loops` | 0 | 64 |
| `config_export -vivado_optimization_level` | 2 | 0 |
| `set_clock_uncertainty` | 12.5% | 27% |
| `config_interface -m_axi_alignment_byte_size` | 0 | 64 |
| `config_interface -m_axi_latency` | 0 | 64 |
| `config_interface -m_axi_max_widen_bitwidth` | 0 | 512 |
| `config_export -vivado_phys_opt` | place | none |
| `config_interface -m_axi_addr64` | false | true |
| `config_schedule -enable_dsp_full_reg` | false | true |
| `config_rtl -module_auto_prefix` | false | true |
| `config_rtl -register_reset_num` | 0 | 3 |
| Interface pragma defaults | ip mode | kernel mode |

> **Key impact:** The clock uncertainty increase from 12.5% to 27% in Vitis HLS is the most common cause of Fmax differences when comparing QoR between tools.

---

## Interface Differences

### AXI Bundle Rules

Vitis HLS groups function arguments with compatible options into a single `m_axi`/`s_axilite` adapter by default. Bundling saves device resources but can limit memory bandwidth. Use **multiple bundles** to connect to multiple memory banks for higher throughput.

See: *M_AXI Bundles / S_AXILITE Bundles* section in UG1399 for full rule details.

### Memory Storage Type on Interface

The deprecated `RESOURCE` pragma is replaced by `storage_type` on the `INTERFACE` pragma:

```cpp
#pragma HLS INTERFACE ap_memory port=in1  storage_type=RAM_2P
#pragma HLS INTERFACE ap_memory port=out  storage_type=RAM_1P latency=3
```

Default behavior when no `storage_type` is specified:
- Single-port RAM by default.
- Dual-port RAM if it reduces II or latency.

### AXI4-Stream Side-Channels

AXI4-Stream side-channel signals (`TKEEP`, `TSTRB`, `TID`, etc.) are handled differently between Vivado HLS and Vitis HLS. In Vitis HLS, side-channel signals are registered whenever TDATA is registered, with additional limitations. See *AXI4-Stream Interfaces with Side-Channels* in UG1399.

---

## Memory Model Changes

Vitis HLS uses a different memory model from Vivado HLS — aligning with the **C++ compiler standard for data alignment**:

| Aspect | Vivado HLS | Vitis HLS |
|---|---|---|
| Struct aggregation at interface | Disaggregated by default | **Aggregated by default** — use `AGGREGATE`/`disaggregate` pragma to change |
| Struct with `hls::stream` member | Disaggregated | Disaggregated (exception to aggregation default) |
| Struct with partitioned internal array | Disaggregated | Disaggregated (exception to aggregation default) |
| Structs in internal / global code | Disaggregated | Disaggregated — decomposed into member elements |
| Arrays of structs | Arrays of structs | Multiple arrays (one per struct member) |

> **Action required:** If your Vivado HLS design relied on interface struct disaggregation, add `#pragma HLS disaggregate` to Vitis HLS for the same behavior.

---

## Unconnected Ports

| Port Type | Vivado HLS | Vitis HLS |
|---|---|---|
| Unconnected output scalars | Accepted | Accepted |
| Unconnected output arrays (PIPO in dataflow) | Accepted | Accepted |
| Unconnected output streams | Accepted | **Error** |
| Unconnected output streamed arrays | Accepted | **Error** |

---

## Global Variables on the Interface

| Feature | Vivado HLS | Vitis HLS |
|---|---|---|
| Global variables in code | Supported (synthesizable) | Supported (synthesizable) |
| Global variables as top-level interface ports | Supported (exported) | **Not supported** |

Variables needed on the RTL interface must be **explicitly declared as top-level function arguments** in Vitis HLS.

---

## Module Naming Changes

### Auto-Prefix Behavior

| Scenario | Vivado HLS | Vitis HLS (2020.1+) |
|---|---|---|
| `config_rtl -module_auto_prefix true` | Top module: `top_top.v`; subs: `top_submodule1.v` | Top module: `top.v`; subs: `top_submodule1.v` |
| `-module_prefix` option | Prefix applied to all modules including top | Unchanged — prefix applied to all modules including top |

> `-module_prefix` takes precedence over `-module_auto_prefix`.

### Memory Module and RTL File Names

Memory modules were renamed to include explicit memory type and configuration:

| Old Name | New Name |
|---|---|
| `ncp_encoder_func_parbits_memcore_ram` | `ncp_encoder_func_parbits_RAM_1P_LUTRAM_1R1W` |
| `test_A_V_ROM` | `test_A_V_ROM_1P_BRAM_1R`, `test_A_V_ROM_1P_BRAM_1.v` |

---

## Function Inlining Changes

| Aspect | Vivado HLS | Vitis HLS |
|---|---|---|
| Automatic inlining trigger | Size of function | Cost model / user pragma preference |
| Small functions in pipelined loops | Often auto-inlined | Only inlined if tool determines II=1 benefit |

> **Impact:** Vitis HLS may achieve different QoR than Vivado HLS for designs with small helper functions called inside pipelined loops. Manually inline sub-functions (`#pragma HLS INLINE`) to reproduce prior behavior.

---

## Dataflow: std::complex Support

In Vivado HLS, `std::complex` could not be used directly as a DATAFLOW channel variable because the class constructor caused multiple-writer issues.

Vitis HLS supports `std::complex` in DATAFLOW via the **`no_ctor` attribute**:

```cpp
void proc_1(std::complex<float> (&buffer)[50], const std::complex<float> *in);
void proc_2(hls::stream<std::complex<float>> &fifo,
            const std::complex<float> (&buffer)[50], std::complex<float> &acc);
void proc_3(std::complex<float> *out, hls::stream<std::complex<float>> &fifo,
            const std::complex<float> acc);

void top(std::complex<float> *out, const std::complex<float> *in) {
#pragma HLS DATAFLOW
    // Suppress constructor to avoid multiple-writer issue:
    std::complex<float> acc    __attribute__((no_ctor));
    std::complex<float> buffer[50] __attribute__((no_ctor));
    // hls::stream has no_ctor internally — no attribute needed:
    hls::stream<std::complex<float>, 5> fifo;

    proc_1(buffer, in);
    proc_2(fifo, buffer, acc);
    proc_3(out, fifo, acc);
}
```

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Review clock uncertainty change (12.5% → 27%) first | This is the most impactful default change for timing QoR |
| Check struct interface behavior after migration | Aggregation default changed: add `disaggregate` pragma if needed |
| Add `__VITIS_HLS__` guards around tool-specific code | Allows same source to compile in both Vivado HLS and Vitis HLS |
| Replace all `RESOURCE` pragmas with `BIND_OP`/`BIND_STORAGE` | `RESOURCE` is deprecated and will be removed |
| Manually inline small functions in tight loops if QoR regresses | Vitis HLS inlining is driven by cost model, not function size |
| Use `no_ctor` attribute for `std::complex` in DATAFLOW channels | Prevents multiple-writer false positive from class constructor |

---

### See Also

- [Chapter 33 — Migrating to Unified IDE](ch33_migration_unified_ide.md) — Classic-to-Unified IDE migration
- [Chapter 35 — Deprecated Features](ch35_deprecated_unsupported.md) — Deprecated libraries, pragmas, and Tcl commands
- [Appendix A — Tcl to Config File Map](../appendices/appendix_a_tcl_config_map.md) — Tcl → config-file mapping

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 34, pages 875–881*
