# Chapter 10 — Python Vitis Commands

The Vitis CLI is an interactive and scriptable command-line interface based on Python. It supports project management, configuration, building, and debugging — including creating platforms and domains, creating system and application projects, configuring/building BSPs and applications, managing repositories, downloading/running applications on hardware, reading/writing registers, and setting breakpoints and watch expressions.

> **Tip:** View all Python APIs from the Vitis menu: **Help → Document → Vitis Python API Documentation.**

> **Reference:** Full CLI command details at `<Vitis_install>/2025.2/Vitis/cli/api_docs/build/html/vitis.html`

---

## Enabling the Vitis API in a Python Environment

Enables the Vitis Python API in your own Python environment so you can run generic Python scripts within the Vitis tool.

### Linux

```bash
# Set environment
export XILINX_VITIS=<VITIS_INSTALL_DIR>/2025.2/Vitis
source <VITIS_INSTALL_DIR>/2025.2/Vitis/cli/examples/customer_python_utils/setup_vitis_env.sh

# Launch Python
$VITIS_INSTALL_PATH/2025.2/Vitis/tps/lnx64/python-3.13.0/bin/python

# Or use your local Python
./python
```

```python
# In the Python shell
import vitis
client = vitis.create_client()
client.get_template()
```

```bash
# Run a script directly
$VITIS_INSTALL_PATH/2025.2/Vitis/tps/lnx64/python-3.13.0/bin/python -s sample_testcase.py
```

### Windows

```bat
:: Set environment
set XILINX_VITIS=<VITIS_INSTALL_DIR>\2025.2\Vitis
<VITIS_INSTALL_DIR>\2025.2\Vitis\cli\examples\customer_python_utils\setup_vitis_env.bat

:: Launch Python
<VITIS_INSTALL_DIR>\2025.2\Vitis\tps\win64\python-3.13.0\python.exe

:: Run a script
<VITIS_INSTALL_DIR>\2025.2\Vitis\tps\win64\python-3.13.0\python.exe -s sample_testcase.py
```

---

## Executing Python APIs

Two ways to run Python APIs:

| Mode | Command | Description |
|------|---------|-------------|
| **CLI Interactive** | `vitis -i` | Opens the Vitis interactive Python shell |
| **Batch Script** | `vitis -s <script.py>` | Executes a Python script in batch mode |
| **Interactive + Script** | `vitis -i` then `run <script.py>` | Runs a script inside the interactive shell |

### Client Lifecycle APIs

| Python API | Description | Example |
|------------|-------------|---------|
| `vitis.create_client()` | Create Vitis client | `client = vitis.create_client()` |
| `client.set_workspace(path)` | Set/switch workspace | `client.set_workspace(path="/vitis_2025.2_ws")` |
| `client.get_template()` | Get available templates | `templates = client.get_template()` |
| `client.get_component(name)` | Get existing component | `comp = client.get_component(name="app1")` |
| `vitis.dispose()` | Close client connections | `vitis.dispose()` |

### Platform Component

| Python API | Description | Example |
|------------|-------------|---------|
| `create_platform_component` | Creates a platform | `platform = client.create_platform_component(name=<name>, hw_design=<xsa>, ...)` |
| `get_platform` | Gets existing platform | `plat = client.get_platform(name="platform_name")` |
| `add_domain` | Adds a domain (BSP/OS) | `domain = platform.add_domain(name=<name>, cpu=<cpu_name>, ...)` |
| `build` | Builds platform | `platform.build()` |

```python
platform = client.create_platform_component(
    name="vck190_platform",
    hw_design="/project_2/ext_platform_wrapper.xsa",
    os="aie_runtime", cpu="ai_engine", domain_name="aie_runtime_ai_engine",
    generate_dtb=False
)
platform = client.get_component(name="vck190_platform")
status = platform.build()
```

### Application Component

| Python API | Description | Example |
|------------|-------------|---------|
| `create_app_component` | Creates an application | `app = client.create_app_component(name=<name>, platform=<platform>, ...)` |
| `get_app` | Gets existing application | `app = client.get_app(name="app_name")` |
| `build` | Builds application | `app.build()` |

```python
app = client.create_app_component(
    name="test_app",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="template_name"
)
app = client.get_component(name="test_app")
app.build()
```

### System Project

| Python API | Description | Example |
|------------|-------------|---------|
| `create_sys_project` | Creates a system project | `sys_proj = client.create_sys_project(name=<name>, platform=<platform>, ...)` |
| `add_component` | Adds component to system | `sys_proj.add_component(name=<comp_name>)` |
| `build` | Builds system project | `sys_proj.build()` |

```python
sys_proj = client.create_sys_project(
    name="system_project",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="empty_accelerated_application"
)
sys_proj_comp = sys_proj.add_component(name="hello_world")
sys_proj_comp.build()
vitis.dispose()
```

### AI Engine Component

