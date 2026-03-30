# Chapter 4: Using Non-Project Mode

## Overview

This chapter details the Non-Project Mode of the AMD Vivado Design Suite — an in-memory compilation flow where you manage sources and the design process yourself using Tcl commands. Non-Project Mode provides full control over each design step, but requires manual management of source files, reports, and design checkpoints.

---

## Table of Contents

| Section | Description |
|---|---|
| [Non-Project Mode Advantages](#non-project-mode-advantages) | Key benefits of the compile-style flow |
| [Reading Design Sources](#reading-design-sources) | Using `read_*` commands to load sources |
| [Working with IP and IP Subsystems](#working-with-ip-and-ip-subsystems) | IP in Non-Project Mode |
| [Running Logic Simulation](#running-logic-simulation) | Simulation capabilities |
| [Running Logic Synthesis and Implementation](#running-logic-synthesis-and-implementation) | Step-by-step compilation flow |
| [Generating Reports](#generating-reports) | Manual report generation |
| [Using Design Checkpoints](#using-design-checkpoints) | Saving and restoring design state |
| [Performing Design Analysis Using the Vivado IDE](#performing-design-analysis-using-the-vivado-ide) | Interactive analysis in Non-Project Mode |
| [Non-Project Mode Tcl Commands](#using-non-project-mode-tcl-commands) | Command reference and script example |

---

## Non-Project Mode Advantages

Non-Project Mode provides a **compile-style design flow** with full control:

- Manage HDL source files, constraints, and IP yourself
- Manage dependencies manually
- Generate and store synthesis/implementation results as needed
- Full Tcl command suite for creating, configuring, implementing, analyzing, and managing designs

> **Key advantage:** Full control over each step of the flow.

### Features Not Available in Non-Project Mode

| Feature | Status |
|---|---|
| Flow Navigator | ❌ Not available |
| Project Summary | ❌ Not available |
| Vivado IP Catalog (GUI) | ❌ Not available |
| Source file management | ❌ Manual |
| Runs infrastructure | ❌ Not available |
| Design state reporting | ❌ Manual |
| Automatic reports | ❌ Manual |
| Run strategies | ❌ Not available (use command options directly) |

> In Non-Project Mode, an **in-memory project** is created internally for the Vivado tools but is **not preserved** to disk.

---

## Reading Design Sources

Each source file type has a corresponding `read_*` Tcl command:

| Command | Source Type |
|---|---|
| `read_verilog` | Verilog (`.v`) and SystemVerilog (`.sv`) files |
| `read_vhdl` | VHDL (`.vhd`, `.vhdl`) files |
| `read_ip` | IP files (`.xci` or `.xco`) |
| `read_bd` | IP Integrator block designs (`.bd`) |
| `read_xdc` | Constraint files (`.xdc`, `.sdc`) |
| `read_edif` | EDIF or NGC netlist files |
| `read_checkpoint` | Design checkpoint (`.dcp`) files |

> ⚠️ Do **not** use `add_files` or `import_files` in Non-Project Mode — there is no project structure to add files into.

Sources must be **read each time** the Tcl script or interactive flow is started. Sources are read from their current locations (e.g., revision control system).

### Managing Source Files

- Read files in a specific order for proper compilation
- Sources can be located on any network-accessible location
- Read-only sources are processed accordingly

### Working with a Revision Control System

Non-Project Mode works naturally with revision control:

1. Check out source files into a local directory
2. Read sources using `read_*` commands
3. Sources remain in their original locations during design
4. Check files back into source control as needed
5. Optionally check in design checkpoints, reports, and bitstreams

> See [Chapter 5: Source Management](chapter05_source_management_and_revision_control.md) for detailed recommendations.

### Using Third-Party Synthesized Netlists

Import Verilog or EDIF netlists from third-party synthesis tools. These can be used standalone or mixed with RTL files.

---

## Working with IP and IP Subsystems

In Non-Project Mode, **output products must be generated** for IP or block designs prior to top-level synthesis.

### Methods for Adding IP

| Method | Behavior |
|---|---|
| **IP from Vivado IP catalog** (`.xci` / `.xcix`) | If OOC DCP exists in the IP directory, it is used for implementation (black box for synthesis). If no DCP, RTL and constraints are used for global synthesis. |
| **Tcl commands** | Configure and generate IP with each run, ensuring consistency |

> **Important:** Always use the **XCI file**, not the DCP file, when adding IP. This ensures output products are used consistently. If the IP has an associated DCP, it is automatically used and the IP is not re-synthesized.

---

## Running Logic Simulation

The **Vivado simulator** supports:

- Behavioral and structural simulation
- Full timing simulation of implemented designs
- Mixed-mode Verilog/VHDL
- Analog waveform display

Third-party simulators (Mentor Graphics ModelSim, Questa, Cadence, Synopsys, Aldec) can also be used:

- Write Verilog/VHDL netlists and SDF files from the open design
- Launch ModelSim and Questa directly from the Vivado IDE

---

## Running Logic Synthesis and Implementation

In Non-Project Mode, each step is launched with an individual Tcl command. Steps must run in order:

### Implementation Flow

```tcl
# 1. Read sources
read_vhdl -library bftLib [ glob ./Sources/hdl/bftLib/*.vhdl ]
read_vhdl ./Sources/hdl/bft.vhdl
read_verilog [ glob ./Sources/hdl/*.v ]
read_xdc ./Sources/bft_full_kintex7.xdc

# 2. Synthesize
synth_design -top bft -part xc7k70tfbg484-2
write_checkpoint -force $outputDir/post_synth

# 3. Optimize
opt_design

# 4. Place
place_design

# 5. Physical optimization (optional)
phys_opt_design

# 6. Route
route_design

# 7. Generate bitstream
write_bitstream -force $outputDir/bft.bit
```

### Optional Steps

| Command | Description |
|---|---|
| `power_opt_design` | Intelligent clock gating to reduce power (optional) |
| `phys_opt_design` | Physical logic optimization for timing or routability (optional) |

> **Tip:** After each design step, launch the Vivado IDE (`start_gui`) for interactive analysis and constraint definition on the active design.

> ⚠️ Design checkpoints are intended as **snapshots for analysis**, not as starting points to continue the design process (except for bitstream generation).

---

## Generating Reports

Reports must be generated **manually** using Tcl commands. Only `vivado.log` and `vivado.jou` are created automatically.

### Common Report Commands

| Command | Description |
|---|---|
| `report_timing_summary` | Comprehensive timing summary |
| `report_timing` | Detailed timing paths |
| `report_power` | Power estimates |
| `report_utilization` | Resource utilization |
| `report_clock_utilization` | Clock resource usage |
| `report_drc` | Design rule checks |
| `report_design_analysis` | Critical path and complexity analysis |

### Example: Generating Reports at Each Stage

```tcl
# Post-synthesis reports
report_timing_summary -file $outputDir/post_synth_timing_summary.rpt
report_power -file $outputDir/post_synth_power.rpt

# Post-placement reports
report_timing_summary -file $outputDir/post_place_timing_summary.rpt

# Post-route reports
report_timing_summary -file $outputDir/post_route_timing_summary.rpt
report_timing -sort_by group -max_paths 100 -path_type summary \
  -file $outputDir/post_route_timing.rpt
report_clock_utilization -file $outputDir/clock_util.rpt
report_utilization -file $outputDir/post_route_util.rpt
report_power -file $outputDir/post_route_power.rpt
report_drc -file $outputDir/post_imp_drc.rpt
```

---

## Using Design Checkpoints

Design checkpoints (DCPs) capture the current design state — netlist, constraints, and implementation results.

### Capabilities

| Action | Description |
|---|---|
| **Save state** | `write_checkpoint <file>.dcp` after critical design steps |
| **Restore design** | `read_checkpoint <file>.dcp` to reload a saved state |
| **Open for analysis** | `open_checkpoint <file>.dcp` in the Vivado IDE |
| **Continue flow** | Run remaining design steps from a restored checkpoint |

### When to Write Checkpoints

Write checkpoints after each critical step:

```tcl
write_checkpoint -force $outputDir/post_synth.dcp
# ... opt_design ...
write_checkpoint -force $outputDir/post_opt.dcp
# ... place_design ...
write_checkpoint -force $outputDir/post_place.dcp
# ... route_design ...
write_checkpoint -force $outputDir/post_route.dcp
```

> ⚠️ You **cannot add new sources** to a design restored from a checkpoint.

---

## Performing Design Analysis Using the Vivado IDE

### Opening the Vivado IDE from the Active Design

```tcl
start_gui    # Opens the Vivado IDE with the active design in memory
stop_gui     # Closes the Vivado IDE and returns to the Tcl shell
```

> ⚠️ **Do not use `exit`** from the GUI in Non-Project Mode — this closes the Tcl shell and discards the in-memory design. Use `stop_gui` to preserve the active design.

### Available in Non-Project Mode IDE

- Design analysis and reporting features (Tools menu)
- Constraint modification and assignment
- Cross-probing to design objects and RTL source files
- Go To Instantiation / Go To Definition / Go To Source commands

### Not Available in Non-Project Mode IDE

- Flow Navigator
- Project Summary
- Source file access and management
- Synthesis/implementation run management

> **Important:** Any changes made in the Vivado IDE are made to the **active design in memory** and automatically applied to downstream tools.

### Saving Design Changes

**From the Active Design:**
- Changes are automatically passed to downstream tools for the session
- **File → Export → Export Constraints** to save constraint changes for future use
- Can write a new constraints file or override the original

**From Design Checkpoints:**
- **File → Checkpoint → Save** — saves changes to the current checkpoint
- **File → Checkpoint → Write** — saves to a new checkpoint

### Opening Design Checkpoints in the IDE

You can open saved checkpoints for analysis at any stage:

```tcl
open_checkpoint $outputDir/post_route.dcp
start_gui
```

Analysis capabilities include timing analysis, placement adjustment, and routing inspection — even for partially completed designs.

---

## Using Non-Project Mode Tcl Commands

### Basic Non-Project Mode Commands

| Command | Description |
|---|---|
| `read_edif` | Import EDIF or NGC netlist |
| `read_verilog` | Read Verilog (`.v`) and SystemVerilog (`.sv`) sources |
| `read_vhdl` | Read VHDL (`.vhd`, `.vhdl`) sources |
| `read_ip` | Read IP (`.xci` or `.xco`) — uses DCP if available, otherwise RTL |
| `read_checkpoint` | Load a design checkpoint |
| `read_xdc` | Read constraint files (`.sdc`, `.xdc`) |
| `read_bd` | Read IP Integrator block designs (`.bd`) |
| `set_param` / `set_property` | Define design configuration and tool settings |
| `link_design` | Compile netlist sources |
| `synth_design` | Launch synthesis (requires top module and target part) |
| `opt_design` | High-level design optimization |
| `power_opt_design` | Intelligent clock gating (optional) |
| `place_design` | Place the design |
| `phys_opt_design` | Physical logic optimization (optional) |
| `route_design` | Route the design |
| `report_*` | Generate reports (available at all stages) |
| `write_bitstream` | Generate bitstream and run DRCs |
| `write_checkpoint` | Save design state at any point |
| `write_verilog` | Export Verilog netlist |
| `write_xdc` | Export XDC constraints |
| `start_gui` / `stop_gui` | Open/close the Vivado IDE |

### Non-Project Mode Tcl Script Example

```tcl
# run_bft_kintex7_batch.tcl
# BFT sample design - RTL-to-bitstream non-project batch flow
#
# Usage: vivado -mode tcl -source run_bft_kintex7_batch.tcl

# STEP 0: Define output directory
set outputDir ./Tutorial_Created_Data/bft_output
file mkdir $outputDir

# STEP 1: Setup design sources and constraints
read_vhdl -library bftLib [ glob ./Sources/hdl/bftLib/*.vhdl ]
read_vhdl ./Sources/hdl/bft.vhdl
read_verilog [ glob ./Sources/hdl/*.v ]
read_xdc ./Sources/bft_full_kintex7.xdc

# STEP 2: Synthesis
synth_design -top bft -part xc7k70tfbg484-2
write_checkpoint -force $outputDir/post_synth
report_timing_summary -file $outputDir/post_synth_timing_summary.rpt
report_power -file $outputDir/post_synth_power.rpt

# STEP 3: Placement and optimization
opt_design
place_design
phys_opt_design
write_checkpoint -force $outputDir/post_place
report_timing_summary -file $outputDir/post_place_timing_summary.rpt

# STEP 4: Routing
route_design
write_checkpoint -force $outputDir/post_route
report_timing_summary -file $outputDir/post_route_timing_summary.rpt
report_timing -sort_by group -max_paths 100 -path_type summary \
  -file $outputDir/post_route_timing.rpt
report_clock_utilization -file $outputDir/clock_util.rpt
report_utilization -file $outputDir/post_route_util.rpt
report_power -file $outputDir/post_route_power.rpt
report_drc -file $outputDir/post_imp_drc.rpt
write_verilog -force $outputDir/bft_impl_netlist.v
write_xdc -no_fixed_only -force $outputDir/bft_impl.xdc

# STEP 5: Generate bitstream
write_bitstream -force $outputDir/bft.bit
```

---

## Best Practices

1. **Write design checkpoints after each critical step** — enables analysis, debugging, and fallback
2. **Generate reports at each stage** — timing, power, and utilization reports help identify issues early
3. **Use `stop_gui` instead of `exit`** to close the Vivado IDE without losing the in-memory design
4. **Always use XCI files** to reference IP — not DCP files directly
5. **Generate IP output products before synthesis** — required in Non-Project Mode
6. **Use `file mkdir`** at the start of scripts to ensure output directories exist
7. **Use `-force` with `write_checkpoint`** to overwrite previous checkpoints
8. **Add `report_drc` before `write_bitstream`** to catch design rule violations
9. **Structure scripts in numbered steps** for clarity and maintainability
10. **Export constraints** (`write_xdc`) to preserve changes made during interactive analysis

---

## Quick Reference

| Design Stage | Command | Checkpoint | Reports |
|---|---|---|---|
| Source Reading | `read_verilog`, `read_vhdl`, `read_xdc`, `read_ip` | — | — |
| Synthesis | `synth_design -top <top> -part <part>` | `write_checkpoint post_synth` | `report_timing_summary`, `report_power` |
| Optimization | `opt_design` | `write_checkpoint post_opt` | — |
| Power Opt | `power_opt_design` (optional) | — | — |
| Placement | `place_design` | `write_checkpoint post_place` | `report_timing_summary` |
| Physical Opt | `phys_opt_design` (optional) | — | — |
| Routing | `route_design` | `write_checkpoint post_route` | `report_timing_summary`, `report_utilization`, `report_power`, `report_drc` |
| Bitstream | `write_bitstream` | — | — |

---

## See Also

- [Chapter 2: Understanding Use Models](chapter02_understanding_use_models.md)
- [Chapter 3: Using Project Mode](chapter03_using_project_mode.md)
- [Chapter 5: Source Management and Revision Control](chapter05_source_management_and_revision_control.md)

---

## Source Attribution

- **Source:** *Vivado Design Suite User Guide: Design Flows Overview (UG892)*, v2025.2, November 20, 2025
- **Chapter:** Chapter 4 — Using Non-Project Mode (Pages 75–84)
- **Publisher:** Advanced Micro Devices, Inc.
