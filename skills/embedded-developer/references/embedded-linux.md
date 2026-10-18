# Embedded Linux low-level implementation

- Inspect the exact kernel tree, defconfig, device-tree nodes, drivers, BSP layers and build workflow. Reuse existing kernel subsystems/APIs; match code style, locking, ownership and cleanup semantics.
- Validate relevant kernel version documentation for probe/remove, `devm_*`, DMA mapping, IRQ affinity/threading, runtime PM, workqueues and userspace ABI. Choose an API based on lifetime and context, not a blanket code template.
- Treat kernel and userspace IPC as bounded, versioned contracts with validation and failure behavior. Do not invent sysfs/debugfs ABIs or expose secrets in debug endpoints.
- Build the actual kernel/module and DT if possible, run warnings/static checks and exercise the target driver on available hardware. Host-only build is not kernel/device qualification.
- For new kernel/SoC decomposition decisions invoke `embedded-architect`; for test design/instrumentation invoke `embedded-qa`.
