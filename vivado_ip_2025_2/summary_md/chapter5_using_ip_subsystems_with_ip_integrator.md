# Chapter 5: Using IP Subsystems with IP Integrator

This chapter provides a brief reference to the IP Integrator subsystem design flow.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Referencing the IP Integrator Documentation](#referencing-the-ip-integrator-documentation) | Pointer to UG994 for block design and IP subsystems |
| [Validating the Design](#validating-the-design) | Overview of design validation in IP Integrator |

---

## Referencing the IP Integrator Documentation

The Vivado **IP Integrator** provides a graphical block design environment for creating IP subsystems. Complex subsystem assembly, AXI interconnection, and address mapping are handled through the IP Integrator canvas.

For comprehensive coverage of IP Integrator:

- **Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)** — primary reference for block design creation, interface connections, address mapping, and subsystem validation

> **Note:** IP Integrator is the recommended approach for building complex AXI-based subsystems. It automates interconnect insertion, address assignment, and clock domain crossing.

---

## Validating the Design

IP Integrator includes a built-in **Design Rule Check (DRC)** engine that validates:

- Interface compatibility between connected IP
- Clock domain requirements
- Address space assignments
- Missing connections and unconnected ports

Run **Validate Design** (F6) before generating the block design output products.

---

## See Also

- [Chapter 2: IP Basics](chapter2_ip_basics.md) — fundamental IP customization and output product generation
- [Chapter 4: Using IP in Non-Project Mode](chapter4_using_ip_in_non-project_mode.md) — Tcl commands for IP operations
- Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Chapter:** 5 — Using IP Subsystems with IP Integrator
- **Pages:** 88–89
