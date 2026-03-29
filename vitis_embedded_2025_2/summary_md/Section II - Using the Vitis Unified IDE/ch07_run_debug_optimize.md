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
| **FSBL Exit Function** | Specify the FSBL exit function |
| **Init With FSBL** | Use FSBL to initialize the PS |
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
source <Vitis_path>/settings64.sh  # or settings64.bat (Windows) or settings64.csh
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

### Debugging Standalone Application Component on QEMU

> ⚠️ This feature is not yet supported by the Vitis Unified IDE. Use Classic Vitis IDE if this is a requirement. Refer to 2023.1 documentation for details.

### Setting Conditional Breakpoints

1. Right-click on the left margin before the line number
2. Select **Add Conditional Breakpoint**
3. Type any expression that evaluates to a Boolean and hit Enter

To change a normal breakpoint to a conditional breakpoint:
- Right-click an existing breakpoint → **Edit Breakpoint** → add the expression

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

### OS Aware Debugging

> ⚠️ The Vitis Unified IDE does not currently support this feature. Use the Classic Vitis IDE if this is a requirement. Refer to the 2023.1 documentation for details.

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

#### Viewing the Value of a Certain Memory Address

1. After the debug session starts, click **Memory Inspector** (top-right corner)
2. Click **+** to add a new memory view
3. Set the memory address, offset, and length → click **Go**

#### Comparing the Memory Value of Two Addresses

1. Create two memory inspectors (see above)
2. Click **Toggle Comparison Widget Visibility** to compare the difference
3. Select the memory you want to compare and click **Go**

#### Freezing Memory Value

Keeps a snapshot of the memory contents until the Vitis tool closes. Useful for comparing stored values or debugging issues.

1. Create a new memory inspector (see above)
2. Click the **lock icon** to freeze the memory view

### Export Memory

During debug: Memory Inspector → **Export Memory** icon → specify start/end address and output file path (S-record format).

### Viewing Registers

The Register Inspector lists all registers (general purpose, system, IP, and co-processor). For Zynq devices, it displays processor and co-processor registers when Cortex-A9 targets are selected; system/IOU registers when APU target is selected.

- Open via **View → Register Inspector** after debug session starts
- Editable field values during debug
- Click register name to view detailed information

### Exporting Registers

1. Start the debug session and open the Register Inspector view
2. Click the **Export Registers** button
3. Select registers/groups to export and specify output location
4. Click **OK** to dump registers to the specified file

### Using Virtual UART Terminal

TCF Virtual UART terminal provides MDM terminal support. Right-click the MicroBlaze or MicroBlaze V core → **TCF Debug Virtual Terminal**.

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

#### Zynq Devices

4 broadcast channels, 4 CTIs (ETB/TPIU, FTM, CPU0, CPU1), 1 CTM.

**Table 9: CTI Trigger Ports in Zynq Devices** (hard-wired connections)

| CTI | Trigger Port | Signal |
|-----|-------------|--------|
| **ETB/TPIU CTI** | IN 2 | ETB full |
| | IN 3 | ETB acquisition complete |
| | IN 4 | ITM trigger |
| | OUT 0 | ETB flush |
| | OUT 1 | ETB trigger |
| | OUT 2 | TPIU flush |
| | OUT 3 | TPIU trigger |
| **FTM CTI** | IN 0–3 | FTM trigger (×4) |
| | OUT 0–3 | FTM trigger (×4) |
| **CPU0/1 CTIs** | IN 0 | CPU DBGACK |
| | IN 1 | CPU PMU IRQ |
| | IN 2–3 | PTM EXT |
| | IN 4–5 | CPU COMMTX |
| | IN 6 | PTM TRIGGER |
| | OUT 0 | CPU debug request |
| | OUT 1–4 | PTM EXT |
| | OUT 7 | CPU restart request |

#### Zynq UltraScale+ MPSoC

4 broadcast channels, 9 CTIs, 1 CTM. See UG1085 for details.

**Table 10: CTI Trigger Ports in Zynq UltraScale+ MPSoCs** (hard-wired connections)

