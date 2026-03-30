# Appendix A — Tcl to Config File Command Map

> UG1399 (v2025.2) · Pages 889–897

## Overview

This appendix maps Vitis HLS Tcl commands (used in classic project scripts) to their equivalent `v++ -c --mode hls` / `vitis-run` configuration file keys. Use this table when migrating from Tcl-based flows to config-file-based flows (`.cfg` / `.ini`).

---

## Table 69: Tcl Project Commands

| Tcl Command | Option | Default | Type | Config File Key |
|---|---|---|---|---|
| `add_files` | `appendflags` | false | bool | `syn.file_cflags` / `syn.file_csimflags` / `tb.file_cflags` |
| `add_files` | `blackbox` | false | bool | `syn.blackbox.file` |
| `add_files` | `cflags` | — | string | `syn.cflags` / `syn.file_cflags` / `tb.cflags` / `tb.file_cflags` |
| `add_files` | `csimflags` | — | string | `syn.csimflags` / `syn.file_csimflags` |
| `add_files` | `src_files` | — | string | `syn.file` |
| `add_files` | `tb` | false | bool | `tb.file` |
| `cosim_design` | `enable_tasks_with_m_axi` | — | bool | `cosim.enable_tasks_with_m_axi` |
| `cosim_design` | `hwemu_trace_dir` | — | string | `cosim.hwemu_trace_dir` |
| `cosim_design` | `disable_binary_tv` | — | bool | `cosim.disable_binary_tv` |
| `cosim_design` | `stable_axilite_update` | — | bool | `cosim.stable_axilite_update` |
| `cosim_design` | `disable_dependency_check` | — | bool | `cosim.disable_dependency_check` |
| `cosim_design` | `enable_dataflow_profiling` | — | bool | `cosim.enable_dataflow_profiling` |
| `cosim_design` | `enable_fifo_sizing` | — | bool | `cosim.enable_fifo_sizing` |
| `cosim_design` | `random_stall` | — | bool | `cosim.random_stall` |
| `cosim_design` | `user_stall` | — | string | `cosim.user_stall` |
| `cosim_design` | `disable_deadlock_detection` | — | bool | `cosim.disable_deadlock_detection` |
| `cosim_design` | `wave_debug` | — | bool | `cosim.wave_debug` |
| `cosim_design` | `argv` | — | string | `cosim.argv` |
| `cosim_design` | `compiled_library_dir` | — | string | `cosim.compiled_library_dir` |
| `cosim_design` | `coverage` | — | bool | `cosim.coverage` |
| `cosim_design` | `ldflags` | — | string | `cosim.ldflags` |
| `cosim_design` | `mflags` | — | string | `cosim.mflags` |
| `cosim_design` | `O` | — | bool | `cosim.O` |
| `cosim_design` | `rtl` | verilog | enum | `cosim.rtl` |
| `cosim_design` | `setup` | — | bool | `cosim.setup` |
| `cosim_design` | `tool` | xsim | enum | `cosim.tool` |
| `cosim_design` | `trace_level` | none | enum | `cosim.trace_level` |
| `cosim_stall` | `generate_burst_default` | — | string | — |
| `cosim_stall` | `check` | — | string | — |
| `cosim_stall` | `generate` | — | string | — |
| `cosim_stall` | `list` | — | bool | — |
| `create_clock` | `name` | — | string | — |
| `create_clock` | `period` | 10ns | string | `clock` |
| `csim_design` | `code_analyzer` | 0 | bool | `csim.code_analyzer` |
| `csim_design` | `argv` | — | string | `csim.argv` |
| `csim_design` | `clean` | — | bool | `csim.clean` |
| `csim_design` | `ldflags` | — | string | `csim.ldflags` |
| `csim_design` | `mflags` | — | string | `csim.mflags` |
| `csim_design` | `O` | — | bool | `csim.O` |
| `csim_design` | `setup` | — | bool | `csim.setup` |
| `csynth_design` | `dump_post_cfg` | 0 | bool | — |
| `csynth_design` | `synthesis_check` | 0 | bool | — |
| `csynth_design` | `dump_cfg` | 0 | bool | — |
| `export_design` | `output` | — | string | `package.output.file` |
| `export_design` | `description` | — | string | `package.ip.description` |
| `export_design` | `display_name` | — | string | `package.ip.display_name` |
| `export_design` | `flow` | none | enum | `vivado.flow` |
| `export_design` | `format` | ip_catalog | enum | `package.output.format` |
| `export_design` | `ipname` | — | string | `package.ip.name` |
| `export_design` | `library` | — | string | `package.ip.library` |
| `export_design` | `rtl` | verilog | enum | `vivado.rtl` |
| `export_design` | `taxonomy` | — | string | `package.ip.taxonomy` |
| `export_design` | `vendor` | — | string | `package.ip.vendor` |
| `export_design` | `version` | — | string | `package.ip.version` |
| `open_project` | `name` | — | string | — |
| `open_project` | `reset` | 0 | bool | — |
| `open_project` | `upgrade` | 0 | bool | — |
| `open_solution` | `flow_target` | — | enum | `flow_target` |
| `open_solution` | `name` | — | string | — |
| `open_solution` | `reset` | 0 | bool | — |
| `set_clock_uncertainty` | `uncertainty` | — | string | `clock_uncertainty` |
| `set_part` | `value` | — | string | `part` |
| `set_part` | `board` | — | string | `board` |
| `set_top` | `name` | — | string | `syn.top` |

