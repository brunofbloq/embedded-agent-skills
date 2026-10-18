# Model-fidelity and verification policy

## Decide whether Renode is appropriate

| Aspect | Required evidence / question |
|---|---|
| CPU / image | Can this exact architecture and firmware ELF execute under a modeled CPU, startup and memory map? |
| Register/IRQ | Does the required device model expose the actual register semantics, IRQ priorities/routing, DMA request behavior, and reset values? |
| Clocks / reset | Are relevant clocks, timers, reset sequences and low-power states modeled enough for the assertion? |
| External devices | Do sensor, CAN/RS485/I2C/SPI, memory and hardware events have deterministic virtual models or injection hooks? |
| Test observability | Can a Robot assertion observe the *outcome* (state, frame, GPIO, error path), not merely an initialization message? |
| Negative tests | Can timeouts, absent device, malformed frame, reset, and bounded recovery be injected and asserted? |

Classify each critical behavior as `SUPPORTED`, `APPROXIMATE`, `MISSING`, or `UNVERIFIED`; only use strong PASS claims for supported behaviors that were exercised by actual assertions. A tool running without errors is not proof of all device semantics.

## What simulated testing can and cannot show

**Useful:** target-code boot smoke, modeled driver state machines, IPC/protocol handling over modeled UART/network, deterministic error paths, RTOS scheduling interactions if modeled, regression under scripted stimuli.

**Not HIL evidence:** actual GPIO voltage/current, bus signal integrity, watchdog oscillator tolerance, analog sensor fidelity, physical RF/BLE/Wi-Fi behavior, electrical power modes/current, signal timing/jitter guarantees, cache/memory interference not modeled, manufacturing revision differences, real DMA/peripheral errata, USB line behavior, EMC/safety.

If the product depends on missing peripheral fidelity, prefer host-side tests for business logic, QEMU/Zephyr native simulation where compatible, or actual board HIL with probes. Do not force Renode to replace the right test tool.

For a future MCP adapter: GitHub renode/renode issue #975 was open during the October 2026 review; verify merged release and available tool schemas before enabling it. Keep local monitor connections restricted to the loopback interface and treat monitor commands as privileged execution capabilities.

Renode evidence source: https://renode.readthedocs.io/en/latest/introduction/testing.html ; https://renode.readthedocs.io/en/latest/advanced/writing-peripherals.html
