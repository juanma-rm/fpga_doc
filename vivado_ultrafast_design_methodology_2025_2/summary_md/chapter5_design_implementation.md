# Chapter 5: Design Implementation

After selecting your device, choosing and configuring the IP, writing the RTL, and creating constraints, the next step is implementation. Implementation compiles the design through synthesis and place-and-route, then generates the programming file. This chapter describes the various implementation steps, highlights points for special attention, and gives tips and tricks for identifying and eliminating specific bottlenecks.

> **Important:** Regularly validate that synthesis and implementation occur without errors and with minimal timing violations before adding new blocks or generating a platform for the AMD Vitis tools.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Running Synthesis](#running-synthesis) | Synthesis flows, optimizations, attributes, and block-level strategy |
| [Moving Past Synthesis](#moving-past-synthesis) | Post-synthesis validation: DRCs, methodology, log review, QoR assessment |
| [Implementing the Design](#implementing-the-design) | Strategies, directives, iterative flows, checkpoints |
| [Using Incremental Implementation Flows](#using-incremental-implementation-flows) | Automatic mode, directives, configuration, parallel runs |
| [Implementation Steps](#implementation-steps) | opt_design, place_design, phys_opt_design, route_design |

---

## Running Synthesis

Synthesis takes RTL and timing constraints and generates an optimized netlist that is functionally equivalent to the RTL. Realistic timing constraints are required.

### Synthesis Flows

#### Global Synthesis

In global synthesis, the full design is synthesized in one run.

| Aspect | Detail |
|--------|--------|
| **Advantage** | Maximum optimization — tool is aware of full design and can optimize across hierarchies |
| **Advantage** | Easy post-synthesis analysis |
| **Disadvantage** | Longer compile time (full design rerun each time) |
| **Mitigation** | Use incremental synthesis to reduce recompile time |

> **Note:** If the design includes XDC constraints, objects must reference the top-level design.

#### Block Design Synthesis

The block design (BD) flow creates complex systems using custom and AMD IP via the Vivado IP integrator.

| Aspect | Detail |
|--------|--------|
| **Advantage** | Encapsulates large functionality into a compact design |
| **Advantage** | Enables focus on system level rather than individual parts |
| **OOC mode** | BD synthesized separately — faster resynthesis when hierarchies outside BD change |
| **Global mode** | Full compile each time — easier constraint setup but higher run time |

#### Out-of-Context (OOC) Synthesis

In OOC synthesis, certain hierarchy levels are synthesized separately from the top-level. OOC modules are synthesized first, then top-level synthesis treats each OOC run as a black box.

| Aspect | Detail |
|--------|--------|
| **Advantage** | Reduces compile time for subsequent runs — only specified modules resynthesized |
| **Advantage** | Stability — only runs including changes are resynthesized |
| **Disadvantage** | Requires additional setup; XDC must be defined separately per OOC run |

#### Incremental Synthesis

Incremental synthesis reuses existing synthesis results by reusing RTL partitions from a previous run, reducing typical compile time by ~50%.

**Activation requirement:** Design must create at least four RTL partitions, each containing at least 50,000 instances.

```tcl
synth_design -incremental_mode <value>
```

| Mode | Behavior |
|------|----------|
| `off` | Incremental synthesis disabled |
| `quick` | Fastest — no cross-boundary optimizations; limits operating frequency |
| `default` | Most optimizations enabled including cross-boundary; significant compile time reduction |
| `aggressive` | All optimizations enabled; significant compile time reduction |

**Mode Selection Guidelines:**

| Design Type | Recommended Modes |
|-------------|-------------------|
| Low-performance designs | `quick` (if hierarchy has registered boundaries) |
| High-performance designs | `default`, `aggressive`, or `off` |

> **Note:** In `quick` mode, resynthesis in a given area is triggered only by RTL changes in that area. In other modes, changes may trigger resynthesis of additional partitions. When >50% of partitions are modified, full resynthesis is triggered.

**Incremental Synthesis vs. OOC Synthesis:**

| Factor | Incremental Synthesis | OOC Synthesis |
|--------|-----------------------|---------------|
| Compile time | Faster than non-incremental but slower than OOC | Fastest — only re-elaborates modified OOC modules |
| Performance | Higher max clock frequency — cross-boundary optimizations | Limited by OOC boundaries |
| Setup | No additional setup required | Requires wrappers for generics/parameters; separate timing constraints per OOC |

---

### Synthesis Optimizations

#### Synthesis Settings

Global settings affect the entire design and control how logic is inferred and how incremental synthesis runs. Start with defaults, then adjust based on specific design needs.

> **Power Tip:** Evaluate synthesis settings carefully — they can considerably impact power consumption. For example, a low control set threshold increases register clock enable usage at the expense of less dense packing. Run `report_power` after synthesis to evaluate impact.

#### Synthesis Attributes

Attributes allow fine-grained control over logic inference to alter QoR where defaults are insufficient.

> **Note:** Before retargeting to a new device, review synthesis attributes from previous design runs targeting older devices.

##### KEEP and DONT_TOUCH

| Attribute | Scope | Behavior |
|-----------|-------|----------|
| `KEEP` | Synthesis only | Retains a signal; not passed to netlist as a property |
| `DONT_TOUCH` | Synthesis + place-and-route | Object is never optimized through the entire flow |

**Cautions:**

- `KEEP` on a register receiving RAM output prevents merging into RAM, blocking BRAM inference
- Do not place on hierarchy driving a 3-state or bidirectional signal in the level above — prevents IOBUF inference
- Both attributes result in larger, higher-power circuits — use sparingly and remove when no longer needed

**DONT_TOUCH scope behavior:**

| Placement | Effect |
|-----------|--------|
| On a signal | That signal is kept |
| On a hierarchy | Boundaries preserved, no constant propagation through hierarchy, but internal optimizations retained |

##### MAX_FANOUT

Forces synthesis to replicate logic to meet a fanout limit. The tool can replicate logic but **not** inputs or black boxes.

> **Important:** Use `MAX_FANOUT` sparingly during synthesis. The `place_design` and `phys_opt_design` commands perform placement-based replication, which is more effective than logical replication in synthesis. For specific fanout requirements, manually coding extra registers is often worthwhile.

**Limitations:**

- Cannot replicate a signal driven by a direct input to the design
- Ignored if paired with `DONT_TOUCH` on the driver or on a hierarchy containing the fanout targets
- Replicated cells are appended with `_rep`, `_rep__0`, `_rep__1`, etc.

---

### Block-Level Synthesis Strategy

Allows synthesizing different hierarchy levels with different global options in a top-down flow — faster and easier than bottom-up compile. Constraints are set for the full design.

```tcl
set_property BLOCK_SYNTH.<option_name> <value> [get_cells <instance_name>]
```

**Example:**

```tcl
set_property BLOCK_SYNTH.RETIMING 1                 [get_cells U1]
set_property BLOCK_SYNTH.STRATEGY {AREA_OPTIMIZED}  [get_cells U2]
set_property BLOCK_SYNTH.STRATEGY {AREA_OPTIMIZED}  [get_cells U3]
set_property BLOCK_SYNTH.STRATEGY {DEFAULT}          [get_cells U3/inst1]
```

Multiple `BLOCK_SYNTH` properties can be set on the same instance:

```tcl
set_property BLOCK_SYNTH.STRATEGY {ALTERNATE_ROUTABILITY} [get_cells inst]
set_property BLOCK_SYNTH.FSM_EXTRACTION {OFF} [get_cells inst]
```

> **Note:** Properties are set on hierarchical instances, so the same module instantiated multiple times can use different options. For OOC IP, use global settings when compiling the IP instead.

---

## Moving Past Synthesis

### Reviewing and Cleaning DRCs

```tcl
report_drc
```

The default rule deck checks:

- Post-synthesis netlist
- I/O, BUFG, and other placement-specific requirements
- Attributes and wiring on MGTs, IODELAYs, MMCMs, PLLs, and other primitives

> **Recommended:** Review and correct DRC violations as early as possible to avoid timing or logic issues later. For safely ignorable violations, use the waiver mechanism (see UG906).

### Running Report Methodology

```tcl
report_methodology
```

Checks vary by design stage:

| Stage | Checks Performed |
|-------|------------------|
| RTL design | RTL lint-style checks |
| Synthesized design | Netlist, constraints, and timing checks |
| Implemented design | Constraints and timing checks |

> **Recommended:** Run the first time you synthesize the design, and again after significant module additions, constraint changes, or clocking circuit changes.

> **Important:** Resolve all Critical Warnings and most Warnings to ensure good QoR, timing analysis accuracy, and reliable hardware stability. Methodology checks SYNTH-6, SYNTH-11, SYNTH-12, SYNTH-13 (RAMB/DSP pipelining) are not reported when setup slack >1 ns on all input/output paths.

### Reviewing the Synthesis Log

Review synthesis log files to confirm all messages match design intent. Pay special attention to Critical Warnings and Warnings.

> **Caution:** If a message appears more than 100 times, the tool writes only the first 100 occurrences. Adjust with:
> ```tcl
> set_param messaging.defaultLimit <new_value>
> ```

### Reviewing Timing Constraints

Clean timing constraints with proper exceptions are essential. Bad constraints result in long compile time, maximum clock frequency issues, and hardware failures.

> **Recommended:** Review all Critical Warnings and Warnings related to timing constraints indicating constraints have not been loaded or properly applied.

### Assessing Post-Synthesis Quality of Results

```tcl
report_qor_assessment
```

Combines logic level checks, utilization checks, and clocking topology checks into a summary with a score from 1–5:

| Score | Meaning |
|-------|---------|
| **1** | Design will likely not complete implementation |
| **2** | Design will complete implementation but will not meet timing |
| **3** | Design will likely not meet timing |
| **4** | Design will likely meet timing |
| **5** | Design will meet timing |

> **Note:** Thresholds in the detailed table are not absolute device limits — they indicate when timing closure becomes increasingly difficult. Exceeding any threshold makes difficulty increase exponentially.

Plan to correct any items marked for review. Many items can be resolved automatically by **Report QoR Suggestions**.

### Following Guidelines to Address Remaining Violations

> **Important:** Analyze timing post-synthesis to identify major design issues before moving forward.

HDL changes have the biggest impact on QoR. Pay special attention to:

- Most frequent offenders (cells/nets appearing most in top worst failing timing paths)
- Paths sourced by unregistered block RAMs
- Paths sourced by SRLs
- Paths with unregistered, cascaded DSP blocks
- Paths with large number of logic levels
- Paths with large fanout

### Dealing with High Levels of Logic

Estimated net delays post-synthesis are close to the best possible placement. To evaluate if a high-logic-level path can meet timing:

```tcl
report_timing -no_net_delay
```

> Timing closure cannot be achieved on paths that still violate timing with no net delays.

### Reviewing Utilization

```tcl
report_utilization
```

Review LUT, FF, block RAM, and DSP utilization independently. A design with low LUT/FF utilization might still experience placement difficulties if block RAM utilization is high.

> **Note:** After synthesis, utilization numbers might change due to optimization later in the flow.

### Reviewing Clock Trees

#### Clock Buffer Utilization

```tcl
report_clock_utilization
```

- Observe architecture clocking rules to avoid downstream placement issues
- Invalid placement constraints or very high fanout for regional clock buffers may cause placer issues
- For high clock buffer utilization, lock clock generators and some regional clock buffers to aid placement
- For interfaces requiring tight timing (e.g., source synchronous), lock specific resources; otherwise, lock only I/Os as a starting point

#### Clock Tree Topology

```tcl
report_clock_networks
```

- Utilize clock trees to minimize skew
- For PLL/MMCM outputs, use the same clock buffer type to minimize skew
- Look for unintended cascaded BUFG elements that introduce additional delay or skew

---

## Implementing the Design

### Using Project Mode vs. Non-Project Mode

| Mode | Characteristics |
|------|------------------|
| **Project Mode** | Runs management, file sets management, automatic report generation, cross-probing |
| **Non-Project Mode** | Easy integration, Tcl-driven — must explicitly call all desired reports |

### Strategies

Strategies control tool options and generated reports for synthesis and implementation runs in Project Mode.

> **Recommended:** Try the default strategy **Vivado Implementation Defaults** first — provides a good trade-off between compile time and maximum operating clock frequency.

> **Note:** Strategies are tool and version specific. Some strategies may require longer compile time.

### Directives

Directives provide different modes of behavior for implementation commands:

- `opt_design`
- `place_design`
- `phys_opt_design`
- `route_design`

> Use the **default directive** initially. Use other directives when the design nears completion to explore the solution space. Only one directive can be specified at a time.

### Iterative Flows

In Non-Project Mode, iterate between optimization commands with different options:

```tcl
phys_opt_design -directive AggressiveFanoutOpt
phys_opt_design -directive AlternateFlowWithRetiming
```

Running `phys_opt_design` iteratively provides timing improvement by optimizing progressively more critical paths. At post-route stage, `phys_opt_design` reroutes any unrouted nets automatically — no explicit `route_design` needed afterward.

### Analyzing a Design at Different Stages Using Checkpoints

Design checkpoint files (`.dcp`) save and restore the physical design database at key points:

```tcl
write_checkpoint <filename>.dcp
read_checkpoint <filename>.dcp
```

Checkpoint files include:

- Current netlist (including implementation optimizations)
- Design constraints
- Implementation results

**Common uses:**

- Save results for later analysis at a specific flow stage
- Try `place_design` with multiple directives, save each checkpoint, then select the best for subsequent steps

> **Note:** In Project Mode, checkpoints are generated automatically in the implementation runs directory.

### Using Interactive Report Files

Generate interactive reports (`.rpx`) alongside checkpoints for immediate analysis in the Vivado IDE:

```tcl
report_timing_summary -rpx timing_summary.rpx
report_timing -rpx timing.rpx
report_power -rpx power.rpx
report_methodology -rpx methodology.rpx
report_drc -rpx drc.rpx
```

> **Recommended:** Use the `catch` command to prevent errors from stopping the flow:
> ```tcl
> catch {report_timing_summary -rpx timing_summary.rpx -file timing_summary.rpt}
> ```

---

## Using Incremental Implementation Flows

Reuses existing placement and routing data to reduce compile time and produce more predictable results.

> **Recommended:** Include incremental implementation in flow scripts early in the design cycle so it can be enabled during critical periods.

### Automatic Incremental Implementation Mode

Activates the incremental flow but lets the Vivado tools decide at `read_checkpoint` time whether to use default or incremental algorithms, based on the reference checkpoint and current design.

> **Note:** Automatic mode is less aggressive than the default incremental flow, enabling better QoR maintenance.

**Project Mode:**

```tcl
set_property AUTO_INCREMENTAL_CHECKPOINT 1 [get_runs <runName>]
```

Or right-click an implementation run → Set Incremental Compile → Automatically use the checkpoint from the previous run.

**Non-Project Mode:**

```tcl
read_checkpoint -incremental -auto_incremental <reference>.dcp
```

When updating the checkpoint, ensure WNS did not degrade beyond acceptable limits:

```tcl
if {[get_property SLACK [get_timing_path -setup]] > -0.250} {
    file copy -force <postroute>.dcp <reference>.dcp
}
```

### Incremental Directives and Target WNS

| Incremental Directive | Target WNS Behavior |
|-----------------------|---------------------|
| `RuntimeOptimized` | Same as the reference checkpoint |
| `TimingClosure` | 0.000 |
| `Quick` | Not timing driven — placement driven by related logic |

> **Note:** Incremental directives replace directive mapping from previous releases. When the default flow algorithms are used, incremental directives are ignored and `place_design`/`route_design` directives take effect.

### Configuring the Incremental Flow

```tcl
report_config_implementation
config_implementation { {incr.ignore_user_clock_uncertainty true} }
```

Configurable elements:

- Minimum thresholds for cell matching, net matching, and WNS in automatic incremental flow
- Behavior when automatic incremental criteria not met: `Terminate` (stop flow) or `SwitchToDefaultFlow` (continue with defaults)
- Whether to ignore user clock uncertainty constraints used to overconstrain the placer

### Parallel Runs

For default flow, implement many parallel runs with different placer directives. For incremental flows, target the desired incremental directive with different reference checkpoints to achieve a spread of results.

### Compile Time Considerations

| Directive | Compile Time Impact |
|-----------|---------------------|
| `RuntimeOptimized` | Up to 50% reduction when ≥95% design reuse; benefit declines with less reuse |
| `TimingClosure` | May increase compile time — extra algorithms to close timing, especially in congested areas with timing failures |

> When the reference checkpoint meets timing, `TimingClosure` compile time reduction is similar to `RuntimeOptimized`.

---

## Implementation Steps

### Logic Optimization (opt_design)

Optimizes the current in-memory netlist — the first view of the assembled design (RTL + IP blocks).

**Default optimizations:**

- Logic trimming
- Removal of cells with no loads
- Constant input propagation
- Block RAM power optimization

**Optional optimizations:**

- Remap — combines LUTs in series into fewer LUTs to reduce path depth

**Analysis:**

```tcl
opt_design
report_utilization
opt_design -verbose -debug_log  ;# detailed optimization impact and constraint blocking info
```

### Placement (place_design)

Positions cells from the netlist onto specific sites in the target device.

**Post-placement analysis:**

| Condition | Action |
|-----------|--------|
| Very large negative setup slack | Check constraints for completeness/correctness; consider logic restructuring |
| Very large negative hold slack | Likely incorrect constraints or bad clocking topologies — fix before routing |
| Small negative hold slack | Likely fixed by the router |

```tcl
report_timing_summary
report_clock_utilization  ;# view clock resource and load counts by clock region
```

### Physical Optimization (phys_opt_design)

Optional timing-driven optimization on negative-slack paths. Performs replication, retiming, hold fixing, and placement improvement. No subsequent `place_design` is required.

**When to use:**

- High fanout critical paths → benefit from fanout optimization
- High-fanout data/address/control nets of large RAM blocks (multiple block RAMs) failing timing after routing → benefit from **Forced Net Replication**

> Evaluate timing after placement to determine if physical synthesis is needed.

### Routing (route_design)

Routes the placed design and optimizes for hold time violations. Default behavior balances compile time and operating clock frequency while alleviating congestion.

**Route analysis:**

- Sub-optimal routing often results from incorrect timing constraints
- Validate constraints and timing reports from the placed design before experimenting with router settings
- Congested areas can be addressed via targeted fanout optimization in RTL/synthesis or physical optimization
- Preserve design hierarchy to prevent cross-boundary optimization and reduce netlist density
- Use floorplan constraints to ease congestion

#### Route Compile Time

```tcl
route_design -ultrathreads
```

Gives the router extra freedom to execute multiple threads — routing finishes faster but with slightly different results each run. Slack between identical runs differs by a fractional percentage.

> Use this option only if your environment does not require strictly repeatable results.

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| Start with default synthesis settings and strategies | Best results for majority of designs; adjust based on specific needs |
| Use incremental synthesis for large designs | ~50% compile time reduction with good QoR |
| Prefer `default` or `aggressive` incremental mode for high-performance designs | Enables cross-boundary optimizations |
| Run `report_drc` early and fix violations | Prevents downstream timing and logic issues |
| Run `report_methodology` at first synthesis and after significant changes | Catches compliance issues before they become blocking |
| Review synthesis log Critical Warnings and Warnings | Ensures tool messages match design intent |
| Use `report_qor_assessment` after significant netlist updates | Provides 1–5 score predicting timing closure likelihood |
| Analyze timing post-synthesis before proceeding | HDL changes have the biggest QoR impact — fix early |
| Use `MAX_FANOUT` sparingly; prefer placement-based replication | `phys_opt_design` replication is more effective than synthesis-level |
| Remove `KEEP`/`DONT_TOUCH` when no longer needed | These attributes increase area and power |
| Run `phys_opt_design` iteratively for timing improvement | Each iteration optimizes progressively more critical paths |
| Include incremental implementation in flow scripts early | Ready to enable during critical design cycle periods |
| Use `report_clock_networks` and `report_clock_utilization` | Validates clock tree topology and resource usage |
| Use checkpoints to save intermediate results | Enables trying multiple directives and selecting the best result |

---

## Quick Reference

### Key Tcl Commands

| Command | Purpose |
|---------|---------|
| `synth_design -incremental_mode <mode>` | Run incremental synthesis (off/quick/default/aggressive) |
| `set_property BLOCK_SYNTH.<opt> <val> [get_cells <inst>]` | Block-level synthesis strategy per hierarchy |
| `report_drc` | Run design rule checks |
| `report_methodology` | Run methodology compliance checks |
| `report_qor_assessment` | Post-synthesis QoR score (1–5) |
| `report_utilization` | Resource utilization report |
| `report_clock_utilization` | Clock primitive utilization |
| `report_clock_networks` | Clock network detail tree view |
| `report_timing -no_net_delay` | Evaluate path timing without net delay |
| `opt_design` | Logic optimization |
| `place_design` | Placement |
| `phys_opt_design` | Physical optimization (optional, timing-driven) |
| `route_design` | Routing |
| `route_design -ultrathreads` | Faster routing (non-repeatable) |
| `write_checkpoint` / `read_checkpoint` | Save/restore design checkpoints |
| `set_property AUTO_INCREMENTAL_CHECKPOINT 1 [get_runs <run>]` | Enable automatic incremental implementation |
| `read_checkpoint -incremental -auto_incremental <ref>.dcp` | Non-Project Mode automatic incremental |
| `config_implementation` / `report_config_implementation` | Configure/view incremental flow settings |

### QoR Assessment Scoring

| Score | Meaning |
|-------|---------|
| 1 | Will likely not complete implementation |
| 2 | Will complete but not meet timing |
| 3 | Unlikely to meet timing |
| 4 | Will likely meet timing |
| 5 | Will meet timing |

### Incremental Synthesis Mode Comparison

| Mode | Cross-Boundary Opt | Compile Time | Recommended For |
|------|---------------------|--------------|-----------------|
| `off` | N/A (full synthesis) | Full | Max QoR |
| `quick` | No | Fastest | Low-performance designs |
| `default` | Yes | Significantly reduced | Most designs |
| `aggressive` | Yes | Significantly reduced | High-performance designs |

---

## Source Attribution

- **Source:** UG949 (v2025.2) — UltraFast Design Methodology Guide for FPGAs and SoCs, Chapter 5: Design Implementation (pages 188–208)
- **Related Documents:** UG901 (Synthesis), UG904 (Implementation), UG906 (Design Analysis and Closure Techniques), UG892 (Design Flows Overview), UG895 (System-Level Design Entry)
