# Appendix B: Determining IP Version and Change History

This appendix explains why IP becomes locked and provides recommendations for resolving each lock condition.

---

## Table of Contents

| Section | Description |
|---------|-------------|
| [Why IP Becomes Locked](#why-ip-becomes-locked) | Overview of the IP locking mechanism |
| [IP Locked Reasons and Recommendations](#ip-locked-reasons-and-recommendations) | Complete table of lock reasons with resolutions |

---

## Why IP Becomes Locked

AMD Vivado IP cores become **locked** for several reasons. The Vivado IDE provides an **IP Status Report** (`report_ip_status`) that identifies the reason and provides a recommendation.

> ⚠️ **Important:** When working with AMD-delivered patches, IP may become locked due to changes in IP definitions from the patch.

---

## IP Locked Reasons and Recommendations

### Version and Definition Issues

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **IP definition not found** | IP definition for `<ip_name>` was not found in the IP catalog | Add IP definition to catalog. Consult the IP catalog for replacement IP. |
| **IP major version change** | Newer major version available in catalog | `upgrade_ip` — Review impact on design before upgrading. Major version changes may have port/parameter changes. |
| **IP minor version change** | Newer minor version available in catalog | `upgrade_ip` — Review the change log before upgrading. |
| **IP revision change** | Different revision in catalog | `upgrade_ip` — Review the change log before upgrading. |
| **Incompatible IP data** | Repository data not compatible with current instance (typically IP under development) | `upgrade_ip` — Cannot view customization or generate outputs until updated. |

### Part and Board Issues

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **IP unsupported part** | IP does not support current project part `<CURRENT_PART>` | Select a supported project part before upgrading. |
| **IP board change** | Project board and IP customization board do not match (board-specific outputs affected) | Change project part or re-target IP using upgrade flow. Review ports — some IP have port differences based on part (e.g., debug port names change between 7 series and UltraScale). |
| **IP part change** | Current project part and customization part do not match | Change project part or re-target using upgrade flow. |

### File and Permission Issues

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **IP file read-only** | XCI or XML file is read-only / write-protected | Review project and file system permissions. See Editing IP Sources. |
| **Shared output directory** | IP shares a common output directory with other IP | Remove IP with `remove_files`, re-import with `import_files` to a unique directory. |

### License Issues

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **IP license not found** | Mandatory licenses required but not found | Obtain a valid license or review licensing environment. License checkpoints may prevent use in some tool flows. |
| **Incompatible license** | IP requires mandatory licenses but none found | Obtain valid license before upgrading. |

### Subcores and User-Managed IP

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **IP contains locked subcore** | One or more subcores are locked | Upgrade the parent IP. |
| **Locked due to child IP** | Contains locked subcores | Run upgrade on IP or repackage component using newer child IP version. |
| **User-managed IP** | IP configured as user-managed (`IS_MANAGED = false`) | Reconfigure to system-managed if unexpected (see `IS_MANAGED` property). |
| **USER_LOCKED property** | IP locked by user | Remove the `USER_LOCKED` property on the IP. |

### Other Reasons

| Brief Reason | Description | Recommendation |
|-------------|-------------|----------------|
| **Disabled component** | IP component disabled for current part | Select a supported project part before upgrading. |
| **Incompatible XCI/BOM** | Catalog data incompatible with current instance (same version/revision) | `upgrade_ip` — Update IP before viewing customization. |
| **Deprecated flow** | IP supports Vivado generation but was generated using CORE Generator tool | `upgrade_ip` |

> **Note (Port Changes):** When IP is locked due to part or board change and is upgraded, review the ports carefully. Some IP have port differences based on the part selected. Make RTL changes to avoid synthesis/implementation errors.

---

## Best Practices

1. **Run `report_ip_status`** regularly to identify locked IP early
2. **Review change logs** before performing minor or major version upgrades
3. **Avoid `upgrade_ip [get_ips -all]`** — explicitly name IP to prevent issues with sub-cores
4. **Check port changes** after upgrading IP that was re-targeted to a different part family
5. **Use file-level permissions carefully** — read-only XCI files cause IP to lock

---

## See Also

- [Chapter 2: IP Basics — Upgrading IP](chapter02_ip_basics.md#upgrading-ip)
- [Appendix D: Using IP Across Software Versions](appendix_d_using_ip_across_software_versions.md)

---

## Source Attribution

- **Document:** Vivado Design Suite User Guide: Designing with IP (UG896)
- **Version:** v2025.2, December 17, 2025
- **Appendix:** B — Determining IP Version and Change History (Appendix A in source: Determining Why IP is Locked)
- **Pages:** 91–95
