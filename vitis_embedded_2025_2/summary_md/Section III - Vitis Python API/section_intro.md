# Section III — Vitis Python API

The AMD Vitis™ Unified IDE provides logical wizards within the development environment to help you develop your design. For more flexibility and extended functionality, it is essential to become familiar with using scripts. Scripts are especially useful for developing regression tests or running frequently used command sets. The AMD Vitis CLI is an interactive and scriptable command-line interface based on Python.

Vitis API supports:
- Creating platform projects and domains
- Creating system and application projects
- Configuring and building domains/BSPs and applications
- Managing repositories
- Downloading and running applications on hardware targets
- Reading and writing registers
- Setting breakpoints and watch expressions

> **Note:** View all Python APIs from the Vitis menu: **Help → Document → Vitis Python API Documentation**.

---

## Table of Contents

- [Enabling the Vitis API in a Python ENV](#enabling-the-vitis-api-in-a-python-env)
- [Python API: A Command-line Tool](#python-api-a-command-line-tool)
- [Executing Python APIs](#executing-python-apis)
- [Managing Vitis IDE Components through Python APIs](#managing-vitis-ide-components-through-python-apis)
  - [Platform](#platform)
  - [Application](#application)
  - [System Project](#system-project)
  - [AI Engine Component](#ai-engine-component)
  - [HLS Component](#hls-component)
- [Modifying Configuration Files](#modifying-configuration-files)
- [Workspace Journal Coverage](#workspace-journal-coverage)
- [Chapter Files](#chapter-files)

---

## Enabling the Vitis API in a Python ENV

Enabling the Vitis API in your user Python environment allows you to run a generic Python script within the Vitis tool.

### Linux

Open a Linux command prompt and execute:

```bash
export XILINX_VITIS=<LOCAL_VITIS_INSTALLATION_DIRECTORY>/2025.2/Vitis
source <LOCAL_VITIS_INSTALLATION_DIRECTORY>/2025.2/Vitis/cli/examples/customer_python_utils/setup_vitis_env.sh
```

Run the bundled Python interpreter:

```bash
$VITIS_INSTALL_PATH/2025.2/Vitis/tps/lnx64/python-3.13.0/bin/python
# or launch your local python:
./python
```

Execute the following Python commands to verify:

```python
import vitis
client = vitis.create_client()
client.get_template()
```

To run a Python script:

```bash
$VITIS_INSTALL_PATH/2025.2/Vitis/tps/lnx64/python-3.13.0/bin/python -s sample_testcase.py
```

### Windows

Open a Windows command prompt and execute:

```bat
set XILINX_VITIS=<LOCAL_VITIS_INSTALLATION_DIRECTORY>\2025.2\Vitis
<LOCAL_VITIS_INSTALLATION_DIRECTORY>\2025.2\Vitis\cli\examples\customer_python_utils\setup_vitis_env.bat
```

Run the bundled Python interpreter:

```bat
<vitis_install_dir>\2025.2\Vitis\tps\win64\python-3.13.0\python.exe
```

To run a Python script:

```bat
<vitis_install_dir>\2025.2\Vitis\tps\win64\python-3.13.0\python.exe -s sample_testcase.py
```

---

## Python API: A Command-line Tool

The Python API offers a scriptable approach, enabling you to create and manage Vitis components programmatically — platforms, applications, HLS designs, and AI engines.

> **Important:** Full Vitis CLI command reference is in the installation folder:
> `<Vitis_install>/2025.2/Vitis/cli/api_docs/build/html/vitis.html`

Python examples are located in: `<vitis_installation_path>/cli/examples`

---

## Executing Python APIs

To execute Python APIs, first establish the connection between server and client. Two execution modes are supported:

**1. CLI (Interactive) Mode** — supported in interactive mode only:

```bash
vitis -i
```

For more details, see *Vitis Interactive Python Shell* in the Vitis Reference Guide (UG1702).

**2. Python Script Mode** — supports batch and interactive execution:

```bash
# Batch mode:
vitis -s <script.py>

# Interactive mode:
vitis -i
vitis [1]: run <script.py>
```

### Python APIs: Manage Client

| Python API | Description | Example |
|------------|-------------|---------|
| `create_client` | Creates a client instance | `client = vitis.create_client()` |
| `dispose` | Closes all client connections and terminates server connection | `client.dispose()` |
| `exit` | Closes the session | `exit()` |

After creating and building components, open the workspace with:

```bash
vitis -w <workspace_path>
```

Components built or created through Python APIs show status **done** when opened in the IDE.

---

## Managing Vitis IDE Components through Python APIs

Before running scripts, set up the environment variables for the Vitis Unified IDE (see *Setting Up the Vitis Tool Environment* in UG1393).

The Vitis Unified IDE supports Python APIs for project flow management and creation/building of:
- **Platform Control**
- **Application Component**
- **System Project**
- **AIE**
- **HLS**

### Platform

The platform Python API supports creation, building, and modification of a platform.

| Python API | Description | Example |
|------------|-------------|---------|
| `create_platform_component` | Creates a new platform | `platform = client.create_platform_component(name="platform", hw_design="zcu102", cpu="psu_cortexa53_0", os="standalone", domain_name="standalone_a53", architecture="32-bit", compiler="gcc")` |
| `add_domain` | Adds a domain to the platform | `platform.add_domain(cpu="psu_cortexa53_0", os="standalone", name="a53_standalone", display_name="a53_standalone", generate_dtb=True, dt_overlay=True, architecture="64-bit", compiler="gcc")` |
| `build` | Generates the platform | `platform.build()` |

**Example — Create and build a platform:**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")
platform = client.create_platform_component(
    name="platform",
    hw_design="zcu102",
    os="standalone",
    cpu="psu_cortexa53_0",
    domain_name="standalone_psu_cortexa53_0",
    generate_dtb=False,
    architecture="64-bit",
    compiler="gcc"
)
platform = client.get_component(name="platform")
status = platform.build()
```

### Application

After a platform is created, use Python API to create an application component — either from a template or as an empty application with imported source code.

| Python API | Description | Example |
|------------|-------------|---------|
| `create_app_component` | Creates an application component | `app_comp = client.create_app_component(name=<name>, platform=<platform>, domain=<domain>, template=<template>, cpu=<cpu>, os=<os>, sysroot_toolchain=<path>, use_sysroot_toolchain=<bool>)` |
| `import_files` | Imports files to the app component | `app_comp.import_files(from_loc=<path>, files=["file1",...], files_to_exclude=["file1",...], dest_dir_in_cmp=<dest>, is_skip_copy_sources=False)` |
| `build` | Generates the application | `app_comp.build()` |

**Example — Create and build a Hello World application:**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")
comp = client.create_app_component(
    name="hello_world",
    platform="/vitis_2025.2_ws/platform/export/platform/platform.xpfm",
    domain="standalone_psu_cortexa53_0",
    template="hello_world"
)
comp = client.get_component(name="hello_world")
comp.build()
```

### System Project

After creating the platform and application components, create a system project. Add application components to it and trigger a unified build across all associated components.

| Python API | Description | Example |
|------------|-------------|---------|
| `create_sys_project` | Creates a system project for a given template¹ | `proj = client.create_sys_project(name="system_project", platform=<platform_path>)` |
| `add_component` | Adds a component to the system project | `proj.add_component(name="host_component")` |
| `build` | Builds the system project for a given target | `proj.build(target="hw")` |

> ¹ The embedded installer does not support accelerated flows.

**Example — Full platform → app → system project build:**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="./workspace")

plat_name = "vck190_embd"
comp_name = "standalone_embd_app"

# Create and build platform component
platform_obj = client.create_platform_component(
    name=plat_name, hw_design="vck190", cpu="psv_cortexa72_0", os="standalone"
)
platform_obj.build()

# Get the platform xpfm path
platform_xpfm = client.find_platform_in_repos(plat_name)

# Create and build application component
comp = client.create_app_component(
    name=comp_name, platform=platform_xpfm,
    domain="standalone_psv_cortexa72_0", template="hello_world"
)
comp.build()

# Create system project
sys_proj = client.create_sys_project(
    name="system_project", platform=platform_xpfm,
    template="empty_accelerated_application"
)
sys_proj_comp = sys_proj.add_component(name="hello_world")
sys_proj_comp.build()
vitis.dispose()
```

> More Python examples: `<VITIS_INSTALL_DIR>/2025.2/cli/examples`

### AI Engine Component

The Vitis Python APIs support creating and building AI Engine components from scratch or with a template.

| Python API | Description | Example |
|------------|-------------|---------|
| `create_aie_component` | Creates an AIE component | `aie_comp = client.create_aie_component(name=<name>, platform=<platform>, part=<part>, template=<template>)` |
| `add_cfg_file` | Adds a configuration file to the component | `status = component.add_cfg_file(cfg_file=<file>)` |
| `build` | Generates the AI Engine component | `aie_comp.build()` |

**Example:**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")
comp = client.create_aie_component(
    name="simple_aie_application",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="installed_aie_examples/simple"
)
comp = client.get_component(name="simple_aie_application")
comp.build(target="hw")
```

### HLS Component

The Vitis Python APIs support creating and building HLS components from scratch or with a template.

| Python API | Description | Example |
|------------|-------------|---------|
| `create_hls_component` | Creates an HLS component | `hls_comp = client.create_hls_component(name=<name>, platform=<platform>, part=<part>, cfg_file=<cfg_file>, template=<template>)` |
| `add_cfg_file` | Adds a configuration file to the HLS component | `status = component.add_cfg_file(cfg_file=<file>)` |
| `run` | Runs a specified operation on the HLS component | `status = component.run(operation=<operation_type>)` |

**Example — Create an empty HLS component and modify its config:**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")
comp = client.create_hls_component(
    name="mm2s", cfg_file=["hls_config.cfg"], template="empty_hls_component"
)
cfg = client.get_config_file(path="/vitis_2025.2_ws/mm2s/hls_config.cfg")
cfg.set_value(section="hls", key="syn.compile.clang_version", value="7")
cfg.set_value(section="hls", key="package.output.format", value="rtl")
```

---

## Modifying Configuration Files

The Python API can modify configuration files for each Vitis component. The `workspace_journal.py` file records all Python API commands equivalent to IDE actions, making it easy to discover the correct API calls.

Key configuration files that can be modified:

| File | Component | Purpose |
|------|-----------|---------|
| `UserConfig.cmake` | Application/Platform | Build system configuration |
| `lscript.ld` | Application | Linker script (memory regions, stack size) |
| `hls_config.cfg` | HLS | HLS synthesis settings (clang version, output format) |
| `aiecompiler.cfg` | AIE | AI Engine compiler settings (event-trace, xlopt, ADF levels) |

Use `client.get_config_file(path=<file>)` to get a config object, then:
- `cfg.set_value(section=<s>, key=<k>, value=<v>)` — set a single key
- `cfg.add_lines(values=[...])` — append configuration lines

> **Tip:** To discover Python API equivalents for IDE actions, check `workspace_journal.py`. In the Vitis Unified IDE, navigate to **Vitis → Workspace Journal**.

---

## Workspace Journal Coverage

The workspace journal (`workspace_journal.py`) logs all user actions performed in the Vitis Unified IDE, including:
- **Component creation**
- **Component builds**
- **Modification to configuration files** (`UserConfig.cmake`, `lscript.ld`, `hls.config.cfg`, `aie_compiler.cfg`)

**Example — Full workspace journal for a multi-component project (vck190):**

```python
import vitis
client = vitis.create_client()
client.set_workspace(path="vitis_2025.2_ws")

# Create and build platform
platform = client.create_platform_component(
    name="vck190_platform",
    hw_design="/project_2/ext_platform_wrapper.xsa",
    os="aie_runtime", cpu="ai_engine",
    domain_name="aie_runtime_ai_engine",
    generate_dtb=False
)
platform = client.get_component(name="vck190_platform")
status = platform.build()

# Create and build AIE component
comp = client.create_aie_component(
    name="simple_aie_application",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="installed_aie_examples/simple"
)
comp = client.get_component(name="simple_aie_application")
comp.build(target="hw")

# Create HLS components
comp = client.create_hls_component(name="mm2s", cfg_file=["hls_config.cfg"], template="empty_hls_component")
comp = client.create_hls_component(name="s2mm", cfg_file=["hls_config.cfg"], template="empty_hls_component")

# Create system project
proj = client.create_sys_project(
    name="simple_aie_application_system_project",
    platform="/vitis_2025.2_ws/vck190_platform/export/vck190_platform/vck190_platform.xpfm",
    template="empty_accelerated_application",
    build_output_type="xsa"
)
proj = client.get_sys_project(name="simple_aie_application_system_project")
status = proj.add_container(name="binary_container_1")
proj = proj.add_component(name="mm2s", container_name="binary_container_1")
proj = proj.add_component(name="s2mm", container_name="binary_container_1")
proj = proj.add_component(name="simple_aie_application", container_name="binary_container_1")

# Modify configurations
cfg = client.get_config_file(path="/vitis_2025.2_ws/simple_aie_application_system_project/hw_link/binary_container_1-link.cfg")
cfg.add_lines(values=["param=compiler.addOutputTypes=hw_export"])

cfg = client.get_config_file(path="/vitis_2025.2_ws/simple_aie_application/aiecompiler.cfg")
cfg.set_value(section="aie", key="event-trace", value="runtime")
cfg.set_value(section="aie", key="xlopt", value="2")

cfg = client.get_config_file(path="/vitis_2025.2_ws/mm2s/hls_config.cfg")
cfg.set_value(section="hls", key="syn.compile.clang_version", value="7")
cfg.set_value(section="hls", key="package.output.format", value="rtl")

vitis.dispose()
```

> **Note:** To view the workspace journal in the IDE, navigate to **Vitis → Workspace Journal**.

---

## Chapter Files

- [Chapter 10 — Python Vitis Commands](ch10_python_vitis_commands.md)
- [Chapter 11 — Python XSDB Commands](ch11_python_xsdb_commands.md)
- [Chapter 12 — Python XSDB Usage Examples](ch12_python_xsdb_usage_examples.md)

---

*Source: AMD Vitis Embedded Software Development (UG1400, v2025.2) — Section III, pp. 148–163*
