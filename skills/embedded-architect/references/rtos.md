# RTOS architecture: tasks, deadlines and data ownership

- Prefer the smallest task count that cleanly separates independently scheduled work; task-per-feature is not automatically optimal. Define deadline, period, WCET evidence, priority, stack units, memory and blocking resources per task.
- Verify scheduler/RTOS version and port, tick rate, ISR-safe API set, interrupt priority ceiling (especially FreeRTOS on Cortex-M), affinity/SMP support and actual stack size units.
- Prefer clear message ownership (notifications, queues, event groups), bounded queue depth and overflow policy; lock shared state with suitable synchronization, not `volatile`.
- Analyze priority inversion, lock order, deadlock, bounded critical sections, watchdog health criteria and boot/recovery sequence.
- Maintain explicit IRQ-to-task handoff when it reduces high-priority work; deterministic short critical control work may remain in a measured IRQ if platform and requirements justify it.
- RTOS and bare-metal are deployment models, not mandated folder layouts. Preserve the project's established build and APIs.
