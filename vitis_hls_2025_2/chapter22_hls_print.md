# Chapter 22 — HLS Print Function

> UG1399 (v2025.2) · Section VI: Vitis HLS Libraries Reference · Pages 783–784

## Overview

`hls::print` is a synthesizable debug print function analogous to `printf`. It prints a format string and an optional single argument to standard output (and to the simulation log) during C simulation, RTL co-simulation, and HW emulation. It is *silently ignored* in actual hardware (HW implementation targets).

**Header:**
```cpp
#include "hls_print.h"
```

## Use Cases

- Trace the values of selected variables at runtime across all simulation phases.
- Trace execution order across complex control flows and concurrent dataflow regions.

> **Limitation:** `hls::print` cannot be used to trace the order of *individual statements within a basic block*, because the HLS scheduler may reorder them significantly.

## Usage Example

```cpp
#include "hls_print.h"

for (int i = 0; i < N; i++) {
#pragma HLS pipeline ii=1
    hls::print("loop %d\n", i);
    // ...
}
```

This prints the value of `i` at each iteration in C simulation, SW emulation, RTL co-simulation, and HW emulation.

## Supported Format Specifiers

| Specifier | Types |
|---|---|
| `%d` | `int`, `unsigned int` |
| `%f` | `float`, `double` |

> **Long integer cast required:** Values of type `long`, `long long`, and their unsigned variants must be explicitly cast to `int` or `unsigned int` due to C++ argument promotion rules.

## Key Constraints and Caveats

| Constraint | Detail |
|---|---|
| RTL support | Verilog only (not VHDL) |
| Argument count | At most one `int` or `double` argument per call |
| Simulation time | In RTL simulation, the current simulation timestamp is also printed |
| Performance impact | Can alter II and latency of a pipeline — use sparingly |
| Optimization side-effects | Inserting `hls::print` adds an observation point that can change HLS optimizations and thus RTL behavior (analogous to how `printf` affects binary behavior in SW, but more dramatically) |
| Statement ordering | The order of multiple `hls::print` calls within a code block can change due to scheduling |
| Data volume | Not suitable for dumping large arrays — output volume can be significant |

## Best Practices

| Practice | Rationale |
|---|---|
| Use only for targeted variable tracing | Each call can alter pipeline II/latency |
| Cast `long`/`long long` to `int` | Avoid silent format string mismatch due to C++ argument promotion |
| Validate with `%d` / `%f` only | No other format specifiers are supported |
| Do not dump arrays | Output volume can be excessive; use selective index prints instead |

---

### See Also

- [Chapter 7 — Unsupported Constructs](../section02_hls_programmers_guide/ch07_unsupported_constructs.md) — Why `printf` is unsupported in synthesis
- [Chapter 20 — Built-in Functions](ch20_builtin_functions.md) — Other HLS-specific built-ins

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 22, pages 783–784*
