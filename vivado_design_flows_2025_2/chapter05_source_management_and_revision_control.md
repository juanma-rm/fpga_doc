# Chapter 5: Source Management and Revision Control Recommendations

## Overview

This chapter provides methodologies for source management and revision control when working with the AMD Vivado Design Suite. It defines the minimum set of files needed to recreate a design, compares script-based and source-based revision control strategies, and provides recommendations for managing different source types (RTL, XDC, IP, block designs).

---

## Table of Contents

| Section | Description |
|---|---|
| [Interfacing with Revision Control Systems](#interfacing-with-revision-control-systems) | General principles for revision control |
| [Project vs. Non-Project Build Methodologies](#project-vs-non-project-build-methodologies) | Impact of build methodology on revision control |
| [Project Source Types](#project-source-types) | How to manage RTL, XDC, DCP, XCI, BD files |
| [Methods to Revision Control a Project](#methods-to-revision-control-a-project) | Script-based vs. source-based methodologies |
| [Other Files to Revision Control](#other-files-to-revision-control) | Additional files beyond primary sources |
| [Output Files to Optionally Revision Control](#output-files-to-optionally-revision-control) | Optional intermediate and hand-off files |
| [Archiving Designs](#archiving-designs) | Using `archive_project` for full project snapshots |

---

## Interfacing with Revision Control Systems

Vivado generates many intermediate files during design compilation. This chapter defines the **minimum set of files** necessary to recreate the design.

Key principles:
- The term **"manage"** refers to checking source versions in and out using a revision control system
- Managing additional intermediate files is always **optional** (but can improve compile time or simplify analysis)
- Vivado works with all major revision control systems: **RCS, CVS, SVN, ClearCase, Perforce, Git, BitKeeper**, and others

---

## Project vs. Non-Project Build Methodologies

| Methodology | Description | Revision Control Approach |
|---|---|---|
| **Project Mode** | Vivado manages file source sets, dependencies, and runs; driven by scripts or GUI | Revision control strategy depends on chosen method (script or source-based) |
| **Non-Project Mode** | Users compile designs directly from sources using scripts | Closely aligns with the script-based methodology |

> Revision control should not dictate how designs are compiled, but understanding the relationship between compilation method and revision control strategy is critical.

---

## Project Source Types

### RTL, XDC, and DCP

> **Recommendation:** Keep all design sources (RTL, XDC, DCP) **external to the project** and revision control them independently.

- Use `add_*` Tcl commands (not `import_*`) to reference external files
- Files remain in their original locations under revision control

### XCI (IP Configuration)

The recommended method to revision-control IP:

1. **Preserve the IP repository** (parametrizable IP source code)
2. **Check in the XCI file** (contains customization parameters)

The combination of repository + XCI enables Vivado to **regenerate** the IP instance for your design. Generated output products do not need to be preserved.

> **Recommendation:** Upgrade AMD IP when upgrading Vivado, since only the latest version is included.

#### If You Do Not Want to Upgrade IP

| Option | Method | Limitation |
|---|---|---|
| **XCI + output products** | Revision control XCI file and output products in `project.gen` | IP is locked; cannot be re-customized |
| **XCIX core container** | Single file containing XCI + output products | IP is locked; cannot be re-customized |
| **`write_ip_tcl`** | Generates Tcl script to recreate the IP | Requires the IP repository to be present |

> Locked IP can always be upgraded to the latest version to remove restrictions.

### BD (Block Designs)

To revision-control a block design:

- **Required:** Check in the BD file itself
- **Required:** IP repositories used by the BD must be present
- XCI files under the BD source directory contain IP customizations after parameter propagation — these are **automatically regenerated** during BD validation

> ⚠️ When the project is rebuilt, the BD and XCI files beneath it **must be writable**.

#### Alternative: `write_bd_tcl`

Generates a Tcl script to recreate the BD, preserving IP customizations, connections, and all BD properties.

> **Tip:** Use the `diffbd` utility to view differences between two versions of a block diagram. See UG994.

#### Block Design Containers

When block design containers are used:
- Source BD resides in the `.srcs` folder
- Uniquified instances reside in the `.gen` directory
- After restoring the project, instance BDs may appear as missing — regenerating the parent BD recreates them

---

## Methods to Revision Control a Project

### Script-Based Revision Control Methodology

Focus: **Recreate the project from sources using a Tcl script.**

**Steps:**
1. Keep source files **external to the project** (ideally outside the Vivado build directory)
2. Revision-control the source repository
3. Generate a script to recreate the design
4. Revision-control the script (maintain it like any other source as the design evolves)
5. **Test your methodology** — regularly rebuild the design from sources to catch issues

> ⚠️ When Vivado is using source files, they **must be writable**.

#### Generating a Script to Recreate a Design

| Method | Advantages | Drawbacks |
|---|---|---|
| **Manually create script** | Short, well-organized | Risk of missing project settings |
| **`write_project_tcl`** | Comprehensive — captures all files and settings | More verbose and complex |

> `write_project_tcl` calls `write_bd_tcl` for each BD in the project. Alternatively, BDs can be included directly as project sources.

> **Note:** `write_project_tcl` recreates the design as originally created. For IP Integrator designs, propagated parameters require re-running `validate_bd_design`.

### Source-Based Revision Control Methodology

Focus: **Revision control the project file (`.xpr`) and sources directory (`.srcs`) directly.**

**Steps:**
1. Keep source files external to the project
2. Revision-control the source repository
3. Revision-control the `project.xpr` file
4. Revision-control the `project.srcs` directory
5. Test your methodology regularly

The project is recreated by restoring `project.srcs` and `project.xpr`, then opening the XPR file.

> **Note:** Since 2020.2, generated files reside in `project.gen` (separate from `project.srcs`).

### Comparison: Script-Based vs. Source-Based

| Attribute | Script-Based | Source-Based |
|---|---|---|
| **Files to check in** | A Tcl script (auto-generate with `write_project_tcl` or manually create) | Project `.xpr` + `.srcs` directory |
| **Size** | Small | Medium |
| **Compile time** | Slow (BD/IP must be rebuilt, output products regenerated) | Medium (project available immediately, output products must be regenerated) |
| **External sources** | Revision control separately | Revision control separately |
| **BD sources** | Must be writable | Must be writable |
| **IP sources** | Can be locked | Can be locked |
| **Availability** | Must run script before opening project | Project available immediately after checkout |

> **Tip:** With **external OOC synthesis caching** enabled, compile time differences between the two methods become negligible.

---

## Other Files to Revision Control

Beyond primary sources, the following files may be required to rebuild a design:

- **Simulation test benches**
- **HLS IP**
- **Pre/post Tcl hook scripts** (used for synthesis or implementation)
- **Incremental compile DCPs**
- **ELF and MEMDATA files**
- **AI Engine archives**

> ⚠️ Pay special attention to files that are **referenced by `set_property` commands** but not added directly to the project. These should reside external to the project and be revision-controlled separately.

---

## Output Files to Optionally Revision Control

| File Type | Use Case |
|---|---|
| **Simulation scripts** (from `export_simulation`) | Hand-off between design and verification; snapshot at different stages |
| **XSA files** | Hardware hand-off between Vivado and AMD Vitis |
| **Bitstreams / PDIs** | Device programming files |
| **LTX files** | Hardware debug configuration |
| **Intermediate DCP files** | Design checkpoints from the flow |
| **IP output products** | Pre-generated IP for faster rebuilds |

---

## Archiving Designs

The `archive_project` command compresses the entire project into a ZIP file:

```tcl
archive_project my_design_archive.zip
```

**Behavior:**
- Copies the entire project locally in memory and zips it
- Leaves the original project intact
- Copies **remote sources** into the archive
- Options available for storing run results

> **Tip:** You may also need to include your `vivado_init.tcl` file if it sets parameters or variables that affect the design.

### See Also
- *Vivado Design Suite User Guide: System-Level Design Entry (UG895)*

---

## Best Practices

1. **Keep all source files external to the project** — reference them rather than copying
2. **Use the script-based method** for minimal revision control footprint
3. **Use `write_project_tcl`** for reliable script generation — maintain it as a design source
4. **Test your methodology regularly** — rebuild from sources at a regular cadence to catch issues
5. **Always use XCI files to reference IP** — preserve the IP repository and XCI together
6. **Upgrade AMD IP with each Vivado release** to avoid locked/obsolete IP
7. **Use XCIX core containers** for simple single-file IP revision control
8. **Ensure BD and IP source files are writable** when Vivado is using them
9. **Revision-control `set_property` referenced files** that are not directly added to the project
10. **Archive projects** using `archive_project` for portable, self-contained design snapshots

---

## Quick Reference: Minimum Files to Revision Control

| Source Type | What to Check In | Required Companion |
|---|---|---|
| **RTL** (`.v`, `.vhd`, `.sv`) | Source files | — |
| **XDC** (`.xdc`, `.sdc`) | Constraint files | — |
| **DCP** (`.dcp`) | Design checkpoints | — |
| **IP** (`.xci`) | XCI file | IP repository |
| **IP (locked)** (`.xcix`) | Core container | — |
| **Block Design** (`.bd`) | BD file | IP repositories |
| **Project (script-based)** | Tcl rebuild script | External sources |
| **Project (source-based)** | `.xpr` + `.srcs` directory | External sources |
| **Simulation** | Test bench files | — |
| **Tcl hooks** | `tcl.pre` / `tcl.post` scripts | — |

---

## See Also

- [Chapter 3: Using Project Mode](chapter03_using_project_mode.md)
- [Chapter 4: Using Non-Project Mode](chapter04_using_non-project_mode.md)

---

## Source Attribution

- **Source:** *Vivado Design Suite User Guide: Design Flows Overview (UG892)*, v2025.2, November 20, 2025
- **Chapter:** Chapter 5 — Source Management and Revision Control Recommendations (Pages 85–91)
- **Publisher:** Advanced Micro Devices, Inc.
