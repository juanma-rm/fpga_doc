# fpga_doc

LLM-generated markdown summaries of FPGA documentation (e.g. AMD/Xilinx v2025.2). The summaries are comprehensive, internally-consistent, cross-linked markdown documentation extracted from official PDFs with structured item-level documentation, examples, and best practices for each chapter.

These summaries provide a structured, easily navigable, LLM-friendly format for rapid lookup, technical review, and seamless integration with language models, eliminating the need to manually search or parse the original PDFs.

---

## General structure

Each documentation folder contains:
- a `toc.md` (original table of contents)
- a `README.md` (navigation index)
- structured chapter-by-chapter markdown summaries extracted from the official PDFs.

Tools:
- **[tools/split_pdf_by_chapter.py](tools/split_pdf_by_chapter.py)** — Python script to split PDFs by chapter/section using a Markdown Table of Contents. Usage: `python split_pdf_by_chapter.py <toc_file> [--pdf <pdf_path>] [--output <dir>]`
- **[tools/prompt.md](tools/prompt.md)** — Unified prompt template for generating chapter summaries from PDF sources (previously split to ease the process).

---

## Including new documentation

- Create a new folder for the documentation (e.g. `altera_quartus_prime_pro_edition_user_guide`)
- Add the original PDF and a Markdown Table of Contents (`toc.md`, with section titles and page numbers) to the folder. See existing `toc.md` files for examples.
- Run the `split_pdf_by_chapter.py` script to split the PDF into chapter-level PDFs using the `toc.md` file.
- Use the `prompt.md` template to generate structured markdown summaries for each chapter PDF, following the specified output format and structure.
- Update the `README.md` with a new entry for the documentation, linking to the generated chapter summaries and the original PDF source.
- PDF sources can now be removed to save space (this README.md should link to the original online documentation for reference).

---

## Documentation Index

### [vitis_hls_2025_2/](vitis_hls_2025_2/) — Vitis High-Level Synthesis User Guide (UG1399)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug1399-vitis-hls)

Comprehensive reference for C/C++ high-level synthesis into RTL for AMD FPGAs and SoCs. Key topics:

- **HLS Programmers Guide** — Design principles, parallel programming (dataflow, pipelining, task-level parallelism), loops, arrays, functions, data types, interfaces, M_AXI best practices, optimization techniques
- **Flow Steps** — Launching the Vitis Unified IDE, building/running HLS components, C simulation, C synthesis, C/RTL co-simulation, packaging, implementation
- **Command Reference** — `vitis`/`v++`/`vitis-run` commands, HLS config file commands, HLS pragmas (PIPELINE, UNROLL, DATAFLOW, ARRAY_PARTITION, INTERFACE, etc.), HLS Tcl commands
- **C Driver Reference** — AXI4-Lite slave C driver API
- **Libraries** — Arbitrary precision types, HLS streams, math library, task library, split/merge, stream of blocks, IP libraries, OpenCV integration
- **Migration Guide** — Migrating from Vivado HLS to Vitis HLS and to the Vitis Unified IDE

---

### [vitis_ai_2025_2/](vitis_ai_2025_2/) — Vitis AI User Guide (UG1414)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug1414-vitis-ai)

End-to-end AI inference development environment for AMD platforms (edge and data center). Key topics:

- **Vitis AI Overview** — Tools suite (Model Zoo, Optimizer, Quantizer, Compiler, Profiler, Library, Runtime), containers, system requirements
- **Optimizing the Model** — Pruning with vai_p_tensorflow and vai_p_pytorch
- **Quantizing the Model** — Post-training quantization and fine-tuning for TensorFlow 1.x/2.x, PyTorch, ONNX Runtime
- **Compiling the Model** — XIR-based compilation, DPU targeting, supported operators
- **Deploying and Running** — VART runtime programming, custom OP workflow, VOE, multi-FPGA, WeGO integration, ZenDNN
- **Profiling the Model** — vaitrace usage, performance analysis GUI

---

### [vitis_embedded_2025_2/](vitis_embedded_2025_2/) — Vitis Unified Software Platform: Embedded Software Development (UG1400)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug1400-vitis-embedded)

Embedded software development using the Vitis Unified IDE for AMD Zynq, Versal, and MicroBlaze. Key topics:

