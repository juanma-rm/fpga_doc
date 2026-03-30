# Chapter 1: Vivado System-Level Design Flows

## Overview

This chapter provides an overview of working with the AMD Vivado Design Suite to create designs for AMD devices. It covers the various design flows, use models, and tool options available — from RTL-to-bitstream flows to alternate design methodologies including HLS, embedded processor, model-based, and dynamic function exchange (DFX) flows.

---

## Table of Contents

| Section | Description |
|---|---|
| [Navigating Content by Design Process](#navigating-content-by-design-process) | How AMD documentation is organized by design task |
| [Industry Standards-Based Design](#industry-standards-based-design) | Supported industry standards (Tcl, AXI4, SDC, Verilog, VHDL, etc.) |
| [Design Flows](#design-flows) | High-level design flow for FPGAs, SoCs, and Versal devices |
| [RTL-to-Bitstream Design Flow](#rtl-to-bitstream-design-flow) | Core design flow from RTL through implementation |
| [Alternate RTL-to-Bitstream Design Flows](#alternate-rtl-to-bitstream-design-flows) | Accelerated kernels, embedded, HLS, DFX, and hierarchical flows |

---

## Navigating Content by Design Process

AMD documentation is organized around standard design processes accessible via the **Design Hubs** page and the **Design Flow Assistant**. The relevant processes for this document are:

| Design Process | Topics in This Document |
|---|---|
| **System and Solution Planning** | Design Flows, RTL-to-Bitstream Design Flow, Alternate RTL-to-Bitstream Design Flows |
| **Hardware, IP, and Platform Development** | Accelerated Kernel Flows |
| **System Integration and Validation** | Running Logic Simulation, Logic Simulation |
| **Board System Design** | AMD Platform Board Support, Board Files |

---

## Industry Standards-Based Design

The Vivado Design Suite supports the following established industry standards:

| Standard | Usage |
|---|---|
| **Tcl** | Native scripting and command interface |
| **AXI4, IP-XACT** | IP interconnect and packaging protocols |
| **SDC** | Synopsys Design Constraints for timing |
| **XDC** | Xilinx Design Constraints (SDC superset) |
| **Verilog, VHDL, VHDL-2008, SystemVerilog** | RTL design entry and synthesis |
| **SystemC, C, C++** | High-Level Synthesis (HLS) design entry |

> The Vivado Design Suite is natively Tcl-based with SDC and XDC constraint support. The AXI4 and IP-XACT standards enable faster system-level integration and broader EDA ecosystem support.

---

## Design Flows

### FPGA and SoC Design Flow

The high-level system-level design flow covers the following major stages:

1. **System Design Entry** — RTL development, IP configuration, embedded processor design, C-based (HLS) design, or model-based design
2. **IP Integrator** — Configure IP subsystems using the IP Packager and IP Integrator
3. **Assign Constraints** — Define logical and physical constraints
4. **Logic Synthesis** — Synthesize the design
5. **Implementation** — Optimize, place, and route
6. **Timing Closure and Design Analysis** — Verify timing and performance
7. **Generate Bitstream / Programming / Debug** — Create bitstream and program the device

> ⚠️ For **Spartan UltraScale+** devices, `bootgen` must be run after bitstream generation to create the PDI required for device programming. See the *Bootgen User Guide (UG1283)*.

### Versal Device Design Flows

The Versal design flow varies based on design type:

| Design Type | Flow |
|---|---|
| **Hardware-only system** | Traditional flow → Hardware Debug |
| **Embedded system** | Traditional flow → Export Hardware → Vitis software stack |
| **Embedded + PL accelerators** | Traditional flow → Export Hardware → Vitis platform + PL accelerators |
| **Embedded + AI Engine** | Traditional flow → Export Hardware → Vitis platform + PL + AI Engine accelerators |

**Traditional Design Flow for Versal:**
1. Design Entry (RTL, Block Diagrams, IP, Netlists) + Basic Design Constraints
2. Simulation and Verification
3. Synthesis + Complete Design Constraints
4. Implementation (Logic/Physical Optimization, Place, Route)
5. PDI Generation
6. Hardware Design Completion → Export Hardware or Hardware Debug

**Platform-Based Design Flow (Vitis):**
- AI Engine Graph Development & Verification
- PL Kernel Development & Verification
- Embedded Software Application Development
- System Integration → Simulation → Implementation → Hardware Validation

---

## RTL-to-Bitstream Design Flow

### RTL Design

You can specify RTL source files to create a project and use them for code development, analysis, synthesis, and implementation. The Vivado Design Suite provides:

- Library of recommended **RTL and constraint templates**
- Support for **Verilog, VHDL, SystemVerilog, and XDC** source files
- Integration with the *UltraFast Design Methodology Guide (UG949)* for optimal coding techniques

### IP Design and System-Level Integration

The Vivado IP environment supports:

- **IP Catalog** — Quick access to configure, instantiate, and validate IP
- **Custom IP packaging** — Using IP-XACT protocol
- **AXI4 interconnect** — Standard interface for system-level integration
- Support for IP in **RTL or netlist format**

> See *Vivado Design Suite User Guide: Designing with IP (UG896)*.

### IP Subsystem Design

The **Vivado IP Integrator** enables stitching multiple IP together using the **AMBA AXI4** interconnect protocol:

- Block design style interface with DRC-correct connections
- Connection automation and design rule checks
- Block designs are validated, packaged, and treated as a single design source
- Main interface for **embedded design** and **evaluation board** integration

> See *Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)*.

### I/O and Clock Planning

The Vivado IDE pin planning environment provides:

- I/O port assignment to device package pins or internal die pads
- Memory interface assignment to specific I/O banks
- I/O DRC and **simultaneous switching noise (SSN)** analysis

> See *Vivado Design Suite User Guide: I/O and Clock Planning (UG899)*.

### AMD Platform Board Support

When targeting an AMD evaluation board:

- All IP interfaces on the target board are exposed for quick selection
- IP configuration parameters and **physical board constraints** (I/O standard, pin constraints) are automatically assigned
- **Connection automation** enables quick connections to selected IP

### Synthesis

| Feature | Description |
|---|---|
| **Global (top-down) synthesis** | Synthesizes the overall RTL design as one unit |
| **Out-of-context (OOC) synthesis** | Default for IP catalog cores and IP integrator block designs; synthesizes modules independently |
| **OOC module support** | Specific RTL hierarchy modules can be marked for OOC synthesis |
| **Third-party netlist support** | EDIF or structural Verilog supported |
| **Synthesis cache** | Preserves OOC results for reuse across designs |

> ⚠️ **IP cores from the Vivado IP catalog must be synthesized using Vivado synthesis** — third-party synthesis is not supported (with limited exceptions for 7 series memory IP).

> ⚠️ The ISE Netlist format (NGC) is supported for 7 series devices only. It is **not supported** for UltraScale and later devices.

**Tip for Versal users using global mode:**
```tcl
open_run synth_1
write_checkpoint synth.dcp
```

### Design Analysis and Simulation

Design analysis is available at each stage of the flow:

- **DRC and methodology checks**
- **Logic simulation** (behavioral and structural, mixed Verilog/VHDL)
- **Timing and power analysis**
- Third-party simulator integration (Mentor, Cadence, Synopsys, Aldec)

> See *Vivado Design Suite User Guide: Design Analysis and Closure Techniques (UG906)*.

### Placement and Routing

Vivado implementation provides optimization, placement, and routing to satisfy logical, physical, and timing constraints. Advanced features include:

- **Floorplanning** to constrain logic to specific areas
- **Manual placement** and fixing of design elements
- Iterative implementation for challenging designs

### Hardware Debug and Validation

Post-implementation capabilities:

- **Vivado logic analyzer** and standalone **Vivado Lab Edition**
- Debug signal identification in RTL or post-synthesis
- Debug cores added via RTL, synthesized netlist, or **ECO flow**
- Modify debug probe nets or route internal signals to package pins

> See *Vivado Design Suite User Guide: Programming and Debugging (UG908)*.

---

## Alternate RTL-to-Bitstream Design Flows

### Accelerated Kernel Flows

The **AMD Vitis unified software platform** introduces acceleration use cases:

- Vivado creates a **platform** consumed by the Vitis software platform
- Vitis adds **accelerated kernels** to the platform
- The final bitstream is created by **Vitis** (not Vivado) because the complete design is not visible in Vivado

> See *Vitis Unified Software Platform Documentation: Application Acceleration Development (UG1393)*.

### Embedded Processor Design

Creating embedded processor designs uses the **Vivado IP Integrator**:

1. Instantiate, configure, and assemble the processor core and interfaces in IP Integrator
2. Compile through implementation
3. **Export hardware to AMD Vitis** for software development and validation
4. Simulate and debug across hardware/software domains

Supported processors: **Zynq UltraScale+ MPSoC**, **Zynq 7000 SoC**, **MicroBlaze**

**Key resources:**
- *MicroBlaze Processor Embedded Design User Guide (UG1579)*
- *Vivado Design Suite Tutorial: Embedded Processor Hardware Design (UG940)*
- *UltraFast Embedded Design Methodology Guide (UG1046)*

### Model-Based Design Using Model Composer

**Model Composer** enables rapid design exploration within MATLAB and Simulink:

- Model-based graphical design tool
- Automatic code generation for AMD devices
- See *Vitis Model Composer User Guide (UG1483)*

### Model-Based DSP Design Using Vitis Model Composer

The Vitis Model Composer tool (installed with Vivado) supports DSP function implementation:

1. Create DSP functions in Vitis Model Composer
2. Package as an IP module for the Vivado IP catalog
3. Instantiate the generated IP into your Vivado design

### High-Level Synthesis (HLS) C-Based Design

HLS tools enable design using **C, C++, and SystemC**:

- Abstract algorithmic descriptions and data type specifications
- Create "what-if" scenarios to optimize performance and area
- Simulate generated RTL using C-based test benches
- **C-to-RTL synthesis** transforms C-based designs into RTL modules
- Modules can be packaged for RTL designs or IP Integrator block designs

**Key resources:**
- *Vivado Design Suite User Guide: High-Level Synthesis (UG902)*
- *Vivado Design Suite Tutorial: High-Level Synthesis (UG871)*

### Dynamic Function Exchange (DFX)

DFX allows **real-time reconfiguration** of portions of a running AMD device with partial bitstreams:

| Requirement | Description |
|---|---|
| Module interface design | Reduce interface signals into reconfigurable modules |
| Floorplanning | Proper device resource allocation |
| Pin placement | Appropriate configuration I/O pin assignment |
| DFX DRCs | Design rule checks specific to DFX |
| Programming method | Proper planning for partial bitstream updates |

**Key resources:**
- *Vivado Design Suite User Guide: Dynamic Function eXchange (UG909)*
- *Vivado Design Suite Tutorial: Dynamic Function eXchange (UG947)*

### Hierarchical Design (HD)

Hierarchical Design flows enable partitioning a design into smaller modules processed independently:

- **Out-of-context (OOC) synthesis** of individual modules
- Module-level constraints for optimization and validation
- Module design checkpoints (DCPs) applied during top-level implementation
- Supports **team design** methodology
- Reduces top-level synthesis runtime and eliminates re-synthesis of completed modules

---

## Best Practices

1. **Choose the right flow** — Use RTL-to-bitstream for standard FPGA designs; use platform-based flows for Versal embedded or acceleration designs
2. **Use OOC synthesis** — Default for IP and block designs; reduces compile time and preserves results
3. **Leverage IP standards** — Use AXI4 and IP-XACT for faster system-level integration
4. **Use IP Integrator for embedded designs** — Provides rules-based connectivity and design assistance
5. **Validate early and often** — Run DRCs, simulation, and timing analysis at each stage
6. **Use HLS for algorithmic design** — Abstract C/C++ enables rapid design exploration
7. **Plan DFX carefully** — Strict design process required for floorplanning, interfaces, and configuration
8. **Use Vivado Lab Edition** — For standalone hardware debug and programming

---

## Quick Reference

| Flow | Entry Point | Output | Key Tool |
|---|---|---|---|
| RTL-to-Bitstream | Verilog/VHDL/SV | Bitstream | Vivado IDE |
| IP-Centric | IP Catalog / IP Integrator | Bitstream | Vivado IDE |
| Accelerated Kernel | Vivado Platform | Bitstream | Vitis |
| Embedded Processor | IP Integrator | XSA → Vitis | Vivado + Vitis |
| HLS | C/C++/SystemC | RTL IP | Vivado HLS |
| Model-Based | MATLAB/Simulink | RTL IP | Model Composer |
| DFX | RTL + Floorplan | Partial Bitstream | Vivado IDE |
| Hierarchical | Modular RTL | Module DCPs | Vivado IDE |

---

## Source Attribution

- **Source:** *Vivado Design Suite User Guide: Design Flows Overview (UG892)*, v2025.2, November 20, 2025
- **Chapter:** Chapter 1 — Vivado System-Level Design Flows (Pages 4–15)
- **Publisher:** Advanced Micro Devices, Inc.
