# Appendix B — Instruction/Operator Explanation

> UG1399 (v2025.2) · Pages 898–899

## Overview

This appendix defines the internal HLS compiler instruction and operator names that appear in analysis reports, schedules, and the Vitis HLS viewer. Standard LLVM instructions are documented at: https://llvm.org/docs/LangRef.html#instruction-reference

---

## Operator Reference Table

| Name | Description |
|---|---|
| `FSqrt` | Compute the square root of `float` |
| `FRSqrt` | Compute the reciprocal of square root of `float` |
| `FRecip` | Compute the reciprocal of `float` |
| `FLog` | Compute the logarithm of `float` |
| `FExp` | Compute the exponential of `float` |
| `DSqrt` | Compute the square root of `double` |
| `DRSqrt` | Compute the reciprocal of square root of `double` |
| `DRecip` | Compute the reciprocal of `double` |
| `DLog` | Compute the logarithm of `double` |
| `DExp` | Compute the exponential of `double` |
| `BlackBox` | Instantiate a blackbox function |
| `BitSelect` | Select a single bit of a variable |
| `BitSet` | Set a single bit of a variable |
| `PartSelect` | Select a range of bits of a variable |
| `PartSet` | Set a range of bits of a variable |
| `BitConcatenate` | Concatenate two variables |
| `XorReduce` | Compute XOR reduce of a variable — defined by `xor_reduce()` in `ap_(u)int` types |
| `XnorReduce` | Compute XNOR reduce of a variable — defined by `xnor_reduce()` in `ap_(u)int` types |
| `AndReduce` | Compute AND reduce of a variable — defined by `and_reduce()` in `ap_(u)int` types |
| `NandReduce` | Compute NAND reduce of a variable — defined by `nand_reduce()` in `ap_(u)int` types |
| `OrReduce` | Compute OR reduce of a variable — defined by `or_reduce()` in `ap_(u)int` types |
| `NorReduce` | Compute NOR reduce of a variable — defined by `nor_reduce()` in `ap_(u)int` types |
| `Read` | Read a value from an interface |
| `Write` | Write a value to an interface |
| `NbRead` | Non-blocking read a value from an interface |
| `NbWrite` | Non-blocking write a value to an interface |
| `ReadReq` | Send a read request to a bus (M_AXI only) |
| `WriteReq` | Send a write request to a bus (M_AXI only) |
| `WriteResp` | Receive a write response from a bus (M_AXI only) |
| `MemShiftRead` | Shift the registers of an SRL primitive |
| `Mux` | Select a value from multiple values |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Appendix B, pages 898–899*
