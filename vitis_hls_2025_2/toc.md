# Table of Contents

## Section I: Introduction (10)
* Navigating Content by Design Process (10)
* Supported Operating Systems for Vitis HLS (11)
* Obtaining a Vitis HLS License (11)
* Changed Behavior (13)
* Benefits of High-Level Synthesis (14)
* Introduction to Vitis HLS Components (16)
    * Refactoring C++ Source Code for HLS (19)
* Tutorials and Examples (22)

## Section II: HLS Programmers Guide (23)
* **Chapter 1: Design Principles (24)**
    * Three Paradigms for Programmable Logic (25)
    * Combining the Three Paradigms (32)
    * Conclusion - A Prescription for Performance (36)
* **Chapter 2: Abstract Parallel Programming Model for HLS (39)**
    * Control and Data Driven Tasks (41)
    * Data-driven Task-level Parallelism (42)
    * Control-driven Task-level Parallelism (45)
    * Mixing Data-Driven and Control-Driven Models (61)
    * Summary (63)
* **Chapter 3: Loops Primer (65)**
    * Pipelining Loops (65)
    * Unrolling Loops (77)
    * Merging Loops (79)
    * Working with Nested Loops (81)
    * Working with Variable Loop Bounds (82)
* **Chapter 4: Arrays Primer (85)**
    * Mapping Software Arrays to Hardware Memory (85)
    * Array Accesses and Performance (86)
    * Arrays on the Interface (91)
    * Initializing and Resetting Arrays (95)
    * Implementing ROMs (97)
    * C Simulation with Arrays (98)
* **Chapter 5: Functions Primer (100)**
    * Function Inlining (100)
    * Function Pipelining (101)
    * Function Instantiation (102)
* **Chapter 6: Data Types (104)**
    * Standard Types (105)
    * Composite Data Types (110)
    * Arbitrary Precision (AP) Data Types (126)
    * Arbitrary Precision Floating-Point Library ap_float<int W, int E> (132)
    * Global Variables (136)
    * Pointers (137)
    * Vector Data Types (148)
    * Bit-Width Propagation (149)
* **Chapter 7: Unsupported C/C++ Constructs (151)**
    * System Calls (151)
    * Dynamic Memory Usage (152)
    * Pointer Limitations (154)
    * Recursive Functions (154)
    * Undefined Behaviors (155)
    * Virtual Functions and Pointers (156)
* **Chapter 8: Interfaces of the HLS Design (157)**
    * Defining Interfaces (157)
    * Vitis HLS Memory Layout Model (225)
    * Execution Modes of HLS Designs (236)
    * Controlling Initialization and Reset Behavior (254)
* **Chapter 9: Best Practices for Designing with M_AXI Interfaces (257)**
* **Chapter 10: Top-Level Performance Pragma (260)**
* **Chapter 11: Optimizing Techniques and Troubleshooting Tips (265)**
    * Understanding High-Level Synthesis Scheduling and Binding (267)
    * Optimizing Logic (274)
    * Optimizing AXI System Performance (276)
    * Managing Area and Hardware Resources (312)
    * Unrolling Loops in C++ Classes (317)
    * Limitations of Control-Driven Task-Level Parallelism (318)
    * Limitations of Pipelining with Static Variables (323)
    * Canonical Dataflow (324)

## Section III: Vitis HLS Flow Steps (330)
* **Chapter 12: Launching the Vitis Unified IDE (331)**
    * Features of the Vitis Unified IDE (333)
    * Using the Flow Navigator (334)
* **Chapter 13: Building and Running an HLS Component (336)**
    * Creating an HLS Component (337)
    * Defining the HLS Config File (364)
    * Running C Simulation (375)
    * Running C Synthesis (395)
    * Running C/RTL Co-Simulation (417)
    * Packaging the RTL Design (433)
    * Running Implementation (437)
    * Optimizing the HLS Project (443)
    * Component Comparison Feature (444)
    * L1 Library Wizard Flow (445)
* **Chapter 14: Creating HLS Components from the Command Line (449)**

## Section IV: Vitis HLS Command Reference (453)
* **Chapter 15: vitis, v++, and vitis-run Commands (454)**
    * hls_init.tcl (456)
* **Chapter 16: HLS Config File Commands (457)**
    * HLS General Options (458)
    * Array Partition Configuration (460)
    * C-Simulation Configuration (461)
    * Co-Simulation Configuration (462)
    * Compile Options (466)
    * Dataflow Configuration (468)
    * Debug Options (471)
    * Interface Configuration (471)
    * Package Options (476)
    * Operator Configuration (478)
    * RTL Configuration (481)
    * Schedule Setting (484)
    * Storage Configuration (484)
    * Implementation Configuration (485)
    * Unroll Setting (487)
    * HLS Optimization Directives (487)
* **Chapter 17: HLS Pragmas (541)**
* **Chapter 18: HLS Tcl Commands (608)**
    * Project Commands (608)
    * Configuration Commands (636)
    * Optimization Directives (658)

## Section V: Vitis HLS C Driver Reference (712)
* **Chapter 19: AXI4-Lite Slave C Driver Reference (713)**

## Section VI: Vitis HLS Libraries Reference (728)
* **Chapter 20: C/C++ Builtin Functions (729)**
* **Chapter 21: Arbitrary Precision Data Types Library (730)**
    * Using Arbitrary Precision Data Types (730)
    * C++ Arbitrary Precision Integer Types (733)
    * C++ Arbitrary Precision Fixed-Point Types (755)
* **Chapter 22: HLS Print Function (783)**
* **Chapter 23: HLS Math Library (785)**
* **Chapter 24: HLS Stream Library (796)**
* **Chapter 25: HLS Direct I/O (808)**
* **Chapter 26: HLS Fence Library (815)**
* **Chapter 27: HLS Vector Library (818)**
* **Chapter 28: HLS Task Library (821)**
* **Chapter 29: HLS Split/Merge Library (829)**
* **Chapter 30: HLS Stream of Blocks Library (834)**
* **Chapter 31: HLS IP Libraries (843)**
* **Chapter 32: Working with OpenCV (871)**

## Section VII: Vitis HLS Migration Guide (872)
* **Chapter 33: Migrating from Vitis HLS to the Vitis Unified IDE (873)**
* **Chapter 34: Migrating from Vivado HLS to Vitis HLS (875)**
    * Key Behavioral Differences (875)
* **Chapter 35: Deprecated and Unsupported Features (882)**
* **Chapter 36: Unsupported Features (887)**

## Appendices
* **Appendix A: Tcl to Config File Command Map (889)**
* **Appendix B: Instruction/Operator Explanation (898)**
* **Appendix C: Additional Resources and Legal Notices (900)**
    * Finding Additional Documentation (900)
    * Support Resources (901)
    * References (901)
    * Revision History (902)
    * Please Read: Important Legal Notices (903)