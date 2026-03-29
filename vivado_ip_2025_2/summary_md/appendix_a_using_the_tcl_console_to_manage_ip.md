# Appendix A: Using the Tcl Console to Manage IP

This appendix provides a Tcl-based workflow for managing IP from the Vivado Tcl console, including scripting examples for source control integration.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Tcl Commands for IP](#tcl-commands-for-ip) | Summary of essential IP management commands |
| [Tcl Script Example](#tcl-script-example) | End-to-end IP management script for source control |

---

## Tcl Commands for IP

The Vivado IP catalog is fully accessible from the Tcl console. Every action performed in the GUI echoes an equivalent Tcl command in `vivado.log`, enabling full scripting capability.

### Key Commands

| Command | Purpose |
|---------|---------|
| `create_ip` | Create a new IP customization |
| `set_property CONFIG.<param> <value> [get_ips <name>]` | Configure IP parameters |
| `generate_target all [get_ips <name>]` | Generate output products |
| `synth_ip [get_ips <name>]` | Synthesize IP to create OOC DCP |
| `get_files -all -of_objects [get_files <name>.xci]` | Query all files associated with an IP |
| `get_files -compile_order sources -used_in synthesis` | Get ordered source list for synthesis |
| `get_files -compile_order sources -used_in simulation` | Get ordered source list for simulation |
| `report_property [get_ips <name>]` | Report all IP properties |
| `list_property [get_ips <name>]` | List all property names |
| `write_ip_tcl` | Export Tcl script to recreate IP |
| `reset_target all [get_ips <name>]` | Reset generated output products |
| `delete_ip_run` | Remove a design run |
| `export_simulation` | Export simulation scripts |
| `extract_files` | Extract files from core container |

For the full Tcl command reference: `help -category IPFlow` in the Tcl Console.

---

## Tcl Script Example

### Complete IP Creation and Source Control Script

```tcl
# Create a project in memory (no project directory on disk)
create_project -in_memory -part <part>

# Read an IP customization
read_ip <ip_name>.xci

# Generate all output products
generate_target all [get_ips <ip_name>]

# Create a DCP for the IP
synth_ip [get_ips <ip_name>]

# Query all files for source control
get_files -all -of_objects [get_files <ip_name>.xci]
```

> **Note:** For HLS IPs, run `generate_target all [get_ips]` and `compile_c [get_ips]` before `synth_ip`.

---

## See Also

- [Chapter 4: Using IP in Non-Project Mode](chapter4_using_ip_in_non-project_mode.md) — Full Tcl command reference table and scripting examples
- Vivado Design Suite User Guide: Using Tcl Scripting (UG894)
- Vivado Design Suite Tcl Command Reference Guide (UG835)

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Appendix:** A — Using the Tcl Console to Manage IP
- **Pages:** 90–92
