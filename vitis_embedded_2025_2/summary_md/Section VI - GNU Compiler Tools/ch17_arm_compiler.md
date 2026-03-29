# Chapter 17 — Arm Compiler Usage and Options

| Processor | Toolchain |
|-----------|-----------|
| Cortex-A9 | `arm-none-eabi-*` |
| Cortex-A53 / Cortex-A72 | `aarch64-none-elf-*` |
| Cortex-R5F | `armr5-none-eabi-*` |

Each toolchain includes: startup code, binutils, GCC, G++, libstdc++, GDB, newlib C library.

## Compile and Link

```bash
# Compile
arm-none-eabi-gcc -c file1.c -I<include_path> -o file1.o
arm-none-eabi-gcc -c file2.c -I<include_path> -o file2.o

# Link
arm-none-eabi-gcc -Wl,-T -Wl,lscript.ld -L<libxil_path> \
    -o "App.elf" file1.o file2.o \
    -Wl,--start-group,-lxil,-lgcc,-lc,--end-group
```

Help: `--help`, `-v --help`, `--target-help`

> Additional Arm GCC flags available on the GNU website. Actual support depends on the target processor and toolchain.

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 17 (pp. 233–234)*