- **Getting Started** — Installation, platform overview, migration from classic to unified IDE
- **Using the Vitis Unified IDE** — IDE views/features, platform management, application development, run/debug/optimize, boot image creation, flash programming, cross-triggering
- **Vitis Python API** — Python-based project management, XSDB debugging commands
- **XSDB Command Usage** — Hardware debugging via XSDB
- **XSCT to Python API Migration** — Command-by-command migration reference
- **GNU Compiler Tools** — MicroBlaze and Arm compiler usage, linker scripts, startup files
- **Embedded Design Tutorials & Drivers/Libraries** — Reference to external tutorials and bare-metal driver documentation

---

### [vitis_reference_guide_2025_2/](vitis_reference_guide_2025_2/) — Vitis Reference Guide (UG1702)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug1702-vitis-accelerated-reference)

Complete reference for the Vitis accelerated design flow commands and IDE. Key topics:

- **Vitis Commands and Utilities** — `v++` compiler/linker/packager options, `emconfigutil`, `kernelinfo`, `launch_emulator`, `platforminfo`, `vitis-run`, `xrt-smi`, `xclbinutil`, `xrt.ini` configuration
- **Using the Vitis Unified IDE** — System project creation, heterogeneous computing, bare-metal systems, migration, debugging, Python shell
- **Managing HLS Components** — Flow navigator, component creation, build, and command-line usage
- **Managing AI Engine Components** — Build, simulate, prototype code generation, single kernel development
- **Integration Project** — Creating integration projects, input combinations
- **Analysis View (Vitis Analyzer)** — Report configuration, trace summaries, AI Engine compilation summaries
- **Additional Information** — Output structure, Python XSDB commands

---

### [vivado_design_flows_2025_2/](vivado_design_flows_2025_2/) — Vivado Design Suite User Guide: Design Flows Overview (UG892)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug892-vivado-design-flows-overview)

Overview of Vivado design flows for FPGAs and SoCs. Key topics:

- **System-Level Design Flows** — RTL-to-bitstream flow, IP design, I/O planning, synthesis, implementation, hardware debug
- **Use Models** — Vivado IDE, Tcl scripting, project mode vs. non-project mode, third-party tool integration
- **Project Mode** — Flow Navigator, design entry, IP management, simulation, synthesis/implementation, reports
- **Non-Project Mode** — Script-based flow, design checkpoints, report generation
- **Source Management** — Revision control recommendations, project source types, build methodologies

---

### [vivado_getting_started_2025_2/](vivado_getting_started_2025_2/) — Vivado Design Suite User Guide: Getting Started (UG910)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug910-vivado-getting-started)

Introduction to the Vivado Design Suite for new users. Key topics:

- **Vivado Design Suite Overview** — What is Vivado, IDE introduction, Tcl interface
- **Getting Started** — Installation, launching (IDE, Tcl shell, batch scripts), project creation, IP management, Hardware Manager
- **Learning Resources** — Documentation Navigator, Design Hubs, Quick Help, QuickTake video tutorials, documentation suite
- **UltraFast Design Methodology** — Overview and checklist reference

---

### [vivado_ip_2025_2/](vivado_ip_2025_2/) — Vivado Design Suite User Guide: Designing with IP (UG896)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug896-vivado-ip)

Working with intellectual property (IP) in Vivado. Key topics:

- **IP-Centric Design Flow** — IP terminology, IP Packager, IP Integrator, revision control, encryption
- **IP Basics** — Project settings, IP Catalog, customization, instantiation, SystemVerilog support, IP states, constraints, synthesis options, simulation, upgrading, multi-level IP, debug IP, core containers
- **Manage IP Projects** — Standalone IP management flow
- **Non-Project Mode IP** — Scripted IP creation, design checkpoints, output products
- **IP Subsystems** — IP Integrator reference, design validation
- **Appendices** — Tcl console commands, IP versioning, HLS IP, cross-version compatibility

---

### [vivado_ultrafast_design_methodology_2025_2/](vivado_ultrafast_design_methodology_2025_2/) — UltraFast Design Methodology Guide for FPGAs and SoCs (UG949)

> [AMD Online Documentation](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology)

Best practices for FPGA/SoC design with the Vivado Design Suite. Key topics:

- **Introduction** — Methodology overview, checklist usage, DRC methodology, system-level design flow
- **Board and Device Planning** — PCB layout, power/thermal planning, clock resources, I/O planning, SSI devices, HBM, configuration
- **Design Creation with RTL** — Hierarchy definition, IP management, RTL coding guidelines, clocking guidelines, clock domain crossing
- **Design Constraints** — Timing constraints (create_clock, set_input_delay, false paths, multicycle), power/thermal constraints, physical constraints
- **Design Implementation** — Synthesis strategies, implementation options, incremental compile
- **Design Closure** — Timing closure techniques, power closure, DRC closure, configuration and debug