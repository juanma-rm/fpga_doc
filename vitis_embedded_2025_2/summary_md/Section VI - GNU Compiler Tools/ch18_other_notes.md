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

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 18 (pp. 235–236)*
