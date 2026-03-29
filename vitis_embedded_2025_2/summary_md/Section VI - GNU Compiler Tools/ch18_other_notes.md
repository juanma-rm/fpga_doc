# Chapter 18 — Other Notes

## C++ Code Size

C++ generates larger code/data than equivalent C programs due to exception handling and RTTI overhead.

| Switch | Effect |
|--------|--------|
| `-fno-exceptions` | Remove exception handling overhead |
| `-fno-rtti` | Remove runtime type information overhead |

> C++ programs may have more intensive dynamic memory requirements (stack and heap). Review requirements carefully.

## C++ Standard Library Limitations

- Only a few STDIN/STDOUT streams are supported on the default Vivado platform
- Locale functions, thread-safety, and other features may not be supported
- `new` and `delete` are **not thread-safe** — use caution in OS environments

## Position Independent Code

- MicroBlaze supports `-fPIC` but Vivado only provides standalone platforms
- Debuggers cannot interpret relocatable code
- AMD libraries, startup files, and tools do not support PIC features
- Third-party OS vendors may use PIC in their distributions

## Unsupported Features

Not all GCC switches are supported by Vivado compilers (e.g., `-fprofile-arcs`). Some features are experimental and may produce incorrect code. See GCC documentation.

---

## Best Practices

1. **Use `-g` without optimization for debugging** — optimization levels 1+ rearrange code and produce inconsistent debug results.
2. **Place `-l` flags after source files** — the linker searches only in one direction.
3. **Use `extern "C"`** in mixed C/C++ projects to prevent name mangling of C symbols.
4. **Enable hardware features** when available — `-mno-xl-soft-mul`, `-mxl-barrel-shift`, `-mhard-float` significantly improve MicroBlaze performance.
5. **Use `-mxl-gp-opt` consistently** — must be on both compile and link commands.
6. **Review stack/heap sizes** for C++ programs, which have more intensive memory requirements.
7. **Use `-relax`** when invoking `mb-ld` directly to remove unnecessary `imm` instructions.
8. **Single-precision math** (`libm_*_fps.a`) gives better MicroBlaze FPU performance if double precision is not required.
9. **Thread safety** — C/C++ standard libraries are not thread-safe; use mutual exclusion in multi-threaded environments.

---

## Quick Reference

### Compiler Names

| Processor | GCC | G++ | Assembler | Linker |
|-----------|-----|-----|-----------|--------|
| MicroBlaze | `mb-gcc` | `mb-g++` | `mb-as` | `mb-ld` |
| Cortex-A9 | `arm-none-eabi-gcc` | `arm-none-eabi-g++` | `arm-none-eabi-as` | `arm-none-eabi-ld` |
| Cortex-A53/A72 | `aarch64-none-elf-gcc` | `aarch64-none-elf-g++` | `aarch64-none-elf-as` | `aarch64-none-elf-ld` |
| Cortex-R5F | `armr5-none-eabi-gcc` | `armr5-none-eabi-g++` | `armr5-none-eabi-as` | `armr5-none-eabi-ld` |

### MicroBlaze Feature Flags

| Feature | Enable | Disable (Default) |
|---------|--------|-------------------|
| Hardware multiply | `-mno-xl-soft-mul` | `-mxl-soft-mul` |
| Multiply high | `-mxl-multiply-high` | `-mno-xl-multiply-high` |
| Hardware divide | `-mno-xl-soft-div` | `-mxl-soft-div` |
| Barrel shifter | `-mxl-barrel-shift` | `-mno-xl-barrel-shift` |
| Pattern compare | `-mxl-pattern-compare` | `-mno-xl-pattern-compare` |
| Hardware FPU | `-mhard-float` | `-msoft-float` |

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 18 (pp. 235–236)*
