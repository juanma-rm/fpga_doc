# Vitis HLS UG1399 (v2025.2) — Complete Table of Contents

> Consolidated index of all chapters and sections


## Quick Navigation

- [Appendices](#appendices)
- [Section I - Introduction](#section-i--introduction)
- [Section II - Programmers Guide](#section-ii--programmers-guide)
- [Section III - Flow Steps](#section-iii--flow-steps)
- [Section IV - Command Reference](#section-iv--command-reference)
- [Section V - Driver Reference](#section-v--driver-reference)
- [Section VI - Libraries Reference](#section-vi--libraries-reference)
- [Section VII - Migration Guide](#section-vii--migration-guide)

---


## Appendices


### [Appendix A — Tcl to Config File Command Map](Appendices/appendix_a_tcl_config_map.md)

*(No detailed TOC)*


### [Appendix B — Instruction/Operator Explanation](Appendices/appendix_b_operators.md)

*(No detailed TOC)*


### [Appendix C — Additional Resources and Legal Notices](Appendices/appendix_c_resources.md)

- [Finding Additional Documentation](Appendices/appendix_c_resources.md#finding-additional-documentation)
- [Support Resources](Appendices/appendix_c_resources.md#support-resources)
- [References](Appendices/appendix_c_resources.md#references)
- [Revision History Summary](Appendices/appendix_c_resources.md#revision-history-summary)
---


## Section I - Introduction


### [Section I — Introduction to Vitis HLS](Section I - Introduction/section1.md)

1. [What is High-Level Synthesis?](Section I - Introduction/section1.md#1-what-is-high-level-synthesis)
2. [Supported Operating Systems & Licensing](Section I - Introduction/section1.md#2-supported-operating-systems--licensing)
3. [Changed Behavior in v2025.2](Section I - Introduction/section1.md#3-changed-behavior-in-v20252)
4. [Benefits of HLS](Section I - Introduction/section1.md#4-benefits-of-hls)
5. [Introduction to Vitis HLS Components](Section I - Introduction/section1.md#5-introduction-to-vitis-hls-components)
6. [Key Synthesis Concepts](Section I - Introduction/section1.md#6-key-synthesis-concepts)
7. [Refactoring C++ Source Code for HLS](Section I - Introduction/section1.md#7-refactoring-c-source-code-for-hls)
8. [Re-Architecting the Hardware Module](Section I - Introduction/section1.md#8-re-architecting-the-hardware-module)
9. [Best Practices](Section I - Introduction/section1.md#9-best-practices)
10. [Tutorials and Examples](Section I - Introduction/section1.md#10-tutorials-and-examples)
---


## Section II - Programmers Guide


### [Chapter 10: Top-Level Performance Pragma](Section II - Programmers Guide/ch10_performance_pragma.md)

1. [Overview](Section II - Programmers Guide/ch10_performance_pragma.md#1-overview)
2. [Top-Level vs. Loop-Level Performance Pragma](Section II - Programmers Guide/ch10_performance_pragma.md#2-top-level-vs-loop-level-performance-pragma)
3. [Step-by-Step Methodology](Section II - Programmers Guide/ch10_performance_pragma.md#3-step-by-step-methodology)
4. [Pragma Syntax](Section II - Programmers Guide/ch10_performance_pragma.md#4-pragma-syntax)
5. [Optimization Strategy and Priority](Section II - Programmers Guide/ch10_performance_pragma.md#5-optimization-strategy-and-priority)
6. [Limitations and Precedence Rules](Section II - Programmers Guide/ch10_performance_pragma.md#6-limitations-and-precedence-rules)
7. [Unsupported Libraries and Constructs](Section II - Programmers Guide/ch10_performance_pragma.md#7-unsupported-libraries-and-constructs)
8. [Known Issues](Section II - Programmers Guide/ch10_performance_pragma.md#8-known-issues)
9. [Best Practices](Section II - Programmers Guide/ch10_performance_pragma.md#9-best-practices)
---


### [Chapter 11: Optimizing Techniques and Troubleshooting Tips](Section II - Programmers Guide/ch11_optimizing_techniques.md)

1. [Optimization Directives Overview](Section II - Programmers Guide/ch11_optimizing_techniques.md#1-optimization-directives-overview)
2. [HLS Scheduling and Binding](Section II - Programmers Guide/ch11_optimizing_techniques.md#2-hls-scheduling-and-binding)
3. [Optimizing Logic Expressions](Section II - Programmers Guide/ch11_optimizing_techniques.md#3-optimizing-logic-expressions)
- 3.1 [Shift Register Inference](Section II - Programmers Guide/ch11_optimizing_techniques.md#31-shift-register-inference)
- 3.2 [Expression Balancing](Section II - Programmers Guide/ch11_optimizing_techniques.md#32-expression-balancing)
- 3.3 [Floating-Point and Unsafe Math Optimizations](Section II - Programmers Guide/ch11_optimizing_techniques.md#33-floating-point-and-unsafe-math-optimizations)
4. [Optimizing AXI System Performance](Section II - Programmers Guide/ch11_optimizing_techniques.md#4-optimizing-axi-system-performance)
- 4.1 [Burst Transfer Types](Section II - Programmers Guide/ch11_optimizing_techniques.md#41-burst-transfer-types)
- 4.2 [Burst Preconditions and Limitations](Section II - Programmers Guide/ch11_optimizing_techniques.md#42-burst-preconditions-and-limitations)
- 4.3 [AXI Interface Control Options](Section II - Programmers Guide/ch11_optimizing_techniques.md#43-axi-interface-control-options)
- 4.4 [Stencil Optimization](Section II - Programmers Guide/ch11_optimizing_techniques.md#44-stencil-optimization)
- 4.5 [Manual Burst (`hls::burst_maxi`)](Section II - Programmers Guide/ch11_optimizing_techniques.md#45-manual-burst-hlsburst_maxi)
- 4.6 [AXI Performance Case Study Summary](Section II - Programmers Guide/ch11_optimizing_techniques.md#46-axi-performance-case-study-summary)
5. [Managing Area and Hardware Resources](Section II - Programmers Guide/ch11_optimizing_techniques.md#5-managing-area-and-hardware-resources)
- 5.1 [ALLOCATION Directive](Section II - Programmers Guide/ch11_optimizing_techniques.md#51-allocation-directive)
- 5.2 [BIND_OP and BIND_STORAGE Directives](Section II - Programmers Guide/ch11_optimizing_techniques.md#52-bind_op-and-bind_storage-directives)
- 5.3 [DSP Multi-Operation Matching](Section II - Programmers Guide/ch11_optimizing_techniques.md#53-dsp-multi-operation-matching)
6. [Limitations of Control-Driven Task-Level Parallelism (Dataflow)](Section II - Programmers Guide/ch11_optimizing_techniques.md#6-limitations-of-control-driven-task-level-parallelism-dataflow)
7. [Limitations of Pipelining with Static Variables](Section II - Programmers Guide/ch11_optimizing_techniques.md#7-limitations-of-pipelining-with-static-variables)
8. [Canonical Dataflow Coding Style](Section II - Programmers Guide/ch11_optimizing_techniques.md#8-canonical-dataflow-coding-style)
9. [Best Practices](Section II - Programmers Guide/ch11_optimizing_techniques.md#9-best-practices)
---


### [Chapter 1 — Design Principles](Section II - Programmers Guide/ch1_design_principles.md)

1. [Introduction & Motivation](Section II - Programmers Guide/ch1_design_principles.md#1-introduction--motivation)
2. [Throughput and Performance](Section II - Programmers Guide/ch1_design_principles.md#2-throughput-and-performance)
3. [Architecture Matters: CPU vs FPGA](Section II - Programmers Guide/ch1_design_principles.md#3-architecture-matters-cpu-vs-fpga)
4. [Three Paradigms for Programmable Logic](Section II - Programmers Guide/ch1_design_principles.md#4-three-paradigms-for-programmable-logic)
- [Producer-Consumer Paradigm](Section II - Programmers Guide/ch1_design_principles.md#41-producer-consumer-paradigm)
- [Streaming Data Paradigm](Section II - Programmers Guide/ch1_design_principles.md#42-streaming-data-paradigm)
- [Pipelining Paradigm](Section II - Programmers Guide/ch1_design_principles.md#43-pipelining-paradigm)
5. [Combining the Three Paradigms](Section II - Programmers Guide/ch1_design_principles.md#5-combining-the-three-paradigms)
6. [Conclusion — A Prescription for Performance](Section II - Programmers Guide/ch1_design_principles.md#6-conclusion--a-prescription-for-performance)
7. [Best Practices](Section II - Programmers Guide/ch1_design_principles.md#7-best-practices)
---


### [Chapter 2 — Abstract Parallel Programming Model for HLS](Section II - Programmers Guide/ch2_abstract_parallel_programming.md)

1. [The Abstract Parallel Programming Model](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#1-the-abstract-parallel-programming-model)
2. [Channel Semantics: Blocking vs Non-Blocking](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#2-channel-semantics-blocking-vs-non-blocking)
3. [Control-Driven vs Data-Driven TLP](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#3-control-driven-vs-data-driven-tlp)
4. [Data-Driven TLP — `hls::task`](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#4-data-driven-tlp--hlstask)
5. [Control-Driven TLP — Dataflow Pragma](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#5-control-driven-tlp--dataflow-pragma)
6. [Dataflow Region Coding Style (WYSIWYG / Canonical)](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#6-dataflow-region-coding-style-wysiwyg--canonical)
7. [Advanced Dataflow Features](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#7-advanced-dataflow-features)
8. [Configuring Dataflow Memory Channels](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#8-configuring-dataflow-memory-channels)
9. [Stream-of-Blocks (`hls::stream_of_blocks`)](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#9-stream-of-blocks-hlsstream_of_blocks)
10. [Compiler-Created FIFO Types](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#10-compiler-created-fifo-types)
11. [`#pragma HLS stable`](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#11-pragma-hls-stable)
12. [Mixing Data-Driven and Control-Driven Models](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#12-mixing-data-driven-and-control-driven-models)
13. [Summary: Choosing the Right TLP Model](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#13-summary-choosing-the-right-tlp-model)
14. [Best Practices](Section II - Programmers Guide/ch2_abstract_parallel_programming.md#14-best-practices)
---


### [Chapter 3 — Loops Primer](Section II - Programmers Guide/ch3_loops_primer.md)

1. [Why Loops Matter for HLS Performance](Section II - Programmers Guide/ch3_loops_primer.md#1-why-loops-matter-for-hls-performance)
2. [Pipelining Loops](Section II - Programmers Guide/ch3_loops_primer.md#2-pipelining-loops)
3. [Automatic Loop Pipelining](Section II - Programmers Guide/ch3_loops_primer.md#3-automatic-loop-pipelining)
4. [Rewinding Pipelined Loops](Section II - Programmers Guide/ch3_loops_primer.md#4-rewinding-pipelined-loops)
5. [Pipeline Types (STP / FRP / FLP)](Section II - Programmers Guide/ch3_loops_primer.md#5-pipeline-types-stp--frp--flp)
6. [Managing Pipeline Dependencies](Section II - Programmers Guide/ch3_loops_primer.md#6-managing-pipeline-dependencies)
7. [Removing False Dependencies](Section II - Programmers Guide/ch3_loops_primer.md#7-removing-false-dependencies)
8. [Unrolling Loops](Section II - Programmers Guide/ch3_loops_primer.md#8-unrolling-loops)
9. [Merging Loops](Section II - Programmers Guide/ch3_loops_primer.md#9-merging-loops)
10. [Working with Nested Loops](Section II - Programmers Guide/ch3_loops_primer.md#10-working-with-nested-loops)
11. [Working with Variable Loop Bounds](Section II - Programmers Guide/ch3_loops_primer.md#11-working-with-variable-loop-bounds)
12. [Best Practices](Section II - Programmers Guide/ch3_loops_primer.md#12-best-practices)
---


### [Chapter 4 — Arrays Primer](Section II - Programmers Guide/ch4_arrays_primer.md)

1. [Mapping Software Arrays to Hardware Memory](Section II - Programmers Guide/ch4_arrays_primer.md#1-mapping-software-arrays-to-hardware-memory)
2. [Array Accesses and Performance](Section II - Programmers Guide/ch4_arrays_primer.md#2-array-accesses-and-performance)
3. [Array Partitioning](Section II - Programmers Guide/ch4_arrays_primer.md#3-array-partitioning)
4. [Array Reshaping](Section II - Programmers Guide/ch4_arrays_primer.md#4-array-reshaping)
5. [Arrays on the Interface](Section II - Programmers Guide/ch4_arrays_primer.md#5-arrays-on-the-interface)
6. [Initializing and Resetting Arrays](Section II - Programmers Guide/ch4_arrays_primer.md#6-initializing-and-resetting-arrays)
7. [Implementing ROMs](Section II - Programmers Guide/ch4_arrays_primer.md#7-implementing-roms)
8. [C Simulation with Large Arrays](Section II - Programmers Guide/ch4_arrays_primer.md#8-c-simulation-with-large-arrays)
9. [Best Practices](Section II - Programmers Guide/ch4_arrays_primer.md#9-best-practices)
---


### [Chapter 5 — Functions Primer](Section II - Programmers Guide/ch5_functions_primer.md)

1. [Top-Level Function and Hierarchy](Section II - Programmers Guide/ch5_functions_primer.md#1-top-level-function-and-hierarchy)
2. [Function Inlining](Section II - Programmers Guide/ch5_functions_primer.md#2-function-inlining)
3. [Function Pipelining](Section II - Programmers Guide/ch5_functions_primer.md#3-function-pipelining)
4. [Function Instantiation](Section II - Programmers Guide/ch5_functions_primer.md#4-function-instantiation)
5. [Best Practices](Section II - Programmers Guide/ch5_functions_primer.md#5-best-practices)
---


### [Chapter 6 — Data Types](Section II - Programmers Guide/ch6_data_types.md)

1. [Standard C/C++ Types](Section II - Programmers Guide/ch6_data_types.md#1-standard-cc-types)
2. [Floats and Doubles](Section II - Programmers Guide/ch6_data_types.md#2-floats-and-doubles)
3. [Composite Data Types](Section II - Programmers Guide/ch6_data_types.md#3-composite-data-types)
4. [Type Qualifiers](Section II - Programmers Guide/ch6_data_types.md#4-type-qualifiers)
5. [Arbitrary Precision Integer Types (`ap_int`)](Section II - Programmers Guide/ch6_data_types.md#5-arbitrary-precision-integer-types-ap_int)
6. [Arbitrary Precision Fixed-Point Types (`ap_fixed`)](Section II - Programmers Guide/ch6_data_types.md#6-arbitrary-precision-fixed-point-types-ap_fixed)
7. [Arbitrary Precision Floating-Point Library (`ap_float`)](Section II - Programmers Guide/ch6_data_types.md#7-arbitrary-precision-floating-point-library-ap_float)
8. [Global Variables](Section II - Programmers Guide/ch6_data_types.md#8-global-variables)
9. [Pointers](Section II - Programmers Guide/ch6_data_types.md#9-pointers)
10. [Best Practices](Section II - Programmers Guide/ch6_data_types.md#10-best-practices)
---


### [Chapter 7 — Unsupported C/C++ Constructs](Section II - Programmers Guide/ch7_unsupported_constructs.md)

1. [Synthesis Requirements](Section II - Programmers Guide/ch7_unsupported_constructs.md#1-synthesis-requirements)
2. [System Calls](Section II - Programmers Guide/ch7_unsupported_constructs.md#2-system-calls)
3. [Dynamic Memory Allocation](Section II - Programmers Guide/ch7_unsupported_constructs.md#3-dynamic-memory-allocation)
4. [Pointer Limitations](Section II - Programmers Guide/ch7_unsupported_constructs.md#4-pointer-limitations)
5. [Recursive Functions](Section II - Programmers Guide/ch7_unsupported_constructs.md#5-recursive-functions)
6. [Standard Template Libraries (STL)](Section II - Programmers Guide/ch7_unsupported_constructs.md#6-standard-template-libraries-stl)
7. [Undefined Behaviors](Section II - Programmers Guide/ch7_unsupported_constructs.md#7-undefined-behaviors)
8. [Virtual Functions](Section II - Programmers Guide/ch7_unsupported_constructs.md#8-virtual-functions)
9. [Quick Reference Table](Section II - Programmers Guide/ch7_unsupported_constructs.md#9-quick-reference-table)
---


### [Chapter 8: Interfaces of the HLS Design](Section II - Programmers Guide/ch8_interfaces.md)

1. [Interface Synthesis Overview](Section II - Programmers Guide/ch8_interfaces.md#1-interface-synthesis-overview)
2. [Vitis Kernel Flow Defaults](Section II - Programmers Guide/ch8_interfaces.md#2-vitis-kernel-flow-defaults)
3. [Vivado IP Flow Defaults](Section II - Programmers Guide/ch8_interfaces.md#3-vivado-ip-flow-defaults)
4. [M_AXI Interface](Section II - Programmers Guide/ch8_interfaces.md#4-m_axi-interface)
- 4.1 [Core Concepts and Signals](Section II - Programmers Guide/ch8_interfaces.md#41-core-concepts-and-signals)
- 4.2 [Burst Inference Rules](Section II - Programmers Guide/ch8_interfaces.md#42-burst-inference-rules)
- 4.3 [Offset Modes](Section II - Programmers Guide/ch8_interfaces.md#43-offset-modes)
- 4.4 [Auto Port Width Resizing](Section II - Programmers Guide/ch8_interfaces.md#44-auto-port-width-resizing)
- 4.5 [M_AXI Bundles](Section II - Programmers Guide/ch8_interfaces.md#45-m_axi-bundles)
- 4.6 [FIFO Sizing](Section II - Programmers Guide/ch8_interfaces.md#46-fifo-sizing)
- 4.7 [Interface Pragma Reference](Section II - Programmers Guide/ch8_interfaces.md#47-interface-pragma-reference)
5. [S_AXILITE Interface](Section II - Programmers Guide/ch8_interfaces.md#5-s_axilite-interface)
- 5.1 [Control Register Map](Section II - Programmers Guide/ch8_interfaces.md#51-control-register-map)
- 5.2 [Port-Level Protocols](Section II - Programmers Guide/ch8_interfaces.md#52-port-level-protocols)
- 5.3 [Bundle Rules: Vitis vs. Vivado](Section II - Programmers Guide/ch8_interfaces.md#53-bundle-rules-vitis-vs-vivado)
6. [AXI4-Stream (AXIS) Interface](Section II - Programmers Guide/ch8_interfaces.md#6-axi4-stream-axis-interface)
- 6.1 [Protocol and Data Types](Section II - Programmers Guide/ch8_interfaces.md#61-protocol-and-data-types)
- 6.2 [Side-Channel Signals](Section II - Programmers Guide/ch8_interfaces.md#62-side-channel-signals)
- 6.3 [Register Modes](Section II - Programmers Guide/ch8_interfaces.md#63-register-modes)
- 6.4 [Coding Patterns](Section II - Programmers Guide/ch8_interfaces.md#64-coding-patterns)
7. [Aggregation and Disaggregation of Structs](Section II - Programmers Guide/ch8_interfaces.md#7-aggregation-and-disaggregation-of-structs)
8. [Block-Level Control Protocols](Section II - Programmers Guide/ch8_interfaces.md#8-block-level-control-protocols)
9. [Execution Modes](Section II - Programmers Guide/ch8_interfaces.md#9-execution-modes)
- 9.1 [Auto-Restart](Section II - Programmers Guide/ch8_interfaces.md#91-auto-restart)
- 9.2 [Mailbox](Section II - Programmers Guide/ch8_interfaces.md#92-mailbox)
10. [Vivado IP Port-Level Protocols](Section II - Programmers Guide/ch8_interfaces.md#10-vivado-ip-port-level-protocols)
11. [Initialization and Reset Behavior](Section II - Programmers Guide/ch8_interfaces.md#11-initialization-and-reset-behavior)
12. [Best Practices](Section II - Programmers Guide/ch8_interfaces.md#12-best-practices)
---


### [Chapter 9: Best Practices for Designing with M_AXI Interfaces](Section II - Programmers Guide/ch9_maxi_best_practices.md)

1. [Overview and Goals](Section II - Programmers Guide/ch9_maxi_best_practices.md#1-overview-and-goals)
2. [Load–Compute–Store (LCS) Pattern](Section II - Programmers Guide/ch9_maxi_best_practices.md#2-loadcomputestore-lcs-pattern)
3. [Hardware Data Flow Mindset](Section II - Programmers Guide/ch9_maxi_best_practices.md#3-hardware-data-flow-mindset)
4. [Global Memory Access Strategy](Section II - Programmers Guide/ch9_maxi_best_practices.md#4-global-memory-access-strategy)
5. [Port Width Maximization](Section II - Programmers Guide/ch9_maxi_best_practices.md#5-port-width-maximization)
6. [Memory Resource Selection](Section II - Programmers Guide/ch9_maxi_best_practices.md#6-memory-resource-selection)
7. [Concurrent Port Configuration](Section II - Programmers Guide/ch9_maxi_best_practices.md#7-concurrent-port-configuration)
8. [Burst Length Configuration](Section II - Programmers Guide/ch9_maxi_best_practices.md#8-burst-length-configuration)
9. [Outstanding Requests Configuration](Section II - Programmers Guide/ch9_maxi_best_practices.md#9-outstanding-requests-configuration)
10. [Best Practices Summary](Section II - Programmers Guide/ch9_maxi_best_practices.md#10-best-practices-summary)
---


## Section III - Flow Steps


### [Chapter 12: Launching the Vitis Unified IDE](Section III - Flow Steps/ch12_launching_vitis_ide.md)

1. [Overview](Section III - Flow Steps/ch12_launching_vitis_ide.md#overview)
2. [Launching the IDE](Section III - Flow Steps/ch12_launching_vitis_ide.md#launching-the-ide)
3. [Welcome Screen Options](Section III - Flow Steps/ch12_launching_vitis_ide.md#welcome-screen-options)
4. [Features of the Vitis Unified IDE](Section III - Flow Steps/ch12_launching_vitis_ide.md#features-of-the-vitis-unified-ide)
5. [Using the Flow Navigator](Section III - Flow Steps/ch12_launching_vitis_ide.md#using-the-flow-navigator)
6. [Quick Reference](Section III - Flow Steps/ch12_launching_vitis_ide.md#quick-reference)
---


### [Chapter 13: Building and Running an HLS Component](Section III - Flow Steps/ch13_building_hls_component.md)

1. [Overview](Section III - Flow Steps/ch13_building_hls_component.md#overview)
2. [Creating an HLS Component](Section III - Flow Steps/ch13_building_hls_component.md#creating-an-hls-component)
3. [Target Flow Overview](Section III - Flow Steps/ch13_building_hls_component.md#target-flow-overview)
4. [Working with Sources](Section III - Flow Steps/ch13_building_hls_component.md#working-with-sources)
5. [Adding RTL Blackbox Functions](Section III - Flow Steps/ch13_building_hls_component.md#adding-rtl-blackbox-functions)
6. [Defining the HLS Config File](Section III - Flow Steps/ch13_building_hls_component.md#defining-the-hls-config-file)
7. [Specifying the Clock Frequency](Section III - Flow Steps/ch13_building_hls_component.md#specifying-the-clock-frequency)
8. [Adding Pragmas and Directives](Section III - Flow Steps/ch13_building_hls_component.md#adding-pragmas-and-directives)
9. [Running C Simulation](Section III - Flow Steps/ch13_building_hls_component.md#running-c-simulation)
10. [Writing a Test Bench](Section III - Flow Steps/ch13_building_hls_component.md#writing-a-test-bench)
11. [Using Code Analyzer](Section III - Flow Steps/ch13_building_hls_component.md#using-code-analyzer)
12. [Debugging the HLS Component](Section III - Flow Steps/ch13_building_hls_component.md#debugging-the-hls-component)
13. [Running C Synthesis](Section III - Flow Steps/ch13_building_hls_component.md#running-c-synthesis)
14. [Synthesis Summary Reports](Section III - Flow Steps/ch13_building_hls_component.md#synthesis-summary-reports)
15. [Running C/RTL Co-Simulation](Section III - Flow Steps/ch13_building_hls_component.md#running-crtl-co-simulation)
16. [Packaging the RTL Design](Section III - Flow Steps/ch13_building_hls_component.md#packaging-the-rtl-design)
17. [Running Implementation](Section III - Flow Steps/ch13_building_hls_component.md#running-implementation)
18. [Optimizing the HLS Project](Section III - Flow Steps/ch13_building_hls_component.md#optimizing-the-hls-project)
19. [Best Practices Summary](Section III - Flow Steps/ch13_building_hls_component.md#best-practices-summary)
---


### [Chapter 14: Creating HLS Components from the Command Line](Section III - Flow Steps/ch14_hls_command_line.md)

1. [Overview](Section III - Flow Steps/ch14_hls_command_line.md#overview)
2. [Running C Synthesis](Section III - Flow Steps/ch14_hls_command_line.md#running-c-synthesis)
3. [Running C Simulation or Code Analyzer](Section III - Flow Steps/ch14_hls_command_line.md#running-c-simulation-or-code-analyzer)
4. [Running C/RTL Co-Simulation](Section III - Flow Steps/ch14_hls_command_line.md#running-crtl-co-simulation)
5. [Running Implementation](Section III - Flow Steps/ch14_hls_command_line.md#running-implementation)
6. [Exporting the IP/XO](Section III - Flow Steps/ch14_hls_command_line.md#exporting-the-ipxo)
7. [Quick Reference — Command Summary](Section III - Flow Steps/ch14_hls_command_line.md#quick-reference--command-summary)
---


## Section IV - Command Reference


### [Chapter 15 — vitis, v++, and vitis-run Commands](Section IV - Command Reference/ch15_vitis_commands.md)

1. [vitis Command](Section IV - Command Reference/ch15_vitis_commands.md#1-vitis-command)
2. [v++ Command](Section IV - Command Reference/ch15_vitis_commands.md#2-v-command)
3. [vitis-run Command](Section IV - Command Reference/ch15_vitis_commands.md#3-vitis-run-command)
4. [hls_init.tcl Initialization Script](Section IV - Command Reference/ch15_vitis_commands.md#4-hls_inittcl-initialization-script)
---


### [Chapter 16 — HLS Config File Commands](Section IV - Command Reference/ch16_config_file_commands.md)

1. [Overview and Config File Structure](Section IV - Command Reference/ch16_config_file_commands.md#1-overview-and-config-file-structure)
2. [Global Options (Outside [hls])](Section IV - Command Reference/ch16_config_file_commands.md#2-global-options-outside-hls)
3. [HLS General Options](Section IV - Command Reference/ch16_config_file_commands.md#3-hls-general-options)
4. [C-Synthesis Sources](Section IV - Command Reference/ch16_config_file_commands.md#4-c-synthesis-sources)
5. [Test Bench Sources](Section IV - Command Reference/ch16_config_file_commands.md#5-test-bench-sources)
6. [Array Partition Configuration](Section IV - Command Reference/ch16_config_file_commands.md#6-array-partition-configuration)
7. [C-Simulation Configuration](Section IV - Command Reference/ch16_config_file_commands.md#7-c-simulation-configuration)
8. [Co-Simulation Configuration](Section IV - Command Reference/ch16_config_file_commands.md#8-co-simulation-configuration)
9. [Compile Options](Section IV - Command Reference/ch16_config_file_commands.md#9-compile-options)
10. [Dataflow Configuration](Section IV - Command Reference/ch16_config_file_commands.md#10-dataflow-configuration)
11. [Debug Options](Section IV - Command Reference/ch16_config_file_commands.md#11-debug-options)
12. [Interface Configuration](Section IV - Command Reference/ch16_config_file_commands.md#12-interface-configuration)
13. [Package Options](Section IV - Command Reference/ch16_config_file_commands.md#13-package-options)
14. [Operator Configuration](Section IV - Command Reference/ch16_config_file_commands.md#14-operator-configuration)
15. [RTL Configuration](Section IV - Command Reference/ch16_config_file_commands.md#15-rtl-configuration)
16. [Schedule Settings](Section IV - Command Reference/ch16_config_file_commands.md#16-schedule-settings)
17. [Storage Configuration](Section IV - Command Reference/ch16_config_file_commands.md#17-storage-configuration)
18. [Vivado Implementation Settings](Section IV - Command Reference/ch16_config_file_commands.md#18-vivado-implementation-settings)
19. [Unroll Settings](Section IV - Command Reference/ch16_config_file_commands.md#19-unroll-settings)
20. [HLS Optimization Directives (`syn.directive.*`)](Section IV - Command Reference/ch16_config_file_commands.md#20-hls-optimization-directives-syndirecive)
21. [Best Practices](Section IV - Command Reference/ch16_config_file_commands.md#21-best-practices)
---


### [Chapter 17 — HLS Pragmas](Section IV - Command Reference/ch17_hls_pragmas.md)

| Pragma | Category | Link |
|---|---|---|
| aggregate | Struct/Array Packing | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| alias | M_AXI Pointer Aliasing | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| allocation | Resource Utilization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| array_partition | Array Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| array_reshape | Array Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| array_stencil | Array Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| bind_op | Resource Binding | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| bind_storage | Resource Binding | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| cache | M_AXI Cache | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| dataflow | Task-Level Pipelining | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| dependence | Loop Dependency Control | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| disaggregate | Struct Deconstruction | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| expression_balance | Expression Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| function_instantiate | Resource Utilization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| inline | Function Inlining | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| interface | Interface Synthesis | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| latency | Timing Constraints | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| loop_flatten | Loop Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| loop_merge | Loop Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| loop_tripcount | Loop Analysis | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| occurrence | Pipeline Optimization | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| performance | High-Level Performance Goals | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| pipeline | Loop/Function Pipelining | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| protocol | Cycle-Accurate Region | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| reset | Reset Control | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| stable | Stable Signal Declaration | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| stream | FIFO Stream Substitution | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| top | Top-Function Naming | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
| unroll | Loop Unrolling | [Section IV - Command Reference/ch17_hls_pragmas.md](Section IV - Command Reference/ch17_hls_pragmas.md) |
---


### [Chapter 18 — HLS Tcl Commands](Section IV - Command Reference/ch18_hls_tcl_commands.md)

*(No detailed TOC)*


## Section V - Driver Reference


### [Chapter 19 — AXI4-Lite Slave C Driver Reference](Section V - Driver Reference/ch19_axi4lite_driver.md)

- [Overview](Section V - Driver Reference/ch19_axi4lite_driver.md#overview)
- [Initialization / Release](Section V - Driver Reference/ch19_axi4lite_driver.md#initialization--release)
- [X<DUT>_Initialize](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_initialize)
- [X<DUT>_CfgInitialize](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_cfginitialize)
- [X<DUT>_LookupConfig](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_lookupconfig)
- [X<DUT>_Release](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_release)
- [Control Functions](Section V - Driver Reference/ch19_axi4lite_driver.md#control-functions)
- [X<DUT>_Start](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_start)
- [X<DUT>_IsDone](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_isdone)
- [X<DUT>_IsIdle](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_isidle)
- [X<DUT>_IsReady](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_isready)
- [X<DUT>_Continue](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_continue)
- [X<DUT>_EnableAutoRestart](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_enableautorestart)
- [X<DUT>_DisableAutoRestart](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_disableautorestart)
- [Scalar Argument I/O](Section V - Driver Reference/ch19_axi4lite_driver.md#scalar-argument-io)
- [X<DUT>_Set_ARG](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_set_arg)
- [X<DUT>_Set_ARG_vld](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_set_arg_vld)
- [X<DUT>_Set_ARG_ack](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_set_arg_ack)
- [X<DUT>_Get_ARG](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg)
- [X<DUT>_Get_ARG_vld](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_vld)
- [X<DUT>_Get_ARG_ack](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_ack)
- [Array Argument I/O (AXI4-Lite Grouped Arrays)](Section V - Driver Reference/ch19_axi4lite_driver.md#array-argument-io-axi4-lite-grouped-arrays)
- [X<DUT>_Get_ARG_BaseAddress](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_baseaddress)
- [X<DUT>_Get_ARG_HighAddress](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_highaddress)
- [X<DUT>_Get_ARG_TotalBytes](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_totalbytes)
- [X<DUT>_Get_ARG_BitWidth](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_bitwidth)
- [X<DUT>_Get_ARG_Depth](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_get_arg_depth)
- [X<DUT>_Write_ARG_Words](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_write_arg_words)
- [X<DUT>_Read_ARG_Words](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_read_arg_words)
- [X<DUT>_Write_ARG_Bytes](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_write_arg_bytes)
- [X<DUT>_Read_ARG_Bytes](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_read_arg_bytes)
- [Interrupt Functions](Section V - Driver Reference/ch19_axi4lite_driver.md#interrupt-functions)
- [X<DUT>_InterruptGlobalEnable / Disable](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_interruptglobalenable--disable)
- [X<DUT>_InterruptEnable / Disable](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_interruptenable--disable)
- [X<DUT>_InterruptClear](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_interruptclear)
- [X<DUT>_InterruptGetEnabled](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_interruptgetenabled)
- [X<DUT>_InterruptGetStatus](Section V - Driver Reference/ch19_axi4lite_driver.md#xdut_interruptgetstatus)
- [API Quick Reference Table](Section V - Driver Reference/ch19_axi4lite_driver.md#api-quick-reference-table)
---


## Section VI - Libraries Reference


### [Chapter 20 — C/C++ Builtin Functions](Section VI - Libraries Reference/ch20_builtin_functions.md)

*(No detailed TOC)*


### [Chapter 21 — Arbitrary Precision Data Types Library](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md)

1. [Overview & Motivation](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#overview)
2. [ap_[u]int — Arbitrary Precision Integers](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_uint)
- [Configuration & Limits](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_config)
- [Initialization & Assignment](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_init)
- [Console I/O](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_io)
- [Arithmetic Operators & Bit-Growth](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_arith)
- [Bitwise & Logical Operators](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_bitwise)
- [Shift Operators](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_shift)
- [Bit-Level Methods](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_bitmethods)
- [Explicit Conversion Methods](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_conv)
- [Compile-Time Attributes](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_int_static)
3. [ap_[u]fixed — Arbitrary Precision Fixed-Point](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#ap_ufixed)
- [Representation & Template Parameters](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_repr)
- [Quantization Modes (Q)](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_quant)
- [Overflow Modes (O, N)](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_overflow)
- [Initialization & Assignment](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_init)
- [Console I/O](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_io)
- [Arithmetic Operators & Bit-Growth](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_arith)
- [Bit-Level & Class Methods](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_methods)
- [Explicit Conversion Methods](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_conv)
- [Compile-Time Attributes](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#fixed_static)
4. [Best Practices](Section VI - Libraries Reference/ch21_arbitrary_precision_data_types.md#best_practices)
---


### [Chapter 22 — HLS Print Function](Section VI - Libraries Reference/ch22_hls_print.md)

*(No detailed TOC)*


### [Chapter 23 — HLS Math Library](Section VI - Libraries Reference/ch23_hls_math_library.md)

- [Overview](Section VI - Libraries Reference/ch23_hls_math_library.md#overview)
- [Accuracy and ULP Differences](Section VI - Libraries Reference/ch23_hls_math_library.md#accuracy-and-ulp-differences)
- [C Standard Mode Considerations](Section VI - Libraries Reference/ch23_hls_math_library.md#c-standard-mode-considerations)
- [Floating-Point Math Functions](Section VI - Libraries Reference/ch23_hls_math_library.md#floating-point-math-functions)
- [Fixed-Point Math Functions](Section VI - Libraries Reference/ch23_hls_math_library.md#fixed-point-math-functions)
- [Verification Strategies](Section VI - Libraries Reference/ch23_hls_math_library.md#verification-strategies)
- [Option 1: Standard Library + Accept Differences](Section VI - Libraries Reference/ch23_hls_math_library.md#option-1-standard-library--accept-differences)
- [Option 2: HLS Math Library (Source Modification)](Section VI - Libraries Reference/ch23_hls_math_library.md#option-2-hls-math-library-source-modification)
- [Option 3: HLS Math Library File (No Source Changes)](Section VI - Libraries Reference/ch23_hls_math_library.md#option-3-hls-math-library-file-no-source-changes)
- [Common Synthesis Errors](Section VI - Libraries Reference/ch23_hls_math_library.md#common-synthesis-errors)
---


### [Chapter 24 — HLS Stream Library](Section VI - Libraries Reference/ch24_hls_stream_library.md)

- [Overview](Section VI - Libraries Reference/ch24_hls_stream_library.md#overview)
- [C Modeling and RTL Implementation](Section VI - Libraries Reference/ch24_hls_stream_library.md#c-modeling-and-rtl-implementation)
- [Using HLS Streams](Section VI - Libraries Reference/ch24_hls_stream_library.md#using-hls-streams)
- [Declaration](Section VI - Libraries Reference/ch24_hls_stream_library.md#declaration)
- [Stream Naming](Section VI - Libraries Reference/ch24_hls_stream_library.md#stream-naming)
- [Passing Streams Between Functions](Section VI - Libraries Reference/ch24_hls_stream_library.md#passing-streams-between-functions)
- [Blocking API](Section VI - Libraries Reference/ch24_hls_stream_library.md#blocking-api)
- [Blocking Write](Section VI - Libraries Reference/ch24_hls_stream_library.md#blocking-write)
- [Blocking Read](Section VI - Libraries Reference/ch24_hls_stream_library.md#blocking-read)
- [Deterministic Behavior](Section VI - Libraries Reference/ch24_hls_stream_library.md#deterministic-behavior)
- [Non-Blocking API](Section VI - Libraries Reference/ch24_hls_stream_library.md#non-blocking-api)
- [Non-Blocking Write](Section VI - Libraries Reference/ch24_hls_stream_library.md#non-blocking-write)
- [Non-Blocking Read](Section VI - Libraries Reference/ch24_hls_stream_library.md#non-blocking-read)
- [Status Query Methods](Section VI - Libraries Reference/ch24_hls_stream_library.md#status-query-methods)
- [capacity()](Section VI - Libraries Reference/ch24_hls_stream_library.md#capacity)
- [empty()](Section VI - Libraries Reference/ch24_hls_stream_library.md#empty)
- [full()](Section VI - Libraries Reference/ch24_hls_stream_library.md#full)
- [size()](Section VI - Libraries Reference/ch24_hls_stream_library.md#size)
- [Controlling the RTL FIFO Depth](Section VI - Libraries Reference/ch24_hls_stream_library.md#controlling-the-rtl-fifo-depth)
- [Best Practices](Section VI - Libraries Reference/ch24_hls_stream_library.md#best-practices)
---


### [Chapter 25 — HLS Direct I/O](Section VI - Libraries Reference/ch25_hls_direct_io.md)

- [Overview](Section VI - Libraries Reference/ch25_hls_direct_io.md#overview)
- [Features of hls::direct_io](Section VI - Libraries Reference/ch25_hls_direct_io.md#features-of-hlsdirect_io)
- [Using Direct I/O Streams](Section VI - Libraries Reference/ch25_hls_direct_io.md#using-direct-io-streams)
- [Declaration](Section VI - Libraries Reference/ch25_hls_direct_io.md#declaration)
- [Type Support](Section VI - Libraries Reference/ch25_hls_direct_io.md#type-support)
- [Protocol Options](Section VI - Libraries Reference/ch25_hls_direct_io.md#protocol-options)
- [AP_HS — Two-way Handshake](Section VI - Libraries Reference/ch25_hls_direct_io.md#ap_hs--two-way-handshake)
- [AP_VLD — Valid Only](Section VI - Libraries Reference/ch25_hls_direct_io.md#ap_vld--valid-only)
- [AP_ACK — Acknowledge Only](Section VI - Libraries Reference/ch25_hls_direct_io.md#ap_ack--acknowledge-only)
- [AP_NONE — No Handshake](Section VI - Libraries Reference/ch25_hls_direct_io.md#ap_none--no-handshake)
- [Mapping Direct I/O to SAXI Lite](Section VI - Libraries Reference/ch25_hls_direct_io.md#mapping-direct-io-to-saxi-lite)
- [Blocking/Non-Blocking API](Section VI - Libraries Reference/ch25_hls_direct_io.md#blockingnon-blocking-api)
- [Blocking Writes](Section VI - Libraries Reference/ch25_hls_direct_io.md#blocking-writes)
- [Blocking Reads](Section VI - Libraries Reference/ch25_hls_direct_io.md#blocking-reads)
- [Non-Blocking Write](Section VI - Libraries Reference/ch25_hls_direct_io.md#non-blocking-write)
- [Non-Blocking Read](Section VI - Libraries Reference/ch25_hls_direct_io.md#non-blocking-read)
- [Direct I/O vs HLS Stream Comparison](Section VI - Libraries Reference/ch25_hls_direct_io.md#direct-io-vs-hls-stream-comparison)
---


### [Chapter 26 — HLS Fence Library](Section VI - Libraries Reference/ch26_hls_fence_library.md)

- [Overview](Section VI - Libraries Reference/ch26_hls_fence_library.md#overview)
- [Full Fence vs. Half Fence](Section VI - Libraries Reference/ch26_hls_fence_library.md#full-fence-vs-half-fence)
- [Practical Examples](Section VI - Libraries Reference/ch26_hls_fence_library.md#practical-examples)
- [Avoiding Deadlocks in Dataflow](Section VI - Libraries Reference/ch26_hls_fence_library.md#avoiding-deadlocks-in-dataflow)
- [Configuring the Vivado LogiCORE FFT](Section VI - Libraries Reference/ch26_hls_fence_library.md#configuring-the-vivado-logicore-fft)
- [Known Limitations](Section VI - Libraries Reference/ch26_hls_fence_library.md#known-limitations)
---


### [Chapter 27 — HLS Vector Library](Section VI - Libraries Reference/ch27_hls_vector_library.md)

- [Overview](Section VI - Libraries Reference/ch27_hls_vector_library.md#overview)
- [Memory Layout and Alignment](Section VI - Libraries Reference/ch27_hls_vector_library.md#memory-layout-and-alignment)
- [Initialization](Section VI - Libraries Reference/ch27_hls_vector_library.md#initialization)
- [Requirements and Dependencies](Section VI - Libraries Reference/ch27_hls_vector_library.md#requirements-and-dependencies)
- [Supported Operations](Section VI - Libraries Reference/ch27_hls_vector_library.md#supported-operations)
- [Element Access](Section VI - Libraries Reference/ch27_hls_vector_library.md#element-access)
- [Arithmetic Operations](Section VI - Libraries Reference/ch27_hls_vector_library.md#arithmetic-operations)
- [Comparison Operations](Section VI - Libraries Reference/ch27_hls_vector_library.md#comparison-operations)
---


### [Chapter 28 — HLS Task Library](Section VI - Libraries Reference/ch28_hls_task_library.md)

- [Overview](Section VI - Libraries Reference/ch28_hls_task_library.md#overview)
- [Basic Example — Data-Driven TLP](Section VI - Libraries Reference/ch28_hls_task_library.md#basic-example--data-driven-tlp)
- [Restrictions on hls::task](Section VI - Libraries Reference/ch28_hls_task_library.md#restrictions-on-hlstask)
- [Support of Scalars / Memory Interfaces in DTLP](Section VI - Libraries Reference/ch28_hls_task_library.md#support-of-scalars--memory-interfaces-in-dtlp)
- [Control-Driven TLP (CDTLP)](Section VI - Libraries Reference/ch28_hls_task_library.md#control-driven-tlp-cdtlp)
- [Data-Driven TLP (DTLP)](Section VI - Libraries Reference/ch28_hls_task_library.md#data-driven-tlp-dtlp)
- [Stable Memory Interface Example](Section VI - Libraries Reference/ch28_hls_task_library.md#stable-memory-interface-example)
- [Tasks and Channels — Explicit Programming Model](Section VI - Libraries Reference/ch28_hls_task_library.md#tasks-and-channels--explicit-programming-model)
- [Task Nesting](Section VI - Libraries Reference/ch28_hls_task_library.md#task-nesting)
- [Use of Flushing Pipelines](Section VI - Libraries Reference/ch28_hls_task_library.md#use-of-flushing-pipelines)
- [Simulation and Co-Simulation](Section VI - Libraries Reference/ch28_hls_task_library.md#simulation-and-co-simulation)
- [Tasks and Dataflow — Mixed Regions](Section VI - Libraries Reference/ch28_hls_task_library.md#tasks-and-dataflow--mixed-regions)
- [Task-Level Parallelism Hierarchy Rules](Section VI - Libraries Reference/ch28_hls_task_library.md#task-level-parallelism-hierarchy-rules)
- [Best Practices](Section VI - Libraries Reference/ch28_hls_task_library.md#best-practices)
---


### [Chapter 29 — HLS Split/Merge Library](Section VI - Libraries Reference/ch29_hls_split_merge.md)

- [Overview](Section VI - Libraries Reference/ch29_hls_split_merge.md#overview)
- [Specification Syntax](Section VI - Libraries Reference/ch29_hls_split_merge.md#specification-syntax)
- [Template Parameters](Section VI - Libraries Reference/ch29_hls_split_merge.md#template-parameters)
- [Scheduler Types](Section VI - Libraries Reference/ch29_hls_split_merge.md#scheduler-types)
- [Interface — Connecting to Processes](Section VI - Libraries Reference/ch29_hls_split_merge.md#interface--connecting-to-processes)
- [Example — Round-Robin with hls::task Workers](Section VI - Libraries Reference/ch29_hls_split_merge.md#example--round-robin-with-hlstask-workers)
- [Typical Use Case — Multi-Engine DDR/HBM Fanout](Section VI - Libraries Reference/ch29_hls_split_merge.md#typical-use-case--multi-engine-ddrhbm-fanout)
- [Best Practices](Section VI - Libraries Reference/ch29_hls_split_merge.md#best-practices)
---


### [Chapter 30 — HLS Stream of Blocks Library](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md)

- [Overview](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#overview)
- [The Problem with PIPOs](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#the-problem-with-pipos)
- [Template Declaration](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#template-declaration)
- [RAII Locking — write_lock and read_lock](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#raii-locking--write_lock-and-read_lock)
- [Comparison: PIPO vs stream_of_blocks](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#comparison-pipo-vs-stream_of_blocks)
- [Feedback Loop Example](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#feedback-loop-example)
- [Status Methods](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#status-methods)
- [RTL Interface — Handshake Signals](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#rtl-interface--handshake-signals)
- [BIND_STORAGE Pragma](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#bind_storage-pragma)
- [Limitations](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#limitations)
- [Best Practices](Section VI - Libraries Reference/ch30_hls_stream_of_blocks.md#best-practices)
---


### [Chapter 31 — HLS IP Libraries](Section VI - Libraries Reference/ch31_hls_ip_libraries.md)

- [Overview](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#overview)
- [DSP Intrinsics (`hls_dsp_builtins.h`)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#dsp-intrinsics-hls_dsp_builtinsh)
- [Port Data Types by Platform](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#port-data-types-by-platform)
- [Core Functions](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#core-functions)
- [Register Flags](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#register-flags)
- [Unsigned Input Handling](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#unsigned-input-handling)
- [Accumulator Class](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#accumulator-class)
- [Cascade Class](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#cascade-class)
- [DSP Complex Intrinsics (dspcplx — Versal only)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#dsp-complex-intrinsics-dspcplx--versal-only)
- [FFT IP Library (`hls_fft.h`)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fft-ip-library-hls_ffth)
- [Configuration Structure](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#configuration-structure)
- [Runtime Arguments](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#runtime-arguments)
- [Key Configuration Parameters](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#key-configuration-parameters)
- [SSR Restrictions](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#ssr-restrictions)
- [Usage Notes](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fft-usage-notes)
- [FIR IP Library (`hls_fir.h`)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fir-ip-library-hls_firh)
- [Configuration Structure](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fir-configuration-structure)
- [Key Configuration Parameters](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fir-key-configuration-parameters)
- [Usage Notes](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#fir-usage-notes)
- [DDS IP Library (`hls_dds.h`)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#dds-ip-library-hls_ddsh)
- [Configuration Structure](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#dds-configuration-structure)
- [Key Configuration Parameters](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#dds-key-configuration-parameters)
- [SRL Shift Register (`ap_shift_reg.h`)](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#srl-shift-register-ap_shift_regh)
- [Methods](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#srl-methods)
- [Example](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#srl-example)
- [Best Practices](Section VI - Libraries Reference/ch31_hls_ip_libraries.md#best-practices)
---


### [Chapter 32 — Working with OpenCV](Section VI - Libraries Reference/ch32_opencv.md)

*(No detailed TOC)*


## Section VII - Migration Guide


### [Chapter 33 — Migrating from Vitis HLS to the Vitis Unified IDE](Section VII - Migration Guide/ch33_migration_unified_ide.md)

- [Overview](Section VII - Migration Guide/ch33_migration_unified_ide.md#overview)
- [Migration Path 1: Create HLS Component from Existing Project](Section VII - Migration Guide/ch33_migration_unified_ide.md#migration-path-1-create-hls-component-from-existing-project)
- [Migration Path 2: Continue Using an Existing Tcl Script](Section VII - Migration Guide/ch33_migration_unified_ide.md#migration-path-2-continue-using-an-existing-tcl-script)
- [Migration Path 3: Convert to Python Script](Section VII - Migration Guide/ch33_migration_unified_ide.md#migration-path-3-convert-to-python-script)
- [Using write_ini to Create an HLS Config File](Section VII - Migration Guide/ch33_migration_unified_ide.md#using-write_ini-to-create-an-hls-config-file)
- [Best Practices](Section VII - Migration Guide/ch33_migration_unified_ide.md#best-practices)
---


### [Chapter 34 — Migrating from Vivado HLS to Vitis HLS](Section VII - Migration Guide/ch34_migration_vivado_hls.md)

- [Overview](Section VII - Migration Guide/ch34_migration_vivado_hls.md#overview)
- [Tool-Specific Macro](Section VII - Migration Guide/ch34_migration_vivado_hls.md#tool-specific-macro)
- [Default Control Settings](Section VII - Migration Guide/ch34_migration_vivado_hls.md#default-control-settings)
- [Vivado IP Development Flow Defaults](Section VII - Migration Guide/ch34_migration_vivado_hls.md#vivado-ip-development-flow-defaults)
- [Vitis Application Acceleration Flow Defaults](Section VII - Migration Guide/ch34_migration_vivado_hls.md#vitis-application-acceleration-flow-defaults)
- [Interface Differences](Section VII - Migration Guide/ch34_migration_vivado_hls.md#interface-differences)
- [AXI Bundle Rules](Section VII - Migration Guide/ch34_migration_vivado_hls.md#axi-bundle-rules)
- [Memory Storage Type on Interface](Section VII - Migration Guide/ch34_migration_vivado_hls.md#memory-storage-type-on-interface)
- [AXI4-Stream Side-Channels](Section VII - Migration Guide/ch34_migration_vivado_hls.md#axi4-stream-side-channels)
- [Memory Model Changes](Section VII - Migration Guide/ch34_migration_vivado_hls.md#memory-model-changes)
- [Unconnected Ports](Section VII - Migration Guide/ch34_migration_vivado_hls.md#unconnected-ports)
- [Global Variables on the Interface](Section VII - Migration Guide/ch34_migration_vivado_hls.md#global-variables-on-the-interface)
- [Module Naming Changes](Section VII - Migration Guide/ch34_migration_vivado_hls.md#module-naming-changes)
- [Auto-Prefix Behavior](Section VII - Migration Guide/ch34_migration_vivado_hls.md#auto-prefix-behavior)
- [Memory Module and RTL File Names](Section VII - Migration Guide/ch34_migration_vivado_hls.md#memory-module-and-rtl-file-names)
- [Function Inlining Changes](Section VII - Migration Guide/ch34_migration_vivado_hls.md#function-inlining-changes)
- [Dataflow: std::complex Support](Section VII - Migration Guide/ch34_migration_vivado_hls.md#dataflow-stdcomplex-support)
- [Best Practices](Section VII - Migration Guide/ch34_migration_vivado_hls.md#best-practices)
---


### [Chapter 35 — Deprecated and Unsupported Features](Section VII - Migration Guide/ch35_deprecated_unsupported.md)

- [Notation](Section VII - Migration Guide/ch35_deprecated_unsupported.md#notation)
- [Deprecated and Unsupported Tcl / Pragma Commands](Section VII - Migration Guide/ch35_deprecated_unsupported.md#deprecated-and-unsupported-tcl--pragma-commands)
- [Deprecated Libraries](Section VII - Migration Guide/ch35_deprecated_unsupported.md#deprecated-libraries)
- [Linear Algebra Library](Section VII - Migration Guide/ch35_deprecated_unsupported.md#linear-algebra-library)
- [DSP Library](Section VII - Migration Guide/ch35_deprecated_unsupported.md#dsp-library)
---


### [Chapter 36 — Unsupported Features](Section VII - Migration Guide/ch36_unsupported_features.md)

- [Overview](Section VII - Migration Guide/ch36_unsupported_features.md#overview)
- [Unsupported Pragma Usage](Section VII - Migration Guide/ch36_unsupported_features.md#unsupported-pragma-usage)
- [Unsupported Top-Level Function Argument Types](Section VII - Migration Guide/ch36_unsupported_features.md#unsupported-top-level-function-argument-types)
- [HLS Video Library](Section VII - Migration Guide/ch36_unsupported_features.md#hls-video-library)
- [C Arbitrary Precision Types](Section VII - Migration Guide/ch36_unsupported_features.md#c-arbitrary-precision-types)
- [Unsupported C Constructs](Section VII - Migration Guide/ch36_unsupported_features.md#unsupported-c-constructs)
---
