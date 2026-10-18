# Host/CI verification for embedded firmware

- Separate portable business/state logic from hardware interface only when necessary to host-test it; preserve APIs and avoid broad refactors to introduce mocks.
- Select unit tests for critical boundaries, state transitions, timeouts/rollover, invalid length, buffer exhaustion, retry/fault paths and restart/recovery. Test concurrency using explicit scheduling hooks or a stress harness; single-threaded mocks do not prove race freedom.
- Use repository-selected framework (Unity/CMock/Ceedling, CTest, GoogleTest, pytest etc.). Do not add one by default if a simpler existing harness works.
- Run available compiler sanitizers (`address`, `undefined`) on host code, warnings, static analyzers and coverage on meaningful assertions; cross-compiled firmware cannot simply inherit host sanitizer results.
- Parameterize golden vectors independently from implementation. Track requirement -> test -> observed result with the exact revision and toolchain.
