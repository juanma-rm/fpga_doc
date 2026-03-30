# Appendix C: High-Level Synthesis IP

This appendix covers IP file and directory structure, output products, associated file types, and COE file usage.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [IP-Generated Directories and Files](#ip-generated-directories-and-files) | Output products created when IP is customized |
| [Files Associated with IP](#files-associated-with-ip) | Additional file types used by IP (COE, MIF, BMM, etc.) |
| [Using a COE File](#using-a-coe-file) | Coefficient file syntax, keywords, and examples |
| [MIF File Description](#mif-file-description) | Memory initialization file format |

---

## IP-Generated Directories and Files

When customizing IP, the Vivado IDE creates a unique directory for each IP:

- **RTL projects:** IP sources in `<project_name>.srcs`, output products in `<project_name>.gen`
- **Managed IP flow:** All files in a directory parallel to the Managed IP project location

> **Tip:** Use Tcl commands (`get_files`) to access IP files rather than navigating the directory structure directly.

### Output Products

| Directory/File | Description |
|---------------|-------------|
| `/doc` | Contains `<core_name>_changelog.txt` |
| `/sim` | Simulation source files (not present for all IP) |
| `/synth` | Synthesizable source files (not present for simulation-only IP) |
| `<ip_name>.xci` | IP customization file — use this to generate outputs and upgrade |
| `<ip_name>.xcix` | Core Container file listing common elements between IP |
| `<ip_name>.xml` | IP Bill of Material (BOM) — tracks state, parameters, interfaces |
| `<ip_name>.veo` / `.vho` | Verilog / VHDL instantiation template |
| `<ip_name>.dcp` | Synthesized Design Checkpoint (netlist + processed XDC constraints) |
| `<ip_name>_stub.v` / `_stub.vhdl` | Black box stubs for third-party synthesis tools |
| `<ip_name>_funcsim.v` / `.vhdl` | Post-synthesis structural simulation netlist (pre-2015.3) |
| `<ip_name>_sim_netlist` | Post-synthesis structural simulation netlist (2015.3+) |
| `<ip_name>.xdc` | Timing and/or physical constraints |
| `<ip_name>_in_context.xdc` | In-context constraints (see Setting the Target Clock Period) |
| `<ip_name>_clocks.xdc` | Constraints with clock dependency |
| `<ip_name>_board.xdc` | Constraints for platform board flow |
| `<ip_name>_ooc.xdc` | Default clock definitions for OOC synthesis |
| Encrypted HDL | Files for synthesizing and simulating IP |

> **Note:** DCP, `_stub`, and `_sim_netlist` files are created only when using the **Out-of-Context flow** for synthesis (default).

> ⚠️ **Important:** Always reference the **XCI file**, not the DCP directly. The XCI brings in the DCP when needed and ensures proper constraint scoping.

---

## Files Associated with IP

| File Type | Description |
|-----------|-------------|
| `.coe` | Coefficient file — ASCII text with radix header and data vectors |
| `.mif` | Memory Initialization File — binary data translated from COE |
| `.bmm` | Block Memory Manager file |
| `.csv` | Comma-separated spreadsheet file |
| `.elf` | Executable and Linkable Format file (MicroBlaze processor) |

> **Note:** Only some IP use these files. Add them as project sources. Configuration properties for these files are available in the IP customization GUI.

---

## Using a COE File

A **COE (COEfficient) file** is an ASCII text file with a radix header followed by data vectors. The radix can be 2, 10, or 16. Each vector must be terminated by a semicolon.

The Vivado tool reads the COE file and writes MIF files when the core is generated. Behavioral simulation models rely on these MIF files.

> ⚠️ **Important:** Upgrade all IP prior to adding a COE file. Locate the COE file in the same directory as the XCI file.

> **Note:** If a COE file is no longer used by an IP, remove it. Old COE files can cause duplicate data in synthesis or errors if removed from disk but still referenced in the project.

### COE File Syntax

```
Keyword=Value ; Optional Comment
<Radix_Keyword>=Value ; Optional Comment
<Data_Keyword>=Data_Value1, Data_Value2, Data_Value3;
```

Any text after a semicolon is treated as a comment and ignored.

### Radix Keywords

| Keyword | Description |
|---------|-------------|
| `RADIX` | Used for non-memory cores to specify the coefficient radix |
| `MEMORY_INITIALIZATION_RADIX` | Used for memory initialization values |

### Data Keywords

| Keyword | Description |
|---------|-------------|
| `COEFDATA` | Filter coefficients (must be last keyword in file) |
| `MEMORY_INITIALIZATION_VECTOR` | Block and distributed memory data (must be last keyword) |
| `PATTERN` | Bit Correlator COE files |
| `BRANCH_LENGTH_VECTOR` | Interleaver COE files |

### COE File Examples

**Bit Correlator (hex, 19 taps):**
```
radix = 16;
pattern = 3 0 3 1 0 1 1 3 0 2 2 2 3 0 1 1 3 0 3;
```

**Dual Port Block Memory (binary, depth=16, width=4):**
```
memory_initialization_radix=2;
memory_initialization_vector=
1111, 1111, 1111, 1111, 1111, 0000, 0101, 0011,
0000, 1111, 1111, 1111, 1111, 1111, 1111, 1111;
```

**Single Port Block Memory (hex, depth=16, width=8):**
```
memory_initialization_radix=16;
memory_initialization_vector=
ff, ab, f0, 11, 11, 00, 01, aa,
bb, cc, dd, ef, ee, ff, 00, ff;
```

**Distributed Arithmetic FIR Filter (hex, 8 taps, 12-bit coefficients):**
```
Radix = 16;
CoefData= 346, EDA, 0D6, F91, F91, 0D6, EDA, 346;
```

---

## MIF File Description

The COE file is a high-level method for specifying initial memory contents. When the core is generated, Vivado converts the COE into a **MIF (Memory Initialization File)** containing binary data.

- One line of text per memory location
- First line = address 0, second line = address 1, etc.
- Each line contains the initialization value (MSB first) in binary format
- Exactly one binary digit per bit of memory width

> **Note:** For HDL simulations, the MIF file must reside in the simulation directory.

---

## See Also

- [Chapter 2: IP Basics](chapter02_ip_basics.md) — IP output products, customization
- [Chapter 4: Using IP in Non-Project Mode](chapter04_using_ip_in_non-project_mode.md) — Tcl commands for generating outputs

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Appendix:** C — High-Level Synthesis IP (Source Appendix B: IP Files and Directory Structure)
- **Pages:** 95–101
