# Chapter 15 — vitis, v++, and vitis-run Commands
**Section IV: Vitis HLS Command Reference · UG1399 v2025.2, Pages 454–456**

---

## Table of Contents
1. [vitis Command](#1-vitis-command)
2. [v++ Command](#2-v-command)
3. [vitis-run Command](#3-vitis-run-command)
4. [hls_init.tcl Initialization Script](#4-hls_inittcl-initialization-script)

---

## 1. vitis Command

Launches the Vitis Unified IDE. Basic usage:

```bash
vitis -w <workspace>
```

### Supported Modes

| Flag | Mode | Description |
|---|---|---|
| *(none)* | Default | Launches Vitis IDE (GUI) |
| `-g` | GUI | Same as default |
| `-a` / `--analyze` | Analysis | Opens summary file, folder, or waveform file in Analysis view |
| `-w` / `--workspace` | Workspace | Launches IDE with a specified workspace directory |
| `-i` / `--interactive` | Interactive | Launches Vitis Python interactive shell |
| `-s` / `--source` | Script | Runs a specified Python script |
| `-j` / `--jupyter` | Jupyter | Launches Vitis Jupyter Web UI |
| `-h` / `--help` | Help | Displays help message and mode list |
| `-v` / `--version` | Version | Displays the Vitis version |

```bash
vitis -h
# Syntax: vitis [-g (default) | -a | -w | -i | -s | -h | -v]
```

> **Note:** The Vitis Unified IDE internally calls either `v++ -c --mode hls` (for synthesis) or `vitis-run --mode hls` (for C Simulation, co-simulation, Package, and Implementation steps).

---

## 2. v++ Command

Used to **synthesize** the HLS component, targeting either:
- **Vitis kernel** flow (`.xo` output)
- **Vivado IP** flow (`.zip` output)

Also compiles the HLS component for **software emulation** in Vitis System Projects.

### Syntax

```bash
v++ -c --mode hls [OPTIONS] <input_file...>
```

### Options

| Flag | Description |
|---|---|
| `-c` / `--compile` | Run compile flow (required) |
| `-m hls` / `--mode hls` | Select HLS mode (required with `-c`) |
| `-h` / `--help` | Display help |
| `-v` / `--version` | Display version |
| `--config <file>` | Specify a configuration file containing HLS options |
| `--work_dir <dir>` | Specify working directory for output files |
| `-f` / `--platform` | Path to platform spec (`.xpfm`) or hardware spec (`.xsa`) |
| `--freqhz <val>` | Specify PL clock frequency in Hz or MHz |
| `--part <val>` | Specify target device part |
| `--hls.*` | Pass HLS-section options from the config file |

### Configuration File Usage

HLS options belong under the `[hls]` section of a config file:

```ini
part=xcvu11p-flga2577-1-e

[hls]
clock=8
flow_target=vitis
syn.file=../../src/dct.cpp
syn.top=dct
tb.file=../../src/dct_test.cpp
syn.output.format=xo
clock_uncertainty=15%
```

Invoke with:
```bash
v++ -c --mode hls --config hls_config.cfg
```

> See Chapter 16 for the complete reference of all `[hls]` config file options.

---

## 3. vitis-run Command

Used to **run process steps** (other than synthesis) on the HLS component:
- `--csim`: C Simulation
- `--cosim`: C/RTL Co-Simulation
- `--package`: Package / export
- `--impl`: Vivado out-of-context implementation

### Syntax

```bash
vitis-run --mode hls [OPTIONS] [<input_file>]
```

### Options

| Flag | Description |
|---|---|
| `-h` / `--help` | Display help message |
| `-v` / `--version` | Display version info |
| `--config <file>` | Config file specifying HLS options |
| `--csim` | Run C simulation |
| `--cosim` | Run C/RTL co-simulation |
| `--impl` | Run Vivado out-of-context implementation |
| `--package` | Export/package the HLS component |
| `--input_file <file>` | Specify input Tcl file (can also be positional) |
| `--itcl` | Launch interactive HLS Tcl shell |
| `--tcl` | Evaluate an HLS Tcl file |
| `--work_dir <dir>` | Specify working directory for output files |
| `-f` / `--platform` | Path to platform spec |
| `--freqhz <val>` | Clock frequency (Hz or MHz) |
| `--part <val>` | Target device part |

### Example Workflow

```bash
# Synthesize
v++ -c --mode hls --config hls.cfg --work_dir ./output

# Run C simulation
vitis-run --mode hls --csim --config hls.cfg --work_dir ./output

# Run co-simulation
vitis-run --mode hls --cosim --config hls.cfg --work_dir ./output

# Package as .xo
vitis-run --mode hls --package --config hls.cfg --work_dir ./output
```

---

## 4. hls_init.tcl Initialization Script

When Vitis HLS starts, it looks for an optional Tcl initialization script to configure the tool before opening a project.

### Search Locations

| Platform | Path |
|---|---|
| **Windows** | `%APPDATA%\Xilinx\HLS_init.tcl` |
| **Linux** | `$HOME/.Xilinx/HLS_init.tcl` |

> **Important:** There is no default `HLS_init.tcl` in the software installation. You must **create one** if needed. Any valid `vitis-run` Tcl commands can be placed in this file.

---

## Best Practices

| Practice | Rationale |
|---|---|
| **Use `--config` for all HLS options** | Keeps CLI clean; config file is version-controllable |
| **Use `--freqhz` with `platform=`** | Required when using a platform file instead of `part=` |
| **Run `vitis-run --csim` before synthesis** | Validates C logic before generating RTL |
| **Use `--work_dir` to isolate outputs** | Keeps build artifacts separate from source |
| **Use `vitis -i` for interactive debugging** | Python shell supports all Vitis commands interactively |

---

### See Also

- [Chapter 14 — HLS Command Line](../section03_vitis_hls_flow_steps/ch14_hls_command_line.md) — `v++` invocation and scripting
- [Chapter 16 — Config File Commands](ch16_config_file_commands.md) — Config-file directives for `vitis-run`
- [Chapter 18 — HLS Tcl Commands](ch18_hls_tcl_commands.md) — Legacy Tcl command interface

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Section IV, Chapter 15, Pages 454–456*
