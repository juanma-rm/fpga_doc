# Chapter 2: Getting Started with the Vivado Design Suite

This chapter covers the practical steps needed to install, launch, and begin using the Vivado Design Suite. It describes multiple launch methods (GUI - and Tcl-based), project creation, IP management, hardware debugging, the Vivado Store, and documentation access.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Installing the Vivado Design Suite](#installing-the-vivado-design-suite) | Installation, licensing, and customization options |
| [Launching the Vivado Design Suite](#launching-the-vivado-design-suite) | Overview of launch methods and design flow modes |
| [Working with Tcl](#working-with-tcl) | Using Tcl commands and scripts interactively or in batch |
| [Launching the Vivado Design Suite Tcl Shell](#launching-the-vivado-design-suite-tcl-shell) | Command to start the Tcl shell |
| [Launching the Vivado Tools Using a Batch Tcl Script](#launching-the-vivado-tools-using-a-batch-tcl-script) | Running Vivado in batch mode |
| [Working with the Vivado IDE](#working-with-the-vivado-ide) | GUI-based design workflow |
| [Launching the Vivado IDE](#launching-the-vivado-ide) | Platform-specific launch instructions |
| [Using the Vivado IDE](#using-the-vivado-ide) | Getting Started page and initial workflow |
| [Starting with a Project](#starting-with-a-project) | Creating and opening projects |
| [Managing IP](#managing-ip) | IP catalog and remote IP locations |
| [Opening the Hardware Manager](#opening-the-hardware-manager) | Programming and debugging with Hardware Manager |
| [Vivado Store](#vivado-store) | Tcl apps, board files, and example designs |
| [Reviewing Documentation and Videos](#reviewing-documentation-and-videos) | Accessing user guides, tutorials, and videos |

---

## Installing the Vivado Design Suite

The Vivado Design Suite and the ISE Design Suite are released and installed **separately**. Both are available from the [AMD Downloads page](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-download.html).

### Installation Options

- **Custom installation** — Install only the tools and device families you need (e.g., AMD Kintex™ 7 or AMD Artix™ 7)
- **License entitlement** — All current, in-warranty seats of either suite receive entitlement to the equivalent edition of the other suite

### Key Reference Documents

| Document | ID | Purpose |
|----------|----|---------|
| Vivado Design Suite User Guide: Release Notes, Installation, and Licensing | UG973 | OS support, installation, AMD Information Center |
| Xilinx ISE Design Suite 14: Release Notes, Installation, and Licensing | UG631 | Legacy ISE installation |
| ISE to Vivado Design Suite Migration Guide | UG911 | Migrating ISE designs to Vivado |

> ⚠️ **Important:** From 2022.1 onwards, projects containing ISE technology are no longer recognized by Vivado and are not read. Refer to UG911 for migration guidance.

> **Note:** For memory recommendations for the Vivado Design Suite tools, see the Memory Recommendations section in UG973.

### See Also

- [Chapter 1: Vivado Design Suite Overview](chapter1_vivado_design_suite_overview.md)
- Vivado Design Suite User Guide: Release Notes, Installation, and Licensing (UG973)

---

## Launching the Vivado Design Suite

You can launch the Vivado Design Suite using different methods depending on your preference:

| Mode | Description | Command |
|------|-------------|---------|
| **Project Mode** | Automatically manages design process and data using projects and project states | Launch via GUI or Tcl |
| **Non-Project Mode** | Tcl script-based; you manage sources and design process manually | Tcl scripts |
| **Batch Mode** | Runs a Tcl script and exits | `vivado -mode batch -source <script>` |
| **Interactive Tcl** | Enter Tcl commands interactively | `vivado -mode tcl` |
| **GUI (IDE)** | Full graphical interface | `vivado` or Start Menu |

> For more information on design flow modes, see the Vivado Design Suite User Guide: Design Flows Overview (UG892).

---

## Working with Tcl

If you prefer to work directly with Tcl, you can interact with your design using Tcl commands via:

1. **Vivado Design Suite Tcl shell** — Enter individual commands outside the IDE
2. **Tcl Console** — Enter commands at the bottom of the Vivado IDE
3. **Tcl scripts from the Tcl shell** — Run complete flow scripts
4. **Tcl scripts from the Vivado IDE** — Source scripts within the GUI

### See Also

- Vivado Design Suite User Guide: Using Tcl Scripting (UG894)
- Vivado Design Suite Tutorial: Design Flows Overview (UG888)

---

## Launching the Vivado Design Suite Tcl Shell

### Syntax

```bash
vivado -mode tcl
```

Launch at the Linux command prompt or within a Windows Command Prompt window.

> **Note (Windows):** You can also select **Start → All Programs → Xilinx Design Tools → Vivado \<version\> → Vivado \<version\> Tcl Shell**.

---

## Launching the Vivado Tools Using a Batch Tcl Script

### Syntax

```bash
vivado -mode batch -source <your_Tcl_script>
```

| Parameter | Description |
|-----------|-------------|
| `-mode batch` | Runs Vivado in batch mode (exits after script completes) |
| `-source <script>` | Specifies the Tcl script to execute |

> **Note:** When working in batch mode, the Vivado tools exit after running the specified script.

---

## Working with the Vivado IDE

If you prefer a GUI, launch the Vivado IDE from Windows or Linux.

> **Recommended:** Launch the Vivado IDE from your **working directory**. This makes it easier to locate the project file, log files, and journal files, which are written to the launch directory.

### Launching the Vivado IDE on Windows

1. **Start Menu:** Select **Start → All Programs → Xilinx Design Tools → Vivado \<version\> → Vivado \<version\>**
2. **Desktop shortcut:** Double-click the Vivado IDE desktop icon

> **Tip:** Right-click the Vivado IDE shortcut icon → **Properties** → update the **Start In** field to control where log and journal files are written.

### Launching the Vivado IDE from the Command Line (Windows or Linux)

```bash
vivado
```

> **Note:** This automatically runs `vivado -mode gui`. Use `vivado -help` to see all command line options.

### Launching the Vivado IDE from the Tcl Shell

```tcl
start_gui
```

---

## Using the Vivado IDE

When launched, the Vivado IDE displays the **Getting Started page** with options to begin working:

### Quick Start Options

| Action | Description |
|--------|-------------|
| **Create Project** | Launch the New Project wizard |
| **Open Project** | Open an existing project |
| **Open Example Project** | Open example projects provided by AMD |
| **Recent Projects** | Quick access to recently used projects |

---

## Starting with a Project

When working with a project, the tool automatically:

- Manages your design files and tracks file status
- Provides predefined design flow steps
- Generates results reports at each stage

### See Also

- Vivado Design Suite User Guide: System-Level Design Entry (UG895)
- Vivado Design Suite User Guide: Design Flows Overview (UG892)

---

## Managing IP

You can create an **IP location** to configure and manage IP remotely, enabling access from:

- Different design projects
- Source control management systems

The **Vivado IP catalog** allows you to:

- Browse and customize delivered IP
- Open existing IP and repositories

### See Also

- Vivado Design Suite User Guide: System-Level Design Entry (UG895)
- Vivado Design Suite User Guide: Designing with IP (UG896)

---

## Opening the Hardware Manager

The **Vivado Hardware Manager** allows you to program your design into a device and debug using:

| Feature | Description |
|---------|-------------|
| **Vivado Logic Analyzer** | Debug using ILA, VIO, Memory IP, and JTAG-to-AXI cores |
| **Vivado Serial I/O Analyzer** | Test and configure GTs using IBERT example design from IP catalog |

### Debug IP Cores

| Core | Purpose |
|------|---------|
| **ILA** (Integrated Logic Analyzer) | Capture and view internal signal activity |
| **VIO** (Virtual I/O) | Drive and monitor internal signals in real time |
| **Memory IP** | Debug memory interfaces |
| **JTAG-to-AXI** | Access AXI-mapped registers via JTAG |
| **IBERT** | In-system BER testing for serial transceivers |

### See Also

- Vivado Design Suite User Guide: Programming and Debugging (UG908)

---

## Vivado Store

The **Vivado Store** consolidates Tcl apps, board files, and configurable example designs into a single location. A catalog file maintains the list of all available items.

### Store Categories

| Category | Description | Source |
|----------|-------------|--------|
| **Tcl Apps** | Open-source Tcl scripts and utilities for the Vivado Design Suite | Community-contributed |
| **Boards** | AMD and third-party board files for simplified design creation | [GitHub: XilinxBoardStore](https://github.com/Xilinx/XilinxBoardStore) |
| **Example Designs** | Configurable example designs demonstrating specific tool capabilities | [GitHub: XilinxCEDStore](https://github.com/Xilinx/XilinxCEDStore) |

### Managing Store Items

- Click the **refresh button** for the respective store (lower left-hand corner) to update the catalog
- Individual items can be **installed**, **removed**, or **upgraded** from the GUI

### See Also

- Vivado Design Suite User Guide: Using Tcl Scripting (UG894)

---

## Reviewing Documentation and Videos

From the **Getting Started page**, you can open:

- User guides
- Tutorials
- Videos
- Release notes

All accessible via the **AMD Documentation Navigator**.

### See Also

- [Chapter 3: Learning About the Vivado Design Suite](chapter3_learning_about_the_vivado_design_suite.md)

---

## Best Practices

1. **Launch from your working directory** — Log files (`.log`) and journal files (`.jou`) are written to the launch directory
2. **Choose the right design flow mode** — Use Project Mode for automated management; use Non-Project Mode for full Tcl scripting control
3. **Use batch mode for CI/CD** — `vivado -mode batch -source <script>` enables fully automated, headless design flows
4. **Customize your installation** — Install only the device families you need to save disk space
5. **Leverage the Vivado Store** — Access community Tcl scripts, board files, and example designs for faster development
6. **Use the Hardware Manager for debug** — Add ILA/VIO cores early in your design for in-system debugging capability
7. **Migrate ISE projects early** — Refer to UG911 as ISE project formats are no longer supported from Vivado 2022.1+

---

## Quick Reference

| Task | Method |
|------|--------|
| Install Vivado | AMD Downloads page; customize device families |
| Launch Tcl shell | `vivado -mode tcl` |
| Launch batch mode | `vivado -mode batch -source <script>` |
| Launch GUI | `vivado` or Start Menu shortcut |
| Start GUI from Tcl | `start_gui` |
| Create project | Getting Started → New Project wizard |
| Manage IP | Vivado IP Catalog |
| Debug design | Hardware Manager (ILA, VIO, IBERT) |
| Get Tcl apps/boards | Vivado Store |
| View help | `vivado -help` |

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Getting Started (UG910)
- **Version:** v2025.2, November 20, 2025
- **Chapter:** 2 — Getting Started with the Vivado Design Suite
- **Pages:** 6–11