---

## Table 70: Tcl Configuration Commands

| Tcl Command | Option | Default | Type | Config File Key |
|---|---|---|---|---|
| `config_array_partition` | `complete_threshold` | 4 | uint | `syn.array_partition.complete_threshold` |
| `config_array_partition` | `throughput_driven` | auto | enum | `syn.array_partition.throughput_driven` |
| `config_array_stencil` | `throughput_driven` | off | enum | `syn.array_stencil.throughput_driven` |
| `config_compile` | `clang_version` | 16 | enum (7\|16) | `syn.compile.clang_version` |
| `config_compile` | `design_size_maximum_warning` | 100000 | int | `syn.compile.design_size_maximum_warning` |
| `config_compile` | `performance_budgeter` | auto | enum | `syn.compile.performance_budgeter` |
| `config_compile` | `pipeline_flush_in_task` | ii1 | enum | `syn.compile.pipeline_flush_in_task` |
| `config_compile` | `ignore_long_run_time` | 0 | bool | `syn.compile.ignore_long_run_time` |
| `config_compile` | `enable_auto_rewind` | 1 | bool | `syn.compile.enable_auto_rewind` |
| `config_compile` | `pipeline_style` | frp | enum | `syn.compile.pipeline_style` |
| `config_compile` | `pragma_strict_mode` | 0 | bool | `syn.compile.pragma_strict_mode` |
| `config_compile` | `name_max_length` | 80 | uint | `syn.compile.name_max_length` |
| `config_compile` | `no_signed_zeros` | 0 | bool | `syn.compile.no_signed_zeros` |
| `config_compile` | `pipeline_loops` | 64 | uint | `syn.compile.pipeline_loops` |
| `config_compile` | `unsafe_math_optimizations` | 0 | bool | `syn.compile.unsafe_math_optimizations` |
| `config_cosim` | `enable_tasks_with_m_axi` | — | bool | `cosim.enable_tasks_with_m_axi` |
| `config_cosim` | `argv` | — | string | `cosim.argv` |
| `config_cosim` | `compiled_library_dir` | — | string | `cosim.compiled_library_dir` |
| `config_cosim` | `coverage` | — | bool | `cosim.coverage` |
| `config_cosim` | `disable_binary_tv` | — | bool | `cosim.disable_binary_tv` |
| `config_cosim` | `disable_deadlock_detection` | — | bool | `cosim.disable_deadlock_detection` |
| `config_cosim` | `disable_dependency_check` | — | bool | `cosim.disable_dependency_check` |
| `config_cosim` | `enable_dataflow_profiling` | — | bool | `cosim.enable_dataflow_profiling` |
| `config_cosim` | `enable_fifo_sizing` | — | bool | `cosim.enable_fifo_sizing` |
| `config_cosim` | `hwemu_trace_dir` | — | string | `cosim.hwemu_trace_dir` |
| `config_cosim` | `ldflags` | — | string | `cosim.ldflags` |
| `config_cosim` | `mflags` | — | string | `cosim.mflags` |
| `config_cosim` | `O` | — | bool | `cosim.O` |
| `config_cosim` | `random_stall` | — | bool | `cosim.random_stall` |
| `config_cosim` | `rtl` | verilog | enum | `cosim.rtl` |
| `config_cosim` | `sanitize_address` | — | — | `csim.sanitize_address` |
| `config_cosim` | `sanitize_undefined` | — | — | `csim.sanitize_undefined` |
| `config_cosim` | `setup` | — | bool | `cosim.setup` |
| `config_cosim` | `stable_axilite_update` | — | bool | `cosim.stable_axilite_update` |
| `config_cosim` | `tool` | xsim | enum | `cosim.tool` |
| `config_cosim` | `trace_level` | none | enum | `cosim.trace_level` |
| `config_cosim` | `user_stall` | — | string | `cosim.user_stall` |
| `config_cosim` | `wave_debug` | — | bool | `cosim.wave_debug` |
| `config_csim` | `code_analyzer` | 0 | bool | `csim.code_analyzer` |
| `config_csim` | `argv` | — | string | `csim.argv` |
| `config_csim` | `clean` | — | bool | `csim.clean` |
| `config_csim` | `ldflags` | — | string | `csim.ldflags` |
| `config_csim` | `mflags` | — | string | `csim.mflags` |
| `config_csim` | `O` | — | bool | `csim.O` |
| `config_csim` | `setup` | — | bool | `csim.setup` |
| `config_dataflow` | `enable_canonicalization` | true | bool | `syn.dataflow.enable_canonicalization` |
| `config_dataflow` | `override_user_fifo_depth` | 0 | uint | `syn.dataflow.override_user_fifo_depth` |
| `config_dataflow` | `disable_fifo_sizing_opt` | 0 | bool | `syn.dataflow.disable_fifo_sizing_opt` |
| `config_dataflow` | `task_level_fifo_depth` | 2 | uint | `syn.dataflow.task_level_fifo_depth` |
| `config_dataflow` | `strict_stable_sync` | 0 | bool | `syn.dataflow.strict_stable_sync` |
| `config_dataflow` | `default_channel` | pingpong | enum | `syn.dataflow.default_channel` |
| `config_dataflow` | `fifo_depth` | 2 | uint | `syn.dataflow.fifo_depth` |
| `config_dataflow` | `scalar_fifo_depth` | 2 | uint | `syn.dataflow.scalar_fifo_depth` |
| `config_dataflow` | `start_fifo_depth` | 2 | uint | `syn.dataflow.start_fifo_depth` |
| `config_dataflow` | `strict_mode` | warning | enum | `syn.dataflow.strict_mode` |
| `config_debug` | `directory` | .debug | string | `syn.debug.directory` |
| `config_debug` | `enable` | 0 | bool | `syn.debug.enable` |
| `config_export` | `xo_type` | rtl | enum | `package.output.xo_type` |
| `config_export` | `cosim_trace_generation` | 0 | bool | `syn.rtl.cosim_trace_generation` |
| `config_export` | `flow` | none | enum | `vivado.flow` |
| `config_export` | `ip_xdc_file` | — | string | `package.ip.xdc_file` |
| `config_export` | `ip_xdc_ooc_file` | — | string | `package.ip.xdc_ooc_file` |
| `config_export` | `vivado_clock` | — | string | `vivado.clock` |
| `config_export` | `vivado_max_timing_paths` | 10 | uint | `vivado.max_timing_paths` |
| `config_export` | `vivado_pblock` | — | string | `vivado.pblock` |
| `config_export` | `output` | — | string | `package.output.file` |
| `config_export` | `description` | — | string | `package.ip.description` |
| `config_export` | `display_name` | — | string | `package.ip.display_name` |
| `config_export` | `format` | ip_catalog | enum | `package.output.format` |
| `config_export` | `ipname` | — | string | `package.ip.name` |
| `config_export` | `library` | — | string | `package.ip.library` |
| `config_export` | `rtl` | verilog | enum | `vivado.rtl` |
| `config_export` | `taxonomy` | — | string | `package.ip.taxonomy` |
| `config_export` | `vendor` | — | string | `package.ip.vendor` |
| `config_export` | `version` | — | string | `package.ip.version` |
| `config_export` | `vivado_impl_strategy` | default | string | `vivado.impl_strategy` |
| `config_export` | `vivado_optimization_level` | 0 | enum | `vivado.optimization_level` |
| `config_export` | `vivado_phys_opt` | none | enum | `vivado.phys_opt` |
| `config_export` | `vivado_report_level` | 2 | enum | `vivado.report_level` |
| `config_export` | `vivado_synth_design_args` | `-directive sdx_optimization_effort_high` | string | `vivado.synth_design_args` |
| `config_export` | `vivado_synth_strategy` | default | string | `vivado.synth_strategy` |
| `config_interface` | `m_axi_cache_impl` | auto | enum | `syn.interface.m_axi_cache_impl` |
| `config_interface` | `m_axi_auto_id_channel` | 0 | bool | `syn.interface.m_axi_auto_id_channel` |
| `config_interface` | `s_axilite_interrupt_mode` | tow | enum | `syn.interface.s_axilite_interrupt_mode` |
| `config_interface` | `s_axilite_mailbox` | none | enum | `syn.interface.s_axilite_mailbox` |
| `config_interface` | `s_axilite_memory_auto_widen` | true | bool | `syn.interface.s_axilite_memory_auto_widen` |
| `config_interface` | `s_axilite_status_regs` | off | enum | `syn.interface.s_axilite_status_regs` |
| `config_interface` | `s_axilite_sw_reset` | 0 | bool | `syn.interface.s_axilite_sw_reset` |
| `config_interface` | `m_axi_buffer_impl` | bram | enum | `syn.interface.m_axi_buffer_impl` |
| `config_interface` | `m_axi_conservative_mode` | 1 | bool | `syn.interface.m_axi_conservative_mode` |
| `config_interface` | `m_axi_flush_mode` | 0 | bool | `syn.interface.m_axi_flush_mode` |
| `config_interface` | `m_axi_alignment_byte_size` | 1 | uint | `syn.interface.m_axi_alignment_byte_size` |
| `config_interface` | `m_axi_alignment_size` | 0 | uint | `syn.interface.m_axi_alignment_size` |
| `config_interface` | `m_axi_auto_max_ports` | 0 | bool | `syn.interface.m_axi_auto_max_ports` |
| `config_interface` | `m_axi_latency` | 0 | uint | `syn.interface.m_axi_latency` |
| `config_interface` | `m_axi_max_bitwidth` | 1024 | uint | `syn.interface.m_axi_max_bitwidth` |
| `config_interface` | `m_axi_max_read_burst_length` | 16 | uint | `syn.interface.m_axi_max_read_burst_length` |
| `config_interface` | `m_axi_max_widen_bitwidth` | 0 | uint | `syn.interface.m_axi_max_widen_bitwidth` |
| `config_interface` | `m_axi_max_write_burst_length` | 16 | uint | `syn.interface.m_axi_max_write_burst_length` |
| `config_interface` | `m_axi_min_bitwidth` | 8 | uint | `syn.interface.m_axi_min_bitwidth` |
| `config_interface` | `m_axi_num_read_outstanding` | 16 | uint | `syn.interface.m_axi_num_read_outstanding` |
| `config_interface` | `m_axi_num_write_outstanding` | 16 | uint | `syn.interface.m_axi_num_write_outstanding` |
| `config_interface` | `default_slave_interface` | s_axilite | enum | `syn.interface.default_slave_interface` |
| `config_interface` | `s_axilite_data64` | 0 | bool | `syn.interface.s_axilite_data64` |
| `config_interface` | `clock_enable` | 0 | bool | `syn.interface.clock_enable` |
| `config_interface` | `m_axi_addr64` | 1 | bool | `syn.interface.m_axi_addr64` |
| `config_interface` | `m_axi_offset` | slave | enum | `syn.interface.m_axi_offset` |
| `config_interface` | `register_io` | off | enum | `syn.interface.register_io` |
| `config_op` | `precision` | standard | enum | `syn.op` |
| `config_op` | `impl` | all | string | `syn.op` |
| `config_op` | `latency` | -1 | int | `syn.op` |
| `config_op` | `op` | — | string | `syn.op` |
| `config_rtl` | `deadlock_detection` | sim | enum | `syn.rtl.deadlock_detection` |
| `config_rtl` | `register_all_io` | 0 | bool | `syn.rtl.register_all_io` |
| `config_rtl` | `register_reset_num` | 0 | int | `syn.rtl.register_reset_num` |
| `config_rtl` | `header` | — | string | `syn.rtl.header` |
| `config_rtl` | `kernel_profile` | 0 | bool | `syn.rtl.kernel_profile` |
| `config_rtl` | `module_auto_prefix` | 1 | bool | `syn.rtl.module_auto_prefix` |
| `config_rtl` | `module_prefix` | — | string | `syn.rtl.module_prefix` |
| `config_rtl` | `mult_keep_attribute` | 0 | bool | `syn.rtl.mult_keep_attribute` |
| `config_rtl` | `reset` | control | enum | `syn.rtl.reset` |
| `config_rtl` | `reset_async` | 0 | bool | `syn.rtl.reset_async` |
| `config_rtl` | `reset_level` | high | enum | `syn.rtl.reset_level` |
| `config_schedule` | `enable_dsp_full_reg` | 1 | bool | `syn.schedule.enable_dsp_full_reg` |
| `config_storage` | `auto_srl_max_bits` | 1024 | uint | `syn.storage` |
| `config_storage` | `auto_srl_max_depth` | 2 | uint | `syn.storage` |
| `config_storage` | `impl` | autosrl | string | `syn.storage` |
| `config_storage` | `type` | — | string | `syn.storage` |
| `config_unroll` | `tripcount_threshold` | 0 | uint | `syn.unroll.tripcount_threshold` |

