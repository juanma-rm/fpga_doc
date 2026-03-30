# Chapter 32 — Working with OpenCV

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Page 871

## Overview

Chapter 32 is a brief pointer to the **Vitis Vision Library** for image processing and computer vision development with Vitis HLS.

Vitis HLS does **not** come with OpenCV pre-installed. Before using any vision functions in HLS, you must separately obtain and install the OpenCV libraries.

---

## Vitis Vision Library

The recommended path for OpenCV-based HLS development is the **Vitis Libraries** Vision component:

- **Repository:** [https://github.com/Xilinx/Vitis_Libraries/tree/main/vision](https://github.com/Xilinx/Vitis_Libraries/tree/main/vision)
- **Content:** HLS-optimized OpenCV-compatible functions targeting Xilinx FPGAs.
- **Requirement:** OpenCV host installation needed for test bench compilation.

### Install Instructions

Follow the guide provided in the Vitis Libraries documentation:

> *Vitis Libraries — Compiling and Installing OpenCV libraries for use with Vision library*

This covers building OpenCV from source with the appropriate flags for HLS test bench compilation and co-simulation.

---

## Key Points

| Item | Detail |
|---|---|
| OpenCV in Vitis HLS | Not bundled — must install separately |
| Recommended source | Vitis Libraries Vision (`github.com/Xilinx/Vitis_Libraries`) |
| Install guide | Vitis Libraries documentation (OpenCV setup section) |
| HLS test bench | Requires OpenCV host libraries for C simulation |
| Hardware functions | Use Vitis Vision Library HLS-ready functions (not standard OpenCV directly) |

---

### See Also

- [Chapter 35 — Deprecated Features](../section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md) — HLS Video Library deprecation notice
- [Appendix C — Resources](../appendices/appendix_c_resources.md) — Vitis Libraries (successor to HLS OpenCV)

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 32, page 871*
