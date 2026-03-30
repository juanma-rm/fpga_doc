# Chapter 2: Understanding Use Models

## Overview

This chapter helps guide users through the key decisions about how to interact with the AMD Vivado Design Suite. It covers the Vivado IDE, Tcl-based workflows, the distinction between Project Mode and Non-Project Mode, third-party tool integration, and PCB designer interfacing.

---

## Table of Contents

| Section | Description |
|---|---|
| [Vivado Design Suite Use Models](#vivado-design-suite-use-models) | Overview of key decisions for selecting a use model |
| [Working with the Vivado IDE](#working-with-the-vivado-integrated-design-environment-ide) | Launching and using the graphical interface |
| [Working with Tcl](#working-with-tcl) | Tcl shell, batch scripts, and AMD Vivado Store |
| [Understanding Project Mode and Non-Project Mode](#understanding-project-mode-and-non-project-mode) | Key differences, features, and command comparisons |
| [Using Third-Party Design Software Tools](#using-third-party-design-software-tools) | Third-party synthesis and simulation |
| [Interfacing with PCB Designers](#interfacing-with-pcb-designers) | I/O planning and PCB data exchange |

---

## Vivado Design Suite Use Models

Before starting your first design, review the *Vivado Design Suite User Guide: Getting Started (UG910)*.

Key decisions to make when choosing a use model:

| Decision | Options |
|---|---|
| **Interaction style** | GUI (Vivado IDE) or Script/Command-based (Tcl) |
| **Design management** | Project Mode (automatic) or Non-Project Mode (manual) |
| **IP management** | IP contained within a single project or remote IP repository |
| **Source control** | Managed through a revision control system or not |
| **Third-party tools** | Using external synthesis or simulation tools |

### See Also
- [Working with the Vivado IDE](#working-with-the-vivado-integrated-design-environment-ide)
- [Working with Tcl](#working-with-tcl)
- [Understanding Project Mode and Non-Project Mode](#understanding-project-mode-and-non-project-mode)
- [Chapter 5: Source Management](chapter5_source_management_and_revision_control.md)

---

## Working with the Vivado Integrated Design Environment (IDE)

The Vivado IDE provides an interface to assemble, implement, and validate your design and IP. It supports both Project Mode and Non-Project Mode.

### Key Features

- **Flow Navigator** — Push-button design flow (Project Mode only)
- **Design visualization** — Schematic, device, and package views with cross-probing
- **Design checkpoints** — Save and restore design state at any point
- **Interactive analysis** — Open designs after elaboration, synthesis, or implementation

### Launching the Vivado IDE

#### On Windows

```
Start → All Programs → Xilinx Design Tools → Vivado <version> → Vivado <version>
```

> **Tip:** Right-click the Vivado IDE shortcut icon and select **Properties** to update the **Start In** field. This controls where log and journal files are written.

#### From the Command Line (Windows or Linux)

```bash
vivado
```

This automatically runs `vivado -mode gui`. Use `vivado -help` for options.

> **Tip:** Run `settings64.bat` (Windows) or `settings64.sh` (Linux) from `<install_path>/Vivado/<version>` to add the Vivado tools to your PATH.

> **Recommended:** Launch Vivado from your project directory so log and journal files are written there.

#### From the Vivado Tcl Shell

```tcl
start_gui
```

### See Also
- *Vivado Design Suite User Guide: Using the Vivado IDE (UG893)*

---

## Working with Tcl

All supported design flows can be run using Tcl commands — either individual commands or saved scripts.

### Tcl Interaction Methods

| Method | Description |
|---|---|
| **Vivado Tcl Shell** | Standalone command-line interface |
| **Tcl Console** | Integrated within the Vivado IDE |
| **Batch scripts** | Run complete flows non-interactively |

### Launching the Vivado Tcl Shell

```bash
vivado -mode tcl
```

On Windows, you can also use: `Start → All Programs → Xilinx Design Tools → Vivado <version> → Vivado <version> Tcl Shell`

### Launching in Batch Mode

```bash
vivado -mode batch -source <your_Tcl_script>
```

> ⚠️ In batch mode, the Vivado tools **exit after running** the specified script.

### Using the Vivado IDE with a Tcl Flow

When working with Tcl, you can still use the Vivado IDE for interactive analysis and constraint definition:

- Open designs at any stage using `start_gui`
- Save design databases as checkpoint files
- Open checkpoints later for analysis

### AMD Vivado Store

The AMD Vivado Store enables downloading from AMD's public GitHub repositories:

| Store | Content |
|---|---|
| **Tcl Store** | Open source Tcl scripts and utilities for FPGA designs |
| **Board Store** | Board files defining external connectivity for Vivado |
| **CED Store** | Example designs demonstrating specific functionality |

> Download paths for boards and example designs can be configured in **Tools → Settings**.

### AMD Tcl Apps

The Tcl Store repository provides scripts and utilities from multiple sources. You can install existing scripts and contribute your own.

### Board Files

Board files define external connectivity for Vivado. When you select a **board** (vs a part) during project creation, board interfaces become available in IP Integrator via the **Boards** tab.

### Example Designs

Example designs are hosted on GitHub and updated asynchronously to the Vivado release. They are accessed through the **New Project Wizard** when installed via the AMD Vivado Store.

### See Also
- *Vivado Design Suite User Guide: Using Tcl Scripting (UG894)*
- *Vivado Design Suite Tcl Command Reference Guide (UG835)*
- *Vivado Design Suite Tutorial: Design Flows Overview (UG888)*

---

## Understanding Project Mode and Non-Project Mode

The Vivado Design Suite has two primary use models. Both can be used through the Vivado IDE or Tcl commands/batch scripts.

### Project Mode

The Vivado Design Suite manages the entire design process automatically:

- **Directory structure** on disk for source file management
- **Dependency tracking** — out-of-date detection when sources change
- **Automatic report generation** after runs complete
- **Run management** — multiple synthesis/implementation runs
- **Flow Navigator** — push-button GUI workflow

> **Key advantage:** The Vivado Design Suite manages the entire design process, including dependency management, report generation, and data storage.

> ⚠️ Certain operating systems (e.g., Windows) restrict path lengths to 256 characters. Create projects closer to the drive root to keep paths short.

Automated behaviors:
- Modified HDL after synthesis → prompted for re-synthesis
- Modified constraints → prompted for re-synthesis, re-implementation, or both
- Completed routing → automatic timing, DRC, methodology, and power reports
- Entire flow → single click in the Vivado IDE

### Non-Project Mode

An in-memory compilation flow where you manage everything manually:

- Sources read from their current locations (e.g., revision control system)
- Each design step launched individually via Tcl commands
- Design checkpoints and reports generated manually
- Design retained in memory; discarded after each session unless saved

> **Key advantage:** Full control over each step of the flow.

Manual responsibilities:
- Modified HDL after synthesis → must manually rerun synthesis
- Timing report after routing → must explicitly generate it
- Design parameters → set using Tcl commands
- Results → save using `write_checkpoint` and `report_*` commands

### Feature Comparison

| Flow Element | Project Mode | Non-Project Mode |
|---|---|---|
| Design Source File Management | Automatic | Manual |
| Flow Navigation | Guided (Flow Navigator) | Manual (Tcl commands) |
| Flow Customization | Unlimited with Tcl | Unlimited with Tcl |
| Reporting | Automatic | Manual |
| Analysis Stages | Designs and design checkpoints | Designs and design checkpoints |

### Automated Features (Project Mode Only)

- Out-of-the-box design flow
- Push-button interface
- Source file management and status
- Automatically generated standard reports
- Storage and reuse of tool settings
- Multiple synthesis/implementation runs
- Run results management and status

### Command Differences

Tcl commands differ between modes. **Do not mix mode-specific commands.**

| Task | Project Mode | Non-Project Mode |
|---|---|---|
| Add sources | `add_files`, `import_files` | `read_verilog`, `read_vhdl`, `read_xdc`, `read_*` |
| Run synthesis | `launch_runs synth_1` | `synth_design` |
| Run implementation | `launch_runs impl_1` | `opt_design`, `place_design`, `route_design` |
| Wait for completion | `wait_on_run` | N/A (sequential) |
| Open results | `open_run` | `start_gui` / `open_checkpoint` |

**Visual comparison of Tcl scripts:**

**Project Mode:**
```tcl
create_project …
add_files …
import_files …
launch_runs synth_1
wait_on_run synth_1
open_run synth_1
report_timing_summary
launch_runs impl_1
wait_on_run impl_1
open_run impl_1
report_timing_summary
launch_runs impl_1 -to_step write_bitstream
wait_on_run impl_1
```

**Non-Project Mode:**
```tcl
read_verilog …
read_vhdl …
read_ip …
read_xdc …
read_edif …
synth_design …
report_timing_summary
write_checkpoint
opt_design
write_checkpoint
place_design
write_checkpoint
route_design
report_timing_summary
write_checkpoint
write_bitstream
```

> **Tip:** GUI operations result in Tcl commands captured in the `vivado.jou` journal file. Use this file to develop scripts for either mode.

### See Also
- [Chapter 3: Using Project Mode](chapter3_using_project_mode.md)
- [Chapter 4: Using Non-Project Mode](chapter4_using_non-project_mode.md)

---

## Using Third-Party Design Software Tools

### Logic Synthesis

Third-party FPGA synthesis tools from Synopsys and Mentor Graphics are supported:

- Import synthesized netlists in **structural Verilog** or **EDIF** format
- Use SDC or XDC constraints output by synthesis tools

> ⚠️ **All AMD IP and Block Designs must use Vivado Synthesis.** Third-party synthesis for AMD IP or IP Integrator block designs is not supported (with limited exceptions for 7 series memory IP).

### Logic Simulation

Third-party simulators from **Mentor Graphics**, **Cadence**, **Aldec**, and **Synopsys** are supported:

- Integrated and can be launched directly from the Vivado IDE
- Export Verilog or VHDL netlists at any stage of the design flow
- Export structural netlists with post-implementation delays in **SDF** format
- Generate simulation scripts using `export_simulation` for enterprise users

> ⚠️ Some AMD IP provides RTL sources in only Verilog or VHDL format. After synthesis, structural netlists can be created in either language.

---

## Interfacing with PCB Designers

The I/O planning process is critical for high-performing systems. The Vivado IDE enables visualization of the relationship between physical package pins and internal die pads.

### Data Exchange Methods

| Method | Format | Use Case |
|---|---|---|
| **CSV Spreadsheet** | `.csv` | I/O pin configuration, matched length connections, power connections |
| **RTL Header** | HDL | Pin definitions |
| **XDC File** | `.xdc` | Constraint-based pin assignment |
| **IBIS Model** | `.ibs` | Signal integrity analysis on the PCB |

### Key Concerns for PCB Designers

- Relationship and orientation of the FPGA on the PCB
- BGA device routing challenges
- Critical interface routing
- Power rail locations
- Signal integrity

### See Also
- *Vivado Design Suite User Guide: I/O and Clock Planning (UG899)*

---

## Best Practices

1. **Start with Project Mode** if new to Vivado — it provides the easiest on-ramp with automated management
2. **Use Non-Project Mode** for full control in batch/CI environments with existing revision control workflows
3. **Don't mix mode-specific Tcl commands** — Project Mode and Non-Project Mode commands are not interchangeable
4. **Launch Vivado from your project directory** so log and journal files are co-located
5. **Use the `vivado.jou` journal file** to develop Tcl scripts from GUI interactions
6. **Leverage the AMD Vivado Store** for Tcl utilities, board files, and example designs
7. **Collaborate early with PCB designers** using CSV, IBIS, and XDC exports for I/O planning
8. **Always use Vivado Synthesis for AMD IP** — third-party synthesis is not supported for IP catalog cores

---

## Quick Reference

| Use Model | Best For | Interface | Source Management | Reports |
|---|---|---|---|---|
| Project Mode + GUI | New users, interactive design | Vivado IDE + Flow Navigator | Automatic | Automatic |
| Project Mode + Tcl | Scripted Project flows | Tcl Console / Shell | Automatic | Automatic |
| Non-Project Mode | Batch processing, CI/CD | Tcl Shell / Scripts | Manual | Manual |

---

## Source Attribution

- **Source:** *Vivado Design Suite User Guide: Design Flows Overview (UG892)*, v2025.2, November 20, 2025
- **Chapter:** Chapter 2 — Understanding Use Models (Pages 16–27)
- **Publisher:** Advanced Micro Devices, Inc.
