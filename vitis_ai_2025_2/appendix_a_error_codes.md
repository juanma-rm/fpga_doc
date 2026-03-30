# Appendix A — Error Codes

Comprehensive error code reference for all Vitis AI components: Optimizer, Quantizer (TF1.x, TF2.x, PyTorch), WeGO, Compiler (XCOM), Vitis AI Library (VAILIB), VART Runtime, XIR, and Target Factory.

---

## Table of Contents

| Category | Prefix | Count | Description |
|----------|--------|-------|-------------|
| [Optimizer](#optimizer-errors) | `OPTIMIZER_*` | 16 | Model pruning/optimization errors |
| [Quantizer — TensorFlow 1.x](#quantizer--tensorflow-1x) | `QUANTIZER_TF1_*` | 7 | vai_q_tensorflow errors |
| [Quantizer — TensorFlow 2.x](#quantizer--tensorflow-2x) | `QUANTIZER_TF2_*` | 5 | vai_q_tensorflow2 errors |
| [Quantizer — PyTorch](#quantizer--pytorch) | `QUANTIZER_TORCH_*` | 25 | vai_q_pytorch errors |
| [WeGO-Torch](#wego-torch-errors) | `WEGO_TORCH_*` | 7 | WeGO PyTorch compilation/runtime errors |
| [Compiler (XCOM)](#compiler-xcom-errors) | `XCOM_*` | 150+ | XIR compiler: ops, tiling, banks, codegen, DDR, partitioning |
| [Vitis AI Library](#vitis-ai-library-errors) | `VAILIB_*` | 18 | DPU task, CPU runner, graph runner, model config, demo |
| [VART Runtime](#vart-runtime-errors) | `VART_*` | 30+ | Device, XRT, XRM, DPU execution, tensor buffer |
| [XIR](#xir-errors) | `XIR_*` | 35+ | Graph, op, tensor, subgraph, serialization |
| [Target Factory/Explorer](#target-factory-errors) | `TARGET_*` | 12 | Target arch, xclbin, device, fingerprint |

---

## Optimizer Errors

| Error Code | Message |
|-----------|---------|
| `OPTIMIZER_DATA_PARALLEL_NOT_ALLOWED_ERROR` | torch.nn.DataParallel module is not allowed |
| `OPTIMIZER_INVALID_ANA_RESULT_ERROR` | Model analysis result is not valid (usually PyTorch/Python version changes) |
| `OPTIMIZER_INVALID_ARGUMENT_ERROR` | Invalid argument |
| `OPTIMIZER_TORCH_MODULE_ERROR` | The operation is not an instance of torch.nn.Module |
| `OPTIMIZER_NOT_EXCLUDE_NODE_ERROR` | Some nodes must be excluded from pruning |
| `OPTIMIZER_NO_ANA_RESULT_ERROR` | Model analysis results not found |
| `OPTIMIZER_SUBNET_ERROR` | Subnet candidates not found — must do subnet searching first |
| `OPTIMIZER_UNSUPPORTED_OP_ERROR` | The operation is not supported yet |
| `OPTIMIZER_KERAS_MODEL_ERROR` | The given object is not an instance of keras.Model |
| `OPTIMIZER_KERAS_LAYER_ERROR` | The operation is not an instance of keras.Layer |
| `OPTIMIZER_DATA_FORMAT_ERROR` | Data format for saving weights not allowed in pruning |
| `OPTIMIZER_INVALID_GRAPH` | The parsed graph is invalid |
| `OPTIMIZER_IO_ERROR` | IO error (usually disk read/write) |
| `OPTIMIZER_MODEL_ANALYSIS_ERROR` | Error occurred while performing model analysis |
| `OPTIMIZER_PARSE_GRAPH_FAILED` | Unable to parse the model to a computation graph |
| `OPTIMIZER_WEIGHTS_NOT_FOUND` | The weights for the operation cannot be found |

---

## Quantizer — TensorFlow 1.x

| Error Code | Message |
|-----------|---------|
| `QUANTIZER_TF1_INVALID_BITWIDTH` | Invalid parameter |
| `QUANTIZER_TF1_INVALID_METHOD` | Invalid parameter |
| `QUANTIZER_TF1_INVALID_TARGET_DTYPE` | Invalid parameter |
| `QUANTIZER_TF1_MISSING_QUANTIZE_INFO` | Not found |
| `QUANTIZER_TF1_INVALID_INPUT` | Not found |
| `QUANTIZER_TF1_UNSUPPORTED_OP` | Unsupported Op type |
| `QUANTIZER_TF1_LENGTH_MISMATCH` | Invalid parameter |
| `QUANTIZER_TF1_INVALID_INPUT_FN` | Fail to import |

---

## Quantizer — TensorFlow 2.x

| Error Code | Message |
|-----------|---------|
| `QUANTIZER_TF2_UNSUPPORTED_MODEL` | Unsupported model type |
| `QUANTIZER_TF2_UNSUPPORTED_LAYER` | Unsupported layer type |
| `QUANTIZER_TF2_INVALID_CALIB_DATASET` | Invalid calibration dataset |
| `QUANTIZER_TF2_INVALID_INPUT_SHAPE` | Invalid input shape |
| `QUANTIZER_TF2_INVALID_TARGET` | Invalid Target |

---

## Quantizer — PyTorch

| Error Code | Message |
|-----------|---------|
| `QUANTIZER_TORCH_BIAS_CORRECTION` | Bias correction file in quantization result directory does not match current model |
| `QUANTIZER_TORCH_CALIB_RESULT_MISMATCH` | Node name mismatch when loading quantization steps — ensure same vai_q_pytorch and PyTorch versions for test and calibration modes |
| `QUANTIZER_TORCH_EXPORT_ONNX` | Cannot export quantized module to ONNX due to PyTorch internal failure — may need to adjust float model code |
| `QUANTIZER_TORCH_EXPORT_XMODEL` | Fail to convert graph to XMODEL — check message text |
| `QUANTIZER_TORCH_FAST_FINETUNE` | Fast fine-tuned parameter file does not exist — call `load_ft_param` in model code |
| `QUANTIZER_TORCH_FIX_INPUT_TYPE` | Illegal data type or value in quantization OP arguments when exporting ONNX |
| `QUANTIZER_TORCH_ILLEGAL_BITWIDTH` | Illegal tensor quantization configuration — must be integer in given range |
| `QUANTIZER_TORCH_IMPORT_KERNEL` | Error importing vai_q_pytorch library — check PyTorch version matches `pytorch_nndct.__version__` |
| `QUANTIZER_TORCH_NO_CALIB_RESULT` | Quantization result file does not exist — check calibration completion |
| `QUANTIZER_TORCH_NO_CALIBRATION` | Calibration not performed completely — check module FORWARD function is called |
| `QUANTIZER_TORCH_NO_FORWARD` | quant_model FORWARD must be called before exporting quantization result |
| `QUANTIZER_TORCH_OP_REGIST` | OP type cannot be registered multiple times |
| `QUANTIZER_TORCH_PYTORCH_TRACE` | Failed to get PyTorch traced graph — may need to adjust float model code |
| `QUANTIZER_TORCH_QUANT_CONFIG` | Illegal quantization configuration items |
| `QUANTIZER_TORCH_SHAPE_MISMATCH` | Tensor shapes are mismatched |
| `QUANTIZER_TORCH_VERSION` | PyTorch version not supported or does not match vai_q_pytorch version |
| `QUANTIZER_TORCH_XMODEL_BATCHSIZE` | Batch size must be 1 when exporting XMODEL |
| `QUANTIZER_TORCH_INSPECTOR_OUTPUT_FORMAT` | Inspector only supports SVG or PNG format |
| `QUANTIZER_TORCH_INSPECTOR_INPUT_FORMAT` | Inspector no longer supports fingerprint — provide architecture name instead |
| `QUANTIZER_TORCH_UNSUPPORTED_OPS` | Quantization of the op is not supported |
| `QUANTIZER_TORCH_TRACED_NOT_SUPPORT` | Models produced by `torch.jit.script` not supported in vai_q_pytorch |
| `QUANTIZER_TORCH_NO_SCRIPT_MODEL` | vai_q_pytorch does not find any script model |
| `QUANTIZER_TORCH_REUSED_MODULE` | Quantized module called multiple times in forward — use `allow_reused_module=True` |
| `QUANTIZER_TORCH_DATA_PARALLEL_NOT_ALLOWED` | torch.nn.DataParallel object is not allowed |
| `QUANTIZER_TORCH_INPUT_NOT_QUANTIZED` | Input not quantized — use QuantStub/DeQuantStub for quantization scope |
| `QUANTIZER_TORCH_NOT_A_MODULE` | Quantized operation must be instance of torch.nn.Module |
| `QUANTIZER_TORCH_QAT_PROCESS_ERROR` | Must call `trainable_model` before getting deployable model |
| `QUANTIZER_TORCH_QAT_DEPLOYABLE_MODEL_ERROR` | Trained model has BN fused to CONV — ensure `model.fuse_conv_bn()` is not called |
| `QUANTIZER_TORCH_XMODEL_DEVICE` | XMODEL can only be exported in CPU mode — use `deployable_model(src_dir, used_for_xmodel=True)` |

---

## WeGO-Torch Errors

| Error Code | Message |
|-----------|---------|
| `WEGO_TORCH_UNKNOWN_ERROR` | Unknown error |
| `WEGO_TORCH_INTERNAL_ERROR` | Internal error |
| `WEGO_TORCH_INVALID_ARGUMENT` | Invalid argument error |
| `WEGO_TORCH_INVALID_MODEL` | Invalid model error |
| `WEGO_TORCH_OUT_OF_RANGE` | Out of range error |
| `WEGO_TORCH_UNIMPLEMENTED` | Unimplemented error |
| `WEGO_TORCH_RUNTIME_ERROR` | Runtime error |

---

## Compiler (XCOM) Errors

### Operator Parameter Errors

| Error Code | Message |
|-----------|---------|
| `XCOM_OP_CONV_PARAM_ERROR` | Convolution parameter out of range (feature map, kernel, stride, padding, dilation, etc.) |
| `XCOM_OP_IO_TENSOR_TYPE_ERROR` | Error tensor type for IO operator (load/save) |
| `XCOM_OP_MEM_TYPE_ERROR` | Output tensor memory type error |
| `XCOM_OP_PAD_SMF_MISSING` | Failed to generate padding in pool — smf data missing |
| `XCOM_OP_POOL_SIZE_ERROR` | Failed to calculate pooling size |
| `XCOM_OP_SIGMOID_HEIGHT/WIDTH/CHANNEL_NE` | Sigmoid requires same height/width/channel for input and output |
| `XCOM_OP_REORG_HEIGHT/WIDTH/CHANNEL_NE` | Reorg requires scale-multiple relationship between input/output |
| `XCOM_OP_REORG_CHANNEL_OVERFLOW` | Feature channel size overflows reorg channel input |
| `XCOM_OP_TYPE_UNMATCH` | Unknown or inappropriate operator type |
| `XCOM_OP_TYPE_ERROR` | Unrecognized op involved type |
| `XCOM_OP_NONLINEAR_TYPE_ERROR` | Error of operator non-linear type |
| `XCOM_OP_ARGMAX_*` | argmax I/O dimension mismatches, output channel must be 1 |
| `XCOM_OP_CONCAT_IO_CHANNEL_NE` | Concat requires equal input/output channels |
| `XCOM_OP_CORR_ELT_MUL_*` | Correlation eltwise multiply dimension mismatches |
| `XCOM_OP_COST_*` | Cost operator dimension and stride mismatches |
| `XCOM_OP_DOWNSAMPLE_*` | Downsample dimension mismatches |
| `XCOM_OP_CONV_KERNEL/STRIDE/DILATION_*` | Kernel/stride/dilation overflow or all-padding conditions |
| `XCOM_OP_TDPTCONV3D_*` | Transposed depthwise conv3d overflow errors |
| `XCOM_OP_DPTCONV3D_*` | Depthwise conv3d overflow errors |
| `XCOM_OP_THRESHOLD/TILE/UPSAMPLE/ELEW/MUL/MVR_*` | Various operator I/O dimension mismatches |
| `XCOM_OP_TCONV3D_*` | Transposed conv3d kernel/stride/dilation overflow |

### Tiling and Bank Errors

| Error Code | Message |
|-----------|---------|
| `XCOM_TILING_SIZE_ERROR` | Bank group size not enough — input tensor or kernel too large |
| `XCOM_TILING_FAIL` | Tiling error — contact AMD |
| `XCOM_DPUOP_DATA_SIZE_ERROR` | Size not enough/unaligned mapping smf onto banks |
| `XCOM_BANK_UNALIGNED_ADDRESSING` | Bank addressing must be aligned (e.g., stride mod 16 == 0) |
| `XCOM_BANK_CONV_ERROR` | Error banking status for convolution |
| `XCOM_BANK_INVALID_ID` | Invalid bank id — check target_factory |
| `XCOM_ALLOCATE_BANK_FAIL` | Bank allocation error — contact AMD |

### Assembly Code Generation Errors (`XCOM_ACGEN_*`)

| Error Code | Message |
|-----------|---------|
| `XCOM_ACGEN_POOL_KERNEL_OUTRANGE` | Pooling kernel size out of range |
| `XCOM_ACGEN_UNSUPPORT_QUANTIZATION` | Unsupported quantization bit shift |
| `XCOM_ACGEN_NONLINEAR_TYPE_ERROR` | Unrecognized non-linear type |
| `XCOM_ACGEN_BANK_IO_ERROR` | Bank I/O address count exceeds hardware capacity |
| `XCOM_ACGEN_CONV_WEIGHTS_OC_NE` | Conv output channels must equal weights input |
| `XCOM_ACGEN_BANK_OC_WEIGHTS_UNALIGNED` | Weights bank address must align to output channel |
| `XCOM_ACGEN_CONV_FAKE_WEIGHTS/BIAS_BANKID` | Weights/bias bank id must equal base bank id |
| `XCOM_ACGEN_ELEW_IO_*` | Element-wise I/O errors |
| `XCOM_ACGEN_MUL_IO_ERROR` | Mul operator I/O errors |
| `XCOM_ACGEN_INPUT/OUTPUT_MISSING` | Missing bank address for code generation |
| `XCOM_ACGEN_*_NOT_UNIQ` | Operators require unique bank inputs (weights, prelu, bias, param) |
| `XCOM_ACGEN_INVALIDE_STATUS` | Compiler internal error — uninitialized object |
| `XCOM_ACGEN_BANK_JUMP_READ/WRITE_ERROR` | Bank cannot jump read/write |
| `XCOM_ACGEN_CONV_ERROR` | Conv parameter exceeds hardware limitation |
| `XCOM_ACGEN_ERROR` | Instruction generating fail — contact AMD |

### AIE Errors

| Error Code | Message |
|-----------|---------|
| `XCOM_AIE_TARGET_INIT_FAILED` | Failed to init AIE target |
| `XCOM_AIE_SHIMTILE_OVERFLOW` | AIE shim index/size out of range |
| `XCOM_AIE_MEMTILE_OVERFLOW` | AIE memory index/size out of range |
| `XCOM_AIE_AIETILE_OVERFLOW` | AIE tiling index/bd index out of range |
| `XCOM_AIE_OUT_OF_BD` | Cannot find free bd for mem tiling |
| `XCOM_AIE_CORE_NUM_MISMATCH` | AIE core number config mismatch |
| `XCOM_AIE_TIMING_CONFIG_MISMATCH` | AIE timing configuration mismatch |
| `XCOM_AIE_TILING_FAIL` | Not enough bank space in AIE local memory |
| `XCOM_AIE_UNSUPPORTED_OP` | Unsupported op for AIE tiling |

### DDR Allocation Errors (`XCOM_DDRALLOC_*`)

| Error Code | Message |
|-----------|---------|
| `XCOM_DDR_ADDR_ASSIGNMENT_FAILED` | DDR address assignment failed |
| `XCOM_DDR_OPTIMIZATION_0/1_FAILED` | DDR optimization failed — contact AMD |
| `XCOM_DDRALLOC_OUT_OF_MEM` | DDR space not enough for current model |
| `XCOM_DDRALLOC_MEM_ACCESS_OVERFLOW` | Memory access overflow |
| `XCOM_DDRALLOC_NULL_POINTER` | Accessing uninitialized object |
| `XCOM_DDRALLOC_UNEXPECTED_STATE` | Impossible state — logical error |
| `XCOM_DDRALLOC_*` (various) | Size mismatch, unsupported ops, tensor dimension errors |

### Frontend/Pass/Optimization Errors

| Error Code | Message |
|-----------|---------|
| `XCOM_FRONTEND_OP_UNSUPPORTED` | Operator not implemented by target DPU |
| `XCOM_FRONTEND_OP_UNSUPPORTED_NONLIEAR` | Activation unsupported by target DPU |
| `XCOM_FRONTEND_QUANT_ATTR_MISSING` | Quantization info missing for op |
| `XCOM_FRONTEND_QUANT_ATTR_OUT_OF_RANGE` | Shiftbit out of range for target DPU |
| `XCOM_FRONTEND_TENSOR_*_MISMATCH` | Shape/size/dims/datatype mismatches |
| `XCOM_PASS_DEPENDENCY_ERROR` | Pass dependency issue |
| `XCOM_PASS_OP_INVALID_ATTR` | Invalid operator parameter — check input network |
| `XCOM_OPTIMIZE_*` | Graph optimization errors |

### General Compiler Errors

| Error Code | Message |
|-----------|---------|
| `XCOM_INVALID_GRAPH` | Null or error subgraph type |
| `XCOM_INVALID_TARGET` | Invalid DPU target |
| `XCOM_GRAPH_REQUIRED` | Compiler requires an input graph |
| `XCOM_TARGET_REQUIRED` | Compiler requires a target |
| `XCOM_OPERATOR_UNSUPPORT` | Operator not supported |
| `XCOM_UNIMPLEMENT` | Function unimplemented |
| `XCOM_CODE_GEN_ERROR` | Code generation fail |
| `XCOM_FILE_NOT_EXISTS` | File not found |
| `XCOM_USER_INVALID_CMD_PARAM` | Invalid command-line parameter |
| `XCOM_USER_INVALID_TARGET` | Invalid DPU target from command line |
| `XCOM_USER_INVALID_OUTPUT_OPS` | Specified output ops not found in network |

---

## Vitis AI Library Errors

| Error Code | Message |
|-----------|---------|
| `VAILIB_DPU_TASK_NOT_FIND` | Model files not found |
| `VAILIB_DPU_TASK_OPEN_ERROR` | Open file failed |
| `VAILIB_DPU_TASK_CONFIG_PARSE_ERROR` | Parse model config file failed |
| `VAILIB_DPU_TASK_TENSORS_EMPTY` | Runner has no input tensors |
| `VAILIB_DPU_TASK_SUBGRAPHS_EMPTY` | Runner has no subgraphs |
| `VAILIB_CPU_RUNNER_OPEN_LIB_ERROR` | dlopen cannot open lib |
| `VAILIB_CPU_RUNNER_LOAD_LIB_SYM_ERROR` | dlsym load symbol error |
| `VAILIB_CPU_RUNNER_TENSOR_BUFFER_NOT_FIND` | Cannot find tensor buffer with this name |
| `VAILIB_CPU_RUNNER_TENSOR_BUFFER_NOT_CONTIGUOUS` | Tensor buffer not continuous |
| `VAILIB_CPU_RUNNER_READ/WRITE_FILE_ERROR` | File read/write failure |
| `VAILIB_CPU_RUNNER_CPU_OP_NOT_FIND` | Cannot find op with this name |
| `VAILIB_GRAPH_RUNNER_NOT_FIND` | GraphTask cannot find tensor or tensor buffer |
| `VAILIB_GRAPH_RUNNER_DPU_BATCH_ERROR` | DPU batch not equal |
| `VAILIB_GRAPH_RUNNER_NOT_SUPPORT` | Function/value not supported in graph runner |
| `VAILIB_MATH_NOT_SUPPORT` | Function/value not supported in vai-math |
| `VAILIB_MATH_FIX_POS_ERROR` | Softmax table does not support the fix position value |
| `VAILIB_MODEL_CONFIG_*` | Model config not found, open error, or parse error |
| `VAILIB_BENCHMARK_LIST_EMPTY` | Cannot find images — list empty |
| `VAILIB_DEMO_*` | Canvas too small, gstreamer error, image load error, out of boundary, video open error |

---

## VART Runtime Errors

| Error Code | Message |
|-----------|---------|
| `VART_OPEN_DEVICE_FAIL` | Cannot open device |
| `VART_LOAD_XCLBIN_FAIL` | Bitstream download failed |
| `VART_LOCK_DEVICE_FAIL` | Cannot lock device |
| `VART_FUNC_NOT_SUPPORT` | Function not supported |
| `VART_XMODEL_ERROR` | XMODEL error |
| `VART_GRAPH_ERROR` | Graph error |
| `VART_TENSOR_INFO_ERROR` | Tensor info error |
| `VART_DPU_INFO_ERROR` | DPU info error |
| `VART_SYSTEM_ERROR` | File system error |
| `VART_DEVICE_BUSY` | Device busy |
| `VART_DEVICE_MISMATCH` | Device mismatch |
| `VART_DPU_ALLOC_ERROR` | DPU allocate error |
| `VART_VERSION_MISMATCH` | Version mismatch |
| `VART_OUT_OF_RANGE` | Array index out of range |
| `VART_SIZE_MISMATCH` | Array size mismatch |
| `VART_NULL_PTR` | Nullptr |
| `VART_XRT_*` | XRT errors: nullptr, device busy, read errors, function fault, no devices/CU available, context errors |
| `VART_XRM_*` | XRM errors: context creation, connection, CU acquisition |
| `VART_DEVICE_BUFFER_ALLOC_ERROR` | Cannot alloc device buffer — unknown datatype |
| `VART_XCLBIN_READ/DOWNLOAD_ERROR` | Failed to open or download xclbin |
| `VART_CONTROLLER_VIR_MEMORY_ALLOC_ERROR` | Not enough virtual space on host |
| `VART_VERSION_MISMATCH_ERROR` | Subgraph version mismatch with xclbin |
| `VART_DEVICE_MEMORY_ALLOC_ERROR` | Device memory not enough |
| `VART_TENSOR_BUFFER_CREATE/INVALID/CHECK/DIMS_ERROR` | Tensor buffer issues |
| `VART_DPU_EXEC_ERROR` | DPU run fail |
| `VART_DPU_TIMEOUT_ERROR` | DPU timeout |
| `VART_XCLBIN_PATH_INVALID` | xclbinPath not set — consider setting `XLNX_VART_FIRMWARE` |
| `VART_GRAPH_FINGERPRINT_ERROR` | No hardware info in subgraph |

---

## XIR Errors

| Error Code | Message |
|-----------|---------|
| `XIR_ACCESS_ADDRESS_OVERFLOW` | Address does not exist |
| `XIR_ADD_OP_FAIL` | Failed to add an op |
| `XIR_FILE_NOT_EXIST` | File doesn't exist |
| `XIR_INTERNAL_ERROR` | Internal bug (should never happen) |
| `XIR_INVALID_ARG/ATTR_OCCUR` | Invalid argument/attribute occurrence |
| `XIR_INVALID_ATTR_DEF` | Invalid attribute definition |
| `XIR_INVALID_DATA_TYPE` | Invalid data type |
| `XIR_MEANINGLESS_VALUE` | Meaningless parameter value |
| `XIR_MULTI_DEFINED_OP/TENSOR` | Multiple definition of OP/Tensor |
| `XIR_MULTI_REGISTERED_ARG/ATTR/OP` | Multiple registration of argument/attribute/operator |
| `XIR_OPERATION_FAILED` | Failed to execute command |
| `XIR_OP_NAME_CONFLICT` | Two ops have the same name |
| `XIR_OUT_OF_RANGE` | Index out of range |
| `XIR_PROTECTED_MEMORY` | Cannot modify protected tensor memory |
| `XIR_READ/WRITE_PB_FAILURE` | Failed to read/write pb file |
| `XIR_SHAPE_UNMATCH` | Shape mismatch |
| `XIR_SUBGRAPH_*` | Root already created, cycle detected, invalid merge request |
| `XIR_UNDEFINED_ATTR/INPUT_ARG/OP` | Undefined attribute/input/op |
| `XIR_UNREGISTERED_ARG/ATTR/OP` | Unregistered argument/attribute/operator |
| `XIR_UNSUPPORTED_ROUND_MODE/TYPE` | Unsupported round mode or data type |
| `XIR_VALUE_UNMATCH` | Value mismatch |

---

## Target Factory Errors

| Error Code | Message |
|-----------|---------|
| `TARGET_EXPLORER_XCLBIN_ERROR` | No xclbin specified |
| `TARGET_EXPLORER_XCLBIN_ENV_ERROR` | DPU xclbin path from `XLNX_VART_FIRMWARE` doesn't exist |
| `TARGET_EXPLORER_XCLBIN_ENV_VAL_ERROR` | `XLNX_VART_FIRMWARE` must be `/path/to/xxx.xclbin` |
| `TARGET_EXPLORER_SYS_DEVICE_CHECK_ERROR` | System has no device |
| `TARGET_EXPLORER_XCLBIN_SET_ERROR` | xclbinPath not set — consider setting `XLNX_VART_FIRMWARE` |
| `TARGET_EXPLORER_NO_DPU_ERROR` | xclbin is not for DPU — can't find DPU kernel |
| `TARGET_EXPLORER_BATCH_ERROR` | Only supports multiple DPU cores with same batch and fingerprint |
| `TARGET_EXPLORER_DEVICE_CHECK_ERROR` | No device available for current xclbin |
| `TARGET_FACTORY_INVALID_ARCH` | Invalid target arch |
| `TARGET_FACTORY_INVALID_FEATURE_CODE` | Invalid target feature code |
| `TARGET_FACTORY_INVALID_ISA_VERSION` | Invalid target ISA version |
| `TARGET_FACTORY_INVALID_TYPE` | Invalid target type |
| `TARGET_FACTORY_MULTI_REGISTERED_TARGET` | Multiple registration of target |
| `TARGET_FACTORY_PARSE_TARGET_FAIL` | Fail to parse target from prototxt |
| `TARGET_FACTORY_UNREGISTERED_TARGET` | Unregistered target |

---

## See Also

- [Chapter 2 — Optimizing the Model](chapter02_optimizing_the_model.md) — Optimizer errors
- [Chapter 3 — Quantizing the Model](chapter03_quantizing_the_model.md) — Quantizer errors
- [Chapter 4 — Compiling the Model](chapter04_compiling_the_model.md) — Compiler (XCOM) errors
- [Chapter 5 — Deploying and Running the Model](chapter05_deploying_and_running_the_model.md) — VART, VAILIB, WeGO errors

---

## Source Attribution

- **Document:** UG1414 (v3.5) — Vitis AI User Guide
- **Date:** September 28, 2023
- **Appendix:** Appendix A — Error Codes (pp. 226–243)
