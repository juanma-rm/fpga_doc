# Chapter 12: Launching the Vitis Unified IDE

> Source: UG1399 (v2025.2) January 22, 2026 — Vitis HLS User Guide, Section III: Vitis HLS Flow Steps, pages 331–335.

---

## Table of Contents

1. [Overview](#overview)
2. [Launching the IDE](#launching-the-ide)
3. [Welcome Screen Options](#welcome-screen-options)
4. [Features of the Vitis Unified IDE](#features-of-the-vitis-unified-ide)
5. [Using the Flow Navigator](#using-the-flow-navigator)
6. [Quick Reference](#quick-reference)

---

## Overview

The AMD Vitis™ Unified IDE is installed as part of the Vitis software platform and requires no additional installation. It provides a unified environment for HLS component development, integrating source editing, synthesis, simulation, and analysis under one interface.

> Reference: *Embedded Design Development Using Vitis* (UG1701) for full installation and launch details.

---

## Launching the IDE

### Step 1 — Source the environment

```bash
source <Vitis_Installation_Directory>/settings64.sh
```

This sets up all required environment variables for the Vitis software platform.

### Step 2 — Launch with a workspace

```bash
vitis -w <workspace>
```

| Argument | Description |
|---|---|
| `<workspace>` | Path to a folder that holds the elements of the HLS component (and optionally other design projects). Created if it does not exist. |

The workspace groups together:
- Source and data files that make up a design
- Tool configuration settings for that workspace
- One or more design components or projects

> **Tip:** On Windows you can also double-click the Vitis Unified IDE application icon to launch it.

---

## Welcome Screen Options

On first launch the IDE opens to the **Welcome Screen**. The relevant HLS Development section provides:

| Option | Description |
|---|---|
| **Create Component** | Opens the Create HLS Component wizard to start a new HLS component |
| **Create Component from Library** | Creates a new component from AMD-provided library functions |
| **Tutorials** | Opens a browser pointing to the Vitis-HLS-Introductory-Examples on GitHub |
| **User Guide** | Opens UG1399 in a web browser |

The **Online Resources** block provides links to additional documentation and tutorials.

Previously opened workspaces appear under **Recent Workspaces** for quick access.

---

## Features of the Vitis Unified IDE

The Vitis Unified IDE window is organized into five main areas:

| # | Area | Description |
|---|---|---|
| 1 | **Tool Bar** (left) | Quick access to: Vitis Component Explorer, Search, Source Control, Debug view, Examples, and Analysis view |
| 2 | **Vitis Component Explorer** | Virtual hierarchy of the workspace — shows Sources and Outputs folders (logical view, not necessarily the on-disk layout) |
| 3 | **Central Editor** | Main editing area for components, configuration files, and source files |
| 4 | **Flow Navigator** | Process flow representation for the active HLS component; shows all build steps and associated reports |
| 5 | **Console/Terminal area** | Displays build transcripts; also hosts the Terminal window and the Pipeline view |
| 6 | **Index** | History of all build step transcripts for the session — allows reopening a closed transcript |

---

## Using the Flow Navigator

The Flow Navigator presents the HLS design flow as an ordered sequence of interactive steps. Each step can be launched, canceled, and linked to its output reports from within the navigator.

### Flow Steps for an HLS Component

| Step | IDE Label | Description |
|---|---|---|
| 1 | **C SIMULATION** | Runs C Simulation and the Code Analyzer on the source code and test bench |
| 2 | **C SYNTHESIS** | Opens the C Synthesis dialog and lists synthesis reports after completion |
| 3 | **C/RTL CO-SIMULATION** | Opens the Co-Simulation dialog and lists cosim reports after completion |
| 4 | **PACKAGE** | Generates the Vivado IP (`.zip`) or Vitis Kernel (`.xo`) from the synthesized RTL |
| 5 | **IMPLEMENTATION** | Runs Vivado synthesis and implementation for detailed utilization and timing reports |

### Navigator Controls

| Control | Description |
|---|---|
| **Open Settings** (⚙ icon) | Next to **Component**: opens `vitis-comp.json`. Next to a step: opens the Config File Editor |
| **Cancel Run** | Hidden by default; appears on hover over a running step |
| **Warning sign** (⚠ icon) | Indicates a step needs to be re-run (source changed, dependency incomplete). Hover for details |

---

## Quick Reference

```bash
# Environment setup
source <Vitis_Installation_Directory>/settings64.sh

# Launch IDE with a workspace
vitis -w /path/to/my_workspace

# Flow Navigator step order
# 1. C SIMULATION
# 2. C SYNTHESIS
# 3. C/RTL CO-SIMULATION
# 4. PACKAGE
# 5. IMPLEMENTATION
```

| Resource | Reference |
|---|---|
| Installation guide | UG1701 — Embedded Design Development Using Vitis |
| This document | UG1399 — Vitis HLS User Guide v2025.2 |

---

## Best Practices

| Practice | Rationale |
|---|---|
| **Always source `settings64.sh` before launching** | Environment variables and PATH must be set for `vitis` and all downstream tools |
| **Use workspaces to organize projects** | Each workspace can contain multiple HLS components; keeps builds isolated |
| **Follow Flow Navigator step order (Sim → Synth → CoSim → Package → Impl)** | Each step depends on outputs of the previous; skipping steps leads to stale results |
| **Re-run steps when the ⚠ warning icon appears** | Source changes invalidate downstream results; the IDE tracks dependencies automatically |
| **Use the Console/Terminal area to diagnose build failures** | Build transcripts contain detailed error messages from `v++` and `vitis-run` |

---

### See Also

- [Chapter 13 — Building and Running an HLS Component](ch13_building_hls_component.md) — Detailed steps for each Flow Navigator stage
- [Chapter 14 — HLS Command Line](ch14_hls_command_line.md) — Command-line equivalents of all IDE operations
- [Chapter 15 — Vitis Commands](../section04_vitis_hls_command_reference/ch15_vitis_commands.md) — `vitis`, `v++`, `vitis-run` reference

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 12: Launching the Vitis Unified IDE, Pages 331–335.*
