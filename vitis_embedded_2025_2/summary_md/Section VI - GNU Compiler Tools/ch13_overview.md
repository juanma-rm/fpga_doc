# Chapter 13 — Overview

The Vivado Design Suite includes GCC for:

| Processor | Compiler | Assembler | Linker |
|-----------|----------|-----------|--------|
| MicroBlaze / MicroBlaze-V | `mb-gcc` / `mb-g++` | `mb-as` | `mb-ld` |
| Cortex-A9 | `arm-none-eabi-gcc` / `arm-none-eabi-g++` | `arm-none-eabi-as` | `arm-none-eabi-ld` |
| Cortex-A53 / Cortex-A72 | `aarch64-none-elf-gcc` / `aarch64-none-elf-g++` | `aarch64-none-elf-as` | `aarch64-none-elf-ld` |
| Cortex-R5F | `armr5-none-eabi-gcc` / `armr5-none-eabi-g++` | `armr5-none-eabi-as` | `armr5-none-eabi-ld` |

- Supports C and C++ languages
- Includes C, math, GCC, and C++ standard libraries
- Uses GNU binutils (assembler, linker, object dump) based on GNU version 2.32 (2020.x)

> From the 2024.1 release, this guide supports MicroBlaze and MicroBlaze-V devices.

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 13 (p. 200)*