---

## Table 71: Tcl Optimization Directives

| Tcl Command | Config File Key |
|---|---|
| `set_directive_aggregate` | `syn.directive.aggregate` |
| `set_directive_alias` | `syn.directive.alias` |
| `set_directive_allocation` | `syn.directive.allocation` |
| `set_directive_array_partition` | `syn.directive.array_partition` |
| `set_directive_array_reshape` | `syn.directive.array_reshape` |
| `set_directive_bind_op` | `syn.directive.bind_op` |
| `set_directive_bind_storage` | `syn.directive.bind_storage` |
| `set_directive_cache` | `syn.directive.cache` |
| `set_directive_dataflow` | `syn.directive.dataflow` |
| `set_directive_dependence` | `syn.directive.dependence` |
| `set_directive_disaggregate` | `syn.directive.disaggregate` |
| `set_directive_expression_balance` | `syn.directive.expression_balance` |
| `set_directive_function_instantiate` | `syn.directive.function_instantiate` |
| `set_directive_inline` | `syn.directive.inline` |
| `set_directive_interface` | `syn.directive.interface` |
| `set_directive_latency` | `syn.directive.latency` |
| `set_directive_loop_flatten` | `syn.directive.loop_flatten` |
| `set_directive_loop_merge` | `syn.directive.loop_merge` |
| `set_directive_loop_tripcount` | `syn.directive.loop_tripcount` |
| `set_directive_occurrence` | `syn.directive.occurrence` |
| `set_directive_performance` | `syn.directive.performance` |
| `set_directive_pipeline` | `syn.directive.pipeline` |
| `set_directive_protocol` | `syn.directive.protocol` |
| `set_directive_reset` | `syn.directive.reset` |
| `set_directive_resource` | `syn.directive.resource` |
| `set_directive_shared` | `syn.directive.shared` |
| `set_directive_stable` | `syn.directive.stable` |
| `set_directive_stream` | `syn.directive.stream` |
| `set_directive_top` | `syn.top` |
| `set_directive_unroll` | `syn.directive.unroll` |

---

### See Also

- [Chapter 16 — Config File Commands](../section04_vitis_hls_command_reference/ch16_config_file_commands.md) — Full config-file syntax reference
- [Chapter 18 — HLS Tcl Commands](../section04_vitis_hls_command_reference/ch18_hls_tcl_commands.md) — Original Tcl command syntax
- [Chapter 17 — HLS Pragmas](../section04_vitis_hls_command_reference/ch17_hls_pragmas.md) — Source-level pragma equivalents

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Appendix A, pages 889–897*
