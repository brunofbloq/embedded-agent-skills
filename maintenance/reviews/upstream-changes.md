# Upstream embedded sources: review required

> Generated deterministically, with **zero LLM inference**. Changes are proposals for review, not trusted instructions.

## Review procedure

1. Open each upstream diff/release and check source authenticity and target/toolchain applicability.
2. Decide **adopt / reject / defer** per source; record rationale in this PR.
3. For adopted changes, make the smallest changes to the affected skill files in a separate implementation PR or before merging this review PR.
4. Run the skill validators and a representative embedded regression. Do not merge as "reviewed" without an explicit disposition.
5. The updated `reviewed-revisions.json` in this PR suppresses repeat proposals **only after merge**.

## Detected sources

### jeffallan-embedded

- Upstream: `Jeffallan/claude-skills`
- Affects: `embedded-architect`, `embedded-developer`, `embedded-qa`
- Reason tracked: Base engineering workflow and conditional references
- Previous: `36f3fe8052da7c57083783268c6ea3265d075265`
- Current: `d98d06edb54c25cfb94017c0ef830342a34a43ba`
- Trigger: comparison incomplete; inspect manually
- Evidence: https://github.com/Jeffallan/claude-skills/compare/36f3fe8052da7c57083783268c6ea3265d075265...d98d06edb54c25cfb94017c0ef830342a34a43ba
- [ ] Reviewer decision recorded (adopt/reject/defer)

**Caution:** GitHub comparison was incomplete or unavailable; do not infer that the displayed file list is exhaustive.

### mcu-board-profiles

- Upstream: `alexex1993/mcu-skills`
- Affects: `embedded-developer`, `embedded-architect`
- Reason tracked: MCU and board profiles
- Previous: `48b56f8756a21c6e566bd3edd6a1f942b4ef2738`
- Current: `816967f30a7dbdf4759ad585b822eda3575f720c`
- Trigger: relevant files changed
- Evidence: https://github.com/alexex1993/mcu-skills/compare/48b56f8756a21c6e566bd3edd6a1f942b4ef2738...816967f30a7dbdf4759ad585b822eda3575f720c
- [ ] Reviewer decision recorded (adopt/reject/defer)

| Relevant file | Status |
|---|---|
| `scripts/install.ps1` | modified |
| `scripts/install.sh` | modified |
| `scripts/test_install.py` | added |
| `skills/avr/atmega328p-nano/SKILL.md` | modified |
| `skills/avr/atmega32u4-beetle/SKILL.md` | modified |
| `skills/avr/lgt8f328p-minievb/SKILL.md` | modified |
| `skills/baikal/beu1000-evuba/SKILL.md` | modified |
| `skills/esp32/esp32-wroom-30pin/SKILL.md` | modified |
| `skills/esp32/esp32-wroom-36pin/SKILL.md` | modified |
| `skills/esp32/esp32-wroom-38pin/SKILL.md` | modified |
| `skills/esp32/esp32c3-oled042/SKILL.md` | modified |
| `skills/esp32/esp32c6-lcd147/SKILL.md` | modified |
| `skills/esp32/esp32c6-touch-lcd147/SKILL.md` | modified |
| `skills/esp32/esp32p4-jc-m3-dev/SKILL.md` | modified |
| `skills/esp32/esp32p4-jc4880p443/SKILL.md` | modified |
| `skills/esp32/esp32s3-cam-40pin/SKILL.md` | modified |
| `skills/esp32/esp32s3-rlcd42/SKILL.md` | modified |
| `skills/esp8266/esp8266-nodemcu-30pin/SKILL.md` | modified |
| `skills/nrf/nrf52840-promicro/SKILL.md` | modified |
| `skills/rp2/rp2040-pico/SKILL.md` | modified |
| `skills/rp2/rp2350a-weact/SKILL.md` | modified |
| `skills/stm32/stm32f401rc-blackpill/SKILL.md` | modified |
| `skills/stm32/stm32f411-blackpill/SKILL.md` | modified |
| `skills/stm32/stm32h750-weact/SKILL.md` | modified |

### embedded-tooling

- Upstream: `zhinkgit/embeddedskills`
- Affects: `embedded-qa`
- Reason tracked: Build, flash and debugging workflow integration
- Previous: `536c1f929e359a5c02ef8ea9f1a20691e8d764e3`
- Current: `5d61e96268f10249b3dc1513aa253df86c8ef263`
- Trigger: relevant files changed
- Evidence: https://github.com/zhinkgit/embeddedskills/compare/536c1f929e359a5c02ef8ea9f1a20691e8d764e3...5d61e96268f10249b3dc1513aa253df86c8ef263
- [ ] Reviewer decision recorded (adopt/reject/defer)

