# Appendix B — Additional Resources and Legal Notices

Documentation access, reference documents, and complete revision history for UG1414 Vitis AI User Guide.

---

## Table of Contents

- [Finding Additional Documentation](#finding-additional-documentation)
- [References](#references)
- [Revision History](#revision-history)

---

## Finding Additional Documentation

### Documentation Portal

The AMD Adaptive Computing Documentation Portal provides search and navigation for all documentation via web browser:
- **URL:** [https://docs.xilinx.com](https://docs.xilinx.com)

### Documentation Navigator (DocNav)

Installed tool providing access to documents, videos, and support resources:

| Launch Method | Command |
|--------------|---------|
| Vivado IDE | Help → Documentation and Tutorials |
| Windows | Start → Xilinx Design Tools → DocNav |
| Linux | `docnav` |

> See **Documentation Navigator User Guide (UG968)** for details.

### Design Hubs

Links to documentation organized by design tasks and topics:
- In DocNav: click **Design Hubs View** tab
- Web: AMD Design Hubs page

### Support Resources

Answers, Documentation, Downloads, and Forums available at AMD Support.

---

## References

| # | Document | ID |
|---|----------|-----|
| 1 | Release Notes and Known Issues | [Online](https://xilinx.github.io/Vitis-AI/3.5/html/docs/reference/release_notes.html) |
| 2 | Vitis AI Library User Guide | UG1354 |
| 3 | DPUCZDX8G for Zynq UltraScale+ MPSoCs Product Guide | PG338 |
| 4 | DPUCAHX8H for Convolutional Neural Networks Product Guide | PG367 |
| 5 | DPUCVDX8G for Versal Adaptive SoCs Product Guide | PG389 |
| 6 | DPUCV2DX8G for Versal Adaptive SoCs Product Guide | PG425 |
| 7 | Vitis Unified Software Platform: Embedded Software Development | UG1400 |
| 8 | Vitis Unified Software Platform: Application Acceleration Development | UG1393 |
| 9 | PetaLinux Tools Documentation: Reference Guide | UG1144 |

---

## Revision History

| Date | Version | Section | Changes |
|------|---------|---------|---------|
| 09/28/2023 | 3.5 | N/A | Editorial updates only |
| 06/29/2023 | 3.5 | Ch 2: Optimizing the Model | Added chapter |
| | | Ch 3: Quantizing the Model | Added Quantization Strategy Configuration, New Data Format, Inference of Quantized Model, `export_onnx_model`, ONNX Runtime Version (vai_q_onnx) |
| | | Ch 5: Deploying and Running | Added Visualization With OnBoard, WeGO-Torch C++ Classes/APIs, updated VOE programming |
| 02/24/2023 | 3.0 | General | Updated links |
| 01/12/2023 | 3.0 | General | Technical updates for new release |
| 06/15/2022 | 2.5 | General | Technical updates for new release |
| 01/20/2022 | 2.0 | General | Updated minor technical details, supported card versions |
| | | DPU | Updated to include Versal DPUs |
| | | Supported Operators | Updated supported operators table |
| | | vaitrace Usage | Updated CLI usage text |
| 12/13/2021 | 1.4.1 | Ch 3: Quantizing the Model | Updated vai_q_tensorflow2 Supported Operations and APIs |
| 07/22/2021 | 1.4 | Ch 1: Overview | Added Versal AI Core Series: DPUCVDX8G |
| | | vai_q_tensorflow2 | Added QAT, Custom Layers, Usage sections |
| | | vai_q_pytorch | Updated QAT |
| | | Ch 5: Deploying | Updated Apache TVM, ONNX Runtime, TF Lite |
| | | Ch 6: Profiling | Added Text Summary, updated vaitrace usage |
| 12/17/2020 | 1.3 | DPU | Added Alveo U200/U250: DPUCADF8H and Versal: DPUCVDX8G |
| | | vai_q_tensorflow2 | Added new section |
| | | vai_q_pytorch | Added Module Partial Quantization, Fast fine-tuning, QAT |
| | | Ch 4: Compiling | Added XIR-based Toolchain section |
| | | VART | Added VART APIs section |
| 07/07/2020 | 1.2 | Entire document | Added Vitis AI Profiler, unified API introduction, DPU Naming topic |
| 03/23/2020 | 1.1 | DPUCAHX8H | Added new topic; Alveo U50 support |

---

## See Also

- [Chapter 1 — Vitis AI Overview](chapter01_vitis_ai_overview.md) — System requirements and installation
- [Chapter 5 — Deploying and Running](chapter05_deploying_and_running_the_model.md) — VART APIs and deployment
- [Chapter 6 — Profiling](chapter06_profiling_the_model.md) — vaitrace and Vitis Analyzer

---

## Source Attribution

- **Document:** UG1414 (v3.5) — Vitis AI User Guide
- **Date:** September 28, 2023
- **Appendix:** Appendix B — Additional Resources and Legal Notices (pp. 244–248)
