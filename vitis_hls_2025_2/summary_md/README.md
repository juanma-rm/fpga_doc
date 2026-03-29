# Vitis HLS UG1399 (v2025.2) - Complete Table of Contents

> Consolidated index of all chapters and sections.

## Quick Navigation

- [Section I - Introduction](#section-i---introduction)
- [Section II - Programmers Guide](#section-ii---programmers-guide)
- [Section III - Flow Steps](#section-iii---flow-steps)
- [Section IV - Command Reference](#section-iv---command-reference)
- [Section V - Driver Reference](#section-v---driver-reference)
- [Section VI - Libraries Reference](#section-vi---libraries-reference)
- [Section VII - Migration Guide](#section-vii---migration-guide)
- [Appendices](#appendices)

---

## Section I - Introduction

### [Section I - Introduction to Vitis HLS](section1_introduction/section_intro.md)

- [What is High-Level Synthesis?](section1_introduction/section_intro.md#1-what-is-high-level-synthesis)
- [Supported Operating Systems & Licensing](section1_introduction/section_intro.md#2-supported-operating-systems--licensing)
- [Changed Behavior in v2025.2](section1_introduction/section_intro.md#3-changed-behavior-in-v20252)
- [Benefits of HLS](section1_introduction/section_intro.md#4-benefits-of-hls)
- [Introduction to Vitis HLS Components](section1_introduction/section_intro.md#5-introduction-to-vitis-hls-components)
- [Key Synthesis Concepts](section1_introduction/section_intro.md#6-key-synthesis-concepts)
- [Refactoring C++ Source Code for HLS](section1_introduction/section_intro.md#7-refactoring-c-source-code-for-hls)
- [Re-Architecting the Hardware Module](section1_introduction/section_intro.md#8-re-architecting-the-hardware-module)
- [Best Practices](section1_introduction/section_intro.md#9-best-practices)
- [Tutorials and Examples](section1_introduction/section_intro.md#10-tutorials-and-examples)

---

## Section II - Programmers Guide

### [Chapter 1 - Design Principles](section2_hls_programmers_guide/ch01_design_principles.md)

- [Introduction & Motivation](section2_hls_programmers_guide/ch01_design_principles.md#1-introduction--motivation)
- [Throughput and Performance](section2_hls_programmers_guide/ch01_design_principles.md#2-throughput-and-performance)
- [Architecture Matters: CPU vs FPGA](section2_hls_programmers_guide/ch01_design_principles.md#3-architecture-matters-cpu-vs-fpga)
- [Three Paradigms for Programmable Logic](section2_hls_programmers_guide/ch01_design_principles.md#4-three-paradigms-for-programmable-logic)
- [Combining the Three Paradigms](section2_hls_programmers_guide/ch01_design_principles.md#5-combining-the-three-paradigms)
- [Conclusion - A Prescription for Performance](section2_hls_programmers_guide/ch01_design_principles.md#6-conclusion--a-prescription-for-performance)
- [Best Practices](section2_hls_programmers_guide/ch01_design_principles.md#7-best-practices)

### [Chapter 2 - Abstract Parallel Programming Model for HLS](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md)

- [The Abstract Parallel Programming Model](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#1-the-abstract-parallel-programming-model)
- [Channel Semantics: Blocking vs Non-Blocking](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#2-channel-semantics-blocking-vs-non-blocking)
- [Control-Driven vs Data-Driven TLP](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#3-control-driven-vs-data-driven-tlp)
- [Data-Driven TLP - hls::task](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#4-data-driven-tlp--hlstask)
- [Control-Driven TLP - Dataflow Pragma](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#5-control-driven-tlp--dataflow-pragma)
- [Dataflow Region Coding Style (WYSIWYG / Canonical)](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#6-dataflow-region-coding-style-wysiwyg--canonical)
- [Advanced Dataflow Features](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#7-advanced-dataflow-features)
- [Configuring Dataflow Memory Channels](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#8-configuring-dataflow-memory-channels)
- [Stream-of-Blocks (hls::stream_of_blocks)](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#9-stream-of-blocks-hlsstream_of_blocks)
- [Compiler-Created FIFO Types](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#10-compiler-created-fifo-types)
- [#pragma HLS stable](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#11-pragma-hls-stable)
- [Mixing Data-Driven and Control-Driven Models](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#12-mixing-data-driven-and-control-driven-models)
- [Summary: Choosing the Right TLP Model](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#13-summary-choosing-the-right-tlp-model)
- [Best Practices](section2_hls_programmers_guide/ch02_abstract_parallel_programming.md#14-best-practices)

### [Chapter 3 - Loops Primer](section2_hls_programmers_guide/ch03_loops_primer.md)

- [Why Loops Matter for HLS Performance](section2_hls_programmers_guide/ch03_loops_primer.md#1-why-loops-matter-for-hls-performance)
- [Pipelining Loops](section2_hls_programmers_guide/ch03_loops_primer.md#2-pipelining-loops)
- [Automatic Loop Pipelining](section2_hls_programmers_guide/ch03_loops_primer.md#3-automatic-loop-pipelining)
- [Rewinding Pipelined Loops](section2_hls_programmers_guide/ch03_loops_primer.md#4-rewinding-pipelined-loops)
- [Pipeline Types (STP / FRP / FLP)](section2_hls_programmers_guide/ch03_loops_primer.md#5-pipeline-types-stp--frp--flp)
- [Managing Pipeline Dependencies](section2_hls_programmers_guide/ch03_loops_primer.md#6-managing-pipeline-dependencies)
- [Removing False Dependencies](section2_hls_programmers_guide/ch03_loops_primer.md#7-removing-false-dependencies)
- [Unrolling Loops](section2_hls_programmers_guide/ch03_loops_primer.md#8-unrolling-loops)
- [Merging Loops](section2_hls_programmers_guide/ch03_loops_primer.md#9-merging-loops)
- [Working with Nested Loops](section2_hls_programmers_guide/ch03_loops_primer.md#10-working-with-nested-loops)
- [Working with Variable Loop Bounds](section2_hls_programmers_guide/ch03_loops_primer.md#11-working-with-variable-loop-bounds)
- [Best Practices](section2_hls_programmers_guide/ch03_loops_primer.md#12-best-practices)

### [Chapter 4 - Arrays Primer](section2_hls_programmers_guide/ch04_arrays_primer.md)

- [Mapping Software Arrays to Hardware Memory](section2_hls_programmers_guide/ch04_arrays_primer.md#1-mapping-software-arrays-to-hardware-memory)
- [Array Accesses and Performance](section2_hls_programmers_guide/ch04_arrays_primer.md#2-array-accesses-and-performance)
- [Array Partitioning](section2_hls_programmers_guide/ch04_arrays_primer.md#3-array-partitioning)
- [Array Reshaping](section2_hls_programmers_guide/ch04_arrays_primer.md#4-array-reshaping)
- [Arrays on the Interface](section2_hls_programmers_guide/ch04_arrays_primer.md#5-arrays-on-the-interface)
- [Initializing and Resetting Arrays](section2_hls_programmers_guide/ch04_arrays_primer.md#6-initializing-and-resetting-arrays)
- [Implementing ROMs](section2_hls_programmers_guide/ch04_arrays_primer.md#7-implementing-roms)
- [C Simulation with Large Arrays](section2_hls_programmers_guide/ch04_arrays_primer.md#8-c-simulation-with-large-arrays)
- [Best Practices](section2_hls_programmers_guide/ch04_arrays_primer.md#9-best-practices)

### [Chapter 5 - Functions Primer](section2_hls_programmers_guide/ch05_functions_primer.md)

- [Top-Level Function and Hierarchy](section2_hls_programmers_guide/ch05_functions_primer.md#1-top-level-function-and-hierarchy)
- [Function Inlining](section2_hls_programmers_guide/ch05_functions_primer.md#2-function-inlining)
- [Function Pipelining](section2_hls_programmers_guide/ch05_functions_primer.md#3-function-pipelining)
- [Function Instantiation](section2_hls_programmers_guide/ch05_functions_primer.md#4-function-instantiation)
- [Best Practices](section2_hls_programmers_guide/ch05_functions_primer.md#5-best-practices)

### [Chapter 6 - Data Types](section2_hls_programmers_guide/ch06_data_types.md)

- [Standard C/C++ Types](section2_hls_programmers_guide/ch06_data_types.md#1-standard-cc-types)
- [Floats and Doubles](section2_hls_programmers_guide/ch06_data_types.md#2-floats-and-doubles)
- [Composite Data Types](section2_hls_programmers_guide/ch06_data_types.md#3-composite-data-types)
- [Type Qualifiers](section2_hls_programmers_guide/ch06_data_types.md#4-type-qualifiers)
- [Arbitrary Precision Integer Types (ap_int)](section2_hls_programmers_guide/ch06_data_types.md#5-arbitrary-precision-integer-types-ap_int)
- [Arbitrary Precision Fixed-Point Types (ap_fixed)](section2_hls_programmers_guide/ch06_data_types.md#6-arbitrary-precision-fixed-point-types-ap_fixed)
- [Arbitrary Precision Floating-Point Library (ap_float)](section2_hls_programmers_guide/ch06_data_types.md#7-arbitrary-precision-floating-point-library-ap_float)
- [Global Variables](section2_hls_programmers_guide/ch06_data_types.md#8-global-variables)
- [Pointers](section2_hls_programmers_guide/ch06_data_types.md#9-pointers)
- [Best Practices](section2_hls_programmers_guide/ch06_data_types.md#10-best-practices)

### [Chapter 7 - Unsupported C/C++ Constructs](section2_hls_programmers_guide/ch07_unsupported_constructs.md)

- [Synthesis Requirements](section2_hls_programmers_guide/ch07_unsupported_constructs.md#1-synthesis-requirements)
- [System Calls](section2_hls_programmers_guide/ch07_unsupported_constructs.md#2-system-calls)
- [Dynamic Memory Allocation](section2_hls_programmers_guide/ch07_unsupported_constructs.md#3-dynamic-memory-allocation)
- [Pointer Limitations](section2_hls_programmers_guide/ch07_unsupported_constructs.md#4-pointer-limitations)
- [Recursive Functions](section2_hls_programmers_guide/ch07_unsupported_constructs.md#5-recursive-functions)
- [Standard Template Libraries (STL)](section2_hls_programmers_guide/ch07_unsupported_constructs.md#6-standard-template-libraries-stl)
- [Undefined Behaviors](section2_hls_programmers_guide/ch07_unsupported_constructs.md#7-undefined-behaviors)
- [Virtual Functions](section2_hls_programmers_guide/ch07_unsupported_constructs.md#8-virtual-functions)
- [Quick Reference Table](section2_hls_programmers_guide/ch07_unsupported_constructs.md#9-quick-reference-table)

### [Chapter 8: Interfaces of the HLS Design](section2_hls_programmers_guide/ch08_interfaces.md)

- [Interface Synthesis Overview](section2_hls_programmers_guide/ch08_interfaces.md#1-interface-synthesis-overview)
- [Vitis Kernel Flow Defaults](section2_hls_programmers_guide/ch08_interfaces.md#2-vitis-kernel-flow-defaults)
- [Vivado IP Flow Defaults](section2_hls_programmers_guide/ch08_interfaces.md#3-vivado-ip-flow-defaults)
- [M_AXI Interface](section2_hls_programmers_guide/ch08_interfaces.md#4-m_axi-interface)
- [S_AXILITE Interface](section2_hls_programmers_guide/ch08_interfaces.md#5-s_axilite-interface)
- [AXI4-Stream (AXIS) Interface](section2_hls_programmers_guide/ch08_interfaces.md#6-axi4-stream-axis-interface)
- [Aggregation and Disaggregation of Structs](section2_hls_programmers_guide/ch08_interfaces.md#7-aggregation-and-disaggregation-of-structs)
- [Block-Level Control Protocols](section2_hls_programmers_guide/ch08_interfaces.md#8-block-level-control-protocols)
- [Execution Modes](section2_hls_programmers_guide/ch08_interfaces.md#9-execution-modes)

### [Chapter 9: Best Practices for Designing with M_AXI Interfaces](section2_hls_programmers_guide/ch09_maxi_best_practices.md)

- [Overview and Goals](section2_hls_programmers_guide/ch09_maxi_best_practices.md#1-overview-and-goals)
- [Load-Compute-Store (LCS) Pattern](section2_hls_programmers_guide/ch09_maxi_best_practices.md#2-loadcomputestore-lcs-pattern)
- [Hardware Data Flow Mindset](section2_hls_programmers_guide/ch09_maxi_best_practices.md#3-hardware-data-flow-mindset)
- [Global Memory Access Strategy](section2_hls_programmers_guide/ch09_maxi_best_practices.md#4-global-memory-access-strategy)
- [Port Width Maximization](section2_hls_programmers_guide/ch09_maxi_best_practices.md#5-port-width-maximization)
- [Memory Resource Selection](section2_hls_programmers_guide/ch09_maxi_best_practices.md#6-memory-resource-selection)
- [Concurrent Port Configuration](section2_hls_programmers_guide/ch09_maxi_best_practices.md#7-concurrent-port-configuration)
- [Burst Length Configuration](section2_hls_programmers_guide/ch09_maxi_best_practices.md#8-burst-length-configuration)
- [Outstanding Requests Configuration](section2_hls_programmers_guide/ch09_maxi_best_practices.md#9-outstanding-requests-configuration)
- [Best Practices Summary](section2_hls_programmers_guide/ch09_maxi_best_practices.md#10-best-practices-summary)

### [Chapter 10: Top-Level Performance Pragma](section2_hls_programmers_guide/ch10_performance_pragma.md)

- [Overview](section2_hls_programmers_guide/ch10_performance_pragma.md#1-overview)
- [Top-Level vs. Loop-Level Performance Pragma](section2_hls_programmers_guide/ch10_performance_pragma.md#2-top-level-vs-loop-level-performance-pragma)
- [Step-by-Step Methodology](section2_hls_programmers_guide/ch10_performance_pragma.md#3-step-by-step-methodology)
- [Pragma Syntax](section2_hls_programmers_guide/ch10_performance_pragma.md#4-pragma-syntax)
- [Optimization Strategy and Priority](section2_hls_programmers_guide/ch10_performance_pragma.md#5-optimization-strategy-and-priority)
- [Limitations and Precedence Rules](section2_hls_programmers_guide/ch10_performance_pragma.md#6-limitations-and-precedence-rules)
- [Unsupported Libraries and Constructs](section2_hls_programmers_guide/ch10_performance_pragma.md#7-unsupported-libraries-and-constructs)
- [Known Issues](section2_hls_programmers_guide/ch10_performance_pragma.md#8-known-issues)
- [Best Practices](section2_hls_programmers_guide/ch10_performance_pragma.md#9-best-practices)

### [Chapter 11: Optimizing Techniques and Troubleshooting Tips](section2_hls_programmers_guide/ch11_optimizing_techniques.md)

- [Optimization Directives Overview](section2_hls_programmers_guide/ch11_optimizing_techniques.md#1-optimization-directives-overview)
- [HLS Scheduling and Binding](section2_hls_programmers_guide/ch11_optimizing_techniques.md#2-hls-scheduling-and-binding)
- [Optimizing Logic Expressions](section2_hls_programmers_guide/ch11_optimizing_techniques.md#3-optimizing-logic-expressions)
- [Optimizing AXI System Performance](section2_hls_programmers_guide/ch11_optimizing_techniques.md#4-optimizing-axi-system-performance)
- [Managing Area and Hardware Resources](section2_hls_programmers_guide/ch11_optimizing_techniques.md#5-managing-area-and-hardware-resources)
- [Limitations of Control-Driven Task-Level Parallelism (Dataflow)](section2_hls_programmers_guide/ch11_optimizing_techniques.md#6-limitations-of-control-driven-task-level-parallelism-dataflow)
- [Limitations of Pipelining with Static Variables](section2_hls_programmers_guide/ch11_optimizing_techniques.md#7-limitations-of-pipelining-with-static-variables)
- [Canonical Dataflow Coding Style](section2_hls_programmers_guide/ch11_optimizing_techniques.md#8-canonical-dataflow-coding-style)
- [Best Practices](section2_hls_programmers_guide/ch11_optimizing_techniques.md#9-best-practices)

---

## Section III - Flow Steps

### [Chapter 12: Launching the Vitis Unified IDE](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md)

- [Overview](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#overview)
- [Launching the IDE](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#launching-the-ide)
- [Welcome Screen Options](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#welcome-screen-options)
- [Features of the Vitis Unified IDE](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#features-of-the-vitis-unified-ide)
- [Using the Flow Navigator](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#using-the-flow-navigator)
- [Quick Reference](section3_vitis_hls_flow_steps/ch12_launching_vitis_ide.md#quick-reference)

### [Chapter 13: Building and Running an HLS Component](section3_vitis_hls_flow_steps/ch13_building_hls_component.md)

- [Overview](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#overview)
- [Creating an HLS Component](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#creating-an-hls-component)
- [Target Flow Overview](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#target-flow-overview)
- [Working with Sources](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#working-with-sources)
- [Adding RTL Blackbox Functions](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#adding-rtl-blackbox-functions)
- [Defining the HLS Config File](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#defining-the-hls-config-file)
- [Specifying the Clock Frequency](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#specifying-the-clock-frequency)
- [Adding Pragmas and Directives](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#adding-pragmas-and-directives)
- [Running C Simulation](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#running-c-simulation)
- [Writing a Test Bench](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#writing-a-test-bench)
- [Using Code Analyzer](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#using-code-analyzer)
- [Debugging the HLS Component](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#debugging-the-hls-component)
- [Running C Synthesis](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#running-c-synthesis)
- [Synthesis Summary Reports](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#synthesis-summary-reports)
- [Running C/RTL Co-Simulation](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#running-crtl-co-simulation)
- [Packaging the RTL Design](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#packaging-the-rtl-design)
- [Running Implementation](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#running-implementation)
- [Optimizing the HLS Project](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#optimizing-the-hls-project)
- [Best Practices Summary](section3_vitis_hls_flow_steps/ch13_building_hls_component.md#best-practices-summary)

### [Chapter 14: Creating HLS Components from the Command Line](section3_vitis_hls_flow_steps/ch14_hls_command_line.md)

- [Overview](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#overview)
- [Running C Synthesis](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#running-c-synthesis)
- [Running C Simulation or Code Analyzer](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#running-c-simulation-or-code-analyzer)
- [Running C/RTL Co-Simulation](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#running-crtl-co-simulation)
- [Running Implementation](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#running-implementation)
- [Exporting the IP/XO](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#exporting-the-ipxo)
- [Quick Reference - Command Summary](section3_vitis_hls_flow_steps/ch14_hls_command_line.md#quick-reference--command-summary)

---

## Section IV - Command Reference

### [Chapter 15 - vitis, v++, and vitis-run Commands](section4_vitis_hls_command_reference/ch15_vitis_commands.md)

- [vitis Command](section4_vitis_hls_command_reference/ch15_vitis_commands.md#1-vitis-command)
- [v++ Command](section4_vitis_hls_command_reference/ch15_vitis_commands.md#2-v-command)
- [vitis-run Command](section4_vitis_hls_command_reference/ch15_vitis_commands.md#3-vitis-run-command)
- [hls_init.tcl Initialization Script](section4_vitis_hls_command_reference/ch15_vitis_commands.md#4-hls_inittcl-initialization-script)

### [Chapter 16 - HLS Config File Commands](section4_vitis_hls_command_reference/ch16_config_file_commands.md)

- [Overview and Config File Structure](section4_vitis_hls_command_reference/ch16_config_file_commands.md#1-overview-and-config-file-structure)
- [Global Options (Outside [hls])](section4_vitis_hls_command_reference/ch16_config_file_commands.md#2-global-options-outside-hls)
- [HLS General Options](section4_vitis_hls_command_reference/ch16_config_file_commands.md#3-hls-general-options)
- [C-Synthesis Sources](section4_vitis_hls_command_reference/ch16_config_file_commands.md#4-c-synthesis-sources)
- [Test Bench Sources](section4_vitis_hls_command_reference/ch16_config_file_commands.md#5-test-bench-sources)
- [Array Partition Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#6-array-partition-configuration)
- [C-Simulation Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#7-c-simulation-configuration)
- [Co-Simulation Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#8-co-simulation-configuration)
- [Compile Options](section4_vitis_hls_command_reference/ch16_config_file_commands.md#9-compile-options)
- [Dataflow Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#10-dataflow-configuration)
- [Debug Options](section4_vitis_hls_command_reference/ch16_config_file_commands.md#11-debug-options)
- [Interface Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#12-interface-configuration)
- [Package Options](section4_vitis_hls_command_reference/ch16_config_file_commands.md#13-package-options)
- [Operator Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#14-operator-configuration)
- [RTL Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#15-rtl-configuration)
- [Schedule Settings](section4_vitis_hls_command_reference/ch16_config_file_commands.md#16-schedule-settings)
- [Storage Configuration](section4_vitis_hls_command_reference/ch16_config_file_commands.md#17-storage-configuration)
- [Vivado Implementation Settings](section4_vitis_hls_command_reference/ch16_config_file_commands.md#18-vivado-implementation-settings)
- [Unroll Settings](section4_vitis_hls_command_reference/ch16_config_file_commands.md#19-unroll-settings)
- [HLS Optimization Directives (syn.directive.*)](section4_vitis_hls_command_reference/ch16_config_file_commands.md#20-hls-optimization-directives-syndirecive)
- [Best Practices](section4_vitis_hls_command_reference/ch16_config_file_commands.md#21-best-practices)

### [Chapter 17 - HLS Pragmas](section4_vitis_hls_command_reference/ch17_hls_pragmas.md)

- [pragma HLS aggregate](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-aggregate)
- [pragma HLS alias](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-alias)
- [pragma HLS allocation](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-allocation)
- [pragma HLS array_partition](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-array_partition)
- [pragma HLS array_reshape](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-array_reshape)
- [pragma HLS array_stencil](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-array_stencil)
- [pragma HLS bind_op](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-bind_op)
- [pragma HLS bind_storage](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-bind_storage)
- [pragma HLS cache](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-cache)
- [pragma HLS dataflow](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-dataflow)
- [pragma HLS dependence](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-dependence)
- [pragma HLS disaggregate](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-disaggregate)
- [pragma HLS expression_balance](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-expression_balance)
- [pragma HLS function_instantiate](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-function_instantiate)
- [pragma HLS inline](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-inline)
- [pragma HLS interface](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-interface)
- [pragma HLS latency](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-latency)
- [pragma HLS loop_flatten](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-loop_flatten)
- [pragma HLS loop_merge](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-loop_merge)
- [pragma HLS loop_tripcount](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-loop_tripcount)
- [pragma HLS occurrence](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-occurrence)
- [pragma HLS performance](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-performance)
- [pragma HLS pipeline](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-pipeline)
- [pragma HLS protocol](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-protocol)
- [pragma HLS reset](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-reset)
- [pragma HLS stable](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-stable)
- [pragma HLS stream](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-stream)
- [pragma HLS top](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-top)
- [pragma HLS unroll](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#pragma-hls-unroll)
- [Best Practices](section4_vitis_hls_command_reference/ch17_hls_pragmas.md#best-practices)

### [Chapter 18 - HLS Tcl Commands](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md)

- [Project Commands](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md#project-commands)
- [Configuration Commands](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md#configuration-commands)
- [Optimization Directives](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md#optimization-directives)
- [Quick Reference: Config Commands vs. Pragma Scope](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md#quick-reference-config-commands-vs-pragma-scope)
- [Best Practices](section4_vitis_hls_command_reference/ch18_hls_tcl_commands.md#best-practices)

---

## Section V - Driver Reference

### [Chapter 19 - AXI4-Lite Slave C Driver Reference](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md)

- [Overview](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#overview)
- [Initialization / Release](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#initialization--release)
- [Control Functions](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#control-functions)
- [Scalar Argument I/O](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#scalar-argument-io)
- [Array Argument I/O (AXI4-Lite Grouped Arrays)](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#array-argument-io-axi4-lite-grouped-arrays)
- [Interrupt Functions](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#interrupt-functions)
- [API Quick Reference Table](section5_vitis_hls_c_driver_reference/ch19_axi4lite_driver.md#api-quick-reference-table)

---

## Section VI - Libraries Reference

### [Chapter 20 - C/C++ Builtin Functions](section6_vitis_hls_libraries_reference/ch20_builtin_functions.md)

- [Overview](section6_vitis_hls_libraries_reference/ch20_builtin_functions.md#overview)
- [Supported Builtins](section6_vitis_hls_libraries_reference/ch20_builtin_functions.md#supported-builtins)
- [Example](section6_vitis_hls_libraries_reference/ch20_builtin_functions.md#example)
- [Quick Reference](section6_vitis_hls_libraries_reference/ch20_builtin_functions.md#quick-reference)

### [Chapter 21 - Arbitrary Precision Data Types Library](section6_vitis_hls_libraries_reference/ch21_arbitrary_precision_data_types.md)

- [Overview & Motivation](section6_vitis_hls_libraries_reference/ch21_arbitrary_precision_data_types.md#overview)
- [ap_[u]int - Arbitrary Precision Integers](section6_vitis_hls_libraries_reference/ch21_arbitrary_precision_data_types.md#ap_uint)
- [ap_[u]fixed - Arbitrary Precision Fixed-Point](section6_vitis_hls_libraries_reference/ch21_arbitrary_precision_data_types.md#ap_ufixed)
- [Best Practices](section6_vitis_hls_libraries_reference/ch21_arbitrary_precision_data_types.md#best_practices)

### [Chapter 22 - HLS Print Function](section6_vitis_hls_libraries_reference/ch22_hls_print.md)

- [Overview](section6_vitis_hls_libraries_reference/ch22_hls_print.md#overview)
- [Use Cases](section6_vitis_hls_libraries_reference/ch22_hls_print.md#use-cases)
- [Usage Example](section6_vitis_hls_libraries_reference/ch22_hls_print.md#usage-example)
- [Supported Format Specifiers](section6_vitis_hls_libraries_reference/ch22_hls_print.md#supported-format-specifiers)
- [Key Constraints and Caveats](section6_vitis_hls_libraries_reference/ch22_hls_print.md#key-constraints-and-caveats)
- [Best Practices](section6_vitis_hls_libraries_reference/ch22_hls_print.md#best-practices)

### [Chapter 23 - HLS Math Library](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md)

- [Overview](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#overview)
- [Accuracy and ULP Differences](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#accuracy-and-ulp-differences)
- [C Standard Mode Considerations](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#c-standard-mode-considerations)
- [Floating-Point Math Functions](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#floating-point-math-functions)
- [Fixed-Point Math Functions](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#fixed-point-math-functions)
- [Verification Strategies](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#verification-strategies)
- [Common Synthesis Errors](section6_vitis_hls_libraries_reference/ch23_hls_math_library.md#common-synthesis-errors)

### [Chapter 24 - HLS Stream Library](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md)

- [Overview](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#overview)
- [C Modeling and RTL Implementation](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#c-modeling-and-rtl-implementation)
- [Using HLS Streams](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#using-hls-streams)
- [Blocking API](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#blocking-api)
- [Non-Blocking API](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#non-blocking-api)
- [Status Query Methods](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#status-query-methods)
- [Controlling the RTL FIFO Depth](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#controlling-the-rtl-fifo-depth)
- [Best Practices](section6_vitis_hls_libraries_reference/ch24_hls_stream_library.md#best-practices)

### [Chapter 25 - HLS Direct I/O](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md)

- [Overview](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#overview)
- [Features of hls::direct_io](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#features-of-hlsdirect_io)
- [Using Direct I/O Streams](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#using-direct-io-streams)
- [Protocol Options](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#protocol-options)
- [Mapping Direct I/O to SAXI Lite](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#mapping-direct-io-to-saxi-lite)
- [Blocking/Non-Blocking API](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#blockingnon-blocking-api)
- [Direct I/O vs HLS Stream Comparison](section6_vitis_hls_libraries_reference/ch25_hls_direct_io.md#direct-io-vs-hls-stream-comparison)

### [Chapter 26 - HLS Fence Library](section6_vitis_hls_libraries_reference/ch26_hls_fence_library.md)

- [Overview](section6_vitis_hls_libraries_reference/ch26_hls_fence_library.md#overview)
- [Full Fence vs. Half Fence](section6_vitis_hls_libraries_reference/ch26_hls_fence_library.md#full-fence-vs-half-fence)
- [Practical Examples](section6_vitis_hls_libraries_reference/ch26_hls_fence_library.md#practical-examples)
- [Known Limitations](section6_vitis_hls_libraries_reference/ch26_hls_fence_library.md#known-limitations)

### [Chapter 27 - HLS Vector Library](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md)

- [Overview](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md#overview)
- [Memory Layout and Alignment](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md#memory-layout-and-alignment)
- [Initialization](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md#initialization)
- [Requirements and Dependencies](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md#requirements-and-dependencies)
- [Supported Operations](section6_vitis_hls_libraries_reference/ch27_hls_vector_library.md#supported-operations)

### [Chapter 28 - HLS Task Library](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md)

- [Overview](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#overview)
- [Basic Example - Data-Driven TLP](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#basic-example--data-driven-tlp)
- [Restrictions on hls::task](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#restrictions-on-hlstask)
- [Support of Scalars / Memory Interfaces in DTLP](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#support-of-scalars--memory-interfaces-in-dtlp)
- [Tasks and Channels - Explicit Programming Model](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#tasks-and-channels--explicit-programming-model)
- [Use of Flushing Pipelines](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#use-of-flushing-pipelines)
- [Simulation and Co-Simulation](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#simulation-and-co-simulation)
- [Tasks and Dataflow - Mixed Regions](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#tasks-and-dataflow--mixed-regions)
- [Task-Level Parallelism Hierarchy Rules](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#task-level-parallelism-hierarchy-rules)
- [Best Practices](section6_vitis_hls_libraries_reference/ch28_hls_task_library.md#best-practices)

### [Chapter 29 - HLS Split/Merge Library](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md)

- [Overview](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#overview)
- [Specification Syntax](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#specification-syntax)
- [Template Parameters](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#template-parameters)
- [Scheduler Types](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#scheduler-types)
- [Interface - Connecting to Processes](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#interface--connecting-to-processes)
- [Example - Round-Robin with hls::task Workers](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#example--round-robin-with-hlstask-workers)
- [Typical Use Case - Multi-Engine DDR/HBM Fanout](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#typical-use-case--multi-engine-ddrhbm-fanout)
- [Best Practices](section6_vitis_hls_libraries_reference/ch29_hls_split_merge.md#best-practices)

### [Chapter 30 - HLS Stream of Blocks Library](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md)

- [Overview](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#overview)
- [The Problem with PIPOs](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#the-problem-with-pipos)
- [Template Declaration](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#template-declaration)
- [RAII Locking - write_lock and read_lock](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#raii-locking--write_lock-and-read_lock)
- [Comparison: PIPO vs stream_of_blocks](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#comparison-pipo-vs-stream_of_blocks)
- [Feedback Loop Example](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#feedback-loop-example)
- [Status Methods](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#status-methods)
- [RTL Interface - Handshake Signals](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#rtl-interface--handshake-signals)
- [BIND_STORAGE Pragma](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#bind_storage-pragma)
- [Limitations](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#limitations)
- [Best Practices](section6_vitis_hls_libraries_reference/ch30_hls_stream_of_blocks.md#best-practices)

### [Chapter 31 - HLS IP Libraries](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md)

- [Overview](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#overview)
- [DSP Intrinsics (hls_dsp_builtins.h)](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#dsp-intrinsics-hls_dsp_builtinsh)
- [FFT IP Library (hls_fft.h)](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#fft-ip-library-hls_ffth)
- [FIR IP Library (hls_fir.h)](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#fir-ip-library-hls_firh)
- [DDS IP Library (hls_dds.h)](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#dds-ip-library-hls_ddsh)
- [SRL Shift Register (ap_shift_reg.h)](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#srl-shift-register-ap_shift_regh)
- [Best Practices](section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md#best-practices)

### [Chapter 32 - Working with OpenCV](section6_vitis_hls_libraries_reference/ch32_opencv.md)

- [Overview](section6_vitis_hls_libraries_reference/ch32_opencv.md#overview)
- [Vitis Vision Library](section6_vitis_hls_libraries_reference/ch32_opencv.md#vitis-vision-library)
- [Key Points](section6_vitis_hls_libraries_reference/ch32_opencv.md#key-points)

---

## Section VII - Migration Guide

### [Chapter 33 - Migrating from Vitis HLS to the Vitis Unified IDE](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md)

- [Overview](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#overview)
- [Migration Path 1: Create HLS Component from Existing Project](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#migration-path-1-create-hls-component-from-existing-project)
- [Migration Path 2: Continue Using an Existing Tcl Script](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#migration-path-2-continue-using-an-existing-tcl-script)
- [Migration Path 3: Convert to Python Script](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#migration-path-3-convert-to-python-script)
- [Using write_ini to Create an HLS Config File](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#using-write_ini-to-create-an-hls-config-file)
- [Best Practices](section7_vitis_hls_migration_guide/ch33_migration_unified_ide.md#best-practices)

---

### [Chapter 34 - Migrating from Vivado HLS to Vitis HLS](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md)

- [Overview](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#overview)
- [Tool-Specific Macro](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#tool-specific-macro)
- [Default Control Settings](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#default-control-settings)
  - [Vivado IP Development Flow Defaults](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#vivado-ip-development-flow-defaults)
  - [Vitis Application Acceleration Flow Defaults](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#vitis-application-acceleration-flow-defaults)
- [Interface Differences](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#interface-differences)
  - [AXI Bundle Rules](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#axi-bundle-rules)
  - [Memory Storage Type on Interface](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#memory-storage-type-on-interface)
  - [AXI4-Stream Side-Channels](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#axi4-stream-side-channels)
- [Memory Model Changes](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#memory-model-changes)
- [Unconnected Ports](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#unconnected-ports)
- [Global Variables on the Interface](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#global-variables-on-the-interface)
- [Module Naming Changes](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#module-naming-changes)
  - [Auto-Prefix Behavior](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#auto-prefix-behavior)
  - [Memory Module and RTL File Names](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#memory-module-and-rtl-file-names)
- [Function Inlining Changes](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#function-inlining-changes)
- [Dataflow: std::complex Support](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#dataflow-stdcomplex-support)
- [Best Practices](section7_vitis_hls_migration_guide/ch34_migration_vivado_hls.md#best-practices)

---

### [Chapter 35 - Deprecated and Unsupported Features](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md)

- [Notation](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md#notation)
- [Deprecated and Unsupported Tcl / Pragma Commands](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md#deprecated-and-unsupported-tcl--pragma-commands)
- [Deprecated Libraries](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md#deprecated-libraries)
  - [Linear Algebra Library](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md#linear-algebra-library)
  - [DSP Library](section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md#dsp-library)

---

### [Chapter 36 - Unsupported Features](section7_vitis_hls_migration_guide/ch36_unsupported_features.md)

- [Overview](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#overview)
- [Unsupported Pragma Usage](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#unsupported-pragma-usage)
- [Unsupported Top-Level Function Argument Types](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#unsupported-top-level-function-argument-types)
- [HLS Video Library](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#hls-video-library)
- [C Arbitrary Precision Types](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#c-arbitrary-precision-types)
- [Unsupported C Constructs](section7_vitis_hls_migration_guide/ch36_unsupported_features.md#unsupported-c-constructs)

---

## Appendices

### [Appendix A - Tcl to Config File Command Map](Appendices/appendix_a_tcl_config_map.md)

- [Overview](Appendices/appendix_a_tcl_config_map.md#overview)
- [Table 69: Tcl Project Commands](Appendices/appendix_a_tcl_config_map.md#table-69-tcl-project-commands)
- [Table 70: Tcl Configuration Commands](Appendices/appendix_a_tcl_config_map.md#table-70-tcl-configuration-commands)

---

### [Appendix B - Instruction/Operator Explanation](Appendices/appendix_b_operators.md)

- [Overview](Appendices/appendix_b_operators.md#overview)
- [Operator Reference Table](Appendices/appendix_b_operators.md#operator-reference-table)

---

### [Appendix C - Additional Resources and Legal Notices](Appendices/appendix_c_resources.md)

- [Finding Additional Documentation](Appendices/appendix_c_resources.md#finding-additional-documentation)
  - [AMD Technical Information Portal](Appendices/appendix_c_resources.md#amd-technical-information-portal)
  - [Documentation Navigator (DocNav)](Appendices/appendix_c_resources.md#documentation-navigator-docnav)
  - [Design Hubs](Appendices/appendix_c_resources.md#design-hubs)
- [Support Resources](Appendices/appendix_c_resources.md#support-resources)
- [References](Appendices/appendix_c_resources.md#references)
- [Revision History Summary](Appendices/appendix_c_resources.md#revision-history-summary)

---
