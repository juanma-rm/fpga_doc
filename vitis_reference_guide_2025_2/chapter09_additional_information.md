# Chapter 9: Additional Information

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 9 (pp. 430–484)

## Overview

This chapter provides supplementary reference material for the AMD Vitis™ tools, including the output directory structure produced by various `v++` commands and IDE builds, as well as the complete Python XSDB command reference for debug operations.

---

## Table of Contents

| Section | Description |
|---|---|
| [Output Structure of the Vitis Tools](#output-structure-of-the-vitis-tools) | Overview of output organization |
| [Output Directories of the v++ Command](#output-directories-of-the-v-command) | Compile and link output trees |
| [Output Directories of v++ -c --mode aie](#output-directories-of-v---c---mode-aie) | AI Engine compilation output tree |
| [Output Directories of v++ -c --mode hls](#output-directories-of-v---c---mode-hls) | HLS compilation output tree |
| [Output Directories of the Vitis Unified IDE](#output-directories-of-the-vitis-unified-ide) | IDE project output structure |
| [Python XSDB Commands](#python-xsdb-commands) | Complete Python XSDB command reference |

---

## Output Structure of the Vitis Tools

The Vitis tools produce organized output directories containing compiled results, reports, logs, and intermediate files. The structure depends on whether the command-line flow (`v++`) or the Vitis Unified IDE is used.

---

## Output Directories of the v++ Command

### v++ Compile (vadd example)

The `v++ -c` command produces the following output structure:

```
<build_dir>/
├── build/
│   ├── logs/
│   │   └── <kernel>/
│   │       ├── <kernel>.steps.log
│   │       ├── <kernel>_vitis_hls.log
│   │       └── v++.log
│   ├── reports/
│   │   └── <kernel>/
│   │       ├── hls_reports/
│   │       │   └── <kernel>_csynth.rpt
│   │       └── system_estimate_<name>.xtxt
│   └── <kernel>/
│       └── <kernel>/
│           └── <kernel>/
│               ├── hls.app
│               ├── ip/                    # Packaged IP
│               │   ├── component.xml
│               │   ├── drivers/
│               │   ├── hdl/
│               │   │   ├── verilog/
│               │   │   └── vhdl/
│               │   └── hls_files/
│               ├── kernel.xml
│               └── solution/
│                   ├── syn/
│                   │   ├── report/        # Synthesis reports
│                   │   ├── verilog/       # RTL output
│                   │   └── vhdl/
│                   └── impl/
│                       └── export.xo
├── <kernel>.xo                            # Compiled kernel object
├── <kernel>.xo.compile_summary            # Compile summary for Analyzer
└── <kernel>-compile.cfg                   # Configuration used
```

### Key Output Files

| File | Description |
|---|---|
| `<kernel>.xo` | Compiled Xilinx Object file |
| `*.compile_summary` | Summary file for Vitis Analyzer |
| `csynth.rpt` | C Synthesis report |
| `csynth.xml` | Machine-readable synthesis data |
| `component.xml` | IP-XACT component descriptor |
| `kernel.xml` | Kernel interface descriptor |

### v++ Link

The `v++ -l` command produces:

```
<build_dir>/
├── <name>.xclbin                          # Device binary
├── <name>.xclbin.link_summary             # Link summary for Analyzer
├── <name>.xclbin.info                     # Binary information
├── <name>.build/
│   ├── link/
│   │   ├── int/                           # Intermediate files
│   │   │   ├── address_map.xml
│   │   │   ├── systemDiagramModel.json
│   │   │   └── xo/                        # Extracted XO contents
│   │   ├── vivado/
│   │   │   └── vpl/
│   │   │       └── prj/                   # Vivado project
│   │   │           └── prj.xpr
│   │   └── sys_link/
│   │       ├── cfgraph/
│   │       └── iprepo/                    # IP repository
│   ├── logs/
│   │   └── link/
│   │       ├── link.steps.log
│   │       └── v++.log
│   └── reports/
│       └── link/
│           ├── automation_summary.txt
│           └── system_estimate_<name>.xtxt
└── <name>-link.cfg
```

---

## Output Directories of v++ -c --mode aie

The AI Engine compilation produces:

```
<component>/
├── Work/
│   ├── aie/                               # Per-tile compiled code
│   │   └── <col>_<row>/
│   │       ├── Release/
│   │       └── src/
│   ├── arch/                              # Architecture description
│   ├── config/                            # Configuration files
│   ├── logs/                              # Compilation logs
│   ├── ps/
│   │   ├── cdo/                           # Configuration Data Objects
│   │   └── c_rts/                         # C runtime support
│   ├── reports/                           # Compilation reports
│   └── temp/                              # Temporary build files
├── logs/
│   ├── hls_compile.log
│   └── xcd.log
├── <component>.hlscompile_summary
├── reports/
│   ├── hls_compile.rpt
│   └── v++_compile_<name>_guidance.html
└── vitis-comp.json                        # Component descriptor
```

### Key Directories

| Directory | Description |
|---|---|
| `Work/aie/<col>_<row>/` | Per-tile compiled AI Engine code |
| `Work/arch/` | Array architecture description |
| `Work/ps/cdo/` | CDO files for device programming |
| `Work/ps/c_rts/` | C runtime support files |
| `Work/reports/` | Detailed compilation reports |

---

## Output Directories of v++ -c --mode hls

The HLS compilation (e.g., DCT example) produces:

```
<component>/
├── <function>/
│   ├── hls/
│   │   └── <function>/
│   │       ├── ip/
│   │       │   ├── component.xml
│   │       │   ├── constraints/
│   │       │   ├── drivers/
│   │       │   │   └── <function>_v1_0/
│   │       │   │       ├── data/
│   │       │   │       └── src/           # Auto-generated C drivers
│   │       │   ├── hdl/
│   │       │   │   ├── verilog/           # Verilog RTL
│   │       │   │   └── vhdl/              # VHDL RTL
│   │       │   └── hls_files/
│   │       ├── kernel.xml
│   │       └── syn/
│   │           ├── report/                # Synthesis reports
│   │           │   ├── csynth.rpt
│   │           │   ├── csynth.xml
│   │           │   └── <function>_csynth.rpt
│   │           ├── verilog/
│   │           └── vhdl/
│   └── <function>.xo                      # Compiled kernel object
├── logs/
├── reports/
│   ├── hls_compile.rpt
│   └── v++_compile_<name>_guidance.html
└── vitis-comp.json
```

---

## Output Directories of the Vitis Unified IDE

Unlike the command-line flow, the Vitis IDE defines the project structure. A system design project has four associated projects:

| Project | Description |
|---|---|
| **Top-level System Project** | Consolidated system design with packaged output |
| **Software Application Project** | Software source and compiled executables |
| **PL Kernels Project** | PL kernel source and compiled XO files |
| **Hardware Linking Project** | Linked hardware platform and device binary |

> **TIP:** Each project below starts with the `Emulation-HW` folder, which holds the hardware emulation build content.

### Top-Level System Project

```
<system_project>/
├── Emulation-HW/
│   ├── binary_container_1.xclbin
│   ├── binary_container_1.xclbin.package_summary
│   ├── package/
│   │   ├── sd_card/                       # SD card image contents
│   │   │   ├── boot.scr
│   │   │   ├── emconfig.json
│   │   │   ├── Image
│   │   │   ├── <app_name>
│   │   │   └── <name>.xclbin
│   │   ├── sd_card.img
│   │   └── sim/
│   │       └── behav_waveform/
│   ├── package.build/
│   │   ├── logs/
│   │   └── reports/
│   └── package.cfg
├── _ide/
│   └── launch/                            # Debug launch configurations
└── <system_project>.sprj
```

### Software Application Project

```
<app_project>/
├── Emulation-HW/
│   ├── src/
│   │   └── host.o                         # Compiled object
│   ├── <app_name>                         # Executable
│   ├── emconfig.json
│   ├── SystemDebugger_<name>/
│   │   ├── device_trace_0.csv
│   │   ├── native_trace.csv
│   │   ├── summary.csv
│   │   ├── xrt.ini
│   │   └── xrt.run_summary
│   └── xsa.xml
├── src/
│   └── host.cpp                           # Host source code
└── <app_project>.prj
```

### PL Kernels Project

```
<kernels_project>/
├── Emulation-HW/
│   ├── build/
│   │   ├── logs/
│   │   ├── reports/
│   │   │   └── <kernel>/
│   │   │       ├── hls_reports/
│   │   │       └── system_estimate_<name>.xtxt
│   │   └── <kernel>/
│   │       └── <kernel>/
│   │           ├── <kernel>/              # Vitis HLS project
│   │           │   ├── hls.app
│   │           │   ├── ip/                # Packaged IP
│   │           │   ├── kernel.xml
│   │           │   └── solution/
│   │           │       ├── impl/
│   │           │       │   └── export.xo
│   │           │       └── syn/
│   │           │           └── report/
│   │           └── vitis_hls.log
│   ├── <kernel>.xo
│   └── <kernel>.xo.compile_summary
├── src/
│   └── <kernel>.cpp                       # Kernel source code
└── <kernels_project>.prj
```

### Hardware Linking Project

```
<hw_link_project>/
├── Emulation-HW/
│   ├── <name>.build/
│   │   ├── link/
│   │   │   ├── int/                       # Intermediate files
│   │   │   │   ├── address_map.xml
│   │   │   │   ├── systemDiagramModel.json
│   │   │   │   └── xo/
│   │   │   ├── vivado/
│   │   │   │   └── vpl/
│   │   │   │       └── prj/               # Vivado project
│   │   │   └── sys_link/
│   │   │       └── iprepo/
│   │   ├── logs/
│   │   └── reports/
│   ├── <name>.xclbin                      # Device binary
│   ├── <name>.xclbin.link_summary
│   └── <name>-link.cfg
└── <hw_link_project>.prj
```

---

## Python XSDB Commands

This section provides the complete Python XSDB command reference. These commands implement the debug functions supported by XSDB using Python APIs. Commands are organized by category.

### Breakpoints

#### bpadd

Add a breakpoint.

```python
t = self.session.targets(id=2)
b1 = t.bpadd(addr='main')
```

| Option | Python Example |
|---|---|
| `-addr <address>` | `t.bpadd(addr='main')` |
| `-file <file>` | `t.bpadd(file='helloworld.c', line=89)` |
| `-line <line>` | `t.bpadd(file='helloworld.c', line=89)` |
| `-type <type>` | `t.bpadd(addr='main', type='hw', mode=2)` |
| `-mode <mode>` | `t.bpadd(addr='main', type='hw', mode=2)` |
| `-enable <mode>` | `t.bpadd(addr='main', enable=1)` |
| `-ct-input/output` | `t.bpadd(ct_input=0, ct_output=8, skip_on_step=1)` |
| `-skip-on-step` | `t.bpadd(ct_input=0, ct_output=8, skip_on_step=1)` |
| `-target-id` | `t.bpadd(addr='main', target_id='all')` |

Combined file and line syntax:
```python
t.bpadd('helloworld.c:90', type='hw', mode=3)
```

#### bpdisable

```python
t.bpdisable(bp_ids=1)
t.bpdisable(bp_ids=[1, 2])
t.bpdisable('--all')
```

#### bpenable

```python
t.bpenable(bp_ids=1)
t.bpenable(bp_ids=[1, 2])
t.bpenable('--all')
```

#### bplist

```python
t.bplist()
```

#### bpremove

```python
t.bpremove(bp_ids=2)
t.bpremove(bp_ids=[1, 2])
t.bpremove('--all')
```

#### bpstatus

```python
t.bpstatus(bp_id=3)
```

---

### Connections

#### connect

```python
s.connect(host="xhdbfarmrk9", port=3121)
s.connect("--new", url="TCP:xhdbfarmrk9:3121")
s.connect("--list")
s.connect(set="tcfchan#0")
```

#### disconnect

```python
s.disconnect()
s.disconnect(chan="tcfchan#1")
```

#### gdbremote connect / disconnect

```python
session.gdb_connect('localhost:3121')
session.gdb_disconnect(1)
```

#### targets

```python
s.targets()                                    # List all targets
s.targets(1)                                   # Select target by ID
s.targets(id=1)                                # Select target by ID
s.targets("--set", filter="name =~ #1")        # Set active target
s.targets("--no_case", filter="name =~ ARM*")  # Case-insensitive filter
s.targets(filter="name =~ ARM*")               # Filter targets
s.targets("--target_properties")               # Show properties
```

---

### Device

#### device_authjtag

```python
self.session.device_authjtag("tests/elfs/versal/vck190.pdi")
```

#### device_program

```python
self.session.device_program("tests/elfs/versal/vck190.pdi")
```

#### device_status

```python
self.session.device_status()
s.device_status('error_status')    # Query specific JTAG register
```

#### fpga

```python
tgt.fpga(file='tests/elfs/zynq/zc702.bit')
tgt.fpga('--partial', file='tests/elfs/zynq/zc702.bit')
tgt.fpga('--no_revision_check', file='tests/elfs/zynq/zc702.bit')
tgt.fpga('--skip_compatibility_check', file='tests/elfs/zynq/zc702.bit')
tgt.fpga('--state')
tgt.fpga('--config_status')
tgt.fpga('--ir_status')
tgt.fpga('--boot_status')
tgt.fpga('--timer_status')
tgt.fpga('--cor0_status')
tgt.fpga('--cor1_status')
tgt.fpga('--wbstart_status')
```

---

### Download

#### dow

```python
t.dow('tests/elfs/zynq/core0zynq.elf')
t.dow('tests/elfs/zynq/data', '-d', addr=0x10000000)                    # --data
t.dow('tests/elfs/zynq/core0zynq.elf', '-c', relocate_sections=0x30000000)  # --clear
t.dow('--skip_tcm_clear', 'tests/elfs/zynq/core0zynq.elf')
t.dow('tests/elfs/zynq/core0zynq.elf', '-f')                            # --force
t.dow('tests/elfs/zynq/core0zynq.elf', '-b')                            # --bypass_cache_synq
t.dow('tests/elfs/zynq/core0zynq.elf', '-v')                            # -vaddr
```

#### verify

```python
t.verify('tests/elfs/zynq/core0zynq.elf')
t.verify('tests/elfs/zynq/core0zynq.elf', '-d', addr=0x10000000)        # --data
t.verify('tests/elfs/zynq/core0zynq.elf', '-f')                         # --force
t.verify('tests/elfs/zynq/core0zynq.elf', '-v')                         # -vaddr
```

---

### IPI

#### plm

```python
s.plm_copy_debug_log(0x0)
s.plm_set_debug_log(0x0, 0x4000)
s.plm_set_log_level(4)
s.plm_log(0x0, 0x4000)
f = open('tests/data/plm.log', 'w')
s.plm_log(0x0, 0x4000, handle=f)
```

#### pmc

```python
s.pmc('generic', [0x10241, 0x1c000000], response_size=1)
s.pmc(cmd='generic', data=[0x1030115, 0xffff0000, 0x100], response_size=2)
s.pmc(cmd='generic', data=[0x1030115, 0xffff0000, 0x100], ipi=5, response_size=2)
```

---

### JTAG

#### jtag claim / disclaim

```python
jt.claim()
jt.disclaim()
```

#### jtag device_properties

```python
jt.device_properties(0x6ba00477)
props = {'idcode': 0x6ba00477, 'irlen': 4}
jt.device_properties(props=props)
```

#### jtag frequency

```python
jt.frequency()           # Get current frequency
jt.frequency('-l')       # List available frequencies
jt.frequency(freq)       # Set frequency
```

#### jtag lock / unlock

```python
jt.lock(100)             # Lock with timeout (ms)
jt.unlock()
```

#### jtag sequence

```python
s = self.session
jt3 = s.jtag_targets(3)
jseq = jt3.sequence()
jseq.state("RESET")
jseq.irshift(register='bypass', state="IRUPDATE")
jseq.drshift(capture=True, state="IDLE", tdi=0, bit_len=2)
jseq.delay(100)
jseq.get_pin('TDI')
jseq.set_pin('TDI', 0)
jseq.atomic()
jseq.run()
jseq.clear()
del jseq                 # Delete sequence
```

#### jtag servers

```python
jt.servers()
jt.servers('-l')         # List
jt.servers('-f')         # Format
jt.servers(open='xilinx-xvc:localhost:10200')
jt.servers(close='xilinx-xvc:localhost:10200')
```

#### jtag skew

```python
jt.skew()                # Get/set clock skew
```

#### jtag targets

```python
self.session.jtag_targets()
self.session.jtag_targets(id=2)
self.session.jtag_targets('-s', filter="name == xcvc1902")
self.session.jtag_targets('-n', filter="name !~ XCVC*")
self.session.jtag_targets(filter="name == xcvc1902")
self.session.jtag_targets('-t')     # Target properties
self.session.jtag_targets('-o')     # Open
self.session.jtag_targets('-c')     # Close
```

---

### Memory

#### init_ps

```python
init_data = [
    "mask_write 0 0x00001FFF 0x00000001",
    "mask_delay 1",
    "mask_poll 4 1 1"
]
t.init_ps(init_data)
```

#### mask_poll / mask_write

```python
t.mask_poll(4, 1, 1)
t.mask_write(0, 0xFF, 0xFFFF)
```

#### memmap

```python
t.memmap(addr=0xFC000000, size=0x1000, flags=3)
t.memmap(addr=0xFC000000, size=0x1000, flags=3, alignment=4)
t.memmap('-l')                        # List memory maps
t.memmap('-c', addr=0xFC000000)       # Clear mapping
t.memmap(file='tests/elfs/zynq/core0zynq.elf', relocate_sections=0x20000000)
t.memmap(addr=0xFC000000, size=0x1000, flags=3, OSA=1)
```

#### mrd (Memory Read)

```python
t.mrd(0x00100000, word_size=4, size=10)
t.mrd(0x00100002, '-f', word_size=4, size=10)           # --force
x = t.mrd(0x100000, '-v', word_size=4, size=20)         # --value (returns data)
t.mrd(0x00100000, '-b', word_size=8, size=20, file="tests/data/mrd.bin")  # --bin
t.mrd(0x100, address_space="APR")                        # Address space
t.mrd(0x00100000, '-u', word_size=4, size=10)            # --unaligned-access
```

#### mwr (Memory Write)

```python
t.mwr(0x00100000, word_size=4, size=10, words=[0x01, 0x02, 0x03])
t.mwr(0x00100000, '-f', word_size=4, size=10, words=[0x01, 0x02, 0x03])   # --force
t.mwr(0x00100000, '-b', word_size=4, size=5, file="tests/data/mrd.bin")   # --bin
t.mwr(0x80090088, address_space="AP1", words=[0x03186004])
t.mwr(0x00100000, '-u', word_size=4, size=10, words=[0x01, 0x02, 0x03])   # --unaligned
```

#### osa

```python
t.osa('--disable', file='tests/elfs/zynq/core0zynq.elf')
t.osa('--fast_exec', file='tests/elfs/zynq/core0zynq.elf')
t.osa('--fast_step', file='tests/elfs/zynq/core0zynq.elf')
```

---

### Miscellaneous

#### configparams

```python
s.configparams()                     # List all parameters
s.configparams("silent-mode")        # Get specific parameter
s.configparams("silent-mode", 1)     # Set parameter value
s.configparams("--all")              # Show all parameters
```

#### loadhw / loadipxact

```
loadhw -hw <hardware_spec> -list -mem-ranges [list {start1 end1} {start2 end2}]
loadipxact <xml-file> [-clear] [-list]
```

#### mb_drrd / mb_drwr

```python
s.mb_drrd(3, 28)
s.mb_drrd(0x07, 288, user=bscan, which=which, target_id=target_id)
s.mb_drwr(1, 0x282, 10)
s.mb_drwr(0x71, value, 8, user=bscan, which=which)
```

#### mdm_drrd / mdm_drwr

```python
s.mdm_drrd(0, 32)
s.mdm_drwr(8, 0x40, 8)
```

#### version

```python
s.version('-s')
```

#### xsdbserver

```python
s.xsdbserver_start()
s.xsdbserver_stop()
s.xsdbserver_disconnect()
s.xsdbserver_version()
```

---

### Registers

#### rrd (Register Read)

```python
s.targets(2)
s.rrd()                             # Read all registers
s.rrd("usr")                        # Read register group
s.rrd("usr r8")                     # Read specific register
ta = s.targets(2)
ta.rrd("mpcore icdipr ipr95")       # Read via target object
s.rrd("--defs")                     # Show register definitions
s.rrd("usr", "--defs")
s.rrd("cpsr", "--no_bits")          # Suppress bit fields
```

#### rwr (Register Write)

```python
s.targets(2)
s.rwr('r0', 0x5555aaaa)             # Write register
s.rwr('cpsr m', 0x13)               # Write register field
```

---

### Reset

#### rst

```python
s.rst('--stop', endianness='le', type='cores')
s.rst('--start', type='cores')
s.rst('--stop', endianness='le', type='cores')
s.rst('--stop', code_endianness='le', type='cores')  # Code endianness
s.rst('--stop', isa='ARM', type='cores')              # Specify ISA
s.rst(type='system')                                   # System reset
```

**Reset types:** `processor`, `cores`, `dap`, `system`, `srst`, `por`, `ps`

---

### Running / Execution Control

#### backtrace

```python
s.backtrace()          # Using session object
t.backtrace()          # Using target object
s.backtrace(5)         # Limit frames
```

#### con (Continue)

```python
s.con()
t.con()
```

#### dis (Disassemble)

```python
t.dis(0x00100000)             # Disassemble at address
t.dis(0x00100000, 5)          # Disassemble N instructions
```

#### locals

```python
s.locals()                          # List all locals
s.locals(name="test")               # Get variable
s.locals(name="test", value=5)      # Set variable
s.locals("--defs")                  # Show definitions
s.locals("--dict")                  # As dictionary
```

#### mbprofile

```python
s.mbprofile(low='low', high='high')
s.mbprofile('--count_instr', low='low', high='high')
s.mbprofile('--start')
s.mbprofile('--stop', out="tests/elfs/mbprofile/gmon_inst_1.out")
```

#### mbtrace

```python
s.mbtrace('--start')
s.mbtrace('-f', '--stop', out="tests/elfs/mbprofile/gmon_trace.txt")
s.mbtrace('-f', '--con', out="tests/elfs/mbprofile/gmon_trace.txt")
```

#### nxt / nxti (Step Over)

```python
s.nxt()               # Step over (source level)
t.nxt(2)              # Step over N times
s.nxti()              # Step over (instruction level)
t.nxti(2)
```

#### print

```python
s.print()                            # Print watched expressions
s.print(expr="temp")                 # Print expression
s.print("x + y - z")                 # Print complex expression
s.print(expr="temp", value=5555)     # Set value
s.print("--add", expr="temp")        # Add watch
s.print("--defs")                    # Show definitions
s.print("--dict")                    # As dictionary
s.print("--remove", expr="temp")     # Remove watch
```

#### profile

```python
s.profile(freq=10000, addr=0x30000000)
s.profile(out="tests/data/gmon_inst.out")
```

#### state / stop

```python
state = tgt.state()     # Get target state
s.stop()                # Stop execution
t.stop()
```

#### stp / stpi (Step Into)

```python
s.stp()                # Step into (source level)
t.stp(2)               # Step N times
s.stpi()               # Step into (instruction level)
t.stpi(2)
```

#### stpout (Step Out)

```python
s.stpout()
t.stpout(2)            # Step out N levels
```

---

### STAPL

#### stapl config

```python
st = self.session.stapl()
st.config(
    out="tests/data/pystapl.stapl",
    scan_chain=[{'name': 'xcvc1902'}, {'name': 'xcvm1802'}]
)
# Or with file handle
handle = open("tests/data/pystapl.stapl", "w+b")
st.config(handle=handle, part=['xcvc1902', 'xcvm1802'])
```

#### stapl start / stop

```python
st.start()
st.stop()
```

---

### Streams

#### jtagterminal

```python
t.jtagterminal()                 # Start
t.jtagterminal('--stop')         # Stop
t.jtagterminal('--socket')       # Socket mode
```

#### readjtaguart

```python
t.readjtaguart()                                      # Start
t.readjtaguart('--stop')                               # Stop
t.readjtaguart(file='tests/data/streams.log', mode='w')  # Log to file
```

---

### SVF

#### svf commands

```python
svf = s.svf()
svf.con()                          # Connect
svf.config(
    scan_chain=[0x14738093, 12, 0x5ba00477, 4],
    device_index=1, cpu_index=0,
    out='/path/to/output.svf'
)
svf.delay(tcks=1000)
svf.dow(file='/path/to/hello.elf')
svf.dow("--data", file="data.bin", addr=0x1000)
svf.generate()
svf.mwr(0xffff0000, 0x14000000)
svf.rst("--processor")
svf.stop()
```

---

### TFile (Target File System)

```python
tfile = s.tfile()
tfile.ls('/tmp')                                        # List directory
handle = tfile.open('/tmp/tfile_test.txt', flags=0x0F)  # Open file
tfile.write(handle, 'hi, this is a test string')        # Write
print(tfile.read(handle, size=5))                       # Read
fstat = tfile.fstat(handle)                             # File stat
tfile.fsetstat(handle, fstat)                           # Set file stat
tfile.close(handle)                                     # Close
tfile.copy('/tmp/src.txt', '/tmp/dest.txt')             # Copy
tfile.copy('/tmp/src.txt', '/tmp/dest.txt', '-o', '-p') # Copy with owner/perms
tfile.mkdir('/tmp/new')                                 # Create directory
tfile.rmdir('/tmp/new')                                 # Remove directory
tfile.remove('/tmp/rigel.txt')                          # Remove file
tfile.rename('/tmp/old.txt', '/tmp/new.txt')            # Rename
tfile.stat('/tmp/rigel.txt')                            # Stat
tfile.lstat('/tmp/rigel.txt')                           # Lstat (link)
tfile.symlink('/tmp/link.txt', '/tmp/target.txt')       # Create symlink
tfile.readlink('/tmp/link.txt')                         # Read symlink
tfile.realpath('/tmp/../tmp/rigel.txt')                 # Resolve path
f = tfile.opendir('/tmp')                               # Open directory
print(tfile.readdir(f))                                 # Read directory entries
print(tfile.roots())                                    # List roots
print(tfile.user())                                     # Current user
```

**File open flags:**

| Flag | Value | Description |
|---|---|---|
| Read | `0x00000001` | Read mode |
| Write | `0x00000002` | Write mode |
| Append | `0x00000004` | Append mode |
| Create | `0x00000008` | Create mode |
| Truncate | `0x00000010` | Truncate mode |
| Exclusive | `0x00000020` | Exclusive create mode |

**Write options:**

| Option | Description |
|---|---|
| `offset` | Byte offset from beginning of file (default: 0) |
| `pos` | Offset in data to write (default: 0) |
| `size` | Number of bytes to write (default: length of data) |

---

### Usage Examples

#### Debug Operations on Session Object

```python
session = start_debug_session()
session.connect(url="TCP:xhdbfarmrkd11:3121")
session.targets(3)
# All subsequent commands run on target 3
session.dow("test.elf")
session.bpadd(addr='main')
session.con()
session.targets(4)
# Now commands run on target 4
session.dow("foo.elf")
session.bpadd(addr='foo')
session.con()
```

#### Debug Operations on Target Object

```python
session = start_debug_session()
session.connect(url="TCP:xhdbfarmrkd11:3121")
ta3 = session.targets(3)
ta4 = session.targets(4)

# Run debug commands using target objects
ta3.dow("test.elf")
ta4.dow("foo.elf")
bp1 = ta3.bpadd(addr='main')
bp2 = ta4.bpadd(addr='foo')
ta3.con()
ta4.con()
bp1.status()
bp2.status()
```

#### Interactive Mode

```python
import xsdb
xsdb.interactive()
# Now use XSDB commands interactively:
# % conn -host xhdbfarmrkb9
# % ta 2
# % stop
# % q
```

---

## Best Practices

1. **Understand the output structure** — Familiarize yourself with the output directory hierarchy to quickly locate logs, reports, and build artifacts.
2. **Use summary files** — Open `*.compile_summary`, `*.link_summary`, and `*.run_summary` files in Vitis Analyzer for visual analysis.
3. **Use target objects for multi-target debug** — Create target objects with `targets()` for cleaner code when debugging multiple processors simultaneously.
4. **Use interactive mode for exploration** — Use `xsdb.interactive()` for ad-hoc debug sessions with shorter command syntax.
5. **Check logs first** — When builds fail, check `v++.log` and `*.steps.log` files in the logs directory.

---

## See Also

- [Chapter 2: Vitis Commands and Utilities](chapter02_vitis_commands_and_utilities.md) — v++ command-line reference
- [Chapter 3: Using the Vitis Unified IDE](chapter03_using_the_vitis_unified_ide.md) — IDE project structure and system projects
- [Chapter 4: Managing Vitis HLS Components](chapter04_managing_the_vitis_hls_components_in_the_vitis_unified_ide.md) — HLS component build artifacts
- [Chapter 5: Managing AI Engine Components](chapter05_managing_the_ai_engine_component_in_the_vitis_unified_ide.md) — AI Engine build output
- [Chapter 8: Working with the Analysis View](chapter08_working_with_the_analysis_view.md) — Viewing summary reports
- [Appendix A: Additional Resources](appendix_a_additional_resources.md) — Reference documents

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 9 (pp. 430–484)*
