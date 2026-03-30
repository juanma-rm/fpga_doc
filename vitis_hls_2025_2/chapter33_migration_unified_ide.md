# Chapter 33 — Migrating from Vitis HLS to the Vitis Unified IDE

> UG1399 (v2025.2) · Section VII: Vitis HLS Migration Guide · Pages 873–874

## Table of Contents

- [Overview](#overview)
- [Migration Path 1: Create HLS Component from Existing Project](#migration-path-1-create-hls-component-from-existing-project)
- [Migration Path 2: Continue Using an Existing Tcl Script](#migration-path-2-continue-using-an-existing-tcl-script)
- [Migration Path 3: Convert to Python Script](#migration-path-3-convert-to-python-script)
- [Using write_ini to Create an HLS Config File](#using-write_ini-to-create-an-hls-config-file)
- [Best Practices](#best-practices)

---

## Overview

The Vitis Unified IDE provides a single environment for heterogeneous system design and Data Center acceleration applications. It replaces the classic Vitis HLS IDE and supports HLS component creation from C/C++ sources alongside the `v++` and `vitis-run` command-line tools.

There are three migration paths for an existing Vitis HLS classic project:

1. Create an HLS Component from the existing project (GUI-based)
2. Continue using an existing Tcl script (with minimal edits)
3. Convert to a Python script (using Vitis Python APIs)

---

## Migration Path 1: Create HLS Component from Existing Project

In the Vitis Unified IDE, select **Create HLS Component** and specify the `hls.app` file from the existing Vitis HLS classic project. The wizard then:
- Reads the existing `hls.app` file to determine project settings.
- Prompts for a new configuration file name (generating a config `.ini` file).
- If the project has **multiple solutions**, the wizard prompts you to select which solution(s) to import, and creates separate HLS components for each.

---

## Migration Path 2: Continue Using an Existing Tcl Script

Make two changes to the existing Tcl script:

| Change | Old (Classic Vitis HLS) | New (Unified IDE) |
|---|---|---|
| Project command | `open_project <name>` | `open_component <name>` |
| Target flow | — | Add `-flow_target vivado\|vitis` |
| Solution command | `open_solution <name>` | Remove — not required |

Example updated Tcl script header:
```tcl
open_component my_component -flow_target vivado
# open_solution is removed
set_top my_top_function
add_files my_source.cpp
csynth_design
```

**Running the script** with the Unified IDE command line:
```bash
vitis-run --mode hls --tcl <tcl_script>.tcl
```

> The workspace for the Unified IDE is the **directory from which the Tcl script is run**. Using `open_component` places the output HLS reports and generated RTL under the component directory — compatible with the Unified IDE project structure.

---

## Migration Path 3: Convert to Python Script

The Vitis Unified IDE supports Python APIs for HLS component creation and management.

**Running a Python script:**
```bash
vitis -s <python_script>.py
```

HLS component configuration in Python can be specified:
- In a separate config `.ini` file (generated via `write_ini` — see below), or
- Inline as key-value pairs within the Python script itself.

---

## Using write_ini to Create an HLS Config File

`write_ini` exports current project settings as a config file, which can then be used in the Unified IDE.

**Two ways to generate the config file:**

**Option A — Add `write_ini` inside the Tcl script:**
```tcl
open_project my_project
# ... existing project setup ...
write_ini my_config.cfg
```

**Option B — Use the interactive HLS Tcl shell:**
```bash
$ vitis-run --mode hls --itcl
HLS> open_project <project_name>
HLS> write_ini <config_file_name>
```

After generating the config file, create HLS components in the Unified IDE by pointing to the config file and the source files.

> **Tip:** The `Vitis-HLS-Introductory-Examples` repository (Migration directory on GitHub) provides example scripts demonstrating both the Tcl and Python migration approaches.

---

## Best Practices

| Recommendation | Rationale |
|---|---|
| Use `open_component` instead of `open_project` | Required for Unified IDE compatibility; applies correct output directory structure |
| Remove `open_solution` from Tcl scripts | Not required in the Unified IDE; keeping it causes errors |
| Use `write_ini` to capture config before migrating | Provides a clean starting point for the new config-file-based flow |
| Import multi-solution projects as separate HLS components | The Unified IDE maps each solution to a separate component — matches the wizard behavior |
| Use `vitis-run` for CI/CD Tcl scripts | Drop-in replacement for command-line usage with classic Tcl scripts |

---

### See Also

- [Chapter 12 — Launching Vitis IDE](../section03_vitis_hls_flow_steps/ch12_launching_vitis_ide.md) — Unified IDE setup and flow
- [Chapter 34 — Migrating from Vivado HLS](ch34_migration_vivado_hls.md) — Vivado HLS → Vitis HLS migration

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 33, pages 873–874*
