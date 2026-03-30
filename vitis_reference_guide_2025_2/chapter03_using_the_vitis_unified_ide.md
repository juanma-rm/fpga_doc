# Chapter 3: Using the Vitis Unified IDE

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 3 (pp. 213–306)

## Overview

This chapter describes the AMD Vitis™ Unified IDE — the integrated development environment for creating, building, debugging, and profiling accelerated and embedded applications. It covers IDE launch and layout, the migration from the Classic IDE, all component creation workflows (AI Engine, HLS, Application, Platform), system project creation and build, debugging at all levels (hw_emu and hardware), Python API scripting, and the interactive Python shell.

---

## Table of Contents

| Section | Description |
|---|---|
| [Migrating from the Classic IDE](#migrating-from-the-classic-ide) | Export utility, migrate.py, supported project types |
| [Launching the Vitis Unified IDE](#launching-the-vitis-unified-ide) | Command-line launch options |
| [IDE Views and Features](#ide-views-and-features) | Toolbar, Component Explorer, Flow Navigator, Console |
| [Preferences](#preferences) | Configuring IDE behavior |
| [Creating Components](#creating-components) | AI Engine, HLS, Application, Platform components |
| [Embedded Software Development Flow](#embedded-software-development-flow) | Creating embedded applications via GUI and Python API |
| [Creating System Projects](#creating-system-projects) | Heterogeneous computing projects for embedded and data center |
| [System Project Structure](#system-project-structure) | Configuration files: vitis-sys.json, CMakeLists.txt, config.cfg |
| [Building System Projects](#building-system-projects) | Build All, hw_emu and hw targets, reports |
| [Launching Run and Debug](#launching-run-and-debug) | Launch configurations and launch.json |
| [Debugging System Projects](#debugging-system-projects) | Debug view, QEMU, embedded debugging |
| [Creating Bare-Metal Systems](#creating-bare-metal-systems) | Bare-metal platforms, applications, and packaging |
| [Migrating Command-Line Projects to IDE](#migrating-command-line-projects-to-ide) | User-managed flow, analyzing results |
| [Debugging AI Engine and System Projects](#debugging-ai-engine-and-system-projects) | Recommended 4-step debug process |
| [Hardware Debug from IDE](#hardware-debug-from-ide) | SD card, TCF agent, target connections |
| [Using the Debug Environment](#using-the-debug-environment) | Breakpoints, watchpoints, memory, registers, pipeline |
| [Programming Device and Flash Memory](#programming-device-and-flash-memory) | Device programming workflows |
| [Vitis Interactive Python Shell](#vitis-interactive-python-shell) | Auto-completion and shell commands |
| [Python API for Managing IDE Components](#python-api-for-managing-ide-components) | Server-client architecture, script builder |
| [Vitis IDE Examples](#vitis-ide-examples) | Built-in example projects |

---

## Migrating from the Classic IDE

### Export Utility

Use the Classic IDE export utility to generate a migration package from existing projects.

### migrate.py Script

Run the `migrate.py` script to convert exported Classic IDE projects to Unified IDE format:

```bash
python migrate.py --input <classic_export> --output <unified_workspace>
```

### Supported Project Types

| Project Type | Limitations | Workaround |
|---|---|---|
| **Embedded Platforms** | Local BSP source changes not migrated; new BSP is created with settings applied. SW repositories added in Classic IDE not migrated (warning displayed). IP drivers from XSAs created with 2023.1 or older may not work. | Copy sources to new BSP manually. Migrate SW repos to lopper (see UG1400); add path to migration script. Regenerate the XSA. |
| **Embedded Software Applications** | Applications referencing platforms outside the current workspace cannot be migrated. | Migrate the platform first, then update the application to use the new platform before migration. |
| **HW Link** | Hardware linker options defined via "Extra V++ command line options" are not migrated. | Manually define these options in `hw_link.cfg` for the System project. |
| **Accelerated Host Applications** | Only `-D` (defines), `-I` (include paths), `-L` (library paths), and `-l` (libraries) are migrated. | Set other compiler/linker settings manually in the Application component's C/C++ build settings. |
| **HLS Component** | Fully supported | — |
| **AI Engine Component** | Fully supported | — |

---

## Launching the Vitis Unified IDE

```bash
vitis [options]
```

### Command Options

| Option | Description |
|---|---|
| `-workspace <path>` | Open or create workspace at specified path |
| `-a <summary_file>` | Open the Analysis View with a summary file |
| `-i` | Launch in interactive Python shell mode |
| `-s <script.py>` | Execute a Python script |
| `-j <json_file>` | Load a JSON configuration |
| `-help` | Display help information |
| `-version` | Display version information |

---

## IDE Views and Features

### Toolbar

The toolbar provides quick access to build, run, and debug commands.

### Component Explorer

Displays workspace contents organized by components and system projects. Right-click items for contextual actions.

### Flow Navigator

Guides you through component-specific flow steps:
- **HLS Components:** C Simulation → C Synthesis → C/RTL Co-Simulation → Package → Implementation
- **AI Engine Components:** Build → Simulate/Debug → Profile
- **System Projects:** Build All → Run → Debug → Analyze

### Console and Terminal

- **Console:** Displays build output and messages
- **Terminal:** Integrated terminal for command-line operations

### Additional Views

| View | Description |
|---|---|
| **Index** | Global search and navigation |
| **Explorer View** | File system browser |
| **Search View** | Full-text search across workspace |
| **Source Control** | Git integration |
| **Debug View** | Debugging controls and inspection |
| **Example View** | Browse and open built-in examples |
| **Code View / Smart Editor** | Source editor with language support |

---

## Preferences

Configure IDE behavior through **File → Preferences → Settings**:

| Category | Settings |
|---|---|
| **Parallel Compiling** | Number of parallel compilation jobs |
| **File Change Notification** | How the IDE responds to external file changes |
| **Workspace Journal** | Logging of workspace operations |
| **External Lopper Support** | Configuration for device tree generation |

---

## Creating Components

### AI Engine Component

1. **File → New Component → AI Engine**
2. Specify name, location, and platform
3. Add graph and kernel source files
4. Configure `aiecompiler.cfg`

### HLS Component

1. **File → New Component → HLS**
2. Specify name, location, config file
3. Add source files and select top function
4. Set target part/platform, clock, and flow target

### Application Component

#### Data Center Application

1. **File → New Component → Application**
2. Select **Data Center** as the target
3. Specify platform, host source files
4. Configure build options

#### Embedded Application

1. **File → New Component → Application**
2. Select **Embedded** as the target
3. Specify platform and sysroot
4. Add source files and configure

### Platform Component

1. **File → New Component → Platform**
2. Provide the hardware specification (.xsa file)
3. Add software domains (standalone, Linux)
4. Configure platform options

---

## Embedded Software Development Flow

### Workflow Overview

```
Hardware Spec (.xsa) → Platform → Domain → Application → Build → Run/Debug
```

### Creating Embedded App Components (GUI)

1. Create a platform component from an `.xsa` file.
2. Add a software domain (e.g., standalone/bare-metal or Linux).
3. Create an application component targeting the platform.
4. Add source files and configure build settings.
5. Build and deploy.

### Creating Embedded App Components (Python API)

```python
client = create_client()

# Create platform
platform = client.create_platform_component(
    name="my_platform",
    hw="design.xsa",
    os="standalone",
    proc="psu_cortexa53_0"
)
platform.build()

# Create application
app = client.create_app_component(
    name="my_app",
    platform=platform,
    template="hello_world"
)
app.build()
```

---

## Creating System Projects

### Embedded Flow

Create a system project that integrates PL kernels, AI Engine graphs, and embedded software:

1. **File → New → System Project**
2. Select the base platform
3. Add components:
   - PL kernel components (.xo)
   - AI Engine components (.libadf.a)
   - Software application
4. Configure hardware linking and package settings

### Data Center Flow

Create a system project for data center acceleration:

1. **File → New → System Project**
2. Select the target platform (e.g., Alveo)
3. Add PL kernel and host application components
4. Configure binary container settings

### Creating from Examples

Open the **Example View** to create a system project from built-in templates.

### Managing Components

Add or remove components from a system project:
- Right-click the system project → **Add Component** / **Remove Component**

---

## System Project Structure

### Configuration Files

| File | Description |
|---|---|
| `vitis-sys.json` | System project metadata and component references |
| `CMakeLists.txt` | CMake build configuration for the host application |
| `compile_commands.json` | Compilation database for editor IntelliSense |
| `config.cfg` | v++ configuration file for link and package |

### Hardware Link Settings

Configure through the system project settings or `config.cfg`:

| Category | Settings |
|---|---|
| **Debug** | Enable debug features |
| **Report Level** | Verbosity of link reports |
| **HW Optimization** | Optimization strategies |
| **Export Archive** | Export linked archive |
| **Export Hardware** | Export hardware platform |
| **Trace Memory** | Memory allocation for trace |

### Kernel Data Settings

| Setting | Description |
|---|---|
| **CU Name** | Compute unit instance name |
| **Compute Units** | Number of compute unit instances |
| **Memory** | Memory bank assignment |
| **SLR** | SLR placement (multi-die devices) |
| **Protocol Checker** | Enable AXI protocol checking |
| **ChipScope** | Insert ILA debug probes |
| **Data Transfer** | Data transfer profiling |
| **Execute** | Execution profiling |
| **Stall Profiling** | Pipeline stall profiling |

### AI Engine Connectivity

Configure stream connections between PL kernels and AI Engine:

```ini
[connectivity]
stream_connect=<pl_kernel_port>:<aie_port>
```

### Package Configuration

| Category | Settings |
|---|---|
| **General** | Output format and name |
| **Linux Boot** | Boot image, rootfs, kernel image |
| **AI Engine Settings** | AI Engine-specific package options |

---

## Building System Projects

### Build All

The **Build All** action compiles all components and runs link and package steps.

### Build Targets

| Target | Description |
|---|---|
| **hw_emu** | Hardware emulation build (simulated hardware) |
| **hw** | Hardware build (for deployment on device) |

### Reports

After building, review reports in the Analysis View:
- Compile summary per kernel
- Link summary
- Package summary
- Guidance reports (HTML)

---

## Launching Run and Debug

### Launch Configurations (launch.json)

Configure run and debug sessions with `launch.json`:

```json
{
    "name": "System Debugger",
    "type": "vitis",
    "request": "launch",
    "target": "hw_emu",
    "platform": "path/to/platform",
    "application": "path/to/app"
}
```

### Hardware Emulation (hw_emu)

1. Build the system project for `hw_emu` target.
2. Select **Run As → Launch on Emulator** or configure launch.json.
3. The emulator launches QEMU (for embedded) and the PL simulation.

### Hardware (hw)

1. Build for `hw` target.
2. Deploy to the device (SD card, JTAG, or network).
3. Run the application on hardware.

---

## Debugging System Projects

### Debug View

The Debug View provides:
- Call stack navigation
- Variable inspection
- Breakpoint management
- Thread selection (multi-processor debugging)

### QEMU for Embedded

When debugging embedded system projects in hw_emu, QEMU emulates the processor subsystem:
- PS (Processing System) emulation
- Memory-mapped I/O simulation
- Interrupt handling

---

## Creating Bare-Metal Systems

### Creating a Bare-Metal Platform

1. Create a Platform component from an `.xsa` file.
2. Add a **standalone** domain for the target processor.
3. Build the platform.

### Creating a Bare-Metal Application

1. Create an Application component targeting the bare-metal platform.
2. Select a template (e.g., Hello World) or add custom source files.
3. Configure BSP settings.

### Packaging

Package the application for deployment:
- Boot image generation (BOOT.BIN)
- Flash image creation

---

## Migrating Command-Line Projects to IDE

### User-Managed Flow

Import command-line projects into the IDE using the user-managed flow:

1. Create a new system project in the IDE.
2. Point to existing source files and pre-built artifacts.
3. Configure build settings to match the command-line flow.

### Analyzing Results

Open command-line generated summary files in the IDE's Analysis View for visual analysis and debugging.

---

## Debugging AI Engine and System Projects

### Recommended 4-Step Debug Process

| Step | Target | Purpose |
|---|---|---|
| **1. x86sim** | x86 simulation | Functional verification of AI Engine kernels |
| **2. aiesimulator** | AI Engine simulator | Cycle-accurate simulation and profiling |
| **3. hw_emu** | Hardware emulation | Full system simulation including PL and PS |
| **4. hw** | Hardware | On-device verification and debug |

Progress through each step, fixing issues at the earliest possible stage.

### Component-Based Flow Design Debug

Configure the QEMU launch dialog with:

| Option | Description |
|---|---|
| **Waveform** | Enable waveform capture during emulation |
| **Trace** | Enable event tracing |
| **Profile** | Enable profiling data collection |
| **Key-Value Pairs** | Custom emulation settings |

---

## Hardware Debug from IDE

### SD Card Deployment

1. Build the system project for hw target.
2. Copy the SD card image to the device.
3. Boot the device and connect via network.

### TCF Agent

Connect to the running target via TCF (Target Communication Framework):

```bash
# On the target device
ifconfig          # Get IP address
# TCF agent starts automatically on Linux boot
```

### Target Connections

Configure target connections in the IDE:
1. **Window → Target Connections**
2. Add a new connection (hostname/IP, port)
3. Select the target processor

### Launch Configurations

Create hardware debug launch configurations specifying:
- Target connection
- Application executable
- Symbol file
- Processor target

---

## Using the Debug Environment

### Breakpoints

| Type | Description |
|---|---|
| **Line breakpoints** | Break at a specific source line |
| **Function breakpoints** | Break at function entry |
| **Conditional breakpoints** | Break when a condition is true |
| **Hardware breakpoints** | Use processor hardware breakpoint resources |

### Watchpoints

Monitor variable access:
- **Read** watchpoints: trigger on variable read
- **Write** watchpoints: trigger on variable write
- **Access** watchpoints: trigger on any access

### Variable View

Inspect and modify program variables during debug:
- Local variables
- Global variables
- Expression evaluation

### Memory Inspector

View and edit memory contents:
- Multiple display formats (hex, decimal, binary, ASCII)
- Configurable word size and columns
- Memory search

### Register Inspector

View processor registers:
- General-purpose registers
- Special-purpose registers
- Register groups

### Disassembly View

View machine code alongside source code for low-level debugging.

### Multi-Kernel Debug

Debug multiple kernels simultaneously in data center flows:
- Switch between kernel contexts
- Set breakpoints across kernels

### Buffer and Stream Data Viewing

Inspect buffer contents and stream data during debug:
- View input/output buffer data
- Monitor stream transactions

### Pipeline View

Visualize the AI Engine execution pipeline:
- Instruction flow through pipeline stages
- Stall detection
- Performance analysis

---

## Programming Device and Flash Memory

Program devices and flash memory from the IDE:

1. **Vitis → Program Device** to program via JTAG.
2. **Vitis → Program Flash** to write to flash memory (QSPI, SD).
3. Select the target, bitstream/PDI, and configuration options.

---

## Vitis Interactive Python Shell

Launch the interactive Python shell:

```bash
vitis -i
```

### Features

- **Auto-completion** — Tab completion for commands and APIs
- **Command history** — Navigate previous commands

### Shell Commands

| Command | Description |
|---|---|
| `edit` | Open a file in the editor |
| `run` | Execute a Python script |
| `env` | Display environment settings |
| `history` | Show command history |
| `time` | Time a command execution |
| `clear` | Clear the terminal |

---

## Python API for Managing IDE Components

### Architecture

The Python API uses a **server-client architecture**:
- The Vitis IDE runs as a server
- Python scripts connect as clients
- Commands execute through the client connection

### Script Building

Use the `builder.py` logger to generate Python scripts from GUI actions:
- Enable script logging in preferences
- Perform actions in the GUI
- Review the generated Python script

### Create and Build AI Engine Component

```python
client = create_client()
comp = client.create_aie_component(name="aie_comp", platform="<platform>")
comp.import_files(sources=["graph.cpp", "kernels/"])
comp.add_cfg_file("aiecompiler.cfg")
comp.build(target="hw")
comp.report()
comp.clean()
```

### Create and Build HLS Component

```python
comp = client.create_hls_component(name="hls_comp", part="<part>")
comp.add_cfg_file("hls_config.cfg")
comp.set_value(key="hls.top", value="my_function")
comp.run(operation="C_SYNTHESIS")
```

### Create and Build System Project

```python
sys = client.create_sys_project(name="my_system", platform="<platform>")
sys.add_container(name="binary_container_1")
sys.add_component(component="kernel_comp", container="binary_container_1")
sys.build(target="hw_emu")
```

### Create and Build Platform Component

```python
plat = client.create_platform_component(
    name="my_platform",
    hw="design.xsa",
    os="standalone",
    proc="psu_cortexa53_0"
)
plat.add_domain(name="domain_1", os="standalone", proc="psu_cortexa53_0")
plat.build()
```

### Create and Build Application Component

```python
app = client.create_app_component(
    name="my_app",
    platform="my_platform"
)
app.set_app_config(key="USER_COMPILE_OPTIONS", value="-O2")
app.set_sysroot(path="/path/to/sysroot")
app.build()
```

---

## Vitis IDE Examples

The IDE includes built-in examples accessible from the **Example View**:

- System design examples
- AI Engine examples (18 templates — see [Chapter 5](chapter05_managing_the_ai_engine_component_in_the_vitis_unified_ide.md))
- HLS examples
- Embedded application examples

Open the Example View: **View → Example View** or from the Welcome page.

---

## Best Practices

1. **Migrate early** — Use `migrate.py` to move Classic IDE projects to the Unified IDE to access the latest features.
2. **Follow the 4-step debug process** — Progress from x86sim → aiesim → hw_emu → hw for efficient debugging.
3. **Use the Flow Navigator** — Let the Flow Navigator guide you through the correct sequence of build and analysis steps.
4. **Generate scripts** — Use the script builder logger to capture GUI workflows as Python scripts for automation.
5. **Configure kernel data carefully** — Set memory bank assignments, SLR placement, and compute units in the system project settings.
6. **Enable protocol checkers** — Use AXI protocol checkers during hw_emu to catch interface violations early.
7. **Use templates** — Start new projects from built-in examples to establish correct project structure.
8. **Leverage the Python API** — Automate repetitive tasks and enable CI/CD pipelines using the Python CLI.

---

## See Also

- [Chapter 1: Navigating Content by Design Process](chapter01_navigating_content_by_design_process.md) — Design process overview
- [Chapter 2: Vitis Commands and Utilities](chapter02_vitis_commands_and_utilities.md) — Command-line equivalents for IDE operations
- [Chapter 4: Managing Vitis HLS Components](chapter04_managing_the_vitis_hls_components_in_the_vitis_unified_ide.md) — HLS-specific IDE workflows
- [Chapter 5: Managing AI Engine Components](chapter05_managing_the_ai_engine_component_in_the_vitis_unified_ide.md) — AI Engine-specific IDE workflows
- [Chapter 6: Managing Integration Projects](chapter06_managing_the_integration_project_component.md) — Integration project wizard
- [Chapter 8: Working with the Analysis View](chapter08_working_with_the_analysis_view.md) — Report viewing and analysis
- [Chapter 9: Additional Information](chapter09_additional_information.md) — IDE output directory structure
- *Embedded Design Development Using Vitis (UG1701)*

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 3 (pp. 213–306)*
