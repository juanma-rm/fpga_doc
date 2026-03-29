# Chapter 14 — Compiler Framework

The GNU compiler is a wrapper that calls four stages sequentially:

```
Input C/C++ Files
  → cpp0 (Pre-processor) — replaces macros with definitions
  → cc1 / cc1plus (C/C++ Compiler) — optimizations, assembly generation
  → as (Assembler) — converts mnemonics to machine language, creates .o files
  → ld (Linker) — links object files + libraries → Output ELF File
```

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 14 (p. 200)*
