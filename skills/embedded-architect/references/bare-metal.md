# Bare-metal architecture: load for superloop, event-driven and register-level design

- Prefer a main-loop/event loop when work has bounded run-to-completion time and responsiveness is achievable without a scheduler. Explicitly state every periodic/event source, maximum handler work, maximum time between servicing each input and idle/sleep path.
- Ownership: keep interrupt routines short, acknowledge register sources correctly, capture bounded data and expose safe producer/consumer access. `volatile` is insufficient for multiword consistency and ordering; inspect architecture atomics/critical sections.
- Drivers: group application state separately from register-facing code when testing or portability justify it; do not force a universal interface per GPIO.
- Define boot sequence (clock, memory, peripherals), clock source/timeout validity before tick init, brownout/watchdog reset paths, safe output states and startup tests.
- When comparing against RTOS, evaluate ISR load, jitter, worst-case blocking of event loop, schedulability, memory/flash overhead and debugging complexity. Choose RTOS only when its scheduling/service isolation pays for itself.