| Python API | Description | Example |
|------------|-------------|---------|
| `create_aie_component` | Creates an AIE component | `aie = client.create_aie_component(name=<name>, platform=<platform>, template=<template>)` |
| `add_cfg_file` | Adds a configuration file | `aie.add_cfg_file(cfg_file=<file>)` |
| `build` | Generates the AIE component | `aie.build(target="hw")` |

```python
comp = client.create_aie_component(
    name="simple_aie_application",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="installed_aie_examples/simple"
)
comp = client.get_component(name="simple_aie_application")
comp.build(target="hw")
```

### HLS Component

| Python API | Description | Example |
|------------|-------------|---------|
| `create_hls_component` | Creates an HLS component | `hls = client.create_hls_component(name=<name>, cfg_file=[<file>], template=<template>)` |
| `add_cfg_file` | Adds a configuration file | `hls.add_cfg_file(cfg_file=<file>)` |
| `run` | Runs a specified operation | `hls.run(operation=<operation_type>)` |

```python
comp = client.create_hls_component(
    name="mm2s", cfg_file=["hls_config.cfg"],
    template="empty_hls_component"
)
cfg = client.get_config_file(path="/vitis_2025.2_ws/mm2s/hls_config.cfg")
cfg.set_value(section="hls", key="syn.compile.clang_version", value="7")
cfg.set_value(section="hls", key="package.output.format", value="rtl")
```

---

## Modifying Configuration Files

Python APIs can modify configuration files for each component (UserConfig.cmake, lscript.ld, hls_config.cfg, aie_compiler.cfg). The equivalent Python commands are always visible in the `workspace_journal.py` file.

### Configuration File API

| Python API | Description | Example |
|------------|-------------|---------|
| `get_config_file` | Gets a handle to a configuration file | `cfg = client.get_config_file(path="<workspace>/<comp>/hls_config.cfg")` |
| `set_value` | Sets a key-value pair in a config section | `cfg.set_value(section="hls", key="syn.compile.clang_version", value="7")` |
| `add_lines` | Adds configuration lines | `cfg.add_lines(values=["param=compiler.addOutputTypes=hw_export"])` |

Supported configuration files:

| File | Component | Typical Keys |
|------|-----------|-------------|
| `UserConfig.cmake` | Application | Sources, symbols, libraries, linker, optimization |
| `lscript.ld` | Application | Memory regions, stack/heap sizes, section mapping |
| `hls_config.cfg` | HLS | `syn.compile.clang_version`, `package.output.format` |
| `aiecompiler.cfg` | AI Engine | `event-trace`, `xlopt` |
| `*-link.cfg` | System Project | Container linking parameters |

---

## Workspace Journal Coverage

The workspace journal (`workspace_journal.py`) logs all user actions from the IDE:

- **Component creation** — platform, application, AIE, HLS, system project
- **Component builds** — all build operations
- **Configuration file modifications** — UserConfig.cmake, lscript.ld, hls_config.cfg, aie_compiler.cfg

> **Tip:** View journal in the IDE: **Vitis → Workspace Journal**

> **Replay:** You can find all the Vitis Python commands to rebuild a workspace in `<vitis_workspace>/_ide/workspace_journal.py`

```python
# Example workspace journal (auto-generated)
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")

# Platform
platform = client.create_platform_component(
    name="vck190_platform", hw_design="/project_2/ext_platform_wrapper.xsa",
    os="aie_runtime", cpu="ai_engine", domain_name="aie_runtime_ai_engine",
    generate_dtb=False
)
platform = client.get_component(name="vck190_platform")
status = platform.build()

# AIE component
comp = client.create_aie_component(
    name="simple_aie_application",
    platform="<ws>/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="installed_aie_examples/simple"
)
comp.build(target="hw")

# HLS components
comp = client.create_hls_component(name="mm2s", cfg_file=["hls_config.cfg"], template="empty_hls_component")
comp = client.create_hls_component(name="s2mm", cfg_file=["hls_config.cfg"], template="empty_hls_component")

# System project
proj = client.create_sys_project(
    name="simple_aie_application_system_project",
    platform="<ws>/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="empty_accelerated_application", build_output_type="xsa"
)
proj = client.get_sys_project(name="simple_aie_application_system_project")
status = proj.add_container(name="binary_container_1")
proj = proj.add_component(name="mm2s", container_name="binary_container_1")
proj = proj.add_component(name="s2mm", container_name="binary_container_1")
proj = proj.add_component(name="simple_aie_application", container_name="binary_container_1")

# Configuration modifications
cfg = client.get_config_file(path="<ws>/simple_aie_application/aiecompiler.cfg")
cfg.set_value(section="aie", key="event-trace", value="runtime")
cfg.set_value(section="aie", key="xlopt", value="2")

cfg = client.get_config_file(path="<ws>/mm2s/hls_config.cfg")
cfg.set_value(section="hls", key="syn.compile.clang_version", value="7")
cfg.set_value(section="hls", key="package.output.format", value="rtl")

vitis.dispose()
```

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Chapter 10 (pp. 148–165)*
