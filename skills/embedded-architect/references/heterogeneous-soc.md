# Heterogeneous SoC architecture

- Confirm actual silicon core topology, memory map, boot owner, reset and power domains before assigning work to an M-core or discussing inter-processor messaging. NXP i.MX8 family is not one uniform hardware architecture.
- Enumerate supported IPC from vendor BSP and current firmware: RPMsg/OpenAMP only where available, shared memory plus mailbox, UART/SPI/CAN, or network links. Choose based on bandwidth, latency, fault containment, boot order and recovery requirements.
- Explicitly define buffer ownership, framing/versioning, serialization, cache coherency, notification ordering, replay/timeout policy, loss and restart handling.
- Measure or bound cross-domain deadlines; Linux userspace service response times are not hard-real-time guarantees absent a justified runtime and verified evidence.
- Avoid Linux/kernel/MCU all-at-once scaffolds for small changes. Evolve the current design incrementally.
