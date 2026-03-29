# Chapter 16 — MicroBlaze Compiler Usage and Options

The MicroBlaze GNU compiler automatically defines `__MICROBLAZE__` during compilation.

## Processor Feature Selection Options

| Option | Description | Default | Pre-processor Definition |
|--------|-------------|---------|------------------------|
| `-mcpu=vX.YY.Z` | Target hardware version | — | — |
| `-mlittle-endian` / `-mbig-endian` | Endianness selection | Big-endian | — |
| `-mno-xl-soft-mul` | Enable 32-bit hardware multiplier | — | `HAVE_HW_MUL` |
| `-mxl-multiply-high` | Enable 32×32 high multiply | — | `HAVE_HW_MUL_HIGH` |
| `-mxl-soft-mul` | Software multiply emulation | **Default** | — |
| `-mno-xl-soft-div` | Enable hardware divider | — | `HAVE_HW_DIV` |
| `-mxl-soft-div` | Software divide emulation | **Default** | — |
| `-mxl-barrel-shift` | Enable hardware barrel shifter | — | `HAVE_HW_BSHIFT` |
| `-mno-xl-barrel-shift` | No barrel shifter | **Default** | — |
| `-mxl-pattern-compare` | Enable pattern compare instructions | — | `HAVE_HW_PCMP` |
| `-mno-xl-pattern-compare` | No pattern compare | **Default** | — |
| `-mhard-float` | Hardware single-precision FPU | — | `HAVE_HW_FPU` |
| `-msoft-float` | Software floating point emulation | **Default** | — |
| `-mxl-float-convert` | Enable FPU conversion instructions (fint, flt) | — | — |
| `-mxl-float-sqrt` | Enable FPU square root (fsqrt) | — | — |

**`-mcpu` behavior by version:**

| Version | Pipeline | Delay Slot Behavior |
|---------|----------|-------------------|
| Pre-v3.00.a | 3-stage | Does not inhibit exceptions in delay slots |
| v3.00.a, v4.00.a | 3-stage | Inhibits exception-causing instructions in delay slots |
| v5.00.a+ | 5-stage | Does not inhibit exceptions in delay slots |

## General Program Options

| Option | Description |
|--------|-------------|
| `-msmall-divides` | Optimized table-lookup for small divides (0–15 range, signed) |
| `-mxl-gp-opt` | Use small data area anchors for variables < threshold (saves instructions) |
| `-mno-clearbss` | Skip .bss zero-initialization at startup (for simulation) |
| `-mxl-stack-check` | Add stack overflow checking in function prologues |

> ⚠️ When using `-mxl-gp-opt`, provide it to **both** compile and link commands. Inconsistent use leads to errors.

**Stack overflow handling:** When `-mxl-stack-check` is enabled, stack overflow sets `_stack_overflow_error = 1` and jumps to `_stack_overflow_exit`. Override by providing your own `_stack_overflow_exit` function.

## Application Execution Modes

| Mode | Flag | CRT File | Description |
|------|------|----------|-------------|
| Executable | `-xl-mode-executable` | `crt0.o` | Default standalone mode |
| Bootstrap | `-xl-mode-bootstrap` | `crt2.o` | For bootloader-loaded applications |
| No Vectors | `-xl-mode-novectors` | `crt3.o` | No reset/interrupt/exception vectors (smaller code) |

> ⚠️ Do not use more than one execution mode on the command line.

## Position Independent Code

The MicroBlaze compiler supports `-fPIC` and `-fpic` for PIC generation:
- Uses Global Offset Table (GOT) for data access relocation
- Uses Procedure Linkage Table (PLT) for shared library function calls
- Used by Linux for shared libraries and relocatable executables

## MicroBlaze Assembler

`mb-as` supports all MicroBlaze instruction set opcodes except `imm` (auto-generated when needed).

**Pseudo-opcodes:**

| Pseudo-op | Replacement Instruction | Explanation |
|-----------|------------------------|-------------|
| `nop` | `or R0, R0, R0` | No operation |
| `la Rd, Ra, Imm` | `addik Rd, Ra, Imm` | Load address |
| `not Rd, Ra` | `xori Rd, Ra, -1` | Bitwise NOT |
| `neg Rd, Ra` | `rsub Rd, Ra, R0` | Negate |
| `sub Rd, Ra, Rb` | `rsub Rd, Rb, Ra` | Subtract |

> The `-relax` linker option removes unnecessary `imm` instructions auto-inserted by the assembler.

## MicroBlaze Linker Options

| Option | Description | Default |
|--------|-------------|---------|
| `-defsym _TEXT_START_ADDR=<value>` | Set text section start address | `0x28` |
| `-relax` | Remove unnecessary `imm` instructions | Auto with mb-gcc |
| `-N` | Set text/data as readable and writable | Auto with mb-gcc |

