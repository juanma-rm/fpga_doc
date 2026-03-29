# Chapter 6: Managing the Integration Project Component in the Vitis Unified IDE

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 6 (pp. 395–400)

## Overview

The Integration Project Component in the AMD Vitis™ Unified IDE decouples the link and package stages of the build process. It provides a wizard-driven flow for creating Fixed XSA, VMA, or VSS outputs from flexible combinations of XSA/XPFM, AI Engine, PL kernel, and VSS inputs. This chapter describes how to create an integration project and select the appropriate build outputs and input combinations.

---

## Table of Contents

| Section | Description |
|---|---|
| [Creating Integration Projects](#creating-integration-projects) | How to create an integration project in the Vitis Unified IDE |
| [Build Output Types](#build-output-types) | Available build outputs: Fixed XSA, VMA, VSS |
| [Input Selection Wizard](#input-selection-wizard) | How to select inputs for each build output type |
| [Input Combinations](#input-combinations) | Valid input combinations for each build output type |

---

## Creating Integration Projects

To create an integration project in the Vitis Unified IDE:

1. Open the Vitis Unified IDE.
2. Select **File → New Component → Integration Project**.
3. Follow the wizard to specify the project name and location.
4. Select the desired **Build Output** type.
5. Provide the required inputs based on the selected output type.

---

## Build Output Types

The integration project supports the following build output types:

| Build Output | Description |
|---|---|
| **Fixed XSA** | A fixed hardware platform archive for deployment |
| **VMA** | A Vitis Metadata Archive used for further integration |
| **VSS** | A Vitis Subsystem used in system-level integration |

---

## Input Selection Wizard

The wizard guides you through selecting the appropriate inputs based on your desired build output. Each build output type accepts different input combinations.

---

## Input Combinations

### Fixed XSA

| Input 1 | Input 2 | Input 3 | Notes |
|---|---|---|---|
| Extensible XSA / XPFM | PL Kernels (.xo) | — | Standard PL kernel flow |
| Extensible XSA / XPFM | PL Kernels (.xo) | AI Engine (.libadf.a) | Combined PL + AI Engine flow |
| Extensible XSA / XPFM | AI Engine (.libadf.a) | — | AI Engine only flow |

### VMA

| Input 1 | Input 2 | Notes |
|---|---|---|
| Extensible XSA / XPFM | PL Kernels (.xo) | PL kernel integration |
| Extensible XSA / XPFM | PL Kernels (.xo) + AI Engine (.libadf.a) | Combined integration |

### VSS

| Input 1 | Input 2 | Notes |
|---|---|---|
| Fixed XSA | VSS components | Subsystem creation from fixed platform |
| VMA | VSS components | Subsystem creation from VMA |

---

## Best Practices

1. **Choose the right output type** — Use Fixed XSA for direct deployment, VMA for intermediate integration, and VSS for system-level subsystem composition.
2. **Verify input compatibility** — Ensure your input artifacts (XSA, XPFM, .xo, .libadf.a) are built for compatible target devices and platforms.
3. **Use the wizard** — The input selection wizard validates combinations and prevents invalid configurations.

---

## See Also

- [Chapter 3: Using the Vitis Unified IDE](chapter3_using_the_vitis_unified_ide.md) — IDE workflows and system project creation
- [Chapter 4: Managing Vitis HLS Components](chapter4_managing_the_vitis_hls_components_in_the_vitis_unified_ide.md) — HLS component management for generating PL kernels
- [Chapter 5: Managing AI Engine Components](chapter5_managing_the_ai_engine_component_in_the_vitis_unified_ide.md) — AI Engine component management
- [Chapter 2: Vitis Commands and Utilities](chapter2_vitis_commands_and_utilities.md) — `v++ --link` and `v++ --package` command-line equivalents

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 6 (pp. 395–400)*
