# Chapter 2: IP Basics

This chapter describes the features of Designing with IP in the Vivado Design Suite, covering IP project settings, the IP catalog, IP customization, output product generation, instantiation, simulation, upgrading, multi-level IP, debug IP, and the core container feature.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Using IP Project Settings](#using-ip-project-settings) | IP-specific project settings: core containers, simulation, upgrade log, default location, IP cache |
| [Using the IP Catalog](#using-the-ip-catalog) | Browsing, filtering, and searching the IP catalog; versioning, licensing, Alliance Partner IP |
| [Creating an IP Customization](#creating-an-ip-customization) | Customizing IP via GUI and Tcl; generating output products |
| [Instantiating an IP](#instantiating-an-ip) | Using instantiation templates; reporting IP status |
| [Designing with System Verilog](#designing-with-system-verilog) | SV wrapper support for BD and XCI; `.sveo` templates; SV XPMs |
| [Understanding IP States Within a Project](#understanding-ip-states-within-a-project) | IP state icons and their meaning |
| [Managing IP Constraints](#managing-ip-constraints) | XDC constraint processing order; `dont_touch.xdc`; `in_context.xdc` |
| [Setting the Target Clock Period](#setting-the-target-clock-period) | OOC clock period configuration via GUI and Tcl |
| [Synthesis Options for IP](#synthesis-options-for-ip) | Global Synthesis vs. Out-of-Context (OOC) flow |
| [Simulating IP](#simulating-ip) | Simulation models, simulator language settings, test benches, Verification IP |
| [Upgrading IP](#upgrading-ip) | Upgrading IP across Vivado releases; selective upgrade; Tcl commands |
| [Understanding Multi-Level IP](#understanding-multi-level-ip) | Sub-core, static, dynamic, and subsystem IP parent-child relationships |
| [Working with Debug IP](#working-with-debug-ip) | ILA, VIO, IBERT, JTAG-to-AXI; debugging flows |
| [Using a Core Container](#using-a-core-container) | XCIX single-file IP representation; simulation and support files |

---

## Using IP Project Settings

IP-specific settings are configured via **Settings → IP** in the Vivado IDE. Available when working with an RTL project or Manage IP project.

### IP Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Core Containers** | Use XCIX single-file format for IP and output products | Disabled |
| **Simulation — Use Precompiled IP** | Reference precompiled libraries for AMD IP static files | Enabled |
| **Simulation — Auto Generate Scripts** | Generate simulation scripts per IP in `<project>.ip_user_files` | Enabled |
| **Upgrade IP — Generate Log File** | Create `ip_upgrade.log` when upgrading IP | Enabled |
| **Default IP Location** | Where to store IP sources | `<project>.srcs/sources_1/ip/` |
| **IP Cache** | Cache OOC synthesis results to avoid re-synthesis | Local (enabled) |

> Output products are always generated to `<project_name>.gen/` — separate from sources in `<project_name>.srcs/`.

### IP Cache

The IP Cache speeds up OOC synthesis by caching synthesis results. When a new IP customization matches an existing cache entry (identical customization, same part and language), the cached DCP is reused instead of re-running synthesis.

| Cache Option | Description |
|-------------|-------------|
| **Disabled** | No caching |
| **Local** (default) | Cache in `<project_name>.ip_cache/`; location not changeable |
| **Remote** | User-specified directory; enables shared team caching |

#### Configuring Cache Defaults via `Vivado_init.tcl`

```tcl
# Disable IP cache for all new projects
set_param project.defaultIPCacheSetting none

# Set remote cache location (Linux)
set_param project.defaultIPCacheSetting /wrk/staff/smith/ip_cache/

# Set remote cache location (Windows)
set_param project.defaultIPCacheSetting c:/<project_dir>/ip_cache/
```

#### Managing the Cache

```tcl
# Clear the cache
config_ip_cache -clear_output_repo

# Zip cache entries for distribution as read-only repository
config_ip_cache -zip_cache
```

> ⚠️ **Important:** The Non-Project flow does not support IP Caching.

> **Caution:** IP Cache can grow large depending on the number of IP present.

### IP Repository Management

Manage IP repositories via **Settings → IP → Repository**:

- **Add** — Specify location of IP definitions (hierarchical search)
- **Remove** — Remove a repository listing
- **Reorder** — Change search order with up/down arrows

```tcl
# Alternative: add repository directly via right-click menu in IP catalog
```

### See Also

- [Chapter 1: IP-Centric Design Flow](chapter1_ip-centric_design_flow.md)
- Vivado Design Suite User Guide: Using Tcl Scripting (UG894)
- Vivado Design Suite User Guide: Creating and Packaging Custom IP (UG1118)

---

## Using the IP Catalog

The Vivado IP catalog provides access to AMD IP, Alliance Partner IP, and user repositories.

### Key Features

- Consistent access to AMD IP (building blocks, wizards, connectivity, DSP, embedded, AXI, video)
- Multiple repository support including shared network drives
- On-demand delivery of output products (instantiation templates, simulation models)
- IP example designs for evaluation
- Version history via Change Log

### IP Catalog Views

| View | Contents |
|------|----------|
| **Cores** | IP from AMD, Alliance Partners, and customer repositories |
| **Interfaces** | Available interfaces categorized by Vivado Repository packaging |

### IP Versioning

| Change Level | User Action | Examples |
|-------------|-------------|----------|
| **Revision** | No need to react | New device support, cosmetic GUI changes, bug fixes for unusable configs |
| **Minor** | May need to react | Reduction in parameter range, removed optional port, added optional register |
| **Major** | Will need to react | Added/renamed/removed non-optional ports, interface standard change, behavior changes |

### Filtering and Searching

- Filter by: Supported Output Products, Supported Interfaces, Licensing, Provider, Status
- Group by: Taxonomy or Repository
- Text search matches IP names and folder names

### Querying IP Properties via Tcl

```tcl
# List all properties for an IP definition
report_property -all [get_ipdefs <IP_VLNV>]

# Example: FIFO Generator
report_property -all [get_ipdefs amd.com:ip:fifo_generator:13.1]

# Query specific property
get_property supported_families [get_ipdefs amd.com:ip:fifo_generator:13.1]
```

### Alliance Partner IP

Alliance Partner IP is shown with a blue disk icon. When selected, a dialog provides a purchase link. Customization is disabled until the IP is purchased and installed.

### Fee-Based Licensed IP

| License Status | Description |
|---------------|-------------|
| **Included** | AMD End User License Agreement — no additional charge |
| **Purchase** | Core License Agreement — fee-based AMD LogiCORE IP |
| **Full** | Purchased license |
| **Simulation** | Simulation-only license |
| **Eval** | Evaluation license |

| License Type | Description |
|-------------|-------------|
| **Floating** | Locked to license server; checked out per unique user |
| **Node-Locked** | Locked to specific machine or dongle |

> ⚠️ **Important:** During implementation, Vivado confirms that a license exists for the IP. You must regenerate LogiCORE IP for the core netlist to receive the current license status.

### See Also

- AMD IP Versioning page
- Vivado Design Suite User Guide: Release Notes, Installation, and Licensing (UG973)

---

## Creating an IP Customization

### Via GUI

1. Double-click IP in the catalog (or right-click → Customize IP)
2. Configure parameters in the Customize IP dialog
3. Set **IP Location** if storing outside default project directory
4. Click **OK**

> ⚠️ **Caution (Windows):** The OS has a 260-character path length limit. Use short names and directory locations.

### Via Tcl

```tcl
# Create an IP customization
create_ip -name fifo_generator -version 12.0 -vendor amd.com -library ip \
  -module_name fifo_gen

# Set IP properties
set_property CONFIG.Input_Data_Width 12 [get_ips fifo_gen]

# Report all CONFIG properties
report_property CONFIG.* [get_ips <ip_name>]

# Check if property is default or user-set
get_property CONFIG.Read_Data_Count_Width.value_src [get_ips char_fifo]
# Returns: "default" or "user"
```

> **Note:** `create_ip` creates the XCI file and instantiation template but does not generate other output products.

### Generating Output Products

After customization, the **Generate Output Products** dialog lists deliverable products. Options:

| Option | Description |
|--------|-------------|
| **Global Synthesis** | Top-down synthesis; removes all OOC run files |
| **Out-of-Context Settings** | Add OOC settings description |
| **Number of Jobs** | Max parallel OOC synthesis runs (default: 1) |

#### Default Output Products (OOC flow)

- Synthesized DCP
- Structural simulation netlist (`<ip_name>_sim_netlist.v` / `.vhdl`)
- Stub files (`*_stub.v` / `*_stub.vhdl`)
- Instantiation templates (`.veo`, `.vho`)
- XDC constraints
- Change log

```tcl
# Reset and regenerate output products
reset_target all [get_files <path>/<core_name>.xci]
generate_target all [get_files <path>/<core_name>.xci]

# Disable OOC DCP generation
set_property GENERATE_SYNTH_CHECKPOINT FALSE [get_ips <ip_name>]
```

### Adding Existing IP

```tcl
# Import IP (copies into project)
import_files <ip_filename>

# Reference IP remotely
read_ip <ip_filename>

# Create design runs for added IP
create_ip_run -force [get_ips <ip_name>]
```

> ⚠️ **Important:** NGC format files are not supported for AMD UltraScale devices. Use `NGC2EDIF` or regenerate the IP.

### Copying IP

```tcl
copy_ip -name newFIFO [get_ips char_fifo]
```

### Re-Customizing Existing IP

Double-click the IP or right-click → **Re-customize IP** in IP Sources. Changed output products are reset and regenerated automatically.

### See Also

- [Chapter 3: Using Manage IP Projects](chapter3_using_manage_ip_projects.md)
- [Appendix A: Using the Tcl Console to Manage IP](appendix_a_using_the_tcl_console_to_manage_ip.md)

---

## Instantiating an IP

### Using Instantiation Templates

1. Open the instantiation template (`.veo` for Verilog, `.vho` for VHDL) from IP Sources
2. Copy the template section between the indicated comments
3. Paste into your design HDL file
4. Edit port connections and provide a unique instance name

### Reporting IP Status

```tcl
report_ip_status
```

Filterable by: Major change, Minor change, Revision change, Part change, Up-to-date, Other (definition not found, read-only, user-managed, disabled, incompatible license, deprecated).

### Viewing Change Logs

- IP Sources → right-click IP → IP Documentation → **View Change Log**
- Source File Properties → scroll → **View Change Log**

---

## Designing with System Verilog

**New in Vivado 2025.2:** System Verilog wrapper support for BD and `.xci` files.

### Create HDL Wrapper Dialog

| Checkbox State | Behavior |
|---------------|----------|
| **Checked** (use as Top Module) | Defaults to target language from Project Settings |
| **Unchecked** | Manual selection: System Verilog, Verilog, or VHDL |

> **Note:** System Verilog cannot be used as the Top-level wrapper.

### Tcl Commands

```tcl
# Generate SV wrapper for BD
make_wrapper -language system_verilog -inst_template [get_files my_bd.bd]

# Generate SV wrapper for XCI (import into project)
make_wrapper [get_files my_ip.xci] -language systemverilog -import

# Generate SV wrapper for XCI (add reference)
make_wrapper [get_files my_ip.xci] -language systemverilog -add
```

### `.sveo` Instantiation Templates

Auto-generated System Verilog instantiation templates located at: `<project>.gen/sources_1/ip/<ip_name>/<ip_name>_sv.sveo`

### System Verilog XPMs

Available under **Tools → Language Templates → System Verilog → XPMs**:

| XPM Category | Templates |
|-------------|-----------|
| `xpm_fifo` | `xpm_fifo_axil_sv`, `xpm_fifo_axif_sv`, `xpm_fifo_axis_sv` |
| `xpm_noc` | `xpm_nmu_strm_sv`, `xpm_nsu_strm_sv`, `xpm_nmu_mm_sv`, `xpm_nsu_mm_sv` |

---

## Understanding IP States Within a Project

| Icon | State | Description |
|------|-------|-------------|
| OOC | Out-of-Context | IP in RTL project to be synthesized OOC |
| Global | Global Synthesis | IP to be synthesized with the project |
| Unmanaged | Unmanaged | `IS_MANAGED` set to false; user owns HDL/constraints; IP becomes locked |
| Locked (with outputs) | Locked | Cannot recustomize/regenerate, but usable in flow |
| Locked (no outputs) | Locked/Unusable | Must provide original outputs or upgrade to latest version |

> ⚠️ **Important:** Imported IP with versions not accessible from the IP catalog cannot be re-customized, reset, or regenerated.

---

## Managing IP Constraints

The Vivado IDE manages XDC timing and physical constraints for AMD IP.

### Constraint File Processing Order

| Order | Constraint Source |
|-------|------------------|
| 1 | User XDC set to `EARLY` |
| 2 | IP XDC set to `EARLY` (default for IP) |
| 3 | User XDC set to `NORMAL` (default for user) |
| 4 | IP XDC set to `LATE` |
| 5 | User XDC set to `LATE` |

### IP Constraint Files

| File | Purpose | When Used |
|------|---------|-----------|
| `<ip_name>.xdc` | Core constraints (clock creation, no external dependencies) | Synthesis & Implementation |
| `<ip_name>_clocks.xdc` | Clock-dependent constraints (processed after user XDC) | Implementation |
| `<ip_name>_ooc.xdc` | Default clock definitions for OOC synthesis | OOC synthesis only |
| `<ip_name>_in_context.xdc` | Clock definitions on IP boundary for top-level synthesis | Top-level synthesis (OOC flow) |
| `<ip_name>_board.xdc` | PACKAGE_PIN, IOSTANDARD from board flow | When using platform board |
| `dont_touch.xdc` | Sets `DONT_TOUCH` on IP top-level ports | Synthesis |

```tcl
# Report constraint compile order
report_compile_order -constraints

# Change IP synthesis run properties
set_property STEPS.SYNTH.DESIGN.ARGS.FSM_EXTRACTION sequential [get_runs <ip_name>_synth_1]
```

> ⚠️ **Caution:** If IP is synthesized OOC, top-level synthesis cannot reference internal IP objects (pins, nets, cells). These are resolved during implementation.

### Referencing IP-Created Clocks

```tcl
# Reference clock produced by an IP indirectly via pin
get_clocks -of_objects [get_pins <IP_clock_pin>]
```

### See Also

- Vivado Design Suite User Guide: Using Constraints (UG903)
- Vivado Design Suite User Guide: Creating and Packaging Custom IP (UG1118)

---

## Setting the Target Clock Period

By default, IP synthesized OOC uses a default clock period defined in `<ip_name>_ooc.xdc`. You can customize this.

### Clock Configuration Options

- IP GUI: Frequency/period settings or Clocks tab
- Tcl: Set `FREQ_HZ` properties on clock ports

### Example: Setting Target Clock via Tcl

```tcl
# 1. Find available FREQ_HZ properties
report_property [get_ips char_fifo]
# Properties ending in FREQ_HZ:
#   CONFIG.core_clk.FREQ_HZ (common clock)
#   CONFIG.read_clk.FREQ_HZ (independent clocks)
#   CONFIG.write_clk.FREQ_HZ (independent clocks)
#   CONFIG.slave_aclk.FREQ_HZ (AXI)
#   CONFIG.master_aclk.FREQ_HZ (AXI)

# 2. Set desired frequency (250 MHz)
set_property CONFIG.core_clk.FREQ_HZ 250000000 [get_ips char_fifo]

# 3. Generate IP → _ooc.xdc now contains:
#    create_clock -period 4 -name clk [get_ports clk]
```

### Clocking Diagnostics

```tcl
# Find unconstrained clocks
report_clock_networks

# Report all clocks in the design
report_clocks

# Show constraint processing order
report_compile_order -constraints
```

### See Also

- Vivado Design Suite User Guide: Using Constraints (UG903)

---

## Synthesis Options for IP

### Global Synthesis Flow

Synthesizes IP RTL with the top-level design. Any user HDL change causes IP re-synthesis.

```tcl
# Disable OOC (enable global synthesis)
set_property GENERATE_SYNTH_CHECKPOINT FALSE [get_ips <ip_name>]
```

### Out-of-Context (OOC) Flow (Default, Recommended)

Synthesizes IP standalone, producing:
- OOC DCP (netlist + constraints container)
- HDL stub module (black box for top-level synthesis)
- `_in_context.xdc` (clock definitions for top-level)
- `_ooc.xdc` (default clock definitions for IP synthesis)
- Structural simulation netlists

| Benefit | Description |
|---------|-------------|
| **Faster synthesis** | IP only re-synthesized when customization or version changes |
| **Simulation netlist** | Produces `_sim_netlist.v`/`.vhdl` for single-language simulators |

> Always reference IP using the **XCI file**, not the DCP alone.

---

## Simulating IP

### Simulation Models

| Model Type | Description |
|-----------|-------------|
| Custom behavioral | IP-specific behavioral model |
| Synthesizable RTL | Plain text or encrypted RTL for simulation |
| Structural netlist | Generated from DCP (`_sim_netlist.v`/`.vhdl`) |
| C model | C-based simulation model |

### Simulator Language Setting

```tcl
set_property SIMULATOR_LANGUAGE <Mixed|Verilog|VHDL> [current_project]
```

| IP Delivers | Language Setting | Simulation Model Used |
|------------|-----------------|----------------------|
| VHDL + Verilog | Mixed | Behavioral in specified language |
| Verilog only | VHDL | Structural netlist from DCP |
| VHDL only | Verilog | Structural netlist from DCP |
| No behavioral | Any | Structural netlist from DCP |

### Using IP Test Benches

Some IP deliver test benches (`tb_<ip_name>`). To use:

1. Expand IP hierarchy in Simulation Sources
2. Select `tb_<ip_name>`, right-click → **Set as Top**
3. **Run Simulation** from Flow Navigator

### Verification IP

```tcl
# Insert VIP on a block design interface
set_property CONFIG.INSERT_VIP 1 [get_bd_intf_pin <path_to_interface>]

# Insert VIP on an IP interface
set_property CONFIG.<interface_name>.INSERT_VIP 1 [get_ips <ipname>]
```

> ⚠️ **Important:** AXI Verification IP is written in SystemVerilog with randomization. Check UG973 for third-party simulator compatibility.

### See Also

- Vivado Design Suite User Guide: Logic Simulation (UG900)
- AXI Verification IP Product Guide (PG267)

---

## Upgrading IP

Each Vivado release delivers one version of each IP. IP from previous releases become **locked** and must be upgraded.

> ⚠️ **Caution:** Upgrading removes all previously generated output products including DCPs and design runs. Archive your project first.

### Pre-Upgrade Checklist

1. Generate all output products (including DCPs) before moving to a new release
2. Copy Manage IP project locations as backup
3. Archive design projects containing IP
4. Review `report_ip_status` for change information

### Upgrade via GUI

1. **Reports → Report IP Status** → opens IP Status tab
2. Review Change Log via "More info" link
3. Check IP to upgrade → click **Upgrade Selected**

### Upgrade via Tcl

```tcl
# Upgrade all IP in the design
upgrade_ip

# Upgrade specific IP with log
upgrade_ip [get_ips cfifo] -log c:/prj/IP/cfifo_upgrade.log
```

> ⚠️ **Caution:** Do NOT use `upgrade_ip [get_ips -all]` — the `-all` option returns sub-core IP that may be removed during parent upgrade, causing unreferenced Tcl objects.

### Selective Upgrade

You can upgrade individual IP while leaving others locked. Locked IP with existing OOC DCPs can still be used for bitstream generation.

### See Also

- [Appendix D: Using IP Across Software Versions](appendix_d_using_ip_across_software_versions.md)

---

## Understanding Multi-Level IP

| Type | Description | OOC Runs |
|------|-------------|----------|
| **Sub-core reference** | IP references another IP as a library of files | 1 (parent only) |
| **Static IP** | Packaged with XCI files for child IP | Multiple XCI visible |
| **Dynamic IP** | Dynamically creates child IP and HDL | 1 (all synthesized together) |
| **Subsystem IP** | Uses IP Integrator to create and interconnect child IP | Children in parallel, then linked |

> **Tip:** Subsystem IP based on block design launch children OOC runs in parallel — combined with IP Caching, this can greatly speed up generation.

---

## Working with Debug IP

| Debug Core | Purpose | Instantiation |
|-----------|---------|---------------|
| **ILA** (Integrated Logic Analyzer) | Monitor signals, trigger on events, capture data at system speed | HDL or post-synthesis insertion |
| **VIO** (Virtual I/O) | Drive and monitor internal signals in real time | HDL instantiation required |
| **IBERT** (Integrated BER Tester) | In-system serial I/O validation and debug | Example design from IP catalog |
| **JTAG-to-AXI** | Generate AXI transactions for debugging AXI slaves | IP catalog (Debug category) |

### Debugging Flows

| Flow | Method | Advantages | Disadvantages |
|------|--------|-----------|---------------|
| **HDL Instantiation** | Add debug IP cores in HDL | Probe at HDL level | Manual; error-prone |
| **Netlist Insertion** (Recommended) | Use `MARK_DEBUG` attribute + Set up Debug wizard | Flexible; no HDL modification | Cannot add IBERT or JTAG-to-AXI |
| **Tcl-based Netlist Insertion** | `create_debug_core`, `create_debug_port`, `connect_debug_port` | Fully scriptable | Requires Tcl expertise |

### See Also

- Vivado Design Suite User Guide: Programming and Debugging (UG908)
- Vivado Design Suite Tutorial: Programming and Debugging (UG936)

---

## Using a Core Container

The Core Container feature provides a **single XCIX file** containing the IP and all output products.

> **Note:** Binary files are not ideal for revision control. XCI can be extracted alongside XCIX:
> ```tcl
> set_property coreContainer.alwaysCreateXCI 1 [current_project]
> ```

### Enabling/Disabling

| Method | Steps |
|--------|-------|
| **All new IP** | Settings → IP → Check "Use Core Containers for IPs" |
| **Existing IP** | IP Sources → right-click → Enable/Disable Core Container |

> **Note:** 7 series Memory Interface IP and IP inside IP Integrator block designs do not support Core Container.

### Support Files Locations

| Context | Location |
|---------|----------|
| **RTL Project** | `<project_dir>/<project>.ip_user_files/ip/<ip_name>/` |
| **Manage IP Project** | `<managed_ip_dir>/ip_user_files/ip/<ip_name>/` |

### `ip_user_files` Directory Contents

| Directory | Contents |
|-----------|----------|
| `bd/` | Support files for each IP Integrator block design |
| `ip/` | Support files per IP customization (sim, templates, stubs) |
| `ipstatic/` | Common IP static simulation files |
| `mem_init_files/` | Memory initialization files (MIF, TXT) |
| `sim_scripts/` | Simulation scripts for all supported simulators |

```tcl
# Export support files manually
export_ip_user_files -of_objects [get_ips <ip_name>]
```

---

## Best Practices

1. **Always reference IP via the XCI file** — never use only the DCP; it lacks constraints and other required products since 2017.1
2. **Use the default OOC flow** to reduce synthesis runtimes during development
3. **Enable IP caching** (especially shared/remote) for team environments to avoid redundant synthesis
4. **Generate output products before upgrading** Vivado releases — this lets you use old IP versions if needed
5. **Archive projects before IP upgrades** — upgrading removes all previously generated outputs
6. **Store IP outside the project directory** when using revision control to minimize checked-in files
7. **Use the netlist insertion debug flow** (recommended) — more flexible than HDL instantiation with fewer errors
8. **Set the simulator language property** correctly to ensure appropriate simulation models are delivered
9. **Review the IP Change Log** before any version upgrade, especially for major version changes

---

## Quick Reference

| Task | Tcl Command |
|------|-------------|
| Create IP | `create_ip -name <name> -version <ver> -vendor amd.com -library ip -module_name <mod>` |
| Set IP property | `set_property CONFIG.<prop> <value> [get_ips <name>]` |
| Report IP properties | `report_property CONFIG.* [get_ips <name>]` |
| Generate output products | `generate_target all [get_files <path>/<name>.xci]` |
| Reset output products | `reset_target all [get_files <path>/<name>.xci]` |
| Disable OOC | `set_property GENERATE_SYNTH_CHECKPOINT FALSE [get_ips <name>]` |
| Create IP run | `create_ip_run -force [get_ips <name>]` |
| Copy IP | `copy_ip -name <new_name> [get_ips <name>]` |
| Import IP | `import_files <ip_file>` |
| Read IP remotely | `read_ip <ip_file>` |
| Report IP status | `report_ip_status` |
| Upgrade IP | `upgrade_ip [get_ips <name>] -log <path>` |
| Set simulator language | `set_property SIMULATOR_LANGUAGE <lang> [current_project]` |
| Export user files | `export_ip_user_files -of_objects [get_ips <name>]` |
| Report constraint order | `report_compile_order -constraints` |
| Clear IP cache | `config_ip_cache -clear_output_repo` |
| SV wrapper | `make_wrapper -language system_verilog [get_files <file>]` |

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Chapter:** 2 — IP Basics
- **Pages:** 9–71
