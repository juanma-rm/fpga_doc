# Section V — XSCT to Python API Migration

Migration reference from XSCT (Xilinx Software Command-line Tool, now deprecated) to the Python CLI in the Vitis Unified IDE 2025.2. Covers all major command categories with XSCT→Python API mappings, argument translations, and behavioral differences.

---

## Table of Contents

- [Overview](#overview)
- [app — Application Project Management](#app--application-project-management)
- [bsp — BSP Configuration](#bsp--bsp-configuration)
- [createdts — Device Tree Creation](#createdts--device-tree-creation)
- [domain — Domain Management](#domain--domain-management)
- [getaddrmap / getperipherals / getprocessors](#getaddrmap--getperipherals--getprocessors)
- [getws / setws — Workspace Management](#getws--setws--workspace-management)
- [lscript — Linker Script](#lscript--linker-script)
- [platform — Platform Management](#platform--platform-management)
- [repo — Software Repositories](#repo--software-repositories)
- [sysproj — System Project Management](#sysproj--system-project-management)
- [importprojects — Project Import](#importprojects--project-import)
- [importsources — Source Import](#importsources--source-import)
- [library — Library Component](#library--library-component)
- [Key Migration Differences](#key-migration-differences)

---

## Overview

Key changes in 2025.2:

- **XSCT is deprecated** — no longer the primary scripting interface
- **Debug via XSDB** — XSDB continues to be supported for debug operations, or convert scripts to Python CLI
- **Project management via Python API** — use workspace journal (`workspace_journal.py`) to learn the Python API equivalents
- See [Section III — Vitis Python API](../Section%20III%20-%20Vitis%20Python%20API/section3_vitis_python_api.md) and the **Vitis Scripting Flows Tutorial** for details

---

## app — Application Project Management

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `app create -name <name> -platform <plat> -proc <cpu> -template <tmpl> -os <os>` | `client.create_aie_component(...)` (AIE) or `client.create_app_component(...)` (host) | In XSCT, system project is specified at creation; in Python CLI, component is created first, then added to system project separately |
| `app remove <name>` | `client.delete_component(name=<name>)` | |
| `app switch <name>` | `client.get_component(name=<name>)` | Returns app object for further operations |
| `app list` | `client.list_components()` | `-dict` option not supported in Python CLI |
| `app build -name <name>` | `component.build()` | Must get component object first; `-all` not supported in Python CLI |
| `app clean -name <name>` | `component.clean()` | |
| `app report <name>` | `component.report()` | |

### create_app_component Arguments

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Application component name |
| `platform` | Yes | Platform path or name; for baremetal, can specify domain along with platform |
| `template` | No | Template for the component |
| `domain` | No | Specify when there is more than one domain on the platform |

> **Key Difference:** In XSCT, the system project is specified during `app create`. In Python CLI, you create the component first, then add it to a system project with `sys_proj.add_component()`. This gives flexibility to add components to multiple system projects.

---

## bsp — BSP Configuration

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `bsp config <param> <value>` | `domain.set_config(option=<"lib"/"os"/"proc">, param_value=[key1:value1, ...])` | Use `list_param()` to get configurable parameters |
| `bsp getdrives` | `domain.get_drivers()` | `-dict` option not supported |
| `bsp getlibs` | `domain.get_libs()` | |
| `bsp getos` | `domain.get_os()` | |
| `bsp listparams -lib <name>` | `domain.list_params(option="lib", lib_name=<name>)` | Options: `"lib"`, `"os"`, `"proc"` |
| `bsp regenerate` | `domain.regenerate()` | |
| `bsp reload` | *Not supported in Python CLI* | |
| `bsp write` | *Not supported in Python CLI* | |
| `bsp removelib` | `domain.remove_lib(lib_name=<name>)` | |
| `bsp setdriver -driver <drv> -ip <ip>` | `domain.update_path(option='DRIVER', name=<name>, new_path=<path>)` | In Python CLI, path replaces version |
| `bsp setlib -name <lib> -ver <ver>` | `domain.update_path(option='LIBRARY', name=<name>, new_path=<path>)` | In Python CLI, path replaces version |
| `bsp setosversion -ver <ver>` | `domain.update_path(option='OS', name=<name>, new_path=<path>)` | In Python CLI, path replaces version |

> **Key Difference:** In XSCT, BSP commands use `-ver` (version) to set drivers/libraries/OS. In Python CLI, `update_path()` takes a `new_path` parameter instead — you point to the source path rather than specifying a version number.

---

## createdts — Device Tree Creation

| XSCT Argument | Python API (`client.create_platform()`) | Notes |
|--------------|---------------------------------------|-------|
| `-platform-name <name>` | `name=<platform_name>` | Required |
| `-hw <handoff-file>` | `hw=<handoff_file>` | Required |
| `-board <board>` | — | Board names from `<DTG_Repo>/device_tree/data/kernel_dtsi` |
| `-out <dir>` | — | Default: workspace directory |
| `-local-repo <dir>` | — | DTG repo cloned from Git if not specified |
| `-git-url <url>` | — | |
| `-git-branch <branch>` | — | Default: `xlnx_rel_v<Vitis-release>` |
| `-zocl` | — | Enable zocl driver support (PL-enabled designs only) |
| `-overlay` | — | Enable device-tree overlay support |
| `-dtsi <file-list>` | — | Include custom DTSI files |
| `-compile` | — | Compile DTS to DTB |
| `-update` | — | Update existing platform with new XSA |

### Additional Platform Creation Options (Python CLI)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `os` | OS for default domain | — |
| `cpu` | Processor for default domain | — |
| `domain_name` | Name of domain to create | — |
| `template` | Template for baremetal domain | `"Empty"` |
| `no_boot_bsp` | Build without boot components | — |
| `fsbl_target` | FSBL processor type (ZU+ only) | `psu_cortexa53_0` |
| `fsbl_path` | Custom FSBL path (with `no_boot_bsp`) | — |
| `pmufw_elf` | Prebuilt PMUFW ELF (with `no_boot_bsp`) | — |

> In Python CLI, `create_platform()` creates both a DTS and a platform project.

### DTS Compilation Commands

```bash
# Compile DTS to DTB
dtc -I dts -O dtb -f <file_name>.dts -o <file_name>.dtb

# Convert DTB to DTS
dtc -I dtb -O dts -f <file_name>.dtb -o <file_name>.dts
```

---

## domain — Domain Management

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `domain create -name <name> -proc <cpu> -os <os>` | `platform.add_domain(cpu=<cpu>, os=<os>, name=<name>)` | |
| `domain active <name>` | `platform.get_domain(name=<name>)` | Returns domain object |
| `domain config -display-name <name>` | `domain.update_name(name=<name>)` | |
| `domain config -sd-dir <path>` | `domain.set_sd_dir(path=<path>)` | Linux domains only |
| `domain config -generate-bif` | `domain.add_bif(path=<file>)` | |
| `domain config -boot <dir>` | `domain.add_boot_dir(boot_dir=<dir>)` | |
| `domain config -qemu-args <file>` | `domain.add_qemu_args(qemu_option="PS"/"PMC"/"PMU", file_name=<file>)` | |
| `domain config -qemu-data <dir>` | `domain.add_qemu_data(data_dir=<dir>)` | |
| `domain list` | `platform.list_domain()` | |
| `domain report <name>` | `domain.report(name=<name>)` | |
| `domain remove <name>` | — | |

### add_domain Arguments

| Parameter | Required | Description |
|-----------|----------|-------------|
| `cpu` | Yes | Processor core (or list for SMP Linux) |
| `os` | No | OS type (default: `standalone`) |
| `name` | No | Domain name |
| `display_name` | No | Display name |
| `support_app` | No | Create BSP settings for specified apps (standalone only) |
| `sd_dir` | No | Pre-built Linux images directory |

### domain config Sub-commands (Python CLI)

| Python API | Required Arguments |
|-----------|-------------------|
| `update_name` | `name=<new_name>` |
| `add_custom_dtb` | `path=<dtb_file>` |
| `set_sd_dir` | `path=<path>` |
| `add_boot_dir` | `boot_dir=<dir>` |
| `add_bif` | `path=<file_path>` |
| `add_qemu_args` | `qemu_option="PS"/"PMC"/"PMU"`, `file_name=<file>` |
| `add_qemu_data` | `data_dir=<dir>` |

---

## getaddrmap / getperipherals / getprocessors

| XSCT Command | Python API | Arguments |
|-------------|-----------|-----------|
| `getaddrmap` | — | Get address ranges of IP connected to a processor |
| `getperipherals` | — | Get list of all peripherals in the hardware design |
| `getprocessors <xsa>` | `client.get_processor_os_list(xsa=<path>)` or `client.get_processor_os_list(platform=<name>)` | XSA path or platform name |

---

## getws / setws — Workspace Management

| XSCT Command | Python API | Arguments |
|-------------|-----------|-----------|
| `getws` | `client.get_workspace()` | — |
| `setws <workspace>` | `client.set_workspace(path=<path>)` | Required: `path` |

---

## lscript — Linker Script

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `lscript memory -app <name> -supported-mem` | `lscript.get_memory_regions()` | In Python CLI, lscript object is created from host component |
| — | `lscript.add_memory_region(name, base_address, size)` | **New in Python CLI** — no XSCT equivalent |
| — | `lscript.update_memory_region(...)` | **New in Python CLI** — no XSCT equivalent |
| `lscript section -app <name> -name <sec> -mem <region>` | `lscript.get_ld_sections()` / `lscript.update_ld_section(section, region)` | |
| `lscript def-mem -app <name> -stack` | `lscript.get_stack_size()` / `lscript.get_heap_size()` | |
| `lscript generate` | `lscript.regenerate()` | |

> **New in Python CLI:** `add_memory_region` and `update_memory_region` commands allow creating and modifying memory regions, which was not possible in XSCT.

---

## platform — Platform Management

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `platform active <name>` | `client.get_platform_component(name=<name>)` | Returns platform object |
| `platform clean` | `platform.clean()` | |
| `platform config -desc <desc>` | `platform.update_desc(desc=<desc>)` | |
| `platform config -updatehw <xsa>` | `platform.update_hw(hw=<xsa>)` | Also accepts `emulation_xsa_path` |
| `platform config -fsbl-target <cpu>` | `platform.retarget_fsbl(target_processor=<cpu>)` | ZU+ only |
| `platform config -create-boot-bsp` | `platform.generate_boot_bsp(target_processor=<cpu>)` | Default target: `zynqmp_fsbl` |
| `platform config -remove-boot-bsp` | `platform.remove_boot_bsp(fsbl_path=<path>, pmufw_elf=<path>)` | |
| `platform list` | `client.list_platforms()` | |
| `platform report` | `platform.report()` | |
| `platform remove <name>` | — | |
| `platform config -samples <dir>` | *Not supported in Python CLI* | |
| `platform config -prebuilt-data <dir>` | *Not supported in Python CLI* | |
| `platform config -make-local` | *Not supported in Python CLI* | |
| `platform read` | *Not supported in Python CLI* | |
| `platform write` | *Not supported in Python CLI* | |

---

## repo — Software Repositories

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `repo -set` (examples) | `client.add_local_example_repo(name, local_directory, type, display_name, description)` | Type: `"SYS_PROJ"` (default), `"HLS"`, `"AIE"` |
| `repo -set` (sw repos) | `client.set_sw_repo(level=<"LOCAL"/"GLOBAL">, path=<path>)` | LOCAL: current workspace; GLOBAL: across workspaces |
| `repo -get` (examples) | `client.list_example_repos(type=<type>)` | Types: `"SYS_PROJ"`, `"HLS"`, `"AIE"`, `"EMBD_APP"` |
| `repo -get` (sw repos) | `client.get_sw_repo(level=<"LOCAL"/"GLOBAL">)` | |
| `repo -scan` (platforms) | `client.rescan_platform_repos(platform=<path>)` | Single path or list of paths |
| `repo -scan` (sw repos) | `client.rescan_sw_repo()` | |
| `repo -os` | `domain.get_os()` | |
| `repo -libs` | `domain.get_libs()` | |
| `repo -drivers` | `domain.get_drivers()` | |
| `repo -app` | `domain.get_applicable_libs()` | |
| `repo -add-platforms <dir>` | `client.add_platform_repos(platform=<path>)` | String or list of paths |
| `repo -remove-platforms-dir <dir>` | `client.delete_platform_repos(platform=<path>)` | |

---

## sysproj — System Project Management

| XSCT Command | Python API | Notes |
|-------------|-----------|-------|
| `sysproj build` | `sys_proj.build(target=<target>)` | Targets: `sw_emu` (default), `hw_emu`, `hw`; optional `comp_name`, `build_comps` (default: True) |
| `sysproj clean` | `sys_proj.clean(target=<target>)` | |
| `sysproj list` | `client.list_sys_projects()` | |
| `sysproj remove` | `client.remove_sys_proj(name=<name>)` | |
| `sysproj report` | `sys_proj.report()` | |

---

## importprojects — Project Import

```python
sys_proj = client.import_projects(
    src=<source_zip_dir>,          # Required: full path to zipped project
    components=<component_names>,   # Optional: names of components to import
    system_projects=<proj_names>,   # Optional: names of system projects to import
    dest=<destination_dir>          # Optional: import path (default: current workspace)
)
```

> Use `client.get_project_info(src)` to list available components and projects from a ZIP file before importing.

---

## importsources — Source Import

```python
status = platform.import_files(
    from_loc=<path>,                # Required: source directory or file (absolute/relative)
    files=["file1", ...],           # Optional: specific files (whole folder if omitted)
    dest_dir_in_cmp=<dest_path>     # Optional: destination folder (created if doesn't exist)
)
```

---

## library — Library Component

```python
lib_comp = client.create_library_component(
    name=<comp_name>,       # Required: library component name
    platform=<platform>,    # Required: platform path (e.g., "/tmp/vck190.xpfm")
    domain=<domain>         # Optional: specify for baremetal domains with multiple domains
)
```

**Example:**

```python
lib_comp = client.create_library_component(
    name="lib_component1",
    platform="/tmp/vck190.xpfm",
    domain="psv_cortexa72_0"
)
```

---

## Key Migration Differences

| Aspect | XSCT | Python CLI |
|--------|------|-----------|
| **System project creation** | Specified during `app create` | Component created first, then added to system project |
| **BSP driver/lib/OS version** | Uses `-ver` argument | Uses `update_path(new_path=<path>)` |
| **Memory region creation** | Not supported | Supported via `lscript.add_memory_region()` |
| **Platform `read`/`write`** | Supported | Not supported |
| **BSP `reload`/`write`** | Supported | Not supported |
| **`app build -all`** | Supported | Not supported; must build individually |
| **`app list -dict`** | Returns Tcl dictionary | Not supported |
| **Repository type** | Implicit | Explicit `type` parameter (`SYS_PROJ`, `HLS`, `AIE`, `EMBD_APP`) |
| **Workspace journal** | Not available | All actions logged to `workspace_journal.py` |

---

*Source: UG1400 (v2025.2) — Vitis Embedded Software Development, November 20, 2025, Section V (pp. 180–199)*
