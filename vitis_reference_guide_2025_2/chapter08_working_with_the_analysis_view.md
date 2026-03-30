# Chapter 8: Working with the Analysis View (Vitis Analyzer)

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 8 (pp. 404–429)

## Overview

The Analysis View (Vitis Analyzer) is the unified report viewing environment in the AMD Vitis™ tools. It enables opening, navigating, and cross-probing summary reports from compile, link, package, and run stages. This chapter covers how to open and configure the Analysis View, navigate reports, view AI Engine compilation summaries, and import external data files.

---

## Table of Contents

| Section | Description |
|---|---|
| [Opening Vitis Analyzer](#opening-vitis-analyzer) | Command-line and IDE launch methods |
| [Configuring the Analysis View](#configuring-the-analysis-view) | Preferences and display settings |
| [Open Summary Reports](#open-summary-reports) | Loading compile/link/package/run summaries |
| [Open Trace Summary Using Time Window](#open-trace-summary-using-time-window) | Filtering trace data by time range |
| [Analysis View Window Manager](#analysis-view-window-manager) | Report navigation and cross-probing |
| [Viewing AI Engine Compilation Summary Reports](#viewing-ai-engine-compilation-summary-reports) | AI Engine-specific reports |
| [Viewing AI Engine Graphs and Arrays](#viewing-ai-engine-graphs-and-arrays) | Graph connectivity and array spatial views |
| [Graph and Array Detail Tables](#graph-and-array-detail-tables) | Kernels, I/O, buffers, ports, nets, tiles |
| [FIFO Depth Evaluation](#fifo-depth-evaluation) | Estimating optimal FIFO depth |
| [AI Engine Compilation Summary](#ai-engine-compilation-summary) | Resource utilization and kernel summary |
| [AI Engine Kernel Stack and Heap Reports](#ai-engine-kernel-stack-and-heap-reports) | Memory analysis reports |
| [Importing JSON Output Files](#importing-json-output-files) | Importing xrt-smi data into Analysis View |

---

## Opening Vitis Analyzer

### Command Line

```bash
# Open standalone
vitis_analyzer

# Open with a specific summary file
vitis_analyzer <summary_file>

# Using vitis command
vitis -a <summary_file>
```

### From the IDE

Open the Analysis View from the **Flow Navigator** after a build step completes, or by double-clicking a summary file in the Component Explorer.

### Combined Methods

You can open the analyzer standalone and then load summary files, or launch it directly with a specific summary from either the command line or IDE.

---

## Configuring the Analysis View

### Preferences

| Preference | Description | Default |
|---|---|---|
| **Auto Reveal** | Automatically reveal reports in the navigator | On |
| **Max Recent Summaries** | Maximum number of recent summaries to track | 10 |
| **Restore Last Session** | Restore previously opened summaries on launch | Off |
| **Font** | Display font for the Analysis View | System default |

Access preferences via **Edit → Preferences** in the Analysis View.

---

## Open Summary Reports

Load summary reports from any stage of the Vitis flow:

| Summary Type | Source | File Pattern |
|---|---|---|
| **Compile Summary** | `v++ -c` | `*.compile_summary` |
| **Link Summary** | `v++ -l` | `*.link_summary` |
| **Package Summary** | `v++ --package` | `*.package_summary` |
| **Run Summary** | Runtime execution | `*.run_summary` |

### Open Summary Folder

Use **Open Summary Folder** to load all summary files from a build directory. Reports are organized in a **hierarchy grouping** by build stage.

---

## Open Trace Summary Using Time Window

Filter trace data to a specific time range using `vcdanalyze`:

1. Open the trace summary in the Analysis View.
2. Select **Time Window** to specify start and end times.
3. The view filters to show only events within the selected window.

This is useful for analyzing specific phases of execution in large trace files.

---

## Analysis View Window Manager

### Report Navigator

The **Report Navigator** panel lists all loaded summaries and their available reports in a tree view.

### Report Window

The main content area displays the selected report. Multiple reports can be open simultaneously in tabs.

### Code Viewer

Source code associated with a report can be viewed side-by-side, enabling **cross-probing** between reports and source code.

### Cross-Probing

Click on elements in one report to highlight related elements in other open reports. For example:
- Click a kernel in the Graph view to highlight it in the Array view
- Click an operation in the Schedule Viewer to jump to the source code
- Select a function in the timeline to see its synthesis metrics

### Out-of-Date Banners

When a summary file is older than the current build, an **out-of-date banner** is displayed to warn that the report may not reflect the latest results.

---

## Viewing AI Engine Compilation Summary Reports

Open the `aiecompile_summary` file to access AI Engine-specific reports:

| Report | Description |
|---|---|
| **Summary** | High-level compilation status and statistics |
| **Kernel Guidance** | Optimization recommendations for kernels |
| **Graph** | Graph connectivity visualization |
| **Array** | Spatial placement on the AI Engine array |
| **Constraints** | Applied constraints and their resolution |
| **Mapping Analysis** | Kernel-to-tile mapping details |
| **DMA Analysis** | DMA channel allocation and usage |
| **Lock Allocation** | Lock resource allocation per tile |
| **AI Engine Compilation** | Detailed compilation metrics |

---

## Viewing AI Engine Graphs and Arrays

### Graph View

Displays the **connectivity** of the AI Engine graph:
- Kernels shown as nodes
- Connections (buffers, streams) shown as edges
- Port connections to PL and memory

### Array View

Displays the **spatial placement** of kernels on the AI Engine array:
- Physical tile locations
- Routing paths
- Resource utilization per tile

### Settings Panel

Configure display options:
- Show/hide connection types
- Filter by kernel or graph instance
- Toggle labels and annotations

---

## Graph and Array Detail Tables

### Kernels Table

| Column | Description |
|---|---|
| **Graph Instance** | Parent graph instance name |
| **ID** | Unique kernel identifier |
| **AI Engine Kernel** | Kernel function name |
| **Source** | Source file location |
| **Column** | Array column placement |
| **Row** | Array row placement |
| **Schedule** | Scheduling type |
| **Runtime Ratio** | Kernel runtime ratio |
| **Graph Source** | Source graph definition file |

### I/O Table (PLIO Connections)

| Column | Description |
|---|---|
| **Name** | I/O port name |
| **Type** | PLIO type |
| **Data Width** | Data width in bits |
| **Frequency** | Operating frequency |
| **Buffers** | Associated buffer resources |
| **Connected Ports** | Ports connected to this I/O |
| **Column** | Interface tile column |
| **Channel ID** | DMA channel identifier |
| **Packet IDs** | Packet switching identifiers |

### Buffers Table

| Column | Description |
|---|---|
| **Name** | Buffer name |
| **ID** | Buffer identifier |
| **Type** | Buffer type (ping/pong, single) |
| **Net** | Parent net |
| **Column** | Tile column |
| **Row** | Tile row |
| **Bank** | Memory bank |
| **Offset** | Address offset |
| **Size** | Buffer size in bytes |
| **Lock ID** | Associated lock |
| **Lock Name** | Lock name |

### Ports Table

| Column | Description |
|---|---|
| **Name** | Port name |
| **ID** | Port identifier |
| **Type** | Port type |
| **Direction** | Input/output |
| **Data Type** | Data type |
| **Buffers** | Associated buffers |
| **Connected Ports** | Connected port list |

### Nets Table

| Column | Description |
|---|---|
| **Name** | Net name |
| **Variable** | Associated variable |
| **Source Graph Node/Port/ID** | Source endpoint |
| **Destination Graph Node/Port/ID** | Destination endpoint |
| **Latency** | Net latency |
| **FIFO Depth** | FIFO depth if applicable |
| **Constraint** | Applied constraint |
| **Buffers** | Associated buffers |
| **Switch Count** | Number of switch hops |
| **Switch FIFOs** | Switch FIFO resources used |

### Tiles Table

| Column | Description |
|---|---|
| **Tile** | Tile name |
| **Column** | Array column |
| **Row** | Array row |
| **Kernels** | Kernels placed on this tile |
| **Buffers** | Buffers allocated on this tile |

### Interface Channels Table

| Column | Description |
|---|---|
| **Name** | Channel name |
| **PL Instance** | PL instance connection |
| **Net** | Associated net |
| **AI Engine/Memory/Interface Tile Trace** | Trace configuration |

---

## FIFO Depth Evaluation

Evaluate optimal FIFO depths using the `--evaluate-fifo-depth` compiler option:

```bash
v++ -c --mode aie --evaluate-fifo-depth ...
```

After evaluation, the Nets table includes additional columns:

| Column | Description |
|---|---|
| **Estimated FIFO** | Compiler-estimated optimal FIFO depth |
| **Peak FIFO** | Peak observed FIFO depth during simulation |

### Setting FIFO Depth

```
fifo_depth=<net_name>:<depth>
```

---

## AI Engine Compilation Summary

The compilation summary includes:

### Status
- Overall compilation pass/fail status
- Warning and error counts

### AI Engine Resource Utilization

| Resource | Metrics |
|---|---|
| **AI Engine Tiles** | Total used / available |
| **Memory Tiles** | Total used / available |
| **Interface Tiles** | Total used / available |
| **DMA Channels** | Channels allocated |
| **Lock Resources** | Locks allocated |

### AI Engine Kernels Section
- Per-kernel compilation status
- Memory usage (stack + heap)
- Cycle count estimates

### Command Section
- Full compiler command that was executed

---

## AI Engine Kernel Stack and Heap Reports

### Call Tree Report
- Function call hierarchy per kernel
- Stack frame sizes at each level

### Memory Reports
- Stack and heap usage per kernel
- Memory bank allocation details
- Potential memory conflicts

---

## Importing JSON Output Files

Import JSON output files generated by `xrt-smi examine` into the Analysis View:

1. Run `xrt-smi examine` to generate a JSON report from the device.
2. In the Analysis View, use **File → Import** to load the JSON file.
3. Combine with a compile summary for correlated analysis of runtime and compile-time data.

---

## Best Practices

1. **Open all summaries together** — Use Open Summary Folder to load compile, link, package, and run summaries for a complete view.
2. **Use cross-probing** — Click elements in one report to find related information in other reports.
3. **Watch for out-of-date banners** — Rebuild and reload summaries when reports become stale.
4. **Evaluate FIFO depths** — Use `--evaluate-fifo-depth` to find optimal FIFO sizes and avoid deadlocks.
5. **Export tables** — Export detail tables to CSV for offline analysis and documentation.
6. **Time-window trace analysis** — Use the time window feature to focus on specific execution phases in large traces.

---

## See Also

- [Chapter 4: Managing Vitis HLS Components](chapter04_managing_the_vitis_hls_components_in_the_vitis_unified_ide.md) — Schedule Viewer, Dataflow Viewer, and synthesis reports
- [Chapter 5: Managing AI Engine Components](chapter05_managing_the_ai_engine_component_in_the_vitis_unified_ide.md) — AI Engine build and simulation
- [Chapter 2: Vitis Commands and Utilities](chapter02_vitis_commands_and_utilities.md) — `xrt-smi` utility and `v++ -c --mode aie`
- [Chapter 9: Additional Information](chapter09_additional_information.md) — Output directory structure and report file locations

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 8 (pp. 404–429)*
