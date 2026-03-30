# Chapter 3: Using Manage IP Projects

The Vivado IDE provides a special project type for managing customizations and output products of IP, called a Manage IP Project. This chapter covers creating Manage IP projects, customizing IP, and using IP example designs.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Manage IP Flow](#manage-ip-flow) | Overview and invocation of the Manage IP flow |
| [Creating a Manage IP Project](#creating-a-manage-ip-project) | Setting up a new IP location with part, language, and simulator |
| [Customizing IP in the Manage IP Project](#customizing-ip-in-the-manage-ip-project) | Working with IP in Manage IP; features and limitations |
| [Managing IP in the Manage IP Project](#managing-ip-in-the-manage-ip-project) | IP example designs and standalone IP evaluation |

---

## Manage IP Flow

The Manage IP Project provides:

- Exploring IP in the IP catalog
- Customizing IP with full parameter control
- Managing a centralized location of customized IP

IP customization (XCI) and output products are stored in **separate directories outside** the Manage IP project. The project manages design runs for DCP generation and other output products.

> **Note:** This flow does not support subsystem IP.

### When to Use Manage IP

| Scenario | Recommendation |
|----------|---------------|
| **Team environments** | Create and maintain customized IP outside the project structure |
| **Many AMD IP** | Centralized management simplifies revision control |
| **Non-project script flow** | Recommended methodology for IP management |
| **Cross-project IP reuse** | Customized IP with output products can be used in multiple designs |

### See Also

- [Chapter 2: IP Basics — Adding Existing IP](chapter2_ip_basics.md#creating-an-ip-customization)

---

## Creating a Manage IP Project

### Steps

1. Launch Vivado IDE → Getting Started page → **Manage IP**
2. Select **New IP Location** (or Open existing / Recent)
3. Configure settings in the **Manage IP Settings** dialog:

| Setting | Description |
|---------|-------------|
| **Part** | Active part — all output products generated for this part |
| **Target language** | Language of the top-level module (Verilog/VHDL) |
| **Target Simulator** | Vivado simulator or third-party simulator |
| **Simulator language** | VHDL, Verilog, SystemVerilog, or Mixed |
| **IP location** | Where the `managed_ip_project` directory is created |

4. Click **Finish**

> **Note:** IP location may also be referred to as an IP Repository.

Each IP customization gets its own directory under the specified manage IP location, containing the XCI file and generated output products.

---

## Customizing IP in the Manage IP Project

After the project opens, you have access to the full IP catalog including:

- IP Product Guides
- Change Logs
- Product web pages
- Answer Records

### Managed IP Features

- Simple IP project interface
- Direct access to AMD IP catalog
- Ability to customize multiple IP simultaneously
- Separate, unique directories for each IP customization
- Option to generate or skip DCP generation (DCP is default)

> ⚠️ **Important:** AXI Peripheral IP is not suited for use in a Managed IP Project — Vivado issues an error. Use a regular project instead.

> ⚠️ **Caution:** When creating a new AXI4 peripheral, verification through AXI4 VIP and JTAG interface are not available in Manage IP. Create a standard Vivado project for peripheral verification.

---

## Managing IP in the Manage IP Project

### IP Example Designs

Many AMD IP deliver an **example design project** consisting of:

- Top-level logic and constraints that interact with the IP customization
- Example test bench for simulation

> **Tip:** Rather than upgrading an existing example design, create a new one from the IP in the new release to ensure it supports the latest IP version.

### Opening an Example Design

1. In IP Sources tab, select the IP customization
2. Right-click → **Open IP Example Design**
3. Specify the output location (project named `<ip_name_ex>`)
4. Review summary → new Vivado IDE session opens with the example design

```tcl
# Open example design via Tcl
open_example_project [get_ips <ip_name>]
```

> ⚠️ **Important:** Do not store example designs in the IP directory. AMD recommends putting IP directories into revision control but not projects.

### Examining Standalone IP

After implementing a standalone IP example design:

- **Implementation Completed** dialog offers: open implemented design, generate bitstream, or view reports
- Timing analysis uses ideal clocks (not fully accurate — hold analysis may show violations the router would fix)
- Some IP include `HD.CLK_SRC` property in `_ooc.xdc` for improved timing accuracy

> ⚠️ **Important:** The implemented IP is for analysis only — results are not used or preserved during implementation of the top-level design.

### See Also

- [Chapter 2: IP Basics](chapter2_ip_basics.md)
- Vivado Design Suite QuickTake Video: Configuring and Managing Reusable IP in Vivado
- Vivado Design Suite QuickTake Video: Working with Design Checkpoints

---

## Best Practices

1. **Store IP outside the project directory** for easier revision control and team sharing
2. **Generate DCP for all IP** before sharing — recipients can use IP immediately without resynthesis
3. **Use the Manage IP flow** for team environments to provide a consistent IP repository
4. **Create fresh example designs** from new IP versions rather than upgrading existing ones
5. **Do not store example design projects in IP directories** — keep them separate for clean revision control

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Chapter:** 3 — Using Manage IP Projects / Chapter 4 — Using IP Example Designs
- **Pages:** 72–79
