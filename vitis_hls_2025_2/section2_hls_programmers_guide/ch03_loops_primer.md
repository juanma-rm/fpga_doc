# Chapter 3 — Loops Primer
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Why Loops Matter for HLS Performance](#1-why-loops-matter-for-hls-performance)
2. [Pipelining Loops](#2-pipelining-loops)
3. [Automatic Loop Pipelining](#3-automatic-loop-pipelining)
4. [Rewinding Pipelined Loops](#4-rewinding-pipelined-loops)
5. [Pipeline Types (STP / FRP / FLP)](#5-pipeline-types-stp--frp--flp)
6. [Managing Pipeline Dependencies](#6-managing-pipeline-dependencies)
7. [Removing False Dependencies](#7-removing-false-dependencies)
8. [Unrolling Loops](#8-unrolling-loops)
9. [Merging Loops](#9-merging-loops)
10. [Working with Nested Loops](#10-working-with-nested-loops)
11. [Working with Variable Loop Bounds](#11-working-with-variable-loop-bounds)
12. [Best Practices](#12-best-practices)

---

## 1. Why Loops Matter for HLS Performance

Loops are a primary optimization target in HLS because:
- Each loop iteration requires **at least one clock cycle** in hardware.
- There is an **implicit wait-until-clock** at each iteration boundary.
- Without optimization, each iteration starts only after the previous one finishes.

Two main strategies improve loop performance:

| Strategy | Effect | Trade-off |
|---|---|---|
| **Pipelining** | Overlaps successive iterations; reduces Initiation Interval (II) | Requires resolving data/memory dependencies |
| **Unrolling** | Creates multiple parallel copies of loop body | Increased LUT/FF resource usage |

> **Tip:** Always **label loops** (e.g., `SUM_LOOP: for (...)`) — this aids debugging and reporting in the Vitis HLS GUI. Unused labels generate harmless warnings.

---

## 2. Pipelining Loops

### Concept

Pipelining allows subsequent loop iterations to start before prior ones finish — overlapping their execution stages.

**Without pipelining (II = 3, 3 iterations):** Total = 8 cycles.  
**With pipelining (II = 1):** Total = 4 cycles. A new input is read every cycle.

$$\text{Total Latency} = \text{Iteration Latency} + II \times (N - 1)$$

### Syntax

```cpp
vadd: for (int i = 0; i < len; i++) {
    #pragma HLS PIPELINE        // target II=1 (default)
    c[i] = a[i] + b[i];
}
```

To specify an explicit target:
```cpp
#pragma HLS PIPELINE II=2
```

> **Important:** Pipelining a loop **automatically unrolls all loops nested inside it**.

### Key Constraints

- If data dependencies exist (loop-carried), the tool increases II until dependencies are satisfied.
- If a loop cannot be pipelined at all (e.g., scalar dependency as the exit condition), pipelining is halted and a non-pipelined design is output.

**Example of an un-pipelineable loop:**
```cpp
// Next iteration depends on both a and b from the current iteration:
Minim_Loop: while (a != b) {
    if (a > b) a -= b;
    else       b -= a;
}
```

---

## 3. Automatic Loop Pipelining

The `syn.compile.pipeline_loops` configuration command controls automatic pipelining:

| Setting | Behavior |
|---|---|
| Default threshold = **64** | All loops with **trip count ≥ 64** are automatically pipelined |
| `= 0` | Disables all automatic pipelining (only explicit pragmas apply) |
| Custom value N | Loops with trip count ≥ N are pipelined |

**Nested loop auto-pipelining behavior:**
1. Start at the innermost loop.
2. If it can be pipelined (trip count ≥ threshold), pipeline it.
3. Move up the nest: if the outer loop contains only sub-loops that were also unrolled (cumulative trip count ≥ threshold), pipeline the outer loop instead and unroll inner.

```cpp
loop3: for (y = 0; y < 480; y++) {   // 480 >= 64 → pipeline here
    loop2: for (x = 0; x < 640; x++) { // 640 >= 64 → checked
        loop1: for (i = 0; i < 5; i++) { // 5 < 64 → unrolled into loop2
        }
    }
}
```

> To prevent auto-pipelining on a specific loop, use `#pragma HLS PIPELINE off`.

> **Order:** The `syn.compile.pipeline_loops` command is applied **after** all user-specified directives (e.g., a user UNROLL removes the loop before auto-pipeline can apply).

---

## 4. Rewinding Pipelined Loops

The `rewind` option on `#pragma HLS PIPELINE` enables the **overlap of successive calls** to the pipelined loop:

```cpp
outermost_loop: for (int i = 0; i < N; i++) {
    #pragma HLS PIPELINE rewind
    // ...
}
```

**Conditions for rewind:**
- The loop must be the **outermost construct** in the top function or in a dataflow region.
- The dataflow region (or function) must be called multiple times.

> **Note:** If a loop wraps a `#pragma HLS DATAFLOW` region, Vitis HLS **automatically** implements rewind behavior.

> **Compatibility:** FLP pipelines are compatible with `rewind` when `syn.compile.enable_auto_rewind` is also set.

---

## 5. Pipeline Types (STP / FRP / FLP)

The tool automatically selects the most appropriate pipeline style. You can override the global default with `syn.compile.pipeline_style` or per-scope with `#pragma HLS PIPELINE style=<type>`.

| Type | Pragma | Global Config | Best Used When | Disadvantages |
|---|---|---|---|---|
| **STP** (Stalled Pipeline) | `style=stp` | `pipeline_style=stp` (default) | No timing issues; flushable not needed | Not flushable → more deadlocks; timing issues from high-fanout control |
| **FRP** (Free-Running Pipeline) | `style=frp` | `pipeline_style=frp` | High-fanout control causes timing closure issues; flushable needed; **only in dataflow regions** | FIFOs on outputs add resource use; requires at least one blocking I/O (stream/ap_hs) |
| **FLP** (Flushing Pipeline) | `style=flp` | `pipeline_style=flp` | Flushable required; used with `hls::task` (automatically selected); avoids deadlock | II can be larger; greater resource use when II > 1 |

### Why Free-Running Pipeline (FRP)?

Standard pipelines distribute blocking signals to register enables — a **high-fanout net** that causes timing closure failures in deep pipelines. FRP:
- Eliminates blocking signal connections to register enables.
- Is fully flushable (supports bubbling invalid transactions).
- Reduces wire length and high-fanout.

**Cost:** Output FIFO buffers + mux delay at blocking output ports.

> **Restriction:** `frp` can only be used inside a `DATAFLOW` region.

---

## 6. Managing Pipeline Dependencies

When a loop or function is pipelined, the tool must ensure all data dependencies are satisfied across overlapping iterations.

### Dependency Types

| Type | Alias | Description | Example |
|---|---|---|---|
| **RAW** (Read After Write) | True dependency | Result of a write must be available before the next read | `I1: t = a * b;` → `I2: c = t + 1;` |
| **WAR** (Write After Read) | Anti-dependency | A write cannot complete until a previous read has used the old value | `I1: b = t + a;` → `I2: t = 3;` |
| **WAW** (Write After Write) | Output dependency | Writes to the same location must occur in order | `I1: t = a*b;` then `I3: t = 1;` must come after |
| **RAR** (Read After Read) | No dependency | No ordering requirement (unless `volatile`) | Free to reorder |

### Memory Dependencies in Pipelined Loops

Loop-carried memory RAW dependencies force II > 1:

```cpp
// This loop has a loop-carried RAW dependency through mem[]:
for (i = 0; i <= 254; i++) {
    #pragma HLS PIPELINE II=1
    m = r * a; mem[i+1] = m;     // write mem[i+1]
    rnext = mem[i]; r = rnext;   // read mem[i] — next iter reads mem[i+1]!
}
// Result: HLS achieves Final II: 2 (cannot achieve II=1)
```

The II is forced higher because the multiply latency (2+ cycles) means the write of `mem[i+1]` isn't complete before the next iteration needs to read `mem[i+1]` as `mem[i]`.

> **Implication:** Higher clock frequencies → more pipeline stages in multiply → higher required II.

---

## 7. Removing False Dependencies

False dependencies are **overly conservative assumptions** by the compiler — they don't exist in the real algorithm but cannot be statically disproven.

**Example:** Two array accesses in mutually exclusive branches that the compiler assumes may alias:

```cpp
void histogram(int in[INPUT_SIZE], int hist[VALUE_SIZE]) {
    int acc = 0, old = in[0];
    for (int i = 0; i < INPUT_SIZE; i++) {
        #pragma HLS PIPELINE II=1
        int val = in[i];
        if (old == val) {
            acc = acc + 1;
        } else {
            hist[old] = acc;               // hist[old] and hist[val]
            acc = hist[val] + 1;           // can NEVER alias (else branch)
        }
        old = val;
    }
    hist[old] = acc;
}
```

The compiler conservatively assumes `hist[old]` and `hist[val]` may overlap → schedules them in alternate cycles → II = 2.

**Fix:** Use `#pragma HLS DEPENDENCE` to declare the false dependency:

```cpp
#pragma HLS DEPENDENCE variable=hist type=intra direction=RAW dependent=false
```

### Dependency Types for `DEPENDENCE` Pragma

| Type | Scope | `dependent=false` effect | `dependent=true` effect |
|---|---|---|---|
| **inter** | Between different loop iterations | Allows parallel execution of unrolled/pipelined iterations | Prevents concurrent access |
| **intra** | Within the same loop iteration | Frees operations to move within the iteration (more scheduling freedom) | Operations must follow the specified order |

> **Warning:** Declaring a false dependency as `dependent=false` when it actually **is** real produces **incorrect hardware** — verify carefully before applying.

---

## 8. Unrolling Loops

### Concept

Unrolling creates **multiple hardware copies of the loop body** to execute several iterations simultaneously. By default, all loops stay rolled (single hardware instance, reused every iteration).

| Mode | Pragma | Effect | Trade-off |
|---|---|---|---|
| **Full unroll** | `#pragma HLS UNROLL` | Loop disappears; all iterations run in parallel | Maximum area consumption |
| **Partial unroll (factor N)** | `#pragma HLS UNROLL factor=N` | N copies of body; trip count reduced to original/N | Balanced area vs. performance |
| **No unroll (default)** | (none) | Single hardware copy; all iterations sequential | Minimum area |

```cpp
// Full unroll: 10 parallel adders
LOOP_1: for (x = 0; x < N; x++) {
    #pragma HLS UNROLL
    out_accum += A[x];
}
```

**Example result (N=10, at 5 ns clock):**

| Configuration | Latency | LUT increase |
|---|---|---|
| No optimization | 200 ns | Baseline |
| Full unroll | 50 ns | Significant |
| Partial unroll (factor=2) | ~100 ns | Moderate |

### Partial Unroll Exit Check

When trip count is **not divisible** by the unroll factor, the tool adds an **exit check** for the remainder. This check is skipped if trip count is perfectly divisible.

### Constraints

- **Variable-bound loops cannot be fully unrolled** — HLS doesn't know how many copies to create.
- When a loop or function is pipelined, **all inner loops are automatically unrolled** (required for pipelining).
- Variable-bound inner loops **prevent pipelining** of outer loops.

---

## 9. Merging Loops

Every **rolled loop** generates at least one FSM state. Sequential loops create unnecessary transition cycles.

**Without merging (2 sequential loops, 4 iterations each):**

| Phase | Cycles |
|---|---|
| Enter ADD loop | 1 |
| Execute ADD (4 iter) | 4 |
| Exit ADD, Enter SUB | 1 |
| Execute SUB (4 iter) | 4 |
| Exit SUB | 1 |
| **Total** | **11** |

**With `LOOP_MERGE`:**

| Phase | Cycles |
|---|---|
| Enter merged loop | 1 |
| Execute merged (4 iter) | 4 |
| Exit merged loop | 1 |
| **Total** | **6** |

```cpp
void top(a[4], b[4], c[4], d[4], ...) {
    #pragma HLS LOOP_MERGE   // merges all loops in this scope
    Add: for (i = 3; i >= 0; i--) {
        if (d[i]) a[i] = b[i] + c[i];
    }
    Sub: for (i = 3; i >= 0; i--) {
        if (!d[i]) a[i] = b[i] - c[i];
    }
}
```

> **Note:** `LOOP_MERGE` has limitations and may not always succeed. Manual loop merging (rewriting) is the fallback.

---

## 10. Working with Nested Loops

### Pipelining Rule

A loop can be pipelined **only if it contains no sub-loops** (after unrolling inner loops). Moving up a loop nest:
- Outer loop iteration overhead: +1 cycle entry + +1 cycle exit per nest level.
- The optimal balance for area vs. performance is almost always to **pipeline the innermost loop**.

### Perfect vs. Imperfect Nested Loops

| Type | Definition | Flatten-able? |
|---|---|---|
| **Perfect nested** | Each outer loop contains exactly one sub-loop and nothing else | Yes, with `LOOP_FLATTEN` |
| **Almost-perfect** | Outer loop has one sub-loop + elementary instructions | Yes — instructions pushed to innermost by tool |
| **Imperfect** | Outer loop has multiple sub-loops | Not automatically flatten-able |

```cpp
// Perfect nested (flatten-able):
outer: for (int i = 0; i < N; ++i) {
    inner: for (int j = 0; j < M; ++j) { ... }
}

// Imperfect nested (not flatten-able):
outer: for (int i = 0; i < N; ++i) {
    inner_A: for (int j = 0; j < M; ++j) { ... }
    inner_B: for (int j = 0; j < M; ++j) { ... }
}
```

### `LOOP_FLATTEN` Pragma

```cpp
inner: for (int j = 0; j < M; ++j) {
    #pragma HLS LOOP_FLATTEN  // applied to innermost loop
    body;
}
```

Merges the loop nest into a single flat loop that can be pipelined, eliminating inter-level transition cycles.

---

## 11. Working with Variable Loop Bounds

**Problem:** Variable loop bounds prevent:
- Static latency calculation (report shows `?`).
- Full unrolling.
- Pipelining of outer loops containing the variable-bound loop.

```cpp
LOOP_X: for (x = 0; x < width; x++) {  // 'width' is a runtime input
    out_accum += A[x];
}
// HLS reports: Trip count: ? Latency: ?
```

### Workaround 1 — `LOOP_TRIPCOUNT` (reporting only)

```cpp
#pragma HLS LOOP_TRIPCOUNT min=1 max=32
```

Provides trip count **for reporting and `PERFORMANCE` pragma support only** — does **not affect synthesis**.

```
Result: Trip count: 0~32  Latency: 0~32
```

### Workaround 2 — Fixed bounds with conditional body (affects synthesis)

```cpp
// Replace variable bound with constant; guard body with conditional:
LOOP_X: for (x = 0; x < N; x++) {      // N = 32 (compile-time constant)
    if (x < width) {
        out_accum += A[x];
    }
}
```

- Loop can now be **fully unrolled** (N copies, each with its own conditional).
- Removes the "cannot unroll loop with variable trip count" warning.
- Use `assert(width <= N)` to communicate the runtime constraint to synthesis.

> **Important:** Loops with variable bounds in the hierarchy of a pipelined/unrolled loop **block the pipeline** — the tool cannot determine the structure of the inner hardware.

---

## 12. Best Practices

| Practice | Rationale |
|---|---|
| **Always label loops** | Enables precise reporting, pragma targeting, and GUI waveform debugging |
| **Target II=1 for innermost loops** | Maximum throughput; tool will increase II only when dependencies require it |
| **Pipeline innermost loops first** | Lowest overhead; fastest compile time; best QoR for most designs |
| **Use `LOOP_FLATTEN` for perfect nested loops** | Eliminates state-transition cycles between loop levels |
| **Use `LOOP_MERGE` for sequential sibling loops** | Reduces FSM states and inter-loop cycle overhead |
| **Convert variable-bound loops to fixed bounds + guards** | Enables unrolling and pipelining; removes `?` lap count from reports |
| **Add `LOOP_TRIPCOUNT` to remaining variable-bound loops** | Enables accurate performance reporting even when bounds can't be made constant |
| **Investigate memory bottlenecks when II > 1** | Often caused by insufficient RAM ports; fix with `ARRAY_PARTITION` |
| **Use `DEPENDENCE dependent=false` only when certain** | Declaring a nonexistent dependency causes silent RTL correctness errors |
| **Prefer `PIPELINE rewind` for top-level loop dataflow** | Enables successive invocations to overlap without manual restructuring |
| **Use FLP (`style=flp`) when tasks can deadlock** | Automatically selected for `hls::task`; required when feedback streams are present |

---

### See Also

- [Chapter 4 — Arrays Primer](ch04_arrays_primer.md) — Array partitioning to resolve port contention in pipelined loops
- [Chapter 5 — Functions Primer](ch05_functions_primer.md) — Function pipelining and inlining
- [Chapter 17 — HLS Pragmas](../section4_vitis_hls_command_reference/ch17_hls_pragmas.md) — `PIPELINE`, `UNROLL`, `LOOP_MERGE`, `LOOP_FLATTEN` pragma reference
- [Chapter 10 — Performance Pragma](ch10_performance_pragma.md) — `PERFORMANCE` pragma as an alternative to manual pipeline/unroll

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 3: Loops Primer, Pages 65–84.*
