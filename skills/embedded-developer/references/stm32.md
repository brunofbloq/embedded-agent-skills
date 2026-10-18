# STM32 and Cortex-M target checks

Load only for STM32/Cortex-M tasks. Identify exact STM32 part number, core (M0+/M3/M4/M7/M33 etc.), silicon revision, board revision, STM32Cube/HAL/LL/CMSIS versions, and generated-code ownership.

1. **Pins and alternate functions:** Verify pinout, package bonding, AF matrix, supply voltage domains, boot/debug pins, pull/reset levels, and conflicts with peripherals on the *board schematic*. Pin compatibility cannot be inferred from a different STM32 family.
2. **Clocks and timers:** Cross-check oscillator, PLL, prescaler, bus/peripheral mux, startup sequencing and ready flags. Account for applicable APB timer-clock multipliers and system clock transitions. Confirm baudrate/timer formulas against actual config, not an example clock.
3. **Interrupt priority:** Inspect implemented NVIC priority bits (`__NVIC_PRIO_BITS`), grouping, and FreeRTOS `configPRIO_BITS` / max syscall priority macros (if present). Numerically lower Cortex-M priority means higher urgency. Do **not** hardcode `NVIC_PRIORITYGROUP_4` or `configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY` for every part/port; verify how this STM32 HAL, FreeRTOS port, and CMSIS encode priorities.
4. **DMA and memory:** Inspect controller/channel/request/DMAMUX allocation, reachable memory domains, transfer direction, width/alignment, buffer ownership, IRQ order and cache. On D-cache cores (e.g. selected STM32F7/H7), prove coherence with suitable MPU placement or correct aligned maintenance and barriers. Other STM32 lines need not have D-cache.
5. **Startup and linker:** Check vector table, ISR symbol, boot mode, flash/RAM regions, stack/heap symbols, interrupt entry, init order, low-power wake path, fault/reset handling, and (when used) TrustZone/MPU options.
6. **Generated files:** Preserve STM32CubeMX user sections, project metadata and regenerate-safe layering. Do not relocate `Core/`, `Drivers/`, or generated startup files just for a stylistic architecture diagram.

Source priority: exact device datasheet + reference manual + errata (ST), board schematic/BOM, installed CMSIS/device headers, generated clock/linker files, installed STM32Cube middleware. Search [ST product documentation](https://www.st.com/) for the exact ordering code.
