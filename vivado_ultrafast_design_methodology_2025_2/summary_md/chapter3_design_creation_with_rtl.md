# Chapter 3: Design Creation with RTL

This chapter covers the RTL design creation process for AMD FPGAs, including defining optimal design hierarchy, working with IP, RTL coding guidelines for control signals, memory, DSP, and shift registers, clocking architecture and guidelines for UltraScale and 7 series devices, and clock domain crossing (CDC) best practices.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Defining Good RTL Design Hierarchy](#defining-good-rtl-design-hierarchy) | Hierarchy planning for I/O, clocking, floorplanning, and debug |
| [Working with IP](#working-with-ip) | IP catalog, customization, versioning, and AXI protocols |
| [RTL Coding Guidelines](#rtl-coding-guidelines) | Control signals, resets, clock enables, RAM/ROM, DSP, SRL inference |
| [Coding Styles to Improve Maximum Frequency](#coding-styles-to-improve-maximum-frequency) | Fanout management, pipelining, retiming, auto-pipelining |
| [Coding Styles to Improve Power](#coding-styles-to-improve-power) | Clock/data gating, case blocks, block RAM power trade-offs |
| [Running RTL DRCs](#running-rtl-drcs) | Methodology checks on elaborated design |
| [Clocking Guidelines](#clocking-guidelines) | UltraScale and 7 series clocking architecture, primitives, constraints |
| [Clock Domain Crossing](#clock-domain-crossing) | XPM CDC modules, MTBF optimization, constraining CDC |

---

## Defining Good RTL Design Hierarchy

A well-structured RTL hierarchy improves synthesis, placement, timing closure, and debug. Key principles:

### I/O Components Near Top Level

Place I/O-related components (IBUF, OBUF, IOBUF, ISERDES, OSERDES, IDELAY, ODELAY) at or near the top level of the design hierarchy. This simplifies board-level interfacing and constraint application.

### Clocking Elements Near Top Level

Instantiate clocking resources (MMCM, PLL, clock buffers) near the top of the hierarchy so that clocks can be easily distributed to multiple modules. Sharing clocking resources avoids redundancy, reduces power, and minimizes placement conflicts.

### Register at Logical Boundaries

Register outputs (and optionally inputs) at the boundary of each hierarchical module. This:

- Simplifies timing analysis by creating well-defined timing paths
- Facilitates module-level constraint development
- Enables better cross-boundary optimization or out-of-context synthesis

### Floorplanning Considerations

Group related logic so that each module maps naturally to a region of the device. If a module is too large for a single region, break it into sub-modules that can be individually constrained.

### Optimize for Debug

Design hierarchy with debug in mind:

- Expose key signals at module ports for probing
- Apply `MARK_DEBUG` attributes to internal signals of interest
- Use `KEEP_HIERARCHY` where needed to preserve debug access

### Apply Attributes at Module Level

Synthesis attributes such as `KEEP_HIERARCHY`, `SHREG_EXTRACT`, and `MAX_FANOUT` are most effective when applied at the module/entity level rather than individual signals.

### DSP Hierarchy Example

For DSP-heavy designs, separating the arithmetic pipeline into its own module allows:

- Targeted `KEEP_HIERARCHY` to prevent SRL absorption of pipeline registers
- Independent `SHREG_EXTRACT = "no"` on pipeline stages
- Better floorplanning of DSP blocks

---

## Working with IP

### Planning IP Requirements

Before selecting IP, understand:

- **AMBA AXI protocols** — AXI4, AXI4-Lite, and AXI4-Stream for interconnect compatibility
- Target device resource availability (block RAM, DSP, I/O)
- Clock domain requirements and expected throughput

### IP Catalog

The Vivado IP Catalog provides parameterizable IP cores that can be customized via:

- **GUI** — Interactive customization dialog with port/parameter configuration
- **Tcl** — Scripted IP generation for repeatable flows

### Custom IP and IP-XACT

Package custom RTL as IP-XACT components using the IP Packager. This enables reuse in Vivado IP Integrator block designs.

### IP Versioning and Revision Control

- Lock IP versions to avoid unexpected behavior during upgrades
- Use IP status reports to identify outdated IP
- Version-control the `.xci` files (IP customization) alongside RTL

---

## RTL Coding Guidelines

### HDL Templates

Use the Vivado Design Suite HDL Templates (accessible via **Tools → Language Templates**) for coding common structures: RAM, ROM, DSP, FIFO, shift registers, state machines, etc.

### Control Signals and Control Sets

A **control set** is the unique combination of clock, clock enable (CE), and set/reset (SR) driving a group of registers within a slice. Excessive unique control sets reduce packing density and increase power.

| Problem | Impact |
|---------|--------|
| Too many unique control sets | Increased utilization, decreased density, decreased frequency, increased power |
| Low-fanout clock enables | Main contributor to high control set count |

**Mitigation:** Close incomplete conditional (if/else) blocks with a defined constant value rather than infer a clock enable, especially for small groups of registers.

### Resets

#### When to Use Resets

- AMD devices initialize all registers to a known state via **Global Set/Reset (GSR)** during configuration
- Additional resets are only needed when a register must be re-initialized during operation
- Avoid resets on shift registers, pipeline registers, and synchronization registers

#### Synchronous vs. Asynchronous Resets

| Attribute | Synchronous Reset | Asynchronous Reset |
|-----------|-------------------|---------------------|
| **Timing analysis** | Covered by standard setup/hold | Requires recovery/removal timing |
| **Block RAM compatibility** | Compatible | Prevents output register inference |
| **DSP48 compatibility** | Compatible (only sync reset supported) | Prevents DSP mapping |
| **SRL compatibility** | SRL has no reset pin | SRL has no reset pin |
| **Recommendation** | ✅ Recommended | ⚠️ Avoid unless required by external interface |

> **Recommended:** Use synchronous resets. If an asynchronous reset is absolutely required, synchronize its deassertion to the clock domain.

#### DSP Multiplier Reset Impact

DSP48 slices contain only reset (not set) pins and support only synchronous reset. Coding a **set** (value = 1) or asynchronous reset around multipliers/adders prevents mapping to DSP blocks, increasing area and power.

### Reset and Clock Enable Precedence

In AMD devices, set/reset takes precedence over clock enable. Code reset **before** enable in if/else constructs:

```verilog
// Recommended: reset before enable
always @(posedge clk) begin
    if (reset)
        dout <= 0;
    else if (enable)
        dout <= din;
end
```

Coding clock enable first forces the reset into the data path and creates additional logic.

### Controlling Enable/Reset Extraction with Synthesis Attributes

| Attribute | Effect |
|-----------|--------|
| `DIRECT_ENABLE` | Forces a signal onto the CE pin of the register |
| `DIRECT_RESET` | Forces a signal onto the R/S pin of the register |
| `EXTRACT_ENABLE = "no"` | Pushes enable logic from CE pin to D pin (data path) |
| `EXTRACT_RESET = "no"` | Pushes reset logic from R/S pin to D pin |

**Control set threshold** (`-control_set_opt_threshold`):

| Device Family | Default Threshold |
|--------------|-------------------|
| 7 series | 4 |
| UltraScale | 2 |

When the load count equals or exceeds the threshold, synthesis maps through CE/R/S pins; below the threshold, synthesis maps through the D pin.

### Tips for Control Signals

- Check whether a global reset is really needed
- Avoid asynchronous control signals
- Keep clock, enable, and reset **polarities consistent**
- Do not code a set and reset into the same register
- If asynchronous reset required, synchronize its deassertion

---

## Know What You Infer

Understand hardware resource mapping from your code:

| RTL Construct | Resource Mapping | Notes |
|--------------|-----------------|-------|
| 8-bit adder | 8 LUTs + carry chain | Ternary add uses 1 LUT per 3 bits |
| Signed multiply < 18×25 (18×27 UltraScale) | 1 DSP block | 3 pipeline stages recommended |
| SRL depth ≤ 16 | 2 SRLs per LUT | Single SRL up to 32 bits in 1 LUT |
| 4:1 MUX | 1 LUT (1 level) | |
| 8:1 MUX | 2 LUTs + MUXF7 (1 level) | |
| 16:1 MUX | 4 LUTs + MUXF7 + MUXF8 (1 level) | |
| General logic ≤ 6 inputs | 1 LUT (1 level) | ~20 inputs max for 2 levels |

> ⚠️ Check availability of hardware resources and utilization early in the design cycle.

---

## Inferring RAM and ROM

### RAM Specification Methods

| Method | Advantages | Disadvantages |
|--------|-----------|---------------|
| **Inference** | Portable, readable, fast simulation | May not access all RAM configurations |
| **XPM (Parameterizable Macros)** | Portable across families, asymmetric width, predictable QoR | Limited to supported options |
| **Direct Instantiation** | Highest control, all capabilities | Less portable, more verbose |
| **IP Catalog** | Optimized multi-component result | Less portable, core management |

### Performance Considerations

- **Depth ≤ 64** → LUTRAM (2 bits/LUT for depth ≤ 32, 1 bit/LUT for depth ≤ 64)
- **Depth > 256** → Block RAM (various width/depth configurations)
- **Output pipeline register** — Required for high frequency; 2 registers (BRAM + slice) give read latency of 3
- **Input pipeline register** — Helps when RAM spans large area; replicate with `phys_opt_design`

### Preventing Block RAM Output Register Inference Issues

| Issue | Solution |
|-------|----------|
| Multi-fanout on read data output | Ensure fanout of 1 from memory array to output register |
| Asynchronous reset on read data register | Use synchronous reset only; reset value must be 0 |
| Reset on address register | Do not reset memory arrays |
| Feedback structures on registers | Avoid feedback; prevents register optimization |

### UltraRAM (UltraScale+ Only)

Available in certain UltraScale+ devices as a 4K×72 single-clock, dual-port memory block.

```verilog
// Key XPM parameters for UltraRAM
// MEMORY_PRIMITIVE = "ultra"
// READ_LATENCY — pipeline registers for optimal mapping
// CASCADE_HEIGHT — controls UltraRAM column height (default: 8)
```

- **Single column** — uses built-in hardware cascade, no fabric logic
- **Multiple columns** — uses hardware cascade + fabric logic; increase `READ_LATENCY` to maintain frequency

---

## Coding for Optimal DSP and Arithmetic Inference

DSP48 blocks support: multiplication, addition/subtraction, comparators, counters, general logic.

### DSP48 Best Practices

- **Fully pipeline** — use all internal pipeline stages for best performance and power
- **Use synchronous reset only** — asynchronous resets prevent DSP mapping
- **No set conditions** — DSP registers only support reset
- **Use signed values** — DSP uses signed arithmetic; unsigned values may lose bit precision
- **Pre-adder/post-adder** — exploit for FIR filters and systolic structures
- **Ternary addition** — 6-input LUT can do A+B+C with same resources as A+B

---

## Coding Shift Registers and Delay Lines

SRL16/SRL32 resources (integrated in LUTs) efficiently implement shift registers:

- **SRL16** — 2 SRLs per LUT (depth ≤ 16)
- **SRL32** — 1 SRL per LUT (depth ≤ 32)
- Support: clock, clock enable, serial data in/out, address inputs
- **No** set/reset pins — reset in RTL adds extra logic around SRL

> **Recommended:** Register the last stage of the shift register in a dedicated slice register for better clock-to-out timing. Use `SHREG_EXTRACT = "no"` to disable SRL inference and use flip-flops instead for placement flexibility.

### Initialization of All Inferred Registers, SRLs, and Memories

Initialize all synchronous elements in HDL to match the post-configuration hardware state:

```vhdl
signal reg1 : std_logic := '0';
signal reg2 : std_logic := '1';
signal reg3 : std_logic_vector(3 downto 0) := "1011";
```

```verilog
reg register1 = 1'b0;
reg register2 = 1'b1;
reg [3:0] register3 = 4'b1011;
```

---

## Deciding When to Instantiate or Infer

| Approach | When to Use |
|----------|-------------|
| **Infer** | Recommended default — portable, visible to optimizer |
| **Instantiate** | When inference doesn't meet timing/power/area, or features can't be inferred (DDR outputs in VHDL, I/O SerDes, hard FIFOs) |

> Use Vivado Language Templates for both inference coding styles and primitive instantiation.

---

## Coding Styles to Improve Maximum Frequency

### High Fanout Management

Identify high fanout nets after synthesis:

```tcl
report_high_fanout_nets
```

| Technique | Description |
|-----------|-------------|
| **Reduce loads** | Remove unnecessary connections to high-fanout control signals |
| **Balanced reset tree** | Manually replicate registers by hierarchy to balance fanout |
| **KEEP attribute** | Preserve duplicated registers (prefer over `DONT_TOUCH` to allow phys_opt) |

> ⚠️ Do **not** replicate CDC synchronization registers (protected by `ASYNC_REG`). Add an extra register after the synchronization chain instead.

#### Fanout Guidelines (Medium Performance 7 Series)

| Frequency Range | Fanout > 5000 | Fanout > 200 | Fanout > 100 |
|----------------|---------------|--------------|--------------|
| Low (1–125 MHz) | Few logic levels < 13 | N/A | N/A |
| Medium (125–250 MHz) | May need reduction | < 6 logic levels | N/A |
| High (> 250 MHz) | Not recommended | Small logic levels | Advanced pipelining required |

### Pipelining

- **Pipeline up front** — adding pipelining later propagates latency differences
- **Balance pipeline stages** — add stages to control path (narrower) rather than data path (wider)
- **Optimal LUT:FF ratio** is ~1:1
- **SSI devices** — pipeline SLR boundary crossings; prevent SRL inference on crossing paths

### Retiming

Use Vivado synthesis retiming to automatically redistribute registers across combinational logic:

```verilog
(* retiming_backward = 3 *) reg reg1;
(* retiming_backward = 2 *) reg reg2;
(* retiming_backward = 1 *) reg reg3;
```

Or use global retiming: `BLOCK_SYNTH.RETIMING` option.

### Determine Whether Pipelining is Needed

```tcl
report_design_analysis -logic_level_distribution
```

Identifies logic-level distribution per clock group and highlights paths with zero logic levels.

### Balance Pipeline Depth and SRL Usage

For deep pipelines, map registers into SRLs to save utilization. Control with `srl_style` attribute:

| Attribute Value | Structure |
|----------------|-----------|
| `"srl"` | SRL only |
| `"reg_srl"` | REG → SRL |
| `"srl_reg"` | SRL → REG |
| `"reg_srl_reg"` | REG → SRL → REG |

> ⚠️ Ensure no resets on pipeline stages intended for SRL inference. Use reset on first or last stage only.

### Auto-Pipelining

The auto-pipelining feature allows the placer to determine pipeline stage count and placement. Enable via:

- **AXI Register Slice core** — auto-pipelining mode
- **HDL attributes**: `autopipeline_module`, `autopipeline_group`, `autopipeline_limit`
- **XDC constraints**: `AUTOPIPELINE_MODULE`, `AUTOPIPELINE_GROUP`, `AUTOPIPELINE_LIMIT`

Apply proper timing constraints on targeted paths — insertion is timing-driven.

---

## Coding Styles to Improve Power

### Gate Clock or Data Paths

- `power_opt_design` can automatically generate gating logic
- Maximize elements affected by gating signal — gate at source rather than each load

### Use Clock Enable Pins of Dedicated Clock Buffers

Use CE ports of BUFGCE, BUFGCTRL, etc. instead of LUT-based clock gating.

### Use Case Block When Priority Encoder Not Needed

```verilog
// Inefficient — priority encoding via if-else
if (reg1) val = reg_in1;
else if (reg2) val = reg_in2;
else if (reg3) val = reg_in3;
else val = reg_in4;

// Efficient — parallel case
(* parallel_case *) casex ({reg1, reg2, reg3})
    3'b1xx: val = reg_in1;
    3'b01x: val = reg_in2;
    3'b001: val = reg_in3;
    default: val = reg_in4;
endcase
```

### Block RAM Power/Performance Trade-Off

Control with `CASCADE_HEIGHT` and `RAM_DECOMP` attributes:

| Configuration | Power | Frequency | Description |
|--------------|-------|-----------|-------------|
| `CASCADE_HEIGHT=1` | Highest (all BRAMs enabled) | Best | No cascading, parallel decode |
| `CASCADE_HEIGHT=N` (max) | Lowest (one BRAM active) | Lower | Full cascading, sequential decode |
| `CASCADE_HEIGHT` + `RAM_DECOMP="power"` | Balanced | Balanced | Controlled cascade + wider decomposition |

---

## Running RTL DRCs

Run methodology checks on the elaborated design:

1. Open Elaborated Design in the Flow Navigator
2. Select **RTL Analysis → Report Methodology** or run:

```tcl
report_methodology
```

These DRC rules identify potential coding issues with your HDL before synthesis.

---

## Clocking Guidelines

### UltraScale Device Clocking

UltraScale devices use a unified clocking structure (no separate regional clock buffers). Key characteristics:

- **Smaller, fixed-size clock regions** — number varies per device
- **24 vertical + 24 horizontal routing tracks** per clock region
- **24 vertical + 24 horizontal distribution tracks** per clock region
- Up to **24 unique clocks per clock region**
- Over **100 clock trees** depending on topology, fanout, and placement

#### Clock Types

| Type | Description |
|------|-------------|
| **High-Speed I/O Clocks** | PLL-generated for SelectIO bit slice logic; managed by AMD IP |
| **General Clocks** | Sourced by GCIO pin, MMCM/PLL, or fabric; driven by BUFGCE/BUFGCE_DIV/BUFGCTRL |
| **GT Clocks** | TX/RX/reference clocks for transceivers; use BUFG_GT for fabric connectivity |

#### Clock Primitives (per CMT)

| Resource | Count | Description |
|----------|-------|-------------|
| **PLL** | 2 | Clock generation |
| **MMCM** | 1 | Clock generation with fine phase control |
| **BUFGCE** | 24 | General clock buffer with enable |
| **BUFGCTRL** | 8 | Clock buffer with MUX control |
| **BUFGCE_DIV** | 4 | Clock buffer with simple division |
| **BUFG_GT** | 24 per GT clock region | GT user clock buffer with dynamic division |

#### BUFGCE

Most commonly used buffer — general clock buffer with clock enable/disable. Equivalent to 7 series BUFHCE.

#### BUFGCE_DIV

Simple clock division (/1, /2, /3, /4, /5, /6, /7, /8). More power efficient than MMCM for simple division. Can show less skew between clock domains compared to MMCM/PLL. Replacement for 7 series BUFR.

#### BUFGCTRL (BUFGMUX)

Used for multiplexing two or more clock sources to a single clock network.

#### BUFG_GT

Connects GT clocks to the global clock network. Includes built-in dynamic clock division. Used as regional buffer with loads in 1–2 adjacent clock regions.

### Clock Routing, Root, and Distribution

1. **Buffer → Clock Root**: Signal travels on routing tracks (same track ID 0–23)
2. **Clock Root**: Transitions from routing to distribution track; placed at center of clock window for minimal skew
3. **Root → Loads**: Travels on vertical then horizontal distribution tracks to CLB leaf clock routing

> Only routing/distribution segments actually used are consumed — no waste in clock regions without loads.

### Clock Tree Placement and Routing

Placement occurs in three phases:

1. **I/O and clock placement** — I/O buffers, MMCM/PLLs, clock buffers assigned to clock regions
2. **SLR partitioning + global placement** — Initial clock tree implementation; excessive clock window overlap causes errors
3. **Clock tree pre-routing** — Guides subsequent steps and provides accurate delay estimates

### Clock Constraints

#### LOC Constraints

| Object | Behavior |
|--------|----------|
| Clock input (GCIO, PACKAGE_PIN) | MMCM/PLL and buffers placed in same clock region |
| MMCM or PLL | Connected buffers/ports placed in same clock region |
| GT*_CHANNEL | BUFG_GTs placed in same clock region |

> ⚠️ Do **not** use LOC constraints on clock buffer cells in UltraScale devices — forces specific track ID, may cause unroutable clocks.

#### CLOCK_REGION Property

Assign a clock buffer to a clock region without specifying a site:

```tcl
set_property CLOCK_REGION X2Y2 [get_cells clkgen/clkout2_buf]
```

Preferred over LOC for clock buffers — gives placer more flexibility.

#### USER_CLOCK_ROOT Property

Force clock root location on a clock net:

```tcl
set_property USER_CLOCK_ROOT X2Y3 [get_nets clkgen/wbClk_o]
```

Query actual clock root:

```tcl
get_property CLOCK_ROOT [get_nets clkgen/wbClk_o]
report_clock_utilization -clock_roots_only
```

#### CLOCK_DELAY_GROUP Constraint

Match insertion delay of multiple related clock networks:

```tcl
set_property CLOCK_DELAY_GROUP grp12 [get_nets {clk1_net clk2_net}]
```

Commonly used for synchronous CDC paths between clocks from the same MMCM/PLL.

#### CLOCK_DEDICATED_ROUTE Constraint

| Value | Use | Behavior |
|-------|-----|----------|
| `TRUE` (default) | Clock nets | Buffer and MMCM/PLL must be in same clock region |
| `SAME_CMT_COLUMN` | Buffer → MMCM/PLL in same column | Vertically adjacent clock regions; global clock resources only |
| `ANY_CMT_COLUMN` | Buffer → MMCM/PLL in any region | Non-vertically adjacent; global clock resources only |
| `FALSE` | Non-buffer-driven clock nets | Routes with fabric + global resources; ⚠️ adversely affects timing |

#### CLOCK_LOW_FANOUT Constraint

Contain loads of a clock buffer in a single clock region:

```tcl
# On a clock net (< 2000 loads):
set_property CLOCK_LOW_FANOUT TRUE [get_nets -of [get_pins clkOut0_bufg_inst/O]]

# On flip-flops (opt_design creates parallel buffer):
set_property CLOCK_LOW_FANOUT TRUE [get_cells safeClockStartup_reg[*]]
```

### Clocking Capability

| Scenario | Max Clocks | Notes |
|----------|-----------|-------|
| ≤ 24 clocks | All high-fanout OK | No special considerations |
| ~288 clocks | Low-fanout only | 6 rows × 2 windows × 24 clocks (3 CR each) |
| Balanced mix | 12–24 HF + multiple LF per GT Quad | HF: 12 (monolithic), 24 (SSI) |

### Clocking Topology Recommendations

#### Parallel Clock Buffers (Recommended)

- Ensures predictable placement across runs
- Matches insertion delays between branches
- Preferred over cascaded buffers for synchronous paths

#### Cascaded Clock Buffers (Use with Caution)

- Useful for routing clocks to different clock regions or balancing clock buffer levels
- Keep cascaded buffers in same or adjacent clock regions
- Use `DONT_TOUCH="TRUE"` to prevent `opt_design` from removing them
- For 5:1 to 8:1 MUX, use cascaded BUFGCTRL (dedicated cascade paths)

> Prefer two cascaded BUFGCTRLs over cascaded BUFGCEs — dedicated routing with minimum delay.

### PLL/MMCM Feedback Path and Compensation

| Mode | Feedback Required | Notes |
|------|-------------------|-------|
| **INTERNAL** | No | Remove unnecessary feedback buffers to save resources |
| **ZHOLD / BUF_IN** | Yes | Placer matches clock root for feedback and CLKOUT0 buffers |

Use `CLOCK_DELAY_GROUP` or `USER_CLOCK_ROOT` to match insertion delay with other MMCM outputs.

### BUFG_GT Divider

Use BUFG_GT's built-in divider instead of MMCM/BUFGCE_DIV for simple GT clock division.

### SelectIO Clocking

#### ISERDESE3 / IDDRE1

Use **local inversion** on CLK_B/CB pins instead of MMCM CLKOUT0B — guarantees maximum skew requirement and uses fewer resources.

#### OSERDESE3

Use parallel BUFGCE + BUFGCE_DIV from a single MMCM output — removes additional clock uncertainty between two MMCM outputs.

### I/O Timing with MMCM ZHOLD/BUF_IN Compensation

- ZHOLD aligns MMCM to compensate I/O register hold timing
- Force clock root placement near I/O registers for less variability:

```tcl
report_clock_utilization -clock_roots_only
set_property USER_CLOCK_ROOT X0Y0 [get_nets <feedback_net>]
set_property USER_CLOCK_ROOT X0Y0 [get_nets <clkout0_net>]
```

### Synchronous CDC

For synchronous CDC between MMCM/PLL outputs, use BUFGCE_DIV to avoid phase error:

- Connect two BUFGCE_DIVs to a single MMCM CLKOUT
- One divides by 1, the other by 2 (or /4, /8)
- Use the **same buffer type** for both — BUFGCE and BUFGCE_DIV have different cell delays

> ⚠️ Both BUFGCE_DIV cells must use the **same CE and RST signals** to maintain phase alignment.

Use `CLOCK_DELAY_GROUP` to balance multiple related clock networks:

```tcl
set_property CLOCK_DELAY_GROUP grp12 [get_nets {clk_fb_net clk0_net clk1_net}]
```

> **Recommended:** Use the Clocking Wizard for optimal clocking structures with auto-generated constraints.

### GT Interface Clocking

#### BUFG_GT with Dynamic Divider

Replaces the need for MMCM in simple GT clock division. Each `BUFG_GT_SYNC` is required for synchronizing reset/clear (auto-inserted by tools if missing).

#### Single Quad vs. Multi-Quad Interface

- **Multi-quad**: Master channel generates `[RT]XUSRCLK[2]` for all channels; max 2 clock regions above/below reference clock source
- **Single quad**: Placer treats BUFG_GT clocks as local; loads placed in horizontally adjacent clock regions

#### RXUSRCLK/TXUSRCLK Skew Matching

When `[RT]XUSRCLK2` = half frequency of `[RT]XUSRCLK`:

- GT channels max 2 clock regions above/below master
- Placer assigns BUFG_GT pairs to upper or lower 12 BUFG_GTs in a Quad

#### PCIe CORECLK/PIPECLK/USERCLK

Three clocks from TXOUTCLK via BUFG_GTs with tight skew requirements. Placer assigns same clock root for all three.

### 7 Series Device Clocking

| Resource | Type | Scope |
|----------|------|-------|
| BUFG / BUFGCE / BUFGMUX / BUFGCTRL | Global | Up to 32 per device |
| BUFH / BUFHCE | Regional (horizontal) | 1 clock region; low-skew between adjacent left/right regions |
| BUFR | Regional | Up to 3 clock regions (via BUFMR) |
| BUFIO | I/O | Single I/O bank |
| BUFMR | Multi-regional | Drives BUFR/BUFIO across up to 3 vertical clock regions |

#### BUFHCE for Clock Gating

Use BUFHCE with BUFGs for medium-grained clock gating (hundreds to thousands of loads). A BUFG can drive multiple BUFHCEs in different clock regions for individual clock control.

### Additional Clocking Considerations for SSI Devices

- BUFMR cannot cross SLR boundaries — place driving clocks in center clock region of SLR
- ≤ 16 BUFGs: no additional considerations
- 17–32 BUFGs: careful pin selection and placement needed
- > 32 BUFGs: use BUFR/BUFH for smaller domains; SLR clock spine isolation possible

> **Recommended:** Place global clocks driving multiple SLRs in the **center SLR** for even distribution and minimal skew.

### Designing the Clock Structure

| Method | Description |
|--------|-------------|
| **Inference** | Vivado synthesis auto-infers BUFG up to architecture max |
| **Synthesis constraints** | Use `CLOCK_BUFFER_TYPE` to prevent/replace/add clock buffers |
| **IP** | Clocking Wizard, IO Wizard for MMCM/PLL/buffer configuration |
| **Instantiation** | Direct control over all clocking resources; place in top-level module |

### Controlling Phase, Frequency, Duty-Cycle, and Jitter

#### MMCM and PLL

- Use **Clocking Wizard** for proper configuration
- Do not leave inputs floating; connect RST to user logic
- Use LOCKED output in reset implementation (synchronize before use)
- Confirm CLKFBIN/CLKFBOUT connectivity

> Use BUFGCE_DIV instead of BUFGCE on UltraScale to avoid MMCM phase error penalty on synchronous CDC paths.

#### Using Gated Clocks

- Do **not** code clock gating in HDL — use clock enables instead
- Use `-gated_clock_conversion auto` in Vivado synthesis for automatic conversion
- Use `GATED_CLOCK` attribute for complex structures
- Gate large domains with BUFGCE/BUFGCTRL/BUFGCE_DIV/BUFG_GT

### Controlling and Synchronizing Device Startup

After configuration, GSR deassertion followed by GWE release — design enters operation. Methods for controlled startup:

1. Use clock enables and local synchronized resets on critical logic (state machines)
2. Instantiate clock buffers with CE; delay reset release by N cycles
3. Use **Safe Clock Startup** option in Clocking Wizard (MMCM LOCKED → BUFGCE/CE)

### Clocking for Dynamic Function eXchange (DFX)

| Clock Type | Description | Recommendation |
|-----------|-------------|----------------|
| **RM Internal** | Driver and loads inside reconfigurable module | Clock root at center of RP Pblock — best flexibility |
| **Boundary** | Crosses RM/static boundary | Use `USER_CLOCK_ROOT` to constrain root location |

### Avoiding Local Clocks

Local clocks (fabric-routed) cause unpredictable skew and routing problems. Common causes:

- Clock divided by fabric counter
- Clock gating not fully converted
- Too many clock buffers (7 series)

```tcl
report_clock_utilization
```

### Creating an Output Clock

Use **ODDR** component (D1=0, D2=1 for 180° phase shift). For fine phase control, use MMCM/PLL with external feedback compensation.

---

## Clock Domain Crossing

### XPM CDC Modules

AMD provides XPM (Xilinx Parameterizable Macro) modules for safe CDC:

#### Single-Bit CDC

| Scenario | XPM Module |
|----------|-----------|
| Synchronous reset crossing | `XPM_CDC_SYNC_RST` |
| Asynchronous reset crossing | `XPM_CDC_ASYNC_RST` |
| Pulse transfer | `XPM_CDC_PULSE` |
| Generic single-bit | `XPM_CDC_SINGLE` |

#### Multi-Bit CDC

| Scenario | XPM Module |
|----------|-----------|
| Static data | No CDC needed — use `report_cdc` waivers |
| Counter (gray-coded) | `XPM_CDC_GRAY` |
| Buffered, every-cycle transfer | `XPM_FIFO_ASYNC` |
| All bits on same cycle required | `XPM_CDC_HANDSHAKE` |
| Independent bits | `XPM_CDC_ARRAY_SINGLE` |

### Optimizing for MTBF

Total MTBF depends on:

- Number of asynchronous CDC points
- Number of synchronizer stages per crossing (`DEST_SYNC_FF`)
- Destination FF frequency
- Source toggle rate

### Selecting DEST_SYNC_FF

Iterative process:

1. Implement design
2. For **7 series**: use default value (conservative)
3. For **UltraScale**: run `report_synchronizer_mtbf`, iterate to balance MTBF vs. latency vs. resources

### Constraining CDC Correctly

- XPM CDCs provide their own `set_max_delay -datapath_only` constraints
- XPM CDCs are **not compatible** with `set_clock_groups` (higher precedence overwrites XPM constraints)

---

## Best Practices

1. **Register module boundaries** to simplify timing and enable out-of-context synthesis
2. **Use synchronous resets** — avoid asynchronous resets on DSP, block RAM, and SRL paths
3. **Initialize all registers** in HDL to eliminate GSR-only dependency
4. **Minimize control sets** — close if/else blocks, keep consistent polarities
5. **Fully pipeline DSP48 blocks** with 3 register stages for best performance and power
6. **Use output registers on block RAM** — 2 levels recommended (BRAM + slice)
7. **Prefer inference** over instantiation — let synthesis optimize across boundaries
8. **Monitor fanout** with `report_high_fanout_nets` after synthesis
9. **Pipeline early** rather than retrofitting — reduces timing closure difficulty
10. **Use XPM CDC modules** instead of custom synchronizers for reliable CDC
11. **Use Clocking Wizard** for MMCM/PLL configuration — validated settings with auto-constraints
12. **Parallel clock buffers** preferred over cascaded for synchronous paths
13. **Use CLOCK_DELAY_GROUP** for matching insertion delay between related clock domains
14. **Place global clocks in center SLR** for SSI devices to minimize skew
15. **Run `report_methodology`** on elaborated design to catch RTL coding issues early

---

## Quick Reference

| Topic | Key Command / Attribute |
|-------|------------------------|
| Report high fanout | `report_high_fanout_nets` |
| Logic level distribution | `report_design_analysis -logic_level_distribution` |
| RTL DRCs | `report_methodology` (on elaborated design) |
| Clock utilization | `report_clock_utilization` |
| Clock root query | `report_clock_utilization -clock_roots_only` |
| Synchronizer MTBF | `report_synchronizer_mtbf` |
| Force direct enable | `(* DIRECT_ENABLE = "yes" *)` |
| Force direct reset | `(* DIRECT_RESET = "yes" *)` |
| Disable SRL inference | `(* SHREG_EXTRACT = "no" *)` |
| SRL style | `(* srl_style = "reg_srl_reg" *)` |
| Retiming | `(* retiming_backward = N *)` or `BLOCK_SYNTH.RETIMING` |
| Clock buffer type | `CLOCK_BUFFER_TYPE` synthesis attribute |
| UltraRAM inference | `(* ram_style = "ultra" *)` |
| RAM power decomposition | `(* RAM_DECOMP = "power" *)` |
| Auto-pipelining | `(* autopipeline_module = "yes" *)` |
| Clock low fanout | `set_property CLOCK_LOW_FANOUT TRUE` |
| Clock delay group | `set_property CLOCK_DELAY_GROUP <name>` |
| Clock root | `set_property USER_CLOCK_ROOT <region>` |

---

## Source Attribution

- **Source:** UG949 — *UltraFast Design Methodology Guide for FPGAs and SoCs*, v2025.2, November 20, 2025
- **Chapter:** 3 — Design Creation with RTL (pages 43–145)
