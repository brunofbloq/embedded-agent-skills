# Concurrency, ISR, DMA, and RTOS checks

Read for scheduler design, ISR changes, shared state, DMA, watchdog, or timing faults. Inspect the installed RTOS port/SDK version and relevant configuration before choosing APIs.

## Shared data

- Establish exactly who owns each buffer, register state, queue, peripheral, and lifetime. Prefer single-owner state with messages; use mutexes/critical sections/atomics for real sharing.
- `volatile` conveys observable access for MMIO and certain ISR-visible flags but **does not guarantee atomicity, mutual exclusion, or cross-core memory ordering**. Confirm compiler, architecture, C/C++ memory model, and RTOS guarantees. For Cortex-M bare-metal interrupt sharing, check whether aligned native-size operations are atomic on the exact core; protect compound read-modify-write sequences.
- For DMA, document CPU/device handoff, alignment, accessible memory regions, cache line sharing, clean/invalidate direction, completion barriers and lifetime. Check silicon-specific cache/MPU rules; never insert cache-maintenance calls blindly.
- Define queue size, throughput assumptions, overflow/drop strategy, producer wake behavior, and recovery from full/empty/late consumers.

## ISR and task behavior

- Bound ISR work and verify status/clear semantics from *that* peripheral generation (some registers are clear-on-read, write-one-to-clear, or require ordered accesses). Avoid stale or repeated IRQs.
- With FreeRTOS, use only ISR-permitted APIs in ISRs; ensure IRQ priority is compatible with the kernel's max-syscall threshold and priority-bit configuration. Use the correct port-specific yield idiom. Never assume one macro works on all targets.
- Do not introduce extra tasks just to achieve a conceptual "one task per responsibility" ideal; quantify stack cost, queue overhead, scheduling latency, and deadline impact. Timers, cooperative loops, callbacks, and dedicated hardware may be better.
- Configure timeouts using a clock that is running during the wait. For wraparound counters, use modular subtraction with a suitably bounded interval; consider stopped SysTick, scheduler not started, tickless sleep, and tick-rate conversion rounding.
- Evaluate priority inversion, callback context, critical-section duration, nested interrupts, and reentrancy. Task stack metrics, stack-overflow hooks, and deadline/jitter instrumentation are evidence, not substitutes for worst-case tests.

## Watchdog and fail-safe

- Identify what progress proves health; a watchdog fed by an idle/timer ISR may mask blocked application tasks. Review startup window, long flash erase, low-power mode, and debugger effects.
- Validate faults: absent device, bus stuck, lost interrupt, queue saturation, unexpected reset, partial NVM write, malformed frame, and watchdog recovery. Prefer bounded retries and explicit degraded/safe state.

Sources to consult as applicable: project FreeRTOS/CMSIS-RTOS/Zephyr source and config, ARM architecture reference, MCU reference manual/errata, SDK RTOS port docs. Never lift a foreign port's ISR snippet or stack unit assumptions into the project.
