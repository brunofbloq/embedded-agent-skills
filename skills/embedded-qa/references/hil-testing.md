# Hardware-in-the-loop verification

- Verify exact board revision, voltage rails, power limits, boot/debug interface and approved probe/firmware before touching hardware. Require explicit permission before flash/erase, programming one-time fuses or exercising dangerous power outputs.
- Choose probe available in actual lab (ST-Link, J-Link, OpenOCD, pyOCD, probe-rs); prefer project scripts and pinned tool versions. On Windows, probe driver substitution can interfere with other debug tools.
- Reserve probes/serial ports to avoid concurrent writes. Record target part, flash image hash, reset reason, voltage, test fixture revision and timebase.
- Validate boot, pinmux, DMA/cache, interrupts, realistic bus faults, timer deadline, watchdog, brownout and interrupted updates as relevant. Always reset to a defined initial state and tear down safely.
- Measure timing with instruments/trace suitable to resolution: SWO/RTT, GPIO toggle + logic analyzer, cycle counter, oscilloscope. Measure power on the electrical rail with known instrument bandwidth/dynamic range; model-based current estimates are not measurements.
- Evidence should contain commands, test conditions, raw logs/traces (or immutable artifact references), tolerances, errors and PASS/FAIL/NOT_RUN. Require separate physical qualification for RF/EMC/thermal/electrical requirements.
