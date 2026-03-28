# Chapter 16 — HLS Config File Commands
**Section IV: Vitis HLS Command Reference · UG1399 v2025.2, Pages 457–540**

---

## Table of Contents
1. [Overview and Config File Structure](#1-overview-and-config-file-structure)
2. [Global Options (Outside [hls])](#2-global-options-outside-hls)
3. [HLS General Options](#3-hls-general-options)
4. [C-Synthesis Sources](#4-c-synthesis-sources)
5. [Test Bench Sources](#5-test-bench-sources)
6. [Array Partition Configuration](#6-array-partition-configuration)
7. [C-Simulation Configuration](#7-c-simulation-configuration)
8. [Co-Simulation Configuration](#8-co-simulation-configuration)
9. [Compile Options](#9-compile-options)
10. [Dataflow Configuration](#10-dataflow-configuration)
11. [Debug Options](#11-debug-options)
12. [Interface Configuration](#12-interface-configuration)
13. [Package Options](#13-package-options)
14. [Operator Configuration](#14-operator-configuration)
15. [RTL Configuration](#15-rtl-configuration)
16. [Schedule Settings](#16-schedule-settings)
17. [Storage Configuration](#17-storage-configuration)
18. [Vivado Implementation Settings](#18-vivado-implementation-settings)
19. [Unroll Settings](#19-unroll-settings)
20. [HLS Optimization Directives (`syn.directive.*`)](#20-hls-optimization-directives-syndirecive)
21. [Best Practices](#21-best-practices)

---

## 1. Overview and Config File Structure

The HLS config file is the primary mechanism for feeding options to the `v++` compiler in HLS mode. All HLS-specific settings belong under a `[hls]` section header.

```ini
part=xcvu11p-flga2577-1-e          # Global v++ option — NOT under [hls]

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
v++ -c --mode hls --config myconfig.cfg
```

> **Key rule:** Options under `[hls]` are HLS-specific. Options like `--part`, `--platform`, and `--freqhz` are global `v++` options and should NOT be under `[hls]`.

---

## 2. Global Options (Outside [hls])

These options appear outside any section header in the config file — they are standard `v++` options:

| Option | Description |
|---|---|
| `--platform <path>` | Path to platform specification (`.xpfm`) or hardware spec (`.xsa`) |
| `--freqhz <arg>` | Clock frequency in Hz (required when using `platform=` instead of `part=`) |
| `--part <arg>` | Target device part number |

> **Important:** When using `platform=` instead of `part=`, you must use `freqhz=` (not `clock=`) to override the platform clock.

---

## 3. HLS General Options

> All options below go under the `[hls]` header.

| Option | Default | Description |
|---|---|---|
| `clock=<value>` | `10ns` | Clock period in ns or MHz. Default 10 ns. E.g., `clock=8ns` or `clock=125MHz` |
| `clock_uncertainty=<value>` | 27% | Clock uncertainty margin subtracted from period. Units: ns, MHz, or %. E.g., `clock_uncertainty=15%` |
| `flow_target=<vitis\|vivado>` | — | Target flow: `vitis` (Application Acceleration kernel `.xo`) or `vivado` (embedded IP `.zip`) |
| `relative_roots=<paths>` | — | Ordered list of absolute paths used to resolve relative file paths (semicolon-separated). Special prefixes: `file:`, `cwd:` |

**Example `relative_roots`:**
```ini
[hls]
relative_roots=/tmp/aaa ; /tmp/bbb ; file/../ccc ; cwd
syn.file=top.cpp
```

---

## 4. C-Synthesis Sources

| Option | Description |
|---|---|
| `syn.file=<path>` | Source file for synthesis. One `syn.file` per file. |
| `syn.top=<funcname>` | Name of the top-level function. Required if multiple functions exist. |
| `syn.cflags=<flags>` | Compilation flags for all `syn.file` sources (synthesis). E.g., `syn.cflags=-I../../src/` |
| `syn.csimflags=<flags>` | Compilation flags applied to all `syn.file` sources during C/RTL co-simulation. |
| `syn.file_cflags=<file>,<flags>` | Per-file syntax compilation flag for synthesis: `syn.file_cflags=../../src/dct.cpp,-I../../src/` |
| `syn.file_csimflags=<file>,<flags>` | Per-file simulation compilation flag: `syn.file_csimflags=../../src/dct.cpp,-Wno-unknown-pragmas` |
| `syn.blackbox.file=<path>` | JSON file for an RTL blackbox used during synthesis and co-simulation. |

---

## 5. Test Bench Sources

| Option | Description |
|---|---|
| `tb.file=<path>` | Test bench source file (not synthesized). One per file. |
| `tb.cflags=<flags>` | Compilation flags for all `tb.file` sources. |
| `tb.file_cflags=<file>,<flags>` | Per-file compilation flags for a test bench source. |

---

## 6. Array Partition Configuration

These settings apply globally; override per-array with `syn.directive.array_partition`.

| Option | Default | Description |
|---|---|---|
| `syn.array_partition.complete_threshold=<N>` | — | Arrays with ≤ N elements are automatically fully partitioned into registers. |
| `syn.array_partition.throughput_driven=<auto\|off>` | `auto` | `auto`: smart area/throughput tradeoff. `off`: disable auto partitioning. |

---

## 7. C-Simulation Configuration

| Option | Default | Description |
|---|---|---|
| `csim.O=<true\|false>` | `false` | Enable optimized compilation (faster runtime, but disables debug constructs). |
| `csim.argv=<args>` | — | Arguments passed to `main()` in the C test bench. |
| `csim.clean=<true\|false>` | `false` | Force clean rebuild (disables incremental compilation). |
| `csim.profile_tripcount=<true\|false>` | `false` | Enable trip-count profiling during C simulation. |
| `csim.ldflags=<flags>` | — | Linker options for simulation (library paths, etc.). |
| `csim.mflags=<flags>` | — | Compiler options for C simulation. |
| `csim.setup=<true\|false>` | `false` | Create simulation binary only; do not run simulation. |

---

## 8. Co-Simulation Configuration

| Option | Default | Description |
|---|---|---|
| `cosim.argv=<args>` | — | Arguments for the test bench `main()`. |
| `cosim.rtl=<verilog\|vhdl>` | `verilog` | RTL language for co-simulation. |
| `cosim.tool=<simulator>` | `xsim` | HDL simulator: `auto`, `vcs`, `modelsim`, `riviera`, `ncsim`, `xceilum`, `xsim`. |
| `cosim.trace_level=<level>` | `none` | Waveform trace: `none`, `port`, `port_hier`, `all`. |
| `cosim.wave_debug=<true>` | `false` | Open Vivado simulator GUI for waveform viewing (requires `cosim.tool=xsim`). |
| `cosim.setup=<true\|false>` | `false` | Create simulation binary only; don't execute simulation. |
| `cosim.clean=<true\|false>` | `false` | Force clean rebuild. |
| `cosim.coverage=<true\|false>` | `false` | Enable VCS coverage. |
| `cosim.disable_deadlock_detection=<true>` | — | Disable deadlock detection during co-simulation. |
| `cosim.disable_dependency_check=<true>` | — | Disable dependency checks. |
| `cosim.enable_dataflow_profiling=<true>` | — | Track dataflow channel sizes during co-simulation. |
| `cosim.enable_fifo_sizing=<true>` | — | Auto-tune FIFO depths using co-simulation profiling. |
| `cosim.enable_tasks_with_m_axi=<true>` | — | Enable `hls::task` with stable `m_axi` interfaces. |
| `cosim.random_stall=<true>` | `false` | Enable random stalling of top-level interfaces. |
| `cosim.stable_axilite_update=<true>` | — | Allow `s_axilite` to update stable registers on successive transactions. |
| `cosim.user_stall=<path>` | — | JSON stall file for co-simulation (generated via `cosim_stall`). |
| `cosim.hwemu_trace_dir=<path>` | — | Location of hardware emulation test vectors for co-simulation replay. |
| `cosim.ldflags=<flags>` | — | Linker flags for co-simulation. |
| `cosim.mflags=<flags>` | — | Compiler flags for co-simulation. |
| `cosim.compiled_library_dir=<path>` | — | Pre-compiled library directory for third-party simulators. |
| `cosim.disable_binary_tv=<true>` | — | Use plain text (not compressed binary) test vector files. |

---

## 9. Compile Options

| Option | Default | Description |
|---|---|---|
| `syn.compile.pipeline_loops=<N>` | `64` | Auto-pipeline loops with trip count ≥ N. Set `0` to disable auto-pipelining. |
| `syn.compile.pipeline_style=<stp\|flp\|frp>` | `frp` | Default pipeline style (preference, not hard constraint). `stp`=stall, `flp`=flushable, `frp`=free-running. |
| `syn.compile.pipeline_flush_in_task=<always\|never\|ii1>` | `ii1` | Controls pipeline flushing in `hls::task`. `ii1`=flush II=1 pipelines only. |
| `syn.compile.enable_auto_rewind=<0\|1>` | `1` | Enable automatic loop rewind for pipelined loops. |
| `syn.compile.unsafe_math_optimizations=<0\|1>` | `0` | Enable associative float ops and ignore signed zeros (may cause co-sim mismatch). |
| `syn.compile.no_signed_zeros=<0\|1>` | `0` | Ignore float zero sign for aggressive optimization. |
| `syn.compile.pragma_strict_mode=<0\|1>` | `0` | Promote unrecognized pragma warnings to errors. |
| `syn.compile.name_max_length=<N>` | `256` | Maximum length of function names before truncation. |
| `syn.compile.design_size_maximum_warning=<N>` | — | Threshold for slow-compilation/poor-QoR warnings. |
| `syn.compile.ignore_long_run_time=<0\|1>` | `0` | Suppress long-runtime warnings. |
| `syn.compile.performance_budgeter=<auto\|enable\|disable>` | `auto` | Controls design-wide performance analysis for the PERFORMANCE pragma. |
| `syn.compile_use_csim_directives=<true\|false>` | `false` | Apply C-simulation generated directives during synthesis. |

---

## 10. Dataflow Configuration

| Option | Default | Description |
|---|---|---|
| `syn.dataflow.default_channel=<fifo\|pingpong>` | `pingpong` | Default memory channel type for dataflow regions. Use `fifo` for streaming access patterns. |
| `syn.dataflow.fifo_depth=<N>` | Auto | Default FIFO depth. Overrides the auto-computed depth. Use with caution. |
| `syn.dataflow.override_user_fifo_depth=<N>` | — | Override ALL `hls::stream` depths (useful for deadlock diagnosis with large N). |
| `syn.dataflow.scalar_fifo_depth=<N>` | 2 | Minimum depth for scalar propagation FIFOs. Rule of thumb: avg starts of producing process before consumer starts. |
| `syn.dataflow.start_fifo_depth=<N>` | 2 | Minimum depth for start propagation FIFOs (ap_start handshake forwarding). |
| `syn.dataflow.task_level_fifo_depth=<N>` | — | Default FIFO depth for intra-task scalar FIFOs (synchronized like PIPO). |
| `syn.dataflow.strict_mode=<error\|warning\|off>` | `warning` | Severity for violations of canonical dataflow form. |
| `syn.dataflow.strict_stable_sync=<0\|1>` | `0` | Force synchronization of stable ports with `ap_done`. |
| `syn.dataflow.disable_fifo_sizing_opt=<0\|1>` | `0` | Disable FIFO depth optimization (can improve performance, reduce deadlocks). |

---

## 11. Debug Options

| Option | Default | Description |
|---|---|---|
| `syn.debug.enable=<0\|1>` | `0` | Enable debug file generation (needed for application-level debugging). Corresponds to `v++ -c -g`. |
| `syn.debug.directory=<path>` | `hls/.debug` | Output directory for debug files. |

---

## 12. Interface Configuration

### M_AXI Interface Options

| Option | Vitis Default | Vivado Default | Description |
|---|---|---|---|
| `syn.interface.m_axi_addr64=<0\|1>` | `1` | Enable 64-bit addressing for all `m_axi` ports. |
| `syn.interface.m_axi_alignment_byte_size=<N>` | `64` | `1` | Alignment for auto port widening. |
| `syn.interface.m_axi_max_widen_bitwidth=<N>` | `512` | `0` (off) | Auto port width resizing target (power of 2, 8–1024). |
| `syn.interface.m_axi_max_bitwidth=<N>` | `1024` | — | Maximum data channel bitwidth. |
| `syn.interface.m_axi_min_bitwidth=<N>` | `8` | — | Minimum data channel bitwidth. |
| `syn.interface.m_axi_max_read_burst_length=<N>` | `16` | — | Max data values per read burst. |
| `syn.interface.m_axi_max_write_burst_length=<N>` | `16` | — | Max data values per write burst. |
| `syn.interface.m_axi_num_read_outstanding=<N>` | `16` | — | Outstanding read requests before stall. FIFO size = N × burst_len × word_size. |
| `syn.interface.m_axi_num_write_outstanding=<N>` | `16` | — | Outstanding write requests before stall. |
| `syn.interface.m_axi_latency=<N>` | `64` (Vitis) | 0 | Expected M_AXI bus latency. Initiates requests N cycles early. |
| `syn.interface.m_axi_offset=<slave\|direct\|off>` | `slave` | — | Base address source: `slave`=AXI-Lite reg, `direct`=scalar port, `off`=none. |
| `syn.interface.m_axi_buffer_impl=<auto\|lutram\|bram\|uram>` | `bram` | — | Resource for M_AXI adapter internal buffers. |
| `syn.interface.m_axi_cache_impl=<auto\|lutram\|bram\|uram>` | `auto` | — | Resource for M_AXI adapter cache. |
| `syn.interface.m_axi_conservative_mode=<0\|1>` | `1` | — | Wait for full write data before issuing request (prevents deadlock). |
| `syn.interface.m_axi_flush_mode=<0\|1>` | `0` | — | Allow adapter to flush (write garbage) when burst is interrupted. |
| `syn.interface.m_axi_auto_id_channel=<0\|1>` | `0` | — | Auto-assign channel IDs for M_AXI interfaces. |
| `syn.interface.m_axi_auto_max_ports=<0\|1>` | `0` | — | Create separate M_AXI adapters per argument (vs. bundling). |

### S_AXILITE Interface Options

| Option | Default | Description |
|---|---|---|
| `syn.interface.s_axilite_data64=<0\|1>` | `0` | Enable 64-bit data width for the S_AXILITE interface. |
| `syn.interface.s_axilite_interrupt_mode=<cor\|tow>` | `tow` | Interrupt mode: `cor`=Clear-on-Read (1 txn), `tow`=Toggle-on-Write (2 txns). |
| `syn.interface.s_axilite_mailbox=<in\|out\|both\|none>` | `none` | Mailbox for non-stream, non-stable arguments (for auto-restart). |
| `syn.interface.s_axilite_status_regs=<ecc\|off>` | `off` | Expose ECC error bits via COR counters in the S_AXILITE register file. |
| `syn.interface.s_axilite_sw_reset=<0\|1>` | `0` | Enable software reset port in S_AXILITE adapter. |

### General Interface Options

| Option | Default | Description |
|---|---|---|
| `syn.interface.clock_enable=<0\|1>` | `0` | Add `ap_ce` clock-enable port (active-Low disables all sequential ops). |
| `syn.interface.default_slave_interface=<s_axilite\|none>` | `s_axilite` | Default slave interface for the design. |
| `syn.interface.register_io=<off\|scalar_in\|scalar_out\|scalar_all>` | `off` | Register scalar I/O ports globally. |

---

## 13. Package Options

### Output Options

| Option | Description |
|---|---|
| `package.output.file=<path>` | Output file path and name. Defaults to the HLS component name. |
| `package.output.format=<format>` | Export format: `ip_catalog`, `xo`, `syn_dcp`, `sysgen`, `rtl` |
| `package.output.syn=<true>` | Run Package step as part of C synthesis. |

**Output Formats:**

| Format | Description |
|---|---|
| `ip_catalog` | Vivado IP catalog entry (`.zip`) |
| `xo` | Vitis kernel object (`.xo`) for Application Acceleration flow |
| `syn_dcp` | Synthesized checkpoint (runs RTL synthesis in Vivado) |
| `sysgen` | System Generator compatible IP archive |
| `rtl` | Raw RTL output only (for development/debug) |

### IP Options (VLNV Identification)

| Option | Description |
|---|---|
| `package.ip.vendor=<name>` | VLNV Vendor field |
| `package.ip.library=<name>` | VLNV Library field |
| `package.ip.name=<name>` | VLNV Name field |
| `package.ip.version=<ver>` | VLNV Version field (e.g., `2.3`) |
| `package.ip.display_name=<name>` | Display name in the IP catalog |
| `package.ip.description=<text>` | Description text for the IP catalog entry |
| `package.ip.taxonomy=<category>` | IP taxonomy category (e.g., `video`) |
| `package.ip.xdc_file=<path>` | XDC constraints file included in the packaged IP |
| `package.ip.xdc_ooc_file=<path>` | Out-of-context XDC file for Vivado synthesis of the IP |

---

## 14. Operator Configuration

The `syn.op` command configures the default implementation, latency, and precision for arithmetic operators globally. Per-variable overrides: use `syn.directive.bind_op`.

```ini
syn.op=op:mul impl:dsp
syn.op=op:add impl:fabric latency:6
syn.op=op:fmacc precision:high
```

### Supported Operators

| Category | Operators |
|---|---|
| Integer | `mul`, `add`, `sub` |
| Single-precision float | `fadd`, `fsub`, `fmul`, `fdiv`, `fexp`, `flog`, `fsqrt`, `frsqrt`, `frecip`, `facc`, `fmacc`, `fmadd` |
| Double-precision float | `dadd`, `dsub`, `dmul`, `ddiv`, `dexp`, `dlog`, `dsqrt`, `drsqrt`, `drecip` |
| Half-precision float | `hadd`, `hsub`, `hmul`, `hdiv`, `hsqrt` |

### `impl` Values

| Value | Description |
|---|---|
| `all` (default) | Let tool choose |
| `dsp` | Use DSP resources |
| `fabric` | Use LUT-based fabric |
| `meddsp` | FP IP Medium DSP usage |
| `fulldsp` | FP IP Full DSP usage |
| `maxdsp` | FP IP Maximum DSP usage |
| `primitivedsp` | FP IP Primitive DSP usage |
| `auto` | Infer combined `facc\|fmacc\|fmadd` ops |
| `none` | Disable inference of combined ops |

### `precision` Values (for `facc`, `fmacc`, `fmadd`)

| Value | Notes |
|---|---|
| `standard` (default) | True float accumulator; II=1 on Versal, II=3–5 on others |
| `low` | Integer accumulator (fast); may cause co-sim mismatch |
| `high` | Extra precision bit fused multiply-add; Versal only; may cause co-sim mismatch |

---

## 15. RTL Configuration

| Option | Default | Description |
|---|---|---|
| `syn.rtl.reset=<none\|control\|state\|all>` | `control` | Reset scope: `none`, `control` (FSM/protocol regs), `state` (+ static/global vars), `all` (all regs). |
| `syn.rtl.reset_async=<0\|1>` | `0` | Use asynchronous reset (default: synchronous). |
| `syn.rtl.reset_level=<high\|low>` | `high` | Reset polarity. AXI requires active-Low; tool warns if high is chosen with AXI. |
| `syn.rtl.fsm_encoding=<auto\|gray\|johnson\|one_hot\|sequential\|none>` | `auto` | RTL FSM encoding attribute passed to Vivado synthesis. |
| `syn.rtl.fsm_safe_state=<auto_safe_state\|default_state\|power_on_state\|reset_state\|none>` | `none` | RTL FSM safe-state attribute (Hamming-3 encoding with `auto_safe_state`). |
| `syn.rtl.module_auto_prefix=<0\|1>` | `1` | Use top-level function name as prefix for all generated RTL modules. |
| `syn.rtl.module_prefix=<name>` | — | Override the default module name prefix. |
| `syn.rtl.header=<path>` | — | File whose contents are prepended to every generated RTL file. |
| `syn.rtl.register_all_io=<0\|1>` | `0` | Register all I/O signals by default. |
| `syn.rtl.register_reset_num=<N>` | — | Number of pipeline registers on the reset signal. |
| `syn.rtl.mult_keep_attribute=<0\|1>` | `0` | Add `keep` attribute to multiplier outputs. |
| `syn.rtl.deadlock_detection=<none\|sim\|hw>` | `sim` | `sim`=simulation-only, `hw`=adds deadlock ports (`ap_local_deadlock`, `ap_local_block`) to RTL. |
| `syn.rtl.deadlock_diagnosis=<0\|1>` | `0` | Enable deadlock diagnosis for Vitis kernels during hardware emulation. |
| `syn.rtl.cosim_trace_generation=<0\|1>` | `0` | Generate test vectors during hardware emulation for future co-simulation. |
| `syn.rtl.kernel_profile=<0\|1>` | `0` | Add event/stall profiling ports (corresponds to `v++ --profile.stall`). |
| `syn.rtl.fsm_encoding=<value>` | `auto` | State machine encoding strategy for RTL synthesis. |

---

## 16. Schedule Settings

| Option | Default | Description |
|---|---|---|
| `syn.schedule.enable_dsp_full_reg=<0\|1>` | `1` | Require DSP pipeline registers to be fully registered. |

---

## 17. Storage Configuration

Configures global defaults for FIFO storage resources. Override per-element with `syn.directive.bind_storage` or `storage_type` option on `syn.directive.interface`.

```ini
syn.storage=fifo impl=auto auto_srl_max_bits=512 auto_srl_max_depth=3
```

| Sub-option | Default | Description |
|---|---|---|
| `impl=<auto\|bram\|lutram\|uram\|memory\|srl>` | `auto` | FIFO implementation resource. |
| `auto_srl_max_bits=<N>` | `1024` | Max total bits (depth × width) for SRL-based auto implementation. |
| `auto_srl_max_depth=<N>` | `2` | Max SRL depth for auto implementation. |

> Only `fifo` storage type is currently supported.

---

## 18. Vivado Implementation Settings

These settings control the Vivado synthesis/implementation runs used for **resource and timing estimates only** — they do not affect the exported IP/XO output.

| Option | Default | Description |
|---|---|---|
| `vivado.flow=<syn\|impl>` | `impl` | Run synthesis only or full implementation for estimates. |
| `vivado.clock=<period_ns>` | HLS clock | Override clock constraint for Vivado OOC run. |
| `vivado.rtl=<verilog\|vhdl>` | `verilog` | RTL language for Vivado flow. |
| `vivado.optimization_level=<0\|1\|2\|3>` | `0` | Vivado optimization level for estimate run. |
| `vivado.synth_strategy=<name>` | — | Vivado synthesis strategy name (from UG901). |
| `vivado.impl_strategy=<name>` | — | Vivado implementation strategy name (from UG904). |
| `vivado.phys_opt=<none\|place\|route\|all>` | — | Physical optimization stage for implementation estimate run. |
| `vivado.pblock=<range>` | — | Pblock range for implementation. E.g., `{SLICE_X8Y105:SLICE_X23Y149}` |
| `vivado.report_level=<0\|1\|2>` | `2` | Report detail: 0=utilization+timing, 1=adds analysis, 2=adds failfast. |
| `vivado.max_timing_paths=<N>` | — | Max number of timing paths reported when timing is not met. |
| `vivado.synth_design_args=<args>` | — | Extra arguments for Vivado `synth_design` (from UG835). |

---

## 19. Unroll Settings

| Option | Default | Description |
|---|---|---|
| `syn.unroll.tripcount_threshold=<N>` | `0` | Auto-unroll loops with fewer iterations than N. Default 0 = no auto-unroll. |

---

## 20. HLS Optimization Directives (`syn.directive.*`)

Directives apply optimization pragmas to specific code locations from the config file, without modifying source code. Equivalent to `#pragma HLS` in source — but controllable across multiple solutions.

**General syntax:**
```ini
syn.directive.<directive>=<location> [options]
```

Where `<location>` is `function[/loop_label]`.

| Directive | Description | Example |
|---|---|---|
| `syn.directive.aggregate` | Pack struct fields into a single wide vector | `syn.directive.aggregate=func AB compact=bit` |
| `syn.directive.alias` | Define aliasing between M_AXI pointer arguments | `syn.directive.alias=top arr0,arr1 distance=10000000` |
| `syn.directive.allocation` | Limit RTL instances of functions or operations | `syn.directive.allocation=top function instances=foo limit=2` |
| `syn.directive.array_partition` | Partition an array into smaller arrays/registers | `syn.directive.array_partition=func/loop mem type=cyclic factor=2` |
| `syn.directive.array_reshape` | Widen array word width (fewer addresses, wider data) | `syn.directive.array_reshape=func array1 type=block factor=2` |
| `syn.directive.bind_op` | Bind a specific operation to a hardware resource | `syn.directive.bind_op=func variable=c op=mul impl=dsp latency=2` |
| `syn.directive.bind_storage` | Bind a storage variable to a specific memory type | `syn.directive.bind_storage=func variable=buf type=fifo impl=bram` |
| `syn.directive.cache` | Add a read-only cache to an M_AXI port | `syn.directive.cache=func port=in lines=512` |
| `syn.directive.dataflow` | Enable task-level pipelining in a region | `syn.directive.dataflow=top_func` |
| `syn.directive.dependence` | Override loop-carried dependency analysis | `syn.directive.dependence=func/loop variable=arr type=inter direction=RAW false` |
| `syn.directive.disaggregate` | Split a struct into individual elements | `syn.directive.disaggregate=func variable=s` |
| `syn.directive.expression_balance` | Enable/disable adder-tree balancing | `syn.directive.expression_balance=func off` |
| `syn.directive.function_instantiate` | Create per-call-site specialized copies | `syn.directive.function_instantiate=func variable=incr` |
| `syn.directive.inline` | Inline a function into its caller | `syn.directive.inline=func_sub` |
| `syn.directive.interface` | Configure an interface port type | `syn.directive.interface=top_func port=in mode=m_axi bundle=gmem0` |
| `syn.directive.latency` | Constrain min/max latency of a function/loop | `syn.directive.latency=func min=10 max=20` |
| `syn.directive.loop_flatten` | Collapse nested loops into a single loop | `syn.directive.loop_flatten=func/outerloop` |
| `syn.directive.loop_merge` | Merge consecutive loops into one | `syn.directive.loop_merge=func` |
| `syn.directive.loop_tripcount` | Provide trip-count hint for variable-bound loops | `syn.directive.loop_tripcount=func/loop min=1 max=256` |
| `syn.directive.occurrence` | Specify a sub-region runs at a slower rate | `syn.directive.occurrence=func/region cycle=2` |
| `syn.directive.performance` | Set transaction interval target | `syn.directive.performance=func target_ti=100` |
| `syn.directive.pipeline` | Pipeline a loop or function | `syn.directive.pipeline=dct2d II=4` |
| `syn.directive.protocol` | Define a region with explicit handshake (no clock insertions) | `syn.directive.protocol=func/region mode=floating` |
| `syn.directive.reset` | Add/remove reset on static/global variables | `syn.directive.reset=func variable=state off` |
| `syn.directive.stable` | Mark a dataflow region port as stable | `syn.directive.stable=func variable=cfg` |
| `syn.directive.stream` | Configure an array as a FIFO or PIPO stream | `syn.directive.stream=func variable=data type=fifo depth=32` |
| `syn.directive.top` | Designate the top-level function | `syn.directive.top=my_kernel` |
| `syn.directive.unroll` | Unroll a loop by a given factor | `syn.directive.unroll=func/loop factor=4` |

---

## 21. Best Practices

| Practice | Rationale |
|---|---|
| **Use `flow_target=vitis` for application acceleration** | Ensures correct AXI-Lite register map and default offsets; use `vivado` only for embedded IP |
| **Set `clock_uncertainty=15–25%`** | Default 27% is conservative; tighter margin leaves more slack for logic |
| **Use `syn.compile.pipeline_loops=64` (or lower)** | Automatically pipelines common loops without manual pragmas |
| **Set `cosim.enable_fifo_sizing=true` during development** | Let co-sim automatically find minimum FIFO depths to prevent deadlock |
| **Use `syn.interface.m_axi_max_widen_bitwidth=512`** | Maximize bus utilization for memory-bandwidth-bound kernels |
| **Set `syn.dataflow.strict_mode=error`** | Catch non-canonical dataflow patterns at compile time |
| **Use `syn.directive.*` instead of source pragmas for multi-solution designs** | Config-file directives allow different optimizations per solution without touching source |
| **Use `vivado.flow=syn` for faster iteration** | Synthesis-only estimate is much faster than full implementation |
| **Set `syn.rtl.deadlock_detection=hw`** | Enables runtime deadlock detection in deployed hardware |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Section IV, Chapter 16, Pages 457–540*
