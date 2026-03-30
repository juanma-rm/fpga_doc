# Appendix A: Additional Resources and Legal Notices

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Appendix A (pp. 485–488)

## Overview

This appendix provides links to supplemental documentation, support resources, and the revision history for the Vitis Accelerated Reference Guide (UG1702).

---

## Finding Additional Documentation

### Technical Information Portal

The AMD Technical Information Portal provides robust search and navigation for documentation using your web browser:
- **URL:** [https://docs.amd.com](https://docs.amd.com)

### Documentation Navigator (DocNav)

DocNav is an installed tool providing access to AMD Adaptive Computing documents, videos, and support resources.

**To open DocNav:**
- From the AMD Vivado™ IDE: **Help → Documentation and Tutorials**
- On Windows: **Start → Xilinx Design Tools → DocNav**
- On Linux: run `docnav` at the command prompt

> **Note:** For more information on DocNav, refer to the *Documentation Navigator User Guide (UG968)*.

### Design Hubs

AMD Design Hubs provide links to documentation organized by design tasks and other topics:
- In DocNav, click the **Design Hubs View** tab
- Visit the **Design Hubs** web page

---

## Support Resources

For support resources such as Answers, Documentation, Downloads, and Forums, visit the AMD Support page.

---

## References

| # | Document | ID |
|---|---|---|
| 1 | Data Center Acceleration using Vitis | UG1700 |
| 2 | Embedded Design Development Using Vitis | UG1701 |
| 3 | Vitis Software Platform Release Notes | UG1742 |
| 4 | Introduction to FPGA Design with Vivado High-Level Synthesis | UG998 |
| 5 | Vitis Unified Software Platform Documentation: Embedded Software Development | UG1400 |
| 6 | Vitis High-Level Synthesis User Guide | UG1399 |
| 7 | AI Engine Tools and Flows User Guide | UG1076 |
| 8 | AI Engine Kernel and Graph Programming Guide | UG1079 |
| 9 | Vivado Design Suite User Guide: Logic Simulation | UG900 |
| 10 | Vivado Design Suite User Guide: Synthesis | UG901 |
| 11 | Vivado Design Suite Properties Reference Guide | UG912 |
| 12 | Vivado Design Suite User Guide: Implementation | UG904 |
| 13 | Vivado Design Suite Tcl Command Reference Guide | UG835 |

---

## Revision History

### Version 2025.2 (November 20, 2025)

| Section | Revision Summary |
|---|---|
| Chapter 6: Managing the Integration Project Component | New topic describing how the Vitis IDE Integration Project decouples link/package and, via a wizard, builds Fixed XSA, VMA, or VSS from flexible mixes of XSA/XPFM, AIE, PL kernels, and VSS |
| General updates | Renamed `xbutil` with `xrt-smi` throughout the document |
| v++ General Options | Added content for `--mode` option |
| v++ Mode VSS | Added new topic |
| v++ Linking and Packaging Options | Added introduction for Vitis Subsystem (VSS) Creation using the V++ Linker |

### Version 2025.1 (July 8, 2025)

| Section | Revision Summary |
|---|---|
| General updates | Editorial and linking revisions |

### Version 2025.1 (May 29, 2025)

| Section | Revision Summary |
|---|---|
| `--package` Options | Removed support for `sw_emu` |
| Event Tracing Options | Updated `num-trace-streams` and `trace-plio-width` |
| `launch_emulator` Utility | Removed support for `sw_emu` |
| Miscellaneous Options | Updated section |
| Open Trace Summary Using Time Window | Updated section and screenshots |
| Output Directories of the `v++` Command | Removed support for `sw_emu` |
| Software Platform Information | Removed support for OpenCL |
| System Project Structure | Removed support for `sw_emu` |
| v++ General Compilation Options | Removed support for `sw_emu` |
| `xclbinutil` Utility | Removed support for `sw_emu` |
| `xrt.ini` File | Removed support for OpenCL |

---

## See Also

- [Chapter 1: Navigating Content by Design Process](chapter01_navigating_content_by_design_process.md) — Design process navigation
- [Chapter 2: Vitis Commands and Utilities](chapter02_vitis_commands_and_utilities.md) — Command-line reference

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Appendix A (pp. 485–488)*
