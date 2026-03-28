# Chapter 19 — AXI4-Lite Slave C Driver Reference

> UG1399 (v2025.2) · Section V: Vitis HLS C Driver Reference · Pages 713–727

## Table of Contents

- [Overview](#overview)
- [Initialization / Release](#initialization--release)
  - [X\<DUT\>_Initialize](#xdut_initialize)
  - [X\<DUT\>_CfgInitialize](#xdut_cfginitialize)
  - [X\<DUT\>_LookupConfig](#xdut_lookupconfig)
  - [X\<DUT\>_Release](#xdut_release)
- [Control Functions](#control-functions)
  - [X\<DUT\>_Start](#xdut_start)
  - [X\<DUT\>_IsDone](#xdut_isdone)
  - [X\<DUT\>_IsIdle](#xdut_isidle)
  - [X\<DUT\>_IsReady](#xdut_isready)
  - [X\<DUT\>_Continue](#xdut_continue)
  - [X\<DUT\>_EnableAutoRestart](#xdut_enableautorestart)
  - [X\<DUT\>_DisableAutoRestart](#xdut_disableautorestart)
- [Scalar Argument I/O](#scalar-argument-io)
  - [X\<DUT\>_Set_ARG](#xdut_set_arg)
  - [X\<DUT\>_Set_ARG_vld](#xdut_set_arg_vld)
  - [X\<DUT\>_Set_ARG_ack](#xdut_set_arg_ack)
  - [X\<DUT\>_Get_ARG](#xdut_get_arg)
  - [X\<DUT\>_Get_ARG_vld](#xdut_get_arg_vld)
  - [X\<DUT\>_Get_ARG_ack](#xdut_get_arg_ack)
- [Array Argument I/O (AXI4-Lite Grouped Arrays)](#array-argument-io-axi4-lite-grouped-arrays)
  - [X\<DUT\>_Get_ARG_BaseAddress](#xdut_get_arg_baseaddress)
  - [X\<DUT\>_Get_ARG_HighAddress](#xdut_get_arg_highaddress)
  - [X\<DUT\>_Get_ARG_TotalBytes](#xdut_get_arg_totalbytes)
  - [X\<DUT\>_Get_ARG_BitWidth](#xdut_get_arg_bitwidth)
  - [X\<DUT\>_Get_ARG_Depth](#xdut_get_arg_depth)
  - [X\<DUT\>_Write_ARG_Words](#xdut_write_arg_words)
  - [X\<DUT\>_Read_ARG_Words](#xdut_read_arg_words)
  - [X\<DUT\>_Write_ARG_Bytes](#xdut_write_arg_bytes)
  - [X\<DUT\>_Read_ARG_Bytes](#xdut_read_arg_bytes)
- [Interrupt Functions](#interrupt-functions)
  - [X\<DUT\>_InterruptGlobalEnable / Disable](#xdut_interruptglobalenable--disable)
  - [X\<DUT\>_InterruptEnable / Disable](#xdut_interruptenable--disable)
  - [X\<DUT\>_InterruptClear](#xdut_interruptclear)
  - [X\<DUT\>_InterruptGetEnabled](#xdut_interruptgetenabled)
  - [X\<DUT\>_InterruptGetStatus](#xdut_interruptgetstatus)
- [API Quick Reference Table](#api-quick-reference-table)

---

## Overview

When Vitis HLS synthesizes a function with an AXI4-Lite slave interface (`s_axilite`), it automatically generates a C software driver. The driver exposes a consistent API where `<DUT>` is replaced by the name of the top-level function.

The driver supports three target environments:

| Environment | Identification argument | Notes |
|---|---|---|
| Standalone (baremetal) — SDT flow | `uintptr BaseAddress` | Preferred in new designs; `DeviceId` deprecated |
| Standalone (baremetal) — classic | `u16 DeviceId` | Legacy; `DeviceId` populated from `xparameters.h` |
| Linux (UIO) | `const char* InstanceName` | Up to 5 memory-mapped UIO regions |

---

## Initialization / Release

### X\<DUT\>_Initialize

```c
int X<DUT>_Initialize(X<DUT> *InstancePtr, uintptr BaseAddress);
int X<DUT>_Initialize(X<DUT> *InstancePtr, u16 DeviceId);
int X<DUT>_Initialize(X<DUT> *InstancePtr, const char* InstanceName);
```

**Description:**
- `BaseAddress` overload: standalone, no MMU. Writes `InstancePtr` from the given base address. Preferred in SDT flow.
- `DeviceId` overload: standalone classic, no MMU. Looks up config from `xparameters.h`.
- `InstanceName` overload: Linux UIO. Creates up to 5 `mmap` regions from sysfs UIO info.

> **Note (DeviceId deprecation):** The DeviceId is no longer populated in the driver config struct or `xparameters.h` in the SDT flow. Use `#ifdef SDT` guards when maintaining cross-compatible code:
> ```c
> #ifndef SDT
> #define GPIO_EXAMPLE_DEVICE_ID  XPAR_GPIO_0_DEVICE_ID
> #else
> #define XGPIO_AXI_BASEADDRESS   XPAR_XGPIO_0_BASEADDR
> #endif
> ```

**Parameters:**

| Parameter | Description |
|---|---|
| `InstancePtr` | Pointer to the device instance struct |
| `DeviceId` | Device ID from `xparameters.h` (classic flow only) |
| `BaseAddress` | Base address from `xparameters.h` (SDT flow) |
| `InstanceName` | UIO device name (Linux only) |

**Return:** `XST_SUCCESS` on success, otherwise failure code.

---

### X\<DUT\>_CfgInitialize

```c
int X<DUT>_CfgInitialize(X<DUT> *InstancePtr, X<DUT>_Config *ConfigPtr);
```

**Description:** Initializes the device when an MMU is active. The effective address of the AXI4-Lite slave may differ from the address in `xparameters.h`, so the config pointer carries the remapped address.

**Parameters:**

| Parameter | Description |
|---|---|
| `InstancePtr` | Pointer to the device instance |
| `ConfigPtr` | Pointer to a `X<DUT>_Config` struct (obtained from `X<DUT>_LookupConfig`) |

**Return:** `XST_SUCCESS` on success.

---

### X\<DUT\>_LookupConfig

```c
X<DUT>_Config* X<DUT>_LookupConfig(uintptr BaseAddress);
X<DUT>_Config* X<DUT>_LookupConfig(u16 DeviceId);
```

**Description:** Returns a pointer to the config struct for the device identified by `BaseAddress` or `DeviceId`. Used together with `X<DUT>_CfgInitialize` when an MMU is present.

**Return:** Pointer to `X<DUT>_Config`, or `NULL` if no match found.

---

### X\<DUT\>_Release

```c
int X<DUT>_Release(X<DUT> *InstancePtr);
```

**Description:** Releases the Linux UIO device by calling `munmap` on all mapped regions. The mapping is also automatically released when the process terminates.

**Return:** `XST_SUCCESS` on success.

---

## Control Functions

These functions control execution flow and map to block-level I/O ports (`ap_start`, `ap_done`, etc.).

### X\<DUT\>_Start

```c
void X<DUT>_Start(X<DUT> *InstancePtr);
```

Asserts `ap_start`, triggering the device to begin execution. Available only if `ap_start` is present.

---

### X\<DUT\>_IsDone

```c
u32 X<DUT>_IsDone(X<DUT> *InstancePtr);
```

Returns the value of `ap_done`. Indicates the device has completed its current execution. Available only if `ap_done` is present.

---

### X\<DUT\>_IsIdle

```c
u32 X<DUT>_IsIdle(X<DUT> *InstancePtr);
```

Returns the value of `ap_idle`. Indicates the device is in the idle state. Available only if `ap_idle` is present.

---

### X\<DUT\>_IsReady

```c
u32 X<DUT>_IsReady(X<DUT> *InstancePtr);
```

Returns the value of `ap_ready`. Indicates the device is ready to accept new input data. Available only if `ap_ready` is present.

---

### X\<DUT\>_Continue

```c
void X<DUT>_Continue(X<DUT> *InstancePtr);
```

Asserts `ap_continue`. Must be used when the block-level protocol is `ap_ctrl_chain` to allow the device to proceed after `ap_done`. Available only if `ap_continue` is present.

---

### X\<DUT\>_EnableAutoRestart

```c
void X<DUT>_EnableAutoRestart(X<DUT> *InstancePtr);
```

**Description:** Enables automatic restart after each execution:
- With `ap_ctrl_hs`: `ap_start` is re-asserted immediately when `ap_done` is asserted.
- With `ap_ctrl_chain`: next transaction starts when `ap_ready` is asserted and `ap_continue` is asserted when `ap_done` fires.

Available only if `ap_start` is present.

---

### X\<DUT\>_DisableAutoRestart

```c
void X<DUT>_DisableAutoRestart(X<DUT> *InstancePtr);
```

Disables the auto-restart function. Available only if `ap_start` is present.

---

## Scalar Argument I/O

These functions read/write scalar function arguments mapped into the AXI4-Lite register space.

### X\<DUT\>_Set_ARG

```c
void X<DUT>_Set_ARG(X<DUT> *InstancePtr, u32 Data);
```

Write a value to scalar input port `ARG`. Available only if `ARG` is an input.

---

### X\<DUT\>_Set_ARG_vld

```c
void X<DUT>_Set_ARG_vld(X<DUT> *InstancePtr);
```

Assert the valid signal for `ARG`. Available only if `ARG` is an input using `ap_hs` or `ap_vld` protocol.

---

### X\<DUT\>_Set_ARG_ack

```c
void X<DUT>_Set_ARG_ack(X<DUT> *InstancePtr);
```

Assert the acknowledge signal for `ARG`. Available only if `ARG` is an output using `ap_hs` or `ap_ack` protocol.

---

### X\<DUT\>_Get_ARG

```c
u32 X<DUT>_Get_ARG(X<DUT> *InstancePtr);
```

Read a value from output port `ARG`. Available only if `ARG` is an output.

**Return:** Value of `ARG`.

---

### X\<DUT\>_Get_ARG_vld

```c
u32 X<DUT>_Get_ARG_vld(X<DUT> *InstancePtr);
```

Read the valid signal for output `ARG`. Available only if `ARG` is an output using `ap_hs` or `ap_vld`.

**Return:** Value of `ARG_vld`.

---

### X\<DUT\>_Get_ARG_ack

```c
u32 X<DUT>_Get_ARG_ack(X<DUT> *InstancePtr);
```

Read the acknowledge signal for input `ARG`. Available only if `ARG` is an input using `ap_hs` or `ap_ack`.

**Return:** Value of `ARG_ack`.

---

## Array Argument I/O (AXI4-Lite Grouped Arrays)

When an array argument is grouped into the AXI4-Lite interface, additional APIs are generated to query the array layout and to perform bulk reads/writes.

> **Packing rules:** Elements narrower than 16 bits are packed into 32-bit words (multiple elements per address). Elements wider than 32 bits span multiple consecutive addresses.

### X\<DUT\>_Get_ARG_BaseAddress

```c
u32 X<DUT>_Get_ARG_BaseAddress(X<DUT> *InstancePtr);
```

**Return:** Base address of the array inside the AXI4-Lite address space.

---

### X\<DUT\>_Get_ARG_HighAddress

```c
u32 X<DUT>_Get_ARG_HighAddress(X<DUT> *InstancePtr);
```

**Return:** Address of the uppermost element of the array.

---

### X\<DUT\>_Get_ARG_TotalBytes

```c
u32 X<DUT>_Get_ARG_TotalBytes(X<DUT> *InstancePtr);
```

**Return:** Total number of bytes consumed by the array in the AXI4-Lite interface.

---

### X\<DUT\>_Get_ARG_BitWidth

```c
u32 X<DUT>_Get_ARG_BitWidth(X<DUT> *InstancePtr);
```

**Return:** Bit width of each individual array element.

---

### X\<DUT\>_Get_ARG_Depth

```c
u32 X<DUT>_Get_ARG_Depth(X<DUT> *InstancePtr);
```

**Return:** Total number of elements in the array.

---

### X\<DUT\>_Write_ARG_Words

```c
u32 X<DUT>_Write_ARG_Words(X<DUT> *InstancePtr, int offset, int *data, int length);
```

Write `length` 32-bit words starting at `offset` within the array's AXI4-Lite region.

| Parameter | Description |
|---|---|
| `offset` | Byte offset from `BaseAddress` |
| `data` | Pointer to source data buffer |
| `length` | Number of 32-bit words to write |

**Return:** Number of words written.

---

### X\<DUT\>_Read_ARG_Words

```c
u32 X<DUT>_Read_ARG_Words(X<DUT> *InstancePtr, int offset, int *data, int length);
```

Read `length` 32-bit words starting at `offset` from the array's AXI4-Lite region into `data`.

**Return:** Number of words read.

---

### X\<DUT\>_Write_ARG_Bytes

```c
u32 X<DUT>_Write_ARG_Bytes(X<DUT> *InstancePtr, int offset, char *data, int length);
```

Write `length` bytes starting at `offset` within the array's AXI4-Lite region.

**Return:** Number of bytes written.

---

### X\<DUT\>_Read_ARG_Bytes

```c
u32 X<DUT>_Read_ARG_Bytes(X<DUT> *InstancePtr, int offset, char *data, int length);
```

Read `length` bytes starting at `offset` from the array's AXI4-Lite region into `data`.

**Return:** Number of bytes read.

---

## Interrupt Functions

Interrupt functions require `ap_start` to be present (i.e., the block-level I/O protocol must not be `ap_ctrl_none`). Up to two interrupt sources exist: source 0 = `ap_done`, source 1 = `ap_ready`.

### X\<DUT\>_InterruptGlobalEnable / Disable

```c
void X<DUT>_InterruptGlobalEnable(X<DUT> *InstancePtr);
void X<DUT>_InterruptGlobalDisable(X<DUT> *InstancePtr);
```

Enable or disable the interrupt output pin globally.

---

### X\<DUT\>_InterruptEnable / Disable

```c
void X<DUT>_InterruptEnable(X<DUT>  *InstancePtr, u32 Mask);
void X<DUT>_InterruptDisable(X<DUT> *InstancePtr, u32 Mask);
```

Enable or disable individual interrupt sources via bitmask.

| Mask bit | Interrupt source |
|---|---|
| Bit 0 | `ap_done` |
| Bit 1 | `ap_ready` |

- Enable: bit n = 1 → enable source n; bit n = 0 → no change.
- Disable: bit n = 1 → disable source n; bit n = 0 → no change.

---

### X\<DUT\>_InterruptClear

```c
void X<DUT>_InterruptClear(X<DUT> *InstancePtr, u32 Mask);
```

Clear (toggle) interrupt status bits. Bit n = 1 → toggle source n; bit n = 0 → no change.

---

### X\<DUT\>_InterruptGetEnabled

```c
u32 X<DUT>_InterruptGetEnabled(X<DUT> *InstancePtr);
```

**Return:** Bitmask of currently enabled interrupt sources (bit n = 1: enabled; bit n = 0: disabled).

---

### X\<DUT\>_InterruptGetStatus

```c
u32 X<DUT>_InterruptGetStatus(X<DUT> *InstancePtr);
```

**Return:** Bitmask of currently triggered interrupt sources (bit n = 1: triggered; bit n = 0: not triggered).

---

## API Quick Reference Table

| Function | Availability | Purpose |
|---|---|---|
| `X<DUT>_Initialize` | Always | Init device (standalone or Linux) |
| `X<DUT>_CfgInitialize` | Always | Init with MMU-remapped address |
| `X<DUT>_LookupConfig` | Always | Retrieve config struct |
| `X<DUT>_Release` | Linux UIO | Unmap UIO device |
| `X<DUT>_Start` | `ap_start` present | Trigger execution |
| `X<DUT>_IsDone` | `ap_done` present | Poll completion |
| `X<DUT>_IsIdle` | `ap_idle` present | Poll idle state |
| `X<DUT>_IsReady` | `ap_ready` present | Poll ready for next input |
| `X<DUT>_Continue` | `ap_continue` present | Assert continue (`ap_ctrl_chain`) |
| `X<DUT>_EnableAutoRestart` | `ap_start` present | Enable auto-restart |
| `X<DUT>_DisableAutoRestart` | `ap_start` present | Disable auto-restart |
| `X<DUT>_Set_ARG` | ARG is input | Write scalar argument |
| `X<DUT>_Set_ARG_vld` | ARG input + `ap_hs`/`ap_vld` | Assert valid |
| `X<DUT>_Set_ARG_ack` | ARG output + `ap_hs`/`ap_ack` | Assert acknowledge |
| `X<DUT>_Get_ARG` | ARG is output | Read scalar argument |
| `X<DUT>_Get_ARG_vld` | ARG output + `ap_hs`/`ap_vld` | Read valid signal |
| `X<DUT>_Get_ARG_ack` | ARG input + `ap_hs`/`ap_ack` | Read acknowledge signal |
| `X<DUT>_Get_ARG_BaseAddress` | ARG is AXI4-Lite array | Array base address |
| `X<DUT>_Get_ARG_HighAddress` | ARG is AXI4-Lite array | Array top address |
| `X<DUT>_Get_ARG_TotalBytes` | ARG is AXI4-Lite array | Total byte size of array |
| `X<DUT>_Get_ARG_BitWidth` | ARG is AXI4-Lite array | Element bit width |
| `X<DUT>_Get_ARG_Depth` | ARG is AXI4-Lite array | Number of elements |
| `X<DUT>_Write_ARG_Words` | ARG is AXI4-Lite array | Bulk write (32-bit words) |
| `X<DUT>_Read_ARG_Words` | ARG is AXI4-Lite array | Bulk read (32-bit words) |
| `X<DUT>_Write_ARG_Bytes` | ARG is AXI4-Lite array | Bulk write (bytes) |
| `X<DUT>_Read_ARG_Bytes` | ARG is AXI4-Lite array | Bulk read (bytes) |
| `X<DUT>_InterruptGlobalEnable` | `ap_start` present | Enable interrupt output |
| `X<DUT>_InterruptGlobalDisable` | `ap_start` present | Disable interrupt output |
| `X<DUT>_InterruptEnable` | `ap_start` present | Enable specific interrupt sources |
| `X<DUT>_InterruptDisable` | `ap_start` present | Disable specific interrupt sources |
| `X<DUT>_InterruptClear` | `ap_start` present | Clear interrupt status |
| `X<DUT>_InterruptGetEnabled` | `ap_start` present | Query enabled sources |
| `X<DUT>_InterruptGetStatus` | `ap_start` present | Query triggered sources |

---

*Source: Vitis HLS User Guide UG1399 v2025.2, Chapter 19, pages 713–727*
