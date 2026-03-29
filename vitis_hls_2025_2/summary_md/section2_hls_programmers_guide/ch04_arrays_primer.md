# Chapter 4 — Arrays Primer
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Mapping Software Arrays to Hardware Memory](#1-mapping-software-arrays-to-hardware-memory)
2. [Array Accesses and Performance](#2-array-accesses-and-performance)
3. [Array Partitioning](#3-array-partitioning)
4. [Array Reshaping](#4-array-reshaping)
5. [Arrays on the Interface](#5-arrays-on-the-interface)
6. [Initializing and Resetting Arrays](#6-initializing-and-resetting-arrays)
7. [Implementing ROMs](#7-implementing-roms)
8. [C Simulation with Large Arrays](#8-c-simulation-with-large-arrays)
9. [Best Practices](#9-best-practices)

---

## 1. Mapping Software Arrays to Hardware Memory

### Key Difference from Software

| Software Arrays | Hardware Arrays (HLS) |
|---|---|
| Dynamically allocated (`new`, `malloc`) | **Static size required** at compile time |
| OS-managed memory | Maps to FPGA on-chip memory (BRAM/URAM/registers) or off-chip memory (DDR/HBM) |
| Flexible access (random, cached) | Port-limited; access parallelism must be designed explicitly |
| Unlimited size (swap-backed) | Limited by on-chip memory resources |

> **Arrays must always be sized**, even as function arguments: `Array[10]` is valid; `Array[]` is not synthesizable.

### Memory Resource Mapping

| Array Type / Size | Default Hardware Implementation |
|---|---|
| Small arrays (few elements) | **Shift register** (automatic for sequential access patterns) |
| Larger internal arrays | **Block RAM (BRAM)** — up to 2 ports |
| Arrays specified with `BIND_STORAGE` | BRAM, LUTRAM, or **UltraRAM (URAM)** |
| Fully partitioned arrays | **Registers** (one per element, fully parallel) |
| Top-level interface arrays (Vitis Kernel) | **M_AXI** ports (off-chip DDR/HBM, default) |
| Top-level interface arrays (Vivado IP) | Standard BRAM with latency = 1 (default) |

### Shift Register Inference

HLS automatically infers a shift register when it detects a shift access pattern:
```cpp
int A[N];  // inferred as shift register
for (...) {
    for (int i = 0; i < N-1; ++i)
        A[i] = A[i+1];   // shift operation
    A[N-1] = new_value;
    result = A[x];        // random read — shift register supports this
}
```

Shift registers support:
- One shift operation per cycle.
- Random read access anywhere in the register per cycle (more flexible than FIFO).

> **Arrays of pointers** are supported; each pointer can only point to a scalar or a 1D array of scalars.

---

## 2. Array Accesses and Performance

### Memory Port Contention

BRAM has **at most 2 data ports** (dual-port). This limits how many accesses can occur per clock cycle and is the most common cause of II > 1 in pipelined loops.

**Example — 3 accesses needed, only 2 ports available:**

```cpp
SUM_LOOP: for (i = 2; i < N; ++i)
    sum += mem[i] + mem[i-1] + mem[i-2];  // 3 reads per iteration
```

HLS error:
```
WARNING: Unable to schedule 'load' operation on array 'mem' due to limited memory ports.
INFO: Pipelining result: Target II: 1, Final II: 2, Depth: 3.
```

The tool relaxes II from 1 to 2 to fit 3 reads across 2 clock cycles.

**Software fix — pre-read and shift:**
```cpp
din_t tmp0 = mem[0], tmp1 = mem[1];
SUM_LOOP: for (int i = 2; i < N; i++) {
    din_t tmp2 = mem[i];           // only 1 read per iteration now
    sum += tmp2 + tmp1 + tmp0;
    tmp0 = tmp1;
    tmp1 = tmp2;
}
```
This restructuring achieves II = 1 with a single-port RAM.

### Optimization Directives (Preferred over Manual Restructuring)

| Optimization | Pragma | Effect |
|---|---|---|
| **Array Partition** | `#pragma HLS ARRAY_PARTITION` | Splits array into multiple smaller arrays or individual registers — more ports |
| **Array Reshape** | `#pragma HLS ARRAY_RESHAPE` | Widens the array word (bit concatenation) — same number of addresses, more data per access |

---

## 3. Array Partitioning

Partitioning splits the original array into multiple arrays, each with its own address/data ports, increasing concurrent access bandwidth.

### Partition Styles

| Style | How It Splits | factor=2 result (size N array) |
|---|---|---|
| `block` | Consecutive element chunks | Array 0: `[0..N/2-1]`, Array 1: `[N/2..N-1]` |
| `cyclic` | Interleaved elements | Array 0: even indices `[0, 2, 4, ...]`, Array 1: odd indices `[1, 3, 5, ...]` |
| `complete` | Every element → individual register | N separate registers (fully parallel access) |

```
block   (factor=2):  [0|1|...|N/2-1] and [N/2|...|N-1]
cyclic  (factor=2):  [0|2|4|...    ] and [1|3|5|...  ]
complete           :  reg0, reg1, reg2, ..., regN-1
```

### Pragma Syntax

```cpp
#pragma HLS ARRAY_PARTITION variable=mem type=cyclic factor=2 dim=1
#pragma HLS ARRAY_PARTITION variable=mem type=complete dim=1  // → registers
```

### Multi-Dimensional Partitioning

```cpp
void foo() {
    int my_array[10][6][4];
    // Partition along dimension 3 → 4 arrays of [10][6]
    #pragma HLS ARRAY_PARTITION variable=my_array type=complete dim=3
    // Partition along dimension 1 → 10 arrays of [6][4]
    #pragma HLS ARRAY_PARTITION variable=my_array type=complete dim=1
    // Partition ALL dimensions → 240 scalar registers
    #pragma HLS ARRAY_PARTITION variable=my_array type=complete dim=0
}
```

### Automatic Array Partitioning

Two configuration commands govern automatic partitioning:

| Config | Effect |
|---|---|
| `syn.array_partition.complete_threshold=N` | Arrays with ≤ N elements are automatically fully partitioned into registers |
| `syn.array_partition.throughput_driven` | Partition based on throughput demand |

---

## 4. Array Reshaping

Reshaping **widens** the array word by concatenating elements (vertical remapping). This reduces the number of BRAM instances needed while increasing the data bandwidth per access.

| Reshape Style | Memory Before | Memory After |
|---|---|---|
| `block factor=2` | N entries at width W | N/2 entries at width 2W (consecutive pairs concatenated) |
| `cyclic factor=2` | N entries at width W | N/2 entries at width 2W (alternating elements concatenated) |
| `complete` | N entries at width W | 1 entry at width N×W (all elements in one register) |

```cpp
void foo() {
    int array1[N], array2[N], array3[N];
    #pragma HLS ARRAY_RESHAPE variable=array1 type=block  factor=2 dim=1
    #pragma HLS ARRAY_RESHAPE variable=array2 type=cyclic factor=2 dim=1
    #pragma HLS ARRAY_RESHAPE variable=array3 type=complete dim=1
}
```

**Key difference from partitioning:** Reshaping keeps the array as a single BRAM (or fewer BRAMs) but with a wider data bus — fewer blocks consumed, same parallelism improvement.

**Auto-unroll on reshape:** When reshaped data allows more data per cycle, HLS may automatically unroll consuming loops to exploit the wider access. Controlled by `syn.unroll.tripcount_threshold`. Example: `syn.unroll.tripcount_threshold=16` — loops with trip count < 16 are auto-unrolled if it improves throughput.

---

## 5. Arrays on the Interface

### Interface Type Selection

| Interface Mode | Usage | Notes |
|---|---|---|
| `m_axi` | Default for Vitis Kernel; off-chip DDR/HBM | High latency; burst inference available |
| `ap_memory` (BRAM) | Default for Vivado IP; single or dual-port RAM | Latency = 1 (default); configurable with `latency=` option |
| `ap_fifo` | Streaming FIFO port | **Requires strictly sequential access order** |
| `axis` | AXI4-Stream | Requires sequential access |

### INTERFACE Pragma Options for Arrays

```cpp
#pragma HLS INTERFACE mode=ap_memory port=arr storage_type=ram_2p  // dual-port
#pragma HLS INTERFACE mode=m_axi     port=arr                       // off-chip
#pragma HLS INTERFACE mode=ap_fifo   port=arr                       // streaming
#pragma HLS INTERFACE mode=ap_memory port=arr latency=3             // external SRAM
```

### FIFO Interface Constraints

Arrays mapped to `ap_fifo` or `axis` must follow strict rules:

1. The array must be **only read or only written** in the loop/function (not both).
2. Array reads must occur in the **same order** as writes (no random access).
3. Struct elements of streaming arrays must be accessed through a **local copy** (not directly).

**Correct streaming struct access:**
```cpp
struct A { short foo; int bar; };
void dut(A in[N], A out[N], bool flag) {
    #pragma HLS interface ap_fifo port=in,out
    for (unsigned i = 0; i < N; i++) {
        A tmp = in[i];            // copy first
        if (flag) tmp.bar += 5;
        out[i] = tmp;             // write whole struct
    }
}
```

HLS issues `@W [XFORM-124]` when it cannot verify sequential access — the RTL co-simulation will catch violations at runtime.

### Interface Sizing

> `Arrays must be sized.` Unsized array arguments (`arr[]`) cause: `@E [SYNCHK-61]: unsupported memory access on variable with unknown size.`

> **Performance note:** Array interface ports can be a bottleneck. Apply `ARRAY_PARTITION` or `ARRAY_RESHAPE` to the interface array to create multiple ports and improve throughput.

---

## 6. Initializing and Resetting Arrays

### `static` Qualifier (Recommended)

| Without `static` | With `static` |
|---|---|
| Array reloaded with initial values on every function call | Array initialized **once** in RTL at power-on; retains values across calls |
| N clock cycles of initialization overhead per call | Zero initialization overhead at runtime |
| Behaves like C software initialization | Behaves like hardware memory (ROM/RAM) |

```cpp
// Without static: 8 cycles to reload coeff every call
int coeff[8] = {-2, 8, -4, 10, 14, 10, -4, 8, -2};

// With static: loaded once into bitstream; retained across calls
static int coeff[8] = {-2, 8, -4, 10, 14, 10, -4, 8, -2};
```

> **AMD recommends** using `static` for any array intended to be a memory in the RTL.

### Reset Behavior

| Reset Config | Effect |
|---|---|
| `syn.rtl.reset=control` (default) | Only control logic is reset; arrays retain their last state on reset signal |
| `syn.rtl.reset=state` | All static/global arrays return to initial values on reset; expensive — takes N cycles for N-element BRAM |
| `syn.rtl.reset=all` | All arrays + control logic reset; maximum overhead |

**Granular control:** Use `#pragma HLS RESET variable=<name>` to opt individual arrays into reset when using `control` mode; or `#pragma HLS RESET off variable=<name>` to exclude specific arrays when using `state` mode.

### Memory Resource Reset Behavior

| Memory | Power-on Init | Hardware RESET signal |
|---|---|---|
| Block RAM (all platforms) | Supported | Requires N-cycle iteration to reset all addresses |
| URAM (all platforms) | Versal only | Maintains separate "initial value" and "runtime value" arrays |

> **URAM write mode warning:** URAM supports **no-change** write mode only (no read-first). Simultaneous read and write to the same address on the same URAM port may worsen II. Use BRAM when read-first behavior is needed.

---

## 7. Implementing ROMs

HLS can infer ROMs from arrays that are fully written then only read, never modified again. To ensure ROM inference:

1. Use the **`const`** qualifier on read-only arrays.
2. Initialize the array as **early as possible** in the function.
3. **Group all writes together** — do not interleave initialization writes with non-init code.
4. Never store different values to the same element after initialization.
5. Initialization computations must depend **only on compile-time constants** or the loop counter.

**ROM inferred with `math.h` init function:**
```cpp
#include <math.h>

void init_sin_table(short sin_table[256]) {
    for (int i = 0; i < 256; i++) {
        double real_val = sin(M_PI * (double)(i - 128) / 256.0);
        sin_table[i] = (short)(32768.0 * real_val);  // compile-time constant
    }
}

dout_t array_ROM(din1_t inval, din2_t idx) {
    short sin_table[256];
    init_sin_table(sin_table);       // separate init function → ROM inferred
    return (int)inval * (int)sin_table[idx];
}
```

> Placing complex initialization in a **separate function** helps HLS recognize that the computation produces constant values and thus synthesize it as a ROM.

---

## 8. C Simulation with Large Arrays

Large arrays placed on the **stack** can exhaust simulation memory:

```cpp
ap_int<32> la0[10000000], la1[10000000];  // ~80 MB on stack — may fail
```

**Solutions:**

1. **Increase stack size** (linker flag): `syn.csimflags -z stack-size=10485760`

2. **Use `__SYNTHESIS__` macro** to separate stack (synthesis) from heap (simulation):
```cpp
#ifdef __SYNTHESIS__
    ap_int<32> la0[10000000], la1[10000000];    // stack: synthesis only
#else
    ap_int<32> *la0 = malloc(10000000 * sizeof(ap_int<32>));  // heap: sim only
    ap_int<32> *la1 = malloc(10000000 * sizeof(ap_int<32>));
#endif
```

> **Important:** Only use `__SYNTHESIS__` in the design source — **never in the test bench** (it has no meaning in C simulation or co-simulation).

> The RTL co-simulation will verify correctness of memory accesses in the synthesized (stack-based) code even if the simulation used heap allocation.

---

## 9. Best Practices

| Practice | Rationale |
|---|---|
| **Declare all arrays with explicit sizes** | Required for synthesis; unsized arrays cause errors |
| **Use `static` for constant-value arrays (ROM data, LUTs)** | Eliminates per-call reload overhead; synthesizes to ROM/initialized BRAM |
| **Use `const` on read-only arrays** | Enables reliable ROM inference; prevents accidental writes |
| **Apply `ARRAY_PARTITION cyclic` for loop-parallel access** | Cyclic partitioning distributes consecutive accesses across banks for pipelined loops |
| **Use `ARRAY_RESHAPE` to widen BRAMs before partitioning** | Conserves BRAM count while still improving bandwidth |
| **Check for port-limited II warnings** | "Unable to schedule load due to limited memory ports" → apply partitioning |
| **Pre-read and shift variables for multi-access loops** | Reduces reads per iteration to match available RAM ports |
| **Use `ARRAY_PARTITION complete` only for small, hot arrays** | Complete partition → registers; too many registers wastes routing resources |
| **Never use `ap_fifo` interface for random-access arrays** | FIFO interfaces require strictly sequential access; random access causes co-sim failure |
| **Initialize complex ROM tables in a separate function** | Helps HLS identify all elements as compile-time constants → ROM inference |
| **Use `syn.rtl.reset=control` + selective `RESET` pragmas** | Avoids expensive full-array reset logic; only reset what truly needs initialization on reset |

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 4: Arrays Primer, Pages 85–99.*