| CTI | Trigger Port | Signal |
|-----|-------------|--------|
| **CTI 0 (soc_debug_fpd)** | IN 0–1 | ETF 1 FULL / ACQCOMP |
| | IN 2–3 | ETF 2 FULL / ACQCOMP |
| | IN 4–5 | ETR FULL / ACQCOMP |
| | OUT 0–1 | ETF 1 FLUSHIN / TRIGIN |
| | OUT 2–3 | ETF 2 FLUSHIN / TRIGIN |
| | OUT 4–5 | ETR FLUSHIN / TRIGIN |
| | OUT 6–7 | TPIU FLUSHIN / TRIGIN |
| **CTI 1 (soc_debug_fpd)** | IN 0–3 | FTM (×4) |
| | IN 4 | STM TRIGOUTSPTE |
| | IN 5 | STM TRIGOUTSW |
| | IN 6 | STM TRIGOUTHETE |
| | IN 7 | STM ASYNCOUT |
| | OUT 0–3 | FTM (×4) |
| | OUT 4–5 | STM HWEVENTS |
| | OUT 7 | HALT SYSTEM TIMER |
| **CTI 2 (soc_debug_fpd)** | IN 0–1 | ATM 0 / ATM 1 |
| | OUT 0–1 | ATM 0 / ATM 1 |
| | OUT 7 | picture debug start |
| **CTI 0, 1 (RPU)** | IN 0 | DBGTRIGGER |
| | IN 1 | PMUIRQ |
| | IN 2–3 | ETMEXTOUT[0–1] |
| | IN 4–5 | COMMRX / COMMTX |
| | IN 6 | ETM TRIGGER |
| | OUT 0 | EDBGRQ |
| | OUT 1–2 | ETMEXTIN[0–1] |
| | OUT 7 | DBGRESTART |
| **CTI 0, 1, 2, 3 (APU)** | IN 0 | DBGTRIGGER |
| | IN 1 | PMUIRQ |
| | IN 4–7 | ETMEXTOUT[0–3] |
| | OUT 0 | EDBGRQ |
| | OUT 1 | DBGRESTART |
| | OUT 2 | CTIIRQ |
| | OUT 4–7 | ETMEXTIN[0–3] |

#### Versal Devices

4 broadcast channels, 12 CTIs, 1 CTM. See AM011 for details.

**Table 11: CTI Trigger Ports in Versal Devices** (hard-wired connections)

| CTI | Trigger Port | Signal |
|-----|-------------|--------|
| **R5 CTI 0, 1 (RPU)** — XSDB IDs: 0–7 (R5 #0), 8–15 (R5 #1) |||
| | IN 0 | R5 DBGTRIGGER |
| | IN 1 | R5 PMUIRQ |
| | IN 2–3 | ETM EXTOUT[0–1] |
| | IN 4–5 | R5 COMMRX / COMMTX |
| | IN 6 | ETM TRIGGER |
| | OUT 0 | R5 EDBGRQ |
| | OUT 1–2 | ETM EXTIN[0–1] |
| | OUT 7 | R5 DBGRESTART |
| **CTI 0, 1, 2, 3 (APU)** — XSDB IDs: 16–23 (A72 #0), 24–31 (#1), 32–39 (#2), 40–47 (#3) |||
| | IN 0 | A72 DBGTRIGGER |
| | IN 1 | A72 PMUIRQ |
| | IN 4–7 | ETM EXTOUT[0–3] |
| | OUT 0 | A72 EDBGRQ |
| | OUT 1 | A72 DBGRESTART |
| | OUT 2 | GIC PPI 24 |
| | OUT 4–7 | ETM EXTIN[0–3] |
| **CTI p (pmc_debug)** — XSDB IDs: 48–55 |||
| | IN 0 | ATM TRIGOUT[0] |
| | OUT 0 | ATM TRIGIN[0] |
| **CTI 0d (soc_debug_lpd)** — XSDB IDs: 56–63 |||
| | IN 0–4 | ATM0 TRIGOUT[0–4] |
| | OUT 0–4 | ATM0 TRIGIN[0–4] |
| **CTI 1a (APU ATM)** — XSDB IDs: 64–71 |||
| | IN 0–1 | ELA 1a CTTRIGOUT[0–1] |
| | IN 2–3 | ETF 1a FULL / ACQCOMP |
| | OUT 0–1 | ELA 1a CTTRIGIN[0–1] |
| | OUT 2–3 | ETF 1a FLUSHIN / TRIGIN |
| | OUT 4–5 | PMUSNAPSHOT[0–1] |
| **CTI 1b (soc_debug_fpd)** — XSDB IDs: 72–79 |||
| | IN 0 | STM TRIGOUTSPTE |
| | IN 1 | STM TRIGOUTSW |
| | IN 2 | STM TRIGOUTHETE |
| | IN 3 | STM ASYNCOUT |
| | IN 4–5 | ETF 1 FULL / ACQCOMP |
| | IN 6–7 | ETR FULL / ACQCOMP |
| | OUT 0–1 | STM HWEVENTS |
| | OUT 2–3 | TPIU FLUSHIN / TRIGIN |
| | OUT 4–5 | ETF 1 FLUSHIN / TRIGIN |
| | OUT 6–7 | ETR FLUSHIN / TRIGIN |
| **CTI 1c (soc_debug_fpd)** — XSDB IDs: 80–87 |||
| | IN 0–3 | pl_ps_trigger[0–3] |
| | OUT 0–3 | ps_pl_trigger[0–3] |
| | OUT 6 | HALT System Timer |
| | OUT 7 | RESTART System Timer |
| **CTI 1d (soc_debug_fpd)** — XSDB IDs: 88–95 |||
| | IN 0–6 | ATM1 TRIGOUT[0–6] |
| | OUT 0–6 | ATM1 TRIGIN[0–6] |

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

## Source Attribution

- **Document:** UG1400 (v2025.2) — Vitis Embedded Software Development
- **Date:** November 20, 2025
- **Chapter:** 7 (pp. 86–139)
