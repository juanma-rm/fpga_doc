# Chapter 4: Managing the Vitis HLS Components in the Vitis Unified IDE

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 4 (pp. 307–367)

## Overview

This chapter describes how to create, build, simulate, synthesize, analyze, package, and implement HLS components in the AMD Vitis™ Unified IDE. It covers the full HLS development workflow from component creation through C/RTL co-simulation, synthesis analysis, RTL packaging, Vivado implementation, and command-line flows. It also covers the RTL Blackbox Wizard, analysis viewers, component comparison, and the L1 Library Wizard.

---

## Table of Contents

| Section | Description |
|---|---|
| [Using the Flow Navigator](#using-the-flow-navigator) | Available flow steps for HLS components |
| [Creating Vitis HLS Components](#creating-vitis-hls-components) | Component creation wizard |
| [Building and Running an HLS Component](#building-and-running-an-hls-component) | Development flow overview |
| [Using the RTL Blackbox Wizard](#using-the-rtl-blackbox-wizard) | Integrating existing RTL IP into HLS |
| [Running C Synthesis](#running-c-synthesis) | Synthesis configuration and execution |
| [Synthesis Summary](#synthesis-summary) | Understanding synthesis reports |
| [Function Call Graph](#function-call-graph) | Throughput and resource visualization |
| [Schedule Viewer](#schedule-viewer) | Operation scheduling analysis |
| [Dataflow Viewer](#dataflow-viewer) | Channel and process visualization |
| [Running C/RTL Co-Simulation](#running-crtl-co-simulation) | Co-simulation configuration and reports |
| [Timeline Trace Viewer](#timeline-trace-viewer) | Runtime profile of functions |
| [Viewing Simulation Waveforms](#viewing-simulation-waveforms) | Waveform analysis in Vivado simulator |
| [Packaging the RTL Design](#packaging-the-rtl-design) | Output format options for RTL |
| [Running Implementation](#running-implementation) | Vivado synthesis and implementation |
| [Cloning HLS Components](#cloning-hls-components) | Duplicating components for comparison |
| [Component Comparison](#component-comparison) | Tabular and graphical comparison |
| [L1 Library Wizard Flow](#l1-library-wizard-flow) | Using Vitis Accelerated Libraries |
| [Creating HLS Components from Command Line](#creating-hls-components-from-command-line) | v++ and vitis-run CLI flow |

---

## Using the Flow Navigator

The Flow Navigator provides access to HLS flow steps:

| Flow Step | Description |
|---|---|
| **C Simulation** | Compile and run the C/C++ testbench |
| **C Synthesis** | Synthesize C/C++ to RTL |
| **C/RTL Co-Simulation** | Verify RTL against C testbench |
| **Package** | Export the RTL as IP or XO |
| **Implementation** | Run Vivado synthesis and implementation |

---

## Creating Vitis HLS Components

### Wizard Steps

1. **Name and Location** — Specify the component name and workspace location.
2. **Configuration File** — Select or create an HLS configuration file.
3. **Source Files** — Add C/C++ source files and specify the **top function**.
4. **Part/Platform** — Select the target FPGA part or platform.
5. **Settings** — Configure:
   - **Clock period** (ns or frequency)
   - **Flow target** (`vivado` for IP flow, `vitis` for kernel flow)

### Configuration File

The HLS configuration file (`.cfg`) stores all component settings including source files, top function, clock, part selection, and optimization directives.

---

## Building and Running an HLS Component

### Development Flow

The recommended development flow progresses through these stages:

1. **Architect** — Design the C/C++ algorithm and interfaces
2. **C Simulation** — Verify functional correctness with testbench
3. **Code Analyzer** — Analyze code structure and potential issues
4. **C Synthesis** — Generate RTL from C/C++
5. **C/RTL Co-Simulation** — Verify RTL functional equivalence
6. **Analyze** — Review synthesis reports and viewers
7. **Package** — Export RTL as IP catalog or XO

### Code Analyzer

The Code Analyzer runs alongside C Simulation and provides static analysis of the source code to identify optimization opportunities and potential issues before synthesis. Enable it by setting `csim.code_analyzer=true` in the HLS configuration file or through the Flow Navigator checkbox.

```ini
[hls]
csim.code_analyzer=true
```

> **TIP:** Run Code Analyzer early in the development cycle to identify structural issues (e.g., suboptimal loop structures, memory access patterns) before investing time in C Synthesis.

---

## Using the RTL Blackbox Wizard

The RTL Blackbox Wizard enables integrating existing RTL IP into the HLS design. It generates a C++ wrapper and a JSON description file.

### Steps

1. **C++ Model Files** — Provide the C++ model that represents the RTL behavior.
2. **C File Wizard** — Generate the C wrapper interface.
3. **RTL IP Definition** — Specify the RTL source files (Verilog/VHDL).
4. **RTL Common Signals** — Map RTL signals to HLS interface signals (clock, reset, CE).
5. **JSON Generation** — The wizard generates a JSON file describing the RTL blackbox configuration.

---

## Running C Synthesis

### Flow Target

| Target | Description |
|---|---|
| **vivado** | IP flow — generates IP for Vivado integration |
| **vitis** | Kernel flow — generates XO for Vitis system integration |

### Configuration

1. **Load Sources** — Source files and top function from configuration.
2. **Default Settings** — Clock period, part/platform.
3. **Design Directives** — Apply optimization directives (PIPELINE, UNROLL, ARRAY_PARTITION, etc.).
4. **Run Synthesis** — Execute `v++ -c --mode hls` or through the Flow Navigator.

---

## Synthesis Summary

After C Synthesis completes, the synthesis summary provides:

### General Information

- Component name, top function, part/platform
- Clock target and estimated clock

### Timing Estimate

- Target clock period vs. estimated clock period
- Timing margin/violation indicators

### Performance & Resource Estimates

| Resource | Metrics |
|---|---|
| **BRAM** | Utilization count and percentage |
| **DSP** | Utilization count and percentage |
| **FF** | Flip-flop utilization |
| **LUT** | Look-up table utilization |
| **URAM** | UltraRAM utilization (if applicable) |

### Additional Reports

| Report | Description |
|---|---|
| **HW Interfaces** | Generated hardware interfaces (s_axilite, m_axi, ap_ctrl, etc.) |
| **SW I/O** | Software-accessible I/O mapping |
| **M_AXI Burst Info** | AXI master burst configuration details |
| **Pragma Report** | Summary of applied pragmas and their effects |
| **Bind Op Report** | Operation binding to hardware resources |
| **Bind Storage Report** | Storage binding to memory resources |

---

## Function Call Graph

The Function Call Graph provides a visual representation of the function hierarchy with performance metrics overlaid as a **heat map**.

### Heat Map Metrics

| Metric | Description |
|---|---|
| **II (Initiation Interval)** | Cycles between successive iterations |
| **Latency** | Total cycles for one execution |
| **Resource** | Resource utilization per function |
| **Stalling** | Stall information per function |

Select different metrics to highlight performance bottlenecks in the function hierarchy.

---

## Schedule Viewer

The Schedule Viewer displays the scheduled operations across clock cycles:

| Element | Description |
|---|---|
| **Operations** | Individual C/RTL operations (read, write, compute) |
| **Clock Cycles** | Time axis showing cycle-by-cycle scheduling |
| **Dependencies** | Data and control dependency edges between operations |
| **Timing Violations** | Highlighted paths that exceed the clock period |
| **Properties View** | Detailed properties of selected operations |

Use the Schedule Viewer to:
- Identify operations on the critical path
- Find timing violations
- Understand operation scheduling and parallelism

---

## Dataflow Viewer

The Dataflow Viewer visualizes dataflow designs with channels and processes:

| Element | Description |
|---|---|
| **FIFO Channels** | First-In-First-Out buffers between processes |
| **PIPO Channels** | Ping-Pong buffers between processes |
| **Processes** | Individual task functions in the dataflow |
| **Deadlock Detection** | Visual indicators of potential deadlocks |

### Process Profiling

View per-process execution metrics to identify bottlenecks in the dataflow pipeline.

---

## Running C/RTL Co-Simulation

### Configuration Options

| Option | Description | Default |
|---|---|---|
| **trace_level** | Waveform trace detail level (`none`, `all`, `port`, `port_and_axi`) | `none` |
| **random_stall** | Enable random stall injection on AXI interfaces | Off |
| **wave_debug** | Enable waveform debugging | Off |
| **Deadlock Detection** | Enable deadlock detection during simulation | On |
| **Dataflow Profiling** | Profile dataflow channels during co-simulation | Off |

### Simulator Selection

Use the default XSIM simulator or configure a third-party simulator (see [Chapter 7](chapter07_enabling_third_party_simulators.md)).

### Output

Co-simulation generates:
- Pass/fail status based on testbench results
- `cosim.rpt` report with latency and II measurements
- Waveform files (if `wave_debug` enabled)

---

## Timeline Trace Viewer

The Timeline Trace Viewer displays a runtime profile of function execution:

- Shows function start/end times across clock cycles
- Identifies **FIFO stall** and **starve** states in dataflow designs
- Helps visualize pipeline throughput and latency

---

## Viewing Simulation Waveforms

When `wave_debug` is enabled during co-simulation, waveforms can be viewed in the Vivado simulator GUI:

- **HLS Process Summary** — High-level view of process activity
- **Dataflow Analysis** — Channel fill levels, stall/starve detection
- Signal-level waveform inspection

---

## Packaging the RTL Design

### Output Formats

| Format | Description | Use Case |
|---|---|---|
| **ip_catalog** (.zip) | Vivado IP Catalog format | Integration into Vivado block design |
| **xo** | Xilinx Object file | Vitis kernel flow (v++ --link) |
| **sysgen** | System Generator format | System Generator integration |
| **rtl** | Raw RTL output | Manual RTL integration |

### IP Configuration (VLNV)

When packaging as `ip_catalog`, configure the IP metadata:

| Field | Description |
|---|---|
| **Vendor** | IP vendor name (e.g., `xilinx.com`) |
| **Library** | IP library name (e.g., `hls`) |
| **Name** | IP name (from top function) |
| **Version** | IP version number |

---

## Running Implementation

Run Vivado synthesis and implementation directly from the Vitis IDE to get accurate resource and timing results.

### Configuration Options

| Category | Options |
|---|---|
| **Vivado Synthesis** | Strategy, directive, optimization settings |
| **Vivado Implementation** | Place and route strategy, timing closure options |

### Reports

| Report | Description |
|---|---|
| **Design Characteristics** | Overall design metrics |
| **Fail Fast** | Early-stage implementation results for quick feedback |
| **Timing Paths** | Detailed timing path analysis |

---

## Cloning HLS Components

Clone an existing HLS component to create a copy for experimentation:

1. Right-click the component in Component Explorer.
2. Select **Clone Component**.
3. The cloned component gets a new name while retaining all settings and source files.

Use cloning to test different optimization strategies without modifying the original component.

---

## Component Comparison

Compare two HLS components side-by-side:

### Comparison Methods

| Method | Description |
|---|---|
| **Tabular** | Side-by-side table of synthesis metrics (latency, II, resources) |
| **Graphical** | Bar/chart visualization of differences |
| **CSV Export** | Export comparison data to CSV for external analysis |

### Steps

1. Select two components in the Component Explorer.
2. Right-click and select **Compare**.
3. View differences in timing, resource utilization, and performance.

---

## L1 Library Wizard Flow

The L1 Library Wizard provides access to **Vitis Accelerated Libraries** (L1 functions from Solver and Vision libraries).

### Three Library Flows

| Flow | Description |
|---|---|
| **Examples** | Open and run pre-built library examples |
| **Create from Library** | Create a new HLS component from a library function |
| **Auto-completion** | Use IDE auto-completion with library headers |

### Supported Libraries

| Library | Description |
|---|---|
| **Solver** | Math solver functions (linear algebra, DSP) |
| **Vision** | Computer vision functions (OpenCV-compatible HLS) |

---

## Creating HLS Components from Command Line

### Compilation

```bash
v++ -c --mode hls --config <config_file>.cfg
```

### Flow Steps

```bash
# C Simulation
vitis-run --mode hls --csim --config <config_file>.cfg

# C/RTL Co-Simulation
vitis-run --mode hls --cosim --config <config_file>.cfg

# Implementation
vitis-run --mode hls --impl --config <config_file>.cfg

# Package
vitis-run --mode hls --package --config <config_file>.cfg
```

### Configuration File Example

```ini
[hls]
flow_target=vitis
clock=10
top=my_kernel
part=xcu250-figd2104-2L-e

[vivado]
synth.strategy=Flow_PerfOptimized_high
impl.strategy=Performance_Auto

[csim]
argv=-I/path/to/testbench/data

[cosim]
trace_level=all
wave_debug=1
```

### Opening Reports from Command Line

After running flow steps via the command line, view reports using:
- Vitis Analyzer: `vitis_analyzer <compile_summary_file>`
- Report files in the component's output directory

---

## Best Practices

1. **Follow the development flow** — Progress sequentially: C-sim → Synthesis → Co-sim → Analyze → Package.
2. **Use Code Analyzer early** — Identify optimization opportunities before synthesis.
3. **Check the Schedule Viewer** — Understand critical paths and timing before optimization.
4. **Use Dataflow Viewer for pipelines** — Identify FIFO sizing issues and deadlocks.
5. **Enable deadlock detection** — Always enable during co-simulation of dataflow designs.
6. **Clone before optimizing** — Clone components to compare before/after optimization results.
7. **Run Implementation** — Use Vivado implementation for accurate post-place-and-route metrics before deployment.
8. **Leverage L1 Libraries** — Use pre-optimized library functions (Solver, Vision) instead of writing from scratch.
9. **Use configuration files** — Store all settings in `.cfg` files for reproducible builds across GUI and CLI flows.

---

## See Also

- [Chapter 2: Vitis Commands and Utilities](chapter02_vitis_commands_and_utilities.md) — `v++ -c --mode hls`, HLS optimization directives, and pragma reference
- [Chapter 3: Using the Vitis Unified IDE](chapter03_using_the_vitis_unified_ide.md) — IDE overview and system project integration
- [Chapter 7: Enabling Third-Party Simulators](chapter07_enabling_third_party_simulators.md) — Configuring alternative simulators for co-simulation
- [Chapter 8: Working with the Analysis View](chapter08_working_with_the_analysis_view.md) — Viewing HLS synthesis and co-simulation reports
- [Chapter 9: Additional Information](chapter09_additional_information.md) — Output directory structure for HLS builds
- *Vitis High-Level Synthesis User Guide (UG1399)*

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 4 (pp. 307–367)*
