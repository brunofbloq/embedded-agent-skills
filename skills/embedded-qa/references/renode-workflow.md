# Renode execution & Robot Framework workflow

Source priority: the installed Renode version's `--help` and bundled scripts; then https://renode.readthedocs.io/en/latest/introduction/testing.html , https://renode.readthedocs.io/en/latest/introduction/using.html , https://renode.readthedocs.io/en/latest/basic/monitor-syntax.html . Confirm commands against the installed version.

## File ownership

- `.repl`: emulated CPU, memories, peripherals, registers, IRQ topology and board wiring. It is **not** the production device tree or an electrical schematic.
- `.resc`: machine setup / includes, model load, firmware ELF, terminals, virtual device connections, execution controls. Prefer a small script extending a verified existing board rather than copying an unrelated board.
- `.robot`: executable checks, stimulus, assertions and automatic setup/teardown, run with `renode-test`.
- `.elf`: exact target-architecture firmware, built from project commit using its toolchain; record its SHA-256.

Renode monitor `include @path/to/board.resc` configures a script; `start @path/to/board.resc` configures and starts the simulation. Paths in scripts can use `$ORIGIN`; do not prepend `@` when using `$ORIGIN`. Reuse the sample's established `$bin` override when it offers one; check whether the script itself loads ELF or starts the machine. Avoid double-loading/double-starting.

## Minimal verified-style Robot monitor smoke test

```robotframework
*** Settings ***
Suite Setup       Setup
Suite Teardown    Teardown
Test Teardown     Test Teardown
Resource          ${RENODEKEYWORDS}

*** Test Cases ***
Monitor Is Available
    ${result}=    Execute Command    help
    Should Contain    ${result}    Available commands:
```

Run with `renode-test sim/smoke.robot`. `renode-test` manages the Renode process and produces Robot XML + HTML artifacts. This monitor-only test establishes harness health, **not** target firmware correctness.

For a target-specific test, after loading a correct model and ELF, use `Create Terminal Tester  <actual-uart-object>`, `Start Emulation`, `Wait For Line On Uart <expected>`; use `Execute Command` for modeled peripherals and `Should Be Equal...` assertions. Obtain **exact keyword signatures and emulator object names** from the installed Renode tests and loaded `.repl` rather than extrapolating from snippets. Use unique test names and timeouts; beware UART buffering and asynchronous start ordering.

## CI execution

1. Pin Renode version/image, firmware toolchain and model files. Avoid unreviewed external ELF/network downloads.
2. Build actual target ELF; record ELF SHA-256 and git revision.
3. Run targeted `renode-test sim/<suite>.robot` with a job timeout. For parallel independent `renode-test` invocations, configure distinct Robot control ports with `-P` (see installed CLI). Capture process exit code.
4. Parse Robot XML using `python scripts/summarize_robot.py <path/to/output.xml>` and require a real executed test count; `SKIP` means incomplete coverage, not PASS.
5. Archive XML, model/script SHA-256, firmware SHA-256 and selected UART/monitor traces. Store full logs as artifacts, not in an LLM prompt.
6. Separate simulation gate from real hardware testing gate. For model deviations, file a targeted model bug/test and temporarily rely on host/HIL evidence rather than modifying production firmware to hide the mismatch.

Official Renode resources:
- https://renode.readthedocs.io/en/latest/introduction/testing.html
- https://renode.readthedocs.io/en/latest/basic/renode-testing-api.html
- https://renode.readthedocs.io/en/latest/introduction/supported-boards.html
- https://renode.readthedocs.io/en/latest/advanced/writing-peripherals.html
- https://renode.readthedocs.io/en/latest/host-integration/uart.html
