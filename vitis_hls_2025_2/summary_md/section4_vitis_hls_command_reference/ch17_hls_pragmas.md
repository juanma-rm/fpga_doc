# Chapter 17 — HLS Pragmas

> Source: *Vitis HLS User Guide* UG1399 v2025.2, Chapter 17 (pp. 541–607)

## Table of Contents

| Pragma | Category |
|---|---|
| [aggregate](#pragma-hls-aggregate) | Struct/Array Packing |
| [alias](#pragma-hls-alias) | M_AXI Pointer Aliasing |
| [allocation](#pragma-hls-allocation) | Resource Utilization |
| [array_partition](#pragma-hls-array_partition) | Array Optimization |
| [array_reshape](#pragma-hls-array_reshape) | Array Optimization |
| [array_stencil](#pragma-hls-array_stencil) | Array Optimization |
| [bind_op](#pragma-hls-bind_op) | Resource Binding |
| [bind_storage](#pragma-hls-bind_storage) | Resource Binding |
| [cache](#pragma-hls-cache) | M_AXI Cache |
| [dataflow](#pragma-hls-dataflow) | Task-Level Pipelining |
| [dependence](#pragma-hls-dependence) | Loop Dependency Control |
| [disaggregate](#pragma-hls-disaggregate) | Struct Deconstruction |
| [expression_balance](#pragma-hls-expression_balance) | Expression Optimization |
| [function_instantiate](#pragma-hls-function_instantiate) | Resource Utilization |
| [inline](#pragma-hls-inline) | Function Inlining |
| [interface](#pragma-hls-interface) | Interface Synthesis |
| [latency](#pragma-hls-latency) | Timing Constraints |
| [loop_flatten](#pragma-hls-loop_flatten) | Loop Optimization |
| [loop_merge](#pragma-hls-loop_merge) | Loop Optimization |
| [loop_tripcount](#pragma-hls-loop_tripcount) | Loop Analysis |
| [occurrence](#pragma-hls-occurrence) | Pipeline Optimization |
| [performance](#pragma-hls-performance) | High-Level Performance Goals |
| [pipeline](#pragma-hls-pipeline) | Loop/Function Pipelining |
| [protocol](#pragma-hls-protocol) | Cycle-Accurate Region |
| [reset](#pragma-hls-reset) | Reset Control |
| [stable](#pragma-hls-stable) | Stable Signal Declaration |
| [stream](#pragma-hls-stream) | FIFO Stream Substitution |
| [top](#pragma-hls-top) | Top-Function Naming |
| [unroll](#pragma-hls-unroll) | Loop Unrolling |

---

## pragma HLS aggregate

**Description:** Groups all struct fields into a single wide scalar word rather than separate ports/signals.

```c
#pragma HLS aggregate variable=<variable> compact=[bit|byte|none|auto]
```

- First struct element → LSB; last element → MSB.
- Arrays inside the struct are completely partitioned and reshaped, then packed with scalar fields.
- `compact=bit` — no padding (tightly packed).
- `compact=byte` — byte-level alignment (padded).
- `compact=none` — no aggregation.
- `compact=auto` — tool decides (default).

> ⚠️ Caution: a 4096-element `int` array inside a struct produces a 131072-bit port that is unlikely to route.

---

## pragma HLS alias

**Description:** Declares that two or more `m_axi` pointer arguments point to the same underlying memory buffer. Enables proper data dependency analysis across pointers.

```c
#pragma HLS alias ports=<list> [distance=<int> | offset=<list>]
```

- `distance` and `offset` are mutually exclusive.
- `distance` — integer offset between pointer values passed to each port.
- `offset` — one offset per port specifying position relative to the shared array origin.

**Requirements:**
- All aliased ports must be in **different** M_AXI bundles.
- All ports must have the same depth.
- One offset entry per port when `offset=` is used.
- Interface `offset` must be `slave` or `direct` (not `off`).

---

## pragma HLS allocation

**Description:** Limits the number of RTL instances of functions or operations.

```c
#pragma HLS allocation <type> instances=<list> limit=<value>
```

- `type` = `function` or `operation`.
- Template functions: use `foo<DT>` syntax, not `foo`.
- Applies only within the scope of the enclosing function or loop.

**Example:** Limit multipliers to 1:
```c
#pragma HLS allocation operation instances=mul limit=1
```

---

## pragma HLS array_partition

**Description:** Partitions an array into smaller arrays or individual elements, increasing available read/write ports.

```c
#pragma HLS array_partition variable=<name> type=<type> [factor=<int>] [dim=<int>] [off=true]
```

| `type` | Behavior |
|---|---|
| `complete` (default) | Decompose into individual elements (registers) |
| `block` | Split into `factor` consecutive chunks |
| `cyclic` | Interleave elements round-robin into `factor` arrays |

- `factor` required for `block` and `cyclic`.
- `dim=0` applies partitioning to all dimensions; default is `dim=1`.
- `off=true` disables partitioning for the specified variable.

> **Not supported** for M_AXI interface arguments at the top level. Use `hls::vector` instead.

---

## pragma HLS array_reshape

**Description:** Like `array_partition` but merges the resulting sub-arrays back into a single array with fewer elements and wider words. Reduces element count, increases bit-width.

```c
#pragma HLS array_reshape variable=<name> type=<type> [factor=<int>] [dim=<int>] [off=true]
```

- Same `type` options as `array_partition`: `complete`, `block`, `cyclic`.
- `object` keyword: apply reshape to objects *inside* a container array (preserves container dimensions).
- Useful when you want more memory bandwidth without creating separate arrays.

> **Not supported** for M_AXI interface arguments.

---

## pragma HLS array_stencil

**Description:** Disables automatic stencil window buffer inference for a specific array within a loop.

```c
#pragma HLS array_stencil variable=<name> off
```

**Global control:** `config_array_stencil -throughput_driven <off|on>`

**Restrictions for auto stencil to be applied:**
- Must be inside a top-level loop.
- Loop bounds must be constant.
- Pragma must be inside the loop.
- Pipeline II = 1 required.
- Perfect nested loops only.
- Fixed access pattern (increment ±1 only).

---

## pragma HLS bind_op

**Description:** Maps a specific arithmetic operation for a given variable to a chosen hardware implementation and sets its pipeline latency.

```c
#pragma HLS bind_op variable=<variable> op=<type> impl=<value> [latency=<int>]
```

**Functional ops:**

| `op` | `impl` options | Latency range |
|---|---|---|
| `mul`, `add`, `sub` | `fabric`, `dsp` | 0–4 |

**Floating-point ops** (single `f`, double `d`, half `h` prefix):

| `op` | `impl` options |
|---|---|
| `fadd`, `fsub` | `fabric` (0–13), `fulldsp` (0–12), `primitivedsp` (0–3) |
| `fmul` | `fabric` (0–9), `meddsp`/`fulldsp` (0–9), `maxdsp` (0–7), `primitivedsp` (0–4) |
| `fdiv`, `fsqrt`, `frsqrt`, `frecip`, `fexp`, `flog` | `fabric`, `meddsp`, `fulldsp` (ranges vary) |
| `dadd`, `dsub` | `fabric` (0–13), `fulldsp` (0–15) |
| `dmul` | `fabric` (0–10), `meddsp`/`fulldsp` (0–13), `maxdsp` (0–14) |
| `hadd`, `hsub` | `fabric` (0–9), `meddsp`/`fulldsp` (0–12) |
| `hmul` | `fabric` (0–7), `fulldsp` (0–7), `maxdsp` (0–9) |

- `primitivedsp` is **Versal only**.
- Using `BIND_OP` to force DSP can **prevent** compiler multi-operation matching (MULADD, AMA, ADDMUL).

---

## pragma HLS bind_storage

**Description:** Assigns an array or variable to a specific memory type and implementation resource.

```c
#pragma HLS bind_storage variable=<variable> type=<type> [impl=<value>] [latency=<int>]
```

> For top-level function arguments, use the `INTERFACE` pragma with `storage_type`/`storage_impl` options instead.

**Storage types:**

| Type | Description |
|---|---|
| `fifo` | FIFO buffer |
| `ram_1p` | Single-port RAM |
| `ram_1wnr` | 1 write, N read ports (N banks internally) |
| `ram_2p` | Dual-port: read on one, read/write on other |
| `ram_s2p` | Dual-port: read only / write only |
| `ram_t2p` | True dual-port: read+write on both ports |
| `rom_1p` | Single-port ROM |
| `rom_2p` | Dual-port ROM |
| `rom_np` | Multi-port ROM |

**Implementations:** `auto`, `bram`, `bram_ecc`, `lutram`, `uram`, `uram_ecc`, `srl`, `memory`

- `bram_ecc` and `uram_ecc` supported for all types except ROM.
- PIPO + single-port → **merged-PIPO** (one bank, reader/writer use different halves).
- PIPO + dual-port → **split-PIPO** (separate banks per block).
- FIFO latency: 1–4; RAM/ROM latency: 1–3.
- FIFO read-after-write latency is **global only**: `config_storage fifo -read_after_write_latency N`

---

## pragma HLS cache

**Description:** Adds a read cache to an M_AXI port to reduce average DRAM access latency by exploiting locality of reference.

```c
#pragma HLS cache port=<name> lines=<value> depth=<value> [ports=<N>] [l2_lines=<M>]
```

**Single-port mode** (default):
- Direct-mapped, read-only cache on one M_AXI port.
- `lines` — number of cache lines.
- `depth` — words per line (power-of-2); defaults to max burst length (default 16).

**Multi-port mode** (`ports=N`):
- Enables N simultaneous reads/cycle to the **same** M_AXI pointer.
- Creates per-port L1 caches + shared L2 cache.
- L2 is shared, direct-mapped, loaded from DRAM via bursts.
- L2 broadcasts loaded lines to requesting L1 caches.
- `l2_lines` must be > `lines`.

**Limitations:**
- Read-only ports only (inout not supported).
- Multi-port: only one read-only array per bundle.
- Both L1 and L2 are direct-mapped (single way).

**Global resource control:** `config_interface -m_axi_cache_impl [auto|lutram|bram|uram]`

---

## pragma HLS dataflow

**Description:** Enables task-level pipelining — producer and consumer tasks overlap in execution. Creates PIPO or FIFO channels between tasks.

```c
#pragma HLS dataflow [disable_start_propagation]
```

- Not hierarchical by default — must be applied at each level where overlap is desired.
- `disable_start_propagation` — prevents a start FIFO from becoming a bottleneck.

**Coding style requirements:**
- Single-producer → single-consumer per channel.
- No feedback between tasks (circular data flow).
- No conditional execution of tasks.
- No loops with multiple exit conditions.

> When any above condition is violated, HLS issues a warning and skips DATAFLOW.

**Global defaults:** `config_dataflow`

---

## pragma HLS dependence

**Description:** Provides HLS with explicit dependency information for loop variables. Can either declare a false dependency (allowing more aggressive scheduling) or enforce a true one.

```c
#pragma HLS dependence variable=<var> [class=<class>] [type=<type>] [direction=<dir>] [distance=<int>] <dependent>
```

| Parameter | Values | Notes |
|---|---|---|
| `variable` | variable name | Mutually exclusive with `class` |
| `class` | `array`, `pointer` | Applies to all variables of that class |
| `type` | `intra`, `inter` | Intra = same iteration; Inter = between iterations |
| `direction` | `RAW`, `WAR`, `WAW` | Loop-carried only |
| `distance` | integer | Inter-iteration distance (for `inter` + `dependent=true`) |
| `dependent` | `true`, `false` | `false` removes/ignores dependency |

> ⚠️ Cannot use on bundled M_AXI arguments or struct elements unless the struct is disaggregated.  
> ⚠️ Specifying a false dependency on a *real* dependency produces **incorrect hardware**.

---

## pragma HLS disaggregate

**Description:** Deconstructs a struct variable into its individual scalar elements as separate HLS variables.

```c
#pragma HLS disaggregate variable=<variable>
```

- Top-level function struct arguments are **aggregated by default**; use this pragma to disaggregate.
- Applies only one level: targets inner struct directly if full disaggregation of nested structs is needed.
- After disaggregation, access members the standard C++ way:
  - Pointer: `a->x`
  - Reference: `c.x`

---

## pragma HLS expression_balance

**Description:** Rearranges operations using associative/commutative properties to form a balanced tree, reducing logic chain depth and latency.

```c
#pragma HLS expression_balance [off]
```

- Integer ops: **on by default** — use `off` to disable.
- Float ops: **off by default** — omit `off` to enable.
- Placed anywhere within a function body scope.

---

## pragma HLS function_instantiate

**Description:** Creates a unique RTL implementation for each call-site instance of a function, specialized on a specific constant argument.

```c
#pragma HLS FUNCTION_INSTANTIATE variable=<variable>
```

- `variable` should be a constant argument whose value differs per call site.
- Without this pragma, all instances share one RTL block.
- Use with `#pragma HLS inline off` on the same function to prevent auto-inlining.
- Reduces control logic complexity by eliminating mux logic for varying constants.

---

## pragma HLS inline

**Description:** Controls whether a function is inlined into its caller(s), dissolved from the RTL hierarchy.

```c
#pragma HLS inline [off] [recursive]
```

| Usage | Effect |
|---|---|
| `inline` | Inline this function one level up |
| `inline off` | Prevent inlining (including automatic inlining) |
| `inline recursive` | Recursively inline all sub-functions below |
| `inline off` + sub-function `recursive` | Preserve current level; flatten everything below |

- Inlining dissolves all pragmas applied to the inlined function.
- `INLINE recursive` in a dataflow region: if result is a single function, the pragma is **ignored**.

---

## pragma HLS interface

**Description:** Specifies how RTL ports are derived from top-level function arguments during interface synthesis. Defines I/O protocol and AXI interface modes. **Top-level function only.**

```c
#pragma HLS interface mode=<mode> port=<name> [OPTIONS]
```

### Interface Modes

**Port-Level Protocols:**

| Mode | Description |
|---|---|
| `ap_none` | Simple data port, no protocol |
| `ap_vld` | Data + valid signal |
| `ap_ack` | Data + acknowledge signal |
| `ap_hs` | Data + valid + acknowledge (two-way handshake) |
| `ap_ovld` | Output valid only; input half uses `ap_none` |
| `ap_memory` | Standard RAM interface (separate ports in IP Integrator) |
| `bram` | RAM interface as a single port in IP Integrator |
| `ap_fifo` | FIFO interface (read-only or write-only only; no bidirectional) |

**AXI Protocols:**

| Mode | Description |
|---|---|
| `s_axilite` | AXI4-Lite slave interface (also generates C driver files) |
| `m_axi` | AXI4 master memory-mapped interface |
| `axis` | AXI4-Stream interface |

**Block-Level Control Protocols** (assigned to `port=return`):

| Mode | Description |
|---|---|
| `ap_ctrl_hs` | Start, idle, done, ready signals |
| `ap_ctrl_chain` | All of above + continue signal (for chaining) |
| `ap_ctrl_none` | No block-level I/O protocol (co-sim may fail) |

### Key Options

| Option | Description |
|---|---|
| `bundle=<string>` | Group ports into a named bundle (use **lowercase**) |
| `channel=<string>` | Multi-channel M_AXI (multiple channels in one adapter) |
| `clock=<name>` | Separate clock for AXI4-Lite interface |
| `depth=<int>` | Max samples for co-sim FIFO sizing (required for pointers) |
| `latency=<value>` | Read latency (`ap_memory`) or AXI bus latency (`m_axi`) |
| `max_read_burst_length=<int>` | Max data values per M_AXI read burst |
| `max_write_burst_length=<int>` | Max data values per M_AXI write burst |
| `max_widen_bitwidth=<int>` | Override max auto-widen bitwidth for M_AXI |
| `name=<string>` | Custom RTL port name |
| `num_read_outstanding=<int>` | Pending read requests before stall (M_AXI) |
| `num_write_outstanding=<int>` | Pending write requests before stall (M_AXI) |
| `offset=<string>` | AXI4-Lite address or M_AXI offset: `off`, `direct`, `slave` |
| `autorestart` | Generate auto-restart counter in AXI4-Lite (applies to `port=return`, `s_axilite`, `ap_ctrl_hs` only) |
| `register` | Register signal and protocol signals until last execution cycle |
| `register_mode=<fwd\|rev\|both\|off>` | AXI4-Stream register path control (default: `both`) |
| `storage_impl=<impl>` | `s_axilite` only: `auto`, `bram`, `uram` |
| `storage_type=<value>` | `ap_memory` only: RAM/ROM type (e.g., `ram_t2p`) |
| `direct_io=<true/false>` | Mark direct I/O stream mapping to AXI4-Lite |
| `interrupt=<int>` | `ap_vld`/`ap_hs`: bit position in ISR/IER (16–31) |

> **TIP:** Register on `port=return` is not supported. Use `#pragma HLS LATENCY min=1 max=1` instead.

---

## pragma HLS latency

**Description:** Constrains the minimum and/or maximum latency of a function, loop, or code region.

```c
#pragma HLS latency [min=<int>] [max=<int>]
```

- At least one of `min` or `max` must be specified.
- If latency < min: HLS extends latency to minimum (enables sharing).
- If latency > max: HLS tries harder; if still failing, issues warning and outputs smallest achievable latency.
- To constrain total iterations of a loop (including after unrolling), wrap the loop in a named region:
  ```c
  Region: {
    #pragma HLS latency max=10
    for (...) { ... }
  }
  ```
- Use to limit synthesis search space and improve tool runtime.

---

## pragma HLS loop_flatten

**Description:** Collapses nested loops into a single loop for more effective pipelining and reduced latency due to loop transition overhead.

```c
#pragma HLS loop_flatten [off]
```

- Place in the **innermost loop body**.
- Without `off`: enable flattening of this loop with (perfect/almost-perfect) outer loops.
- With `off`: disable flattening of this loop (and subloops).

**Flattenable loop requirements:**
- Perfect nests: each outer loop body contains **only one** sub-loop, no other instructions.
- Almost-perfect nests: outer loop body contains only one sub-loop, no other *control flow* (non-control instructions are pushed into innermost loop automatically).
- Each loop is a `for`-loop without `break`.
- Trip counts must be loop-invariant (not dependent on outer loop counter).
- Non-flattenable: inner trip count depends on outer counter.

---

## pragma HLS loop_merge

**Description:** Merges consecutive loops into a single loop, reducing loop-transition clock cycles and enabling parallel implementation.

```c
#pragma HLS loop_merge [force]
```

- Placed in the enclosing scope (will merge all sub-loops there); or placed in a loop body to merge inner loops of that loop.
- `force` — merge even when HLS issues a warning (user ensures correctness).

**Merge rules:**
- Variable bounds loops: must have identical iteration counts.
- Constant bounds: merged loop uses maximum constant bound.
- Variable + constant bounds: cannot merge.
- Code between loops cannot have side-effects (e.g., `a=b` allowed, `a=a+1` not).
- Loops with FIFO reads cannot be merged (read ordering would change).

---

## pragma HLS loop_tripcount

**Description:** Provides HLS with estimated iteration counts for loops where the tripcount cannot be statically determined. **Analysis only — no effect on synthesis results.**

```c
#pragma HLS loop_tripcount [min=<int>] [max=<int>] [avg=<int>]
```

- Used when the loop bound depends on an input argument or a dynamically computed value.
- Allows accurate latency reporting in the analysis reports.
- At least one of `min`, `max`, or `avg` should be specified.

> **TIP:** Using a C `assert` macro to constrain loop variables causes HLS to use those limits for both reporting and hardware sizing.

---

## pragma HLS occurrence

**Description:** Declares that a pipelined function call inside a conditional block executes less frequently than the enclosing pipeline. Allows that region to be pipelined with a slower (higher) II.

```c
#pragma HLS occurrence cycle=<int> [off=true]
```

- `cycle = N/M` where N = loop iterations, M = times the conditional block executes.
- N must be an integer multiple of M.
- Without the pragma, the conditional sub-function defaults to the same II as the caller.
- The pragma enables resource sharing within the less-frequently-called region.

**Example:** Loop executes 16 times; `if` block executes every 4 iterations → `cycle=4`.

---

## pragma HLS performance

**Description:** Specifies high-level performance goals. At top level, triggers design-wide analysis and automatically infers lower-level directives. At loop level, targets a specific transaction interval.

```c
#pragma HLS performance target_ti=<value> [unit=[sec|cycle]]
```

- `target_ti` — target interval between successive starts (in clock cycles or time units).
- `unit=sec` — supports `ns`, `us`, `ps` suffixes (e.g., `100us`).
- Applied at top-level: tool performs design-wide analysis and infers loop-level `PERFORMANCE`, `UNROLL`, `PIPELINE`, `ARRAY_PARTITION`, `INLINE` directives.
- Applied at loop level: targets interval between starts of that loop in successive outer loop iterations.

**Example:** 60 fps at 180 MHz → `target_ti = 180M / 60 = 3,000,000` cycles.

---

## pragma HLS pipeline

**Description:** Reduces the initiation interval (II) of a function or loop by allowing concurrent execution of operations across iterations.

```c
#pragma HLS pipeline [II=<int>] [off] [rewind[=true|false]] [style=<stp|frp|flp>]
```

| Option | Description |
|---|---|
| `II=<int>` | Target initiation interval (HLS will attempt to meet it) |
| `off` | Disable pipelining for this loop/function |
| `rewind` / `rewind=true` | Continuous re-entry: no pause between last iteration and next start. Only for single loop (or perfect nest) inside top function |
| `style=stp` | **Stall pipeline** — stalls when no input; default |
| `style=flp` | **Flushable pipeline** — flushes on missing input; more resources |
| `style=frp` | **Free-running flushable** — runs even without data; best timing/deadlock; higher power |

- HLS generates minimum achievable II by default (timing first).
- Use `DEPENDENCE` pragma to resolve loop-carry dependencies that block pipelining.
- This is a hint, not a hard constraint — tool may revert to `stp` if conditions are not met.

---

## pragma HLS protocol

**Description:** Defines a cycle-accurate protocol region where HLS will not insert clock cycles unless explicitly specified with `ap_wait()` / `wait()`.

```c
#pragma HLS protocol [floating | fixed]
```

- `floating` (default) — operations outside the protocol region may overlap with it.
- `fixed` — operations outside the region do **not** overlap with the protocol region.
- Create the region using a named C/C++ block: `io_section: { ... }`.
- `ap_wait()` (C) or `wait()` (C++) inside the region explicitly inserts one clock cycle.
- These statements have no effect in simulation.

---

## pragma HLS reset

**Description:** Adds or removes reset behavior for specific static or global state variables.

```c
#pragma HLS reset variable=<a> [off]
```

- Without `off` — adds reset to the variable even when global setting is `none` or `control`.
- With `off` — removes reset from the variable even when global setting is `state` or `all`.

**Global reset policy (set via `config_rtl -reset`):**

| Setting | Behavior |
|---|---|
| `none` | No reset in design |
| `control` | Reset state machine/control registers only (default) |
| `state` | Control + static/global variables |
| `all` | All registers and memories |

**Class variables:**
- Must be `public static` for reset at the `class` level.
- Apply the pragma to an *object* of the class in the top-function or sub-function, not inside constructors.

---

## pragma HLS stable

**Description:** Declares that an argument remains constant during kernel execution (it can only change when the kernel is idle).

```c
#pragma HLS stable variable=<a> [off]
```

- Suppresses synchronization overhead: port fanout does not need to be registered.
- In DATAFLOW networks: removes the requirement for the first process to read the input and the last process to write the output, improving II dramatically.
- Only valid for **Control-Driven** task modeling (not applicable to Data-Driven TLP).
- `off` — turns off stable inference.

---

## pragma HLS stream

**Description:** Overrides the default array-to-RAM mapping, forcing a DATAFLOW array channel or top-level argument to be implemented as a streaming FIFO instead.

```c
#pragma HLS stream variable=<variable> [type=<type>] [depth=<int>]
```

| `type` | Description |
|---|---|
| `fifo` (default when stream applied) | FIFO buffer with specified depth |
| `pipo` | Ping-pong buffer (depth = number of banks, default 2) |
| `shared` | Synchronized shared channel without data duplication; depth = sync distance (default 1) |
| `unsync` | No synchronization — consistency guaranteed by design |

- `depth` — overrides the default FIFO depth (default matches the original array size).
- In DATAFLOW where all tasks run at II=1, `depth=1` can greatly reduce area.
- `config_dataflow -depth` sets the global default; per-variable `depth=` in this pragma overrides it.
- Top-level arrays specified as `ap_fifo` interface are automatically streaming.

---

## pragma HLS top

**Description:** Assigns an alias name to a function for use with `set_top`. Primarily useful for synthesizing C++ class member functions.

```c
#pragma HLS top name=<string>
```

- After placing the pragma, also run `set_top <string>` from Tcl or configure it in the IDE project settings.

---

## pragma HLS unroll

**Description:** Unrolls a loop by creating multiple copies of the loop body in RTL, enabling parallel execution of iterations.

```c
#pragma HLS unroll [factor=<N>] [skip_exit_check] [off=true]
```

| Option | Description |
|---|---|
| *(none)* | Fully unroll the loop (compile-time constant bound required) |
| `factor=<N>` | Partially unroll: N copies of the loop body |
| `skip_exit_check` | Skip the exit-check logic (only valid if N divides the bound exactly) |
| `off=true` | Disable unrolling for this loop |

- Partial unrolling does NOT require N to divide the maximum iteration count — HLS adds an exit check automatically. Use `skip_exit_check` only when it is guaranteed to divide evenly.
- HLS auto-unrolls loops when `ARRAY_PARTITION`/`ARRAY_RESHAPE` creates more data bandwidth than a rolled loop can consume.
- Auto-unrolling threshold: `config_unroll -tripcount_threshold`.

---

## Best Practices

1. **Pipeline before partition** — Pipeline innermost loops first; then use `ARRAY_PARTITION` if II > 1 due to memory port conflicts.
2. **DATAFLOW for parallel stages** — Use `DATAFLOW` with `STREAM` for in-order producer/consumer chains; use PIPO for out-of-order or random-access patterns.
3. **Avoid BIND_OP for DSP when multi-op matching matters** — `BIND_OP` prevents MULADD/AMA pattern recognition.
4. **Use LOOP_TRIPCOUNT for analysis, not synthesis** — It only affects reporting, not hardware.
5. **STABLE in DATAFLOW** — Mark configuration/weight arrays as STABLE to dramatically improve II in dataflow regions.
6. **CACHE for stencil patterns** — When compiler cannot infer burst access due to overlapping reads, add `CACHE` to reduce DRAM bandwidth.
7. **M_AXI pointer aliasing** — Always declare `ALIAS` when host passes the same buffer to multiple kernel arguments; otherwise HLS treats them as independent.

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 17 (pp. 541–607)*