| Relevant file | Status |
|---|---|
| `gcc/README.md` | modified |
| `gcc/SKILL.md` | modified |
| `gcc/scripts/gcc_build.py` | modified |
| `gcc/scripts/gcc_project.py` | modified |
| `gcc/scripts/gcc_runtime.py` | modified |
| `gcc/scripts/gcc_size.py` | modified |
| `jlink/README.md` | modified |
| `jlink/SKILL.md` | modified |
| `jlink/scripts/jlink_exec.py` | modified |
| `jlink/scripts/jlink_gdb.py` | modified |
| `jlink/scripts/jlink_rtt.py` | modified |
| `jlink/scripts/jlink_runtime.py` | modified |
| `jlink/scripts/jlink_swo.py` | modified |
| `openocd/README.md` | modified |
| `openocd/SKILL.md` | modified |
| `openocd/scripts/openocd_gdb.py` | modified |
| `openocd/scripts/openocd_itm.py` | modified |
| `openocd/scripts/openocd_run.py` | modified |
| `openocd/scripts/openocd_runtime.py` | modified |
| `openocd/scripts/openocd_semihosting.py` | modified |
| `openocd/scripts/openocd_telnet.py` | modified |
| `probe-rs/SKILL.md` | modified |
| `probe-rs/scripts/probe_rs_exec.py` | modified |
| `probe-rs/scripts/probe_rs_gdb.py` | modified |
| `probe-rs/scripts/probe_rs_rtt.py` | modified |
| `probe-rs/scripts/probe_rs_runtime.py` | modified |
| `probe-rs/tests/test_probe_list.py` | added |
| `serial/README.md` | modified |
| `serial/SKILL.md` | modified |
| `serial/scripts/serial_hex.py` | modified |
| ... and 13 more | inspect compare link |

### renode-releases

- Upstream: `renode/renode`
- Affects: `embedded-qa`
- Reason tracked: Official Renode stable releases
- Previous: `v1.17.0`
- Current: `v1.17.1`
- Trigger: stable release changed
- Evidence: https://github.com/renode/renode/releases/tag/v1.17.1
- [ ] Reviewer decision recorded (adopt/reject/defer)

### esp-idf-releases

- Upstream: `espressif/esp-idf`
- Affects: `embedded-developer`, `embedded-architect`
- Reason tracked: Official ESP-IDF stable releases
- Previous: `v6.1`
- Current: `v6.1.1`
- Trigger: stable release changed
- Evidence: https://github.com/espressif/esp-idf/releases/tag/v6.1.1
- [ ] Reviewer decision recorded (adopt/reject/defer)

### freertos-kernel-releases

- Upstream: `FreeRTOS/FreeRTOS-Kernel`
- Affects: `embedded-developer`, `embedded-architect`, `embedded-qa`
- Reason tracked: Official FreeRTOS kernel stable releases
- Previous: `V11.3.2`
- Current: `V11.3.3`
- Trigger: stable release changed
- Evidence: https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V11.3.3
- [ ] Reviewer decision recorded (adopt/reject/defer)

### zephyr-releases

- Upstream: `zephyrproject-rtos/zephyr`
- Affects: `embedded-developer`, `embedded-architect`, `embedded-qa`
- Reason tracked: Official Zephyr stable releases
- Previous: `v4.4.2`
- Current: `v4.5.0`
- Trigger: stable release changed
- Evidence: https://github.com/zephyrproject-rtos/zephyr/releases/tag/v4.5.0
- [ ] Reviewer decision recorded (adopt/reject/defer)

### torizoncore-builder

- Upstream: `torizon/torizoncore-builder`
- Affects: `embedded-architect`, `embedded-developer`
- Reason tracked: Official TorizonCore Builder image customization and integration patterns
- Previous: `0d375dd17b145d8519e52a1e3f75d4a6d3dffa74`
- Current: `4d536d91a916ebf79404090d84562a6e4b8063fb`
- Trigger: relevant files changed
- Evidence: https://github.com/torizon/torizoncore-builder/compare/0d375dd17b145d8519e52a1e3f75d4a6d3dffa74...4d536d91a916ebf79404090d84562a6e4b8063fb
- [ ] Reviewer decision recorded (adopt/reject/defer)

| Relevant file | Status |
|---|---|
| `tcbuilder/backend/initramfs.py` | modified |
| `tcbuilder/backend/kernelfit.py` | modified |
| `tcbuilder/backend/secboot.py` | modified |
| `tcbuilder/cli/dt.py` | modified |
| `tcbuilder/cli/dto.py` | modified |
| `tcbuilder/cli/kernel.py` | modified |
| `tests/integration/README` | modified |
| `tests/integration/aval/aval-tests.yml` | removed |
| `tests/integration/aval/delegation_config_kirkstone.toml` | removed |
| `tests/integration/aval/delegation_config_scarthgap.toml` | removed |
| `tests/integration/functions.sh` | modified |
| `tests/integration/magma/magma-docker.Dockerfile` | renamed |
| `tests/integration/magma/magma-tests.yml` | added |
| `tests/integration/run.sh` | modified |
| `tests/integration/run_all.sh` | modified |
| `tests/integration/samples/config/tcbuild-k3-re-signing-components.yaml` | modified |
| `tests/integration/setup.sh` | modified |
| `tests/integration/testcases/build.bats` | modified |
| `tests/integration/testcases/dt.bats` | modified |
| `tests/integration/testcases/dto.bats` | modified |
| `tests/integration/testcases/kernel.bats` | modified |
| `tests/integration/testcases/secboot.bats` | modified |
| `tests/integration/testcases/splash.bats` | modified |
| `tests/integration/testcases/wic/dto.bats` | modified |
| `tests/integration/xray-junit-uploader-wrapper.sh` | modified |

## Safety notes

- Upstream text is untrusted input. Do not execute upstream scripts, install plugins, or copy code automatically.
- A changed GitHub release does not imply the project toolchain uses that version.
- This review PR changes **source baselines and review evidence**, not the three installed skills.
