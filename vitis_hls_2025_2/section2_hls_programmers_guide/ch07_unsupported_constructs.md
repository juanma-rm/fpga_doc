# Chapter 7 — Unsupported C/C++ Constructs
**Section II: HLS Programmers Guide · UG1399 v2025.2**

---

## Table of Contents
1. [Synthesis Requirements](#1-synthesis-requirements)
2. [System Calls](#2-system-calls)
3. [Dynamic Memory Allocation](#3-dynamic-memory-allocation)
4. [Pointer Limitations](#4-pointer-limitations)
5. [Recursive Functions](#5-recursive-functions)
6. [Standard Template Libraries (STL)](#6-standard-template-libraries-stl)
7. [Undefined Behaviors](#7-undefined-behaviors)
8. [Virtual Functions](#8-virtual-functions)
9. [Quick Reference Table](#9-quick-reference-table)

---

## 1. Synthesis Requirements

For a C/C++ function to be synthesized into hardware:

1. The function and all its calls must contain the **entire functionality** of the design.
2. None of the functionality can be performed via **system calls** to the OS.
3. All C/C++ constructs must have **fixed or bounded size** — no dynamic sizing.
4. The implementation must be **unambiguous** — all paths must be statically determinable.

---

## 2. System Calls

System calls operate on the OS and have no hardware equivalent. They cannot be synthesized.

### Automatically Ignored (No Error)

| Call | Behavior |
|---|---|
| `printf()` | Ignored during synthesis |
| `fprintf(stdout, ...)` | Ignored during synthesis |
| `cout <<` | Ignored during synthesis |

### Must Be Removed

| Category | Examples |
|---|---|
| File I/O | `fopen()`, `fclose()`, `fprintf(fp, ...)`, `getc()` |
| Time | `time()`, `sleep()` |
| Memory | `malloc()`, `free()`, `alloc()` |

### Using `__SYNTHESIS__` to Exclude Code

```cpp
void my_func(...)
{
#ifndef __SYNTHESIS__
    FILE *fp = fopen("debug.dat", "w");
    fprintf(fp, "%d\n", intermediate_value);
    fclose(fp);
#endif
    // synthesizable logic continues here
}
```

> **Rules for `__SYNTHESIS__`:**
> - Only use it in **synthesizable source code** — NOT in test bench files.
> - **Never define or undefine** `__SYNTHESIS__` in your code or compiler options — HLS defines it automatically.
> - Do **not** use it to change design functionality (causes C sim ≠ RTL mismatch).

---

## 3. Dynamic Memory Allocation

`malloc()`, `free()`, `alloc()`, `new`, `delete` — all use OS-managed memory and cannot be synthesized. The design must be **fully self-contained** with statically known resources.

### Transformation Pattern (Preferred)

Use a user-defined macro (not `__SYNTHESIS__`) so both C sim and synthesis use the same final code path after validation:

```cpp
//#define NO_SYNTH   // Enable for initial C-sim, disable before synthesis

dout_t malloc_removed(din_t din[N], dsel_t width) {
#ifdef NO_SYNTH
    long long *out_accum  = malloc(sizeof(long long));
    int       *array_local = malloc(64 * sizeof(int));
#else
    long long  _out_accum;
    long long *out_accum  = &_out_accum;        // pointer to stack variable
    int        _array_local[64];
    int       *array_local = &_array_local[0];  // pointer to stack array
#endif
    // ... original pointer-based code unchanged ...
}
```

### Recommended Workflow

1. Add user macro `NO_SYNTH`; modify code to add both versions.
2. Enable `NO_SYNTH` → run C sim → save golden results.
3. Disable `NO_SYNTH` → run C sim → verify identical results.
4. Synthesize with `NO_SYNTH` disabled.

> This ensures that **the exact same code is simulated and synthesized**, avoiding hidden behavioral divergences.

---

## 4. Pointer Limitations

| Limitation | Status |
|---|---|
| Pointer to pointer on **top-level interface** | ❌ Not supported |
| Pointer to pointer **internally** | ✅ Supported (HLS inlines functions using it — can increase runtime) |
| General pointer casting (user-defined types) | ❌ Not supported |
| Pointer casting between native C/C++ types | ✅ Supported |
| Array of pointers — pointer to scalars/arrays | ✅ Supported |
| Array of pointers — pointer to pointers | ❌ Not supported |
| Function pointers | ❌ Not supported |

---

## 5. Recursive Functions

Recursive functions cannot be synthesized. This includes:

**Standard recursion:**
```cpp
unsigned foo(unsigned n) {
    if (n == 0 || n == 1) return 1;
    return foo(n-2) + foo(n-1);  // ❌ multiple recursion
}
```

**Tail recursion:**
```cpp
unsigned foo(unsigned m, unsigned n) {
    if (m == 0) return n;
    if (n == 0) return m;
    return foo(n, m % n);     // ❌ tail recursion not supported either
}
```

### Synthesis-Safe Alternative: C++ Templates for Tail Recursion

```cpp
// Tail-recursive Fibonacci using template specialization
template<data_t N> struct fibon_s {
    template<typename T>
    static T fibon_f(T a, T b) {
        return fibon_s<N-1>::fibon_f(b, a+b);   // recursive template
    }
};

// Termination condition (N=1 → base case)
template<> struct fibon_s<1> {
    template<typename T>
    static T fibon_f(T a, T b) { return b; }
};
```

The compiler resolves the recursion at compile-time through template instantiation, producing a fully static call tree.

---

## 6. Standard Template Libraries (STL)

Most STL implementations use:
- Function recursion
- Dynamic memory allocation
- Dynamic construction/destruction of objects

All of these are unsynthesizable. **STLs cannot be directly synthesized.**

**Solution:** Write a local equivalent function that:
1. Has no recursion.
2. Uses only statically sized arrays or stack variables.
3. Does not dynamically create or destroy objects.

> **Exception:** Standard data types like `std::complex<T>` are supported (except `std::complex<long double>`).

---

## 7. Undefined Behaviors

C/C++ undefined behaviors produce **different results in simulation vs synthesis**.

### Classic Example — Uninitialized Variable in Loop

```cpp
for (int i = 0; i < N; i++) {
    int val;               // uninitialized
    if (i == 0)    val = 0;
    else if (cond) val = 1;
    // val is UNDEFINED here if neither condition true
    A[i] = val;            // undefined behavior
    val++;                 // dead code — never executes in hardware
}
```

**CPU behavior:** `val` happens to retain its value from the previous iteration (same register/stack slot) — looks like "it works".

**HLS behavior:** The synthesized RTL does NOT preserve the previous value across iterations — result is indeterminate.

### Fix

Option 1 — Initialize every iteration:
```cpp
int val = 0;   // always initialized
```

Option 2 — Move declaration above loop (extend lifetime to match intended scope):
```cpp
int val = 0;    // declared and initialized outside the loop
for (int i = 0; i < N; i++) { ... }
```

> Do **not** rely on CPU-specific undefined behavior to "work" in HLS — the compiler may synthesize a different behavior than the CPU runtime.

---

## 8. Virtual Functions

**Virtual functions are not supported** for synthesis.

---

## 9. Quick Reference Table

| Construct | Supported? | Workaround |
|---|---|---|
| `printf()`, `cout <<` | Ignored (safe) | None needed — automatically discarded |
| `fopen()`, `fclose()`, file I/O | ❌ | Wrap with `#ifndef __SYNTHESIS__` |
| `malloc()` / `free()` / `new` / `delete` | ❌ | Replace with fixed-size stack/global arrays |
| Recursive functions | ❌ | Rewrite iteratively; use C++ templates for compile-time recursion |
| Function pointers | ❌ | Inline directly or use `FUNCTION_INSTANTIATE` |
| Virtual functions | ❌ | Use non-virtual C++ polymorphism / templates |
| Pointer-to-pointer on interface | ❌ | Use arrays instead |
| Pointer casting (native types) | ✅ | |
| Pointer casting (user types) | ❌ | Assign member-by-member using native types |
| STL containers (`std::vector`, etc.) | ❌ | Write bounded local equivalents |
| `std::complex<T>` (non-long-double) | ✅ | |
| `std::complex<long double>` | ❌ | Use `float`/`double` complex instead |
| Uninitialized variables in conditionals | ⚠ Undefined | Always initialize; extend variable lifetime |
| `-m32` compilation flag | ❌ | Use 64-bit builds only |

---

### See Also

- [Chapter 6 — Data Types](ch06_data_types.md) — Supported types and pointer patterns
- [Chapter 36 — Unsupported Features](../section7_vitis_hls_migration_guide/ch36_unsupported_features.md) — Additional unsupported pragmas and features
- [Chapter 35 — Deprecated Features](../section7_vitis_hls_migration_guide/ch35_deprecated_unsupported.md) — Deprecated Tcl commands and libraries

---

*Summary generated from Vitis HLS User Guide UG1399 v2025.2 — Chapter 7: Unsupported C/C++ Constructs, Pages 151–156.*
