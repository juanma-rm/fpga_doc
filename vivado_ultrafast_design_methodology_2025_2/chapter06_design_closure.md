# Chapter 6 — Design Closure

Design closure consists of meeting all system performance, timing, and power requirements, and successfully validating functionality in hardware. During this phase, both timing and power considerations should be top priorities. Combining power and timing analysis early saves engineering time and enables more accurate project planning.

> **Reference:** UltraFast Design Methodology Timing Closure Quick Reference Guide (UG1292) for a condensed version of the techniques in this chapter.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Timing Closure](#timing-closure) | Meeting all timing requirements through constraints, analysis, and optimization |
| [Understanding Timing Closure Criteria](#understanding-timing-closure-criteria) | Valid constraints, positive slacks, timing reports |
| [Baselining the Design](#baselining-the-design) | Creating simplest constraints and validating timing at each step |
| [Analyzing and Resolving Timing Violations](#analyzing-and-resolving-timing-violations) | Root cause identification and resolution techniques |
| [Reducing Clock Skew](#reducing-clock-skew) | Techniques for minimizing clock skew impact |
| [Reducing Clock Uncertainty](#reducing-clock-uncertainty) | MMCM/PLL optimization, BUFGCE_DIV usage |
| [Applying Common Timing Closure Techniques](#applying-common-timing-closure-techniques) | Block-level synthesis, logic levels, control sets, fanout, congestion |
| [Tuning the Compilation Flow](#tuning-the-compilation-flow) | Strategies, directives, ML strategies, overconstraining |
| [SSI Technology Considerations](#ssi-technology-considerations) | SLR floorplanning, crossing registers, auto-pipelining |
| [Using Intelligent Design Runs](#using-intelligent-design-runs) | Automated timing closure with ML and QoR suggestions |
| [Power Closure](#power-closure) | Power estimation, constraints, optimization |
| [DRC Closure](#drc-closure) | Design rule checks and waivers |
| [Configuration and Debug](#configuration-and-debug) | Bitstream generation, ILA/VIO cores, IBERT, ECO flow |

---

## Timing Closure

Timing closure means the design meets all timing requirements. General guidelines:

- Evaluate timing throughout the flow when initially not meeting timing
- Focus on **worst negative slack (WNS)** of each clock as the main lever for improving **total negative slack (TNS)**
- Review large **worst hold slack (WHS)** violations (< −1 ns) to identify missing or inappropriate constraints
- Revisit trade-offs between design choices, constraints, and target architecture
- Be aware that tools do **not** further improve timing after timing is met (no additional margin)

> ⚠️ Timing results after synthesis use **estimated net delays**, not actual routing delays. Run implementation and check `report_timing_summary` for final results.

---

## Understanding Timing Closure Criteria

### Checking for Valid Constraints

Review the **Check Timing** section of the Timing Summary report:

- All active clock pins reached by a clock definition
- All active path endpoints have a requirement (setup/hold/recovery/removal)
- All active input ports have an `input_delay` constraint
- All active output ports have an `output_delay` constraint
- Timing exceptions are correctly specified

```tcl
# Verify constraint coverage
report_timing_summary
report_exceptions    ;# Identify timing exception conflicts
```

> ⚠️ Excessive use of wildcards in constraints can cause actual constraints to differ from intent. Use `report_exceptions` to review coverage.

In addition to `check_timing`, the **Methodology report** (TIMING and XDC checks) flags constraints that can lead to inaccurate timing analysis and possible hardware malfunction.

### Checking for Positive Timing Slacks

| Metric | Check Type | Requirement |
|--------|-----------|-------------|
| **WNS** > 0 ns, **TNS** = 0 ns | Setup/Recovery (max delay) | All setup paths must pass |
| **WHS** > 0 ns, **THS** = 0 ns | Hold/Removal (min delay) | All hold paths must pass |
| **WPWS** > 0 ns, **TPWS** = 0 ns | Pulse Width | All pulse width checks must pass |

### Understanding Timing Reports

- **TNS** — Sum of setup/recovery violations for each endpoint. Worst is WNS
- **THS** — Sum of hold/removal violations for each endpoint. Worst is WHS
- **TPWS** — Sum of pulse width/period/skew violations. Worst is WPWS

Total Slack only reflects violations — when all checks pass, Total Slack is null.

**Fundamental timing checks:**

| Check | Definition |
|-------|-----------|
| **Setup time** | Data must be stable before next active clock edge |
| **Hold requirement** | Data must remain stable after active clock edge |
| **Recovery time** | Min time from async reset inactive to next clock edge |
| **Removal time** | Min time after clock edge before async reset can toggle |

### Checking That the Design Is Properly Constrained

```tcl
# Identify unconstrained paths
check_timing
report_timing_summary  ;# Includes Unconstrained Paths section

# Identify non-optimal constraints
report_methodology     ;# TIMING and XDC checks

# Evaluate whether target frequencies are realistic
report_qor_assessment
```

### Fixing Issues Flagged by check_timing

Priority order (most to least important):

1. **No Clock / Unconstrained Internal Endpoints** — Must be zero for signoff. Ensures all internal paths are constrained
2. **Generated Clocks** — If derived from a master clock not on the same tree, timing engine cannot properly calculate delay → erroneous slack in hardware
3. **Loops / Latch Loops** — Combinational loops are broken by the timing engine; broken paths are not analyzed → can lead to incorrect behavior
4. **No Input/Output Delays / Partial I/O Delays** — All I/O ports must be properly constrained (can defer during baselining)
5. **Multiple Clocks** — Paths between different clocks are timed by default. Verify synchronous relationship or add `set_clock_groups` / `set_false_path`

### Fixing Issues Flagged by report_methodology

#### Methodology DRCs with Impact on Timing Closure

These flag missing CDC constraints, inappropriate clock trees, or inconsistent timing exception coverage due to replication. **Highest priority.**

| Check | Severity | Description |
|-------|----------|-------------|
| TIMING-6 | Critical Warning | No common clock between related clocks |
| TIMING-7 | Critical Warning | No common node between related clocks |
| TIMING-8 | Critical Warning | No common period between related clocks |
| TIMING-14 | Critical Warning | LUT on the clock tree |
| TIMING-15 | Warning | Large hold violation on inter-clock path |
| TIMING-16 | Warning | Large setup violation |
| TIMING-30 | Warning | Sub-optimal master source pin for generated clock |
| TIMING-31 | Critical Warning | Inappropriate multicycle path between phase-shifted clocks |
| TIMING-32/33/34/37/38/39 | Warning | Non-recommended bus skew constraint |
| TIMING-36 | Critical Warning | Missing master clock edge propagation for generated clock |
| TIMING-42 | Warning | Clock propagation prevented by path segmentation |
| TIMING-44/45 | Warning | Unreasonable user clock uncertainty |
| TIMING-49 | Critical Warning | Unsafe enable/reset topology from parallel BUFGCE_DIV |
| TIMING-56 | Warning | Missing logically/physically excluded clock groups constraint |
| XDCB-3 | Warning | Same clock in multiple groups in same `set_clock_groups` |
| XDCH-1 | Warning | Hold option missing in multicycle path constraint |
| XDCV-1/2 | Warning | Incomplete constraint coverage due to replication |

#### Methodology DRCs with Impact on Signoff Quality / Hardware Stability

These do not usually impact timing closure ease but flag problems with timing analysis accuracy. Even with positive slacks, hardware might not function properly.

| Check | Severity | Description |
|-------|----------|-------------|
| TIMING-1/2/3/4/27 | Critical Warning | Non-recommended clock source point definition |
| TIMING-5/25/19 | Critical Warning | Unexpected clock waveform |
| TIMING-9/10 | Warning | Unknown or incomplete CDC circuitry |
| TIMING-11 | Warning | Inappropriate `set_max_delay -datapath_only` |
| TIMING-17 | Critical Warning | Non-clocked sequential cell |
| TIMING-18/20/26 | Warning | Missing clock or I/O delay constraints |
| TIMING-21/22 | Warning | Issues with MMCM compensation |
| TIMING-35 | Critical Warning | No common node in paths with same clock |
| TIMING-47 | Warning | False path or async clock group between synchronous clocks |
| TIMING-51/52 | Critical Warning | No common phase between related clocks from parallel MMCMs/PLLs |
| TIMING-54 | Critical Warning | Scoped false path/clock group between clocks |

> Pay particular attention to **TIMING-28** (Auto-derived clock referenced by timing constraint) — auto-derived clock names change when modifying design source and resynthesizing.

### Assessing Maximum Frequency (FMAX)

Iteratively increase target clock frequency and re-run synthesis + implementation until small setup violations appear:

$$F_{MAX} = \max\left(\frac{1000}{T_i - WNS_i}\right) \text{ MHz}$$

Where $T_i$ is target clock period (ns) and $WNS_i$ is worst negative slack (ns) of run $i$.

- Use **Default** or **PerformanceOptimized** synthesis directives with **Explore** implementation directives
- Avoid overly tight clock periods (causes automatic effort reduction)
- For multi-clock designs, proportionally decrease all synchronous clock periods
- For a given implementation, max operating frequency across all conditions = $1000/(T - WNS)$

---

## Baselining the Design

Baselining creates the simplest timing constraints and initially ignores I/O timing. After all clocks are constrained, all internal paths are automatically constrained.

### Baselining Process

```
Post-Synthesis Checkpoint
  ↓
Define Baseline Constraints (Timing Constraints wizard, skip I/O)
  ↓ Validate with report_methodology
opt_design + report_timing_summary → Resolve setup violations (WNS)
  ↓
place_design + report_timing_summary → Resolve setup (WNS), reduce large hold (WHS > -0.500 ns)
  ↓ Optional phys_opt_design
route_design + report_timing_summary → Resolve all timing violations, verify methodology/DRC clean
  ↓
Baseline Process Complete
```

After baselining: eliminate smaller violations, achieve full constraint coverage, individually baseline new modules before adding to top-level.

### Defining Baseline Constraints

Use a valid post-synthesis checkpoint without user timing constraints. Open the **Timing Constraints wizard**:

1. Define **all clock constraints**
2. Define **CDC constraints** (timing exceptions between asynchronous clocks)
3. **Skip I/O timing constraints** (deselect suggested I/O constraints in wizard)

> All AMD IP constraints are automatically included and must be kept intact.

### Identifying Clocks

```tcl
# Remove all existing timing constraints
reset_timing

# List all primary clocks to define
report_clock_networks

# Verify generated clocks and attributes (P=propagated, G=generated, A=auto-derived)
report_clocks

# Verify no unconstrained endpoints
check_timing  ;# no_clock category
```

### Constraining Clock Domain Crossings

```tcl
# View clock relationships matrix
report_clock_interaction
```

**Clock Interaction Report Colors:**

| Color | Label | Meaning | Action |
|-------|-------|---------|--------|
| Black | No path | No interaction | Info only |
| Green | Timed | Paths being timed | Info unless unexpected |
| Cyan | Partial False Path | Some paths not timed due to exceptions | Verify exceptions desired |
| **Red** | **Timed (unsafe)** | **Clocks appear independent but timed** | **Check if should be async** |
| **Orange** | **Partial False Path (unsafe)** | **Independent clocks, partial exceptions** | **Check why partial** |
| Blue | User Ignored | Paths not timed (clock groups/false path) | Confirm async, verify CDC circuitry |
| Light blue | Max Delay Datapath Only | Timed via `set_max_delay -datapath_only` | Confirm async, verify delay |

**Identifying tight timing requirements:**

Sort `report_clock_interaction` by **Path Req (WNS)**. Example: 250 MHz → 200 MHz crossing results in 1 ns requirement (launch at 4 ns, capture at 5 ns).

Options for handling tight CDC requirements:
- `set_clock_groups` / `set_false_path` / `set_max_delay -datapath_only` — treat as async (validate with `report_cdc`)
- `set_multicycle_path` — relax requirement (requires proper clock circuitry)

### Decoupling Primary and Generated Clocks

```tcl
# Decouple all asynchronous primary clocks and their generated clocks
set_clock_groups -asynchronous \
  -group [get_clocks sysClk -include_generated_clocks] \
  -group [get_clocks gt0_txusrclk_i -include_generated_clocks] \
  -group [get_clocks gt2_txusrclk_i -include_generated_clocks] \
  -group [get_clocks gt4_txusrclk_i -include_generated_clocks]
```

### Limiting I/O Constraints and Timing Exceptions

```tcl
# Ignore I/O timing during baselining
config_timing_analysis -ignore_io_paths yes
```

- I/O constraints not needed during first baselining iterations
- Add I/O timing constraints after design and constraints are stable
- Keep all IP constraints intact

### Evaluating WNS After Each Step

Run `report_timing_summary` after each synthesis and implementation step. Track:

| Step | WNS | TNS | Failing Endpoints | WHS | THS | Failing Endpoints |
|------|-----|-----|-------------------|-----|-----|-------------------|
| Synth | | | | | | |
| Opt | | | | | | |
| Place | | | | | | |
| Physopt | | | | | | |
| Route | | | | | | |

**Key checkpoints:**

- **Post-Synthesis / Post-Opt:** Estimated net delays close to best possible placement. Fix via RTL changes, synthesis options, or timing exceptions
- **Post-Place:** Estimated net delays close to best route. Clock skew accurately estimated. Large hold violations (WHS ≥ −0.500 ns) between slices/BRAM/DSP need attention; small violations acceptable
- **Post-Physopt:** Evaluate need for high fanout nets, distant driver-load nets, sub-optimal DSP/BRAM pipeline registers
- **Post-Route:** Actual routed delays. **No hold violation should remain** regardless of WNS. Hold failures typically indicate very high congestion or improper constraints

### Baselining Validation Procedure

```tcl
# 1. Open synthesized design, record timing
report_timing_summary -delay_type min_max

# 2. Check missing clocks
report_clock_networks

# 3. Check tightest requirements and large hold violations
report_clock_interaction -delay_type min_max

# 4. Check high fanout nets
report_high_fanout_nets -timing -load_types -max_nets 25

# 5. Implement and record timing after each step
# 6. Check for overlapping constraints
report_exceptions -ignored
```

---

## Analyzing and Resolving Timing Violations

The timing-driven algorithms focus on the worst violations per clock domain. Fixing the worst violations often resolves many less critical paths automatically.

```tcl
# Automated analysis and suggestions
report_qor_suggestions

# Track progress
report_qor_assessment  ;# Before and after applying suggestions
```

### Identifying Timing Violations Root Cause

**For setup:** analyze worst violation of each clock group first.

**For hold:** review all violations — before routing only > 0.5 ns; after routing start with the worst.

### Reviewing Timing Slack

**Slack equations (simplified):**

$$\text{Setup Slack} = \text{Requirement} - \text{Datapath}_{max} + \text{Clock Skew} - \text{Clock Uncertainty} - \text{Setup Time}$$

$$\text{Hold Slack} = \text{Requirement} + \text{Datapath}_{min} - \text{Clock Skew} - \text{Clock Uncertainty} - \text{Hold Time}$$

$$\text{Clock Skew} = \text{Dest Clock Delay} - \text{Source Clock Delay (after common node)}$$

**Typical contributor order for setup/recovery** (worst to least):

1. **Datapath delay** — If (datapath − requirement) ≈ |slack|, requirement too tight or datapath too large
2. **Datapath + setup time** — Setup/recovery time larger than usual
3. **Clock skew** — If skew ≈ slack and |skew| > few 100 ps, review clock topology
4. **Clock uncertainty** — If > 100 ps, review clock topology and jitter

**For hold/removal:**

1. **Clock skew** — If > 300 ps, review clock topology
2. **Clock uncertainty** — If > 200 ps, review topology and jitter
3. **Hold/removal time** — If > few 100 ps, verify against primitive data sheet
4. **Hold requirement** — Usually zero; if not, verify constraints

### Using the Design Analysis Report

```tcl
# Report worst 50 setup timing paths with characteristics
report_design_analysis -max_paths 50 -setup -name design_analysis_postRoute
```

Key columns in the Timing Path Characteristics table:

| Issue | Columns to Check | Questions |
|-------|-----------------|-----------|
| High logic delay | Logic Delay, Logic Levels | Many levels? DONT_TOUCH/MARK_DEBUG preventing optimization? BRAM/DSP with high delay? |
| High net delay | Net Delay, High Fanout, Bounding Box | High fanout nets? Cells in multiple Pblocks? SLR crossings? |
| High skew (< −0.5 setup, > 0.5 hold) | Clock Skew, Clock Relationship | CDC path? Clocks sync or async? I/O column crossing? |

### Review Logic Level Distribution

```tcl
# Logic level distribution of worst 5000 paths
report_design_analysis -logic_level_distribution -logic_level_dist_paths 5000

# Narrow to specific logic levels
report_design_analysis -logic_level_distribution -min_level 16 -max_level 20 \
  -logic_level_dist_paths 5000

# Report longest paths
report_timing -of_objects [get_timing_paths -setup -to [get_clocks cpuClk_5] \
  -max_paths 5000 -filter {LOGIC_LEVELS>=16 && LOGIC_LEVELS<=20}]
```

### Datapath Delay and Logic Levels

**Cell delay dominated** (> 25% in 7 series, > 50% in UltraScale):
- Modify path to be shorter or use faster logic cells → see [Reducing Logic Delay](#reducing-logic-delay)

**Route delay dominated** (> 75% in 7 series, > 50% in UltraScale):
1. Check if impacted by **hold fixing** (`report_design_analysis -show_all`, Hold Detour column)
   - If CDC path missing constraint → add constraint
   - If not CDC → check clock tree balance (skew value)
2. Check if impacted by **congestion** (individual net delay, fanout, routing in Device view)
   - Low fanout but long delay with optimal routing → sub-optimal placement from congestion
   - High fanout → replicate driver → see [Optimizing High Fanout Nets](#optimizing-high-fanout-nets)
3. If neither → design spread too much → try [Reducing Control Sets](#reducing-control-sets), [Tuning the Compilation Flow](#tuning-the-compilation-flow), [Floorplanning](#considering-floorplanning)

---

## Reducing Clock Skew

Clock skew typically:
- < 300 ps for intra-clock paths
- < 500 ps for paths between balanced synchronous clocks
- Several ns for unbalanced clock trees or no common node → timing closure nearly impossible

500 ps at 300 MHz = 15% of period = budget of 1–2 logic levels.

### Techniques for Reducing Clock Skew

1. **Avoid cascaded clock buffers** — connect in parallel instead
2. **Combine parallel buffers into single buffer** — move clock enable logic to sequential cell CE pins; use multicycle exceptions if division was involved
3. **Remove LUTs/combinatorial logic in clock paths** — makes skew unpredictable; move to clock enable logic

### 7 Series Specific

- **Never** use `CLOCK_DEDICATED_ROUTE=FALSE` in production — only for temporary debugging
- Do not allow BUFR/BUFIO/BUFH to drive logic in multiple clock regions

### UltraScale / UltraScale+ Specific

- Avoid MMCM/PLL for simple division of `BUFG_GT` clock — use BUFG_GT's built-in divider for balanced trees
- Use **`CLOCK_DELAY_GROUP`** on critical synchronous clock driver nets for route matching
- Use **Pblocks** to keep timing paths within a single SLR or avoid I/O column crossings
- Constrain MMCM/PLL location to center of clock loads for high-speed synchronous CDC
- Use **`ANY_CMT_COLUMN`** instead of `FALSE` for `CLOCK_DEDICATED_ROUTE` waivers to ensure dedicated clocking resources

### Reducing Clock Delay in UltraScale+ SSI Devices

Clock routing: global buffer → routing track → **clock root** → vertical distribution → BUFCE_ROW per row → horizontal distribution → leaf level.

Row programmable tap delays decrease from the clock root outward. Higher tap values add uncertainty (process variation).

```tcl
# Query maximum row programmable tap delay
get_property MAX_PROG_DELAY [get_nets -of [get_pins BUFG/O]]

# Limit row programmable tap delay (recommended 3 or 4 for clocks spanning most of device)
set_property USER_MAX_PROG_DELAY 4 [get_nets -of [get_pins BUFG/O]]
```

- For `CLOCK_DELAY_GROUP` clocks, all clocks in the group must use the same `USER_MAX_PROG_DELAY` value
- Review tap settings in the **Clock Utilization Report** (HORIZONTAL PROG DELAY column)

---

## Reducing Clock Uncertainty

Clock uncertainty sources: user-specified (`set_clock_uncertainty`), system jitter, duty cycle distortion, MMCM/PLL discrete jitter and phase error.

### Optimizing MMCM Settings

Maximize VCO frequency for lowest output jitter:

$$F_{VCO} = F_{CLKIN} \times \frac{M}{D}$$

$$F_{OUT} = F_{CLKIN} \times \frac{M}{D \times O}$$

- Increase M, lower D, or both; compensate by increasing O
- Higher VCO → lower jitter but higher MMCM power
- Use Clocking Wizard with **Jitter Optimization = Minimize Output Jitter**
- MMCMs preferred over PLLs (higher VCO, better M/D granularity, fractional dividers on CLKOUT0)

**Example — 62.5 MHz input → ~40 MHz output:**

| Parameter | MMCM_1 (lower VCO) | MMCM_2 (higher VCO) |
|-----------|-------------------|---------------------|
| Output clock | 40.0 MHz | 39.991 MHz |
| M | 16 | 22.875 |
| D | 1 | 1 |
| VCO Frequency | 1000 MHz | 1429.688 MHz |
| O | 25 | 35.750 |
| **Jitter** | **167.5 ps** | **128.6 ps** |
| **Phase Error** | **384.4 ps** | **123.6 ps** |

### Using BUFGCE_DIV to Eliminate Phase Error

For synchronous CDC (e.g., 300 MHz ↔ 150 MHz from same MMCM), replace the MMCM-generated divided clock with a BUFGCE_DIV:

- 300 MHz through BUFGCE_DIV (divide=1) and 150 MHz through BUFGCE_DIV (divide=2)
- Setup uncertainty reduced by ~120 ps (phase error eliminated)
- Hold uncertainty reduced to 0 ns (same-edge hold)
- Apply `CLOCK_DELAY_GROUP` on both nets for matched routing

| Analysis | MMCM 150 MHz | BUFGCE_DIV 150 MHz |
|----------|--------------|--------------------|
| Setup: TSJ | 0.071 ns | 0.071 ns |
| Setup: DJ | 0.115 ns | 0.115 ns |
| Setup: PE | 0.120 ns | **0.000 ns** |
| Setup: Total | 0.188 ns | **0.068 ns** |
| Hold: Total | 0.188 ns | **0.000 ns** |

---

## Applying Common Timing Closure Techniques

> Run `report_qor_suggestions` to automatically identify and apply many of these techniques.

### Block-Level Synthesis Strategies

Mix synthesis strategies per hierarchy. Example: `PERFORMANCE_OPTIMIZED` BLOCK_SYNTH for timing-critical module + `Flow_AlternateRoutability` for the rest to reduce congestion.

See [chapter05_design_implementation.md](chapter05_design_implementation.md#block-level-synthesis-strategy).

### Improving Logic Levels

- **Global retiming** enabled by default. For power/compile recovery, disable globally and use `BLOCK_SYNTH.RETIMING` on specific modules
- Use `retiming_forward` / `retiming_backward` attributes for register-level control (RTL or XDC)

```tcl
# Enable retiming on specific hierarchy
set_property BLOCK_SYNTH.RETIMING 1 [get_cells inst1/inst2]
```

### Reducing Logic Delay

Identify and improve longest paths after synthesis/opt_design for biggest impact on timing and power QoR.

**Optimizing regular fabric paths:**

| Issue | Solution |
|-------|----------|
| Several small LUTs cascaded | `opt_design -remap` or AddRemap/ExploreWithRemap directives; `LUT_REMAP` property |
| Single CARRY cell in path | FewerCarryChains synthesis directive or PerfThresholdCarry strategy; `CARRY_REMAP` property |
| Path ends at SRL | `SRL_STYLE` attribute in RTL; `SRL_STAGES_TO_REG_INPUT` property before opt_design |
| Path ends at CE or sync set/reset | `EXTRACT_ENABLE="no"` or `EXTRACT_RESET="no"` in RTL; `CONTROL_SET_REMAP` property |

**Optimizing paths with dedicated blocks (DSP, BRAM, URAM):**

- Pipeline paths to/from dedicated blocks as much as possible
- Restructure combinational logic to reduce levels by 1–2 cells
- Meet setup by at least **500 ps** on these paths before placement
- Replicate logic cones connected to many dedicated blocks placed far apart
- Use `opt_design -dsp_register_opt` and `phys_opt_design -dsp_register_opt` for DSP paths

### Reducing Control Sets

A **control set** = group of clock, enable, and set/reset signals per sequential cell. Packing restrictions force registers to less optimal locations → logic spreading, longer delays, higher interconnect utilization.

**Guidelines:**

| Percentage of Device Control Sets | Status |
|-----------------------------------|--------|
| < 7.5% | Acceptable |
| 7.5% – 15% | Reduction recommended |
| > 15% | Reduction required |

Total control sets in device = CLB registers / 8.

```tcl
# Check control sets
report_control_sets -verbose   ;# Before placement
report_utilization              ;# After placement (text mode)
```

**Reduction strategies:**

```tcl
# Increase control set threshold during synthesis
synth_design -control_set_opt_threshold 16

# Merge equivalent control sets after synthesis
opt_design -control_set_merge
opt_design -merge_equivalent_drivers

# Remap low-fanout control signals to D-input
# Use CONTROL_SET_REMAP property on registers
```

- Remove `MAX_FANOUT` on control signals (rely on `place_design` + `phys_opt_design -directive Explore`)
- Avoid low-fanout asynchronous set/reset (cannot be moved to datapath)
- Avoid using both active-High and active-Low of same control signal
- Only use CE/reset when necessary (data paths often auto-flush)

### Optimizing High Fanout Nets

**Allow register replication:**
- Avoid `KEEP_HIERARCHY`, `KEEP`, `DONT_TOUCH` on nets that need replication
- Avoid low `MAX_FANOUT` or `MAX_FANOUT` on nets spanning major hierarchies
- Consider manual balanced replication trees based on design hierarchy

```tcl
# Merge equivalent drivers first, then replicate per hierarchy
opt_design -merge_equivalent_drivers
opt_design -hier_fanout_limit 1000

# Force replication during placement (fanout > 1000)
set_property FORCE_MAX_FANOUT 500 [get_nets netName]

# Physical fanout mode (CLOCK_REGION, SLR, MACRO)
set_property MAX_FANOUT_MODE CLOCK_REGION [get_nets netName]
```

**Promote to global routing:**

```tcl
# Insert clock buffer for high fanout nets
set_property CLOCK_BUFFER_TYPE BUFG [get_nets netName]
```

Automatically applied by `opt_design` for fanout > 25000 when limited clock buffers in use. Placer automatically routes fanout > 10000 on available global tracks.

**Physical optimization:**

```tcl
# Replicate specific critical nets
phys_opt_design -force_replication_on_nets [get_nets [list netA netB netC]]

# Higher effort directives
phys_opt_design -directive AggressiveFanoutOpt
```

### Prioritizing Critical Logic with group_path

```tcl
# Give higher priority to a clock domain
group_path -name [get_clocks clock] -weight 2
```

- Only one level of high priority supported; applies to entire clock group
- Not recommended for highly congested designs, high Rent exponent clocks, or clocks with high hold violations
- Reserve for high-frequency, smaller clock domains

### Fixing Large Hold Violations Prior to Routing

For hold violations > 0.4 ns, reduce before routing to help the router:

```tcl
# Insert negative-edge triggered registers (splits path into two half-period paths)
phys_opt_design -insert_negative_edge_ffs

# Insert LUT1 delays — standard
phys_opt_design -hold_fix

# Insert LUT1 delays — aggressive (more paths considered)
phys_opt_design -aggressive_hold_fix

# Combined directive
phys_opt_design -directive ExploreWithAggressiveHoldFix
```

### Addressing Congestion

#### Congestion Level Ranges

| Level | Area | Congestion | QoR Impact |
|-------|------|-----------|------------|
| 1, 2 | 2×2, 4×4 | None | None |
| 3, 4 | 8×8, 16×16 | Mild | Possible QoR degradation |
| **5** | **32×32** | **Moderate** | **Likely QoR degradation** |
| **6** | **64×64** | **High** | **Difficulty routing** |
| **7, 8** | **128×128, 256×256** | **Impossible** | **Likely unroutable** |

```tcl
# Analyze congestion
report_design_analysis -congestion

# View congestion metrics in Device window:
# Right-click → Metric → Interconnect Congestion Level
# Right-click → Metric → Vertical/Horizontal Routing Congestion per CLB (7 series/UltraScale)
```

**Router congestion messages:**
- `WARNING: [Place 46-14]` — Placer detected high congestion
- `WARNING: [Route 35-447]` — Router prioritizing completion over timing
- `INFO: [Route 35-443]` — CLB routing congestion, see generated text file
- `CRITICAL WARNING: [Route 35-162]` — Signals failed to route

#### Congestion Analysis Reports

```tcl
# Congestion report with hierarchical modules
report_design_analysis -congestion

# Complexity report (Rent exponent, Average Fanout)
report_design_analysis -complexity
report_design_analysis -complexity -hierarchical_depth 3
```

**Rent Exponent ranges:**

| Range | Meaning |
|-------|---------|
| 0.0 – 0.65 | Low to normal |
| 0.65 – 0.85 | High (especially > 15K instances) |
| > 0.85 | Very high — may fail implementation |

**Average Fanout ranges:**

| Range | Meaning |
|-------|---------|
| < 4 | Normal |
| 4 – 5 | High — placement without congestion difficult |
| > 5 | Very high — may fail implementation |

#### Congestion Alleviation Techniques

1. **Lower device utilization** — Remove non-essential modules when average fabric utilization > 75%
2. **Balance SLR utilization** — Use different placer directives or Pblocks to redistribute
3. **Alternate placer directives:**
   - `AltSpreadLogic_high/medium/low` — spread logic to avoid congested regions
   - `SSI_SpreadLogic_high/low` — for SSI devices
   - `SSI_BalanceSLLs` — balance SLLs between SLRs
   - `SSI_SpreadSLLs` — allocate extra area for high connectivity regions
   - `AlternateCLBRouting` (router directive, UltraScale only)
4. **Turn off cross-boundary optimization** — `synth_design -flatten_hierarchy none` or `KEEP_HIERARCHY` in RTL
5. **Reduce MUXF mapping:**
   ```tcl
   # Remap MUXF* to LUT3 globally
   opt_design -muxf_remap
   # Or target specific cells
   set_property MUXF_REMAP TRUE [get_cells ...]
   # Or via synthesis constraint per module
   set_property BLOCK_SYNTH.MUXF_MAPPING 0 [get_cells inst_name4]
   ```
6. **Disable LUT combining:**
   ```tcl
   # Use Flow_AlternateRoutability synthesis strategy, or:
   reset_property SOFT_HLUTNM [get_cells -hierarchical -filter {NAME =~ <module> && SOFT_HLUTNM != ""}]
   ```
7. **Limit high fanout nets** in congested areas — replicate drivers, promote to global routing
8. **Cell bloating:**
   ```tcl
   # Insert whitespace during placement (LOW, MEDIUM, HIGH)
   set_property CELL_BLOAT_FACTOR HIGH [get_cells module_inst]
   ```
   > ⚠️ Not recommended when device already overuses routing resources or for large cells.

---

## Tuning the Compilation Flow

### ML Strategies

Generate strategy suggestions on a routed design:

```tcl
# After implementation with Default or Explore directives
report_qor_suggestions
write_qor_suggestions -strategy_dir <directory>

# Apply ML strategy in next run
read_qor_suggestions <rqs_file>
opt_design -directive RQS
place_design -directive RQS
phys_opt_design -directive RQS
route_design -directive RQS
```

- Resolve all methodology checks first; QoR assessment score ≥ 3
- Run three implementation runs with different strategy suggestions
- Combine ML strategies with other QoR suggestions for best FMAX

### Custom Strategies

1. Try various placer directives with only I/O location constraints (no Pblocks)
2. Review WNS/TNS from placer log, select best 2–3 directives
3. For each placement checkpoint, try multiple `phys_opt_design` and `route_design` directives
4. Remove Pblocks before exploring: `delete_pblock [get_pblocks *]`

### Optimization Iterations

```tcl
# Iterate phys_opt_design: first targeted, then global
phys_opt_design -force_replication_on_nets [get_nets -hier *phy_reset*]
phys_opt_design -directive Explore
```

### Overconstraining the Design

Use `set_clock_uncertainty` to tighten requirements during placement, then remove before routing:

```tcl
# Overconstrain specific clock crossings for placement
set_clock_uncertainty -from clk0 -to clk1 0.3 -setup
set_clock_uncertainty -from clk2 -to clk3 0.4 -setup

# Run through placement and phys_opt
# ...

# Remove before routing
set_clock_uncertainty -from clk0 -to clk1 0 -setup
set_clock_uncertainty -from clk2 -to clk3 0 -setup

# Run router
route_design
```

> ⚠️ Do **not** overconstrain beyond 0.5 ns — increases power and compile time.

### Considering Floorplanning

- Fix worst problems first — group outlier paths in same region via Pblocks
- Keep Pblock size to a clock region for maximum placer flexibility
- Avoid overlapping Pblocks
- Minimize nets crossing Pblock boundaries
- For SSI devices, consider SLR Pblocks or `USER_SLR_ASSIGNMENT`

### Reusing Placement Results

```tcl
# Save BRAM placement for reuse across runs
set_property IS_LOC_FIXED 1 [get_cells -hier -filter {PRIMITIVE_TYPE =~ BLOCKRAM.*.*}]
write_xdc bram_loc.xdc -exclude_timing
```

> ⚠️ Do **not** reuse general slice logic placement. Use Incremental Compile for small design changes.

### Using Incremental Implementation

**Reference checkpoint selection:**
- Must meet timing or be close (WNS > −0.250 ns for automatic mode)
- Cell matching ≥ 94%, net matching ≥ 90% for automatic mode
- Select lowest congestion checkpoint
- Use incremental synthesis to reduce netlist changes
- Avoid AddRemap/ExploreWithRemap directives (reduce naming consistency)

**Directives:**

| Directive | Target | Use When |
|-----------|--------|----------|
| **RuntimeOptimized** (default) | Targets WNS from reference | Maintain consistency, improve runtime by ≥ 2× |
| **TimingClosure** | Targets WNS = 0 | Reference very close to meeting timing; trade consistency for effort |
| **Quick** | Minimal changes | > 99% reuse, ASIC emulation/prototype with minor changes |

```tcl
# Project Mode
set_property -name INCREMENTAL_CHECKPOINT.MORE_OPTIONS \
  -value {-directive TimingClosure} -object [get_runs <runName>]

# Non-Project Mode
read_checkpoint -incremental -directive TimingClosure <reference>.dcp
```

> ⚠️ Do **not** floorplan or overconstrain incremental runs — overrides reference placement and severely impacts reuse.

```tcl
# Ignore user clock uncertainty in incremental runs
config_implementation {incr.ignore_user_clock_uncertainty 1}
```

### XPIO-PL Interface Techniques (BLI)

```tcl
# Place flip-flops at XPIO-PL boundary logic interface
set_property BLI TRUE [get_cells {oddr_D1_BLI_reg oddr_D2_BLI_reg}]
set_property BLI TRUE [get_cells {iddr_Q1_BLI_reg iddr_Q2_BLI_reg}]
```

---

## SSI Technology Considerations

SSI devices consist of multiple **Super Logic Regions (SLRs)** connected by **Super Long Lines (SLLs)** through an interposer. There is a delay penalty crossing SLRs.

### Hard SLR Floorplan Constraints

Use SLR Pblocks + SLR-crossing Pblocks aligned to clock regions:

```tcl
# Define SLR Pblocks
resize_pblock pblock_SLR0 -add SLR0
resize_pblock pblock_SLR1 -add SLR1
# Use CLOCKREGION ranges (not LAGUNA) for crossing Pblocks
```

### Soft SLR Floorplan Constraints

```tcl
# Assign blocks to specific SLRs (soft constraint — placer can override)
set_property USER_SLR_ASSIGNMENT SLR1 [get_cells {IP1 IP2}]
set_property USER_SLR_ASSIGNMENT SLR0 [get_cells IP3]

# Control individual SLR crossings
set_property USER_CROSSING_SLR FALSE [get_pins -leaf -of [get_nets net_A]]
set_property USER_CROSSING_SLR TRUE  [get_pins -leaf -of [get_nets net_B]]
```

Unlike Pblocks, `USER_SLR_ASSIGNMENT` allows detailed placer and phys_opt to move pipeline registers across SLR boundaries for timing.

### SLR Crossing Registers (UltraScale+)

Map register-to-register SLR crossings to Laguna TX_REG → RX_REG:

```tcl
# Soft: let placer use Laguna registers
set_property USER_SLL_REG TRUE [get_cells {reg_A reg_B}]

# Hard: explicit BEL + LOC (position must match between TX/RX)
set_property BEL TX_REG3 [get_cells reg_A]
set_property BEL RX_REG3 [get_cells reg_B]
set_property LOC LAGUNA_X2Y480 [get_cells reg_A]
set_property LOC LAGUNA_X2Y360 [get_cells reg_B]
# Distance between paired Laguna sites = 120 rows
```

Benefits: spreads SLR crossings vertically, better delay estimation, faster/more consistent crossing performance.

### Auto-Pipelining for SLR Crossings

Use `AUTOPIPELINING_*` RTL attributes or AMD AXI Register Slice IP (SLR crossing mode). Placer automatically determines pipeline stages and uses Laguna registers.

### Clustering Logic

```tcl
# Group instances for closest possible placement
set_property USER_CLUSTER group1 [get_cells {instA instB}]
```

Use `USER_SLR_ASSIGNMENT` first, then `USER_CLUSTER` to control grouping within SLR.

---

## Using Intelligent Design Runs

Automated timing closure leveraging `report_qor_suggestions`, ML strategy predictions, and incremental compile. Runs up to **6 iterations** (typical compile time ~3.5× standard run).

**Stages:**
1. Apply optimization properties via `report_qor_suggestions`
2. Generate ML-optimized tool options for opt/place/physopt/route
3. Last Mile Timing Closure for difficult paths

**Requirements:**
- Project-based implementation (Non-Project: create post-synthesis netlist project)
- UltraScale or UltraScale+ device
- Accurate, achievable baseline constraints
- Clean `report_methodology`
- QoR assessment score ≥ 3
- SLR-based floorplan may be required for SSI devices

> Use intelligent design runs less frequently than standard runs — after resolving methodology warnings and trying common strategies (Default, Explore).

---

## Power Closure

### Estimating Power Throughout the Flow

```tcl
# Set power budget for margin reporting
set_operating_conditions -design_power_budget <watts>

# Estimate power at any stage
report_power
```

**Accuracy by stage:**
- **Post-Synthesis:** Netlist mapped to target resources (least accurate)
- **Post-Placement:** Final logic resource count/configuration available (export to XPE/PDM)
- **Post-Route:** Actual routing resources and exact timing (most accurate pre-hardware)

### Recommended Power Constraints

**Minimum:**

```tcl
set_operating_conditions -design_power_budget <Power in Watts>
set_operating_conditions -process maximum
```

**Additional (for accurate junction temperature / static power):**

```tcl
set_operating_conditions -ambient_temp <max ambient °C>
set_operating_conditions -thetaja <°C/W from thermal simulation>
```

**Per-regulator reporting:**

```tcl
create_power_rail <rail_name> -power_sources {supply1 supply2}
add_to_power_rail <rail_name> -power_sources {supply3}
set_operating_conditions -supply_current_budget {<rail_name> <Amps>} \
  -voltage {<rail_name> <voltage>}
```

### Power Constraint Advisor

Review tool-computed switching activity on control signals sorted by fanout. Watch for **Low confidence** levels indicating resets with high switching activity or enables with very low/zero activity.

### Power Optimization

```tcl
# Pre-place (maximizes power saving, rare timing degradation)
power_opt_design

# Post-place (preserves timing)
power_opt_design

# Block RAM power optimization (required when using Explore directives/strategies)
opt_design -bram_power_opt

# Exclude specific portions
set_power_opt -exclude_cells $pwr_critical_cells

# Report power optimization impact
report_power_opt -file myopt.rep
```

### Power-Timing Co-Optimization

Run `report_power` alongside timing analysis for every compilation run:

```tcl
# After each routed run
report_timing_summary
report_power

# Export to XPE/PDM for analysis
report_power -xpe {design_export.xpe}
```

Select runs that satisfy both timing and power budgets. In practice, ~10% power variation across different timing closure strategies.

> Minimize memory resources to reduce power. Use `report_power` RAM Utilization Report to find inefficient mapping. Consider `RAM_STYLE MIXED` attribute.

---

## DRC Closure

```tcl
# Run design rule checks
report_drc
```

- DRC rule decks are automatically executed as pre-conditions for `opt_design`, `place_design`, `route_design`
- Critical Warning DRCs during implementation become **Errors during bitstream generation**
- Address Critical Warning and Warning DRCs before moving to next stage
- Use the **waiver mechanism** for safely ignorable violations

---

## Configuration and Debug

### Configuration

After successful implementation, generate and load the bitstream:

- **Direct Programming:** Load bitstream to device via cable/processor
- **Indirect Programming:** Load bitstream to external flash → flash loads device

```tcl
# Create bitstream
write_bitstream

# Review configuration settings: Tools → Edit Device
# Format for flash programming (.mcs)
# Program device or flash
```

> If configuration fails, use JTAG to read the **Status register** for error conditions. Use readback/verify to check configuration data.

### Debugging the PL

#### ILA Cores (Integrated Logic Analyzer)

Monitor signals, trigger on hardware events, capture data at system speeds.

**Probing flows:**

| Flow | Method | Pros/Cons |
|------|--------|-----------|
| **HDL Instantiation** | Attach signals in HDL to ILA instance | HDL modification required; supports AXI interface probing |
| **Netlist Insertion** | `MARK_DEBUG` in RTL or post-synthesis + Set up Debug wizard | Most flexible; no HDL modification required |
| **Tcl-based Netlist Insertion** | `set_property mark_debug true` + Tcl commands | Fully automatic; debug on/off via Tcl |

**Choosing debug nets:**
- Probe at hierarchy boundaries (inputs/outputs) first
- Do **not** probe nets between combinatorial logic (prevents optimizations)
- Probe synchronous nets for cycle-accurate capture

**MARK_DEBUG in HDL:**

```vhdl
-- VHDL
attribute mark_debug : string;
attribute mark_debug of sine : signal is "true";
```

```verilog
// Verilog
(* mark_debug = "true" *) wire sine;
```

```tcl
# Post-synthesis
set_property mark_debug true [get_nets -hier [list {sine[*]}]]
```

**ILA timing considerations:**
- Choose probe width and data depth judiciously (impact utilization and timing)
- Use **free-running clocks** for ILA and dbg_hub
- Close timing before adding debug cores
- If dbg_hub is critical path: set `C_CLK_INPUT_FREQ_HZ` and enable `C_ENABLE_CLK_DIVIDER`
- Pipeline input probes with `C_INPUT_PIPE_STAGES` for high-speed designs

**ILA feature impact:**

| Feature | Timing Impact | Area Impact |
|---------|--------------|-------------|
| Capture Control / Storage Qualification | Medium-High | Slight LUT/FF increase |
| Advanced Trigger | High | Moderate LUT/FF increase |
| Number of Comparators (max 4) | Medium-High | Slight-Moderate LUT/FF |
| Data Depth | High | Additional BRAMs |
| Probe Port Width | Medium | Additional BRAMs |
| Number of Probe Ports | Low | Additional BRAMs |

#### VIO Cores (Virtual Input/Output)

Monitor and drive internal signals in real time — for low-speed signals (resets, status).

- Input probes must be synchronous to VIO `clk`
- Output probes asserted/deasserted synchronous to VIO `clk`
- Low refresh rate (replaces push-buttons/LEDs, not high-speed capture)

#### In-System IBERT

RX margin analysis (eye scan plots) on UltraScale/UltraScale+ GT transceivers. Configure/tune GTH/GTY via DRP. One instance per design; separate cores per GT type (GTH, GTY).

> If using internal system clock (MGTREFCLK) for In-System IBERT, eye scans may fail with "Incomplete" status. Use external clock or toggle MB_RESET register.

#### Debugging IP Integrator Designs

- **System ILA core** — debug interfaces/nets in block design (supports cross-trigger with MicroBlaze/Zynq)
- **Netlist insertion** — analyze I/O ports and internal nets post-synthesis

### Modifying Debug Probes Post-Implementation

- **Replace debug nets:** Use the Engineering Change Order (ECO) flow on a placed/routed checkpoint to modify nets on existing ILA cores without full re-implementation. See UG904 for ECO flow details.
- **Add/delete/edit ILA cores:** Use the **Incremental Compile** flow from a synthesized DCP with a reference implemented checkpoint. This can save significant time versus full re-implementation. See UG908 for incremental debug core insertion.
- **Net to external pin:** Use the ECO flow to bring an internal net out to a free device I/O pin for external debug equipment — useful when debugging requires measurements not obtainable through ILA/VIO. Requires an unused I/O pin on the device.

### Remote Debugging

Use the **Vivado hardware server** (`hw_server`) to connect to a remote computer in the lab for debug or design upgrades. See UG908 for remote connection setup.

---

## Best Practices

1. **Baseline early** — Create simplest timing constraints before design is complete; skip I/O timing initially
2. **Monitor timing at every step** — Run `report_timing_summary` after each implementation step; track WNS/TNS/WHS/THS progression
3. **Fix worst first** — Focus on WNS of each clock domain; fixing worst violations often resolves many secondary paths
4. **Use `report_qor_suggestions`** — Automates identification and application of many timing closure techniques
5. **Clean methodology first** — Resolve all `report_methodology` warnings before iterating on implementation
6. **Validate constraint coverage** — Zero unconstrained internal endpoints; properly decouple all asynchronous clocks
7. **Minimize control sets** — Keep below 7.5% of device capacity; avoid unnecessary resets and clock enables
8. **Address congestion proactively** — Congestion level ≥ 5 likely impacts QoR; use `report_design_analysis -congestion`
9. **Balance timing and power** — Run `report_power` alongside timing analysis; select runs that satisfy both budgets
10. **Plan debug early** — Decide probe strategy before implementation; use `MARK_DEBUG` judiciously (prevents optimization on marked nets)
11. **Use intelligent design runs** for difficult designs — After resolving methodology issues and trying standard strategies
12. **Never overconstrain beyond 0.5 ns** — Increases power and compile time without proportional benefit

---

## Quick Reference — Key Commands

| Command | Purpose |
|---------|---------|
| `report_timing_summary` | Overall timing status (WNS/TNS/WHS/THS/WPWS) |
| `check_timing` | Identify unconstrained paths |
| `report_clock_networks` | List primary clocks needing constraints |
| `report_clocks` | Verify all clocks (primary, generated, auto-derived) |
| `report_clock_interaction` | Clock relationships matrix with colors |
| `report_methodology` | TIMING/XDC constraint quality checks |
| `report_qor_assessment` | Score design readiness (1–5) |
| `report_qor_suggestions` | Automated timing closure recommendations |
| `report_design_analysis -setup` | Path characteristics analysis |
| `report_design_analysis -congestion` | Congestion analysis with hierarchical modules |
| `report_design_analysis -complexity` | Rent exponent and average fanout |
| `report_design_analysis -logic_level_distribution` | Logic level distribution for paths |
| `report_high_fanout_nets` | Identify high fanout non-clock nets |
| `report_control_sets -verbose` | Control set count and distribution |
| `report_exceptions -ignored` | Identify overlapping/conflicting constraints |
| `report_cdc` | Comprehensive CDC circuitry analysis |
| `report_power` | Power estimation and margin |
| `report_drc` | Design rule checks |
| `power_opt_design` | Run power optimization |
| `phys_opt_design -hold_fix` | Fix hold violations with LUT1 insertion |
| `phys_opt_design -insert_negative_edge_ffs` | Fix hold by inserting neg-edge registers |

## Quick Reference — Key Properties

| Property | Target | Purpose |
|----------|--------|---------|
| `CLOCK_DELAY_GROUP` | Net | Force route matching for synchronous clocks |
| `USER_MAX_PROG_DELAY` | Net | Limit row programmable tap delay (UltraScale+ SSI) |
| `FORCE_MAX_FANOUT` | Net | Force physical fanout-based replication |
| `MAX_FANOUT_MODE` | Net | Replication scope (CLOCK_REGION, SLR, MACRO) |
| `CLOCK_BUFFER_TYPE` | Net | Promote net to global routing (BUFG) |
| `CELL_BLOAT_FACTOR` | Cell | Insert whitespace during placement (LOW/MEDIUM/HIGH) |
| `MUXF_REMAP` | Cell | Remap MUXF* to LUT3 in opt_design |
| `LUT_REMAP` | Cell | Force LUT collapsing in opt_design |
| `CARRY_REMAP` | Cell | Remap CARRY to LUTs in opt_design |
| `CONTROL_SET_REMAP` | Cell | Move control signals to D-input |
| `SRL_STAGES_TO_REG_INPUT` | Cell | Pull register out of SRL |
| `BLOCK_SYNTH.RETIMING` | Cell | Enable/disable retiming per module |
| `BLOCK_SYNTH.MUXF_MAPPING` | Cell | Control MUXF synthesis per module |
| `USER_SLR_ASSIGNMENT` | Cell | Soft SLR floorplanning |
| `USER_CROSSING_SLR` | Net/Pin | Control individual SLR crossings |
| `USER_SLL_REG` | Cell | Map register to Laguna site |
| `USER_CLUSTER` | Cell | Group instances for closer placement |
| `BLI` | Cell | Place at XPIO-PL boundary logic interface |
| `MARK_DEBUG` | Net | Preserve net for ILA debugging |

---

## Source Attribution

- **Document:** UG949 — Vivado UltraFast Design Methodology Guide for FPGAs and SoCs
- **Version:** 2025.2 (November 20, 2025)
- **Chapter:** 6 — Design Closure (pp. 209–315)
- **Related:** UG906 (Design Analysis & Closure Techniques), UG907 (Power Analysis & Optimization), UG908 (Programming & Debugging), UG1292 (Timing Closure Quick Reference)
