# Chapter 12 — Python XSDB Usage Examples

## Debug on Session Object

Create a session object and run debug operations on different targets using the same session:

```python
from xsdb import *

session = start_debug_session()
session.connect(url="TCP:xhdbfarmrkd11:3121")

session.targets(3)
# All subsequent commands run on target 3 until changed
session.dow("test.elf")
session.bpadd(addr='main')
session.con()

session.targets(4)
# All subsequent commands run on target 4
session.dow("foo.elf")
session.bpadd(addr='foo')
session.con()
```

---

## Debug on Target Object

Use Target objects returned by `targets()` for independent operations:

```python
session = start_debug_session()
session.connect(url="TCP:xhdbfarmrkd11:3121")

ta3 = session.targets(3)
ta4 = session.targets(4)

ta3.dow("test.elf")
ta4.dow("foo.elf")

bp1 = ta3.bpadd(addr='main')
bp2 = ta4.bpadd(addr='foo')

ta3.con()
ta4.con()

bp1.status()
bp2.status()
```

---

## Interactive Mode

Use `xsdb.interactive()` for command-line style interaction (uses commands/options instead of functions/arguments):

```python
import xsdb
xsdb.interactive()
```

```
% conn -host xhdbfarmrkb9
tcfchan#0
% ta
1 APU
    2 ARM Cortex-A9 MPCore #0 (Running)
    3 ARM Cortex-A9 MPCore #1 (Running)
4 xc7z020
% ta 2
% stop
Info: ARM Cortex-A9 MPCore #0 (target 2) Stopped at 0xffffff28 (Suspended)
% q
```

---

## Programming U-Boot over JTAG

ZynqMP example: load PMU FW, FSBL, and U-Boot sequentially.

```python
import xsdb, time

s = xsdb.start_debug_session()
s.connect(url="TCP:xhdbfarmrkg7:3121")

# Disable security gates for DAP, PLTAP, and PMU
s.targets("--set", filter="name =~ PSU")
s.mwr(0xffca0038, words=0x1ff)
time.sleep(0.5)

# Load and run PMU FW
s.targets("--set", filter="name =~ MicroBlaze PMU")
s.dow('pmufw.elf')
s.con()
time.sleep(0.5)

# Reset A53, load and run FSBL
s.targets("--set", filter="name =~ Cortex-A53 #0")
s.rst(type='processor')
s.dow('fsbl.elf')
s.con()
time.sleep(5)
s.stop()

# Download U-Boot and related files
s.dow('system.dtb', '-d', addr=0x100000)
s.dow('u-boot.elf')
s.dow('bl31.elf')
s.con()
```

---

## Generate SVF Files

Generate Serial Vector Format files for programming via JTAG:

```python
s = xsdb.start_debug_session()
s.connect(url="TCP:xhdxxxx41x:3121")

# Generate SVF for linking DAP to JTAG chain (Rev2.0+ silicon only)
svf = s.svf()
svf.config('--linkdap',
    scan_chain=[0x14738093, 12, 0x5ba00477, 4],
    device_index=1, out="dapcon.svf")
svf.generate()

# Generate SVF for FSBL + application
core = 0
apu_reset_a53 = [0x380e, 0x340d, 0x2c0b, 0x1c07]

svf = s.svf()
svf.config(
    scan_chain=[0x14738093, 12, 0x5ba00477, 4],
    device_index=1, cpu_index=core, delay=10, out="fsbl_hello.svf")

svf.mwr(0xffff0000, 0x14000000)           # Write bootloop
svf.mwr(0xfd1a0104, apu_reset_a53[core])  # Release A53 from reset
svf.stop()
svf.dow(file='zynq_fsbl.elf')
svf.con()
svf.delay(100000)
svf.stop()
svf.dow(file='zynq_hello.elf')
svf.con()
svf.generate()
```

---

## JTAG UART Functions

Three methods for JTAG UART communication:

### `readjtaguart` — Console Output

```python
s = xsdb.start_debug_session()
s.connect(url="TCP:xhdbfarmrke9:3121")
s.targets("--set", filter="name =~ ARM Cortex-A9 MPCore #0")
s.rst()
s.loadhw(hw='zc702.xsa')

# Run FSBL for ps7_init
s.dow('fsbl.elf')
s.con()
time.sleep(0.5)
s.stop()

# Download and run application
s.dow('test_jtag_uart.elf')
s.readjtaguart()
s.con()
s.readjtaguart('--stop')  # when done
```

### `readjtaguart` — File Output

```python
# Same setup as above, then:
s.dow('test_jtag_uart.elf')
s.readjtaguart(file='streams.log', mode='w')
s.con()
s.readjtaguart('--stop')
```

### `jtagterminal` — Interactive Terminal

```python
# Same setup as above, then:
s.dow('test_jtag_uart.elf')
s.jtagterminal()
s.con()
s.jtagterminal('--stop')
```

---

## Standalone App Debug (Zynq-7000)

