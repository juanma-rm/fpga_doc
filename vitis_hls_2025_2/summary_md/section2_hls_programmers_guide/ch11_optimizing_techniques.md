# Chapter 11: Optimizing Techniques and Troubleshooting Tips

> **Source:** Vitis HLS User Guide UG1399 v2025.2, Chapter 11, Pages 265–329

---

## Table of Contents
1. [Optimization Directives Overview](#1-optimization-directives-overview)
2. [HLS Scheduling and Binding](#2-hls-scheduling-and-binding)
3. [Optimizing Logic Expressions](#3-optimizing-logic-expressions)
   - 3.1 [Shift Register Inference](#31-shift-register-inference)
   - 3.2 [Expression Balancing](#32-expression-balancing)
   - 3.3 [Floating-Point and Unsafe Math Optimizations](#33-floating-point-and-unsafe-math-optimizations)
4. [Optimizing AXI System Performance](#4-optimizing-axi-system-performance)
   - 4.1 [Burst Transfer Types](#41-burst-transfer-types)
   - 4.2 [Burst Preconditions and Limitations](#42-burst-preconditions-and-limitations)
   - 4.3 [AXI Interface Control Options](#43-axi-interface-control-options)
   - 4.4 [Stencil Optimization](#44-stencil-optimization)
   - 4.5 [Manual Burst (`hls::burst_maxi`)](#45-manual-burst-hlsburst_maxi)
   - 4.6 [AXI Performance Case Study Summary](#46-axi-performance-case-study-summary)
5. [Managing Area and Hardware Resources](#5-managing-area-and-hardware-resources)
   - 5.1 [ALLOCATION Directive](#51-allocation-directive)
   - 5.2 [BIND_OP and BIND_STORAGE Directives](#52-bind_op-and-bind_storage-directives)
   - 5.3 [DSP Multi-Operation Matching](#53-dsp-multi-operation-matching)
6. [Limitations of Control-Driven Task-Level Parallelism (Dataflow)](#6-limitations-of-control-driven-task-level-parallelism-dataflow)
7. [Limitations of Pipelining with Static Variables](#7-limitations-of-pipelining-with-static-variables)
8. [Canonical Dataflow Coding Style](#8-canonical-dataflow-coding-style)
9. [Best Practices](#9-best-practices)

---

## 1. Optimization Directives Overview

### Pragma Directives

| Directive | Description |
|---|---|
| `AGGREGATE` | Group all struct elements into one wide vector for simultaneous read/write |
| `ALIAS` | Define distance between multiple pointers accessing the same DRAM buffer for dependence analysis |
| `ALLOCATION` | Limit the number of operations, implementations, or functions (forces sharing; may increase latency) |
| `ARRAY_PARTITION` | Partition large arrays into smaller arrays or registers to eliminate BRAM bottlenecks |
| `ARRAY_RESHAPE` | Reshape array to wider word width (improves BRAM access without extra BRAM) |
| `BIND_OP` | Specify exact RTL implementation for a given operation |
| `BIND_STORAGE` | Specify exact RTL implementation for a storage element (BRAM, URAM, LUTRAM) |
| `DATAFLOW` | Enable task-level pipelining: functions and loops run concurrently |
| `DEPENDENCE` | Override loop-carried dependences to allow lower II pipelining |
| `DISAGGREGATE` | Break a struct into its individual elements |
| `EXPRESSION_BALANCE` | Disable/enable automatic adder-tree expression balancing |
| `INLINE` | Inline a function to enable cross-boundary optimization |
| `INTERFACE` | Specify RTL ports from function arguments |
| `LATENCY` | Specify min/max latency constraint on a function or loop |
| `LOOP_FLATTEN` | Collapse nested loops into one (reduces latency, eases pipelining) |
| `LOOP_MERGE` | Merge consecutive loops (reduces latency, improves sharing) |
| `LOOP_TRIPCOUNT` | Provide trip count estimate for variable-bound loops (affects reporting only, not synthesis) |
| `OCCURRENCE` | Specify a code region executes at a lesser rate than the enclosing loop (pipelining) |
| `PERFORMANCE` | Specify desired transaction interval; tool infers how to achieve it |
| `PIPELINE` | Reduce initiation interval by overlapping loop/function iteration execution |
| `PROTOCOL` | Define a region where no clock operations are inserted (for explicit handshake protocols) |
| `RESET` | Add or remove reset on specific static/global variables |
| `STABLE` | Mark dataflow input/output as stable (skip synchronization at dataflow region boundaries) |
| `STREAM` | Implement array as FIFO or RAM channel in dataflow; override `hls::stream` depth/type |
| `TOP` | Designate an alternative function as the synthesis top |
| `UNROLL` | Unroll for-loops to create multiple independent instances of the loop body |

### Configuration Commands (Global Settings)

| Config | Description |
|---|---|
| Array Partition Configuration | Global array partitioning options (includes interface arrays) |
| Compile Options | Loop auto-pipelining, floating-point math optimizations |
| Dataflow Configuration | Default FIFO depth and channel type for dataflow |
| Interface Configuration | Ports not tied to top function args; eliminate unused ports |
| Operator Configuration | Default latency/implementation per operation type |
| RTL Configuration | Output naming, reset polarity, synchronous/asynchronous |
| Schedule Setting | Scheduler effort level and verbosity |
| Storage Configuration | Default latency/implementation per storage type |
| Unroll Setting | Default tripcount threshold for automatic loop unrolling |

---

## 2. HLS Scheduling and Binding

HLS transforms untimed C/C++ into timed RTL through six steps:

1. **Compile** — Dead-code elimination, constant folding, unsupported construct detection
2. **Schedule** — Assigns C operations to clock cycles, respecting:
   - Data dependency ordering
   - Clock period and target device delays
   - Multi-cycle resource requirements
   - User directives (`PIPELINE`, `LATENCY`, etc.)
3. **Bind** — Maps scheduled operations to RTL implementations:
   - `add` → combinational AddSub
   - `mul` → combinational Mul **or** pipelined multiplier **or** DSP48/58
   - Arrays → BRAM, LUTRAM, URAM, or registers
   - Shared resources if operations don't overlap in time
4. **Control logic extraction** — Creates a finite state machine (FSM) from the C control flow
5. **I/O port creation** — Top-level function arguments → RTL ports; arrays → BRAM address/data/CE/WE signals
6. **RTL generation** — Merge datapath + FSM + I/O into RTL HDL

**Key metrics:**

$$\text{Latency} = \text{clock cycles from first input to last output}$$

$$\text{Initiation Interval (II)} = \text{clock cycles before the design can accept new inputs}$$

$$\text{Loop Latency} = \text{loop\_iter\_latency} \times \text{trip\_count}$$

**Example** — `y = x*a + b + c` scheduled in 2 clock cycles:
- Cycle 1: multiplication `x*a` + first addition `+b`
- Cycle 2: second addition `+c`, output `y`

FSM optimization: constant operations (`b+c`) are computed once per function call and moved **outside** the for-loop by the scheduler (loop-invariant code motion).

---

## 3. Optimizing Logic Expressions

### 3.1 Shift Register Inference

Vitis HLS automatically infers **SRL shift registers** from this pattern:

```cpp
int A[N];
for (...) {
    for (int i = 0; i < N-1; ++i)
        A[i] = A[i+1];   // shift-left: triggers SRL inference
    A[N-1] = new_value;
    ... A[k] ...           // random read from any SRL tap
}
```

A shift register performs one shift per cycle AND allows one random-access read per cycle — more flexible than a FIFO.

### 3.2 Expression Balancing

Expression balancing rearranges sequential operations into a parallel tree to reduce latency:

**Before balancing** (4 sequential additions → 4 cycle latency):
```
sum = 0; sum += a; sum += b; sum += c; sum += d;
```

**After balancing** (parallel tree → 2 cycle latency):
```
sum = (a + b) + (c + d)  // computed in 2 cycles in parallel
```

| Type | Default | Control |
|---|---|---|
| Integer | **ON** | `#pragma HLS EXPRESSION_BALANCE off` to disable |
| Float/Double | **OFF** | `syn.compile.unsafe_math_optimizations=1` to enable |

> **Area trade-off:** Expression balancing reduces latency but **prevents resource sharing** and increases area.

### 3.3 Floating-Point and Unsafe Math Optimizations

```bash
# hls_config.cfg
syn.compile.unsafe_math_optimizations=1   # enables expression balancing for float/double
syn.compile.no_signed_zeros=1             # can be used alone; enables:
```

With `no_signed_zeros`: `x - 0.0 = x`, `x + 0.0 = x`, `0.0 - x = -x`, `x - x = 0.0`, `x*0.0 = 0.0`

> **Warning:** Enabling these options means C/RTL co-simulation results may **differ** from C-only simulation due to floating-point rounding. Test benches must use range-based checks, not exact equality.

---

## 4. Optimizing AXI System Performance

**Maximum theoretical throughput:**
$$512\text{ bits} \times 300\text{ MHz} \div 8 = 19.2\text{ GB/s (theoretical)}$$
$$\approx 17\text{ GB/s (80–95\% DDR efficiency)}$$

### 4.1 Burst Transfer Types

The compiler infers two types of bursts per port per function:

**Pipeline Burst** (preferred — high throughput):
- Read/write requests are **outside** the loop body
- All loop iterations combine into one large request
- Future iterations (i+1) do NOT wait for current (i) to finish
- Full DDR bandwidth utilization, no gaps

```cpp
// Pipeline burst inferred:
// ReadReq and WriteReq are placed BEFORE loop entry
rb = ReadReq(0, size);
wb = WriteReq(0, size);
for (int i = 0; i < size; i++) {
#pragma HLS PIPELINE II=1
    Write(wb, i) = f(Read(rb, i));
}
WriteResp(wb);
```

**Sequential Burst** (fallback — lower throughput):
- Read/write requests are **inside** the loop body
- Each iteration waits for the previous request to complete (gap between requests)
- Better than no burst; acceptable for conditional or complex access patterns

```cpp
// Sequential burst (requests inside loop):
for (int i = 0; i < size; i++) {
    rb = ReadReq(i, 1);
    wb = WriteReq(i, 1);
    Write(wb, i) = f(Read(rb, i));
    WriteResp(wb);
}
```

**Burst scope:** Burst analysis is done **per function** — bursting across function boundaries is not supported.

**Burst reporting:** The Synthesis Summary report shows:
- Successful burst inferences (type, length, bit-width, port)  
- Missed burst opportunities with reasons

### 4.2 Burst Preconditions and Limitations

All preconditions must be met for **pipeline burst** to be inferred:

| Precondition | Details |
|---|---|
| **Homogeneous direction** | All reads OR all writes — cannot mix in one burst |
| **Monotonically increasing** | Addresses must increase in both space and time; no backwards jumps |
| **Consecutive** | No gaps or overlaps between elements; strictly forward |
| **Known length before request** | Burst length must be determinable (even if runtime variable) before the first request |
| **Single direction per bundle** | If two arrays share the same m_axi bundle: only one can burst per direction at a time |
| **No intra-bundle same-direction overlap** | Same direction accesses on the same channel of the same bundle in the same region → no burst |
| **No dependency during burst** | No read-after-write or write-after-read conflicts in the burst window |

**Common causes of burst failure:**

```cpp
// FAIL: outer loop burst failure — iteration 0 and 1 share element 8
for (int i = 0; i < 8; ++i)
    for (int j = 0; j < 9; ++j)
        b[i*8 + j] = a[i*8 + j];
// Burst stops at element 8; only inner loop burst of length 9 is inferred

// FAIL: volatile prevents burst
volatile int *p = ptr;

// FAIL: ap_int/ap_uint as loop induction variable — use unsigned int instead
// FAIL: conditional memory access inside burst loop
// FAIL: m_axi access inside a called function — use #pragma HLS INLINE
// FAIL: DATAFLOW loop — add per-task bursts inside dataflow tasks instead
```

**Fix: INLINE for cross-function access**
```cpp
void my_function(hls::stream<T> &out, int *din, int idx) {
#pragma HLS INLINE    // add this to enable burst in the calling scope
    T v; v.data = din[idx]; out_pkt.write(v);
}
```

**Fix: Loop induction variable address dependency**
```cpp
// Bad (idx not a function of i, j):
my_function(out_pkt, din, idx++);

// Good (use (i*N+j)):
my_function(out_pkt, din, i*num_512_bytes + j);
```

### 4.3 AXI Interface Control Options

**INTERFACE pragma parameters:**

| Parameter | Default | Effect |
|---|---|---|
| `latency` | 64 cycles (Vitis) | Estimated AXI round-trip latency; scheduler pre-issues requests |
| `max_read_burst_length` | 16 | Max transfers per read burst; larger bursts → higher priority in interconnect |
| `max_write_burst_length` | 16 | Max transfers per write burst |
| `num_read_outstanding` | 16 | Read requests in-flight (FIFO depth = N_out × max_burst × word_bytes) |
| `num_write_outstanding` | 16 | Write requests in-flight |

**Global configuration commands:**

| Command | Default | Description |
|---|---|---|
| `syn.interface.m_axi_conservative_mode` | `true` | Delay write until all data buffered (prevents deadlock; slight write latency increase) |
| `syn.interface.m_axi_latency` | 0=auto (Vivado), 64 (Vitis) | Global default latency override |
| `syn.interface.m_axi_min_bitwidth` | 8 | Minimum m_axi data channel width (power-of-2, 8–1024) |
| `syn.interface.m_axi_max_bitwidth` | 1024 | Maximum m_axi data channel width |
| `syn.interface.m_axi_max_widen_bitwidth` | 512 (Vitis), 0 (Vivado) | Target width for auto port widening |
| `syn.interface.m_axi_auto_max_ports` | `false` | `true` → each unbundled port gets its own adapter (more resource) |
| `syn.interface.m_axi_alignment_byte_size` | 64 (Vitis), 1 (Vivado) | Pointer alignment assumption for auto widening |
| `syn.interface.m_axi_num_read_outstanding` | 16 | Global default for read outstanding |
| `syn.interface.m_axi_num_write_outstanding` | 16 | Global default for write outstanding |
| `syn.interface.m_axi_max_read_burst_length` | 16 | Global default read burst length |
| `syn.interface.m_axi_max_write_burst_length` | 16 | Global default write burst length |

**Latency effect summary:**
- **Pipeline burst:** latency has NO impact — one large request regardless
- **Sequential burst:** latency strongly affects throughput:
  - Default (64) too high → idle cycles wasted
  - Decrease latency → tightly packed sequential requests → better throughput
  - Typical real system latency breakdown: AXI adapter ~5–7 cycles, interconnect ~30 cycles, DDR ~9–14 cycles

**Pipelining between bursts:**
```cpp
// Without inter-burst pipelining (inner loop pipelined, outer loop not):
for (int x = 0; x < k; ++x) {
    int off = f(x);
    for (int i = 0; i < N; ++i) {
#pragma HLS PIPELINE II=1
        ... = gmem[off + i];   // burst of N from each outer iteration
    }
}

// With inter-burst pipelining (unroll inner, pipeline outer):
for (int x = 0; x < k; ++x) {
#pragma HLS PIPELINE II=N     // outer loop II = N cycles
    int off = f(x);
    for (int i = 0; i < N; ++i) {
#pragma HLS UNROLL             // unrolled inner
        ... = gmem[off + i];   // still burst N, but outer iterations overlap
    }
}
```

### 4.4 Stencil Optimization

For 2D convolutions/filters accessing non-sequential pixel positions (stencil patterns), manual line-buffer/window-buffer implementation is normally needed. Use the `#pragma HLS array_stencil` to **automatically** implement the line and window buffer optimization:

```cpp
for (int y = 0; y < HEIGHT; ++y) {
    for (int x = 0; x < WIDTH; ++x) {
#pragma HLS PIPELINE II=1
#pragma HLS array_stencil variable=src     // auto line+window buffer
        int sum = 0;
        for (int row = 0; row < FILTER_V; row++)
            for (int col = 0; col < FILTER_H; col++)
                sum += src[y+row-(FILTER_V/2)][x+col-(FILTER_H/2)] * coeffs[row][col];
        dst[y][x] = sum;
    }
}
```

Benefits: eliminates multiple DDR reads of the same pixel; caches relevant data on-chip in BRAM-based line buffers.

### 4.5 Manual Burst (`hls::burst_maxi`)

Use `hls::burst_maxi<T>` when automatic burst inference fails and you cannot restructure the code to satisfy the preconditions:

```cpp
#include "hls_burst_maxi.h"

void dut(hls::burst_maxi<int> A) {
#pragma HLS INTERFACE m_axi port=A depth=1000 num_read_outstanding=32 max_read_burst_length=16

    // Issue 4 separate read requests before entering the processing loop
    A.read_request(0,   16);   // request A[0..15]
    A.read_request(128, 16);   // request A[128..143]
    A.read_request(256, 16);   // request A[256..271]
    A.read_request(384, 16);   // request A[384..399]

    for (int i = 0; i < 64; i++) {
#pragma HLS PIPELINE II=1
        int val = A.read();    // blocking: waits for next element
        // process val...
    }
}
```

**API summary:**

| Method | Description |
|---|---|
| `read_request(offset, len)` | Issue read request: len elements starting at offset; returns when FIFO has space |
| `T read()` | Blocking read of one element from m_axi FIFO |
| `write_request(offset, len)` | Issue write request |
| `write(val, mask=-1)` | Write one element with optional byte-enable mask |
| `write_response()` | Block until all write responses received; call once per `write_request` |

**Testbench usage:** Pass regular arrays — the constructor `burst_maxi(T *p)` converts automatically in C-simulation. HLS design and testbench **must be in separate files**.

**Critical rules:**
1. Always call `read_request` before `read()`; `write_request` before `write()`; `write_response()` matches each `write_request()`
2. Mismatched write requests/responses → AXI protocol violation
3. Overlapping read and write groups to same address → undefined behavior
4. Multiple burst_maxi in same bundle → all must be `hls::burst_maxi<T>` with same element type
5. Too many `read_request` calls before any `read()` → deadlock (FIFO fills up)
6. DATAFLOW between `read_request` and `read()` (in different processes) is not supported

**Deadlock prevention:**
```cpp
// BAD — if N is large, read_request fills FIFO before any read() is called:
for (int i = 0; i < N; i++) A.read_request(i*128, 16);
for (int i = 0; i < N*16; i++) val = A.read();  // deadlock if N > FIFO depth

// GOOD — interleave request and read:
for (int batch = 0; batch < N; batch++) {
    A.read_request(batch*128, 16);
    for (int j = 0; j < 16; j++) { val = A.read(); ... }
}
```

### 4.6 AXI Performance Case Study Summary

Optimization progression for a read-then-write kernel (`transfer_kernel`):

| Step | Change | Impact |
|---|---|---|
| Baseline | 512-bit port width | Read: pipeline burst ✓; Write inner loop: pipeline burst ✓; Write outer loop: sequential burst |
| Step 2 | Reduce `latency=` from 64 to 21 | Sequential burst gaps reduced → throughput improvement |
| Step 3 | Rewrite write loop to eliminate outer sequential burst | Both read + write → pipeline burst → high throughput; no further gains from outstanding/ports |

**Case study takeaways:**
- Port width (512-bit) is the highest-impact single setting
- Pipeline burst > sequential burst; optimize code to achieve pipeline burst
- Latency matters **only** for sequential burst; irrelevant for pipeline burst
- num_outstanding: increase only if burst length < 16 (double the default of 16)
- Multiple ports: only useful when there are genuinely concurrent independent accesses

---

## 5. Managing Area and Hardware Resources

### 5.1 ALLOCATION Directive

Limits the number of specific operations/implementations/functions in the design, forcing resource sharing at the cost of increased latency:

```cpp
// Limit to 256 floating-point multipliers (DSP-efficient for 317 muls):
#pragma HLS ALLOCATION instances=fmul limit=256 operation
for (int i = 0; i < 317; i++) {
#pragma HLS UNROLL
    acc += acc * d[i];
}
```

`type` options: `operation` (limit operator count), `implementation` (limit specific impl), `function` (limit function instances).

**Operations controllable via ALLOCATION:**

Integer: `add`, `sub`, `mul`, `sdiv`, `udiv`, `srem`, `urem`, `shl`, `lshr`, `ashr`, `icmp`

Floating-point (single): `fadd`, `fsub`, `fmul`, `fdiv`, `fcmp`, `fsqrt`, `frecip`, `frsqrt`, `frem`

Floating-point (double): `dadd`, `dsub`, `dmul`, `ddiv`, `dcmp`, `dsqrt`, `drecip`, `drsqrt`, `drem`

### 5.2 BIND_OP and BIND_STORAGE Directives

Force specific RTL implementations for individual operations or storage types:

```cpp
// Force variable c to use a 2-stage pipelined multiplier in fabric:
#pragma HLS BIND_OP variable=c op=mul impl=fabric latency=2
c = a * b;

// Force variable temp's add operation into a DSP block:
#pragma HLS BIND_OP variable=temp op=add impl=dsp
temp = inB + inA;

// Force out1's multiply to use a 3-stage pipelined multiplier:
#pragma HLS BIND_OP variable=out1 op=mul latency=3
*out1 = inA * inB;
```

> **Multiple identical operators:** If one expression has multiple `*` operators (e.g., `a * b * c`), split into named temporaries and apply pragma to the desired one.

```cpp
// Disambiguate: control only first multiplication
#pragma HLS BIND_OP variable=tmp op=mul latency=3
tmp = inA * inB;       // this mul → 3-stage pipeline
*out = tmp * inC;      // this mul → tool's choice
```

### 5.3 DSP Multi-Operation Matching

The HLS compiler looks for **Add-Multiply (MULADD)**, **Multiply-Add (MULDADD)**, and **Accumulate-Multiply-Add (AMA)** patterns to map to DSP48/DSP58 blocks:

**Matching process:**
1. Inline functions as needed
2. Extract common sub-expressions
3. Match fanout-free `add→mul`, `mul→add`, `add→mul→add` fragments within DSP bitwidth limits
4. Schedule and bind

**Bitwidth limits for DSP58 (Versal):** A=34b, B=24b, D=27b, C=58b, P=58b.

**Coding style for DSP matching:**

```cpp
// BAD: shared sub-expression a*b prevents DSP MULADD recognition
f1 = a*b + c;
f2 = a*b + d;   // a*b extracted → fan-out; no DSP match

// GOOD: non-inlined functions isolate the expression
inline_mac_f1 = mac(a, b, c);  // contained in one function → DSP match
inline_mac_f2 = mac(a, b, d);  // independent call → DSP match
```

**BIND_OP can interfere with DSP matching:**
```cpp
// BAD: assigning 'mul' individually breaks the MULADD recognition
ACC_T MAC(DATA_T din, COEF_T coef, ACC_T acc) {
    acc = din * coef + acc;
#pragma HLS BIND_OP variable=acc op=mul impl=dsp latency=2  // prevents MULADD
    return acc;
}

// FIX: remove BIND_OP, let compiler match the full MULADD to DSP:
ACC_T MAC(DATA_T din, COEF_T coef, ACC_T acc) {
    acc = din * coef + acc;   // compiler matches MULADD to DSP natively
    return acc;
}
```

**PIPELINE + expression balancing conflict:**
```cpp
// Pipeline might unroll and rebalance, breaking DSP match. Fix:
#pragma HLS PIPELINE II=1
#pragma HLS EXPRESSION_BALANCE off    // disable balancing → preserve MULADD pattern
```

### 5.4 Unrolling Loops in C++ Classes

> ⚠️ **Important:** When loops are used in C++ classes, the loop induction variable must **not** be a data member of the class — this prevents the loop from being unrolled.

**Broken example** — `k` is a class member:
```cpp
template <typename T0, typename T1, typename T2, typename T3, int N>
class loop_class {
private:
    pe_mac<T0, T1, T2> mac;
public:
    T0 shift[N];
    int k;              // ← Class member — prevents UNROLL
    T0 shift_output;

    void exec(T1 *pcout, T0 *dataOut, T1 pcin, T3 coeff, T0 data, int col) {
    Function_label0:;
    #pragma HLS inline off
        SRL: for (k = N-1; k >= 0; --k) {
        #pragma HLS unroll   // ← FAILS: k is a class member
            if (k > 0)
                shift[k] = shift[k-1];
            else
                shift[k] = data;
        }
        *dataOut = shift_output;
        shift_output = shift[N-1];
        *pcout = mac.exec1(shift[4*col], coeff, pcin);
    }
};
```

**Fix:** Remove `k` as a class member and make it **local to the function**:
```cpp
    void exec(T1 *pcout, T0 *dataOut, T1 pcin, T3 coeff, T0 data, int col) {
    Function_label0:;
    #pragma HLS inline off
        SRL: for (int k = N-1; k >= 0; --k) {  // ← Local variable — UNROLL works
        #pragma HLS unroll
            if (k > 0)
                shift[k] = shift[k-1];
            else
                shift[k] = data;
        }
        // ...
    }
```

---

## 6. Limitations of Control-Driven Task-Level Parallelism (Dataflow)

Four patterns that **prevent or limit** the DATAFLOW optimization:

### Reading Inputs / Writing Outputs in the Middle

All reads from top-level function inputs must happen at the **start** of the dataflow region, and all writes to outputs at the **end**. Reading/writing mid-region forces sequential execution.

### Single-Producer-Consumer Violations

Each local variable passed between tasks must have exactly **one writer** and **one reader**:

```cpp
// VIOLATION: temp1 has one writer (Loop1) but two readers (Loop2 and Loop3)
Loop1: for (int i = 0; i < N; i++) temp1[i] = data_in[i] * scale;
Loop2: for (int j = 0; j < N; j++) out1[j] = temp1[j] * 123;  // reader 1
Loop3: for (int k = 0; k < N; k++) out2[k] = temp1[k] * 456;  // reader 2

// FIX: introduce a Split function to duplicate the data:
void Split(int in[N], int out1[N], int out2[N]) {
    for (int i = 0; i < N; i++) { out1[i] = in[i]; out2[i] = in[i]; }
}
// Now: Loop1 → Split → Loop2, Loop3  (four tasks, each variable single-producer-consumer)
```

### Bypassing Tasks and Channel Sizing

If a variable from task A is consumed by task C (skipping task B), the PIPO buffer for that variable must be sized appropriately:

```cpp
// temp2 is produced by Loop1 but consumed by Loop3 (bypasses Loop2)
// Default PIPO depth = 2; must increase to 3:
#pragma HLS STREAM type=pipo variable=temp2 depth=3
```

PIPO depth rule: depth = (number of bypassed tasks) + 2.

> **Note:** Mismatched FIFO/PIPO depths cause unintended synchronization points inside the dataflow region.

### Feedback Streams

Non-stream feedback (scalars or arrays going backwards in execution order) is NOT supported. Only `hls::stream` can carry feedback:

```cpp
void firstProc(hls::stream<int> &forwardOUT, hls::stream<int> &backwardIN) {
    static bool first = true;
    int val = first ? 10 : backwardIN.read();  // initial value on first call
    first = false;
    forwardOUT.write(val * 2);
}
void secondProc(hls::stream<int> &forwardIN, hls::stream<int> &backwardOUT) {
    backwardOUT.write(forwardIN.read() + 1);
}
void top(...) {
#pragma HLS DATAFLOW
    hls::stream<int> forward, backward;
    firstProc(forward, backward);   // writes forward, reads backward (feedback)
    secondProc(forward, backward);  // reads forward, writes backward
}
```

### Conditional Execution of Tasks

Tasks that are inside an `if`/`else` cannot be dataflow-optimized. Move the conditional **inside** the loop body:

```cpp
// BAD: conditional wraps entire loops
if (sel) { Loop1: for(...) {...} } else { Loop2: for(...) {...} }

// GOOD: conditional inside always-executed loops
Loop1: for (int i = 0; i < N; i++) {
    temp1[i] = sel ? data_in[i] * 123 : data_in[i] * 321;
}
```

### Loops with Multiple Exit Conditions

`break` and `continue` statements in a loop prevent it from being used in dataflow:
- The loop's exit condition must be solely the loop bound
- Remove `break`/`continue` from loops within dataflow regions

---

## 7. Limitations of Pipelining with Static Variables

Static variables create loop-carried dependencies that force II ≥ 2 in pipelined regions:

```cpp
// Problematic: one store and one load in same iteration → II = 2
void function_foo() {
    static bool change = 0;
    if (cond) change = x;  // write
    y = change;            // read (depends on write above)
}

// Fix: separate read and write into distinct branches → II = 1 possible
void function_fixed() {
    static bool change = 0;
    bool change_temp;
    if (cond) {
        change = x;        // write path
        change_temp = x;
    } else {
        change_temp = change;  // read path
    }
    y = change_temp;
}
```

---

## 8. Canonical Dataflow Coding Style

Canonical dataflow is the **predictable, structured** form of `#pragma HLS DATAFLOW` that produces consistent performance. Deviating from canonical form can cause the tool to create non-overlapping sequential FSMs instead of concurrent processes.

### Basic Level Rules

**Two valid contexts for `#pragma HLS DATAFLOW`:**

1. **Function body** — pragma inside the function:
```cpp
void dataflow_func(int in0, int in1[], int &out0, int out1[]) {
#pragma HLS DATAFLOW
    int C0, C1[N], C2;  // no initialization allowed
    func1(in0, in1, C0, C1);   // single writer C0, C1
    func2(C0, C1, C2);         // single reader C0, C1; single writer C2
    func3(C2, out0, out1);     // single reader C2
}
```

2. **Loop body** — pragma inside a for-loop that is the only statement in a function:
```cpp
void dataflow_loop(int in0, int in1[], int &out0, int out1[]) {
    for (int i = 0; i < N; i++) {
#pragma HLS DATAFLOW
        int C1[M], C2;
        UserType C0 __attribute__((no_ctor));  // suppress constructor
        func1(in0, in1, C0, C1, i);
        func2(C0, C1, C2, i);
        func3(C2, out0, out1, i);
    }
}
```

**Constraints:**
- Only **function calls** and/or `hls::task` declarations in the dataflow body
- No `if`/`else`, no loops (only a `for` loop with the pragma inside)
- Called functions must have `void` return type
- No variable initialization (use `__attribute__((no_ctor))` for objects with constructors)
- No expressions passed by value to processes (pass by reference/pointer)
- `hls::task` and `hls::thread` instances must be `hls_thread_local`
- Local variables: non-static scalars or arrays only (static allowed only inside processes)

**Channel rules:**
- Arrays: one writer, one reader; writer must be lexically before reader
- `hls::stream` / `hls::stream_of_blocks`: one reader, one writer; feedback also allowed
- Scalars: multiple writers/readers allowed; automatically converted to FIFO channels

> **Feedback streams**: processes reading from feedback channels must handle the first iteration specially (use a static `bool first` flag + initial value) since `hls::stream` doesn't support initial values.

### Advanced Level Support

- **Fully unrolled loops** within dataflow: loop bodies can contain only function calls and `hls::task` instances
- **Fully partitioned arrays**: each partition passes as an independent variable to one process

```cpp
// Pipeline of N identical processes using hls::stream array:
void dut(int in[M], int out[M]) {
#pragma HLS DATAFLOW
    hls_thread_local hls::stream<int> chan[N+1];  // fully partitioned stream array

    read_in(in, chan[0]);
    hls_thread_local hls::task t[N];
    for (int i = 0; i < N; i++) {
#pragma HLS UNROLL
        t[i](worker, chan[i], chan[i+1]);  // N concurrent worker processes
    }
    write_out(chan[N], out);
}

// Same pattern with PIPO (add #pragma HLS STREAM variable=chan for FIFO):
void dut(int in[M], int out[M]) {
#pragma HLS DATAFLOW
    int chan[N+1][M];
#pragma HLS ARRAY_PARTITION complete dim=1 variable=chan
    read_in(in, chan[0]);
    for (int i = 0; i < N; i++) {
#pragma HLS UNROLL
        worker(chan[i], chan[i+1]);
    }
    write_out(chan[N], out);
}
```

---

## 9. Best Practices

| Topic | Recommendation |
|---|---|
| **Burst inference** | Write burst loops in a separate Load/Store function; use `INLINE` on helper functions that access m_axi |
| **Burst type** | Aim for pipeline burst; restructure loops to move read/write requests outside the loop body |
| **Latency** | For sequential bursts, reduce `latency=` from default 64 to match your actual system latency (e.g., 21–30) |
| **Port width** | Always target 512-bit ports; use `ap_uint<512>` or `hls::vector<int,16>` |
| **Multiple ports** | Use separate bundles for truly concurrent accesses; same-bundle accesses are serialized |
| **Expression balancing** | Use `EXPRESSION_BALANCE off` when DSP pattern recognition is needed; never enable `unsafe_math_optimizations` in production without range-based testbench checks |
| **DSP matching** | Isolate MULADD patterns in non-inlined sub-functions; avoid shared sub-expressions; avoid standalone `BIND_OP mul` inside MULADD functions |
| **Dataflow single-producer** | Always obey single-producer-consumer; split fan-out variables with a `Split` helper function |
| **Task bypassing** | When a variable bypasses N tasks, set PIPO depth = N + 2 with `STREAM type=pipo depth=N+2` |
| **Feedback in dataflow** | Only `hls::stream` supports feedback; use `static bool first` to handle the initial value |
| **Static variables in pipeline** | Separate read and write of static variables into different conditional branches to achieve II=1 |
| **Class loop unroll** | Loop induction variables must be local — not class members — for UNROLL to work |
| **Conditional tasks** | Move conditions inside always-executed loops; never wrap entire tasks in conditionals |
| **Manual burst** | Use `hls::burst_maxi` as a last resort; always pair each `read_request(N)` with N `read()` calls; same for write |
| **Deadlock prevention** | Never queue more `read_request`s than `num_read_outstanding` before consuming with `read()` |
| **Stencil kernels** | Use `#pragma HLS array_stencil` on 2D image arrays to auto-generate line+window buffers |

---

### See Also

- [Chapter 2 — Abstract Parallel Programming](ch02_abstract_parallel_programming.md) — Dataflow and `hls::task` fundamentals
- [Chapter 3 — Loops Primer](ch03_loops_primer.md) — Loop pipelining and unrolling basics
- [Chapter 8 — Interfaces](ch08_interfaces.md) — AXI interface burst inference and struct alignment
- [Chapter 17 — HLS Pragmas](../section4_vitis_hls_command_reference/ch17_hls_pragmas.md) — All optimization pragmas
- [Chapter 31 — HLS IP Libraries](../section6_vitis_hls_libraries_reference/ch31_hls_ip_libraries.md) — DSP intrinsics for expression matching

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 11: Optimizing Techniques and Troubleshooting Tips, Pages 265–329.*
