# Chapter 8: Interfaces of the HLS Design

> **Source:** Vitis HLS User Guide UG1399 v2025.2, Chapter 8, Pages 157–256

---

## Table of Contents
1. [Interface Synthesis Overview](#1-interface-synthesis-overview)
2. [Vitis Kernel Flow Defaults](#2-vitis-kernel-flow-defaults)
3. [Vivado IP Flow Defaults](#3-vivado-ip-flow-defaults)
4. [M_AXI Interface](#4-m_axi-interface)
   - 4.1 [Core Concepts and Signals](#41-core-concepts-and-signals)
   - 4.2 [Burst Inference Rules](#42-burst-inference-rules)
   - 4.3 [Offset Modes](#43-offset-modes)
   - 4.4 [Auto Port Width Resizing](#44-auto-port-width-resizing)
   - 4.5 [M_AXI Bundles](#45-m_axi-bundles)
   - 4.6 [FIFO Sizing](#46-fifo-sizing)
   - 4.7 [Interface Pragma Reference](#47-interface-pragma-reference)
5. [S_AXILITE Interface](#5-s_axilite-interface)
   - 5.1 [Control Register Map](#51-control-register-map)
   - 5.2 [Port-Level Protocols](#52-port-level-protocols)
   - 5.3 [Bundle Rules: Vitis vs. Vivado](#53-bundle-rules-vitis-vs-vivado)
6. [AXI4-Stream (AXIS) Interface](#6-axi4-stream-axis-interface)
   - 6.1 [Protocol and Data Types](#61-protocol-and-data-types)
   - 6.2 [Side-Channel Signals](#62-side-channel-signals)
   - 6.3 [Register Modes](#63-register-modes)
   - 6.4 [Coding Patterns](#64-coding-patterns)
7. [Aggregation and Disaggregation of Structs](#7-aggregation-and-disaggregation-of-structs)
8. [Block-Level Control Protocols](#8-block-level-control-protocols)
9. [Execution Modes](#9-execution-modes)
   - 9.1 [Auto-Restart](#91-auto-restart)
   - 9.2 [Mailbox](#92-mailbox)
10. [Vivado IP Port-Level Protocols](#10-vivado-ip-port-level-protocols)
11. [Initialization and Reset Behavior](#11-initialization-and-reset-behavior)
12. [Best Practices](#12-best-practices)

---

## 1. Interface Synthesis Overview

Every top-level function argument becomes a hardware port. Vitis HLS maps each argument to one of three interface **paradigms**:

| Paradigm | Description | Typical Interface |
|---|---|---|
| **Register** | Single-clock data transfer; direct wire or AXI-Lite register | `s_axilite`, `ap_none`, `ap_vld`, `ap_hs` |
| **Memory** | Array mapped to external RAM via address/data/control | `m_axi`, `ap_memory`, `bram` |
| **Stream** | FIFO-like, sequential burst with flow control | `axis`, `ap_fifo` |

The tool determines the default paradigm from the **flow** (Vitis kernel vs. Vivado IP) and the **C/C++ argument type**.

---

## 2. Vitis Kernel Flow Defaults

Default interface assignments when compiling a Vitis kernel (`.xo` / `v++`):

| C/C++ Argument Type | Default Paradigm | Default Interface |
|---|---|---|
| Scalar (pass by value) | Register | `s_axilite` |
| Array / pointer to array | Memory | `m_axi` |
| Pointer to scalar | Register | `s_axilite` |
| Reference | Register | `s_axilite` |
| `hls::stream<T>&` | Stream | `axis` |

- Default **block-level protocol**: `ap_ctrl_chain` (supports pipelined, overlapping calls)
- All `m_axi` ports default to `offset=slave` (base address via `s_axilite` register)
- Auto port widening enabled: `syn.interface.m_axi_max_widen_bitwidth=512`

---

## 3. Vivado IP Flow Defaults

Default interface assignments when packaging a Vivado IP:

| C/C++ Argument Type | Default Paradigm | Input | Output | Inout |
|---|---|---|---|---|
| Scalar (by value) | Register | `ap_none` | — | — |
| Array | Memory | `ap_memory` | `ap_memory` | `ap_memory` |
| Pointer | Register | `ap_none` | `ap_vld` | `ap_ovld` |
| Reference | Register | `ap_none` | `ap_vld` | `ap_vld` |
| `hls::stream<T>&` | Stream | `ap_fifo` | `ap_fifo` | — |

- Default **block-level protocol**: `ap_ctrl_hs` (sequential execution)
- Auto port widening **disabled** by default (`m_axi_max_widen_bitwidth=0`)
- 1-byte alignment default (`m_axi_alignment_byte_size=1`)

---

## 4. M_AXI Interface

### 4.1 Core Concepts and Signals

M_AXI (AXI4 Memory-Mapped) provides high-bandwidth access to external memory (DDR, HBM, PLRAM). Key features:

- Independent read and write channels (potential ~17 GB/s aggregate)
- **Burst transfers**: single address phase, up to 4 KB per burst
- Outstanding transactions queue: pipelining of address and data phases

Key configuration parameters (Vitis kernel flow):

| Parameter | Vitis Default | Vivado Default | Description |
|---|---|---|---|
| `m_axi_max_widen_bitwidth` | 512 | 0 (off) | Auto port widening target width |
| `m_axi_alignment_byte_size` | 64 | 1 | Alignment for auto widening |
| `m_axi_offset` | `slave` | `slave` | Base address source |
| `m_axi_addr64` | 1 | 1 | Use 64-bit addresses (0 = 32-bit) |
| `max_read_burst_length` | 16 | 16 | Max burst length (transfers per burst) |
| `max_write_burst_length` | 16 | 16 | Max burst length |
| `num_read_outstanding` | 16 | 16 | Outstanding read requests queued |
| `num_write_outstanding` | 16 | 16 | Outstanding write requests queued |

> **Important:** `syn.interface.m_axi_addr64=0` switches ALL m_axi interfaces to 32-bit addressing.

### 4.2 Burst Inference Rules

All of the following must be satisfied for the compiler to infer a burst transfer:

1. **Pipeline the loop** — use `#pragma HLS PIPELINE II=1`
2. **Monotonically increasing addresses** — access must be sequential, no backward jumps
3. **No conditional accesses** inside the loop body
4. **No `LOOP_FLATTEN`** on nested loops containing m_axi accesses
5. **Only one read and one write** per loop iteration (unless mapped to different `m_axi` bundles)

```cpp
void load(int *in, hls::stream<int> &s, int n) {
#pragma HLS PIPELINE II=1
    for (int i = 0; i < n; i++) {
        s.write(in[i]);   // monotonically increasing: in[0], in[1], ...
    }
}
```

> **`memcpy` is strongly discouraged:** Cannot be pipelined, silently changes argument type to `char*`, and conflicts with `array_partition`/`array_reshape`. Always replace with explicit pipelined `for` loops.

```cpp
// Bad: disables burst, type confusion
memcpy(local, ptr, N * sizeof(int));

// Good: burst-friendly, explicit pipeline
for (int i = 0; i < N; i++) {
#pragma HLS PIPELINE II=1
    local[i] = ptr[i];
}
```

### 4.3 Offset Modes

The **offset** determines at runtime how the base address of the external buffer is provided:

| Mode | Pragma Option | Base Address Source | Runtime Changeable |
|---|---|---|---|
| `off` | `offset=off` | Hardcoded 0x00000000 | No |
| `direct` | `offset=direct` | Dedicated input port (synthesized wire) | Yes (via port) |
| `slave` | `offset=slave` | S_AXILITE register (host-written) | Yes (via register) |

```cpp
// Vitis kernel flow: always use offset=slave (default)
#pragma HLS INTERFACE mode=m_axi port=in offset=slave bundle=gmem0

// Vivado IP: offset=direct adds explicit base address port
#pragma HLS INTERFACE mode=m_axi port=in offset=direct bundle=gmem
```

### 4.4 Auto Port Width Resizing

Vitis HLS can automatically widen m_axi ports (e.g., `int` → 512-bit wide bus) to maximize DRAM bandwidth utilization. Preconditions **all** must hold:

- Access pattern is **monotonically increasing** (sequential)
- Accesses are **aligned** to the widen target size
- Data type is **primitive or power-of-2 sized struct**
- Array length is **divisible by the widen factor**
- No `struct` types on the interface (must be disaggregated first)
- No `volatile` qualifier on the pointer

```bash
# hls_config.cfg
syn.interface.m_axi_max_widen_bitwidth=512   # target width (Vitis default)
syn.interface.m_axi_alignment_byte_size=64   # 64-byte = 512-bit aligned
```

### 4.5 M_AXI Bundles

By default, all `m_axi` arguments are bundled into a single AXI4 adapter (`gmem`). Use multiple bundles to achieve parallel memory access:

```cpp
void kernel(int *a, int *b, int *c, int n) {
#pragma HLS INTERFACE mode=m_axi port=a bundle=gmem0 offset=slave
#pragma HLS INTERFACE mode=m_axi port=b bundle=gmem1 offset=slave
#pragma HLS INTERFACE mode=m_axi port=c bundle=gmem0 offset=slave // shares with a
#pragma HLS INTERFACE mode=s_axilite port=return
    // gmem0 (a, c) and gmem1 (b) can operate in parallel
}
```

**Rule:** Each bundle becomes one AXI4 master port. Mapping two arguments to the same bundle means they share one port and serialize.

### 4.6 FIFO Sizing

Three internal FIFOs are generated per m_axi interface:

| FIFO | Width | Depth | Implementation |
|---|---|---|---|
| Address/request queue | `m_axi_addr64` bits | `m_axi_latency` | Shift register (SRL) |
| Data buffer | `port_width` bits | `num_outstanding × max_burst_length` | BRAM (default), or LUTRAM/URAM via `m_axi_buffer_impl` |
| Write response | 1 bit | `num_write_outstanding` | Register |

$$\text{data FIFO depth} = \text{num\_outstanding} \times \text{max\_burst\_length}$$

**Implication:** Increasing `num_outstanding` or `max_burst_length` grows the data buffer BRAM. Set these conservatively for resource-limited designs.

### 4.7 Interface Pragma Reference

```cpp
#pragma HLS INTERFACE mode=m_axi port=input offset=slave bundle=gmem0 \
    depth=1024*1024                  \    // for cosim: array depth
    latency=100                      \    // estimated AXI latency (cycles)
    num_read_outstanding=32          \
    num_write_outstanding=32         \
    max_read_burst_length=16         \
    max_write_burst_length=16
```

---

## 5. S_AXILITE Interface

S_AXILITE exposes the kernel's control interface as an AXI4-Lite slave. It serves three functions:
1. **Block-level control**: start, done, idle, ready signals
2. **Scalar argument registers**: pass small inputs (size, threshold, etc.)
3. **M_AXI base address registers**: configures `offset=slave` pointers

### 5.1 Control Register Map

Offset map for `ap_ctrl_chain` (and `ap_ctrl_hs`); `ap_ctrl_none` has no registers:

| Offset | Register | Description |
|---|---|---|
| `0x00` | Control | `ap_start` (R/W), `ap_done` (R), `ap_idle` (R), `ap_ready` (R), `ap_continue` (R/W), `auto_restart` (R/W) |
| `0x04` | Global Interrupt Enable | Enable/disable global interrupt |
| `0x08` | IP Interrupt Enable | Interrupt enable mask |
| `0x0c` | IP Interrupt Status | Interrupt status (W1C) |
| `0x10` | Auto-restart counter | Iterations for counted auto-restart |
| `0x14` | Input mailbox write | SW→HW mailbox (mailbox enabled only) |
| `0x18` | Output mailbox read | HW→SW mailbox (mailbox enabled only) |
| `0x10+` | Function arguments | Scalar inputs, m_axi offsets (auto-assigned, sequentially) |

Signal semantics:
- **`ap_start = 1`** → kernel begins operation
- **`ap_done = 1`** → output is valid; pulse in `ap_ctrl_hs`, held in `ap_ctrl_chain`
- **`ap_ready = 1`** → ready to accept new inputs (1-cycle pulse)
- **`ap_continue = 1`** → required acknowledgment in `ap_ctrl_chain`; releases `ap_done` hold
- **`ap_idle`** → goes Low while executing, goes High 1 cycle after `ap_done` if no pending `ap_start`

### 5.2 Port-Level Protocols

| Argument Direction | Default Protocol | Alternatives |
|---|---|---|
| Scalar input | `ap_none` | `ap_vld`, `ap_ack` |
| Pointer/ref input | `ap_none` | `ap_vld`, `ap_ack` |
| Pointer/ref output | `ap_vld` | `ap_none`, `ap_ack`, `ap_ovld` |
| Pointer/ref inout | `ap_ovld` | `ap_none`, `ap_ack`, `ap_vld` |

### 5.3 Bundle Rules: Vitis vs. Vivado

| Feature | Vitis Kernel Flow | Vivado IP Flow |
|---|---|---|
| Number of bundles | **1 only** (auto-named `s_axi_control`) | Multiple bundles allowed |
| `bundle=` option | **Must not be specified** | Optional; each bundle → separate adapter |
| Port for `return` | Must have `s_axilite` on `port=return` | Same |

```cpp
// Vitis kernel flow — correct (no bundle= option):
#pragma HLS INTERFACE mode=s_axilite port=scalar_in
#pragma HLS INTERFACE mode=s_axilite port=return

// Vivado IP flow — multiple bundles OK:
#pragma HLS INTERFACE mode=s_axilite port=a bundle=CTRL_A
#pragma HLS INTERFACE mode=s_axilite port=b bundle=CTRL_B
```

---

## 6. AXI4-Stream (AXIS) Interface

### 6.1 Protocol and Data Types

AXI4-Stream is a point-to-point, unidirectional, FIFO-like protocol:

- **TVALID** / **TREADY**: flow-control handshake
- **TDATA**: payload (N-bit wide)
- **TLAST**: marks the last byte of a packet/transfer

No addressing or burst size — any transfer length is supported. AXIS maps to `hls::stream<T>` top-level arguments.

> **Constraint:** AXIS can only be assigned to **top-level** function arguments.  
> Internal streaming channels between sub-functions must use `hls::stream<T>` with `ap_fifo`.

**Predefined type aliases** (`ap_axi_sdata.h`):

```cpp
#include "ap_axi_sdata.h"

// Unsigned 32-bit wide AXIS packet (no side-channel USER/ID/DEST)
typedef ap_axiu<32, 0, 0, 0> pkt_u32;

// Signed 64-bit wide AXIS packet with 8-bit USER
typedef ap_axis<64, 8, 0, 0> pkt_s64;

// Full template:
// hls::axis<T, WUser, WId, WDest>
// ap_axis<W, WUser, WId, WDest>   — signed data
// ap_axiu<W, WUser, WId, WDest>   — unsigned data
```

### 6.2 Side-Channel Signals

| Signal | Macro | Template Width | Description |
|---|---|---|---|
| TDATA | `AXIS_ENABLE_DATA` | `W` | Primary payload |
| TKEEP | `AXIS_ENABLE_KEEP` | `W/8` | Byte-enable (which bytes carry data) |
| TSTRB | `AXIS_ENABLE_STRB` | `W/8` | Position byte vs. null byte |
| TLAST | `AXIS_ENABLE_LAST` | 1 | End-of-packet marker |
| TUSER | `AXIS_ENABLE_USER` | `WUser` | User-defined side channel |
| TID | (via `WId > 0`) | `WId` | Stream identifier |
| TDEST | (via `WDest > 0`) | `WDest` | Routing destination |

Enable/disable macros (bitfield):
```
AXIS_ENABLE_DATA  = 0b00000001
AXIS_ENABLE_KEEP  = 0b00001000
AXIS_ENABLE_LAST  = 0b00010000
AXIS_ENABLE_STRB  = 0b00100000
AXIS_ENABLE_USER  = 0b01000000
AXIS_ENABLE_ALL   = 0b01111111
```

**Helper classes:**
- `hls::axis_data<T>` — DATA always enabled; other fields optional
- `hls::axis_user<WUser>` — USER field enabled; DATA field off

### 6.3 Register Modes

The `register_mode` option inserts pipeline registers on the AXIS port:

| Mode | Registered Signals | Use Case |
|---|---|---|
| `forward` | TDATA, TVALID (forward path only) | Improve timing for output-heavy paths |
| `reverse` | TREADY (back-pressure path only) | Improve timing for input-heavy paths |
| `both` | TDATA, TVALID, TREADY | **Default** — best timing; adds one cycle latency |
| `off` | None | Lowest latency; no extra registers |

```cpp
#pragma HLS INTERFACE mode=axis port=out register_mode=both
```

### 6.4 Coding Patterns

**Basic read-modify-write (always use a temporary variable):**
```cpp
void dut(hls::stream<pkt_u32> &in, hls::stream<pkt_u32> &out, bool flag) {
#pragma HLS INTERFACE mode=axis port=in  register_mode=both
#pragma HLS INTERFACE mode=axis port=out register_mode=both
#pragma HLS INTERFACE mode=ap_ctrl_none port=return
    for (unsigned i = 0; i < N; i++) {
        pkt_u32 tmp = in.read();       // MUST read to temp (no random access!)
        if (flag) tmp.data += 5;
        out.write(tmp);
    }
}
```

**Recommended getter/setter API for side channels:**
```cpp
void process(hls::stream<pkt_u32> &A, hls::stream<pkt_u32> &B) {
#pragma HLS INTERFACE mode=axis port=A,B
    pkt_u32 t_in  = A.read();
    pkt_u32 t_out;

    ap_uint<32> val = t_in.get_data();    // typed accessor
    t_out.set_data(val * 5);
    t_out.set_last(t_in.get_last());
    t_out.set_keep(-1);   // all bytes valid = 0xFFFFFFFF

    B.write(t_out);
}
```

> **Warning:** Never use random indexing (`stream[i]`) on an AXIS stream. Always read into a temporary, operate on the temp, then write the temp out.

---

## 7. Aggregation and Disaggregation of Structs

When a `struct` is used as an interface argument, HLS must decide how to lay out its fields on the bus:

| Context | Default Behavior | With AGGREGATE pragma | `compact` option |
|---|---|---|---|
| AXI interface (`m_axi`, `s_axilite`, `axis`) | **Aggregate** (fields padded to power-of-2 total width) | Automatic | `compact=none` — pad to power-of-2 |
| Other interface (`ap_fifo`, `ap_memory`) | **Aggregate** | Use `AGGREGATE` pragma | `compact=bit` — bit-pack (no padding) |
| Internal variable | **Disaggregate** (element-wise) | Use `AGGREGATE` pragma | `compact=bit`, `compact=byte` |
| Struct containing `hls::stream` | **Always disaggregate** | Not applicable | — |

**Struct padding rules (AXI layout):**
1. Fields are ordered by declaration order (no reordering)
2. Each field aligned to its natural size (up to 4-byte alignment by default)
3. Total struct width padded to next power-of-2

**Power-of-2 rule for m_axi burst:**
If the struct size is **not** a power of 2, burst inference fails for loops accessing that struct. Fix:
- Reorder fields to minimize padding
- Add explicit padding fields to reach the next power of 2
- Then use `compact=auto` or `compact=byte`

```cpp
struct data_t {
    int a;    // 32-bit
    short b;  // 16-bit
    // 16-bit padding added automatically to reach 64-bit total (power-of-2) ✓
};
```

**Disaggregating a struct on AXIS** creates one stream per struct member:
```cpp
struct AB { char c; int i; };

void kernel(hls::stream<AB> &in, ...) {
#pragma HLS INTERFACE mode=axis port=in
#pragma HLS DISAGGREGATE variable=in
// Creates: in_c (8-bit stream) and in_i (32-bit stream) as separate AXI streams
}
```

---

## 8. Block-Level Control Protocols

The block-level protocol manages **when** the kernel starts, stops, and signals completion to the host or upstream logic:

| Protocol | `ap_start` | `ap_done` | `ap_ready` | `ap_idle` | `ap_continue` | Use Case |
|---|---|---|---|---|---|---|
| `ap_ctrl_chain` | ✅ R/W | ✅ held until ack | ✅ 1-cycle pulse | ✅ | ✅ backpressure | **Vitis default** — pipelined, flow-controlled |
| `ap_ctrl_hs` | ✅ R/W | ✅ 1-cycle pulse | ✅ 1-cycle pulse | ✅ | Always=1 | No backpressure; Vivado IP default |
| `ap_ctrl_none` | — | — | — | — | — | Data-driven (stream-to-stream); continuously running |

**`ap_ctrl_chain` timing details:**
- `ap_done` is **held High** until `ap_continue = 1` (prevents output overwrite)
- `ap_ready` pulses High for 1 cycle → indicates new inputs can be accepted
- `ap_idle` goes Low on first clock after reset + `ap_start`; returns High 1 cycle after `ap_done` if no new `ap_start`

**`ap_ctrl_none` co-simulation requirements** (at least one must be met):
1. Combinational design (II = 0)
2. Pipelined with `II = 1`
3. Has `hls::stream` ports or array-to-stream ports

```cpp
// ap_ctrl_none — fully data-driven, no handshake overhead
#pragma HLS INTERFACE mode=ap_ctrl_none port=return
```

---

## 9. Execution Modes

### 9.1 Auto-Restart

Auto-restart allows a kernel to re-launch **immediately** after each completion without host intervention:

**Configuration:**
```cpp
#pragma HLS INTERFACE mode=s_axilite port=return autorestart
```
```bash
# hls_config.cfg
syn.interface.s_axilite_sw_reset=1   # optional: allow software reset
```

**Two variants:**

| Variant | Description |
|---|---|
| **Infinite auto-restart** | Kernel loops forever; host must use `run.abort()` to stop |
| **Counted auto-restart** | Host writes iteration count to register at `0x10`; kernel stops after N iterations |

**C/RTL Co-simulation helper** (`hls_task.h`):
```cpp
#include "hls_task.h"

void top(hls::stream<pkt> &in, hls::stream<pkt> &out, int adder) {
    #pragma HLS INTERFACE s_axilite autorestart port=return
}

// Testbench: run 10 back-to-back iterations with no gaps
hls::autorestart run_top(10, top, input, output, adder_val);
// Reuse existing object for another run:
run_top(5, top, input, output, adder_val);
```

**Auto-restart cosim limitations:**
1. No infinite auto-restart in cosim — must specify finite count
2. No `direct` I/O variables
3. Only one `hls::autorestart` instance per testbench
4. No input changes during the specified iterations
5. No output reading before all iterations complete
6. **Only `ap_ctrl_hs`** is supported (not `ap_ctrl_chain` or `ap_ctrl_none`)
7. No mailbox support in cosim
8. Arrays-to-Stream FIFO interfaces not supported

### 9.2 Mailbox

Mailbox enables **semi-synchronous** parameter updates for continuously running kernels:

```bash
syn.interface.s_axilite_mailbox=both   # enables mailbox for both input and output
```

**Transfer mechanism (double-buffered):**

```
         SW copy register         HW copy register
Write:   SW→SW copy updated  →  picked up on NEXT kernel restart
Read:    HW copy → SW copy  →  SW reads SW copy (updated on kernel done)
```

**XRT host code pattern:**
```cpp
xrt::run incr_run = incr(xrt::autostart{0}, nullptr, nullptr, adder1, adder2);
xrt::mailbox incr_mbox(incr_run);

// Each iteration: update mailbox for next round
incr_mbox.set_arg(2, ++adder1);  // queue update for adder1
incr_mbox.set_arg(3, --adder2);  // queue update for adder2
incr_mbox.write();               // request sync to HW (takes effect next restart)

// Stop infinite auto-restart:
incr_run.abort();
```

> **Important:** When an array is mapped to `s_axilite` with mailbox, the **entire array** must be re-written between each mailbox write cycle.

**Direct I/O (alternative to mailbox)** — for inputs that can change mid-execution:
```cpp
hls::ap_vld<int> reset_value;
if (reset_value.valid())
    local_state = reset_value.read();
```

---

## 10. Vivado IP Port-Level Protocols

Complete list of port-level protocols for **Vivado IP flow** (non-AXI assignments):

| Protocol | Signals Generated | Description |
|---|---|---|
| `ap_none` | `data` only | No control; data treated as always-valid |
| `ap_vld` | `data`, `data_ap_vld` | valid asserts that data is valid |
| `ap_ovld` | `data`, `data_ap_vld` | As `ap_vld` but only on outputs; inputs are `ap_none` |
| `ap_ack` | `data`, `data_ap_ack` | Acknowledge signal; source waits for ack |
| `ap_hs` | `data`, `data_ap_vld`, `data_ap_ack` | Full handshake: valid + acknowledge |
| `ap_stable` | `data` | Data stable for entire function execution; sampled once |
| `ap_fifo` | `data`, `empty_n`/`full_n`, `read`/`write` | FIFO: non-empty/non-full flags + read/write enable |
| `ap_memory` | `addr`, `ce`, `we`, `din`, `dout` | Single or dual-port RAM interface |
| `bram` | `addr`, `ce`, `we`, `din`, `dout`, `clk` | Block RAM interface (adds clock port) |

```cpp
// Vivado IP flow example:
#pragma HLS INTERFACE mode=ap_hs    port=data_in
#pragma HLS INTERFACE mode=ap_vld   port=result
#pragma HLS INTERFACE mode=ap_fifo  port=stream_in
#pragma HLS INTERFACE mode=ap_memory port=local_buf
```

---

## 11. Initialization and Reset Behavior

### Initialization

In C/C++, `static` and global-scope variables initialize to zero (or an explicit value) **once at compile time**. HLS preserves this:

- RTL simulation: variables start with the same initial value as C/C++ source
- FPGA bitstream: initial values programmed into the device at power-up
- **There is no mechanism to return variables to their initial state** via initialization alone — only a reset signal can restore them

> **Note:** Top-level function arguments mapped to AXI4-Lite **cannot** have initial values — no way to represent this in C/C++ function arguments, and adding one would break C/RTL co-simulation equivalence.

### Reset Behavior

Reset is controlled via configuration:

```bash
syn.rtl.reset=control   # default
```

| Reset Option | Scope |
|---|---|
| `none` | No reset added |
| `control` | **(Default)** Resets state machine + I/O protocol registers only |
| `state` | `control` + static/global initialized variables (restores initial values) |
| `all` | Resets all registers and memories in the design |

**AXI4 constraint:** When AXI4 interfaces are present, reset polarity is **automatically set to active-Low**, regardless of the `config_rtl` setting (required by the AXI4 standard).

Fine-grain control with `RESET` pragma:
```cpp
static int state_var = 42;
#pragma HLS RESET variable=state_var       // force reset on state_var
#pragma HLS RESET variable=no_reset off    // exclude from reset
```

> **Resource warning:** Using `reset=all` or `reset=state` on large array variables can significantly increase area and timing pressure. Use `RESET` pragma selectively.

---

## 12. Best Practices

| Topic | Recommendation |
|---|---|
| **M_AXI bursting** | Pipeline all load/store loops with `II=1`; keep addresses monotonically increasing; avoid conditionals in burst loops |
| **`memcpy`** | Replace with explicit pipelined `for` loops — `memcpy` cannot burst and silently changes the argument type |
| **Port widening** | Use `m_axi_max_widen_bitwidth=512` (already default in Vitis); ensure access is aligned and sequential |
| **Bundling** | Use separate `bundle=` names for read and write ports to access different DRAM banks in parallel |
| **Struct size** | Ensure structs used on m_axi are power-of-2 in size (add padding if needed) to enable burst inference |
| **S_AXILITE Vitis** | Never specify `bundle=` for s_axilite in Vitis kernel flow — exactly one bundle is required |
| **AXIS coding** | Always read stream to a `tmp` variable, modify `tmp`, then write `tmp` — never assume random access |
| **AXIS constraint** | AXIS only at top-level ports; use `ap_fifo`/`hls::stream` internally |
| **Control protocol** | Use `ap_ctrl_none` + `hls::stream` for purely data-driven kernels to eliminate handshake overhead |
| **Auto-restart** | Prefer counted auto-restart over infinite when possible; use `incr_run.abort()` responsibly |
| **Mailbox** | Use mailbox only when scalar updates are needed between kernel iterations; do not change mid-run |
| **Reset scope** | Use `reset=control` (default) unless you need to restore static/global state; avoid `reset=all` on large arrays |
| **LCS pattern** | Structure kernels as Load–Compute–Store tasks to maximize data-movement / compute overlap |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 8: Interfaces of the HLS Design, Pages 157–256.*
