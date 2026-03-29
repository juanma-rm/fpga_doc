# Chapter 3 — Getting Started with the Vitis Software Platform

## Vitis Unified Software Platform Overview

The Vitis unified software platform combines all AMD software development into one environment, supporting both **embedded software development** and **application acceleration** flows.

**Key characteristics:**
- Based on **Eclipse Theia** framework (replacing the classic Eclipse-based IDE)
- Faster GUI response, rich open-source plugins, flexible configuration
- Works with hardware designs from AMD Vivado Design Suite

**Capabilities:**

| Feature | Description |
|---------|-------------|
| Platform creation | From Vivado-generated XSA; generate BSP for software development |
| Application creation | From example designs or empty templates |
| Configure & build | Platforms and applications |
| Run / Debug / Profile | On actual hardware |
| Target connections | Local or remote hardware via Target Connection Manager |
| Device support | MicroBlaze, Zynq 7000, Zynq UltraScale+ MPSoC, Versal adaptive SoC |
| Boot images | Create BOOT.bin |
| Flash programming | Configure devices |
| Source control | Integrated Git |
| CLI support | All features available from command line |

---

## Vitis Software Development Workflow

```
Export Hardware    Import XSA    Domain       Application    Application    System       Boot Image
from Vivado   →   to Vitis   →  Creation  →  Creation    →  Debugging   →  Debugging →  Generation
     (XSA)                                                                                (BOOT)
```

1. **Hardware engineers** export XSA from Vivado Design Suite
2. **Software developers** import XSA into Vitis by creating a **platform**
3. Create **domains** (BSP/OS with driver collection) within the platform
4. Create **applications** based on the platform and domains
5. **Debug** applications in the Vitis Unified IDE
6. Perform **system-level verification** for multi-app scenarios
7. Create **boot images** to initialize the system and launch applications

> **Note:** The Vitis Unified IDE supports two types of XSA:
> - **Fixed XSA** → Fixed platform for embedded development (complete device image from Vivado)
> - **Extensible XSA** → For acceleration development (device image created during v++ linking stage)
>
> ⚠️ Using an extensible platform for bare-metal applications can cause "cannot find corresponding devices" errors.

---

## Workspace Structure

| Concept | Description |
|---------|-------------|
| **Workspace** | Directory location for project data and metadata; required at IDE launch |
| **XSA** | Exported from Vivado — processor config, peripheral connections, address map, device init code |
| **SDT** | System Device Tree — generated from XSA via SDTGEN; captures HW metadata (not deployed on target) |
| **Platform** | Combination of hardware (XSA) + software (domains/BSPs, boot components like FSBL) |
| **Platform Component** | A project in Vitis Unified IDE that defines a platform |
| **Domain** | BSP or OS with software drivers; ties to a single processor or isomorphic cluster (e.g., A53_0 or A53) |
| **System Project** | Groups applications that run simultaneously on a device |
| **Application** | Source/header files compiled to ELF binary; each application requires a corresponding domain |

**Platform types:**

| Type | Description |
|------|-------------|
| **Embedded** | Fixed platform; supports Arm processors and MicroBlaze only |
| **Embedded Acceleration** | Fixed + acceleration; provides clocks, bus interfaces, interrupts for acceleration kernels |
| **Data Center Acceleration** | Acceleration kernels + x86 host applications via PCIe bus |

**System project rules:**
- Two standalone applications for the same processor **cannot** exist in one system project
- Two Linux applications **can** exist in one system project
- A workspace can contain multiple system projects
- System projects are optional for single-application scenarios

**Lopper utility:** Extracts HW metadata from SDT, including processor list, `xparameters.h` generation, linker script generation, and BSP creation.

---

## Migrating from Classic IDE to Unified IDE

### Method 1: Manual Migration (2025.1 Onward — Recommended)

Starting with 2025.1, the Classic IDE is removed. Manual recreation is required:

1. Generate new XSA with latest Vivado tools
2. Recreate platform project in Unified IDE from updated XSA
3. Recreate application project using the new platform
4. Import application source code into new project
5. Build and resolve any issues

### Method 2: Migration Utility (2023.2–2024.2 Only)

Available in Classic IDE for releases 2023.2, 2024.1, and 2024.2:

1. Open workspace in Classic Vitis IDE
2. Select **Vitis → Export Workspace to Unified IDE**
3. Specify migration target workspace location
4. Click **Finish** to generate migration script
5. Run: `vitis -s migrate.py`
6. Open migrated workspace in Vitis Unified IDE
7. Open platform JSON → click **Switch/Re-read XSA** to select updated XSA
8. Rebuild platform and applications

**Limitations:**

| Project Type | Limitation | Workaround |
|-------------|-----------|------------|
| Platform | Local BSP source changes not migrated; new BSP created with settings applied | Copy sources to new BSP manually |
| Platform | Embedded software repos cannot be migrated | Migrate repos to Lopper first; add path to migration script |
| Platform | IP drivers from XSAs created with 2023.1 or older may have compilation errors | Regenerate XSA with 2024.2+ release |
| Application | Cannot migrate apps referencing platforms outside workspace | Migrate platform first, update app to use new platform |
| Application | Device ID changes in `xparameters.h` (deprecated) | See standalone application migration details |
| Application | Debug configurations cannot be migrated | Recreate launch configuration in Unified IDE |

> To use the classic Vitis IDE in older releases: `vitis --classic`

---

## Standalone Application Component Migration Details

Driver APIs have changed in the Unified IDE:

- All driver APIs now use the **base address** of the peripheral IP (industry standard)
- `DeviceID` is **no longer generated** in `xparameters.h`
- Compiling migrated applications directly may cause compilation errors

> ⚠️ If your application relies on DeviceID for IP driver initialization, refer to **AR: Standalone Application Migration Details**.

---

## Unified IDE vs. Classic IDE Features

| Feature | Vitis Unified IDE | Vitis Classic IDE |
|---------|------------------|-------------------|
| Platform Creation | Target Platform | Target Platform |
| Application Development | Applications | Applications |
| Custom Libraries | Creating a Library Project | Using Customer Libraries in App Projects |
| Run Application | Running the Application Component | Run Application Project |
| Debug Application | Debugging Application Component | Debug Application Project |
| Cross Trigger | Cross-Triggering | Cross Triggering |
| TCF Profiling | ✅ | ✅ |
| Gprof Profiling | ❌ | ✅ |
| OS Aware Debug | ❌ | ✅ |
| XEN Aware Debug | ✅ | ✅ |
| Performance Analysis | ❌ | ✅ |
| Boot Image | Creating a Boot Image | Creating a Boot Image |
| Flash Programming | ✅ | ✅ |
| Multi-Cable / Multi-Device | ✅ | ✅ |
| Target Management | Target Connections | Target Connections |
| Version Control | Source Control (Git) | Git |
| User Managed Flow | User Managed Mode | ❌ |
| Import/Export | Project Export and Import | Project Export and Import |
| Software Debugger | Software Debugger Reference Guide (UG1725) | Software Command-Line Tool |
| Python CLI | Section III: Vitis Python API | ❌ |

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 3 (pp. 11–20)*
