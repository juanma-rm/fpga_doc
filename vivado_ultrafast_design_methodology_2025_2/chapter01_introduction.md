# Chapter 1: Introduction

The UltraFast Design Methodology is a set of AMD best practices to streamline the design process for UltraScale, UltraScale+, 7 series, and older device families. It emphasizes validating the design at each stage, maximizing early-stage impact, and using methodology DRCs.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [About the UltraFast Design Methodology](#about-the-ultrafast-design-methodology) | Resources, checklist, and methodology DRCs |
| [Understanding UltraFast Design Methodology Concepts](#understanding-ultrafast-design-methodology-concepts) | Creating, validating, and closing designs |
| [Using the Vivado Design Suite](#using-the-vivado-design-suite) | Revision control, IP upgrades, design flows |

---

## About the UltraFast Design Methodology

### Key Resources

| Resource | Description |
|----------|-------------|
| **UG949** (this guide) | Design tasks, analysis, reporting features, and best practices |
| **UG1231** | UltraFast Design Methodology Quick Reference Guide — key steps in double-sided card format |
| **UG1292** | Timing Closure Quick Reference Guide — initial checks, baselining, resolving violations |
| **XTP301** | UltraFast Design Methodology Checklist — spreadsheet of common mistakes and decision points |
| **UG1046** | UltraFast Embedded Design Methodology Guide (for embedded designs) |
| **UG1399** | Vitis HLS User Guide — HLS Programmers Guide (for C-based IP in Vivado IP Integrator) |

### Using the UltraFast Design Methodology Checklist

The checklist (XTP301) is available from AMD Documentation Navigator or as a standalone spreadsheet. Each tab:

- Targets a specific role within a design team
- Includes common questions and recommended actions for each design flow step (project planning, board/device planning, IP/submodule design, top-level design closure)
- Provides links to content in UG949 or other AMD documentation

### Using the UltraFast Design Methodology DRCs

The Vivado Design Suite includes methodology-related DRCs via the `report_methodology` Tcl command:

| Design Stage | When to Run |
|-------------|-------------|
| **Elaborated RTL design** | Before synthesis — validate RTL constructs |
| **After synthesis** | Validate netlist and constraints |
| **After implementation** | Validate constraints and timing concerns |

> **Recommended:** Run methodology DRCs at each stage and address **Critical Warnings** and **Warnings** before moving to the next stage.

```tcl
report_methodology
```

---

## Understanding UltraFast Design Methodology Concepts

### Creating and Implementing a Hardware Design

After planning device I/O, PCB layout, and use model, design creation includes:

1. Planning design hierarchy
2. Identifying and customizing IP cores
3. Instantiating RTL modules for special interconnect or missing functionality
4. Creating timing, power, and physical constraints
5. Specifying additional constraints, attributes, and implementation elements

### Key Design Goals

| Goal | Description |
|------|-------------|
| **Functionality** | Correct operation as specified |
| **Frequency** | Meet target clock frequency |
| **Reliability** | Desired degree of operational reliability |
| **Resource/Power Budget** | Fit within silicon resource and power constraints |

### Maximizing Impact Early in the Development Cycle

Early-stage design changes have dramatically higher impact than later-stage changes:

| Stage | Impact on Performance |
|-------|----------------------|
| HLS (C, C++) | **1000×** |
| RTL Synthesis | **10×** |
| Placement and Optimization | **1.2×** |
| Routing | **1.1×** |

> **Key Insight:** If the design does not meet timing goals, revisit the synthesis stage (HDL and constraints) rather than iterating only in implementation.

### Validating at Each Design Stage

1. **Post-Elaboration:** Create optimal RTL constructs with AMD templates; run methodology DRCs
2. **Post-Synthesis:** Perform timing analysis; analyze master clock ↔ generated clock relationships
3. **Pre-Implementation:** Meet timing using correct constraints before proceeding

> **Tip:** Every clock interaction is timed unless explicitly declared as asynchronous or false path.

### RTL Design Methodology for Rapid Convergence

```
Run Synthesis → Review options & HDL code → Define & Refine Constraints
↓
report_clock_networks → create_clock / create_generated_clock
report_clock_interaction → set_clock_groups / set_false_path
check_timing → I/O delays
report_timing_summary → Timing exceptions
↓
Timing Acceptable? → No: Cross-probe critical paths, return to synthesis
                    → Yes: Place & Route
```

Synthesis is considered complete when design goals are met with positive margin or relatively small negative timing margin.

### Taking Advantage of Rapid Validation

| Approach | Purpose |
|----------|---------|
| **I/O bandwidth validation** | Validate I/O in-system before implementing entire design — highlights system architecture revision needs |
| **Baselining** | Simplest set of constraints to identify internal timing challenges — identifies RTL micro-architecture revision needs |

---

## Using the Vivado Design Suite

### Managing Sources with Revision Control

Most design teams use commercially available revision control systems. The Vivado Design Suite supports various use models for managing design and IP data. See Vivado Design Suite User Guide: Design Flows Overview (UG892).

### Upgrading to New Vivado Design Suite Releases

New releases often contain IP updates. Consider carefully:

- Upgrading IP can result in design changes
- Follow specific rules when using IP configured with previous releases
- See Vivado Design Suite User Guide: Designing with IP (UG896)

---

## Best Practices

1. **Use the UltraFast Design Methodology Checklist** (XTP301) at every design stage
2. **Run `report_methodology`** at each stage — address Critical Warnings before proceeding
3. **Maximize early-stage optimization** — RTL and synthesis changes have 10-1000× more impact than implementation changes
4. **Validate at each stage** — don't defer constraint issues to later stages
5. **Baseline the design** with minimal constraints to identify timing challenges early
6. **Validate I/O bandwidth in-system** before implementing the full design
7. **Revisit synthesis (HDL + constraints)** when timing goals are not met, rather than iterating only in implementation

---

## See Also

- [Chapter 2: Board and Device Planning](chapter02_board_and_device_planning.md)
- [Chapter 3: Design Creation with RTL](chapter03_design_creation_with_rtl.md)
- [Chapter 4: Design Constraints](chapter04_design_constraints.md)
- [Chapter 5: Design Implementation](chapter05_design_implementation.md)
- [Chapter 6: Design Closure](chapter06_design_closure.md)
- Vivado Design Suite User Guide: Design Flows Overview (UG892)

---

## Source Attribution

- **Document:** UltraFast Design Methodology Guide for FPGAs and SoCs (UG949)
- **Version:** v2025.2, November 20, 2025
- **Chapter:** 1 — Introduction
- **Pages:** 4–11
