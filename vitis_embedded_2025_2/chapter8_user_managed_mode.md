# Chapter 8 — User Managed Mode

User Managed Mode lets you manage source code hierarchy and build process independently (via custom Makefile or CMake). Ideal for command-line-oriented developers. Supports Makefile-based projects.

## Activating User Managed Mode

Automatically activated when the IDE opens a workspace with:
- **No JSON component files** (no `vitis-comp.json`)
- **Files/folders present** in the workspace

## Build Configuration

1. Hover over **Build** in Flow Navigator → click **Settings**
2. Click **+ New Build Configuration**
3. Input:
   - Build command/directory
   - Clean command
   - Run directory
4. Click **Build**

## Debug Configuration

1. Hover over **Debug** → click **Settings**
2. Click **+ New Launch Configuration**

### Embedded Standalone options:

| Mode | Description |
|------|-------------|
| **Configure Device and Start Debug** | Specify XSA file; for bare-metal debug |
| **Attach to Running Target** | Connect to already-running target |

### Embedded Linux options:

| Mode | Description |
|------|-------------|
| **Transfer ELF and Start Debugging** | Upload and debug Linux app |
| **Attach to Running Processor on Linux Target** | Connect to running Linux target |

## Setting User Tool Chain

Support multiple toolchain versions:

```bash
# Windows
set VITIS_IDE_USER_TOOLCHAIN=<custom_tool_chain_bin_directory_path>

# Linux
export VITIS_IDE_USER_TOOLCHAIN=<custom_tool_chain_bin_directory_path>
```

Then launch Vitis from the same terminal/CMD.

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 8 (pp. 140–142)*
