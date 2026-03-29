# Chapter 4: Using IP in Non-Project Mode

This chapter covers working with AMD IP in third-party synthesis flows and using Tcl commands for common IP operations in Non-Project Mode.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Third-Party Synthesis Flow](#third-party-synthesis-flow) | Recommended flow for third-party synthesis tools with AMD IP |
| [Tcl Commands for Common IP Operations](#tcl-commands-for-common-ip-operations) | Complete reference for IP Tcl commands in project and non-project modes |
| [Example IP Flow Commands](#example-ip-flow-commands) | Full Tcl script examples for common IP operations |

---

## Third-Party Synthesis Flow

When using Synopsys Synplify Pro or Mentor Graphics Precision netlist for synthesis with AMD IP, the recommended flow is:

1. Use the **Manage IP flow** to create and customize IP (including AMD XPMs)
2. Generate output products including the **synthesis design checkpoint (DCP)**
3. Add the stub file to the third-party synthesis project

### Stub Files for Black Box Inference

When the DCP is generated, stub files are created:

| File | Purpose |
|------|---------|
| `<ip_name>_stub.v` | Verilog stub — infers black box in third-party synthesis |
| `<ip_name>_stub.vhdl` | VHDL stub — infers black box in third-party synthesis |

The stub files contain synthesis directives that **prevent the third-party tool from inferring I/O buffers** for IP connected to top-level ports. You can modify these directives as needed.

> ⚠️ **Important:** AMD encrypts IP HDL files with IEEE Std P1735. IP HDL files are readable only with Vivado synthesis. Third-party tools can only be used for end-user logic, not for AMD IP synthesis. Behavioral simulation with encrypted RTL is supported for third-party simulation tools.

### Non-Project Mode Tcl Script (Third-Party Synthesis)

```tcl
# Set target part
set_part <part>
# Read the netlist from third-party synthesis tool
read_edif top.edif
# Read in the IP XCIs
read_ip ip1.xci
read_ip ip2.xci
# Read in top level constraints
read_xdc top.xdc
# Implement the design
link_design -top <top>
opt_design
place_design
phys_opt_design
route_design
write_bitstream -file <name>
```

> **Note:** When reading in the IP, use the XCI file from the location where output products were previously generated, or use `synth_ip` after reading the XCI.

### Project Mode Tcl Script (Third-Party Synthesis)

```tcl
# Create a project on disk
create_project <name> -part <part>
# Configure as a netlist project
set_property design_mode "GateLvl" [current_fileset]
set_property top <top> [current_fileset]
# Add in the netlist from third-party synthesis tool
add_files top.edif
# Add in XCI files for the IP
add_files {ip1.xci ip2.xci ip3.xci}
# Add in top level constraints
add_files top.xdc
# Launch implementation
launch_run impl_1 -to write_bitstream
```

### Using the XCI File (Not DCP Directly)

Always reference the **XCI file** when using AMD IP:

| Approach | Behavior |
|----------|----------|
| **XCI file (recommended)** | XDC output products applied after all netlists combined; Tcl scripts in IP XDC evaluated in context of end-user constraints |
| **DCP file (not recommended)** | Constraints resolved Out-Of-Context, without end-user context |

---

## Tcl Commands for Common IP Operations

### IP Tcl Commands in Design Flows

The following table lists IP Tcl commands in order of design use. Commands are generally consistent between Project and Non-Project modes.

| Action | Project Mode | Non-Project Mode |
|--------|-------------|-----------------|
| **Set part** | N/A (project setting) | `set_part <part>` |
| **Create IP** | `create_ip <ip_name>` | `create_ip <ip_name>` |
| **Upgrade IP** | `upgrade_ip <ip_name>` | `upgrade_ip <ip_name>` |
| **Configure IP** | `set_property CONFIG.<param> <val> [get_ips <name>]` | Same |
| **Set clock period** | IP Customization GUI (or Tcl) | `set_property CONFIG.<clk>.FREQ_HZ <#> [get_ips <name>]` |
| **Generate outputs** | `generate_target all [get_ips <name>]` | `generate_target all [get_ips <name>]` |
| **Synthesize IP (DCP)** | `create_ip_run [get_ips <name>]` then `launch_runs <name>_synth_1` | `synth_ip [get_ips <name>]` |
| **Read IP** | `import_files <name>.xci` (copy) or `add_files <name>.xci` (reference) | `add_files <name>.xci` or `read_ip <name>.xci` |
| **File queries** | `get_files -of_objects [get_ips <name>]` | Same |
| **IP Definition** | N/A | `report_property -all [get_ipdefs <IPVLNV>]` |
| **Write IP Tcl** | `write_ip_tcl <name>` | `write_ip_tcl <name>` |

> ⚠️ **Caution:** Do not use `upgrade_ip [get_ips -all]` — the `-all` option returns sub-core IP that may be removed during parent upgrade, leading to unreferenced Tcl objects.

> **Note (Non-Project):** Output products are **not generated automatically**. You must run `generate_target` or `synth_ip` (which generates targets automatically).

> ⚠️ **Important:** When using HLS IP in non-project mode, run the `compile_c` command prior to synthesis.

### Common Tcl Operations

```tcl
# Create a customization of the accumulator IP
create_ip -name c_accum -vendor amd.com -library ip -module_name c_accum_0

# Change customization parameters
set_property -dict [list CONFIG.Input_Width {10} CONFIG.Output_Width {10}] [get_ips c_accum_0]

# Generate selective output products
generate_target {synthesis instantiation_template simulation} [get_ips c_accum_0]

# Reset any output products generated
reset_target all [get_ips c_accum_0]

# List all properties of an IP
list_property [get_ips fifo_generator_0]

# List only CONFIG parameters (alphabetized)
lsearch -all -inline [list_property [get_ips fifo_generator_0]] CONFIG.*

# Full property report
report_property [get_ips fifo_generator_0]

# Remove a design run
delete_ip_run

# Export a simulation
export_simulation

# Extract files from a core container to disk
extract_files

# Write constraints to XDC
write_xdc <file>

# Write complete IP Tcl recreation script
write_ip_tcl
```

### Querying IP Customization Files

```tcl
# Get all files for an IP (e.g., for source control)
create_project -in_memory -part <part>
read_ip <ip_name>.xci
generate_target all [get_ips <ip_name>]
synth_ip [get_ips <ip_name>]
get_files -all -of_objects [get_files <ip_name>.xci]
```

### Querying an Ordered Source List

```tcl
# IP-only synthesis files
get_files -compile_order sources -used_in synthesis -of_objects [get_files <ip_name>.xci]

# IP-only simulation files
get_files -compile_order sources -used_in simulation -of_objects [get_files <ip_name>.xci]

# Top-level design including IP (synthesis)
get_files -compile_order sources -used_in synthesis

# Top-level design including IP (simulation)
get_files -compile_order sources -used_in simulation
```

> **Note:** Run `generate_target all [get_ips]` and `compile_c [get_ips]` before `synth_ip` for HLS IPs.

---

## Example IP Flow Commands

### Creating IP in Manage IP Project

```tcl
# Create a Manage IP project
create_project <managed_ip_project> ./managed_ip_project -part <part> -ip
set_property simulator_language Mixed [current_project]
set_property target_language Verilog [current_project]

# Create and customize IP
create_ip -name c_accum -vendor amd.com -library ip -module_name c_accum_0
set_property -dict {CONFIG.Input_Width 10 CONFIG.Output_Width 10} [get_ips c_accum_0]

# Synthesize IP
create_ip_run [get_ips c_accum_0]
launch_run c_accum_0_synth_1
```

### Implementing an IP Example Design

```tcl
create_project <name> <dir> -part <part>
create_ip ...
create_ip_run [get_ips <ip>.xci]
launch_runs <ip>_synth_1
wait_on_run <ip>_synth_1
open_example_project -force -dir <project_location> -in_process [get_ips <ip>]
launch_runs synth_1
wait_on_run synth_1
launch_runs impl_1
wait_on_run impl_1 -to write_bitstream
open_run impl_1
report_timing_summary ...
report_utilization ...
```

### Non-Project Synthesis with Mixed OOC and Global IP

```tcl
set_part <part>
read_verilog top.v

# IP with OOC DCP
read_ip ip1.xci
synth_ip [get_ips ip1]

# IP with global synthesis (no DCP)
read_ip ip2.xci
set_property generate_synth_checkpoint false [get_files ip2.xci]
generate_target all [get_ips ip2]

# Synthesize complete design
synth_design -top top
opt_design
place_design
route_design
write_bitstream -file top
```

### Simulating an IP Example Design

```tcl
create_project <name> <dir> -part <part>
create_ip ...
create_ip_run [get_ips <ip_name>]
launch_runs <ip>_synth_1
wait_on_run <ip>_synth_1
open_example_project -force -dir <project_location> -in_process [get_ips <ip>]
launch_simulation
```

---

## Best Practices

1. **Always reference the XCI file**, not the DCP directly, for proper constraint resolution
2. **Use `write_ip_tcl`** to create portable IP recreation scripts for revision control
3. **Run `compile_c` before synthesis** for HLS IP in non-project mode
4. **Generate output products before sharing** IP with team members
5. **Use project-based flows** when possible — AMD recommends them over non-project flows
6. **Avoid `upgrade_ip [get_ips -all]`** — use explicit IP names to prevent sub-core issues
7. **Use absolute paths** when associating files with Tcl commands

---

## Quick Reference

| Task | Command |
|------|---------|
| Create IP | `create_ip -name <ip> -vendor amd.com -library ip -module_name <name>` |
| Configure IP | `set_property -dict {CONFIG.Param1 val1 CONFIG.Param2 val2} [get_ips <name>]` |
| Generate outputs | `generate_target all [get_ips <name>]` |
| Synthesize IP | `synth_ip [get_ips <name>]` (non-project) |
| Query files | `get_files -of_objects [get_ips <name>]` |
| List CONFIG params | `lsearch -all -inline [list_property [get_ips <name>]] CONFIG.*` |
| Write IP script | `write_ip_tcl <name>` |
| Read IP | `read_ip <name>.xci` |

---

## See Also

- [Chapter 2: IP Basics](chapter2_ip_basics.md) — IP customization, output products, synthesis options
- [Chapter 3: Using Manage IP Projects](chapter3_using_manage_ip_projects.md) — Manage IP flow
- Vivado Design Suite User Guide: Using Tcl Scripting (UG894)
- Vivado Design Suite Tcl Command Reference Guide (UG835)
- Vivado Design Suite Tutorial: Designing with IP (UG939)

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Chapters:** 5 — Using AMD IP with Third-Party Synthesis Tools / 6 — Tcl Commands for Common IP Operations
- **Pages:** 79–90
