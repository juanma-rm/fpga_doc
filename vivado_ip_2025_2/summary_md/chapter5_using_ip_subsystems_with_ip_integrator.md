# Chapter 5: Using IP Subsystems with IP Integrator

UG896 does not contain a standalone chapter on IP Integrator subsystem design. IP Integrator documentation is covered in a separate dedicated guide. This section serves as a cross-reference pointer.

---

## Referencing the IP Integrator Documentation

The Vivado **IP Integrator** provides a graphical block design environment for creating IP subsystems. UG896 defers all IP Integrator coverage to the dedicated guide:

- **Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)** — primary reference for block design creation, interface connections, address mapping, subsystem validation, and the Platform Board Flow in IP Integrator

IP Integrator concepts that relate to IP management in UG896 include:

- **Subsystem IP** — An IP built with multiple child IP in a hierarchical block design topology. When generating output products, child IP OOC runs are launched in parallel. See [Chapter 2: Understanding Multi-Level IP](chapter2_ip_basics.md#understanding-multi-level-ip).
- **Block Design wrappers** — HDL and System Verilog wrappers can be generated for block designs using `make_wrapper`. See [Chapter 2: Designing with System Verilog](chapter2_ip_basics.md#designing-with-system-verilog).
- **Core Container limitation** — IP inside IP Integrator block designs do not support the Core Container feature. See [Chapter 2: Using a Core Container](chapter2_ip_basics.md#using-a-core-container).
- **`ip_user_files/bd/`** — Support files for each IP Integrator block design are stored under this directory, including HDL simulation top-level files and static simulation files.

---

## See Also

- [Chapter 1: IP Integrator](chapter1_ip-centric_design_flow.md#ip-integrator) — overview of IP Integrator in the IP-centric design flow
- [Chapter 2: IP Basics](chapter2_ip_basics.md) — IP customization and output product generation
- [Chapter 4: Using IP in Non-Project Mode](chapter4_using_ip_in_non-project_mode.md) — Tcl commands for IP operations
- Vivado Design Suite User Guide: Designing IP Subsystems Using IP Integrator (UG994)

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Note:** UG896 does not contain a dedicated IP Integrator chapter. The table of contents references this topic at pages 88–89, but the actual PDF content at those pages belongs to Chapter 6 (Tcl Commands). All IP Integrator documentation is in UG994.
