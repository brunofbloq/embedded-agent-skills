# Embedded Linux architecture: kernel, BSP, service and container boundaries

Adapted from the user's earlier embedded-systems-architect skill, but without its universal architecture gates.

- Verify SoC variant, board revision, boot chain, vendor BSP release, kernel/Yocto/Torizon versions and production deployment method before recommending overlays, containers, out-of-tree modules or changes to boot configuration.
- Choose between userspace service, UIO, kernel subsystem driver or existing interface based on timing, permissions, DMA, interrupt ownership and upstream conventions. Prefer existing kernel subsystem APIs and device model. `devm_*` resource management is appropriate only when lifetime semantics match.
- For device tree, choose DTS integration, overlays or configuration according to BSP and deployment; no blanket overlay requirement.
- For tunables/observability use an appropriate kernel subsystem interface, netlink, ioctl, sysfs, debugfs or userspace service. Do not create arbitrary sysfs ABI or hard-code ephemeral `/dev/*` paths.
- For Yocto layers/recipes use reproducible pinned sources, minimal layer overrides and documented update path. In Torizon, isolate required device access and preserve least privileges; do not assume all services require Docker.
- For connectivity/security establish trust boundaries and explicit authentication/authorization, resource limits, rollback and diagnostics; avoid requiring REST/JWT/OpenAPI for internal message paths unless justified.
- For architecture outputs document boot/deployment path, interface contracts, memory/storage budgets, recovery, versions and update flow. Keep Linux low-level implementation in `embedded-developer` when the task is code rather than system design.
