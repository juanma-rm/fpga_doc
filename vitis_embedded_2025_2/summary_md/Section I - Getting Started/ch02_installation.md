# Chapter 2 — Vitis Software Platform Installation

### Prerequisites

- System must meet requirements described in **UG1742** — Vitis Software Platform Release Notes
- Disable anti-virus software and close non-essential programs to reduce installation time

### Installation Steps

1. Download the installer from the AMD Adaptive Computing Downloads Website
2. Run `xsetup` (Linux) or `xsetup.exe` (Windows)
3. Accept license agreements
4. Select product to install:

| Product Option | Description |
|---------------|-------------|
| **Vitis** (full) | Embedded + acceleration development; includes Vivado, v++, AI Engine toolchains |
| **Vitis Embedded Development** | Embedded processors only; smaller footprint |

5. Customize installation — select design tools and devices
6. Specify installation directory and install

### Post-Installation

```bash
# Linux only — run with sudo privileges
sudo <install_dir>/<release>/Vitis/scripts/installLibs.sh
```

> ⚠️ Windows does not require this script. On Linux, pay attention to missing package messages and install them manually (e.g., `zip` utility).

### Optional: Vitis IP Cache

Enable **Vitis IP Cache** during installation to install cache files at:
```
<install_dir>/<release>/Vitis/data/cache/xilinx
```

### Device Requirements

> ⚠️ For the Vitis acceleration flow, this device choice is required: **Devices → Install devices for Alveo and Edge acceleration platforms**

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 2 (p. 9)*
