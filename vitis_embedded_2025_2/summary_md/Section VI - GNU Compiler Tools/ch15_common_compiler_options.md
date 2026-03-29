# Chapter 15 — Common Compiler Usage and Options

## Usage

```bash
<Compiler_Name> [options] files...
```

## Input/Output Files and Extensions

| Extension | File Type |
|-----------|-----------|
| `.c` | C file |
| `.C`, `.cxx`, `.cpp`, `.c++`, `.cc` | C++ file |
| `.S` | Assembly file (with preprocessor directives) |
| `.s` | Assembly file (no preprocessor directives) |

**Output files:**

| Option | Output |
|--------|--------|
| (default) | ELF file (`a.out`) |
| `-S` | Assembly file (`.s`) |
| `-c` | Object file (`.o`) |
| `-save-temps` | `.i`/`.ii` (preprocessor) + `.s` (assembly) + `.o` (object) |
| `-o <name>` | Named ELF file |

## Libraries

| Library | Description |
|---------|-------------|
| `libxil.a` | Drivers, software services, initialization files (Vivado-specific) |
| `libc.a` | Standard C library (strcmp, strlen, etc.) |
| `libgcc.a` | GCC low-level library (floating point, 64-bit arithmetic emulation) |
| `libm.a` | Math library (cos, sin, etc.) |
| `libsupc++.a` | C++ support (exception handling, RTTI) |
| `libstdc++.a` | C++ standard platform library (stream I/O, string, etc.) |

All libraries are linked automatically. Vitis modifies `libxil.a` to add driver and library routines.

## Language Dialect and Name Mangling

- **GCC** determines dialect from file extension; **G++** always defaults to C++
- G++ automatically links `libstdc++.a` and `libsupc++.a`
- G++ mangles all symbol names (even `.c` files)
- To prevent name mangling of C symbols in mixed C/C++ code:

```c
#ifdef __cplusplus
extern "C" {
#endif
int foo();
int morefoo();
#ifdef __cplusplus
}
#endif
```

> All Vivado drivers and libraries follow this convention in their header files. Include necessary headers when compiling with G++.

## General Compiler Options

| Option | Description |
|--------|-------------|
| `-E` | Preprocess only |
| `-S` | Compile only (generates `.s`) |
| `-c` | Compile and assemble only (generates `.o`) |
| `-g` | Add DWARF2 debug information |
| `-gstabs` | Add STABS debug info for assembly files |
| `-O0` | No optimization |
| `-O1` | Medium optimization |
| `-O2` | Full optimization |
| `-O3` | Full optimization + automatic inlining |
| `-Os` | Optimize for size |
| `-v` | Verbose mode |
| `-save-temps` | Save intermediate files |
| `-o <file>` | Set output filename |
| `-Wp,<opt>` | Pass option to preprocessor |
| `-Wa,<opt>` | Pass option to assembler |
| `-Wl,<opt>` | Pass option to linker |
| `-help` | Show available options |
| `-B <dir>` | Add to C runtime library search path |
| `-L <dir>` | Add to library search path |
| `-I <dir>` | Add to header search path |
| `-l <lib>` | Search library for undefined symbols (prefixes `lib` automatically) |

> ⚠️ Optimization levels 1+ cause code rearrangement. Do not use optimization while debugging — GDB results can be inconsistent.

> ⚠️ The `-l` library flag must appear **after** all source files on the command line.

## Library and Header Search Options

```bash
# Link custom library
compiler source_files -L${LIBDIR} -l project
# Search custom include path
compiler -I /custom/include source_files
```

## Default Search Paths

| Type | Path |
|------|------|
| Libraries | `$XILINX_VITIS/gnu/<processor>/<platform>/<processor-lib>/usr/lib` |
| Headers | `$XILINX_VITIS/gnu/<processor>/<platform>/<processor-lib>/usr/include` |
| Init files | `$XILINX_VITIS/gnu/<processor>/<platform>/<processor-lib>/usr/lib` |

