# Chapter 5 — Functions Primer
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Top-Level Function and Hierarchy](#1-top-level-function-and-hierarchy)
2. [Function Inlining](#2-function-inlining)
3. [Function Pipelining](#3-function-pipelining)
4. [Function Instantiation](#4-function-instantiation)
5. [Best Practices](#5-best-practices)

---

## 1. Top-Level Function and Hierarchy

The top-level function becomes the **top-level module** of the RTL design after synthesis.

| Entity | RTL Equivalent |
|---|---|
| Top-level function | Top-level RTL module |
| Sub-function (not inlined) | Separate sub-module in the RTL hierarchy |
| Top-level function arguments | RTL interface ports |
| Each function (top-level or sub) | Gets its own synthesis report and HDL files |

> **Important:** The top-level function **cannot** be a static function.
>
> Global variables used by the kernel cannot be accessed from outside the kernel. Any variable accessed by both the test bench and the kernel must be defined as an argument of the top-level function.

---

## 2. Function Inlining

Function inlining dissolves a function's logic into the calling function, eliminating the hierarchical boundary.

### When Inlining Helps

- Enables **resource sharing** across previously separate function boundaries.
- Allows HLS to better **optimize** or share components within the merged logic.
- Vitis HLS automatically inlines small functions.

### Manual INLINE Directive

```cpp
// Force inlining of all instances of foo_sub
void foo_sub(int p, int q) {
#pragma HLS INLINE          // inline this function everywhere it's called
    ...
}
```

### Inlining for Resource Sharing

To share a function across three call sites using only one hardware instance:
```cpp
void foo_sub(int p, int q) {
#pragma HLS INLINE          // dissolve hierarchy into caller
    foo(p1, q);
}

void foo_top(int a, int b, int c, int d) {
#pragma HLS ALLOCATION instances=foo limit=1 function  // only 1 copy of foo
    foo(a, b);              // foo_1
    foo(a, c);              // foo_2
    foo_sub(a, d);          // foo_3 — inlined from foo_sub
}
```
After inlining, three calls to `foo` are visible at the same hierarchy level, enabling ALLOCATION to enforce a single shared instance.

### INLINE Options

| Option | Effect |
|---|---|
| `#pragma HLS INLINE` | Inline this function into its callers |
| `#pragma HLS INLINE recursive` | Recursively inline **all** functions below this level |
| `#pragma HLS INLINE off` | Prevent automatic inlining of this function |

> On the top-level function with `recursive`, **all function hierarchy** in the design is removed.

---

## 3. Function Pipelining

Function pipelining is handled similarly to **loop pipelining** (see Chapter 3). The function body is treated as a loop body called multiple times — overlapping successive calls for throughput.

```cpp
void my_func(int in, int *out) {
#pragma HLS PIPELINE II=1
    // All loops inside are automatically unrolled
    // Successive function calls are pipelined and can overlap
    *out = ...;
}
```

### Requirements

- All loops in the function body and its hierarchy below are **automatically unrolled** when pipelining.
- If a loop has **variable bounds** and cannot be unrolled, it prevents the function from being pipelined.

---

## 4. Function Instantiation

`FUNCTION_INSTANTIATE` creates **independently optimized per-call-site copies** of a function when one or more arguments are compile-time constants at each call site.

### Problem Without Instantiation

```cpp
char func(char inval, char incr) {
#pragma HLS INLINE OFF
    return inval + incr;
}

void top(char inval1, char inval2, char inval3,
         char *outval1, char *outval2, char *outval3)
{
    *outval1 = func(inval1,   0);   // incr always 0 here
    *outval2 = func(inval2,   1);   // incr always 1 here
    *outval3 = func(inval3, 100);   // incr always 100 here
}
```
Without `FUNCTION_INSTANTIATE`: one shared `func` implementation handles all 3 cases, requiring control logic to branch on `incr` at runtime.

### With FUNCTION_INSTANTIATE

```cpp
char func(char inval, char incr) {
#pragma HLS INLINE OFF
#pragma HLS FUNCTION_INSTANTIATE variable=incr   // constant at each call site
    return inval + incr;
}
```
HLS creates **3 separate, specialized copies** of `func` — one per call site:
- `func1`: `incr=0` → simplifies to just `return inval`
- `func2`: `incr=1` → simplifies to just `return inval + 1`
- `func3`: `incr=100` → simplifies to just `return inval + 100`

> Each copy has smaller, simpler logic than the generic version. Best used when:
> - Functions are called at different hierarchy levels (hard to share without extensive inlining).
> - Multiple small optimized copies are preferable to one large unoptimized shared copy.

---

## 5. Best Practices

| Practice | Rationale |
|---|---|
| **Top-level function must not be static** | Required constraint for synthesis |
| **Use `INLINE` to enable cross-boundary sharing** | `ALLOCATION` only works within a single hierarchy level |
| **Use `INLINE recursive` on top-level for flat designs** | Removes all hierarchy — maximum optimization freedom, but harder to read reports |
| **Use `INLINE off` to block aggressive auto-inlining** | Preserves distinct hierarchy for per-function reports and reuse |
| **Use `FUNCTION_INSTANTIATE` for constant-argument specialization** | Reduces control logic area; improves latency at specific call sites |
| **Pipeline functions rather than loops when calls repeat** | Function-level pipeline expresses inter-call overlap cleanly |
| **Do not use variable-bound loops inside pipelined functions** | Cannot unroll → blocks function pipeline |
| **Access global state through top-level arguments, not globals** | External test bench and host code can only observe/drive function arguments |

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 5: Functions Primer, Pages 100–103.*
