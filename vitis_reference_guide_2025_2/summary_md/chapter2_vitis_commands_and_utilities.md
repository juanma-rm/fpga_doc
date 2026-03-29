# Chapter 2: Vitis Commands and Utilities

> **Source**: UG1702 (v2025.2) — Vitis Reference Guide, November 20, 2025, Chapter 2 (pp. 6–212)

This chapter provides a comprehensive reference for the Vitis v++ compiler command, its various modes and options, HLS optimization directives, linking and packaging options, configuration files, and the command-line utilities used throughout the Vitis acceleration development flow.

---

## Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 1 | [Launching Vitis Unified IDE](#launching-vitis-unified-ide) | IDE launch commands and options |
| 2 | [v++ Command](#v-command) | Compiler overview and general options |
| 3 | [v++ Compilation Options](#v-compilation-options) | Compile-time options |
| 4 | [v++ Mode AIE](#v-mode-aie) | AI Engine compilation mode |
| 5 | [v++ Mode HLS](#v-mode-hls) | HLS component compilation mode |
| 6 | [HLS Optimization Directives](#hls-optimization-directives) | Synthesis directives for HLS |
| 7 | [HLS Pragmas](#hls-pragmas) | Source-code pragma reference |
| 8 | [v++ Linking and Packaging Options](#v-linking-and-packaging-options) | --advanced, --clock, --connectivity, --debug, --drc, --linkhook, --package, --profile, --vivado |
| 9 | [Vitis Compiler Configuration File](#vitis-compiler-configuration-file) | Config file format and section tags |
| 10 | [Using the Message Rule File](#using-the-message-rule-file) | Managing v++ build messages |
| 11 | [emconfigutil Utility](#emconfigutil-utility) | Emulation configuration |
| 12 | [kernelinfo Utility](#kernelinfo-utility) | XO file inspection |
| 13 | [launch_emulator Utility](#launch_emulator-utility) | QEMU emulation launch |
| 14 | [manage_ipcache Utility](#manage_ipcache-utility) | HLS IP cache management |
| 15 | [package_xo Command](#package_xo-command) | RTL kernel packaging in Vivado |
| 16 | [RTL Kernel XML File](#rtl-kernel-xml-file) | kernel.xml specification |
| 17 | [platforminfo Utility](#platforminfo-utility) | Platform metadata reporting |
| 18 | [vitis-run Command](#vitis-run-command) | HLS simulation and implementation |
| 19 | [xrt-smi Utility](#xrt-smi-utility) | XRT system management |
| 20 | [xbmgmt Utility](#xbmgmt-utility) | Board management |
| 21 | [xclbinutil Utility](#xclbinutil-utility) | xclbin content management |
| 22 | [xrt.ini File](#xrtini-file) | Runtime initialization configuration |

---

## Launching Vitis Unified IDE

The Vitis Unified IDE is launched from a terminal shell. Set up the environment first, then launch the IDE.

### Environment Setup

```bash
# Linux
source <Vitis_install_path>/settings64.sh

# Windows
call <Vitis_install_path>\settings64.bat
```

### Launch Commands

```bash
# Launch the IDE
vitis -w <workspace_path>
```

### Launch Options

| Option | Description |
|--------|-------------|
| `-w <path>` | Specify workspace path |
| `-new` | Create a new workspace |
| `-open <file>` | Open a specific file |
| `-lp <path>` | Specify local platform repository path |
| `-classic` | Launch the Vitis Classic IDE (where available) |

---

## v++ Command

The `v++` command is the primary tool in the Vitis development environment, supporting compilation, linking, and packaging of kernels and systems for AMD devices. It supports multiple modes including HLS, AI Engine, and system-level flows.

### General Syntax

```bash
v++ [mode] [options] [input files]
```

### v++ General Options

These options apply across compilation, linking, and packaging steps.

| Option | Description |
|--------|-------------|
| `-c`, `--compile` | Run compilation |
| `-l`, `--link` | Run linking |
| `-p`, `--package` | Run packaging |
| `--mode <mode>` | Specify mode: `aie`, `hls`, `vss` |
| `-t`, `--target <target>` | Build target: `sw_emu`, `hw_emu`, `hw` (default: `hw`) |
| `-f`, `--platform <name\|path>` | Target platform for the build |
| `--part <part>` | Specify the target part (alternative to `--platform`) |
| `-k`, `--kernel <name>` | Kernel name (compilation) |
| `-o`, `--output <file>` | Output file name |
| `-s`, `--save-temps` | Save intermediate files |
| `-g`, `--debug` | Generate debug info |
| `-O`, `--optimize <level>` | Optimization level: `0`, `1`, `2`, `3`, `s` |
| `-R`, `--report_level <level>` | Report detail: `0`, `1`, `2`, `estimate` |
| `--config <file>` | Specify a configuration file |
| `--log_dir <dir>` | Directory for log files |
| `--temp_dir <dir>` | Directory for temporary files |
| `--remote_ip_cache <dir>` | Remote IP cache directory location |
| `--no_ip_cache` | Disable IP caching |
| `--freqhz <freq>` | Specify kernel clock frequency in Hz |
| `-j`, `--jobs <n>` | Number of parallel jobs |
| `--message_rules <file>` | Specify a message rule file (`.mrf`) |
| `-h`, `--help` | Display help |
| `--version` | Display version |
| `-I <path>` | Add include directory path |
| `--hls.pre_tcl <file>` | Pre-synthesis Tcl script |
| `--hls.post_tcl <file>` | Post-synthesis Tcl script |
| `--input_files <files>` | Specify input files |
| `--user_ip_repo_paths <paths>` | Add custom IP repository paths |
| `--vivado.synth.jobs <n>` | Jobs for Vivado synthesis |
| `--vivado.impl.jobs <n>` | Jobs for Vivado implementation |

### Build Targets

| Target | Description |
|--------|-------------|
| `sw_emu` | Software emulation — validates functional correctness using a C/C++ model |
| `hw_emu` | Hardware emulation — validates RTL using cycle-accurate simulation with QEMU for embedded |
| `hw` | Hardware build — generates the actual FPGA bitstream for deployment |

---

## v++ Compilation Options

These options are specific to the `v++ --compile` or `v++ -c` step.

| Option | Description |
|--------|-------------|
| `-c`, `--compile` | Invoke the compilation step |
| `-k`, `--kernel <name>` | Specify the kernel function name |
| `--hls.clock <period_ns>` | Set the HLS clock period in nanoseconds |
| `-D<name>[=<value>]` | Define a preprocessor macro |
| `-I <path>` | Add an include directory |
| `--advanced.param compiler.preserveHlsOutput=1` | Preserve HLS output files |

---

## v++ Mode AIE

Use `v++ -c --mode aie` to compile AI Engine graph applications. The AI Engine compiler takes the ADF graph application and compiles it into ELF binaries for each AI Engine tile and generates a `libadf.a` library.

### Syntax

```bash
v++ -c --mode aie --config <config_file> --platform <platform> --work_dir <dir>
```

### AIE Configuration File Commands

These are specified under the `[aie]` section in the configuration file:

| Command | Description |
|---------|-------------|
| `aie.adf-graph-source` | Source file containing the ADF graph |
| `aie.adf-graph-name` | Name of the ADF graph |
| `aie.include` | Include directories for AI Engine compilation |
| `aie.workdir` | Working directory for AI Engine compilation outputs |
| `aie.xlopt` | Optimization level for AI Engine compilation |
| `aie.Xchess` | Pass options to the Chess compiler |
| `aie.Xpreproc` | Pass options to the preprocessor |
| `aie.constraints` | Constraints file for AI Engine mapping |
| `aie.pl-freq` | Specify PL kernel frequency in MHz |
| `aie.heapsize` | Stack/heap size for AI Engine tiles |
| `aie.stacksize` | Stack size for AI Engine tiles |
| `aie.enable-broadcast` | Enable broadcast for AI Engine |

---

## v++ Mode HLS

Use `v++ -c --mode hls` to compile HLS components. This mode synthesizes C/C++ code into RTL. Almost all HLS commands must be specified in a configuration file (exceptions: `--platform` and `--freqhz`).

### Syntax

```bash
v++ -c --mode hls --config <config_file> --platform <platform>
```

### HLS General Configuration

Specified under the `[hls]` section in the config file:

| Command | Description |
|---------|-------------|
| `clock=<period_ns>` | Target clock period in nanoseconds |
| `clock_uncertainty=<value>` | Clock uncertainty (absolute ns or percentage, e.g., `15%`) |
| `flow_target=<vitis\|vivado>` | Target flow: `vitis` for Vitis acceleration, `vivado` for IP export |
| `syn.top=<function>` | Top-level function for synthesis |
| `syn.file=<path>` | Source file(s) for synthesis |
| `syn.file_cflags=<path>,<flags>` | Per-file compile flags |
| `syn.file_csimflags=<path>,<flags>` | Per-file C-simulation flags |
| `tb.file=<path>` | Test bench file(s) |
| `tb.file_cflags=<path>,<flags>` | Per-file test bench compile flags |
| `syn.output.format=<xo\|ip>` | Output format: Xilinx Object or IP |

### C-Synthesis Sources Configuration

| Command | Description |
|---------|-------------|
| `syn.file=<path>` | Add a source file for synthesis |
| `syn.file_cflags=<file>,<flags>` | Set compile flags for a specific source file |
| `syn.top=<function_name>` | Define the top-level function to synthesize |

### Test Bench Configuration

| Command | Description |
|---------|-------------|
| `tb.file=<path>` | Add a test bench file |
| `tb.file_cflags=<file>,<flags>` | Compile flags for test bench files |
| `tb.file_csimflags=<file>,<flags>` | C-simulation flags for test bench files |

### Array Partition Configuration

| Command | Description |
|---------|-------------|
| `syn.directive.array_partition=<variable> <type> <factor> <dim>` | Partition an array by type: `block`, `cyclic`, or `complete` |

### Stencil Configuration

| Command | Description |
|---------|-------------|
| `syn.stencil` | Enable stencil optimization for sliding-window operations |

### C-Simulation Configuration

| Command | Description |
|---------|-------------|
| `csim.code_analyzer=<0\|1>` | Enable code analyzer during C-simulation |
| `csim.O=<true\|false>` | Enable compiler optimizations in C-simulation |
| `csim.clean=<true\|false>` | Clean previous simulation results |
| `csim.profile=<true\|false>` | Enable profiling during C-simulation |
| `csim.setup=<true\|false>` | Only setup, do not run simulation |
| `csim.ldflags=<flags>` | Linker flags for C-simulation |
| `csim.argv=<args>` | Command-line arguments passed to the test bench |

### Co-Simulation Configuration

| Command | Description |
|---------|-------------|
| `cosim.trace_level=<none\|port\|all>` | Signal trace level |
| `cosim.wave_debug=<true\|false>` | Open waveform viewer |
| `cosim.random_stall=<true\|false>` | Insert random stalls to test tolerance |
| `cosim.enable_dataflow_profiling=<true\|false>` | Profile dataflow channels |
| `cosim.setup=<true\|false>` | Only setup, do not run co-simulation |
| `cosim.O=<true\|false>` | Enable optimizations in co-simulation |
| `cosim.ldflags=<flags>` | Linker flags for co-simulation |
| `cosim.argv=<args>` | Command-line arguments for co-simulation test bench |

### Implementation Configuration

| Command | Description |
|---------|-------------|
| `impl.run_strategy=<strategy>` | Vivado implementation strategy |
| `impl.jobs=<n>` | Number of parallel implementation jobs |

### Compile Options Configuration

| Command | Description |
|---------|-------------|
| `compile.pipeline_loops=<threshold>` | Auto-pipeline loops with trip count above threshold (0 disables) |
| `compile.unsafe_math_optimizations=<0\|1>` | Allow unsafe floating-point optimizations |
| `compile.no_signed_zeros=<0\|1>` | Ignore sign of zero |

### Dataflow Configuration

| Command | Description |
|---------|-------------|
| `syn.directive.dataflow` | Enable task-level pipelining (dataflow) |
| `dataflow.default_channel=<fifo\|pingpong>` | Default channel type between dataflow tasks |
| `dataflow.fifo_depth=<n>` | Default FIFO depth |

### Debug Options

| Command | Description |
|---------|-------------|
| `debug.directive=<directive>` | Enable specific debug directives |

### Interface Configuration

| Command | Description |
|---------|-------------|
| `syn.directive.interface` | Configure function interfaces (mode, bundle, port, etc.) |

### Operator Configuration

| Command | Description |
|---------|-------------|
| `syn.directive.bind_op` | Bind operations to specific implementations (DSP, fabric) |
| `syn.directive.bind_storage` | Bind storage to specific implementations (BRAM, LUTRAM, URAM) |

### RTL Configuration

| Command | Description |
|---------|-------------|
| `rtl.register_reset_num=<n>` | Number of clock cycles for reset |

### Schedule Configuration

| Command | Description |
|---------|-------------|
| `schedule.enable_pipeline_style=<stp\|flp\|frp>` | Pipeline style: stall pipeline, flush pipeline, free-running pipeline |

### Storage/Implementation Configuration

| Command | Description |
|---------|-------------|
| `syn.directive.bind_storage` | Assign arrays/variables to specific storage resources |

### Unroll Settings

| Command | Description |
|---------|-------------|
| `syn.directive.unroll` | Unroll loops by a specified factor |

---

## HLS Optimization Directives

HLS optimization directives fine-tune how C/C++ code is synthesized into RTL. Each directive can be specified in the configuration file under `[hls]` using `syn.directive.<name>` syntax, or in source code as `#pragma HLS <name>`.

### syn.directive.aggregate

Combines the elements of a struct into a single wide word to improve memory access efficiency.

**Syntax:**
```
syn.directive.aggregate=<variable> <compact|bit|byte|none>
```

| Option | Description |
|--------|-------------|
| `compact` | Pack struct into minimum number of bits (default) |
| `bit` | Bit-level packing, data aligned to bit boundaries |
| `byte` | Byte-level packing, data aligned to byte boundaries |
| `none` | Do not aggregate |

### syn.directive.alias

Links two or more arrays to the same physical memory resource.

**Syntax:**
```
syn.directive.alias=<function> <ports> <offset> <distance>
```

| Option | Description |
|--------|-------------|
| `ports=<p1,p2,...>` | Ports to alias together |
| `offset=<n>` | Address offset between aliased arrays |
| `distance=<n>` | Distance between the arrays |

### syn.directive.allocation

Limits the number of operations, cores, or functions used in RTL — enables resource sharing to reduce area.

**Syntax:**
```
syn.directive.allocation=<function> <instances|operations> <name> limit=<n>
```

| Option | Description |
|--------|-------------|
| `instances` | Limit the number of RTL instances of a function |
| `operations` | Limit the number of operations (e.g., `mul`, `add`) |
| `limit=<n>` | Maximum number of instances/operations allowed |

### syn.directive.array_partition

Splits an array into smaller arrays or individual registers, allowing more parallel access.

**Syntax:**
```
syn.directive.array_partition=<variable> <type> factor=<n> dim=<d>
```

| Type | Description |
|------|-------------|
| `block` | Divide into N contiguous blocks |
| `cyclic` | Interleaved partitioning with factor N |
| `complete` | Fully decompose into individual registers |

| Option | Description |
|--------|-------------|
| `factor=<n>` | Number of partitions (not used with `complete`) |
| `dim=<d>` | Array dimension to partition (0 = all dimensions) |

### syn.directive.array_reshape

Combines `array_partition` with vertical recombination into wider elements to increase throughput without increasing the number of memory ports.

**Syntax:**
```
syn.directive.array_reshape=<variable> <type> factor=<n> dim=<d>
```

Options are the same as `array_partition`.

### syn.directive.bind_op

Binds a specific operation to a particular implementation (DSP or fabric).

**Syntax:**
```
syn.directive.bind_op=<variable> op=<op_type> impl=<impl_type> latency=<n>
```

**Functional Operations:**

| Operation | Description | Implementations |
|-----------|-------------|-----------------|
| `mul` | Multiplication | `fabric`, `dsp`, `auto` |
| `add` | Addition | `fabric`, `dsp`, `auto` |
| `sub` | Subtraction | `fabric`, `dsp`, `auto` |

**Floating Point Operations:**

| Operation | Description | Implementations |
|-----------|-------------|-----------------|
| `fadd` | FP addition | `fabric`, `meddsp`, `fulldsp`, `maxdsp`, `primitivedsp` |
| `fsub` | FP subtraction | `fabric`, `meddsp`, `fulldsp`, `maxdsp`, `primitivedsp` |
| `fmul` | FP multiplication | `fabric`, `meddsp`, `fulldsp`, `maxdsp`, `primitivedsp` |
| `fdiv` | FP division | `fabric` |
| `fexp` | FP exponential | `fabric`, `meddsp`, `fulldsp` |
| `flog` | FP logarithm | `fabric`, `meddsp`, `fulldsp` |
| `fsqrt` | FP square root | `fabric`, `meddsp`, `fulldsp`, `maxdsp` |
| `frsqrt` | FP reciprocal sqrt | `fabric`, `meddsp`, `fulldsp` |
| `frecip` | FP reciprocal | `fabric`, `meddsp`, `fulldsp` |
| `fcmp` | FP comparison | `fabric`, `auto` |
| `dcmp` | Double comparison | `fabric`, `auto` |
| `dadd` | Double addition | `fabric`, `fulldsp`, `primitivedsp` |
| `dsub` | Double subtraction | `fabric`, `fulldsp`, `primitivedsp` |
| `dmul` | Double multiplication | `fabric`, `fulldsp`, `maxdsp`, `primitivedsp` |
| `ddiv` | Double division | `fabric` |
| `dsqrt` | Double square root | `fabric` |
| `hcmp` | Half comparison | `fabric`, `auto` |
| `hadd` | Half addition | `fabric`, `fulldsp`, `primitivedsp` |
| `hsub` | Half subtraction | `fabric`, `fulldsp`, `primitivedsp` |
| `hmul` | Half multiplication | `fabric`, `dsp`, `primitivedsp` |
| `hdiv` | Half division | `fabric` |
| `hsqrt` | Half square root | `fabric` |

### syn.directive.bind_storage

Assigns a variable (array or register) to a specific storage resource.

**Syntax:**
```
syn.directive.bind_storage=<variable> type=<type> impl=<impl> latency=<n>
```

**Storage Types:**

| Type | Description |
|------|-------------|
| `fifo` | FIFO buffer |
| `ram_1p` | Single-port RAM |
| `ram_1wnr` | 1 write, N read RAM |
| `ram_2p` | Dual-port RAM |
| `ram_s2p` | Simple dual-port RAM |
| `ram_t2p` | True dual-port RAM |
| `rom_1p` | Single-port ROM |
| `rom_2p` | Dual-port ROM |
| `rom_np` | Multi-port ROM |

**Implementation Types:**

| Implementation | Description |
|----------------|-------------|
| `auto` | Automatic selection (default) |
| `bram` | Block RAM |
| `bram_ecc` | Block RAM with ECC |
| `lutram` | Distributed (LUT) RAM |
| `uram` | UltraRAM |
| `uram_ecc` | UltraRAM with ECC |
| `srl` | Shift register LUT |

### syn.directive.dataflow

Enables task-level pipelining, allowing functions and loops to overlap execution.

**Syntax:**
```
syn.directive.dataflow=<function>
```

> ⚠️ **Important**: Dataflow requires that functions communicate through well-defined channels (FIFOs or ping-pong buffers). Functions must have a single-producer, single-consumer relationship.

### syn.directive.dependence

Provides additional information about data dependencies to the tool so it can better optimize scheduling.

**Syntax:**
```
syn.directive.dependence=<variable> <class> <type> <direction> <dependent> <distance>
```

| Option | Values | Description |
|--------|--------|-------------|
| `class` | `array`, `pointer` | Type of dependency |
| `type` | `inter`, `intra` | Between loop iterations or within same iteration |
| `direction` | `RAW`, `WAR`, `WAW` | Read-after-write, write-after-read, write-after-write |
| `dependent` | `true`, `false` | Whether dependency exists |
| `distance` | `<n>` | Distance in loop iterations |

### syn.directive.disaggregate

Breaks an aggregated struct back into individual elements. Opposite of `aggregate`.

**Syntax:**
```
syn.directive.disaggregate=<variable>
```

### syn.directive.expression_balance

Controls expression balancing (tree rewriting for shorter operator chains), which can reduce latency at the expense of area.

**Syntax:**
```
syn.directive.expression_balance=<function> off=<true|false>
```

### syn.directive.function_instantiate

Creates unique hardware instances for each call of a function, allowing per-call optimization when constant arguments are used.

**Syntax:**
```
syn.directive.function_instantiate=<function> variable=<arg>
```

### syn.directive.inline

Inlines a function, removing the function call overhead and enabling cross-boundary optimizations.

**Syntax:**
```
syn.directive.inline=<function> <off|recursive>
```

| Option | Description |
|--------|-------------|
| (default) | Inline the function |
| `off` | Prevent inlining |
| `recursive` | Inline recursively all functions called within |

### syn.directive.interface

Configures the physical I/O ports generated for the top-level function arguments.

**Syntax:**
```
syn.directive.interface=<function> <mode> <port> <bundle> <options>
```

**Interface Modes:**

| Mode | Description |
|------|-------------|
| `ap_none` | Simple wire with no handshake |
| `ap_stable` | Input that does not change during kernel operation |
| `ap_hs` | Two-way handshake (valid + acknowledge) |
| `ap_vld` | Output valid signal |
| `ap_ack` | Input acknowledge signal |
| `ap_ovld` | Output valid on output port |
| `ap_fifo` | FIFO interface |
| `ap_memory` | Standard memory interface (address + CE + WE + data) |
| `bram` | Block RAM interface |
| `axis` | AXI4-Stream interface |
| `s_axilite` | AXI4-Lite slave interface |
| `m_axi` | AXI4 master memory-mapped interface |
| `ap_ctrl_hs` | Block-level control with ap_start/ap_done/ap_idle/ap_ready |
| `ap_ctrl_chain` | Block-level with ap_continue for dataflow |
| `ap_ctrl_none` | No block-level control |

**Common Options:**

| Option | Description |
|--------|-------------|
| `port=<name>` | Port to configure |
| `bundle=<name>` | Group ports into the same AXI bundle |
| `register` | Register the port (reduce timing path) |
| `register_mode=<off\|both\|forward\|reverse>` | Which signals to register |
| `depth=<n>` | FIFO depth for `m_axi` reads/writes (for co-simulation) |
| `max_read_burst_length=<n>` | Maximum AXI read burst length |
| `max_write_burst_length=<n>` | Maximum AXI write burst length |
| `num_read_outstanding=<n>` | Outstanding read transactions |
| `num_write_outstanding=<n>` | Outstanding write transactions |
| `offset=<off\|direct\|slave>` | Address offset mode for `m_axi` ports |
| `latency=<n>` | Expected latency of the port |
| `max_widen_bitwidth=<n>` | Maximum bit-width for automatic widening |
| `storage_impl=<auto\|bram\|lutram\|uram>` | Storage implementation for `s_axilite` |
| `clock=<name>` | Assign port to a different clock domain |
| `name=<name>` | Override the default port name |

### syn.directive.latency

Constrains the latency of a function, loop, or region.

**Syntax:**
```
syn.directive.latency=<scope> min=<n> max=<n>
```

### syn.directive.loop_flatten

Flattens nested perfect or semi-perfect loop nests into a single loop, reducing loop overhead.

**Syntax:**
```
syn.directive.loop_flatten=<loop_label> off=<true|false>
```

### syn.directive.loop_merge

Merges consecutive loops in the same scope to reduce latency and improve sharing.

**Syntax:**
```
syn.directive.loop_merge=<function|region> force
```

### syn.directive.loop_tripcount

Provides the tool with estimated loop bounds for reporting purposes. Does not affect synthesis.

**Syntax:**
```
syn.directive.loop_tripcount=<loop_label> min=<n> max=<n> avg=<n>
```

### syn.directive.occurrence

Specifies that code in a region executes at a lower rate than the surrounding code.

**Syntax:**
```
syn.directive.occurrence=<region> cycle=<n>
```

### syn.directive.performance

Specifies a target throughput for a loop or function.

**Syntax:**
```
syn.directive.performance=<scope> target_ti=<n> target_tl=<n> unit=<cycle|sec>
```

| Option | Description |
|--------|-------------|
| `target_ti` | Target initiation interval |
| `target_tl` | Target latency |
| `unit` | `cycle` or `sec` |

### syn.directive.pipeline

Enables function or loop pipelining to process new inputs every N clock cycles.

**Syntax:**
```
syn.directive.pipeline=<scope> II=<n> style=<stp|flp|frp> rewind off
```

| Option | Description |
|--------|-------------|
| `II=<n>` | Target initiation interval (default: 1) |
| `style=stp` | Stall pipeline (default) — stalls all stages if any stage stalls |
| `style=flp` | Flush pipeline — allows earlier stages to flush while later stall |
| `style=frp` | Free-running pipeline — no stall logic, lowest resource but requires careful design |
| `rewind` | Allow pipeline to restart without waiting for last iteration to finish |
| `off` | Disable pipelining |

### syn.directive.protocol

Applies a protocol region, specifying that interface accesses in the region follow a specific timing behavior.

**Syntax:**
```
syn.directive.protocol=<region> mode=<floating|fixed>
```

### syn.directive.reset

Controls reset behavior for specific variables.

**Syntax:**
```
syn.directive.reset=<variable> off
```

### syn.directive.stable

Indicates that a port value does not change while the kernel is running.

**Syntax:**
```
syn.directive.stable=<variable>
```

### syn.directive.stream

Specifies that an array should be implemented as a streaming FIFO rather than RAM.

**Syntax:**
```
syn.directive.stream=<variable> depth=<n> dim=<d> off type=<fifo|pipo|shared>
```

| Option | Description |
|--------|-------------|
| `depth=<n>` | Depth of the FIFO |
| `dim=<d>` | Dimension of the array to stream |
| `off` | Disable streaming |
| `type=fifo` | FIFO implementation (default) |
| `type=pipo` | Ping-pong buffer |
| `type=shared` | Shared FIFO |

### syn.directive.top

Specifies the top-level function for synthesis.

**Syntax:**
```
syn.directive.top=<function>
```

### syn.directive.unroll

Unrolls a loop to create parallel hardware copies.

**Syntax:**
```
syn.directive.unroll=<loop_label> factor=<n> skip_exit_check region
```

| Option | Description |
|--------|-------------|
| `factor=<n>` | Unroll factor (omit for full unroll) |
| `skip_exit_check` | Skip exit condition check for partially unrolled loops |
| `region` | Unroll all loops in the region |

---

## HLS Pragmas

HLS pragmas are equivalent to the config-file directives above, placed directly in C/C++ source code. The general syntax is:

```c
#pragma HLS <directive_name> <options>
```

**Pragmas by Category:**

| Category | Pragmas |
|----------|---------|
| **Kernel optimization** | `pipeline`, `unroll`, `loop_flatten`, `loop_merge`, `loop_tripcount`, `occurrence`, `performance`, `expression_balance`, `dataflow`, `inline`, `function_instantiate`, `allocation` |
| **Array optimization** | `array_partition`, `array_reshape`, `bind_storage`, `aggregate`, `disaggregate`, `stream`, `alias` |
| **Interface** | `interface`, `protocol`, `stable`, `reset` |
| **Resource binding** | `bind_op`, `bind_storage` |
| **Dependency** | `dependence` |
| **Top-level** | `top` |
| **Latency** | `latency` |

---

## v++ Linking and Packaging Options

The `v++ --link` (or `-l`) step connects compiled kernels, assigns connectivity, applies profiling and debug monitors, and configures the Vivado implementation. The options below are organized by option group.

### --advanced Options

Advanced parameters and properties for fine-tuning the build.

#### --advanced.param

| Parameter | Description |
|-----------|-------------|
| `compiler.interfaceWrBurstLen=<n>` | Default write burst length for AXI4 master interfaces |
| `compiler.interfaceRdBurstLen=<n>` | Default read burst length for AXI4 master interfaces |
| `compiler.interfaceRdOutstanding=<n>` | Default number of outstanding read transactions |
| `compiler.interfaceWrOutstanding=<n>` | Default number of outstanding write transactions |
| `compiler.maxComputeUnits=<n>` | Maximum compute units allowed in a design |
| `compiler.addOutputTypes=<hw_export\|sd_card>` | Additional output types |
| `compiler.errorOnHoldViolation=<1\|0>` | Error on hold violations |
| `compiler.skipTimingCheckAndFrequencyScaling=<1\|0>` | Skip timing check (use with caution) |
| `compiler.userPreSysLinkOverlayTcl=<file>` | Pre-SysLink Tcl overlay script |
| `compiler.userPostSysLinkOverlayTcl=<file>` | Post-SysLink Tcl overlay script |
| `hw_emu.enableProtocolChecker=<true\|false>` | Enable AXI protocol checker in HW emulation |
| `hw_emu.compiledLibs=<path>` | Path to pre-compiled simulation libraries |
| `hw_emu.platformPath=<path>` | Path to HW emulation platform |
| `package.enableEdfHwEmu=<true\|false>` | Enable EDF-based HW emulation |

#### --advanced.prop

```bash
--advanced.prop <object_type>.<object_name>.<property_name>=<value>
```

#### --advanced.misc

Passes miscellaneous advanced parameters.

### --clock Options

Configure clocks for compilation and linking.

**AIE Compilation Clock Directives:**

| Directive | Description |
|-----------|-------------|
| `--clock.defaultFreqHz=<freq>` | Default AI Engine frequency in Hz |
| `--clock.freqHz=<freq>:<cu>` | Per-CU clock frequency for AIE |

**HLS Compilation Clock Directives:**

| Directive | Description |
|-----------|-------------|
| `--clock.defaultTolerance=<value>` | Default clock tolerance |
| `--clock.freqHz=<freq>:<kernel>` | Per-kernel clock frequency |

**v++ Linking Clock Directives:**

| Directive | Description |
|-----------|-------------|
| `--clock.defaultFreqHz=<freq>` | Default kernel clock frequency for linking |
| `--clock.freqHz=<freq>:<cu>.<clk>` | Per-CU, per-clock pin frequency |
| `--clock.defaultTolerance=<value>` | Default clock tolerance |
| `--clock.id=<id>:<cu>.<clk>` | Assign a platform clock index to a CU clock pin |

### --connectivity Options

Define how kernels connect to memory and to each other.

#### --connectivity.nk

Specify the number of compute units (CU instances) of a kernel to create.

```bash
--connectivity.nk <kernel>:<count>[:<cu_name1>.<cu_name2>...]
```

**Example:**
```bash
v++ --link --connectivity.nk vadd:3:vadd_1.vadd_2.vadd_3
```

#### --connectivity.sc (stream_connect)

Create streaming connections between kernel ports or between kernel and platform ports.

```bash
--connectivity.sc <source>:<destination>[:<FIFO_depth>]
```

**Example:**
```bash
v++ --link --connectivity.sc k1.out:k2.in:512
```

#### --connectivity.sp (system_port)

Assign kernel ports to specific memory banks or platform interfaces.

```bash
--connectivity.sp <cu_name>.<port>:<memory_resource>
```

**Example:**
```bash
v++ --link --connectivity.sp vadd_1.m_axi_gmem:DDR[0]
```

#### --connectivity.connect

General connection directive for connecting various component interfaces.

```bash
--connectivity.connect <source>:<destination>
```

#### --connectivity.noc.connect

Connect a specific NoC instance.

#### --connectivity.noc.read_bw / noc.write_bw

Specify read/write bandwidth for NoC connections.

#### --connectivity.slr

Assign a compute unit to a specific SLR (Super Logic Region) on multi-die devices.

```bash
--connectivity.slr <cu_name>:<SLR>
```

### --debug Options

Insert debug infrastructure into the design.

| Option | Description |
|--------|-------------|
| `--debug.chipscope <cu_name>:<port>` | Add ILA (ChipScope) debug probe on port |
| `--debug.protocol <all\|<cu>:<interface>>` | Add AXI protocol checker |
| `--debug.list_ports` | List available debug ports |

**Example:**
```bash
v++ --link --debug.chipscope vadd_1:m_axi_gmem
v++ --link --debug.protocol all
```

### --drc Options

Manage Design Rule Check (DRC) messages from Vivado.

| Option | Description |
|--------|-------------|
| `--drc.disable <DRC_ID>` | Disable a DRC check |
| `--drc.enable <DRC_ID>` | Re-enable a DRC check |
| `--drc.severity <DRC_ID>:<level>` | Change DRC severity (e.g., `TIMING-18:Warning`) |
| `--drc.waive <DRC_ID>` | Waive a DRC (still checked, marked as waived) |

### --linkhook Options

Specify Tcl scripts to run at specific build steps during the linking process.

| Option | Description |
|--------|-------------|
| `--linkhook.custom <step>,<script>` | Run Tcl script at a predefined step |
| `--linkhook.do_first <step>,<script>` | Run Tcl script before the given step |
| `--linkhook.do_last <step>,<script>` | Run Tcl script after the given step |
| `--linkhook.list_steps` | List available build steps (requires `--target`) |

**Example:**
```bash
v++ -l --linkhook.do_first vpl.impl.place_design,runScript.tcl
v++ --target hw -l --linkhook.list_steps
```

### --package Options

The `v++ --package` (or `-p`) step generates the final deployable output. Required for embedded platforms (Versal, Zynq UltraScale+).

**Versal Syntax:**
```bash
v++ --package --platform fixed.xsa -o output.xclbin --package.<options>
```

**Non-Versal Syntax:**
```bash
v++ --package -t <hw_emu|hw> --platform <platform> input.xclbin \
  [-o output.xclbin --package.<options>]
```

| Option | Description |
|--------|-------------|
| `--package.aie_metadata_only` | Include only AI Engine metadata in xclbin (no full data) |
| `--package.aie_overlay` | Include aie.pdi with LOAD_PDI action mask for DFX |
| `--package.aie_resources_bin <file>` | AIE resources binary file |
| `--package.pl_metadata_only` | Include only PL metadata in xclbin |
| `--package.aie_debug_port <port>` | TCP port for AIE debug (default: 10100) |
| `--package.bl31_elf <path>` | Arm trusted FW ELF for A72 |
| `--package.boot_mode <ospi\|qspi\|sd>` | Boot mode (default: sd for embedded) |
| `--package.defer_aie_run` | AI Engine cores enabled by PS app instead of during PDI load |
| `--package.domain <name>` | Domain name (use `aiengine` for AIE designs) |
| `--package.dtb <path>` | Device tree binary for Linux on APU |
| `--package.enable_aie_debug` | Force AIE cores into debug halt mode on PDI load |
| `--package.image_format <ext4\|fat32>` | SD card image format |
| `--package.kernel_image <path>` | Linux kernel image path |
| `--package.no_image` | Skip SD card image creation |
| `--package.out_dir <path>` | Output directory for package command |
| `--package.ps_debug_port <port>` | TCP port for PS debug |
| `--package.ps_elf <path>,<core>` | Baremetal ELF and processor core pair |
| `--package.rootfs <path>` | Root filesystem path |
| `--package.sd_dir <path>` | Folder to package into sd_card directory |
| `--package.sd_file <path>` | File(s) to add to sd_card |
| `--package.uboot <path>` | U-Boot ELF override |

**Processor Core Values:**

| Device | Cores |
|--------|-------|
| Versal | `a72-0`, `a72-1`, `a72-2`, `a72-3` |
| Zynq UltraScale+ MPSoC | `a53-0`–`a53-3`, `r5-0`, `r5-1` |
| Zynq 7000 | `a9-0`, `a9-1` |

### --profile Options

Enable profiling infrastructure in the design. Requires corresponding `xrt.ini` settings at runtime.

> ⚠️ **Important**: Using `--profile` in v++ also requires profile or trace options in the `xrt.ini` file.

**Configuration File Format:**
```ini
[profile]
data=all:all:all
stall=all:all
exec=all:all
memory=all
aie=all
```

| Option | Syntax | Description |
|--------|--------|-------------|
| `--profile.aie` | `<graph_arg\|pin\|all>` | Monitor AIE streams |
| `--profile.aie_trace_offload` | `HSDP` | AIE trace via high-speed debug port |
| `--profile.data` | `<kernel>:<cu>:<interface>(:<counters\|all>)` | Monitor data ports |
| `--profile.exec` | `<kernel>:<cu>(:<counters\|all>)` | Record kernel execution times |
| `--profile.stall` | `<kernel>:<cu>(:<counters\|all>)` | Monitor stalls (⚠️ required during both compile and link) |
| `--profile.trace_memory` | `<FIFO>:<size>\|<MEMORY>[<n>][:<SLR>]` | Memory for trace capture (hw only) |

**Example:**
```bash
v++ --link --profile.data k1:all:all
v++ --compile -k k1 --profile.stall ...
v++ --link --profile.stall:k1:cu2 ...
```

**Trace Memory Configuration:**
```ini
[profile]
trace_memory=DDR[1]:SLR0
trace_memory=DDR[2]:SLR1
```

> ⚠️ You cannot mix DDR and HBM memory banks in a single design when using the `<SLR>` syntax.

### --vivado Options

Configure Vivado synthesis and implementation.

| Option | Description |
|--------|-------------|
| `--vivado.impl.jobs <n>` | Parallel implementation jobs |
| `--vivado.impl.lsf <cmd>` | LSF bsub command for distributed implementation |
| `--vivado.impl.strategies <list\|ALL>` | Comma-separated implementation strategies |
| `--vivado.param <arg>` | Vivado parameter (use `report_param` in Vivado to list) |
| `--vivado.prop <prop>` | Vivado property |
| `--vivado.synth.jobs <n>` | Parallel synthesis jobs |
| `--vivado.synth.lsf <cmd>` | LSF bsub command for distributed synthesis |

**Property Syntax:**
```bash
--vivado.prop <object_type>.<object_name>.<property_name>=<value>
```

Where `<object_type>` is `run`, `fileset`, `file`, or `project`.

**Example:**
```bash
v++ --link --vivado.prop run.impl_1.STEPS.PHYS_OPT_DESIGN.IS_ENABLED=true
v++ --link --vivado.prop run.impl_1.STEPS.PHYS_OPT_DESIGN.ARGS.DIRECTIVE=Explore
v++ --link --vivado.prop run.impl_1.STEPS.PLACE_DESIGN.TCL.PRE=/path/to/xxx.tcl
```

> ⚠️ For properties with spaces (e.g., `MORE OPTIONS`), surround the complete property name with braces:
> ```
> --vivado.prop run.impl_1.{STEPS.PLACE_DESIGN.ARGS.MORE OPTIONS}={-no_bufg_opt}
> ```

**Config File Format:**
```ini
[vivado]
prop=run.impl_1.STEPS.PHYS_OPT_DESIGN.IS_ENABLED=true
prop=run.impl_1.STEPS.PHYS_OPT_DESIGN.ARGS.DIRECTIVE=Explore
impl.jobs=4
synth.jobs=4
```

---

## Vitis Compiler Configuration File

Configuration files are the recommended way to work with v++ and the Vitis IDE. They manage build options under grouped section headers, support multiple processes, and simplify the command line.

### Usage

```bash
v++ --link --config ../src/system.cfg
```

### Precedence Rules

1. Command-line switches (highest)
2. Config files — left-to-right on the command line
3. Within a config file — top-to-bottom

### Section Tags

| Section | Description |
|---------|-------------|
| (Unlabeled) | General commands: `--part`, `--platform`, `--freqhz`, `--debug` |
| `[advanced]` | `--advanced` options |
| `[aie]` | AI Engine compilation (`v++ -c --mode aie`) |
| `[clock]` | `--clock` options |
| `[connectivity]` | `--connectivity` options |
| `[debug]` | `--debug` options |
| `[hls]` | HLS compilation (`v++ -c --mode hls`) |
| `[linkhook]` | `--linkhook` options |
| `[package]` | `--package` options |
| `[profile]` | `--profile` options |
| `[vivado]` | `--vivado` options |

**Example Configuration File:**
```ini
# Platform
platform=xilinx_u200_gen3x16_xdma_2_202110_1

# Connectivity
[connectivity]
nk=vadd:2:vadd_1.vadd_2
sp=vadd_1.m_axi_gmem:DDR[0]
sp=vadd_2.m_axi_gmem:DDR[1]

# Profiling
[profile]
data=all:all:all

# Vivado
[vivado]
prop=run.impl_1.STEPS.PHYS_OPT_DESIGN.IS_ENABLED=true
impl.jobs=4
```

> **TIP:** Keep separate configuration files for separate processes (HLS compilation, linking, packaging).

---

## Using the Message Rule File

The message rule file (`.mrf`) manages v++ build messages — promoting important ones or suppressing unimportant ones.

### Commands

| Command | Description |
|---------|-------------|
| `promote` | Promote matching messages to v++ terminal output |
| `suppress` | Suppress matching messages from v++ output (errors cannot be suppressed) |

### Options (case-sensitive)

| Option | Description |
|--------|-------------|
| `-id <message_id>` | Match by message ID (format: `nnn-mmm`) |
| `-severity <level>` | Match by severity: `info`, `warning`, `critical_warning` |

**Precedence:** `suppress` takes precedence over `promote`.

**Example `.mrf` File:**
```
# Promote all warning, critical warning
promote -severity warning
promote -severity critical_warning
# Suppress the critical warning with id 19-2342
suppress -id 19-2342
```

---

## emconfigutil Utility

Creates the `emconfig.json` configuration file needed for software or hardware emulation.

### Syntax

```bash
emconfigutil --platform <platform_name> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-f`, `--platform` | **(Required)** Target platform |
| `--nd <n>` | Number of devices to emulate (default: 1) |
| `--od <dir>` | Output directory (default: current directory) |
| `-s`, `--save-temps` | Keep intermediate files |
| `--xp <param>` | Additional parameters/properties |
| `-h`, `--help` | Print help |

> **TIP:** The `emconfig.json` location can be set via `$EMCONFIG_PATH`, or it must be in the same directory as the host executable.

**Example:**
```bash
emconfigutil --platform xilinx_u200_gen3x16_xdma_2_202110_1 --nd 2
```

---

## kernelinfo Utility

Extracts and displays information from Xilinx Object (XO) files: kernel names, arguments, offsets, and port data.

### Syntax

```bash
kernelinfo <filename.xo>
```

### Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Print help |
| `-x`, `--xo_path <path>` | Absolute path to XO file |
| `-l`, `--log <file>` | Output to file instead of screen |
| `-j`, `--json` | Output in JSON format |

### Output Sections

The report contains three sections:

1. **Kernel Definition** — name, language, vlnv, debug info, source file
2. **Arguments** — name, address qualifier, ID, port, size, offset, type
3. **Ports** — name, mode, range, data width, port type

**Example Output (Arguments):**
```
=== Arg ===
name: a
addressQualifier: 1
id: 0
port: M_AXI_GMEM
size: 0x8
offset: 0x10
type: int*
```

---

## launch_emulator Utility

Launches QEMU for PS emulation and manages PLsimulator synchronization for embedded hardware emulation.

### Basic Usage

The `v++ --package` step generates `launch_hw_emu.sh` which calls `launch_emulator.py` with the required arguments.

> **TIP:** Press `Ctrl+a h` for QEMU help, `Ctrl+a x` to terminate QEMU.

### Common Options

| Option | Description |
|--------|-------------|
| `-add-env` | Additional environment variables for emulation |
| `-aie-sim-options <file>` | AIE simulator options file |
| `-enable-debug` | Debug mode with separate XTERMs for QEMU and PL |
| `-graphic-qemu` | Start QEMU in GUI mode |
| `-run-app <script>` | Run application script after QEMU boots |
| `-timeout <n>` | Terminate emulation after n seconds (default: 4000 with `-run-app`) |
| `-user-pre-sim-script <tcl>` | Pre-simulation Tcl script |
| `-user-post-sim-script <tcl>` | Post-simulation Tcl script |
| `-verbose` | Enable debug messages |
| `-wcfg-file-path <file>` | XSIM waveform config file |
| `-wdb-File <file>` | Load WDB waveform file |
| `-xtlm-aximm-log` | Generate AXI4 transaction logs |
| `-xtlm-axis-log` | Generate AXI4-Stream transaction logs |

### Advanced Options

| Option | Description |
|--------|-------------|
| `-disable-host-completion-check` | Skip host/test completion check |
| `-enable-tcp-sockets` | Enable TCP sockets |
| `-kill <pid>` | Kill a specific emulator process |
| `-no-reboot` | Exit QEMU instead of rebooting |
| `-no_build` | Check build without running |
| `-no_run` | Build but do not run emulation |
| `-ospi-image <file>` | OSPI image file for booting |
| `-pl-sim-args <args>` | Additional simulator arguments |
| `-pmc-args <args>` | PMC/PMU arguments directly (alternative to args file) |
| `-pmc-args-file <file>` | PMC QEMU arguments file |
| `-print-qemu-version` | Print QEMU version |
| `-qemu-args <args>` | PS QEMU arguments directly |
| `-qemu-dtb <file>` | Override device tree binary |
| `-result-string <str>` | Custom test completion string (default: "TEST PASSED") |

### Versal PS and PMC Arguments for QEMU

**PS qemu_args.txt Options:**

| Argument | Description |
|----------|-------------|
| `-boot mode=<n>` | Boot mode: qspi24=1, qspi32=2, sd0=3, sd1=5, emmc0=6, ospi=8 |
| `-display none` | Disable QEMU display |
| `-hw-dtb <file>` | PS device tree binary |
| `-M arm-generic-fdt` | QEMU machine type for Versal |
| `-serial` | UART configuration (positional: 4 UARTs — first 2 debug, last 2 UART0/UART1) |
| `-sync-quantum <ms>` | Sync frequency with RTL simulator |

**PMC pmc_args.txt Options:**

| Argument | Description |
|----------|-------------|
| `-M microblaze-fdt` | QEMU machine for MicroBlaze |
| `-display none` | Disable display |
| `-device loader,file=<BOOT_bh.bin>,addr=0xf201e000,force-raw` | Boot header file |
| `-device loader,file=<pmc_cdo.bin>,addr=0xF2000000,force-raw` | PMC CDO binary |
| `-device loader,file=<plm.bin>,addr=0xF0200000,force-raw` | PLM firmware |
| `-hw-dtb <file>` | PS device tree binary |

### Zynq UltraScale+ MPSoC PS and PMU Arguments

**PS qemu_args.txt:**

| Argument | Description |
|----------|-------------|
| `-M arm-generic-fdt` | QEMU machine for Zynq UltraScale+ |
| `-serial mon:stdio` | UART configuration |
| `-global xlnx,zynqmp-boot.cpu-num=0` | CPU out of reset |
| `-net nic -net user` | Network interface (per GEM enabled) |
| `-m 4G` | 4 GB DDR |
| `-device loader,file=<bl31.elf>,cpu-num=0` | Arm trusted firmware |
| `-device loader,file=<u-boot.elf>` | U-Boot loader |
| `-hw-dtb <file>` | PS device tree binary |

**PMU pmu_args.txt:**

| Argument | Description |
|----------|-------------|
| `-M microblaze-fdt` | QEMU machine for PMU |
| `-device loader,file=<pmufw.elf>` | PMU firmware |
| `-machine-path <path>` | Path for shared RAM and remote-port sockets |
| `-display none` | Disable display |
| `-hw-dtb <file>` | PMU device tree binary |

### Zynq 7000 PS Arguments

| Argument | Description |
|----------|-------------|
| `-M arm-generic-fdt-7series` | QEMU machine for Zynq 7000 |
| `-serial /dev/null -serial mon:stdio` | UART configuration |
| `-boot mode=5` | SD boot mode |
| `-kernel <u-boot.elf>` | Guest software to load |
| `-machine linux=on` | Make QEMU a Linux loader |

---

## manage_ipcache Utility

Manages the HLS IP cache repository to improve build performance by reusing synthesis results.

### Syntax

```bash
manage_ipcache --cache <dir> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-c`, `--cache <dir>` | **(Required)** IP cache directory |
| `-d`, `--disk_space <MB>` | Keep entries fitting in specified MB |
| `-k`, `--keep_top <N>` | Keep only N most recently used entries |
| `-o`, `--outfile <file>` | Report stats to file |
| `-p`, `--purge` | Delete ALL cache entries |
| `-r`, `--report` | Report stats to stdout |
| `-u`, `--unused` | Delete entries never used (no cache hits) |
| `-h`, `--help` | Print help |

**Example:**
```bash
manage_ipcache --cache ./ip_cache --report
```

Returns 0 on success, -1 on error.

---

## package_xo Command

A Vivado Tcl command that packages RTL kernels into Xilinx Object (XO) files for use with v++ linking.

### Syntax

```tcl
package_xo -kernel_name <name> -xo_path <path> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `-kernel_name <name>` | **(Required)** RTL kernel name |
| `-xo_path <path>` | **(Required)** Output XO file path |
| `-force` | Overwrite existing XO file |
| `-kernel_xml <path>` | Existing kernel XML file |
| `-output_kernel_xml <path>` | Write generated kernel XML to file |
| `-design_xml <path>` | Existing design XML file |
| `-ip_directory <path>` | Packaged IP directory |
| `-parent_ip_directory <path>` | Parent IP directory (multi-IP) |
| `-kernel_files <files>` | Kernel source files |
| `-kernel_xml_args <args>` | Kernel arguments: `{name:addressQualifier:id:port:size:offset:type:memSize}` |
| `-kernel_xml_pipes <args>` | Kernel pipes: `{name:width:depth}` |
| `-kernel_xml_connections <args>` | Kernel connections: `{srcInst:srcPort:dstInst:dstPort}` |
| `-ctrl_protocol <proto>` | Control protocol: `ap_ctrl_hs` (default), `ap_ctrl_chain`, `ap_ctrl_none`, `user_managed` |
| `-quiet` | Execute quietly, suppress messages |
| `-verbose` | Return all messages |

**Example:**
```tcl
package_xo -xo_path Vadd_A_B.xo -kernel_name Vadd_A_B -ctrl_protocol ap_ctrl_chain -ip_directory ./ip
```

---

## RTL Kernel XML File

The `kernel.xml` file describes RTL kernel attributes, ports, arguments, and connections for use in the Vitis flow.

> **TIP:** The `package_xo` command auto-generates `kernel.xml` from `component.xml`, so manual creation is usually unnecessary.

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root versionMajor="1" versionMinor="6">
  <kernel name="my_kernel" language="ip_c"
    vlnv="mycompany.com:kernel:my_kernel:1.0"
    attributes="" preferredWorkGroupSizeMultiple="0"
    workGroupSize="1" interrupt="true"
    hwControlProtocol="ap_ctrl_hs">
    <ports>
      <port name="s_axi_control" mode="slave" range="0x1000"
        dataWidth="32" portType="addressable" base="0x0"/>
      <port name="m00_axi" mode="master"
        range="0xFFFFFFFFFFFFFFFF" dataWidth="512"
        portType="addressable" base="0x0"/>
    </ports>
    <args>
      <arg name="ptr0" addressQualifier="1" id="0"
        port="m00_axi" size="0x8" offset="0x010"
        type="int*" hostOffset="0x0" hostSize="0x8"/>
    </args>
  </kernel>
</root>
```

### Tag Reference

**`<kernel>` Attributes:**

| Attribute | Description |
|-----------|-------------|
| `name` | Kernel name |
| `language` | Always `ip_c` for RTL kernels |
| `vlnv` | Must match `vendor:library:name:version` from IP `component.xml` |
| `attributes` | Reserved (empty string) |
| `preferredWorkGroupSizeMultiple` | Reserved (set to 0) |
| `workGroupSize` | Reserved (set to 1) |
| `interrupt` | `"true"` if kernel has interrupt |
| `hwControlProtocol` | `ap_ctrl_hs`, `ap_ctrl_chain`, `ap_ctrl_none`, `user_managed` |

**`<port>` Attributes:**

| Attribute | Values | Description |
|-----------|--------|-------------|
| `name` | string | Port name (AXI4-Lite **must** be `S_AXI_CONTROL`) |
| `mode` | `master`, `slave`, `write_only`, `read_only` | AXI4 master/slave, AXI4-Stream write/read |
| `range` | hex | Address space range |
| `dataWidth` | int | Data width in bits (default: 32) |
| `portType` | `addressable`, `stream` | Memory-mapped or streaming |
| `base` | hex | Base address (0x0 for AXI4, N/A for stream) |

**`<arg>` Attributes:**

| Attribute | Description |
|-----------|-------------|
| `name` | Software argument name |
| `addressQualifier` | 0=scalar, 1=global memory, 2=local, 3=constant, 4=pipe |
| `id` | Sequential ID for argument ordering |
| `port` | Port name the arg connects to |
| `size` | Argument size in bytes |
| `offset` | Register memory address |
| `type` | C data type (e.g., `int*`, `float*`) |
| `hostOffset` | Reserved (set to 0x0) |
| `hostSize` | Argument size (default: 4 bytes) |
| `memSize` | FIFO depth for AXI4-Stream ports |

---

## platforminfo Utility

Reports platform metadata: interfaces, clocks, SLRs, resources, and memory.

### Syntax

```bash
platforminfo [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Print help |
| `-l`, `--list` | List available platforms |
| `-e`, `--extended` | Extended platform listing (use with `--list`) |
| `-p`, `--platform <name\|path>` | Platform to query (name or .xpfm path) |
| `-d`, `--hw <path>` | Hardware platform (.xsa) to query |
| `-s`, `--sw <path>` | Software platform (.spfm) to query |
| `-j`, `--json [path]` | JSON format output; optional JSON path for subtree |
| `-k`, `--keys` | List JSON keys |
| `-o`, `--output <file>` | Output to file |
| `-v`, `--verbose` | Full metadata report |
| `-f`, `--force` | Overwrite output file |

### Report Sections

The default report includes:

1. **Basic Platform Information** — name, description, hardware/emulation support
2. **Hardware Platform Information** — vendor, device, board, version, FPGA family
3. **Interface Information** — PCIe type and IDs
4. **Clock Information** — available clocks with index, frequency, and status (scalable/fixed)
5. **Valid SLRs** — available SLR names
6. **Resource Availability** — total and per-SLR: LUTs, FFs, BRAMs, DSPs, URAMs
7. **Memory Information** — DDR/PLRAM/HBM banks with SP tags, SLR assignment, max masters, consumption mode
8. **Software Platform Information** — runtime configs, processor groups, boot images

**Example:**
```bash
platforminfo -p $PLATFORM_REPO_PATHS/xilinx_u200_gen3x16_xdma_2_202110_1.xpfm
platforminfo --json="hardwarePlatform.devices[0].name" --platform xilinx_u200
```

### Memory Consumption Modes

| Mode | Description |
|------|-------------|
| `default` | Used automatically when `--connectivity.sp` is not specified |
| `automatic` | Used when max interfaces of `default` memory are filled |
| `explicit` | Only used when explicitly specified (e.g., PLRAM) |

---

## vitis-run Command

Runs C-simulation, C/RTL Co-simulation, Vivado implementation, or Tcl scripts on HLS components.

### Syntax

```bash
vitis-run --mode hls <action> --config <file> [--work_dir <dir>]
```

### Actions

| Action | Description |
|--------|-------------|
| `--csim` | Run C-simulation |
| `--cosim` | Run C/RTL Co-simulation |
| `--impl` | Run Vivado implementation (OOC) |
| `--package` | Generate IP or XO from RTL |
| `--tcl <script>` | Run a Vitis HLS Tcl script |

### Examples

**C-Simulation:**
```bash
vitis-run --mode hls --csim --config ./hls_csim.cfg --work_dir newTest
```

**Co-Simulation:**
```bash
vitis-run --mode hls --cosim --config ./cosim.cfg --work_dir myHLS
```

**Vivado Implementation:**
```bash
vitis-run --mode hls --impl --config ./impl.cfg --work_dir myHLS
```

**Run Tcl Script:**
```bash
vitis-run --mode hls --tcl dct-build.tcl
```

> **TIP:** Use `write_ini` at the end of a Tcl script to generate a config file for use with `v++ -c --mode hls`.

---

## xrt-smi Utility

A standalone XRT utility for validating and identifying installed accelerator cards, including memory, interfaces, platform, and system information.

### Setup

```bash
# bash
source /opt/xilinx/xrt/setup.sh
# csh
source /opt/xilinx/xrt/setup.csh
```

### Usage

```bash
xrt-smi --help
```

The `xrt-smi` interacts with the **user function** partition of the accelerator card. For management functions, use `xbmgmt`.

Full documentation: https://xilinx.github.io/XRT/master/html/xrt-smi.html

---

## xbmgmt Utility

AMD Board Management utility for card installation, firmware flashing, and administration. Requires `sudo` privileges.

### Setup

```bash
# bash
source /opt/xilinx/xrt/setup.sh
# csh
source /opt/xilinx/xrt/setup.csh
```

### Usage

```bash
xbmgmt --help
xbmgmt help <subcommand>
```

Full documentation: https://xilinx.github.io/XRT/master/html/xbmgmt.html

---

## xclbinutil Utility

Creates, modifies, and reports `xclbin` content — the binary container for FPGA configuration, kernel metadata, and connectivity.

### Syntax

```bash
xclbinutil [options]
```

### Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Print help |
| `-i`, `--input <file>` | Input xclbin file |
| `-o`, `--output <file>` | Output xclbin file |
| `--target <hw\|hw_emu>` | Target flow |
| `--private-key <file>` | Private key for signing |
| `--certificate <file>` | Certificate for signing/validation |
| `--digest-algorithm <alg>` | Digest algorithm (default: sha512) |
| `--validate-signature` | Validate xclbin signature |
| `-v`, `--verbose` | Verbose output |
| `-q`, `--quiet` | Minimal output |
| `--migrate-forward` | Migrate to new binary format |
| `--add-section <s>:<fmt>:<file>` | Add a section |
| `--add-replace-section <s>:<fmt>:<file>` | Add or replace a section |
| `--add-merge-section <s>:<fmt>:<file>` | Add or merge a section |
| `--remove-section <name>` | Remove a section |
| `--dump-section <s>:<fmt>:<file>` | Dump a section to file |
| `--replace-section <s>:<fmt>:<file>` | Replace a section |
| `--key-value [USER\|SYS]:<key>:<value>` | Set key-value pair |
| `--remove-key <key>` | Remove a user key |
| `--add-signature <sig>` | Add user-defined signature |
| `--remove-signature` | Remove signature |
| `--get-signature` | Get user-defined signature |
| `--info` | Report xclbin content |
| `--list-sections` | List all possible section names |
| `--version` | Print version |
| `--force` | Force file overwrite |

### Common Use Cases

```bash
# Report xclbin information
xclbinutil --info --input binary_container_1.xclbin

# Extract bitstream
xclbinutil --dump-section BITSTREAM:RAW:bitstream.bit --input binary_container_1.xclbin

# Extract build metadata
xclbinutil --dump-section BUILD_METADATA:HTML:buildMetadata.json --input binary_container_1.xclbin

# Remove a section
xclbinutil --remove-section BITSTREAM --input in.xclbin --output out.xclbin
```

### --info Report Sections

The `--info` flag reports:

1. **xclbin Information** — generator, version, kernels, UUID, sections
2. **Hardware Platform** — vendor, board, device, version
3. **Clocks** — name, index, type, frequency
4. **Memory Configuration** — bank name, index, type, base address, size, usage
5. **Kernel Information** — function signature, ports (name/mode/width/type), instances with argument mapping
6. **Tool Generation** — v++ command line used to build

---

## xrt.ini File

The XRT runtime initialization file configures debugging, profiling, and logging at application startup.

### Location

Place `xrt.ini` in the same directory as the host executable, or set:
```bash
export XRT_INI_PATH=/path/to/xrt.ini
```

### Format

```ini
# Comments start with ; or #
[Group]
key = value
```

### Runtime Group

| Key | Values | Description |
|-----|--------|-------------|
| `api_checks` | `true` (default) / `false` | Enable/disable OpenCL API checks |
| `cpu_affinity` | `{N,N,...}` | Pin runtime threads to specific CPUs |
| `exclusive_cu_context` | `true` / `false` | Acquire exclusive CU access for low-level AXI R/W |
| `force_program_xclbin` | `true` / `false` | Force xclbin reload even if already loaded |
| `runtime_log` | `null` (default) / `console` / `syslog` / `<filename>` | Log destination |
| `verbosity` | `0`–`7` (default: 4) | Log verbosity level |

### Debug Group

| Key | Values | Description |
|-----|--------|-------------|
| `aie_profile` | `true` / `false` | Enable AIE hardware performance counter polling |
| `aie_trace` | `true` / `false` | Enable AIE event trace collection (hw only) |
| `aie_status` | `true` / `false` | Enable AIE status polling |
| `aie_status_interval_us` | int (default: 1000) | AIE status polling interval in μs |
| `continuous_trace` | `true` / `false` | Continuous dump of trace files |
| `device_counters` | `true` / `false` | Device counter offload only (no trace) |
| `device_trace` | `off` (default) / `fine` / `coarse` / `accel` | PL monitor data collection level |
| `host_trace` | `true` / `false` | Host code trace |
| `native_xrt_trace` | `true` / `false` | XRT Native C/C++ API trace |
| `pl_deadlock_detection` | `true` / `false` | PL kernel deadlock detection |
| `power_profile` | `true` / `false` | Poll power data during execution |
| `power_profile_interval_ms` | int (default: 20) | Power polling interval in ms |
| `profile_api` | `true` / `false` | HAL API access for reading profiling counters |
| `stall_trace` | `off` / `all` / `dataflow` / `memory` / `pipe` | Device stall capture type |
| `trace_buffer_offload_interval_ms` | int (default: 10) | Device-to-host data transfer interval |
| `trace_buffer_size` | string (default: `1M`) | Memory allocated for trace capture |
| `trace_file_dump_interval_s` | int (default: 5) | Interval between trace file dumps |
| `vitis_ai_profile` | `true` / `false` | Vitis AI application profiling |
| `xocl_debug` | `true` / `false` | Generate xocl.log debug file |
| `xrt_trace` | `true` / `false` | Low-level HW shim function trace |

### AIE_profile_settings Group

Applied when `aie_profile=true` in `[Debug]`.

| Key | Values | Description |
|-----|--------|-------------|
| `graph_based_aie_metrics` | `<graph>:<kernel>:<metric_set>` | AIE core module metrics per graph |
| `graph_based_aie_memory_metrics` | `<graph>:<kernel>:<metric_set>` | AIE memory module metrics per graph |

**Core Metric Sets:** `heat_map`, `stalls`, `execution`, `floating_point`, `write_bandwidths`, `read_bandwidths`, `aie_trace`

**Memory Metric Sets:** `conflicts`, `dma_locks`, `dma_stalls_s2mm`, `dma_stalls_mm2s`, `write_bandwidths`, `read_bandwidths`

### Emulation Group

| Key | Values | Description |
|-----|--------|-------------|
| `debug_mode` | `batch` / `gui` / `off` | Emulation debug mode |
| `print_infos_in_console` | `true` / `false` | Print emulation messages to console |
| `user_pre_sim_script` | `<path>` | Pre-simulation Tcl script |
| `user_post_sim_script` | `<path>` | Post-simulation Tcl script |

### Example xrt.ini

```ini
# Runtime configuration
[Runtime]
runtime_log = console

# Debug and profiling
[Debug]
device_trace = fine
native_xrt_trace = true
stall_trace = all
trace_buffer_size = 64M
continuous_trace = true
aie_profile = true

# AIE profiling settings
[AIE_profile_settings]
graph_based_aie_metrics = all:all:heat_map

# Emulation settings
[Emulation]
debug_mode = batch
```

---

## Best Practices

1. **Use configuration files** instead of long command lines — they are reusable, organized, and support section headers.
2. **Separate config files** for separate processes: one for HLS compilation, one for linking, one for packaging.
3. **Enable profiling incrementally** — start with `--profile.exec` and `device_trace=coarse`, then refine.
4. **Use `--save-temps`** during development to preserve intermediate files for debugging.
5. **IP caching** (`--remote_ip_cache`) significantly reduces rebuild times for unchanged kernels.
6. **HLS directive strategy**: Start with `pipeline` on inner loops, then `array_partition` for parallel access, then `dataflow` for task-level parallelism.
7. **Check platform resources** with `platforminfo` before mapping kernels to SLRs and memory banks.
8. **Use `xclbinutil --info`** to verify connectivity, clocks, and kernel mapping after the build.
9. **Message rule files** help manage build noise — promote critical warnings and suppress known benign messages.

---

## Quick Reference

| Tool / Command | Purpose |
|----------------|---------|
| `v++ -c` | Compile kernels |
| `v++ -c --mode hls` | Compile HLS components |
| `v++ -c --mode aie` | Compile AI Engine graphs |
| `v++ -l` | Link kernels into system |
| `v++ -p` | Package for deployment |
| `vitis-run --mode hls --csim` | C-simulation of HLS component |
| `vitis-run --mode hls --cosim` | C/RTL co-simulation |
| `vitis-run --mode hls --impl` | Vivado implementation of HLS |
| `emconfigutil` | Generate emulation config |
| `kernelinfo` | Inspect XO file contents |
| `launch_emulator.py` | Launch QEMU + PL simulator |
| `manage_ipcache` | Manage HLS IP cache |
| `package_xo` | Package RTL kernel as XO (Vivado Tcl) |
| `platforminfo` | Query platform metadata |
| `xrt-smi` | XRT card validation/info |
| `xbmgmt` | Card administration (sudo) |
| `xclbinutil` | Inspect/modify xclbin files |

---

> **Source**: AMD UG1702 (v2025.2) — *Vitis Reference Guide*, November 20, 2025
