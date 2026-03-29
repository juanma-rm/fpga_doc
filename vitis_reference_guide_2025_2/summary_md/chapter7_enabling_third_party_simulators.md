# Chapter 7: Enabling Third-Party Simulators

> Source: *UG1702 Vitis Accelerated Reference Guide* v2025.2, Chapter 7 (pp. 401–403)

## Overview

The AMD Vitis™ Unified IDE supports integration with third-party simulators for hardware emulation and co-simulation workflows. This chapter describes how to configure the IDE to use third-party simulators instead of the default AMD Vivado™ simulator (XSIM).

---

## Configuring Third-Party Simulators

Third-party simulators are configured through the **Build Configuration Settings** in the Vitis Unified IDE.

### Steps

1. Open the Vitis Unified IDE.
2. Navigate to the **Build Configuration Settings** for your component or system project.
3. Under the **[advanced]** category, locate the simulator settings.
4. Under the **[Vivado]** category, configure the third-party simulator options:
   - Select the simulator type (e.g., Questa, VCS, Xcelium).
   - Set the simulator installation path.
   - Configure any simulator-specific options.
5. Save the settings and rebuild the project.

### Supported Simulators

Third-party simulators can be used for:
- **C/RTL Co-Simulation** in HLS components
- **Hardware Emulation** (hw_emu) builds in system projects
- **Logic simulation** during verification

> **Note:** Ensure the third-party simulator is properly installed and licensed before configuring it in the Vitis IDE. The simulator installation path must be accessible from the build environment.

---

## Best Practices

1. **Verify installation** — Confirm the third-party simulator is installed and its license is active before configuring it in the IDE.
2. **Use consistent simulators** — Use the same simulator across team members to ensure reproducible results.
3. **Check compatibility** — Verify that the simulator version is compatible with the Vitis 2025.2 release.

---

## See Also

- [Chapter 4: Managing Vitis HLS Components](chapter4_managing_the_vitis_hls_components_in_the_vitis_unified_ide.md) — C/RTL Co-Simulation settings
- [Chapter 3: Using the Vitis Unified IDE](chapter3_using_the_vitis_unified_ide.md) — IDE configuration and preferences
- [Chapter 8: Working with the Analysis View](chapter8_working_with_the_analysis_view.md) — Analyzing simulation results
- *Vivado Design Suite User Guide: Logic Simulation (UG900)* — Detailed simulator configuration

---

*Source: UG1702 Vitis Accelerated Reference Guide v2025.2, Chapter 7 (pp. 401–403)*
