# Chapter 5: Managing the AI Engine Component in the Vitis Unified IDE

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 5 (pp. 368–394)

## Overview

This chapter describes how to create, configure, build, simulate, debug, and profile AI Engine components in the AMD Vitis™ Unified IDE. It covers the full development workflow from component creation through simulation, trace and profile analysis, pipeline debugging, and prototype code generation. Support for both GUI-based and Python CLI-based workflows is provided.

---

## Table of Contents

| Section | Description |
|---|---|
| [Creating an AI Engine Component](#creating-an-ai-engine-component) | Wizard-based component creation and configuration |
| [Importing Files](#importing-files) | Adding source files to the component |
| [Vitis Unified IDE Examples](#vitis-unified-ide-examples) | 18 AI Engine template examples |
| [Building the AI Engine Component](#building-the-ai-engine-component) | Build targets, output directory, and reports |
| [Managing AI Engine Components with Python CLI](#managing-ai-engine-components-with-python-cli) | Interactive and scripted Python workflows |
| [Simulating and Debugging](#simulating-and-debugging) | Launch configurations for x86sim and aiesimulator |
| [Enabling Trace](#enabling-trace) | WDB and VCD trace output options |
| [Enabling AI Engine Profile](#enabling-ai-engine-profile) | Throughput and latency profiling with CSV export |
| [Extracting Throughput and Latency Estimates](#extracting-throughput-and-latency-estimates) | Python CLI functions for performance metrics |
| [Enabling AI Engine Pipeline](#enabling-ai-engine-pipeline) | Pipeline view with execution stages |
| [Debugging an AI Engine Component](#debugging-an-ai-engine-component) | Debug view in the IDE |
| [Generating AI Engine Prototype Code](#generating-ai-engine-prototype-code) | Wizard for graph/kernel code generation |
| [Single Kernel Development](#single-kernel-development) | Vectorization, memory access, and software pipelining |
| [Exporting Summary Tables](#exporting-summary-tables) | CSV export from Analysis View |

---

## Creating an AI Engine Component

Use the Vitis IDE wizard to create a new AI Engine component:

1. Select **File → New Component → AI Engine Component**.
2. Specify the component name and location.
3. The wizard generates a `vitis-comp.json` component descriptor and a default `aiecompiler.cfg` configuration file.

### Configuration File Sections (`aiecompiler.cfg`)

The configuration file organizes settings into the following categories:

| Section | Description |
|---|---|
| **Generic** | General compilation settings |
| **AI Engine** | AI Engine-specific options |
| **CDO** | Configuration Data Object settings |
| **Compiler Debugging** | Debug-related compiler flags |
| **DRC** | Design Rule Check settings |
| **File Specific** | Per-file compilation options |
| **Miscellaneous** | Other compilation options |
| **Module-Specific** | Per-module settings |
| **Tracing** | Trace generation options |
| **XLOpt** | Optimization level settings |

---

## Importing Files

Add source files to the component using **File → Import Files** or by dragging files into the Component Explorer. Source files include AI Engine kernel code (`.cc`, `.cpp`), graph files, and data files for simulation.

---

## Vitis Unified IDE Examples

The Vitis IDE provides 18 AI Engine template examples:

| Example | Description |
|---|---|
| System Design | Full system design example |
| Async Buffer | Asynchronous buffer usage |
| Async RTP | Asynchronous run-time parameters |
| C++ Template | C++ template-based kernel |
| GMIO Bandwidth | GMIO bandwidth measurement |
| Mapping Placement | Kernel mapping and placement |
| Interface Tile Constraints | Interface tile constraint setup |
| Simple | Basic AI Engine example |
| 128-bit Interface | 128-bit data interface |
| 64-bit Interface | 64-bit data interface |
| Bypass | Bypass kernel example |
| Margin | Margin data handling |
| Packet Split Merge | Packet splitting and merging |
| Param | Parameterized kernel |
| Single Buffer | Single buffer usage |
| Single Node Graph | Single node graph example |
| Stream Switch FIFO | Stream switch FIFO configuration |

---

## Building the AI Engine Component

### Build Targets

| Target | Description |
|---|---|
| **x86sim** | Functional simulation on x86 (fast, no cycle accuracy) |
| **hw** | Full AI Engine compilation for hardware |

### Build Output

The build produces output in the **work** directory, including:
- Compiled AI Engine binaries
- Build reports
- Microcode files (viewable in the IDE)

### Reports

After a successful build, view reports through the Flow Navigator or Analysis View. Reports include compilation summary, resource utilization, kernel guidance, and graph/array views.

---

## Managing AI Engine Components with Python CLI

### Interactive Mode

```bash
vitis -i
```

Launch the Vitis interactive Python shell, then use AI Engine Python APIs.

### Script Mode

```bash
vitis -s <script.py>
```

### Python APIs

| API | Description |
|---|---|
| `create_aie_component()` | Create a new AI Engine component |
| `import_files()` | Import source files into the component |
| `update_top_level_file()` | Set the top-level graph file |
| `build()` | Build the AI Engine component |
| `report()` | Generate and view reports |

#### Example: Create and Build

```python
client = create_client()
comp = client.create_aie_component(
    name="my_aie",
    platform="<platform_path>",
    template="empty"
)
comp.import_files(sources=["graph.cpp", "kernels/"])
comp.build(target="hw")
comp.report()
```

---

## Simulating and Debugging

### Launch Configurations

Simulation is configured through launch configurations with the following settings:

| Setting | Description |
|---|---|
| **Simulator** | `x86sim` or `aiesimulator` |
| **Enable Pipeline View** | Enable pipeline stage visualization |
| **Package directory** | Path to packaged outputs |
| **Input directory** | Path to simulation input data |
| **Additional arguments** | Extra simulator command-line arguments |
| **Trace Options** | Enable/configure trace output |
| **Profile Options** | Enable/configure profiling |

### Running Simulation

1. Open the Flow Navigator.
2. Select **Run** or **Debug** under the simulation target.
3. Configure the launch settings.
4. Start simulation.

---

## Enabling Trace

### Trace Output Formats

| Format | Description |
|---|---|
| **WDB** (online) | Waveform Database for live viewing in the IDE |
| **VCD** | Value Change Dump for offline analysis |

### Using VCD Trace

```bash
aiesimulator --dump-vcd=<name>
```

Configure trace modules and trace options through the simulation launch configuration or options file.

---

## Enabling AI Engine Profile

### Profiling Modes

- **All cores** — Profile all AI Engine cores
- **Custom core selection** — Select specific cores to profile

### Output

Profiling generates CSV files containing:
- **Throughput** data per kernel/port
- **Latency** data per kernel

---

## Extracting Throughput and Latency Estimates

Use Python CLI functions to extract performance estimates from simulation results:

| Function | Description |
|---|---|
| `export_aiesim_latency()` | Export latency estimates to CSV |
| `export_aiesim_throughput()` | Export throughput estimates to CSV |
| `export_aiesim_continuous_throughput()` | Export continuous throughput data |
| `export_aiesim_continuous_latency()` | Export continuous latency data |

---

## Enabling AI Engine Pipeline

The **Pipeline View** provides a cycle-accurate visualization of kernel execution:

| Column | Description |
|---|---|
| **Program Counter** | Current instruction address |
| **ID** | Instruction identification |
| **E1–E7** | Execution pipeline stages |
| **AGUs** | Address Generation Units activity |

Use this view to identify pipeline stalls and optimize kernel performance.

---

## Debugging an AI Engine Component

The **Debug View** in the Vitis IDE supports:
- Setting breakpoints in AI Engine kernel code
- Step-through debugging (x86sim target)
- Variable inspection
- Memory view
- Register inspection

Launch debugging by selecting **Debug** in the Flow Navigator for the desired simulation target.

---

## Generating AI Engine Prototype Code

The AI Engine Prototype Code wizard generates starter code:

1. Open **File → New → AI Engine Prototype Code**.
2. Configure:
   - **Graph name** and **Kernel names**
   - **Input/output ports** (type, width, window size)
   - **LUTs** (look-up tables)
3. Select generation options.
4. The wizard generates graph and kernel source files.

---

## Single Kernel Development

Key optimization techniques for AI Engine kernels:

| Technique | Description |
|---|---|
| **Vectorization** | Use SIMD vector operations for data parallelism |
| **Vector Registers** | Efficient use of AI Engine vector register files |
| **Memory Access** | Optimize data movement with aligned loads/stores |
| **Software Pipelining** | Overlap iterations of inner loops for throughput |

---

## Exporting Summary Tables

Export summary tables from the Analysis View to CSV format:

1. Open the Analysis View for the AI Engine component.
2. Navigate to the desired summary table.
3. Click the **Export to CSV** button.

---

## Best Practices

1. **Start with x86sim** — Use x86 simulation for initial functional verification before moving to `aiesimulator` for cycle-accurate analysis.
2. **Enable profiling early** — Use profiling to identify throughput and latency bottlenecks during development.
3. **Use Pipeline View** — Examine pipeline stages to find stalls and optimize kernel code.
4. **Vectorize kernels** — Leverage AI Engine SIMD instructions for maximum throughput.
5. **Export metrics** — Use Python CLI throughput/latency export functions for automated regression testing.
6. **Use templates** — Start with one of the 18 built-in examples to accelerate development.

---

## See Also

- [Chapter 2: Vitis Commands and Utilities](chapter2_vitis_commands_and_utilities.md) — `v++ -c --mode aie` compilation command
- [Chapter 3: Using the Vitis Unified IDE](chapter3_using_the_vitis_unified_ide.md) — System project integration with AI Engine components
- [Chapter 8: Working with the Analysis View](chapter8_working_with_the_analysis_view.md) — AI Engine compilation summary reports
- [Chapter 9: Additional Information](chapter9_additional_information.md) — Output directory structure for AI Engine builds
- *AI Engine Tools and Flows User Guide (UG1076)*
- *AI Engine Kernel and Graph Programming Guide (UG1079)*

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 5 (pp. 368–394)*