## MicroBlaze Linker Script Sections

| Section | Description |
|---------|-------------|
| `.vectors.reset` | Reset vector code |
| `.vectors.sw_exception` | Software exception vector code |
| `.vectors.interrupt` | Hardware interrupt vector code |
| `.vectors.hw_exception` | Hardware exception vector code |
| `.text` | Program instructions |
| `.rodata` | Read-only variables |
| `.sdata2` | Small read-only static/global variables |
| `.data` | Static/global variables with initial values |
| `.sdata` | Small static/global variables with initial values |
| `.sbss2` | Small read-only uninitialized variables |
| `.sbss` | Small uninitialized variables |
| `.bss` | Uninitialized variables (zeroed by boot code) |
| `.heap` | Heap memory |
| `.stack` | Stack memory |

**Linker script tips:**
- Assign vector sections to appropriate hardware-defined memories
- Define boundary variables: `_SDATA_START__`, `_SDATA_END__`, `_SDATA2_START__`, `_SDATA2_END__`, `_bss_start`, `_bss_end`, etc.
- Set `_stack` to location after `_STACK_SIZE` in `.bss`
- Multiple `.bss` sections require a custom CRT

## Startup Files

### First Stage CRT Files

| File | Description | Use Case |
|------|-------------|----------|
| `crt0.o` | Populates all vectors, calls `_crtinit`, loops at `_exit` | Standalone (default) |
| `crt1.o` | All vectors except breakpoint/reset, calls `_crtinit` | Software-intrusive debug |
| `crt2.o` | All vectors except reset, calls `_crtinit` | Bootloader-loaded apps |
| `crt3.o` | Only reset vector, calls `_crtinit` | No vectors (small code) |

### Second Stage CRT Files

| File | Steps |
|------|-------|
| `crtinit.o` | Clear .bss → `_program_init` → `_init` (constructors) → `main` → `_fini` (destructors) → `_program_clean` |
| `pgcrtinit.o` | Clear .bss → `_program_init` → `_profile_init` → `_init` → `main` → `_fini` → `_profile_clean` → `_program_clean` |
| `sim-crtinit.o` | `_program_init` → `_init` → `main` → `_fini` → `_program_clean` (no .bss clear, with `-mno-clearbss`) |
| `sim-pgcrtinit.o` | `_program_init` → `_profile_init` → `_init` → `main` → `_fini` → `_profile_clean` → `_program_clean` |

**Register initialization in CRT:**

| Register | Value | Description |
|----------|-------|-------------|
| `r1` | `_stack-16` | Stack pointer (16-byte initial offset for arguments) |
| `r2` | `_SDA2_BASE_` | Read-only small data anchor |
| `r13` | `_SDA_BASE_` | Read-write small data anchor |

**Startup sources:** `<AMD_install>/Vitis/<version>/data/embeddedsw/lib/microblaze/src/`

Use `-nostartfiles` to prevent default startup files, `-B <dir>` to specify custom CRT location.

## Compiler Libraries

MicroBlaze library names encode hardware configuration:

| Encoding | Description |
|----------|-------------|
| `_bs` | Barrel shifter enabled |
| `_m` | Hardware multiplier enabled |
| `_p` | Pattern comparator enabled |

Location: `$XILINX_/gnu/microblaze/<platform>/microblaze-xilinx-elf/lib`

**Math library precision:**
- Default: double-precision (`libm_*_fpd.a`)
- For better performance with MicroBlaze FPU: use single-precision (`libm_*_fps.a`)
- Copy desired `libm_*_fps.a` to your processor library folder as `libm.a` and rebuild

> ⚠️ MicroBlaze C and math libraries are **not thread-safe**. Functions like `printf()`, `scanf()`, `malloc()`, `free()` cause unrecoverable errors in multi-threaded environments. Use mutual exclusion mechanisms.

> MicroBlaze programs cannot take command line arguments. `argc` and `argv` are initialized by CRT routines.

## Interrupt Handlers

| Attribute | Behavior | Return Instruction |
|-----------|----------|-------------------|
| `interrupt_handler` | Saves MSR + all volatiles (or only used volatiles for leaf functions) | `rtid` |
| `save_volatiles` | Same as interrupt_handler but different return | `rtsd` |
| `fast_interrupt` | Minimal register save, jumps directly to handler address | — |

```c
void my_handler() __attribute__((interrupt_handler));
void my_handler2() __attribute__((save_volatiles));
void my_handler3() __attribute__((fast_interrupt));
```

> The attribute should only appear in the prototype, not the definition.

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 16 (pp. 216–232)*
