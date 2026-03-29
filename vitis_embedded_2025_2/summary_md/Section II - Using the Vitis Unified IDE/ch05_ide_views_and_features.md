# Chapter 5 — Vitis Unified IDE Views and Features

Comprehensive guide to all views, panels, and features of the Vitis Unified IDE including the Explorer, Debug view, source control, search, code editor, preferences, and keyboard shortcuts.

---

## Table of Contents

- [IDE Layout Overview](#ide-layout-overview)
- [Vitis Explorer View](#vitis-explorer-view)
- [Terminating a Backend Process](#terminating-a-backend-process)
- [Search View](#search-view)
- [Source Control (Git)](#source-control-git)
- [Debug View](#debug-view)
- [Example View](#example-view)
- [Code View and Smart Editor](#code-view-and-smart-editor)
- [Issue and Source Code Cross-Probing](#issue-and-source-code-cross-probing)
- [Parallel Compiling](#parallel-compiling)
- [Workspace Journal](#workspace-journal)
- [External Lopper Support](#external-lopper-support)
- [Extensions](#extensions)
- [Segmented Configuration (Versal)](#segmented-configuration-versal)
- [Preferences](#preferences)
- [Keyboard Shortcuts and Command Palette](#keyboard-shortcuts-and-command-palette)

---

## IDE Layout Overview

| Area | Description |
|------|-------------|
| **Toolbar Menu** | Quick access to major features; customizable via View dropdown |
| **Component Explorer** (left) | Virtual hierarchy of workspace components and projects |
| **Central Editor** (center) | Edit components, configurations, and source files |
| **Flow Navigator** (right) | Design flow for the active component (build, debug, etc.) |
| **Console/Terminal** (bottom) | Output transcripts, terminal, pipeline view |
| **Index** (bottom) | List of build step transcripts for the session |

---

## Vitis Explorer View

### Toolbar Actions

| Action | Description |
|--------|-------------|
| Create New Component | Start new component wizard |
| Filter Components | Hide/show components |
| Refresh | Refresh the explorer |
| Collapse All | Minimize displayed contents |

### Right-Click Menu (Component)

| Action | Description |
|--------|-------------|
| Open in Terminal | Terminal at component directory |
| Show in Flow Navigator | Highlight component in Flow Navigator |
| Delete | Remove component from workspace |
| Clone Component | Duplicate for design exploration (not for System projects) |
| Reset Linker Script | Generate new linker script for standalone apps |

### Right-Click Menu (Sources Folder)

New File, New Folder, Open in Terminal, Paste, Import → Files/Folders, Add Source File

### Deep JSON-Based Component Display

All components from the current workspace display in the Component View with unique names, regardless of subdirectory depth. Unsupported components show notifications.

---

## Terminating a Backend Process

Click the **'x'** button on the progress bar at the bottom-left corner of the IDE.

**Terminable processes:**
- Building/creating a component
- Emulation
- Flash programming
- BSP update
- Run, debug, and XSDB
- Device programming

---

## Search View

Global find-and-replace within the workspace. Searches inside file contents (not file names).

| Feature | Description |
|---------|-------------|
| Match Case | Case-sensitive search |
| Match Whole Word | Whole word matching |
| Use Regular Expression | Regex search |
| Include Ignored Files | Restore ignored files to search |
| Replace All | Bulk replace |
| Toggle Search Details | Add Files to Include / Exclude fields |

**Include/Exclude syntax:** Comma-separated, supports wildcards — e.g., `AIECompiler.log, *summary*`

> ⚠️ Be careful with the Replace function — it can introduce errors into designs.

---

## Source Control (Git)

### Cross-OS Support

Workspaces can move between Linux and Windows. Distribution methods:
1. **Version Control** — Push to GitHub repo, clone on other OS
2. **Export/Import** — Export as `.zip`, import on other OS

### Files Required for Source Control

**Workspace:**

| File | Track in Git? |
|------|--------------|
| `_ide/version.ini` | Yes |
| `_ide/settings.json` | Depends (personal settings) |
| `_ide/workspace_journal.py` | No |
| `.gitignore` | Yes |

**Platform Component:**

| File | Track in Git? |
|------|--------------|
| `export/` | No (use `git add export/* -f` if needed) |
| `hw/hw.xsa` | Yes |
| `hw/sdt/` | No (regenerate via Switch/Re-read XSA) |
| `resources/` | No |
| `vitis-comp.json` | Yes |
| `.gitignore` | Yes |
| BSP folders (e.g., `psu_cortexa53_0`) | Yes |

**Application:**

| File | Track in Git? |
|------|--------------|
| `src/` | Yes |
| `build/` | No |
| `vitis-comp.json` | Yes |
| `compile_commands.json` | No |
| `_ide/launch.json` | Depends |
| `.gitignore` | Yes |

**System Project:**

| File | Track in Git? |
|------|--------------|
| `vitis-sys.json` | Yes |
| `_ide/launch.json` | Depends |
| `.gitignore` | Yes |

> **Note:** Always ignore `_ide/` folders. The IDE auto-generates them when loading a workspace.

### Enabling Git

```bash
# In workspace terminal
git init
```

> ⚠️ Requires User ID and Password configured.

### Common Git Operations (GUI Equivalents)

| Action | GUI | CLI Equivalent |
|--------|-----|---------------|
| Stage file | Right-click → `+ Stage Changes` | `git add <file>` |
| Stage component | Source Control → View As Tree → `+ Stage Changes` | `git add platform/` |
| Commit | Enter message, Ctrl+Enter | `git commit -m "<msg>"` |
| Push | Via terminal | `git push --set-upstream origin master` |

### Source Control for Platform BSP

1. Clone: `git clone https://github.com/Xilinx/embeddedsw.git`
2. Checkout version: `cd embeddedsw && git checkout xilinx_v2025.2`
3. **Vitis → Embedded SW Repositories** → Add local repository
4. Click **Rescan Repositories**
5. In Platform JSON → Board Support Package → select local BSP → **Regenerate BSP**

---

## Debug View

| Feature | Description |
|---------|-------------|
| **Control Panel** | Continue, Step Over, Step Into, Step Out, Restart, Stop |
| **Threads** | Switch between debugging threads |
| **Call Stack** | Function call stack, updates during execution |
| **Variables** | Current global/local variable values |
| **Watch** | User-specified watch expressions (`+` to add) |
| **Breakpoints** | Set at main function by default; add by clicking line margin |
| **Memory Inspector** | Display memory at specific addresses |
| **Register Inspector** | Processor/co-processor registers at breakpoints |
| **Disassembly View** | Open from Source Code right-click menu |
| **Debug Console** | Transcript of debug process; shows MDM UART prints |

**Breakpoint types:**
- Standard breakpoint — click left margin
- Conditional breakpoint — right-click → Add Conditional Breakpoint
- Logpoint — right-click → Add Logpoint

---

## Example View

Access: Left panel icon, **View → Examples**, or **Ctrl+Shift+R**

- Browse example system projects
- Click **Show Details** to view supported OS and processor
- Click **Create Application Component from Template**

---

## Code View and Smart Editor

**Supported features:**
- Syntax highlighting for C, C++, Python, Makefile, CMakeLists.txt
- Variable/function name hints
- Jump to definition / Peek definition
- Find all references
- Outline view (function list, via `</>` button)

**Smart editor for `launch.json` / `build.json`:**
- Toggle between **GUI rendering** and **Text Editor** using table/code buttons
- Modifications in one view update the other instantly

**Auto Save:** Enabled by default; can configure triggers and delay. Manual save: **Ctrl+S**

---

## Issue and Source Code Cross-Probing

**Ctrl+Click** on an issue in the output console to jump to source code.

### Problem View

The output channel displays all warning and error messages. You can quickly navigate to the source of the error or warning in the Problem pane by clicking the error or warning message.

---

## Parallel Compiling

Non-blocking builds allow multiple concurrent builds.

> Disabled by default. Enable via: **File → Preferences → Open Settings (UI) → Vitis → Build → Parallel Build → Disable** (uncheck)

> Expect a slower response if you launch multiple build or emulation jobs at the same time on a slow server.

---

## Notification for File Change

When you modify files, the yellow indicator beside the build status icon prompts you to review and rebuild the component if necessary.

---

## New Feature Preview

New features are available for you to explore in advance. View new features by clicking **Vitis → New Feature Preview**. Before using a new feature, you must enable it.

**Disclaimer:** Preview features are currently in an early access phase. By using these features, you acknowledge and accept the following:

- **Limited functionality:** Early access features can have limited functionality compared to fully released features. They can lack functions, have bugs, or experience performance issues.
- **Potential instability:** Early access features are still being tested and refined. They are prone to crashes, errors, or unexpected behavior. Use with caution.
- **Feedback and improvements:** Your feedback is crucial. AMD encourages you to report any issues, bugs, or suggestions encountered while using these features.
- **No guarantees:** Early access features are provided on an "as-is" basis, without any warranties or guarantees. AMD reserves the right to modify, suspend, or discontinue these features without prior notice.
- **Use at your own risk:** AMD is not to be held liable for any damages, losses, or inconveniences arising from the use of these features.

---

## Relative Path Support

If imported files share the same initial node in the path as the workspace, the Vitis tool automatically selects the relative path:

- **File Path:** `/local/drive/source/app.cpp`
- **Workspace Path:** `/local/drive/workspace`
- **Resolved as:** `$COMPONENT_LOCATION/../../sources/app.cpp`

> When moving the workspace or committing to source control, remember to keep the relative path relationship.

---

## Workspace Journal

Log file recording backend commands corresponding to GUI actions.

- Open: **Vitis → Workspace Journal**
- Recreate projects: `vitis -s workspace_journal.py`
- Uses relative paths when possible

---

## External Lopper Support

Override the built-in Lopper with an external version:

```bash
export VITIS_LOPPER_INSTALL_LOC="path/to/Lopper"
```

---

## Extensions

Access: **Extensions** icon on left edge of IDE

- Marketplace from **Open VSX** (Eclipse Foundation)
- Each extension has description and detail view

> ⚠️ AMD does not screen extensions for quality or safety. Use at your own risk. This is an early-access preview feature.

### Serial Monitor Extension

- Open from **Vitis → Serial Monitor**
- View serial port output and send messages to embedded devices

---

## Segmented Configuration (Versal)

For AMD Versal devices — separately download/program Boot PDI and PL PDI components.

**Benefits:**
- Faster software boot
- Minimized local boot flash requirements
- Load PL PDI on demand

**Usage:**
- Select PL PDI in launch configuration for run/debug
- Program Flash utility supports PL PDI for flash programming

> ⚠️ Early access preview feature.

---

## Preferences

### Settings (File → Preferences)

| Setting | Description | Default |
|---------|-------------|---------|
| Auto Save | Auto-save files | Enabled |
| Color Themes | Light/Dark theme | — |
| Open Settings (UI) | Full preferences view | — |
| File Icon Theme | Icon theme selection | — |

**Zoom:** Ctrl++ to zoom in, Ctrl-- to zoom out

### Keyboard Shortcuts and Command Palette

**Keyboard Shortcuts:**
- Open: **File → Preferences → Open Keyboard Shortcuts** or **Alt+Ctrl+Comma**
- Search and edit keybindings (e.g., `Build: Hardware` = Alt+Shift+BH)

**Command Palette:**
- Open: **Ctrl+Shift+P**
- Type keyword (build, run, debug, C Syn) to find and execute commands

**Quick Find:**
- **Ctrl+P** — Find files by name
- Type `@` — Go to function in current file
- Type `:40` — Go to line 40
- Type `#` — Find function in workspace
- **Ctrl+T** — Find symbol by name

---

## See Also

- [Chapter 4 — Launching the Vitis IDE](ch04_launching_vitis_ide.md)
- [Chapter 6 — Develop](ch06_develop.md)
- [Chapter 7 — Run, Debug, and Optimize](ch07_run_debug_optimize.md)

---

## Source Attribution

- **Document:** UG1400 (v2025.2) — Vitis Embedded Software Development
- **Date:** November 20, 2025
- **Chapter:** 5 (pp. 25–54)