Where:
- `<processor>`: `microblaze`, `aarch32`, `aarch64`, `armr5`
- `<processor-lib>`: `microblazeeb-xilinx-elf`, `aarch32-xilinx-eabi`, `aarch64-none/aarch64-xilinx-elf`, `gcc-arm-none-eabi/armrm-xilinx-eabi`
- `<platform>`: `lin64` (Linux) or `nt` (Windows)

## Linker Options

| Option | Description | Default |
|--------|-------------|---------|
| `-defsym _STACK_SIZE=<value>` | Total stack allocation (bytes) | 400 bytes (100 words) |
| `-defsym _HEAP_SIZE=<value>` | Total heap allocation (bytes) | 0 |

> Minimum stack size: 16 bytes (0x0010) required for programs linked with AMD-provided CRT files.

## Memory Layout

- **MicroBlaze/MicroBlaze-V and Arm Cortex-A9/R5**: 32-bit logical addresses (0x0 – 0xFFFFFFFF)
- **Arm Cortex-A53/A72**: 64-bit logical addresses

| Memory Type | Description |
|-------------|-------------|
| Reserved memory | Interrupt vectors, OS routines (processor-defined) |
| I/O memory | Memory-mapped peripheral addresses |
| User/Program memory | Instructions, read-only data, read-write data, stack, heap |

**MicroBlaze reserved memory:** 0x0–0x4F (reset, interrupt, exception vectors). Default text start: `0x50`.

> For Arm memory maps: UG585 (Zynq-7000), UG1085 (ZU+/Versal).

## Object-File Sections

| Section | Description | Flags | Map to |
|---------|-------------|-------|--------|
| `.text` | Executable instructions | x, r, i | ROM |
| `.rodata` | Read-only data | r, i | ROM |
| `.sdata2` | Small read-only data (<8 bytes) | r, i | ROM |
| `.data` | Read-write data | w, i | RAM |
| `.sdata` | Small read-write data (<8 bytes) | w, i | RAM |
| `.sbss2` | Small read-only uninitialized data | r | ROM |
| `.sbss` | Small uninitialized data | w | RAM |
| `.bss` | Uninitialized data | w | RAM |
| `.heap` | Program heap | — | RAM |
| `.stack` | Program stack | — | RAM |
| `.init` | Language initialization code | x, r, i | ROM |
| `.fini` | Language cleanup code | x, r, i | ROM |
| `.ctors` | Constructor function list | w, i | RAM |
| `.dtors` | Destructor function list | w, i | RAM |
| `.got` / `.got2` | Program data pointers | w, i | RAM |
| `.eh_frame` | Exception handling frame info | r, i | ROM |
| `.tbss` | Thread-local uninitialized data | w | RAM |
| `.tdata` | Thread-local initialized data | w, i | RAM |
| `.gcc_except_table` | Language-specific exception data | — | RAM |
| `.jcr` | Java class registration info | — | RAM |
| `.fixup` | Fixup tables | — | RAM |

> Use the `-G` option to change the threshold for small data sections (default: 8 bytes).

## Linker Scripts

Linker scripts map input sections to output sections and memories. Use `-T <script>` to specify a custom script:

```bash
# Via compiler
mb-gcc -T linker_script.ld <options and input files>

# Via linker directly
mb-ld -T linker_script.ld <options and input files>
```

To change only the program start address:

```bash
mb-gcc <files> -Wl,-defsym -Wl,_TEXT_START_ADDR=0x100  # MicroBlaze
```

Default linker scripts location: `$XILINX_/gnu/<proc>/<platform>/<proc_name>/lib/ldscripts/`

| Script | Usage |
|--------|-------|
| `elf32<proc>.x` | Default |
| `elf32<proc>.xn` | With `-n` option |
| `elf32<proc>.xbn` | With `-N` option |
| `elf32<proc>.xr` | With `-r` option |
| `elf32<proc>.xu` | With `-Ur` option |

> Generate linker scripts in Vitis by right-clicking the application component and selecting **Reset Link Script**.

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 15 (pp. 201–215)*
