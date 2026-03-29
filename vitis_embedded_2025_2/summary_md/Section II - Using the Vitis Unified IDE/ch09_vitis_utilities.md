# Chapter 9 — Vitis Utilities

## Software Debugger

Launch XSDB console. Reference: **Software Debugger Reference Guide (UG1725)**.

## Program Device

Access: **Vitis → Program Device**

| Option | Description |
|--------|-------------|
| Project | System project to use |
| Connection | Hardware/server connection |
| Bitstream/PDI File | Bitstream or PDI file path |
| Partial Bitstream | Indicates partial bitstream |
| BMM/MMI File | MicroBlaze Block RAM info (Vivado-generated) |
| Skip Revision Check | Skip version check |
| Generate | Stitch ELF with bitstream |
| Program | Program the FPGA |

## Vitis Terminal

**Terminal → New Terminal** — forked from current working environment. Run standalone utilities: Bootgen, Program Flash, Program Device, etc.

## Project Export and Import

### Export:
1. **File → Export**
2. Select component(s) to export
3. Browse output location → **Next** → **Finish**
4. Creates ZIP archive with all relevant files

### Import:
1. **File → Import**
2. Select archive file and target workspace → **Next**
3. Select components → **Next** → **Finish**

> Archives can transfer between workspaces, computers, and users.

## Generating Device Tree

Available during platform creation. Enable **Generate Device Tree Blob (DTB)** option in the platform creation wizard to generate DTB or DTB overlay.

See [Chapter 6 — Creating a Platform Component from XSA](ch06_develop.md#creating-a-platform-component-from-xsa).

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 9 (pp. 143–147)*
