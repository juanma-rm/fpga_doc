# Chapter 7 — Run, Debug, and Optimize

Launch configurations, target connections, debugging standalone and Linux applications, PS Trace, cross-triggering, profiling (TCF), boot image creation, flash programming, and multi-cable/multi-device support.

---

## Table of Contents

- [Launch Configurations](#launch-configurations)
- [Target Connections](#target-connections)
- [Running the Application](#running-the-application)
- [Debugging](#debugging)
  - [Standalone Applications](#debugging-standalone-application-component)
  - [Linux Applications](#debugging-linux-application-component)
  - [Zephyr on MicroBlaze V](#debugging-zephyr-applications-on-microblaze-v)
  - [Attach to Running Target](#debugging-an-application-already-running-on-target)
  - [Self-Relocating Programs](#debugging-self-relocating-programs)
  - [System Project Debug](#running-and-debugging-under-a-system-project)
  - [Remote Board Debug](#debugging-on-a-remote-board)
  - [Xen Aware Debug](#xen-aware-debug)
- [PS Trace](#ps-trace)
- [Memory, Registers, and Disassembly](#memory-registers-and-disassembly)
- [Cross-Triggering](#cross-triggering)
- [Profile / Analyze](#profile--analyze)
- [Creating a Boot Image](#creating-a-boot-image)
- [Programming Flash](#programming-flash)
- [Multi-Cable and Multi-Device Support](#multi-cable-and-multi-device-support)
- [Authenticated JTAG Access](#authenticated-jtag-access)

---

## Launch Configurations

Access: Flow Navigator → select component → hover over Run/Debug → click **Open Settings**

The `launch.json` file contains all launch configurations. Default configurations for system projects: **Emulation SW**, **Emulation HW**, **Hardware**.

### Main Page Options

| Option | Description |
|--------|-------------|
| **Launch Config Name** | Configuration identifier |
| **Target Connection** | Select target or create via **New** |
| **Target Setup Mode** | Standalone debug or Attach to running target |
| **Bitstream File** | Path to .bit file |
| **Board Initialization** | FSBL or Tcl initialization |
| **FSBL File** | FSBL path for PS initialization |
| **Reset Entire System** | System reset (single processor) |
| **Reset APU / Reset RPU** | Reset specific processor clusters |
| **Enable RPU Split Mode** | Independent RPU cores |
| **Program Device** | Program bitfile to device |
| **Enable Cross Triggering** | Enable ECT cross-trigger function |

### Application Part

| Option | Description |
|--------|-------------|
| **Processor** | Specific processor target |
| **Reset Processor** | Reset system, specific processor, or none |
| **Application** | ELF file path |
| **Stop at Entry** | Break at entry point |
| **+** | Add additional processor/application configurations |

---

## Target Connections

Access: **Vitis → Target Connections**

Connections are established through **hw_server**. The hardware server agent must run on the host connected to the target hardware.

### Creating a New Target Connection

1. Right-click Hardware Server or Linux TCF Agent → **Add Target Connection (+)**
2. Configure:

| Field | Description | Default |
|-------|-------------|---------|
| Target Name | Connection identifier | — |
| Host | IP address or hostname of remote host | — |
| Port | hw_server port | 3121 |
| Set as Default | Use for all future interactions | unchecked |
| Use Symbol Server | For remote debugging source view | unchecked |

3. Optionally **Test Connection** before clicking **OK**

### Setting Custom JTAG Frequency

In Target Connection → **Advanced** → **Automatically discover devices on JTAG chain** → Select frequency from dropdown.

> The frequency persists in the workspace. Do not perform simultaneous debug from different clients.

### Establishing Remote Connection

```bash
# On remote host
source <Vitis_path>/settings64.sh  # or settings64.bat on Windows
hw_server -s TCP::3122             # Custom port example
```

---

## Running the Application

1. Flow Navigator → select application component
2. Configure launch configuration (see above)
3. Click **Run**

> After running, terminate the session via the **Terminate** button in Debug view.

---

## Debugging

### Debugging Standalone Application Component

1. Flow Navigator → select component
2. Open Debug Settings → create configuration
3. Set target connection
4. Click **Debug**

### Debugging Linux Application Component

Same flow as standalone, but select Linux application component and use **Linux TCF Agent** for target connection.

### Debugging Zephyr Applications on MicroBlaze V

Uses **User Managed Mode**. Full workflow:

1. **Set up Zephyr environment:**
   ```bash
   cd <local_path>/zephyrproject/
   mv zephyr zephyr.upstream
   git clone https://github.com/Xilinx/zephyr-amd.git -b xlnx_rel_v2025.1 zephyr
   west update
   west lopper-install
   ```

2. **Create hardware design** via Vivado (MicroBlaze V Design Preset CED)

3. **Generate System Device Tree:**
   ```bash
   source /tools/AMD/Vivado/2025.2/settings64.sh
   sdtgen sdt.tcl
   ```

4. **Setup Zephyr repository:**
   ```bash
   LOPPER_DTC_FLAGS="-b 0 -@" west lopper-command \
     -p microblaze_riscv_0 \
     -s design_1_wrapper/system-top.dts \
     -w ~/zephyrproject/zephyr
   ```

5. **Build:**
   ```bash
   cd zephyr
   west build -p -b mbv32 tests/misc/test_build/
   # Output: build/zephyr/zephyr.elf
   ```

6. **Debug in Vitis:** Open folder in User Managed Mode → create launch configuration → set processor to `microblaze_riscv_0` and ELF path → Debug

---

### Debugging an Application Already Running on Target

1. Create target connection to the board host
2. In launch configuration, set **Target Setup Mode** → **Attach to running target**
3. Start debug

> The debugger does not modify processor state — merely connects. Halt processors manually to debug from current PC.

### Source Code Remap

In launch configuration → **Path Map** → **+** to add:
- **SOURCE:** Original path (from CALL STACK hover)
- **DESTINATION:** Current file path

### Debugging Self-Relocating Programs

In `launch.json`: check **Is Self Relocating Application** and provide relative address.

CLI: `memmap -reloc <addr> -file <path-to-elf>`

### Running and Debugging Under a System Project

1. Select system project in Component View
2. Flow Navigator → create launch configuration
3. Debug or Run — applications download and launch sequentially; all stop at `main()` in debug mode

> Select individual cores to step over/in/out, or select parent node to control all cores.

### Debugging on a Remote Board

1. On remote host: `hw_server -s TCP::3122`
2. In Vitis: create target connection with remote IP and port
3. Enable **Use Symbol Server** for source code view
4. Debug

### Xen Aware Debug

For debugging under the Xen hypervisor:

1. Prepare PetaLinux environment for dom0 (UG1144)
2. Create app, launch debug as **Attach to running process**
3. Right-click APU core → **Manage Symbol Files** → add `xen-syms`
4. Right-click VCPU #0 → add `vmlinux` (without OS Awareness option)
5. Pause and verify Call Stack for symbol mapping

> ⚠️ Available as early access feature in New Feature Preview.

---

## PS Trace

Monitors every ARMv8 assembly instruction execution for online diagnosis and performance debugging.

**Supported processors:** Cortex-A53, R52, A78, R5, A72

### Prerequisites: OpenCSD Setup

```bash
export INSTALL_PATH="/path/to/install/"
git clone https://github.com/Linaro/OpenCSD.git
cd OpenCSD/decoder/build/linux/
make install PREFIX=$INSTALL_PATH
export OPENCSD_PATH=$INSTALL_PATH   # Set before launching Vitis
```

### Performing PS Trace

1. **Configure** in launch.json:
   | Field | Description |
   |-------|-------------|
   | Scratch Address | Starting memory address for trace binary |
   | Trace Memory Length | Buffer size for trace data |
   | Output File Path | Location for decoded trace summary |

   > ⚠️ Ring buffer — if trace data exceeds size, new data overwrites existing data.

2. **Set breakpoints:** Right-click line → **Trace Start Breakpoint** / **Trace Stop Breakpoint**

3. **Run:** Click Continue → trace starts at start breakpoint → Continue → trace stops at stop breakpoint

4. **View:** Notification appears → click **Open** or **Vitis → PS Trace → Open PS Trace**

5. **Source mapping:** Browse to ELF file folder when prompted

---

## Memory, Registers, and Disassembly

### Memory Inspector

- **View memory:** Click Memory Inspector (top-right) → **+** → set address, offset, length → **Go**
- **Compare addresses:** Create two inspectors → click **Toggle Comparison Widget** → **Go**
- **Freeze memory:** Click lock icon for a persistent snapshot

### Export Memory

During debug: Memory Inspector → **Export Memory** icon → specify start/end address and output file path (S-record format).

### Register Inspector

- View from **View → Register Inspector** after debug session starts
- Displays general purpose, system, IP, and co-processor registers
- Editable field values during debug
- **Export:** Click **Export Registers** → select registers/groups → specify output location

### Virtual UART Terminal

Right-click MicroBlaze/MicroBlaze V core → **TCF Debug Virtual Terminal**

### Disassembly View

Right-click function in Call Stack → **Open Disassembly**

---

## Cross-Triggering

The **Embedded Cross-Triggering (ECT)** module enables SoC subsystems to exchange debug triggers.

**Components:**
- **Cross Trigger Interface (CTI):** Maps trigger requests to channel events
- **Cross Trigger Matrix (CTM):** Distributes channel events

**Enable:** In launch configuration → check **Enable Cross Triggering** → **Add Item** for breakpoints

### CTI Ports by Device Family

**Zynq:** 4 channels, 4 CTIs (ETB/TPIU, FTM, CPU0, CPU1), 1 CTM

| CTI | Key Trigger Inputs | Key Trigger Outputs |
|-----|-------------------|-------------------|
| ETB/TPIU | ETB full, ETB acq complete, ITM trigger | ETB/TPIU flush, trigger |
| FTM | FTM trigger (×4) | FTM trigger (×4) |
| CPU0/1 | DBGACK, PMU IRQ, PTM EXT, COMMTX | CPU debug request, PTM EXT, restart request |

**Zynq UltraScale+ MPSoC:** 4 channels, 9 CTIs (3 soc_debug, 2 RPU, 4 APU), 1 CTM

**Versal:** 4 channels, 12 CTIs (2 RPU, 4 APU, PMC, soc_debug_lpd, APU ATM, soc_debug_fpd ×3, ATM)

### Cross-Trigger Use Cases

| Use Case | Description |
|----------|-------------|
| **FPGA → CPU** | ILA trigger halts CPU; CPU halt triggers ILA capture |
| **PTM → CPU** | ETB full event halts CPU |
| **CPU → CPU** | CPU0 halt triggers CPU1 halt |

### XSDB Commands

```tcl
# Zynq: Halt core 1 when core 0 stops
bpadd -ct-input 0 -ct-output 8

# Zynq UltraScale+: Halt A53#1 when A53#0 stops
bpadd -ct-input 16 -ct-output 24
```

---

## Profile / Analyze

### TCF Profiling

Non-intrusive profiling via Program Counter sampling over JTAG. Supports standalone and Linux applications.

> No additional compiler flags required. Stack trace collection (optional) decreases execution speed.

**Steps:**
1. Create debug launch configuration
   - Standalone → use **HW server** connection
   - Linux → use **TCF agent** connection
2. Start debug session
3. Click **TCF Profiler** button
4. Configure:
   | Option | Description |
   |--------|-------------|
   | Enable Stack Tracing | Show stack trace for each sample |
   | Max Stack Frames | Maximum frames in stack view |
   | View Update Interval | Update interval (ms) — set differently from sample collection interval |
5. Click **Start** → **Continue** (free run)
6. Click function in profiler → see **Called From** and **Child Calls**
7. Click function name → cross-probe to source code

### MicroBlaze Non-Intrusive Profiling

Use XSDB command: `mbprofile` (or `mbprofile -help`)

### Unsupported in Unified IDE

| Feature | Status |
|---------|--------|
| gprof Profiling | ❌ Use Classic IDE (2024.2) |
| FreeRTOS STM Analysis | ❌ Use Classic IDE (2024.2) |
| QEMU debugging | ❌ Use Classic IDE (2024.2) |
| OS Aware Debug | ❌ Use Classic IDE (2023.1) |

---

## Creating a Boot Image

**Bootgen** stitches binary files together to generate device boot images. See Bootgen User Guide (UG1283).

### Method 1: From Scratch

**Vitis → Create Boot Image** → select device (Zynq/ZynqMP/Versal)

1. Select **Create a new BIF file**
2. Click **+** to add image partitions (bootloader, bitfile, BL31, app ELF)
3. Modify attributes per partition as needed
4. Specify Output BIF File Path and Output Image path
5. Click **Create Image**

### Method 2: From Flow Navigator (Faster)

1. Select built application component
2. Flow Navigator → **Create Boot Image**
3. Review required images → specify output paths → **Create Image**

---

## Programming Flash

Access: **Vitis → Program Flash**

| Option | Description |
|--------|-------------|
| **Project** | System project to use |
| **Connection** | Hardware server connection |
| **Image File** | File to write to flash |
| **Offset** | Relative to Flash Base Address (not needed for MCS) |
| **Flash Type** | Device-specific flash type |
| **Init File** | Initialization file path |
| **Blank Check After Erase** | Verify erased region is blank |
| **Verify After Flash** | Read back and cross-check |

**Flash types by device:**

| Device | Supported Flash Types |
|--------|----------------------|
| **Non-Zynq** | Parallel (BPI), Serial (SPI); file formats: BIT, ELF, SREC, MCS, BIN |
| **Zynq** | qspi_single, qspi_dual_parallel, qspi_dual_stacked, nand_8, nand_16, nor |
| **Versal/ZynqMP** | qspi_single, qspi_dual_parallel, qspi_dual_stacked, emmc, OSPI |

---

## Multi-Cable and Multi-Device Support

- **Multi-cable:** Multiple boards connected to the system
- **Multi-device:** Multiple devices on a single JTAG chain

### Debug with Multi-Cable/Multi-Device

1. Open launch configuration
2. Click **Select** beside Device field
3. Deselect **Auto Detect**
4. Select PS and PL device
5. Click **Select and Start**

### Program Device

**Vitis → Program Device** → click **Select** to choose device/cable → **Program**

---

## Authenticated JTAG Access

Secure JTAG access requiring authentication before any operations (debug, programming, inspection).

1. Enable **Authenticate JTAG** in launch configuration
2. Click **Create** → provide JTAG file path → generates decryption file
3. File auto-populates in **Authenticated JTAG File** field
4. Debug session uses file to open JTAG gate

---

## Best Practices

1. **Use FSBL initialization** for board setup rather than manual Tcl unless required
2. **Enable Symbol Server** for remote debugging to ensure source code visibility
3. **Set appropriate trace buffer size** for PS Trace — ring buffer overwrites on overflow
4. **Use TCF profiling** (non-intrusive) before enabling stack trace (which slows execution)
5. **Test target connections** before starting debug sessions
6. **Use system projects** to debug multi-application scenarios simultaneously

---

## Source Attribution

- **Document:** UG1400 (v2025.2) — Vitis Embedded Software Development
- **Date:** November 20, 2025
- **Chapter:** 7 (pp. 86–139)
