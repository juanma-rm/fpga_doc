# Chapter 14: Creating HLS Components from the Command Line

> Source: UG1399 (v2025.2) January 22, 2026 — Vitis HLS User Guide, Section III: Vitis HLS Flow Steps, pages 449–452.

---

## Table of Contents

1. [Overview](#overview)
2. [Running C Synthesis](#running-c-synthesis)
3. [Running C Simulation or Code Analyzer](#running-c-simulation-or-code-analyzer)
4. [Running C/RTL Co-Simulation](#running-crtl-co-simulation)
5. [Running Implementation](#running-implementation)
6. [Exporting the IP/XO](#exporting-the-ipxo)
7. [Quick Reference — Command Summary](#quick-reference--command-summary)

---

## Overview

All Vitis HLS flow steps available in the Vitis Unified IDE are equally accessible from the command line. The two command-line tools are:

| Command | Purpose |
|---|---|
| `v++ -c --mode hls` | Build (synthesize) an HLS component |
| `vitis-run --mode hls` | Run C simulation, Code Analyzer, C/RTL co-simulation, implementation, and export |

Both commands accept a **configuration file** (`hls_config.cfg`) that specifies all design settings, source files, test bench files, pragmas, and directives.

> **Tip:** Examples in this chapter are based on the DCT design from *Getting Started With Vitis HLS*.

### Workspace and Work Directory

```bash
v++ -c --mode hls --config ./dct/hls_config.cfg --work_dir dct
```

| Option | Description |
|---|---|
| `--config` | Path to the HLS configuration file |
| `--work_dir` | HLS component folder (the **parent** of this directory becomes the workspace for the Vitis IDE) |

---

## Running C Synthesis

```bash
v++ -c --mode hls --config ./dct/hls_config.cfg --work_dir dct
```

### Minimum Config File for Synthesis

```ini
part=xczu9eg-ffvb1156-2-e     # Required: target device
[hls]
syn.file=./src/dct.cpp         # Required: source file(s)
syn.top=dct                    # Required: top-level function name
flow_target=vitis              # Optional: override default (vivado)
clock=8ns                      # Optional: override default (10ns)
clock_uncertainty=12%          # Optional: override default (27%)
syn.output.format=rtl          # Optional: skip packaging during iterations
syn.directive.pipeline=dct_2d II=4  # Optional: optimization directive
```

**Required fields:** `part` (or `platform`), `syn.file`, `syn.top`

> **Important:** If using `platform=` instead of `part=`, replace `clock=` with `freqhz=` to override the platform's default clock frequency.

---

## Running C Simulation or Code Analyzer

C simulation does **not** require C synthesis to have been run first.

```bash
vitis-run --mode hls --csim --config ./dct/hls_config.cfg --work_dir dct
```

### Config File for C Simulation

```ini
part=xczu9eg-ffvb1156-2-e
[hls]
clock=8ns
clock_uncertainty=12%
flow_target=vitis
syn.output.format=rtl
syn.file=./src/dct.cpp          # Design source
syn.file=./src/dct.h
syn.top=dct
tb.file=./src/dct_coeff_table.txt   # Test bench data files
tb.file=./src/dct_test.cpp          # Test bench source
tb.file=./src/in.dat
tb.file=./src/out.golden.dat
csim.clean=true
csim.code_analyzer=false        # Set to true to enable Code Analyzer
syn.directive.pipeline=dct_2d II=4
```

> **Tip:** Set `csim.code_analyzer=true` to run Code Analyzer alongside C simulation.

---

## Running C/RTL Co-Simulation

Requires C synthesis to have been run first.

```bash
vitis-run --mode hls --cosim --config ./dct/hls_config.cfg --work_dir dct
```

### Config File for C/RTL Co-Simulation

```ini
part=xczu9eg-ffvb1156-2-e
[hls]
clock=8ns
clock_uncertainty=12%
flow_target=vitis
syn.output.format=rtl
syn.file=./src/dct.cpp
syn.file=./src/dct.h
syn.top=dct
tb.file=./src/dct_coeff_table.txt
tb.file=./src/dct_test.cpp
tb.file=./src/in.dat
tb.file=./src/out.golden.dat
syn.directive.pipeline=dct_2d II=4
cosim.enable_dataflow_profiling=true
cosim.enable_fifo_sizing=true
cosim.trace_level=port         # none | port | port_hier | all
cosim.wave_debug=true          # Launch Vivado GUI (xsim only)
```

> See *Co-Simulation Configuration* (Chapter 16) for a complete list of `cosim.*` settings.

---

## Running Implementation

```bash
vitis-run --mode hls --impl --config ./dct/hls_config.cfg --work_dir dct
```

The config file used is the same as for synthesis; the `vivado.*` configuration entries control Vivado synthesis and place & route. Refer to *Running Implementation* in Chapter 13 for available `vivado.*` options.

---

## Exporting the IP/XO

```bash
vitis-run --mode hls --package --config ./dct/hls_config.cfg --work_dir dct
```

Exports a Vivado IP or Vitis kernel from the **previously synthesized** HLS component.

### Config File for Export

```ini
part=xcvu9p-flga2104-2-i
[hls]
syn.file=/path/to/src/dct.cpp
syn.top=dct
syn.output.format=xo          # xo = Vitis kernel; ip_catalog = Vivado IP
```

> **Note:** You can export a Vitis kernel as an IP. However, you **cannot** export a Vivado flow IP as an XO unless it meets the specific Vitis kernel interface requirements.

---

## Quick Reference — Command Summary

| Step | Command |
|---|---|
| C Synthesis | `v++ -c --mode hls --config <cfg> --work_dir <dir>` |
| C Simulation | `vitis-run --mode hls --csim --config <cfg> --work_dir <dir>` |
| Code Analyzer | Same as C Simulation with `csim.code_analyzer=true` in config |
| C/RTL Co-Simulation | `vitis-run --mode hls --cosim --config <cfg> --work_dir <dir>` |
| Implementation | `vitis-run --mode hls --impl --config <cfg> --work_dir <dir>` |
| Export IP/XO | `vitis-run --mode hls --package --config <cfg> --work_dir <dir>` |

---

## Best Practices

| Practice | Rationale |
|---|---|
| **Keep one config file per HLS component** | Consolidates all settings (sources, part, clock, pragmas) in a single, version-controllable file |
| **Run C Simulation before C Synthesis** | Validates functional correctness at C level; fixing bugs after synthesis is far more expensive |
| **Use `--work_dir` consistently** | All downstream steps (cosim, package, impl) rely on artifacts in the work directory |
| **Set `cosim.trace_level=port` for debugging** | Generates waveforms viewable in Vivado for I/O-level debugging without excessive file sizes |
| **Use `syn.output.format=xo` for Vitis flow, `ip_catalog` for Vivado IP flow** | Mismatched output format causes integration failures downstream |
| **Automate builds with shell scripts** | Chain `v++` and `vitis-run` calls in a script for reproducible, CI-friendly builds |

---

### See Also

- [Chapter 13 — Building and Running an HLS Component](ch13_building_hls_component.md) — IDE-based equivalent of command-line operations
- [Chapter 15 — Vitis Commands](../section04_vitis_hls_command_reference/ch15_vitis_commands.md) — `vitis`, `v++`, `vitis-run` detailed reference
- [Chapter 16 — HLS Config File Commands](../section04_vitis_hls_command_reference/ch16_config_file_commands.md) — All `syn.*`, `cosim.*`, `vivado.*` settings

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 14: Creating HLS Components from the Command Line, Pages 449–452.*

### Minimum Config File Fields by Step

| Step | Required Config Fields |
|---|---|
| **Synthesis** | `part=`, `syn.file=`, `syn.top=` |
| **C Simulation** | All synthesis fields + `tb.file=` (source + data files) |
| **Co-Simulation** | All C simulation fields |
| **Implementation** | All synthesis fields |
| **Export** | `part=`, `syn.file=`, `syn.top=`, `syn.output.format=` |

### Opening Result in Vitis IDE

After running any command-line step, the parent of `--work_dir` can be used as a workspace:

```bash
vitis -w <parent_of_work_dir>
```

The HLS component built from the command line appears in the Vitis Unified IDE Component Explorer, and all synthesis/simulation reports are accessible through the Flow Navigator.
