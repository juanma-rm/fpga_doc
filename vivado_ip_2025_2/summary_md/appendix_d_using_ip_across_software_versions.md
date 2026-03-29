# Appendix D: Using IP Across Software Versions

This appendix covers the Platform Board Flow for IP and editing or overriding IP sources, including constraint management for customized IP.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Platform Board Flow for IP](#platform-board-flow-for-ip) | Using board interfaces to automate IP pin assignments |
| [Editing or Overriding IP Sources](#editing-or-overriding-ip-sources) | Modifying IP HDL and XDC files safely |
| [Overriding IP Constraints](#overriding-ip-constraints) | Techniques for changing IP-delivered XDC constraints |
| [Editing IP Sources](#editing-ip-sources) | Setting IS_MANAGED property and re-synthesizing |
| [Editing Subsystem IP](#editing-subsystem-ip) | Special handling for complex subsystem IP |

---

## Platform Board Flow for IP

The Platform Board Flow automates creation of **physical constraints** (pin assignments, IOSTANDARDs) when customizing IP for a specific board.

### Enabling the Board Flow

1. When creating a new project, select a **board** as the default part
2. IP supporting the board flow shows a **Board tab** in the customization dialog
3. Associate IP interfaces with board interfaces (USB, LED, buttons, switches, etc.)

### Generated Constraints

When output products are generated, an `<IP_Name>_board.xdc` file is created containing:
- Pin assignments (`PACKAGE_PIN`) mapping IP ports to physical board connectors
- IOSTANDARD constraints matching the board's voltage levels

### Usage Example

For a GPIO IP on a board:
1. Connect `GPIO` interface → `led8bits` board interface
2. Connect `GPIO2` interface → `Custom` board interface
3. Generate output products → `<IP_Name>_board.xdc` contains all pin assignments

### See Also

- Using the Platform Board Flow in IP Integrator (UG994)
- Board File Linter section in System-Level Design Entry (UG895)

---

## Editing or Overriding IP Sources

At times, you may need to modify unencrypted IP source files (XDC or HDL). This should be done **only if absolutely necessary** — modifying IP sources could result in the IP not functioning correctly.

> ⚠️ **Important:** Do not directly modify IP sources on disk without following the guidelines in this appendix. Direct modifications may be removed when IP is reset or regenerated.

> ⚠️ **Important:** Disable the Core Container feature before editing IP sources.

---

## Overriding IP Constraints

IP are validated with their delivered constraints. To change an IP-delivered constraint (e.g., `LOC` or `PACKAGE_PIN`):

### Method 1: Override at Top-Level (Preferred for Physical Constraints)

Create a new XDC or Tcl file with replacement constraints, using **scoped properties** to match the IP's constraint scope.

#### Finding Scope Properties

```tcl
report_compile_order -constraints
# Look for SCOPED_TO_REF and SCOPED_TO_CELLS values
```

- `SCOPED_TO_REF` — typically the IP customization name
- `SCOPED_TO_CELLS` — typically `inst` (Verilog) or `U0` (VHDL)

#### Procedure

```tcl
# 1. Create a new XDC/Tcl file and add to constraint set
# 2. Place override commands in the new file
# 3. Set scope properties
set_property SCOPED_TO_REF <REF> [get_files <new_file.xdc>]
set_property SCOPED_TO_CELLS <CELL> [get_files <new_file.xdc>]
# 4. Mark for implementation only
set_property USED_IN IMPLEMENTATION [get_files <new_file.xdc>]
```

> **Note:** Physical constraints should be overridden during **implementation stage only** (ignored during OOC synthesis). Use `USED_IN IMPLEMENTATION` property.

### Method 2: Edit IP Source Directly

See [Editing IP Sources](#editing-ip-sources) below. Required when timing constraints have higher XDC precedence (e.g., `set_false_path` overrides `set_max_delay`).

### XDC vs. Tcl Files

| Use Case | File Type |
|----------|-----------|
| Standard XDC commands | `.xdc` file |
| Commands like `reset_property` (not valid in XDC) | `.tcl` file |
| Clearing and re-setting a LOC on BUFG_GT | `.tcl` file (requires `reset_property` first) |

> ⚠️ **Strongly recommended:** Do not modify IP timing constraints, except potentially `_ooc.xdc` specifically to set target frequency for OOC synthesis.

---

## Editing IP Sources

### Procedure

1. **Customize the IP** and generate all output products (including DCP)
2. **Set IS_MANAGED to false:**
   ```tcl
   set_property IS_MANAGED false [get_files <IP_Name>.xci]
   ```
3. The `IS_LOCKED` property becomes `TRUE` — the IP icon changes to show user-managed state
4. **Edit the required files** (non-encrypted HDL or XDC)
5. **Re-create output products:**
   ```tcl
   # Reset the OOC run
   reset_run <ip_name>_synth_1
   # Re-launch synthesis
   launch_run <ip_name>_synth_1
   ```

> ⚠️ **Caution:** Once `IS_MANAGED` is set to `false`, you **cannot switch it back to `true`** — there is high risk of edited sources being overwritten.

### After Editing

By referencing the XCI file (recommended), you have access to:
- IP source files for simulation
- DCP for synthesis of the top-level file and implementation

---

## Editing Subsystem IP

Some complex subsystem IP (7 series and UltraScale families) do not allow the `IS_MANAGED` property to be changed directly.

> ⚠️ **Caution:** Editing RTL files of such IP risks invalidating connectivity to sub-cores. Consider changes carefully.

### Procedure

1. Ensure IP is fully generated using **OOC per IP** synthesis option
2. Set `IS_LOCKED` property to `true` (since `IS_MANAGED` cannot be changed)
3. Edit the required RTL file on disk using an external editor
4. Re-synthesize:
   ```tcl
   reset_run <ip_name>_synth_1
   launch_run <ip_name>_synth_1
   ```

> **Note:** Because subsystem IP does not allow changing `IS_MANAGED`, there is no visual indication of modifications. Track modified IP manually.

---

## Best Practices

1. **Override rather than edit** IP constraints when possible — use top-level XDC/Tcl files
2. **Use SCOPED_TO_REF/CELLS** for targeted constraint overrides
3. **Mark override files as implementation-only** (`USED_IN IMPLEMENTATION`)
4. **Never modify IP timing constraints** except the `_ooc.xdc` frequency target
5. **Disable Core Container** before editing IP sources
6. **Track user-managed IP manually** — setting `IS_MANAGED false` is irreversible

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Appendices:** C — Using the Platform Board Flow for IP / D — Editing or Overriding IP Sources
- **Pages:** 102–112
