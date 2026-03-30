# Chapter 1: IP-Centric Design Flow

The Vivado Design Suite provides an intellectual property (IP) centric design flow that lets you add IP modules to your design from various sources. Central to the environment is an extensible IP catalog containing AMD-delivered Plug-and-Play IP, which can be extended with HLS designs, System Generator modules, third-party IP, and user-packaged IP.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [IP-Centric Design Flow Overview](#ip-centric-design-flow-overview) | Overview of the IP-centric flow and available methods to work with IP |
| [Navigating Content by Design Process](#navigating-content-by-design-process) | How this document maps to AMD standard design processes |
| [IP Terminology](#ip-terminology) | Key terms for IP definitions, customizations, output products, and flows |
| [IP Packager](#ip-packager) | Creating reusable plug-and-play IP modules |
| [IP Integrator](#ip-integrator) | Creating complex subsystem designs on a canvas |
| [Using Revision and Source Control](#using-revision-and-source-control) | Working with version control for IP designs |
| [Using Encryption](#using-encryption) | IP HDL encryption with IEEE Std P1735 |

---

## IP-Centric Design Flow Overview

The IP catalog can be extended by adding:

- **Modules from System Generator for DSP** designs (MATLAB/Simulink algorithms)
- **Vivado High-Level Synthesis (HLS)** designs (C/C++ algorithms)
- **Third-party IP**
- **Designs packaged as IP** using the Vivado IP packager

> **Note:** In some cases, third-party providers offer IP as synthesized EDIF netlists. You can load these files into a Vivado design using the **Add Sources** command.

### Methods to Work with IP

| Method | Description |
|--------|-------------|
| **Managed IP Flow** | Customize IP and generate output products including a synthesized DCP. See [Chapter 3: Using Manage IP Projects](chapter3_using_manage_ip_projects.md) |
| **Project / Non-Project Mode** | Reference the created XCI file — recommended for large projects with contributing team members |
| **IP Catalog from Project** | Access the IP catalog to customize and add IP; store IP locally or externally (recommended for small teams) |
| **RTL on Canvas** | Right-click in IP Integrator canvas to add an RTL module to a design diagram (module references) |
| **Non-Project Script Flow** | Create, customize IP, and generate output products including DCP in a scripted flow |

> ⚠️ **Important:** Always reference IP using the **XCI file**. It is not recommended to read only the IP DCP file. Since Vivado 2017.1, the DCP does not contain constraints or other output products an IP could deliver (ELF, COE files, Tcl scripts).

### See Also

- Vivado Design Suite Tutorial: Designing with IP (UG939)
- Vivado Design Suite User Guide: Design Flows Overview (UG892)
- Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)

---

## Navigating Content by Design Process

| Design Process | Relevant Chapters |
|---------------|-------------------|
| **Hardware, IP, and Platform Development** | [Chapter 2: IP Basics](chapter2_ip_basics.md), [Chapter 3: Using Manage IP Projects](chapter3_using_manage_ip_projects.md) |
| **System Integration and Validation** | [Chapter 2: Working with Debug IP](chapter2_ip_basics.md#working-with-debug-ip) |

---

## IP Terminology

| Term | Definition |
|------|-----------|
| **IP Definition** | The description of the IP-XACT characteristics for IP |
| **IP Customization** | Customizing an IP from an IP definition, resulting in an XCI file storing the user configuration |
| **IP Location** | A directory containing one or more customized IP in the current project |
| **IP Repository** | A unified view of a collection of IP definitions added to the AMD IP catalog |
| **IP Catalog** | Allows exploration of AMD plug-and-play IP and third-party IP-XACT-compliant IP. See [Chapter 2: IP Basics](chapter2_ip_basics.md) |
| **Output Products** | Generated files (HDL, constraints, simulation targets) produced for an IP customization |
| **Global Synthesis** | Synthesizes IP along with the top-level user logic |
| **Out-Of-Context (OOC) Design Flow** | Creates a standalone synthesis run for generated output products, producing a DCP and `_ooc.xdc`. See [Chapter 2: Out-of-Context Flow](chapter2_ip_basics.md#synthesis-options-for-ip) |
| **Hierarchical IP / Subsystem IP** | An IP which is a subsystem built with multiple IP in a hierarchical topology (block design or RTL flow) |
| **Sub-core IP** | An IP used within another IP that is not Hierarchical. Can be from IP catalog, user-defined, third-party, or core libraries |

---

## IP Packager

The Vivado IP packager lets you create **plug-and-play IP** to add to the extensible Vivado IP catalog. It is based on the **IEEE Standard for IP-XACT (IEEE Std 1685)** — Standard Structure for Packaging, Integrating, and Reusing IP within Tool Flows.

### Capabilities

- Turn a Vivado user design into a reusable IP module
- Add packaged IP to the Vivado IP catalog
- Use packaged IP within Project or Non-Project-based design flows

### See Also

- Vivado Design Suite User Guide: Creating and Packaging Custom IP (UG1118)
- Vivado Design Suite Tutorial: Creating, Packaging Custom IP (UG1119)

---

## IP Integrator

The Vivado IP Integrator tool lets you create **complex subsystem designs** by instantiating and interconnecting IP cores and module references from the Vivado IP catalog onto a **design canvas**.

### See Also

- Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)
- [Chapter 5: Using IP Subsystems with IP Integrator](chapter5_using_ip_subsystems_with_ip_integrator.md)

---

## Using Revision and Source Control

The Vivado Design Suite is designed to work with **any revision control system**. For IP designs, there are trade-offs between:

| Consideration | Trade-off |
|--------------|-----------|
| **Run time** | Regenerating output products takes time but keeps repo smaller |
| **Number of managed files** | Checking in output products increases repo size but avoids regeneration |

### See Also

- Vivado Design Suite User Guide: Design Flows Overview (UG892)

---

## Using Encryption

AMD encrypts IP HDL files with the **IEEE Recommended Practice for Encryption and Management of Electronic Design Intellectual Property (IEEE Std P1735)**.

### See Also

- Vivado Design Suite QuickTake Video: Using IP Encryption Tool in Vivado Design Suite
- Vivado Design Suite User Guide: Creating and Packaging Custom IP (UG1118)

---

## Best Practices

1. **Always reference IP using the XCI file** — never reference only the DCP, as it lacks constraints and other required output products since Vivado 2017.1
2. **Use the Managed IP flow** for team environments — generate and preserve DCP output products for consistent results across releases
3. **Store IP externally from the project** for small teams to enable cross-project reuse
4. **Use IP Integrator** for complex subsystem designs — the canvas-based approach simplifies interconnection
5. **Consider revision control trade-offs** — balance regeneration time against repository size when deciding which output products to check in

---

## Quick Reference

| Concept | Key File / Format |
|---------|-------------------|
| IP Customization | XCI file |
| Output Products | HDL, constraints, simulation targets, DCP |
| OOC Constraints | `_ooc.xdc` |
| IP-XACT Standard | IEEE Std 1685 |
| Encryption Standard | IEEE Std P1735 |
| IP Catalog Sources | AMD IP, HLS, System Generator, third-party, user-packaged |

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Chapter:** 1 — IP-Centric Design Flow
- **Pages:** 4–8