Full debug session on Zynq-7000 (zc702) — FPGA programming, FSBL, application download, breakpoints, stepping, variable inspection, stack trace:

```python
import xsdb
s = xsdb.start_debug_session()
s.connect(url="TCP:xhdbfarmrke9:3121")

s.targets("--set", filter="name =~ APU")
s.rst()

# Program FPGA
s.fpga(file='zc702.bit')

# Select Cortex-A9 #0, run FSBL
s.targets(2)
s.loadhw(hw='zc702.xsa')
s.dow('fsbl.elf')
s.con()
time.sleep(0.5)
s.stop()

# Download application
s.dow('test_jtag_uart.elf')
s.bpadd(addr='main')
s.con()
# Stops at breakpoint in main()
```

### Debug Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `stp()` | Step into | `s.stp()` |
| `nxt()` | Step over | `s.nxt()` |
| `con()` | Continue | `s.con()` |
| `stop()` | Stop execution | `s.stop()` |
| `rrd()` | Read all registers | `s.rrd()` |
| `mrd(addr)` | Read memory | `s.mrd(0xe000d000)` |
| `locals()` | View local variables | `s.locals()` |
| `locals(name, val)` | Modify local variable | `s.locals(name='l_int_b', val=815)` |
| `print(expr)` | View global/expression | `s.print(expr='g_int_a')` |
| `print(expr, val)` | Modify global variable | `s.print(expr='g_int_a', val=9919)` |
| `print('--add', expr)` | Evaluate expression | `s.print('--add', expr='l_int_a + l_int_b')` |
| `bt()` | View stack trace (backtrace) | `s.bt()` |
| `bpadd(addr)` | Add breakpoint | `s.bpadd(addr='main')` |
| `bpadd(addr='&exit')` | Breakpoint at function address | `s.bpadd(addr='&exit')` |

---

## Target Selection by Properties

Use JTAG target properties to select specific targets:

```python
# Check JTAG targets (node IDs)
s.jtag_targets()
#  1  Digilent JTAG-SMT1 210203344713A
#     2  arm_dap (idcode 4ba00477 irlen 4)
#     3  xc7z020 (idcode 23727093 irlen 6 fpga)

# Get detailed properties for a specific node
props = s.jtag_targets('-t', filter="node_id == 2")
# Returns dict with target_ctx, name, idcode, irlen, etc.

# Use target_ctx to select associated targets
s.targets(filter="jtag_device_ctx == jsn-JTAG-SMT1-210203344713A-4ba00477-0")
```

Key JTAG target properties:

| Property | Description |
|----------|-------------|
| `target_ctx` | Unique target context identifier |
| `node_id` | JTAG chain node ID |
| `name` | Device name (e.g., `arm_dap`) |
| `idcode` | JTAG ID code |
| `irlen` | Instruction register length |
| `jtag_cable_name` | Cable identifier |
| `jtag_cable_serial` | Cable serial number |
| `is_fpga` | Whether the device is an FPGA |

---

## Debugging a Running Program

Attach to a program already executing on the target using `memmap`:

```python
s = xsdb.start_debug_session()
s.connect(url="TCP:xhdbfarmrke9:3121")

# Select target and specify symbol file
s.target(2)
s.memmap(file='test_jtag_uart.elf')

# Stop and inspect
s.stop()
# Shows current location with source info
s.backtrace()
# 0  sleep_A9()+56:sleep.c, line 63
# 1  test_function()+76:../src/helloworld.c, line 78
# 2  main()+44:../src/helloworld.c, line 61
```

---

## Debug on Zynq UltraScale+ MPSoC

Full ZCU102 debug session — system reset, FPGA programming, FSBL on A53, application download and debug:

```python
import xsdb
s = xsdb.start_debug_session()
s.connect(url="TCP:xhdbfarmrkk5:3121")

s.targets()
#  1  PS TAP
#     2  PMU
#     3  PL
#  4  PSU
#     5  RPU (Reset)
#        6  Cortex-R5 #0 (RPU Reset)
#        7  Cortex-R5 #1 (RPU Reset)
#     8  APU (L2 Cache Reset)
#        9  Cortex-A53 #0 (APU Reset)
#       10  Cortex-A53 #1 (APU Reset)
#       11  Cortex-A53 #2 (APU Reset)
#       12  Cortex-A53 #3 (APU Reset)

# System reset and FPGA programming
s.targets("--set", filter="name =~ PSU")
s.rst(type='system')
s.fpga(file='zcu102.bit')

# Reset all A53 cores
s.targets(10)
s.rst(type='cores')
# All 4 A53 cores stop at Reset Catch

# Run FSBL
s.dow('fsbl_a53.elf')
s.con()
time.sleep(0.5)
s.stop()

# Download and debug application
s.dow('zcu102_hello.elf')
s.bpadd(addr='main')
s.con()
# Stops at breakpoint in main()

# Step, inspect variables, evaluate expressions, backtrace
s.stp()
s.locals()
s.print(expr='g_int_a')
s.nxt()
s.bt()
```

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 12 (pp. 167–178)*
