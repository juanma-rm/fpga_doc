# Chapter 6 — Develop

How to create and manage target platforms, domains, applications, system projects, build configurations, linker scripts, and custom libraries in the Vitis Unified IDE.

---

## Table of Contents

- [Managing Platforms and Platform Repositories](#managing-platforms-and-platform-repositories)
- [Target Platform](#target-platform)
  - [Creating a Hardware Design (XSA File)](#creating-a-hardware-design-xsa-file)
  - [Creating a Platform Component from XSA](#creating-a-platform-component-from-xsa)
  - [Customizing a Pre-Built Platform](#customizing-a-pre-built-platform)
  - [Adding a Domain to an Existing Platform](#adding-a-domain-to-an-existing-platform)
  - [Configuring a Domain](#configuring-a-domain)
  - [Switching FSBL Targeting Processor](#switching-fsbl-targeting-processor)
  - [Modifying Domain Sources](#modifying-domain-sources)
  - [Creating a Software Repository](#creating-a-software-repository)
  - [Updating the Hardware Specification](#updating-the-hardware-specification)
- [Applications](#applications)
  - [Creating an Application Component](#creating-an-application-component)
  - [Creating a System Project](#creating-a-system-project)
  - [Build Configuration Settings](#build-configuration-settings)
  - [Linker Scripts](#linker-scripts)
  - [Building the Application Component](#building-the-application-component)
- [Creating a Library Project](#creating-a-library-project)

---

## Managing Platforms and Platform Repositories

Access: **Vitis → Platform Repositories**

The Platform Repositories window shows:
- **Upper section:** Base platforms from the Vitis installation (available to all users)
- **Lower section:** Platforms from `$PLATFORM_REPO_PATHS` environment variable

| Action | Description |
|--------|-------------|
| **+** | Add a platform search directory |
| **-** | Remove a platform search directory |
| **Info link** | View detailed platform information |

---

## Target Platform

A **target platform** = hardware components (XSA) + software components (domains, boot components like FSBL/PLM).

A **platform project** is an editable target platform in the workspace where you can add/modify/remove domains and boot components.

A **domain** = BSP or OS targeting one processor or an isomorphic processor cluster (e.g., 4× Cortex-A53 with SMP Linux). A platform can contain unlimited domains.

---

### Creating a Hardware Design (XSA File)

Create hardware designs in AMD Vivado Design Suite and export as XSA:

1. Create a Vivado project
2. Create a block design
3. Generate the image or bitstream
4. **File → Export → Export Hardware** → select **Fixed Platform**

**Reference tutorials:**
- Zynq 7000 SoC: Embedded Design Tutorial (UG1165)
- Zynq UltraScale+ MPSoC: Embedded Design Tutorial (UG1209)
- Versal Adaptive Compute Acceleration Platform (UG1305)

---

### Creating a Platform Component from XSA

**File → New Component → Platform** (or Welcome page → Create Platform Component)

**Wizard steps:**
1. Enter component name and location → **Next**
2. Browse for XSA file (or select built-in/existing platform) → **Next**
3. Select Operating System and Processor → **Next**
4. Review summary → **Finish**

**Advanced SDTgen options:**
| Option | Description |
|--------|-------------|
| SDT Source REPO | Custom SDTgen repository |
| Board DTS | Board name for board DTS file |
| User DTS | User device tree file (DTSI) |

**Boot artifact options by device family:**

| Device | Generate Boot Artifacts | PMU | DTB | DTB Overlay |
|--------|------------------------|-----|-----|-------------|
| **Zynq** | FSBL for init | N/A | Linux only | Linux only |
| **ZynqMP** | FSBL for init | Required for Linux (manages high-security) | Linux only | Linux only |
| **Versal** | N/A (uses PDI) | N/A | Linux only | Linux only |

**After creation:** The `vitis-comp.json` file opens. Contents vary by OS:
- **Linux:** Specify BIF file, Boot Component Directory, SD Card Directory, Qemu data
- **Standalone/FreeRTOS:** No special operations needed

**Third-party compiler support:**

| Compiler | Supported Processors |
|----------|---------------------|
| ARMClang | Versal A72, R5 |
| ARMCC | Zynq A9 |
| IAR | ZynqMP R5, Zynq A9 |

> ⚠️ These compilers are not included with Vitis — install separately and add to `$PATH`.

```python
# CLI example for ARMClang:
platform = client.create_platform_component(
    name="platform", hw_design="vck190", os="standalone",
    cpu="psv_cortexa72_0", domain_name="standalone_psv_cortexa72_0",
    generate_dtb=False, advanced_options=advanced_options,
    compiler="armclang"
)
```

---

### Customizing a Pre-Built Platform

1. Ensure platform is visible in **Vitis → Platform Repositories**
2. **File → New Component → Platform** → select **Existing platform**
3. Complete wizard → platform copies to workspace for editing

---

### Adding a Domain to an Existing Platform

1. Open `vitis-comp.json` for the platform
2. Click **+ Add Domain**
3. Specify Name, Display name, OS (Linux/FreeRTOS/Standalone), Processor
4. Click **OK**

**Domain types:**
- **FreeRTOS / Standalone:** BSP created with configurable libraries
- **Linux:** Configure BIF, Boot Components Directory, Pre-Built Image Directory, DTB, FAT32 Partition, Qemu Data

> **Tip:** Adding sysroot to a Linux domain is not supported because Windows cannot copy symlinks.

---

### Configuring a Domain

#### Board Support Package Settings (Standalone/FreeRTOS only)

Open `vitis-comp.json` → expand domain → Board Support Package

| Page | Description |
|------|-------------|
| **OS Settings** | Configure OS and processor parameters |
| **Library Settings** | Configure parameters for each enabled library |
| **Drivers** | Assign device drivers per peripheral; set to `none` to remove |
| **Build Settings** | Toolchain selection and extra configuration |

#### Linux Domain Settings

| Field | Description |
|-------|-------------|
| BIF File | Boot Image Format file (Browse or generate) |
| Pre-Built Image Directory | Linux image files (boot components, kernel, rootfs) |
| DTB File | System device tree binary (auto-populated from Pre-Built Image Dir) |
| FAT32 Partition Directory | Additional FAT32 partition files |
| Qemu Data | Boot components for emulation (auto-populated on build) |

---

### Switching FSBL Targeting Processor

On Zynq UltraScale+ MPSoC, retarget FSBL to a different processor:

1. Open `vitis-comp.json` → select `psu_cortexa53_0 → zynqmp_fsbl`
2. Click **Re-target to psu_cortexr5_0**
3. Rebuild the platform

### Modifying FSBL Source Code

1. Expand platform → Source → `zynqmp_fsbl_bsp/`
2. Modify source files
3. Rebuild platform

> To reset: Click **Regenerate BSP** on the Board Support Package overview page.

---

### Modifying Domain Sources

To modify driver/library code, create a custom repository:

1. Copy from `<Vitis_Install_Dir>/data/embeddedsw/`
2. Bump version in `.mld`/`.mdd` files
3. Add repository to Vitis

### Creating a Software Repository

**Required directory structure:**

```
Repository/
├── drivers/          # Device drivers
├── sw_services/      # Libraries
├── bsp/              # Board support packages
├── sw_apps/          # Standalone applications
└── sw_apps_linux/    # Linux applications
```

**Adding the repository:**
1. **Vitis → Embedded SW Repositories**
2. Click **+** under **Local Repositories** (workspace scope) or **Global Repositories** (all workspaces)
3. Click **OK**

**Precedence:** Local repos > Global repos > Vitis installation

### Resetting BSP Sources

1. Open `vitis-comp.json` → select domain
2. Click **Regenerate BSP** (only source files revert; settings are preserved)

---

### Updating the Hardware Specification

When the Vivado XSA is updated:

1. Open `vitis-comp.json`
2. Click **Switch / Re-Read XSA**
3. Select the updated XSA file

### Reading Hardware Specification

In `vitis-comp.json`, click **Hardware Specification** to view processor address info and PL IP addresses.

---

## Applications

### Creating an Application Component

**File → New Component → Application** (or Welcome → Create Embedded Application)

1. Input name and location → **Next**
2. Select fixed platform → **Next**
3. Select processor domain → **Next** (or **+ Create New** for a new domain)
4. Add source files/folders → **Next**
5. Review summary → **Finish**

> **Copy Source:** Enabled by default. Deselect to reference external source files directly.

**Linux application with sysroot toolchain:**
```python
# CLI arguments:
use_sysroot_toolchain=True
sysroot_toolchain=<TOOLCHAIN_PATH>
```

### Creating from Examples

1. **View → Examples** (or **Ctrl+Shift+R**)
2. Select example → **Show Details** → **Create Application Component from Template**

---

### Creating a System Project

**File → New Component → System Project**

1. Input name and location → **Next**
2. Select platform → **Next**
3. Configure Embedded Component Path → **Next**
4. Review → **Finish**

**Adding applications to system project:**
1. Open `vitis-sys.json` → System Project Settings → Components
2. Click **Adding Existing Components** → select application

**Rules:**
- Two standalone apps for the same processor **cannot** coexist in one system project
- A Cortex-A53 standalone app **cannot** combine with a Linux app (same processor cluster)

---

### Build Configuration Settings

All build settings are in `UserConfig.cmake` (supports both GUI and text editor views via `</>` button).

| Setting | Location in UserConfig.cmake | Description |
|---------|------------------------------|-------------|
| **Sources** | Compiler Settings → Sources | Add/remove source files |
| **Symbols** | Compiler Settings → Symbols | Add `#define` / `#undef` symbols |
| **Libraries** | Compiler Settings → Libraries | Library names and paths for the linker |
| **Linker Settings** | Compiler Settings → Linker Settings | Enable/disable linker flags |
| **Optimization** | Compiler Settings → Optimization | `-O` level and debug flags |
| **Miscellaneous** | Compiler Settings → Miscellaneous | Verbose, ANSI support, other flags |

**Build process:**
1. Vitis builds the BSP (platform)
2. Compiles application with platform-specific gcc/g++
3. Links object files from app + BSP using linker script

> ⚠️ Platform BSP changes do not auto-trigger rebuild. Set preference: "always build platform before application" or build manually.

---

### Linker Scripts

> Only standalone applications need linker scripts. Linux manages memory allocation.

The linker script generator reads the System Device Tree (SDT) to determine available memory sections.

**Reset linker script:**
1. Right-click app component → **Reset Linker Script** → **OK**

**Manually add linker script:**
1. Open `UserConfig.cmake` → Linker Script → Browse

**Modify linker script:**
1. Expand Sources → open `lscript.ld`
2. Use GUI editor or `</>` button for text mode

| Editor Section | Function |
|---------------|----------|
| **Add Memory Regions** | Add/modify name, base address, size |
| **Stack and Heap Sizes** | Edit stack/heap values |
| **Section to Memory Region Mapping** | Reassign sections to memory regions (batch select supported) |

> ⚠️ For multiprocessor systems, each processor runs a separate ELF with its own linker script. Ensure no memory overlap.

---

### Building the Application Component

1. Flow Navigator → select application component
2. Click **Build** → select build preference

Output files appear in the output directory under the application component.

**Reading ELF Disassembly:** Double-click the ELF file in the output directory.

---

## Creating a Library Project

**File → New Component → Static Library**

1. Input name and location → **Next**
2. Select fixed platform → **Next**
3. Select target processor domain → **Next**
4. Add source files/folders → **Next**
5. Review → **Finish**

Build via Flow Navigator. Linker settings do not apply to library components.

**Using custom libraries in application projects:** Configure in `UserConfig.cmake` → Libraries.

---

## See Also

- [Chapter 4 — Launching the Vitis IDE](ch04_launching_vitis_ide.md)
- [Chapter 5 — IDE Views and Features](ch05_ide_views_and_features.md)
- [Chapter 7 — Run, Debug, and Optimize](ch07_run_debug_optimize.md)

---

## Source Attribution

- **Document:** UG1400 (v2025.2) — Vitis Embedded Software Development
- **Date:** November 20, 2025
- **Chapter:** 6 (pp. 55–85)
