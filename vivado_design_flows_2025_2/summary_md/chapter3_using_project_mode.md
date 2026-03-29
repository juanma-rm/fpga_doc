# Chapter 3: Using Project Mode

## Overview

This chapter details how to use Project Mode in the AMD Vivado Design Suite. In Project Mode, Vivado automatically manages source files, constraints, IP data, synthesis and implementation runs, reports, and design state. The Flow Navigator provides a push-button design flow through the Vivado IDE.

---

## Table of Contents

| Section | Description |
|---|---|
| [Project Mode Advantages](#project-mode-advantages) | Key benefits of using Project Mode |
| [Creating Projects](#creating-projects) | Project types, source management, archiving |
| [Understanding the Flow Navigator](#understanding-the-flow-navigator) | GUI workflow control |
| [Performing System-Level Design Entry](#performing-system-level-design-entry) | Source management, RTL development, constraint development |
| [Working with IP](#working-with-ip) | IP catalog, output products, OOC flow, IP constraints |
| [Creating IP Subsystems with IP Integrator](#creating-ip-subsystems-with-ip-integrator) | Block designs, designer assistance, platform board flow |
| [Logic Simulation](#logic-simulation) | Simulation flow, libraries, third-party simulators |
| [Running Logic Synthesis and Implementation](#running-logic-synthesis-and-implementation) | Runs, strategies, incremental compile, ECOs |
| [Viewing Log Files, Messages, Reports, and Properties](#viewing-log-files-messages-reports-and-properties) | Log, message, and report management |
| [Opening Designs for Analysis](#opening-designs-to-perform-design-analysis-and-constraints-definition) | Elaborated, synthesized, implemented, and dataflow designs |
| [Device Programming, Debug](#device-programming-hardware-verification-and-debugging) | Bitstream generation, ILA, debug cores |
| [Project Mode Tcl Commands](#using-project-mode-tcl-commands) | Command reference and script examples |

---

## Project Mode Advantages

- Automatically manages project status, HDL sources, constraint files, IP cores, and block designs
- Generates and stores synthesis and implementation results
- Advanced design analysis with cross probing from implementation results to RTL source files
- Automates command options using **run strategies** and generates standard reports
- Supports creation of **multiple runs** to explore constraint or command options

> **Recommended:** Project Mode is the easiest way to get acquainted with the Vivado tools and AMD recommendations.

> ⚠️ Run strategies only apply to Project Mode. In Non-Project Mode, all directives and command options must be set manually.

---

## Creating Projects

### Project Types

| Project Type | Description |
|---|---|
| **RTL Project** | Add RTL sources and constraints, configure IP, synthesize, and implement |
| **Post-Synthesis Project** | Import third-party netlists, implement, and analyze |
| **I/O Planning Project** | Device exploration and early pin planning (no RTL required) |
| **Imported Project** | Import from ISE Design Suite, XST, or Synopsys Synplify |
| **Example Project** | Explore sample designs including Zynq 7000 SoC or MicroBlaze |
| **DFX** | Dynamic Function Exchange with partial bitstream reconfiguration |

The **Create Project wizard** guides you through:
1. Define project name and location
2. Select project type
3. Add sources (RTL, IP, block designs, XDC, simulation test benches, etc.)
4. Choose to reference sources in place or copy into the project directory
5. Select target part

> ⚠️ **Windows has a 260-character path length limit.** Use short names and directory locations when creating projects, IP, or block designs.

### Managing Source Files in Project Mode

- Sources can be **referenced remotely** or **copied locally** into the project
- Vivado tracks file **timestamps** to detect changes
- Modified sources trigger **out-of-date** status for synthesis/implementation runs
- Read-only sources are processed accordingly
- RTL files can be scanned for include files and global source files
- Compilation order and logic hierarchy are automatically derived in the **Sources** window

### Using Remote, Read-Only Sources

The Vivado Design Suite can use remote source files (including read-only files). Changes cannot be saved to read-only originals but can be saved to a different location.

### Archiving Projects

```
File → Project → Archive
```

Creates a ZIP file including source files, IP, design configuration, and optionally run results. Remote sources are copied locally into the archive.

### Creating a Tcl Script to Recreate the Project

```
File → Project → Write Tcl
```

Generates a Tcl script to recreate the entire project. This script can be checked into source control in place of the project directory structure.

### Working with Revision Control

The Vivado tools interact with all major revision control systems (RCS, CVS, SVN, ClearCase, Perforce, Git, BitKeeper, etc.). See [Chapter 5: Source Management](chapter5_source_management_and_revision_control.md) for detailed recommendations.

---

## Understanding the Flow Navigator

The Flow Navigator provides control over major design process tasks:

| Section | Functions |
|---|---|
| **Project Manager** | Project settings, source management, IP catalog |
| **IP Integrator** | Create and generate block designs |
| **Simulation** | Run simulation |
| **RTL Analysis** | Open Elaborated Design, Report DRC, Schematic |
| **Synthesis** | Run Synthesis, Open Synthesized Design |
| **Implementation** | Run Implementation, Open Implemented Design |
| **Program and Debug** | Generate Bitstream/Device Image, Open Hardware Manager |

- Commands are grayed out until prerequisite tasks are completed
- For **third-party netlist projects**, system-level design entry, IP, and synthesis options are not available
- Clicking **Generate Bitstream** ensures synthesis and implementation are current before generating

### Design Analysis Shortcuts

When a design is open, the Flow Navigator shows commonly used commands for the current phase. For example, under Synthesis:

- Open Synthesized Design
- Report Timing Summary
- Report Clock Networks
- Report DRC
- Schematic

---

## Performing System-Level Design Entry

### Automated Source File Compilation and Management

The **Sources window** provides:

- **Hierarchy view** — Displays the design hierarchy
- **Compile Order view** — Shows the order sources will be compiled
- **Libraries view** — Organizes files by library
- Automatic compilation and status reporting when project changes
- Cross-probing from Messages window to RTL source lines

> **Tip:** If you explicitly set a top module, it is retained for synthesis. Otherwise, the Vivado tools automatically select the best possible top module.

Constraints and simulation sources are organized into **sets**, enabling experimentation with different configurations.

### RTL Development

Vivado IDE features for RTL development:

- Integrated **Text Editor** for creating/modifying source files
- Automatic **syntax and language construct checking** across multiple files
- **Language templates** with recommended logic constructs
- **Find in Files** for searching template libraries
- RTL elaboration and interactive analysis
- RTL design rule checks
- RTL constraints assignment and I/O planning

### RTL Elaboration and Analysis

When opening an elaborated RTL design:

- RTL source files are compiled and the RTL netlist is loaded
- Available analysis: syntax checking, methodology rule checks, netlist/schematic exploration, DRCs, I/O planning
- Cross-probe between views and RTL source file lines

### Timing Constraint Development and Verification

The **Timing Constraints wizard** guides you through creating and validating timing constraints:

- Identifies clocks and logic constructs in the design
- Provides an interface to enter and validate constraints
- Available only in **synthesized and implemented designs** (requires clock awareness)

> ⚠️ Vivado supports only **SDC and XDC** constraint formats. UCF (ISE) and Synplicity formats are not directly supported. See the *ISE to Vivado Design Suite Migration Guide (UG911)* for UCF-to-XDC migration.

---

## Working with IP

### Configuring IP

The **Vivado IP Catalog** provides:

| License Type | Description |
|---|---|
| **Included** | AMD LogiCORE IP licensed within Vivado at no additional charge |
| **Purchase** | Fee-based IP under the Core License Agreement |

To configure IP:
1. Double-click an IP in the catalog to launch the **Configuration wizard**
2. A `.xci` (Xilinx Core Instance) file is created with all customization options
3. Output products (HDL, constraints, test bench, etc.) are generated from the `.xci`

**Methods to work with IP in a design:**

| Method | Description |
|---|---|
| **Managed IP flow** | Customize IP and generate output products including DCP |
| **Import XCI to Project/Non-Project** | Read the XCI file — recommended for large team projects |
| **IP Catalog from project** | Customize and add IP directly — recommended for small teams |

### Generating IP Output Products

Generated output products include:

- Instantiation template
- RTL source files and XDC constraints
- Synthesized design checkpoint (DCP) — default
- Third-party simulation sources
- Third-party synthesis sources
- Example design (for applicable IP)
- Test bench (for applicable IP)
- C Model (for applicable IP)

> **Tip:** In Project Mode, missing output products are **automatically generated** during synthesis. In Non-Project Mode, they must be manually generated beforehand.

### Using IP Core Containers

The **Core Container** feature provides a single-file representation (`.xcix`) containing both the XCI and all output products. This simplifies revision control by replacing the loose directory structure with one file.

### Out-of-Context (OOC) Design Flow

The default flow for IP catalog cores and IP Integrator block designs:

- Synthesizes IP/modules **independently** of the top-level design
- Creates a **design checkpoint (DCP)** with synthesized netlist and constraints
- Reduces design cycle time and enables result reuse
- Supports **hierarchical team design** methodologies
- **Synthesis cache** preserves OOC results for reuse across designs

> **Important:** To obtain accurate reports, open and analyze the **top-level synthesized design** which includes all integrated OOC modules. OOC modules appear as black boxes until the synthesized design is opened.

### IP Constraints

- Many IP cores include XDC constraints applied automatically in both Project and Non-Project Mode
- IP clock constraints are processed early to make clocks available to dependent IP cores

### Validating IP

Verification methods:
1. Synthesize the IP and run behavioral/structural simulation
2. Implement the IP to validate timing, power, and resource utilization
3. Use the **Open IP Example Design** command for standalone validation
4. The example design may include test benches for behavioral, post-synthesis, or post-implementation simulation

### Packaging Custom IP

Package custom IP or block designs for the Vivado IP catalog:

- Source: RTL files, IP Integrator block design, or Vivado project
- Use the **Create and Package IP wizard**
- Add the repository location in **Tools → Settings → IP Repository**
- Create AXI4 peripherals for embedded processor designs

> **Tip:** Before packaging IP HDL, simulate and synthesize to validate the design.

> **Important:** Ensure the desired list of supported device families is defined properly in the custom IP definition.

### Using Memory IP

Memory IP requires additional I/O pin planning:

1. Customize the memory IP
2. Assign top-level I/O ports to package pins in the elaborated or synthesized design
3. Use the **Memory Bank/Byte Planner** to assign memory I/O pin groups to byte lanes

### Upgrading IP

- **Recommended:** Upgrade IP with each new Vivado release
- Alternatively, use older IP as **static IP** (requires pre-generated output products)
- Locked IP appears with a lock symbol and cannot be re-customized
- Use `report_ip_status` to check the current IP status
- Locked IP can be preserved using **XCIX** core container files

---

## Creating IP Subsystems with IP Integrator

### Building IP Subsystems

The Vivado IP Integrator enables creation of **Block Designs (.bd)** using AXI4 interconnect:

- Drag and drop IP onto the design canvas
- Connect AXI interfaces with single wires
- Supports AMD Zynq UltraScale+ MPSoC, Zynq 7000 SoC, MicroBlaze processors
- Integrates HLS modules, System Generator DSP modules, and custom IP

### Block Design Containers

- Reference secondary block diagrams from a parent block diagram
- Support multiple instances with different parametrizations
- Enable partitioning into several block diagrams

### Referencing RTL Modules in Block Designs

The **Module Reference** feature adds Verilog or VHDL modules directly to a block design without packaging as IP. Quick but lacks full IP catalog benefits.

### Designer Assistance

| Feature | Description |
|---|---|
| **Block Automation** | Configures basic processor-based designs and complex IP subsystems |
| **Connection Automation** | Automatically makes repetitive connections to pins/ports |
| **Platform Board Flow** | Connects I/O ports to target board components |
| **Clock and Reset Assistance** | Helps define and connect clocks and resets |

### Using the Platform Board Flow

- Vivado is **board-aware** and automatically derives I/O constraints and IP configuration
- Board interfaces shown in the **Board** tab of IP Integrator
- Supports 7 series, Zynq 7000, and UltraScale device boards
- Download partner board support from the AMD Vivado Store

### Validating IP Subsystems

```tcl
validate_bd_design
```

- Runs DRCs on the block design
- Reports warnings and errors with cross-probing
- Runs **Parameter Propagation** to auto-update IP parameters based on context

### Generating Block Design Output Products

Two OOC modes for block designs:
- **Out of context per Block design** — entire block design synthesized OOC
- **Out of context per IP** — each IP within the block design synthesized independently

### Integrating Block Designs into Top-Level Design

- Instantiate the block design as a module in a higher-level HDL file
- Use **Create HDL Wrapper** to generate a top-level HDL file for the IP subsystem

---

## Logic Simulation

### Simulation Flow Overview

Key recommendations for simulation:

1. **Run behavioral simulation before synthesis** — issues caught early save time
2. **Infer logic wherever possible** — instantiated primitives add simulation runtime cost
3. **Set Simulator Language to Mixed** unless you lack a mixed-mode license
4. **Turn off the waveform viewer** when not in use to improve performance
5. **In Vivado simulator:** turn off debug during `xelab` for a performance boost
6. **In Vivado simulator:** turn on multi-threading to speed compile time
7. **Target supported simulator versions** per UG973
8. **Enable incremental compile** with third-party simulators
9. **Use `export_simulation`** to generate batch scripts
10. **Generate simulation scripts** for individual IP, BDs, and hierarchical modules
11. **Use UNIFAST libraries** for 7 series devices to improve simulation performance

> ⚠️ UNIFAST libraries are **not supported** for UltraScale device primitives.

### Simulation Stages

| Stage | Simulation Type |
|---|---|
| **Design Entry** | RTL behavioral simulation |
| **Post-Synthesis** | Functional simulation, timing simulation (Verilog only) |
| **Post-Implementation** | Functional simulation, timing simulation (Verilog only) |

### Compiling Simulation Libraries

- **Vivado simulator** — precompiled libraries are delivered; no action needed
- **Third-party simulators** — you must compile AMD simulation libraries using:

```tcl
compile_simlib
```

Or via the IDE: **Tools → Compile Simulation Libraries**

> ⚠️ Third-party simulators will return "library binding" failures if you do not precompile simulation libraries.

### Simulation Time Resolution

> **Recommended:** Run simulations at **1 ps** resolution. Some primitives (e.g., MMCM) require 1 ps for correct behavior.

> **Tip:** There is no significant simulator performance gain from using coarser resolution with AMD simulation models, and no need to use finer resolution (e.g., femtoseconds).

### Functional Simulation Early in the Design Flow

Use RTL behavioral simulation to verify syntax and functionality before synthesis:

- Simulate individual IP, block designs, or hierarchical modules before testing the complete design
- Create a top-level test bench after individual module verification succeeds
- Reuse the same test bench for final timing simulation

> **Recommended:** At this stage, no timing information is provided. Perform simulation in **unit-delay mode** to avoid race conditions.

> Use **synthesizable HDL constructs** for initial design creation. Do not instantiate specific components unless necessary — this allows for more portable, reusable code.

### Using Structural Netlists for Simulation

After synthesis or implementation, netlist simulation (functional or timing mode) helps identify:

- **Synthesis attribute mismatches** (e.g., `full_case`, `parallel_case`)
- **UNISIM attributes** applied in XDC constraint files
- **Synthesis vs. simulation interpretation differences**
- **Dual-port RAM collisions**
- **Missing or improperly applied timing constraints**
- **Asynchronous path operation issues**
- **Functional issues from optimization techniques**

Additional use cases for netlist simulation:
- Sensitize timing paths declared as false or multi-cycle during STA
- Generate netlist switching activity to estimate power
- Identify **X state pessimism**

#### Simulation Libraries

| Library | Description | VHDL Name | Verilog Name |
|---|---|---|---|
| **UNISIM** | Functional simulation of AMD primitives | UNISIM | UNISIMS_VER |
| **UNIMACRO** | Functional simulation of AMD macros | UNIMACRO | UNIMACRO_VER |
| **UNIFAST** | Fast simulation library (7 series only) | UNIFAST | UNIFAST_VER |

> **UNIFAST** is optional for faster functional simulation on 7 series devices. UltraScale and later architectures incorporate UNIFAST optimizations into the UNISIM libraries by default.

> **UNISIM primitive behavior:** No timing information except on clocked elements (100 ps clock-to-out delay to prevent race conditions). Waveforms may show spikes/glitches for combinatorial signals.

### Timing Simulation

AMD supports timing simulation in **Verilog only**:

- Export a netlist from a synthesized or implemented design: **File → Export → Export Netlist** or `write_verilog`
- The `$sdf_annotate` Verilog system task specifies the SDF file for timing delays
- Use the `-sdf_anno` option in **Simulation Settings → Netlist** tab to add the SDF annotation directive
- Write the SDF file with the `write_sdf` command
- The Vivado simulator reads the SDF file automatically during compilation

> **Tip:** The Vivado simulator supports mixed-language simulation — VHDL users can generate a Verilog simulation netlist and instantiate it from a VHDL test bench.

**If you skip timing simulation**, ensure:
- STA constraints are correct (especially exceptions)
- The netlist is exactly equivalent to your RTL intent (watch for inference-related changes)

### Running Simulation

#### Integrated Simulation

The Vivado IDE supports integrated simulation — launch the simulator directly from the IDE:

- Flow Navigator → click **Run Simulation** and select the simulation type
- Configurable simulation settings in **Tools → Settings → Simulation**
- Tcl command: `launch_simulation`

> ⚠️ The `launch_simulation` command supports **Project Mode only** — it does not support Non-Project Mode.

#### Batch Simulation

> **Recommended:** If your verification environment has a self-checking test bench, run simulation in batch mode. There is a **significant runtime cost** when viewing waveforms via integrated simulation.

Use the `export_simulation` Tcl command:
- Generates separate scripts for compile, elaborate, and simulate stages
- Scripts can be used directly or as reference for custom scripts

---

## Running Logic Synthesis and Implementation

### Logic Synthesis

- Configure, launch, and monitor synthesis runs via the Vivado IDE
- Launch **multiple synthesis runs** concurrently or serially
- On Linux: launch runs locally or on **remote servers**
- Open different synthesized netlists for device and design analysis

> ⚠️ Launching multiple jobs simultaneously on the same machine can exhaust memory. Ensure sufficient memory for all concurrent jobs.

### Implementation

- Configure, launch, and monitor implementation runs
- Create reusable **strategies** for different goals (runtime, performance, area)
- Launch multiple implementation runs simultaneously or serially
- Use **constraint sets** to experiment with different constraints or devices

> **Tip:** Add Tcl scripts to be sourced before/after any step using `tcl.pre` and `tcl.post` files.

> **Important (Versal):** From 2024.2 onwards, all Versal devices only support **Advanced Flow**. See UG904.

### Configuring Synthesis and Implementation Runs

- **Run strategies** control synthesis and implementation features
- AMD provides pre-defined strategies, or create custom settings
- Separate constraint sets can be used for synthesis and implementation

### Creating and Managing Runs

**Launch methods:**
- Flow Navigator → Run Synthesis / Run Implementation / Generate Bitstream
- Design Runs window → right-click → Launch Runs
- Flow menu → Run Synthesis / Run Implementation / Generate Bitstream

**Create additional runs:**
1. Flow Navigator → right-click Synthesis or Implementation
2. Select Create Synthesis/Implementation Runs
3. Select constraint set, target part, and strategy in the wizard

### Managing Runs with the Design Runs Window

- Displays run status, information, and management commands
- **Active run** displayed in bold — controls which results are shown
- Double-click any run to open the design in the Vivado IDE
- Make a run active: right-click → **Make Active**

### Resetting Runs

- **Reset Runs** — returns to original state, optionally deletes generated files
- **Reset to Previous Step** — returns to a specific step

> **Tip:** Click **Cancel** in the upper-right corner of the Vivado IDE to stop an in-process run.

### Launching Runs on Remote Clusters

On Linux, access a **load sharing facility (LSF)** server farm. All cluster commands are configurable through Tcl.

### Incremental Compile

Specify incremental compile to:
- Reduce place and route runtimes for small design changes
- Preserve existing implementation results

**Methods:**
- Set Incremental Compile in Implementation Settings
- Right-click in Design Runs window → Set Incremental Compile
- Tcl: `read_checkpoint -incremental <routed_checkpoint.dcp>`

### Intelligent Design Runs (IDR)

Multi-stage run approach to **automatically close timing**:
- GUI: right-click implementation run → "Close Timing Using Intelligent Design Runs"
- Tcl: create a new run using the IDR flow with a reference run

### Engineering Change Orders (ECOs)

Modifications to an implemented design with minimal impact:
- Modify existing design checkpoints
- Run reports on changed netlist
- Generate updated bitstream files
- Leverages incremental place and route for fast turn-around

---

## Viewing Log Files, Messages, Reports, and Properties

### Log Files

The **Log window** displays standard output for Synthesis, Implementation, and Simulation (also in `vivado.log`).

### Messages

The **Messages window** categorizes messages by:
- Design step and severity: **Errors**, **Critical Warnings**, **Warnings**, **Info**, **Status**
- Many messages include links to specific lines in RTL files

### Reports

The **Reports window** shows standard reports generated by `launch_runs`. Additional capabilities:
- Double-click reports to open in the Text Editor
- Create custom reports using Tcl or **report strategies**
- Report strategies associate groups of reports with specific runs

### Device Properties

With a design open: **Tools → Edit Device Properties** to view and set device configuration and bitstream-related properties.

---

## Opening Designs to Perform Design Analysis and Constraints Definition

### Opening an Elaborated RTL Design

Opens the RTL netlist with physical and timing constraints against the target part.

**Analysis capabilities:**
- Linting DRCs and logic correctness checks
- Missing module and interface mismatch detection
- Schematic exploration with RTL-based logic constructs
- Cross-probing from schematic to RTL source files
- I/O planning and DRC validation

**Open methods:**
- Flow Navigator → RTL Analysis → Open Elaborated Design
- Flow menu → Open Elaborated Design

> **Tip:** When possible, perform I/O planning after synthesis for more extensive DRCs and proper clock constraint resolution.

### Opening a Dataflow Design

Facilitates inspection of high bandwidth bus data movement:
- Generates a stripped-down netlist preserving bus nets above a specified width
- Trims scalar nets and lower-level cells
- Helps identify routing congestion, timing, and power issues

**Open methods:**
- Flow menu → Open Dataflow Design (requires a checkpoint or run to be open)
- Tcl: `create_dataflow_design`

### Opening a Synthesized Design

Opens the synthesized netlist with constraints against the target part.

**Design tasks available:**
- Timing, power, and utilization estimates
- Schematic and netlist exploration with cross-probing
- Timing constraint application and analysis
- I/O planning with comprehensive DRC set
- Debug core configuration and insertion

**Open methods:**
- Flow Navigator → Synthesis → Open Synthesized Design
- Design Runs view → double-click run name

### Opening an Implemented Design

Opens the implemented netlist with placement and routing results.

**Design tasks available:**
- Timing analysis, power analysis, utilization statistics
- Placement and routing visualization in Device window
- Interactive placement and routing editing
- LUT equation, RAM initialization, and PLL configuration changes
- Cross-probing to RTL source files

**Open methods:**
- Flow Navigator → Implementation → Open Implemented Design
- Design Runs view → double-click run name

> **Tip:** Toggle the **Routing Resources** button in the Device window to switch between placement-only and routing views.

### Updating Out-of-Date Designs

When sources or constraints change, the Vivado IDE displays an **out-of-date message** in the design window banner.

**Resolution options:**
- **Force up-to-date** — resets the `NEEDS_REFRESH` property:
  ```tcl
  set_property NEEDS_REFRESH false [get_runs synth_1]
  ```
- **Reload** — refreshes the in-memory design (discards unsaved changes)
- **Close Design** — closes the out-of-date design

### View Layouts

Pre-defined layouts for specific tasks:
- I/O Planning
- Floorplanning
- Debug Configuration
- Custom layouts via **Save Layout As**

### Saving Design Changes

**Save to Original XDC Files:**
- File → Constraints → Save (or Save Constraints button)
- Updates existing constraints in place; adds new constraints at end of file

**Save to a New Constraint Set:**
- File → Constraints → Save As
- Creates a new constraint file preserving originals
- Optionally make it the active constraint set

### Closing Designs

You can close designs to reduce the number of designs in memory and prevent multiple locations where sources can be edited. In some cases, you are prompted to close a design prior to changing to another design representation.

**Close methods:**
- In the design title bar, click the close button (**X**)
- In the Flow Navigator, right-click the design and select **Close**

### Analyzing Implementation Results

In an implemented design:
- **Timing Results window** — select timing paths to highlight in Device window
- Interactive editing of placement, routing, LUT equations, RAM initialization, PLL configuration

> **Important:** Changes are made to the in-memory design only. Resetting the run causes changes to be lost. Use **Save Checkpoint** to preserve changes.

### Running Timing Analysis

Available via **Tools → Timing** commands:
- Clock Networks and Clock Interaction reports
- Slack Histogram for overall timing performance
- Tcl timing analysis: `report_timing_summary`, `report_timing`, etc.

### Running Reports: DRC, Power, Utilization

| Command | Purpose |
|---|---|
| `report_power` | Estimate power at any design stage |
| `report_utilization` | Analyze device resource utilization |
| `report_design_analysis` | Analyze critical paths and complexity |
| `report_drc` | Run comprehensive design rule checks |

Reports support:
- Links to select problem areas
- **RPX files** for interactive reports that can be reloaded with object cross-selection

---

## Device Programming, Hardware Verification, and Debugging

### Debug Capabilities

- Configure and implement **ILA** (Integrated Logic Analyzer) and **Debug Hub** cores
- Insert debug cores in RTL, synthesized netlist, or implemented design (ECO flow)
- Select and configure probe signals from synthesized or implemented designs
- Launch Vivado logic analyzer from any run with a completed bitstream

### ECO Debug Flow

Modify debug cores or probes in an implemented design checkpoint and generate updated bitstream files.

---

## Using Project Mode Tcl Commands

### Basic Project Mode Commands

| Command | Description |
|---|---|
| `create_project` | Creates the project (name, location, top module, target part) |
| `add_files` | Adds source files (`.v`, `.vhd`, `.sv`, `.xci`, `.bd`, `.xdc`, `.sdc`) |
| `set_property` | Defines VHDL libraries, simulation-only sources, tool settings, etc. |
| `import_files` | Imports files into the project infrastructure; assigns XDC to constraint sets |
| `launch_runs` | Starts synthesis or implementation with run strategies and standard reports |
| `launch_runs -to_step` | Launches implementation incrementally, including bitstream generation |
| `wait_on_run` | Blocks until the run completes before processing next commands |
| `open_run` | Opens synthesized or implemented design for reporting and analysis |
| `launch_simulation` | Runs integrated simulation (Project Mode only) |
| `close_design` | Closes the in-memory design |
| `start_gui` | Opens the Vivado IDE with current design |
| `stop_gui` | Closes the Vivado IDE with current design |

> **Tip:** Inspect the Tcl Console or `vivado.jou` file to understand the commands behind GUI operations.

### RTL Project Tcl Script Example

```tcl
# run_bft_kintex7_project.tcl
# BFT sample design
#
# Usage: vivado -mode tcl -source run_bft_kintex7_project.tcl

create_project project_bft ./Tutorial_Created_Data/project_bft -part xc7k70tfbg484-2

add_files {./Sources/hdl/FifoBuffer.v ./Sources/hdl/async_fifo.v ./Sources/hdl/bft.vhdl}
add_files -fileset sim_1 ./Sources/hdl/bft_tb.v
add_files ./Sources/hdl/bftLib

set_property library bftLib [get_files {./Sources/hdl/bftLib/round_4.vhdl \
  ./Sources/hdl/bftLib/round_3.vhdl ./Sources/hdl/bftLib/round_2.vhdl \
  ./Sources/hdl/bftLib/round_1.vhdl \
  ./Sources/hdl/bftLib/core_transform.vhdl ./Sources/hdl/bftLib/bft_package.vhdl}]

import_files -force
import_files -fileset constrs_1 -force -norecurse ./Sources/bft_full_kintex7.xdc

update_compile_order -fileset sources_1
update_compile_order -fileset sim_1

# Launch Synthesis
launch_runs synth_1
wait_on_run synth_1
open_run synth_1 -name netlist_1

# Post-synthesis reports
report_timing_summary -delay_type max -report_unconstrained \
  -check_timing_verbose -max_paths 10 -input_pins \
  -file ./Tutorial_Created_Data/project_bft/syn_timing.rpt
report_power -file ./Tutorial_Created_Data/project_bft/syn_power.rpt

# Launch Implementation + Bitstream
launch_runs impl_1 -to_step write_bitstream
wait_on_run impl_1

# Post-implementation reports
open_run impl_1
report_timing_summary -delay_type min_max -report_unconstrained \
  -check_timing_verbose -max_paths 10 -input_pins \
  -file ./Tutorial_Created_Data/project_bft/imp_timing.rpt
report_power -file ./Tutorial_Created_Data/project_bft/imp_power.rpt

start_gui
```

### Netlist Project Tcl Script Example

```tcl
# Kintex-7 Netlist Example Design

# STEP 1: Create Netlist Project
create_project -force project_K7_netlist ./Tutorial_Created_Data/project_K7_netlist/ \
  -part xc7k70tfbg676-2
set_property design_mode GateLvl [current_fileset]
add_files {./Sources/netlist/top.edif}
import_files -force
import_files -fileset constrs_1 -force ./Sources/top_full.xdc

# STEP 2: Implementation + Bitstream
launch_runs impl_1
wait_on_run impl_1
launch_runs impl_1 -to_step write_bitstream
wait_on_run impl_1

# STEP 3: Reports
open_run impl_1
report_timing_summary -delay_type min_max -report_unconstrained \
  -check_timing_verbose -max_paths 10 -input_pins \
  -file ./Tutorial_Created_Data/project_K7_netlist/imp_timing.rpt
report_power -file ./Tutorial_Created_Data/project_K7_netlist/imp_power.rpt

start_gui
```

---

## Best Practices

1. **Use Project Mode for interactive development** — the Flow Navigator and automated management simplify the workflow
2. **Keep source files external to the project** and reference them — or copy them in for portability
3. **Use OOC synthesis** (default) for IP and block designs to reduce compile times
4. **Generate all IP output products** including DCPs for archival and future-proofing
5. **Run behavioral simulation before synthesis** — catch issues early
6. **Use run strategies** to optimize for specific goals (timing, area, runtime)
7. **Use incremental compile** for small design changes to reduce runtimes
8. **Use Intelligent Design Runs (IDR)** for automated timing closure
9. **Save design checkpoints** after critical steps for analysis and fallback
10. **Use the `vivado.jou` journal file** as a starting point for Tcl script development
11. **Validate IP subsystems** (`validate_bd_design`) before proceeding to synthesis
12. **Monitor memory usage** when launching multiple concurrent jobs

---

## Quick Reference

| Task | GUI Method | Tcl Command |
|---|---|---|
| Create project | Create Project wizard | `create_project` |
| Add sources | File → Add Sources | `add_files` |
| Run simulation | Flow Navigator → Run Simulation | `launch_simulation` |
| Run synthesis | Flow Navigator → Run Synthesis | `launch_runs synth_1` |
| Run implementation | Flow Navigator → Run Implementation | `launch_runs impl_1` |
| Generate bitstream | Flow Navigator → Generate Bitstream | `launch_runs impl_1 -to_step write_bitstream` |
| Open synthesized design | Flow Navigator → Open Synthesized Design | `open_run synth_1` |
| Open implemented design | Flow Navigator → Open Implemented Design | `open_run impl_1` |
| Report timing | Tools → Timing → Report Timing Summary | `report_timing_summary` |
| Report utilization | Reports → Report Utilization | `report_utilization` |
| Report power | Reports → Report Power | `report_power` |
| Run DRC | Reports → Report DRC | `report_drc` |
| Archive project | File → Project → Archive | `archive_project` |
| Write project Tcl | File → Project → Write Tcl | `write_project_tcl` |
| Validate block design | Tools → Validate Design | `validate_bd_design` |

---

## See Also

- [Chapter 1: Vivado System-Level Design Flows](chapter1_vivado_system-level_design_flows.md)
- [Chapter 2: Understanding Use Models](chapter2_understanding_use_models.md)
- [Chapter 4: Using Non-Project Mode](chapter4_using_non-project_mode.md)
- [Chapter 5: Source Management and Revision Control](chapter5_source_management_and_revision_control.md)

---

## Source Attribution

- **Source:** *Vivado Design Suite User Guide: Design Flows Overview (UG892)*, v2025.2, November 20, 2025
- **Chapter:** Chapter 3 — Using Project Mode (Pages 28–74)
- **Publisher:** Advanced Micro Devices, Inc.
