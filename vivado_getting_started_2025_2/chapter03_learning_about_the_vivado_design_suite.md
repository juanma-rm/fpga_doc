# Chapter 3: Learning About the Vivado Design Suite

This chapter provides guidance on where and how to learn about the AMD Vivado Design Suite. It covers the Documentation Navigator, Design Hubs, Quick Help, video tutorials, step-by-step tool tutorials, and the full documentation suite.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Overview](#overview) | Summary of learning resources and recommended starting points |
| [Documentation Navigator](#documentation-navigator) | Integrated documentation management environment (DocNav) |
| [Design Hubs](#design-hubs) | Task-organized documentation links and FAQ resources |
| [Vivado Quick Help](#vivado-quick-help) | Context-sensitive help within the Vivado IDE |
| [QuickTake Video Tutorials](#quicktake-video-tutorials) | Short task-focused training videos |
| [Tool Tutorials](#tool-tutorials) | Step-by-step hands-on tutorials with example designs |
| [Documentation Suite](#documentation-suite) | Complete reference to user guides, reference guides, and methodology guides |

---

## Overview

AMD provides multiple learning paths for the Vivado Design Suite:

> **Recommended:** For a hands-on approach to learning the tool, follow the [QuickTake Video Tutorials](#quicktake-video-tutorials) and the [Tool Tutorials](#tool-tutorials) sections.

> **Tip:** For quick access to information on different parts of the Vivado IDE, click the **Vivado Quick Help** button (?) in the window or dialog box.

---

## Documentation Navigator

The **AMD Documentation Navigator (DocNav)** is integrated with the Vivado Design Suite. It provides an environment to access and manage the entire set of AMD documentation for hardware and software products, training, and support materials.

### How to Open DocNav

| Platform | Method |
|----------|--------|
| **Vivado IDE** | Select any documentation link on the Getting Started page or in the Help menu |
| **Windows** | Start → All Programs → Xilinx Design Tools → DocNav (or double-click the DocNav desktop shortcut) |
| **Linux** | Enter `docnav` at the command prompt |

### Features

| Feature | Description |
|---------|-------------|
| **Catalog** | Displays all available AMD software and hardware documents, QuickTake videos, Design Advisories, and Application Notes |
| **Filters** | View documentation by document type, specific devices, or other relevant categories |
| **Search** | Find documentation based on search terms — works for both local repository and AMD website |
| **Design Hubs** | Quick access to documentation, training, and information for specific design tasks |
| **UltraFast™ Design Methodology Checklist** | Run the checklist on your design to ensure AMD recommended practices are followed |
| **Quick Download** | Manages downloading AMD documentation to your local desktop |
| **Documentation Update** | Monitors and indicates when documents are updated on the AMD website |

> **Recommended:** Click the **Update Catalog** button at the top of the Documentation Navigator to update to the latest document catalog from the AMD website. This ensures the latest documents and videos are available.

### See Also

- [Chapter 2: Getting Started with the Vivado Design Suite](chapter02_getting_started_with_the_vivado_design_suite.md#reviewing-documentation-and-videos)

---

## Design Hubs

**AMD Design Hubs** provide links to documentation organized by **design tasks** and other topics. Use them to learn key concepts and address frequently asked questions.

### How to Access Design Hubs

| Method | Location |
|--------|----------|
| **Documentation Navigator** | Click the **Design Hub View** tab |
| **AMD Website** | Visit the Design Hubs page |

### See Also

- [Chapter 1: Navigating Content by Design Process](chapter01_vivado_design_suite_overview.md#navigating-content-by-design-process)

---

## Vivado Quick Help

The **Vivado Quick Help** system provides context-sensitive help directly within the Vivado IDE.

### How to Use

- Click the **?** button in dialog boxes, windows, and wizards
- **Dialog boxes and wizards:** Button located in the **lower left corner**
- **Windows:** Button located in the **upper-right corner**

### Quick Help Features

| Feature | Description |
|---------|-------------|
| **Overview** | Description of the feature and its inputs/settings |
| **References** | Links to user guides, QuickTake videos, and related documentation |
| **Search** | Locate text within a specific help file |
| **Navigation** | Back and forward buttons for viewing Quick Help history |

---

## QuickTake Video Tutorials

AMD provides a series of **short training videos** focused on specific design tasks.

### Access Points

| Source | Location |
|--------|----------|
| **Documentation Navigator** | Available in the DocNav Catalog |
| **AMD Website** | Vivado Design Suite QuickTake Video Tutorials page |
| **YouTube** | AMD/Xilinx YouTube channel |

### See Also

- [Documentation Navigator](#documentation-navigator)

---

## Tool Tutorials

AMD provides **step-by-step software tool tutorials** to help you get working in the Vivado IDE quickly.

### Tutorial Characteristics

- Use **small example designs** for practical, hands-on learning
- Each tutorial contains a series of **independent labs** relevant to the tutorial subject
- Cover specific design tasks in the tool

### Access Points

| Source | Location |
|--------|----------|
| **Documentation Navigator** | Available in DocNav |
| **AMD Website** | Vivado Design Suite Documentation page |

### Key Tutorials

| Tutorial | Document ID | Description |
|----------|------------|-------------|
| Vivado Design Suite Tutorial: Design Flows Overview | UG888 | Step-by-step instructions for Tcl and design flows |

---

## Documentation Suite

The Vivado Design Suite documentation is organized into three categories:

### User Guides

Categorized by **design task** for easy navigation. Contain detailed information about running specific commands and performing specific design tasks.

| Guide | ID | Topic |
|-------|----|-------|
| Using the Vivado IDE | UG893 | GUI interface and features |
| Using Tcl Scripting | UG894 | Tcl commands and scripting |
| System-Level Design Entry | UG895 | Design entry and source management |
| Designing with IP | UG896 | IP catalog and IP management |
| Design Flows Overview | UG892 | Project Mode, Non-Project Mode, design flows |
| Design Analysis and Closure Techniques | UG906 | Timing analysis and design closure |
| Programming and Debugging | UG908 | Hardware Manager, ILA, VIO |
| Release Notes, Installation, and Licensing | UG973 | Installation and system requirements |
| Getting Started | UG910 | This document |

### Reference Guides

Provide reference information for:

- **Tcl commands**
- **Constraints** (XDC/SDC)
- **Device libraries**

### Methodology Guides

Provide high-level guidance for:

- **Design migration** (ISE to Vivado)
- **Large design guidance**
- **UltraFast Design Methodology**

### See Also

- [Chapter 4: Learning About the UltraFast Design Methodology](chapter04_learning_about_the_ultrafast_design_methodology.md)

---

## Best Practices

1. **Start with QuickTake videos** — Short, focused videos provide the fastest introduction to specific design tasks
2. **Follow the tool tutorials** — Hands-on experience with example designs builds practical skills
3. **Keep DocNav updated** — Click "Update Catalog" regularly to access the latest documentation
4. **Use Quick Help in context** — Click the ? button within the Vivado IDE for immediate, relevant documentation
5. **Use Design Hubs** — Task-organized documentation helps you find what you need for your current design phase
6. **Run the UltraFast Methodology Checklist** — Ensure your design follows AMD recommended practices

---

## Quick Reference

| Resource | Access Method |
|----------|--------------|
| Documentation Navigator | Vivado IDE Help menu, Start Menu (Windows), `docnav` (Linux) |
| Design Hubs | DocNav → Design Hub View tab, or AMD website |
| Quick Help | Click ? button in Vivado IDE dialogs/windows |
| QuickTake Videos | DocNav, AMD website, YouTube |
| Tool Tutorials | DocNav, AMD website |
| User Guides | DocNav, AMD website (by design task) |
| Reference Guides | DocNav, AMD website (Tcl, constraints, libraries) |
| Methodology Guides | DocNav, AMD website (migration, large designs) |

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Getting Started (UG910)
- **Version:** v2025.2, November 20, 2025
- **Chapter:** 3 — Learning About the Vivado Design Suite
- **Pages:** 12–15
