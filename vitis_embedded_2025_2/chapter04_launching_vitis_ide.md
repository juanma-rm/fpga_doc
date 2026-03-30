# Chapter 4 — Launching the Vitis Unified IDE

How to launch the Vitis Unified IDE, including all supported launch modes (GUI, Analysis, Interactive, Batch, Jupyter) and their command-line options.

---

## Table of Contents

- [Environment Setup](#environment-setup)
- [Launch Modes](#launch-modes)
- [Command Reference](#command-reference)

---

## Environment Setup

Before launching the Vitis Unified IDE, source the environment and optionally set up additional variables:

```bash
# Load Vitis environment
source <Vitis_Installation_Directory>/settings64.sh

# Optional: Set up XRT for data center acceleration
source <XRT_Install_Path>/setup.sh

# Optional: Set platform repository path
export PLATFORM_REPO_PATHS=<platform_path>
```

## Launch Modes

| Mode | Command | Description |
|------|---------|-------------|
| **GUI** (default) | `vitis -w <workspace>` | Graphical IDE with optional workspace argument |
| **Analysis** | `vitis -a [<file/folder>]` | Opens Analysis View for summary reports, waveform files (`.wdb`, `.wcfg`) |
| **Interactive** | `vitis -i` | Python interactive shell outside the GUI; type `help()` for available modules |
| **Batch** | `vitis -s <script>.py` | Executes Python script and exits |
| **Jupyter** | `vitis -j` | Launches Jupyter Notebook server with Vitis environment |

> **Note:** The GUI Welcome page differs between the full Vitis installer and the Embedded installer.

## Command Reference

```
Syntax: vitis [-a | -w | -i | -s | -h | -v]

Options:
  (default)    Launches New Vitis IDE
  -a/--analyze [<summary file | folder | waveform file>]
               Open summary/waveform in Analysis view
  -w/--workspace <workspace_location>
               Launch with specified workspace
  -i/--interactive
               Python interactive shell
  -s/--source <python_script>
               Run Python script
  -j/--jupyter
               Launch Jupyter Web UI
  -h/--help    Display help
  -v/--version Display version
```

---

## Source Attribution

- **Document:** UG1400 (v2025.2) — Vitis Embedded Software Development
- **Date:** November 20, 2025
- **Chapter:** 4 (pp. 22–24)
