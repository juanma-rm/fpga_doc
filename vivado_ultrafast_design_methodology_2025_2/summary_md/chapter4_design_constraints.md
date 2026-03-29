# Chapter 4: Design Constraints

This chapter covers constraint organization, synthesis and implementation constraints, the four-step timing constraint methodology (clocks, I/O delays, clock groups/CDC, timing exceptions), and power/thermal/physical constraints for AMD FPGA designs.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Organizing the Design Constraints for Compilation](#organizing-the-design-constraints-for-compilation) | File organization, read sequence, recommended sequence |
| [Creating Synthesis Constraints](#creating-synthesis-constraints) | XDC commands accepted by synthesis, naming considerations |
| [Creating Implementation Constraints](#creating-implementation-constraints) | Accuracy requirements, block-level constraints |
| [Specifying Constraints for the Vitis Environment](#specifying-constraints-for-the-vitis-environment) | IP packaging, Pre/Post Tcl scripts |
| [Defining Timing Constraints](#defining-timing-constraints) | Four-step process: clocks, I/O delays, clock groups, exceptions |
| [Defining Power and Thermal Constraints](#defining-power-and-thermal-constraints) | Operating conditions, power rails, ThetaJa |
| [Defining Physical Constraints](#defining-physical-constraints) | I/O location, floorplanning, configuration |

---

## Organizing the Design Constraints for Compilation

### Recommended Constraint Files

**Simple Design** (small team):

- 1 file for all constraints, **or**
- 1 file for physical + 1 file for timing, **or**
- 1 file for physical + 1 file for timing (synthesis) + 1 file for timing (implementation)

**Complex Design** (multiple teams / IP cores):

- 1 file for top-level timing + 1 file for top-level physical + 1 file per IP/major block

### Validating the Read Sequence

- **Project Mode**: Modify sequence in Vivado IDE or with `reorder_files`
- **Non-Project Mode**: Sequence defined by `read_xdc` and `source` commands in the Tcl script

### Recommended Constraints Sequence

```tcl
## Timing Assertions Section
# Primary clocks
# Virtual clocks
# Generated clocks
# Delay for external MMCM/PLL feedback loop
# Clock Uncertainty and Jitter
# Input and output delay constraints
# Clock Groups and Clock False Paths

## Timing Exceptions Section
# False Paths
# Max Delay / Min Delay
# Multicycle Paths
# Case Analysis
# Disable Timing
```

Key rules:

- **Variables/clocks must be defined before use** — timing clocks before any referencing constraints
- **Equivalent constraints, same precedence** — last one wins
- **Multiple exceptions on same path** — higher precedence applies
- **Physical constraints** can be placed anywhere

---

## Creating Synthesis Constraints

Synthesis transforms RTL into an optimized netlist using timing-driven algorithms. Not all XDC commands influence synthesis.

### Commands That Affect Synthesis QoR (Setup/Recovery)

| Command | Effect |
|---------|--------|
| `create_clock` / `create_generated_clock` | Defines timing references |
| `set_input_delay` / `set_output_delay` | Models external path delays |
| `set_clock_groups` / `set_false_path` | Ignores paths between clock domains |
| `set_max_delay` / `set_multicycle_path` | Modifies setup path requirements |

### Ignored by Synthesis

| Category | Examples |
|----------|---------|
| Hold/removal constraints | `set_min_delay`, `set_false_path -hold`, `set_multicycle_path -hold` |
| Physical constraints | `LOC`, `BEL`, Pblocks |

### RTL Attributes Affecting Synthesis

| Attribute | Purpose |
|-----------|---------|
| `DONT_TOUCH` / `KEEP` / `KEEP_HIERARCHY` | Prevent optimization of objects |
| `MARK_DEBUG` | Preserve signals for debug |
| `MAX_FANOUT` | Force replication at fanout threshold |
| `RAM_STYLE` / `ROM_STYLE` / `USE_DSP` | Control resource mapping |
| `SHREG_EXTRACT` | Control SRL inference |
| `FULL_CASE` / `PARALLEL_CASE` | Verilog synthesis directives |

> Synthesis constraints must use names from the **elaborated netlist** (preferably ports and sequential cells). Use **Open Elaborated Design** to verify object names.

> ⚠️ RTL netlist objects used in timing constraints can be optimized away by synthesis. Use `KEEP` to preserve objects that must exist in both synthesis and implementation.

---

## Creating Implementation Constraints

Implementation constraints must accurately reflect the final application requirements:

- Physical constraints (I/O location, I/O standard) are dictated by board design
- Verify all synthesis constraints still apply with the implementation netlist
- Create additional XDC files for implementation-only constraints when names change

### Creating Block-Level Constraints

For multi-team projects:

- Develop constraints independently from top-level
- Keep constraints generic for reuse in various contexts
- Do not affect logic beyond block boundaries
- Include full clocking network in sub-block timing validation

---

## Specifying Constraints for the Vitis Environment

### IP Packaging

- **C/C++ kernel**: Constraints specified in Vitis HLS, packaged with IP
- **RTL kernel**: Constraints specified during IP packaging

All synthesis/implementation constraints must be packaged with the IP. Post-packaging, additional XDC constraints can be added for implementation only via Pre/Post Tcl scripts.

### Pre/Post Tcl Scripts

**Configuration file syntax:**

```ini
[vivado]
prop=run.impl_1.STEPS.OPT_DESIGN.TCL.PRE=<pathToTclScript>
prop=run.impl_1.STEPS.OPT_DESIGN.TCL.POST=<pathToTclScript>
prop=run.impl_1.STEPS.PLACE_DESIGN.TCL.PRE=<pathToTclScript>
prop=run.impl_1.STEPS.PLACE_DESIGN.TCL.POST=<pathToTclScript>
prop=run.impl_1.STEPS.PHYS_OPT_DESIGN.TCL.PRE=<pathToTclScript>
prop=run.impl_1.STEPS.PHYS_OPT_DESIGN.TCL.POST=<pathToTclScript>
prop=run.impl_1.STEPS.ROUTE_DESIGN.TCL.PRE=<pathToTclScript>
prop=run.impl_1.STEPS.ROUTE_DESIGN.TCL.POST=<pathToTclScript>
```

**Command-line syntax:**

```bash
--vivado.prop run.impl_1.STEP.OPT_DESIGN.TCL.PRE=<pathToTclScript>
```

Supported phases: `INIT_DESIGN`, `OPT_DESIGN`, `PLACE_DESIGN`, `PHYS_OPT_DESIGN`, `ROUTE_DESIGN`, `WRITE_BITSTREAM`

---

## Defining Timing Constraints

### The Four-Step Process

| Step | Purpose | Key XDC Commands | Validation Reports |
|------|---------|------------------|--------------------|
| **1. Create Clocks** | Define timing references | `create_clock`, `create_generated_clock`, `set_input_jitter`, `set_system_jitter`, `set_clock_uncertainty`, `set_external_delay` | `report_clock_networks`, `check_timing` |
| **2. I/O Delays** | Constrain external paths | `set_input_delay`, `set_output_delay` | `check_timing`, `report_timing` |
| **3. Clock Groups & CDC** | Handle asynchronous/exclusive clocks | `set_clock_groups`, `set_false_path` | `report_clock_interaction`, `check_timing` |
| **4. Timing Exceptions** | Modify default path requirements | `set_false_path`, `set_max_delay`, `set_min_delay`, `set_multicycle_path`, `set_case_analysis`, `set_disable_timing` | `report_timing_summary`, `report_timing` |

Steps 1–2 define **timing assertions** (default path requirements). Step 3 handles **clock relationships**. Step 4 applies **timing exceptions** to override defaults.

> **Recommended:** Use the **Timing Constraints Wizard** for steps 1–3 to ensure safe and reliable constraints.

### Step 1: Defining Clock Constraints

#### Identifying Clock Sources

```tcl
# List constrained and unconstrained clock source points
report_clock_networks

# Report clock pins with no clock definition
check_timing -override_defaults no_clock
```

#### Creating Primary Clocks

Primary clocks define timing references at design boundaries. Define on:

| Source | Example |
|--------|---------|
| **Input ports** | `create_clock -name SysClk -period 10 [get_ports sysclk]` |
| **GT output pins** (7 series) | `create_clock -name txclk -period 6.667 [get_pins gt0/TXOUTCLK]` |
| **Primitive output pins** (no timing arc from input) | Define on output pin where clock path breaks |

> ⚠️ **Never** define a primary clock in the transitive fanout of another primary clock — prevents accurate insertion delay/skew computation.

> For UltraScale/UltraScale+ devices, GT clocks are automatically derived from REFCLK — do **not** define a primary clock on GT output pins.

#### Creating Generated Clocks

Generated clocks are derived from master clocks via clock modifying blocks (CMBs):

**7 Series CMBs:** MMCM/PLL, BUFR, PHASER

**UltraScale CMBs:** MMCM/PLL, BUFG_GT/BUFGCE_DIV, GT*_COMMON/GT*_CHANNEL/IBUFDS_GTE3, BITSLICE_CONTROL/RX*_BITSLICE, ISERDESE3

Auto-derived clocks are preferred — safest method. To rename an auto-derived clock:

```tcl
create_generated_clock -name fftClk [get_pins mmcm_i/CLKOUT0]
```

For user-defined generated clocks (logic cone divider):

```tcl
create_generated_clock -name clkDiv2 -divide_by 2 \
    -source [get_pins fd/C] [get_pins fd/Q]
```

> Generated clocks **must** be in the transitive fanout of their master clock for accurate insertion delay computation.

#### Verifying Clock Definitions

```tcl
report_clocks
check_timing -override_defaults {no_clock unconstrained_internal_endpoint}
report_methodology -checks [get_methodology_checks {TIMING-* XDC*}]
```

#### Adjusting Clock Characteristics

**Jitter:**

| Command | Use |
|---------|-----|
| `set_input_jitter` | Peak-to-peak jitter on primary clock entering device |
| `set_system_jitter` | Global jitter for noisy power supply (use default) |

**Additional Uncertainty:**

```tcl
# Tighten all intra-clock paths of clk0 by 500 ps (setup and hold)
set_clock_uncertainty -from clk0 -to clk0 0.500

# Tighten inter-clock paths by 250 ps (setup only, both directions)
set_clock_uncertainty -from clk0 -to clk1 0.250 -setup
set_clock_uncertainty -from clk1 -to clk0 0.250 -setup
```

> This is the safest way to over-constrain without modifying clock edges.

**MMCM/PLL External Feedback Loop:**

```tcl
set_external_delay ...  # Specify board delay for feedback compensation
```

Failure to set this makes I/O timing analysis irrelevant and can prevent timing closure.

**Clock Latency at the Source:**

Model the latency of a clock at its source using `set_clock_latency -source`:

```tcl
# Specify clock source propagation delay outside the device
set_clock_latency -source -early 0.2 [get_clocks clk]
set_clock_latency -source -late 0.5 [get_clocks clk]
```

Use cases:

- Specify clock delay propagation outside the device independently from input/output delay constraints
- Model internal propagation latency during **out-of-context compilation** where the complete clock tree is not described

> ⚠️ This constraint should only be used by advanced users — providing valid latency values is difficult.

### Step 2: Constraining Input and Output Ports

#### Input Delay

```
Input Delay(max) = Tco(max) + Ddata(max) + Dclock_to_ExtDev(max) - Dclock_to_FPGA(min)
Input Delay(min) = Tco(min) + Ddata(min) + Dclock_to_ExtDev(min) - Dclock_to_FPGA(max)
```

```tcl
set_input_delay -max -clock sysClk 5.4 [get_ports DIN]
set_input_delay -min -clock sysClk 2.1 [get_ports DIN]
```

A negative input delay means data arrives before the launch clock edge.

#### Output Delay

```
Output Delay(max) = Tsetup + Ddata(max) + Dclock_to_FPGA(max) - Dclock_to_ExtDev(min)
Output Delay(min) = Ddata(min) - Thold + Dclock_to_FPGA(min) - Dclock_to_ExtDev(max)
```

```tcl
set_output_delay -max -clock sysClk 2.4 [get_ports DOUT]
set_output_delay -min -clock sysClk -1.1 [get_ports DOUT]
```

Min output delay is often negative — a positive value means the signal can have negative internal delay.

#### Choosing the Reference Clock

| Scenario | Reference Clock |
|----------|----------------|
| Direct clock (no CMB) | Primary clock |
| ZHOLD-compensated MMCM | Primary clock (waveforms identical) |
| Different period (CMB transforms waveform) | **Virtual clock** with same period as internal clock |
| Phase-shifted input path | Virtual clock + `set_multicycle_path -setup 2` |
| Source synchronous output | Generated/forwarded clock |

#### Identifying Related Clocks per Port

```tcl
# Report worst path from input port, sorted by clock group
report_timing -from [get_ports din] -sort_by group

# Report from all I/O ports for both setup and hold
report_timing -from [all_inputs] -nworst 1000 -sort_by group -delay_type min_max
report_timing -to [all_outputs] -nworst 1000 -sort_by group -delay_type min_max
```

#### Input-to-Output Feed-Through Paths

**Method 1 — Virtual clock:**

```tcl
create_clock -name vclk -period 10
set_input_delay -clock vclk <input_delay> [get_ports din] -max
set_output_delay -clock vclk <output_delay> [get_ports dout] -max
```

**Method 2 — Direct max/min delay:**

```tcl
set_max_delay -from [get_ports din] -to [get_ports dout] 10
set_min_delay -from [get_ports din] -to [get_ports dout] 2
```

#### Source Synchronous Interfaces

For source synchronous interfaces, AMD recommends using the I/O constraint templates provided by the Vivado Design Suite. Navigate to: **Tools → Language Templates → XDC → Timing Constraints → Input Delay Constraints → Source Synchronous**.

The templates are based on default timing analysis path requirements. The syntax is simpler, but delay values must be adjusted to account for setup analysis being performed with different launch and capture edges (1-cycle or 1/2-cycle) instead of same edge (0-cycle). Timing reports may be more difficult to read as clock edges do not directly correspond to active hardware edges.

> **Note:** The source-synchronous forwarded clock can also be used in input and output delay constraints for a system synchronous interface.

### Step 3: Defining Clock Groups and CDC Constraints

#### Reviewing Clock Interactions

| Relationship | Condition |
|-------------|-----------|
| **Synchronous** | Common circuitry (common node) + common primary clock |
| **Asynchronous** | No common circuitry, no common primary clock, or unexpandable period |
| **Exclusive** | Same clock tree, same clock pins, but never active simultaneously |

```tcl
report_clock_interaction
check_timing -override_defaults multiple_clock
```

#### Constraining Exclusive Clock Groups

**Overlapping clocks on same source:**

```tcl
create_clock -name clk_mode0 -period 10 [get_ports clkin]
create_clock -name clk_mode1 -period 13.334 -add [get_ports clkin]
set_clock_groups -physically_exclusive \
    -group [get_clocks -include_generated_clock clk_mode0] \
    -group [get_clocks -include_generated_clock clk_mode1]
```

**Multiplexed clocks (no direct interaction before MUX):**

```tcl
set_clock_groups -logically_exclusive -group clk0 -group clk1
```

**Multiplexed clocks (interaction exists before MUX):**

```tcl
create_generated_clock -name clk0mux -divide_by 1 \
    -source [get_pins mux/I0] [get_pins mux/O]
create_generated_clock -name clk1mux -divide_by 1 \
    -add -master_clock clk1 \
    -source [get_pins mux/I1] [get_pins mux/O]
set_clock_groups -physically_exclusive -group clk0mux -group clk1mux
```

#### Constraining Asynchronous Clock Groups

**Global — both directions (no latency control needed):**

```tcl
set_clock_groups -asynchronous \
    -group [get_clocks -include_generated_clock clkA] \
    -group [get_clocks -include_generated_clock clkB]
```

**Individual CDC paths — latency control needed:**

```tcl
# Gray-coded bus (limit delay variation among bits)
set_max_delay -from [get_cells GCB0[*]] -to [get_cells GCB1a[*]] \
    -datapath_only 5

# Other paths between same clocks
set_false_path -from [get_cells REG0] -to [get_cells REG1a]
```

**Bus skew control:**

```tcl
set_bus_skew -from [get_cells bus_src[*]] -to [get_cells bus_dst[*]] 1.5
```

Use `report_cdc` for structural analysis of CDC topologies.

> ⚠️ `set_clock_groups` has **higher precedence** than `set_max_delay -datapath_only`. Do **not** use both between the same clocks — the max delay constraint will be silently ignored.

### Step 4: Specifying Timing Exceptions

#### Timing Exceptions Precedence

1. `set_case_analysis` / `set_disable_timing` (highest — disables analysis)
2. `set_clock_groups` (equivalent to bidirectional false path)
3. `set_false_path`
4. `set_max_delay` / `set_min_delay`
5. `set_multicycle_path` (lowest)

**Specificity rule:** More specific `-from`/`-to` targets override less specific ones (pin > cell > clock).

#### Guidelines

- Use a **limited number** of exceptions — many exceptions increase compile time
- Keep them **simple** — complex overlapping exceptions are difficult to debug
- Do not add exceptions to **hide** timing problems
- Prefer specific endpoints over broad targets like `[all_registers]`

#### False Path Constraints

Use cases:

- Path through mutually exclusive MUX inputs (never active simultaneously)
- Asynchronous CDC paths
- Static configuration registers that never toggle after initialization

```tcl
# Unsensitizable path through exclusive MUX inputs
set_false_path -through [get_pins MUX0/I0] -through [get_pins MUX1/I1]

# Static configuration register
set_false_path -from [get_cells config_reg[*]]
```

#### Max/Min Delay Constraints

```tcl
# Overconstrain specific paths
set_max_delay -from [get_pins <start>/C] -to [get_pins <end>/D] 14.5

# Asynchronous CDC with latency control
set_max_delay -from [get_cells src[*]] -to [get_cells dst[*]] -datapath_only 5
```

> ⚠️ **Path segmentation** occurs when specifying invalid startpoints/endpoints for `set_max_delay`/`set_min_delay`. Valid startpoints: clock, clock pin, sequential cell, input/inout port. Valid endpoints: clock, input data pin, sequential cell, output/inout port.

#### Multicycle Path Constraints

For paths with clock enable active every N cycles:

```tcl
# Enable active every 3 cycles, same clock
set_multicycle_path -from [get_pins REGA/C] -to [get_pins REGB/D] -setup 3
set_multicycle_path -from [get_pins REGA/C] -to [get_pins REGB/D] -hold 2
```

> Always specify the **endpoint pin** (not just the cell) to avoid accidentally constraining CE/RST pins that may toggle every cycle.

**Common mistakes:**

- Relaxing setup without adjusting hold → hold requirement becomes ≥ 1 clock period (impossible to meet)
- Constraining cell instead of pin → affects CE and RST pins unintentionally

#### Other Advanced Constraints

| Command | Purpose |
|---------|---------|
| `set_case_analysis` | Set constant on MUX select or port to select functional mode |
| `set_disable_timing` | Turn off a timing arc completely — ⚠️ can break more paths than desired |
| `set_data_check` | Setup/hold check between two pins (reporting only, ignored by implementation) |
| `set_max_time_borrow` | Limit latch time borrowing (expert use only) |

---

## Defining Power and Thermal Constraints

### Minimum Recommended Constraints

```tcl
set_operating_conditions -design_power_budget <Power in Watts>
set_operating_conditions -process maximum
set_operating_conditions -junction_temp <Max Tj based on Temp Grade>
```

### With Known Thermal Design (ThetaJa)

```tcl
set_operating_conditions -design_power_budget <Power in Watts>
set_operating_conditions -process maximum
set_operating_conditions -ambient_temp <Max Supported by Application>
set_operating_conditions -thetaja <°C/W>
```

$\Theta_{JA} = \frac{T_j - T_a}{P_d}$ (Celsius per watt)

### Power Rail Constraints

```tcl
create_power_rail <name> -power_sources {supply1 supply2}
add_to_power_rail <name> -power_sources {supply3}
set_operating_conditions -supply_current_budget {<rail> <amps>} -voltage {<rail> <volts>}
```

---

## Defining Physical Constraints

Ensure each pin has I/O location and standard specified. Physical constraints are covered in:

| Guide | Content |
|-------|---------|
| UG903 | Locking placement/routing, relative placement macros |
| UG906 | Floorplanning |
| UG908 | Configuration |

---

## Best Practices

1. **Define clocks first** — all other constraints depend on clock definitions
2. **Use the four-step methodology** — clocks → I/O delays → clock groups → exceptions
3. **Validate constraints with reports** at each step (`check_timing`, `report_clock_interaction`, `report_timing`)
4. **Use the Timing Constraints Wizard** for initial constraint creation
5. **Specify both min and max I/O delays** for proper setup and hold analysis
6. **Do not over-constrain** — unrealistic constraints degrade QoR and increase compile time
7. **Use `set_clock_groups`** for asynchronous domains without latency requirements
8. **Use `set_max_delay -datapath_only`** for CDC paths needing latency control
9. **Always pair multicycle setup with hold adjustment** — otherwise hold requirement grows unmanageable
10. **Use endpoint pins** (not cells) in multicycle constraints to avoid constraining CE/RST
11. **Apply power/thermal constraints early** — changes to power delivery and thermal solution are costly
12. **Run `report_methodology`** to catch constraint errors before implementation
13. **Keep timing exceptions few and specific** — broad exceptions increase compile time and hide problems

---

## Quick Reference

| Topic | Key Command |
|-------|-------------|
| Clock networks | `report_clock_networks` |
| Missing clocks | `check_timing -override_defaults no_clock` |
| Clock definitions | `report_clocks` |
| Clock interaction | `report_clock_interaction` |
| CDC analysis | `report_cdc` |
| Unconstrained paths | `report_timing_summary -report_unconstrained` |
| Timing from I/O ports | `report_timing -from [all_inputs] -delay_type min_max` |
| Methodology checks | `report_methodology -checks [get_methodology_checks {TIMING-* XDC*}]` |
| Reorder constraints | `reorder_files` (Project Mode) |
| Power report | `report_power` |

---

## Source Attribution

- **Source:** UG949 — *UltraFast Design Methodology Guide for FPGAs and SoCs*, v2025.2, November 20, 2025
- **Chapter:** 4 — Design Constraints (pages 146–187)
