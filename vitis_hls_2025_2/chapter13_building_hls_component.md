# Chapter 13: Building and Running an HLS Component

> Source: UG1399 (v2025.2) January 22, 2026 — Vitis HLS User Guide, Section III: Vitis HLS Flow Steps, pages 336–448.

---

## Table of Contents

1. [Overview](#overview)
2. [Creating an HLS Component](#creating-an-hls-component)
3. [Target Flow Overview](#target-flow-overview)
4. [Working with Sources](#working-with-sources)
5. [Adding RTL Blackbox Functions](#adding-rtl-blackbox-functions)
6. [Defining the HLS Config File](#defining-the-hls-config-file)
7. [Specifying the Clock Frequency](#specifying-the-clock-frequency)
8. [Adding Pragmas and Directives](#adding-pragmas-and-directives)
9. [Running C Simulation](#running-c-simulation)
10. [Writing a Test Bench](#writing-a-test-bench)
11. [Using Code Analyzer](#using-code-analyzer)
12. [Debugging the HLS Component](#debugging-the-hls-component)
13. [Running C Synthesis](#running-c-synthesis)
14. [Synthesis Summary Reports](#synthesis-summary-reports)
15. [Running C/RTL Co-Simulation](#running-crtl-co-simulation)
16. [Packaging the RTL Design](#packaging-the-rtl-design)
17. [Running Implementation](#running-implementation)
18. [Optimizing the HLS Project](#optimizing-the-hls-project)
19. [Best Practices Summary](#best-practices-summary)

---

## Overview

The AMD Vitis™ Unified IDE and `v++` common command line synthesize a C or C++ function into RTL code for implementation in the programmable logic (PL) region of AMD Versal™, Zynq™ MPSoC, or FPGA devices. An HLS component follows a **bottom-up** design flow.

### Output Types

| Output | Use |
|---|---|
| **Vivado IP** (`.zip`) | Integrated into hardware designs using Vivado + Embedded Software Development (UG1400) |
| **Vitis Kernel** (`.xo`) | Heterogeneous compute and Data Center acceleration (Alveo, UG1701) |

### Development Steps

1. Architect the C/C++ algorithm (Design Principles)
2. Verify source code logic with C simulation
3. Analyze parallelism with Code Analyzer
4. Generate RTL from source (C Synthesis)
5. Verify generated RTL contra C test bench (C/RTL Co-Simulation)
6. Analyze HLS synthesis and co-simulation reports
7. Iterate until performance goals are met

---

## Creating an HLS Component

### Wizard Steps (IDE)

| Step | Wizard Page | Key Inputs |
|---|---|---|
| 1 | **File → New Component → HLS** | Launch wizard |
| 2 | **Name and Location** | Component name and directory |
| 3 | **Configuration File** | Empty file / Existing file / Generate from `.hls.app` |
| 4 | **Source Files** | Design files, test bench files, CFLAGS, CSIMFLAGS, Top Function |
| 5 | **Select Part** | Part number or Platform |
| 6 | **Settings** | Clock period/frequency, clock uncertainty, `flow_target`, `package.output.format` |
| 7 | **Summary** | Review and Finish |

> **Tip:** Select **Platform** instead of Part → IDE extracting the part and adding `part=` to config automatically.

After creation the `vitis-comp.json` file opens in the central editor and the component becomes active in the Flow Navigator.

---

## Target Flow Overview

### Vivado IP Flow

Configured with `flow_target=vivado` (default). Generates RTL for Vivado Design Suite integration with maximum flexibility.

- Supports wide variety of interface specifications
- Default interfaces assigned per function argument (see *Interfaces for Vivado IP Flow*)
- Overridden with `INTERFACE` pragma or `set_directive_interface`

### Vitis Kernel Flow

Configured with `flow_target=vitis`. Generates RTL suitable for the Vitis development environment and Xilinx Runtime (XRT).

Default interfaces when no `INTERFACE` pragmas are present:

| Argument Type | Default Interface |
|---|---|
| Scalar arguments, control signals for arrays, return value | `s_axilite` (AXI4-Lite) |
| Pointer and array arguments | `m_axi` (AXI4 Master) |
| `hls::stream` data type | `axis` (AXI4-Stream) |

The tool automatically attempts to infer BURST transactions for `m_axi` arguments to maximize throughput/minimize latency.

### Default Configuration Comparison

| Configuration | Vivado | Vitis |
|---|---|---|
| `clock_uncertainty` | 27% | 27% |
| `syn.compile.pipeline_loops` | 64 | 64 |
| `syn.rtl.register_reset_num` | 0 | 3 |
| `syn.interface.m_axi_latency` | 0 | 64 |
| `syn.interface.m_axi_alignment_byte_size` | 1 | 64 |
| `syn.interface.m_axi_max_widen_bitwidth` | 0 | 512 |
| `syn.directive.interface` | IP mode | Kernel mode |
| `syn.interface.m_axi_offset` | slave | slave |

> **Important:** Selecting `flow_target=vitis` does **not** automatically change `package.output.format`. You must set that separately.

---

## Working with Sources

### C/C++ Language Support

- C and C++11/C++14 language constructs and native data types (including `float` and `double`)
- **Not supported:** dynamic memory allocation, OS operations (file read/write, time/date queries)
- Only **one** function allowed as top-level function for synthesis
- Sub-functions in the hierarchy under the top-level are also synthesized

### Using Libraries

Include by adding the header file; paths are automatically detected in the Vitis Unified IDE.

| Library | Purpose | Header Location |
|---|---|---|
| Arbitrary Precision Data Types | Smaller bit-width variables for area/performance improvements | `include/` |
| HLS Math Library | Standard math operations synthesizable to RTL | `include/` |
| HLS Stream Library | Streaming data structure modeling | `include/` |

### Vitis Libraries (External)

Available at https://github.com/Xilinx/Vitis_Libraries — math, statistics, linear algebra, DSP, Vision, Finance, Database. Downloaded and configured via the Libraries view in the IDE.

> **Caution:** Not available on Windows.

### Resolving References

- The IDE automatically indexes all header files and parses references continuously
- Left sidebar highlights unresolved references at the line number
- Right sidebar shows unresolved references relative to the entire file
- Fix by: saving the header file (new code), or ensuring the search path is set via `syn.cflags`

---

## Adding RTL Blackbox Functions

The RTL blackbox feature allows existing Verilog RTL IP to be used within an HLS project. The RTL IP can be used in sequential, pipeline, or dataflow regions.

> **Note:** Using RTL blackbox restricts output to Verilog only.

### Requirements

- Must be Verilog (`.v`) code
- Unique clock signal + unique active-High reset signal
- CE signal for enable/stall
- Block-level control: `ap_ctrl_chain` or `ap_ctrl_none`

### Limitations

- Supports C++ only (not C)
- Cannot connect to top-level interface I/O signals
- Cannot directly serve as the design-under-test (DUT)
- Does not support `struct` or `class` type interfaces

### Adding Steps

```bash
# 1. Call the C function signature from within the top-level function
# 2. Add the blackbox JSON description file:
add_files –blackbox my_file.json
# 3. Add the RTL IP files
# 4. Run HLS design flow as usual
```

### RTL Port Protocols for Blackbox

| Protocol | C Direction | Key JSON Attributes |
|---|---|---|
| `wire` | `in` | `data_read_in` |
| `ap_vld` | `out` | `data_write_out`, `data_write_valid` |
| `ap_ovld` | `inout` | `data_read_in`, `data_write_out`, `data_write_valid` |
| `FIFO` | `in`/`out` | `FIFO_empty_flag`, `FIFO_read_enable`, `FIFO_data_read_in` |
| `RAM` (1P) | `in`/`out`/`inout` | `RAM_address`, `RAM_clock_enable`, `RAM_data_read_in` |
| `RAM` (T2P) | `in`/`out`/`inout` | Same + `_snd` variants for second port |

### JSON File Format (Key Fields)

| JSON Attribute | Description |
|---|---|
| `c_function_name` | C++ function name for the blackbox |
| `rtl_top_module_name` | RTL module name (must match `c_function_name`) |
| `c_files[].c_file` | Path to the C simulation model |
| `c_files[].cflag` | Compile flags for the C model |
| `rtl_files[]` | RTL IP file paths |
| `c_parameters[].c_name` | Argument name |
| `c_parameters[].c_port_direction` | `in`, `out`, or `inout` |
| `c_parameters[].rtl_ports` | RTL signals mapping |
| `rtl_common_signal.module_clock` | Clock signal name |
| `rtl_common_signal.module_reset` | Reset signal name (active-High) |
| `rtl_common_signal.module_clock_enable` | CE signal name |
| `rtl_performance.latency` | Latency in cycles (0 = combinatorial) |
| `rtl_performance.II` | Initiation interval (0 = not pipelinable) |
| `rtl_resource_usage.{FF,LUT,BRAM,URAM,DSP}` | Resource numbers |

### RTL Blackbox Wizard

Right-click the project in Component Explorer → **RTL Blackbox Wizard**. Pages:
1. **C/C++ Files**: Add C functional model files and CFLAGS
2. **C File Wizard**: Specify C function name, argument names, types, directions, RAM types
3. **RTL IP Definition**: Add RTL files, set module name, performance (latency/II), resource usage
4. **RTL Common Signals**: Map `module_clock`, `module_reset`, `module_clock_enable`, `ap_ctrl_chain_*` signals
5. Click **Finish** → JSON file auto-generated

---

## Defining the HLS Config File

The HLS configuration file (`hls_config.cfg`) contains commands and settings for synthesis, simulation, and export.

Access via: **Config File** hyperlink in `vitis-comp.json` tab, or select the file in Component Explorer under **Settings**.

### Config File Sections

| Section | Config File Key prefix | Purpose |
|---|---|---|
| General | `part=`, `[hls]` entries | Part/platform, clock, `flow_target` |
| C Synthesis Sources | `syn.file=`, `syn.top=` | Source files and top function |
| Testbench Sources | `tb.file=`, `tb.cflags=` | Test bench files and flags |
| C Simulation | `csim.*` | Simulation configuration |
| C Synthesis Settings | `syn.*` | Global synthesis controls |
| C/RTL Cosimulation | `cosim.*` | Co-simulation configuration |
| Package | `package.*` | Export format and IP metadata |
| Implementation | `vivado.*` | Vivado synthesis/implementation settings |
| Design Directives | `syn.directive.*` | Optimization directives |

> **Tip:** The Config File Editor provides both form-based and text-based editing. Use the toggle icon to switch. Enable **File → AutoSave** or `Ctrl-S` to save changes.

---

## Specifying the Clock Frequency

- Single clock only (same for all functions in the design)
- Default: 10 ns clock period, 27% clock uncertainty

```ini
[HLS]
clock=8ns           # or clock=125MHz
clock_uncertainty=15%
```

> **Important:** If using `platform=` instead of `part=`, you must use `freqhz=` instead of `clock=`.

### Clock Period vs. Effective Period

$$\text{Effective Clock Period} = \text{Specified Clock Period} - \text{Clock Uncertainty}$$

The clock uncertainty provides margin for logic synthesis and P&R. If timing constraint cannot be met, the tool issues:

```
@W [SCHED-644] Max operation delay (<op_name> 2.39ns) exceeds the effective cycle time
```

> The tool still produces RTL even if timing constraints are not met. Always review the **Performance Estimates** section of the synthesis report.

### Clock Enable Port

Optionally add a clock-enable port `ap_ce` via `syn.interface.clock_enable` in the HLS config file.

---

## Adding Pragmas and Directives

### Pragma vs. Directive

| Format | Advantages | Disadvantages |
|---|---|---|
| **HLS Config File Directive** | Source unchanged; ideal for design exploration across multiple components | Config file must accompany any archived source |
| **Source Code Pragma** (`#pragma HLS`) | Embedded in source, no extra files needed; ideal for shipped C IP | Applied to every HLS component using that source |

### Conditional Control of Pragmas

```cpp
// Using preprocessor defines
#define OPT 2
#pragma HLS if (OPT==1) PIPELINE II=1
#pragma HLS if (OPT==2) UNROLL factor=16

// Using template parameters
template<int TripCount>
void dot_product(const int* a, const int* b, int& output) {
    DP: for (int i = 0; i < TripCount; ++i) {
        #pragma HLS if (TripCount > 20) pipeline II = 1
        #pragma HLS if (TripCount <=20) unroll
        output += a[i] * b[i];
    }
}
```

### Directive Scope Rules

- **Functions**: Applied to all objects within the function scope (does not propagate to sub-functions, unless `recursive` option used)
- **Interfaces**: Applied to the top-level function containing the interface
- **Loops**: Applied to all objects within the loop scope
- **Arrays**: Applied to the scope containing the array

### Global Variables

Global variables cannot be directly targeted — specify through a scope that uses the variable:
1. Open HLS Directive editor
2. Select the scope (function/loop/region) where the variable is used
3. Select **Add Directive** and edit the variable name to the global variable

### Using Constants and Macros in Pragmas

```cpp
// Constant integer
const int MY_DEPTH = 1024;
#pragma HLS stream variable=my_var depth=MY_DEPTH

// Macro with two levels (required for proper expansion)
#define PRAGMA_SUB(x) _Pragma (#x)
#define PRAGMA_HLS(x) PRAGMA_SUB(x)
#define STREAM_IN_DEPTH 8
PRAGMA_HLS(HLS stream depth=STREAM_IN_DEPTH variable=InStream)
```

### Failure to Satisfy Directives

When synthesis fails to meet an optimization target, the tool automatically relaxes it and reports:
- What performance level *can* be achieved
- Reasons why the target performance was not reached
- A design to analyze to understand bottlenecks

```
INFO: [SCHED 61] Pipelining result: Target II: 1, Final II: 4, Depth: 6.
```

---

## Running C Simulation

C simulation validates the C/C++ source code and test bench before generating RTL.

### Loading Test Bench Files

Configure in the **Testbench sources** section of Config Editor:

```ini
[HLS]
tb.file=../../src/in.dat
tb.file=../../src/out.golden.dat
tb.file=../../src/dct_test.cpp
tb.cflags=<cflag>
tb.file_cflags=../../src/dct_test.cpp,<cflag>
```

### Simulation Configuration

```ini
[HLS]
csim.clean=true       # Remove existing executables before compile
csim.O=true           # Optimizing compile (faster sim, no debug info)
csim.code_analyzer=0  # Enable Code Analyzer (0=off, 1=on)
csim.argv=arg1 arg2   # Arguments for test bench main()
```

### Running Simulation

Select **Run** under **C SIMULATION** in Flow Navigator. Uses `vitis-run --mode hls --csim`.

### Success / Failure Messages

```
# Successful run:
INFO: [SIM 211-1] CSim done with 0 errors.
INFO: [SIM 211-3] *************** CSIM finish ***************

# Failed run:
@E Simulation failed: Function 'main' returns nonzero value '1'.
ERROR: [SIM 211-100] 'csim_design' failed: nonzero return value.
```

### Output Directory Structure

```
<workspace>/<component>/<component>/hls/
└── csim/
    ├── build/        # Simulation executables, test bench I/O, csim.exe
    │   └── obj/      # Object files (.o) and dependency files (.d)
    └── report/       # Log file of C simulation build and run
```

### Sanitizers

```ini
csim.sanitize_address=true      # Detect undefined memory accesses
csim.sanitize_undefined=true    # Detect other undefined behaviors
```

Sanitizer output provides a stack trace — find the first entry pointing to your HLS project to identify the problem location.

---

## Writing a Test Bench

### Key Rules

- `main()` return value: **0 = pass**, **non-zero = fail**
- Must be **self-checking** — do not rely on interactive inputs
- Should run the top-level function **multiple times** to test different data values
- Multiple calls are also required to measure II in RTL simulation
- Constrain return value to **8-bit range** for portability

### Minimal Self-Checking Test Bench Pattern

```cpp
int main () {
    int ret = 0;
    
    // Call top-level function multiple times
    for (int i = 0; i < NUM_TRANS; i++) {
        top_func(input, output);
    }
    
    // Compare against golden results
    ret = system("diff --brief -w output.dat output.golden.dat");
    
    if (ret != 0) {
        printf("Test failed !!!\n");
        ret = 1;
    } else {
        printf("Test passed !\n");
    }
    
    return ret;  // 0 = pass, non-zero = fail
}
```

### Recommended Code Organization

```cpp
// hier_func.h — shared header with data types and function declaration
#ifndef _HIER_FUNC_H_
#define _HIER_FUNC_H_
#include <stdio.h>
#define NUM_TRANS 40
typedef int din_t;
typedef int dint_t;
typedef int dout_t;
void hier_func(din_t A, din_t B, dout_t *C, dout_t *D);
#endif

// hier_func.cpp — design source (not in test bench)
#include "hier_func.h"
void hier_func(din_t A, din_t B, dout_t *C, dout_t *D) {
    dint_t apb, amb;
    sumsub_func(&A, &B, &apb, &amb);
    shift_func(&apb, &amb, C, D);
}

// hier_func_test.cpp — test bench (tb.file=)
#include "hier_func.h"
int main() { /* ... */ return 0; }
```

### Design Files vs. Test Bench Files

- **Design files** (`syn.file=`): The top-level function and its sub-functions
- **Test bench files** (`tb.file=`): `main()`, any calling functions not in the DUT hierarchy, data files (`.dat`)

> If using a **single file** for both design and test bench, add it to **both** `syn.file=` and `tb.file=`.

---

## Using Code Analyzer

Code Analyzer provides pre-synthesis analysis of the design's dataflow and performance potential. Enable with `csim.code_analyzer=1` in the config file.

### Features

| Feature | Description |
|---|---|
| **Dataflow Graph Extraction** | Extracts a DFG from top-level statements even without `DATAFLOW` pragma |
| **Performance Metrics** | Estimates Transaction Interval (TI), throughput, channel data volume pre-synthesis |
| **Performance Guidance** | Identifies cyclic dependencies and memory port contention |
| **Graph Transformations** | Merge/split processes for what-if design space exploration |

### Use Cases

1. **Legality** — Detect R+W access violations, multiple producer/consumer violations, and feedback loops before synthesis
2. **Improve Performance** — Use heat map to find processes with TI bottlenecks; expand process code for detailed guidance
3. **Throughput Analysis** — Review channel widths and data volumes; validate with synthesis when possible

### Working with the Graph

- Drag and drop one process onto another to **merge** sequential processes
- Click the **SPLIT** line to split merged processes back
- Right-click any process → **Goto Source** to view the corresponding source code
- Right-click selected code → **Refactor** to restructure into dataflow form

> **Important:** Changes made in Code Analyzer are for analysis only — they must be manually re-implemented in the original source code.

---

## Debugging the HLS Component

Select **Debug** from Flow Navigator to launch the C simulation debugger.

### Debug View Widgets

| Widget | Description |
|---|---|
| **Control Panel** | Continue, Step Over, Step Into, Step Out, Restart, Stop |
| **Threads** | Active debugging threads; switch between threads |
| **Call Stack** | Function call stack updated during execution |
| **Variables** | Current values of global and local variables; supports **Set Value** |
| **Watch** | Monitor specific expressions; add with `+` command |
| **Breakpoints** | Click left of line number for a breakpoint; right-click for conditional or logpoint |
| **Debug Console** | Transcript of debug process and application messages |

---

## Running C Synthesis

Select **Run** under **C SYNTHESIS** in the Flow Navigator. Uses `v++ -c --mode hls`.

### Key Config File Entries

```ini
part=xcvc1902-vsva2197-2MP-e-S
[hls]
flow_target=vitis        # or vivado
clock=8ns
clock_uncertainty=15%
syn.file=<path/to/file.cpp>
syn.top=<top_function_name>
syn.cflags=<cflag_for_all>
syn.file_cflags=<path>,<cflag>
```

### Directive Examples

```ini
[HLS]
syn.directive.dataflow=dct
syn.directive.array_partition=dct buf_2d_in type=block factor=4
syn.directive.pipeline=dct2d II=4
```

### Improving Synthesis Runtime

- **Avoid over-unrolling/partitioning**: These create more objects to schedule, increasing runtime
- Capture unrolled loop body as a **separate function** to schedule once instead of N copies
- Use **LATENCY constraints** on loops/functions/regions to reduce search space:

```cpp
#pragma HLS LATENCY min=4 max=4  // Same min/max reduces freedom, speeds synthesis
```

### Output Directory Structure

```
<workspace>/<component>/<component>/hls/
└── syn/
    ├── verilog/   # Verilog RTL files (top + sub-functions)
    ├── vhdl/      # VHDL RTL files
    └── report/    # Reports for top-level function and sub-functions
```

> **Important:** Do not use `syn/verilog` or `syn/vhdl` directly in Vivado. Use the **packaged IP output** (`impl/ip`) instead.

---

## Synthesis Summary Reports

### Report Sections

| Report Section | Content |
|---|---|
| **General Information** | Software version, project/solution name, technology details |
| **Timing Estimate** | Target clock, uncertainty, and estimated effective clock period |
| **Performance & Resource Estimates** | Timing slack, latency (cycles + ns), II, trip count, BRAM/DSP/FF/LUT estimates |
| **HW Interfaces** | Tables for each interface type (M_AXI, S_AXILITE, FIFO, etc.) |
| **SW I/O Information** | Mapping from SW arguments to HW port names |
| **M_AXI Burst Information** | Burst Summary (successful) and Burst Missed (with failure reasons) |
| **Pragma Report** | All pragmas: valid / ignored / inferred |
| **Bind Op Report** | Operation-to-resource mappings; auto vs. pragma-specified |
| **Bind Storage Report** | Array-to-memory mappings (BRAM/URAM/LUTRAM); auto vs. pragma-specified |

### Performance Column Definitions

| Column | Meaning |
|---|---|
| **Slack** | Timing slack (negative = timing violation) |
| **Latency** | Cycles (and nanoseconds) to produce all outputs |
| **Iteration Latency** | Cycles per single loop iteration |
| **II** | Initiation Interval — cycles before new inputs can be applied |
| **Trip Count** | Loop iterations implemented in hardware |

> **Tip:** When **Latency** shows `?`, the tool cannot determine loop iteration count. Use `LOOP_TRIPCOUNT` pragma to specify it (affects reports only, not synthesis results).

### Function Call Graph

Available after C Synthesis and after C/RTL Co-simulation:
- Displays full hierarchy with latency and II per function/loop
- Heat Map modes: II (min/max/avg), Latency (min/max/avg), Resource Utilization, Stall Time %
- Red = highest value (worst); Green = lowest value (best)
- Right-click any module → Open Schedule Viewer, Synthesis Summary, Dataflow Viewer, or source

### Schedule Viewer

Shows operations and control steps in clock cycle order:

| Visual Element | Meaning |
|---|---|
| Gray box | Operation; size = delay as percentage of clock period |
| Horizontal line through gray box | Multi-cycle operation |
| Vertical dashed line | Clock uncertainty reserve (left for P&R) |
| Solid blue arrow | Operator data dependency |
| Green dotted line | Inter-iteration data dependency |
| Golden line | Memory dependency |
| Red box | Timing violation |

> **Loop bar**: Pipelined loops shown unrolled; II marked with thick boundary on loop bar.

### Dataflow Viewer

Only available when `DATAFLOW` pragma is used. Shows processes and producer-consumer connections.

Key requirements:
- Must run `cosim.enable_dataflow_profiling=true` to capture full performance data
- Test bench must run **at least two iterations** of the top-level function for II reporting

Features:
- Channel Profiling (FIFO sizes), Read/Write Blocking percentages, Stalling Time
- Deadlock detection highlights: problematic channels in red (full), empty channels in white
- Cross-probing from graph to source code

---

## Running C/RTL Co-Simulation

Select **Run** under **C/RTL COSIMULATION** in Flow Navigator. Uses `vitis-run --mode hls --cosim`.

> **Important:** Random input test vectors (e.g., `std::random_device`) are **not supported** in co-simulation.

### Co-simulation Config

```ini
[HLS]
cosim.trace_level=port     # all | port | port_hier | none
cosim.wave_debug=true      # Launch Vivado GUI for waveform viewing (xsim only)
cosim.enable_dataflow_profiling=true
cosim.disable_deadlock_detection=false
cosim.random_stall=true    # Randomize stall injection per transfer
```

### Co-simulation Requirements

At least one must be true:
- Top-level uses `ap_ctrl_chain` or `ap_ctrl_hs` block control protocol
- Design is purely combinational
- Top-level has II = 1
- All interfaces use `axis` or `ap_hs` with streaming arrays

### 3-Phase Verification Process

```
Phase 1: C Simulation → saves input vectors (TV In .dat)
Phase 2: RTL Simulation using saved input vectors → saves output vectors (TV Out .dat)
Phase 3: Output vectors fed back to C test bench for checking → returns PASS/FAIL
```

### Deadlock Detection

Deadlock = two or more DATAFLOW processes blocking each other via FIFO or mixed PIPO/FIFO channels.

```
ERROR!!! DEADLOCK DETECTED at 1292000 ns! SIMULATION WILL BE STOPPED!
...
// (1): Process: ..proc_1_U0    Channel: ..data_channel1_U, FULL
// (2): Process: ..proc_2_U0    Channel: ..data_array_U, EMPTY
```

- Dataflow Viewer opens automatically showing the deadlock
- Red = FULL channels; White = EMPTY channels
- Fix by increasing FIFO depth (`STREAM` pragma or `syn.dataflow.fifo_depth`)
- Disable with: `cosim.disable_deadlock_detection=true`

### Timeline Trace Viewer

Available after co-simulation. Shows runtime profile of all sub-functions with:
- Start/end times for each dataflow function iteration
- FIFO/PIPO full/empty markers with stall percentages
- Enable with: `cosim.trace_level=all` + `cosim.enable_dataflow_profiling=true`

### Viewing Waveforms

```ini
cosim.tool=xsim          # Use Vivado simulator
cosim.trace_level=port   # or all
```

The Vivado simulator GUI opens and shows all RTL processes with activity timeline.

### Troubleshooting Co-Simulation Failures

| Category | Common Issues and Solutions |
|---|---|
| **Environment** | Third-party simulator not in PATH; missing compiled simulation libraries; `cd` command in `.bashrc` |
| **Optimization Directives** | `DEPENDENCE` directive incorrect; `volatile` pointer missing `DEPTH` option; FIFO too small |
| **Test Bench / Source** | Test bench not returning 0 on pass; random number seed not fixed; out-of-bounds array access; floating-point exact comparison; using `hls::stream` with decimation/interpolation |

---

## Packaging the RTL Design

Select **Package** in Flow Navigator. Uses `vitis-run --mode hls --package`.

### Package Output Formats

```ini
package.output.format=ip_catalog  # .zip for Vivado IP catalog (default)
package.output.format=xo          # .xo for Vitis development flow
package.output.format=sysgen      # .zip for System Generator
package.output.format=rtl         # Verilog/VHDL only, no packaging

package.output.file=../../<filename>
package.output.syn=false          # Skip packaging during synthesis iterations
```

### IP Configuration (ip_catalog only)

```ini
package.ip.vendor=xilinx.com
package.ip.library=hls
package.ip.name=<component_name>
package.ip.version=1.0
package.ip.description=An IP generated by HLS component
```

### Output Files

```
impl/
├── ip/           # Unzipped IP contents (use this, not verilog/vhdl directly)
│   ├── example/  # Tcl and shell scripts to generate/export the IP
│   └── drivers/  # C driver files for AXI4-Lite interfaces
├── report/        # Synthesis or P&R report
├── verilog/       # Raw RTL — do not use directly
└── vhdl/          # Raw RTL — do not use directly
<component>.zip    # IP archive for Vivado IP catalog
<component>.xo     # Compiled kernel for Vitis v++ --link
```

> **Important:** Always use `impl/ip` (packaged IP), never `impl/verilog` or `impl/vhdl` directly, because floating-point designs include IP catalog references that must be resolved.

---

## Running Implementation

Select **Run** under **IMPLEMENTATION** in Flow Navigator. Uses `vitis-run --mode hls --impl`.

Runs Vivado synthesis and/or place & route on the generated RTL, providing better timing and resource estimates than HLS synthesis alone.

### Implementation Config

```ini
[HLS]
vivado.flow=syn            # syn (default, faster) or impl (full P&R)
vivado.rtl=verilog         # RTL language (default: Verilog)
vivado.clock=8ns           # Override default clock
vivado.optimization_level=0
vivado.synth_strategy=<strategy>
vivado.impl_strategy=<strategy>
vivado.max_timing_paths=10
vivado.phys_opt=none       # none | place | route | all
vivado.report_level=failfast
```

### Implementation Report Sections

| Section | Content |
|---|---|
| **General Information** | Design and implementation details |
| **Run Constraints and Options** | All constraints set for synthesis/P&R run |
| **Resource Usage / Final Timing** | Quick summary of resources and timing |
| **Resources** | Per-module resource breakdown with source code correlation |
| **Fail Fast** | Checks with REVIEW status to investigate |
| **Timing Paths** | Top N worst negative slack paths with logic levels and fanout |

> **Tip:** If logic levels increased from RTL Synthesis to P&R, congestion is the likely cause — refactor source code or change BRAM/LUTRAM/URAM choices.

---

## Optimizing the HLS Project

After analysis, apply optimizations using:
- **HLS Pragmas** — embedded in source code
- **HLS Config File Commands** — as `syn.directive.*` entries

See *Section II: HLS Programmers Guide* (Ch1–Ch11) and *HLS Config File Commands* (Ch16) for full optimization catalog.

### Cloning HLS Components

Right-click a component in the Vitis Component Explorer → **Clone Component**.

- Cloned component inherits all source files, test bench files, top function, and config file settings
- Modify the clone for exploration while preserving the original
- Enables A/B comparison of different optimization strategies

### Component Comparison

View → **HLS Compare Reports** (or hover over a component and select the compare icon).

- Compare multiple HLS components for Performance and Resource Utilization
- Tabular and Graphical formats available
- Export as CSV

Requirements: at least one completed stage (C Synthesis, Co-simulation, or Implementation) per component.

### L1 Library Wizard (Vitis Accelerated Libraries)

Three flows to access pre-built L1 HLS functions:

| Flow | Access Method | Output |
|---|---|---|
| **Flow 1 — Examples** | Examples icon → HLS Examples → Vitis Accelerated Libraries | Full HLS component with test bench |
| **Flow 2 — Create from Library** | Welcome page → Create Component from Library | HLS component with wrapper, no test bench |
| **Flow 3 — Auto-completion** | Type `xf::` in IDE editor | Parametrized function inserted into source |

> **Prerequisite:** Solver and Vision subfolders of Vitis Libraries must be downloaded. OpenCV v4.4.0 required for Vision library.

---

## Best Practices Summary

| Practice | Recommendation |
|---|---|
| **Test bench** | Write self-checking, data-file-based; multiple transactions; non-random seeds |
| **Verification order** | C Simulation → C Synthesis → Co-Simulation; never skip steps |
| **Timing margin** | Increase `clock_uncertainty` if there is high device utilization |
| **Directives vs. pragmas** | Use directives during exploration; convert to pragmas when finalized |
| **Synthesis runtime** | Avoid blanket array partition / loop unroll / inline all; add LATENCY constraints |
| **RTL output** | Always package via `vitis-run --package`; never use `syn/verilog` directly |
| **FIFO deadlock** | Run co-sim with `enable_dataflow_profiling=true`; size FIFOs to max producer output |
| **Component exploration** | Clone components to preserve working implementations while experimenting |
| **Float RTL sim** | Compile simulation libraries for third-party simulators via `compile_simlib` in Vivado Tcl |
| **Co-sim requirements** | AP ctrl protocol or II=1 or combinational or all-streaming interfaces required |

---

### See Also

- [Chapter 12 — Launching the Vitis Unified IDE](ch12_launching_vitis_ide.md) — IDE startup and workspace setup
- [Chapter 14 — HLS Command Line](ch14_hls_command_line.md) — Command-line equivalents of all IDE operations
- [Chapter 16 — HLS Config File Commands](../section04_vitis_hls_command_reference/ch16_config_file_commands.md) — All `syn.*`, `csim.*`, `cosim.*`, `vivado.*` settings
- [Chapter 17 — HLS Pragmas](../section04_vitis_hls_command_reference/ch17_hls_pragmas.md) — Pragma reference for optimization directives

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 13: Building and Running an HLS Component, Pages 336–448.*
