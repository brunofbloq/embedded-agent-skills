# Embedded Agent Skills

[![Version](https://img.shields.io/badge/version-v0.1.0-216E39)](https://github.com/brunofbloq/embedded-agent-skills/releases/tag/v0.1.0)
[![Skills](https://img.shields.io/badge/skills-3-0B7285)](skills/)
[![Format](https://img.shields.io/badge/format-Agent%20Skills-6750A4)](https://agentskills.io/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions%20configured-0969DA)](.github/workflows/validate-skills.yml)
[![Upstream](https://img.shields.io/badge/upstream-16%20sources%20monitored-216E39)](maintenance/sources.json)



<p align="center">
  <img
    src="assets/logo-embedded-skills.gif"
    alt="Embedded Agent Skills — MCU and circuit animation"
    width="800"
  />
</p>
  


**Portable, lean, engineering-focused agent skills for embedded development.** Architecture decision-making, implementation and independent verification are separate capabilities. Supports bare-metal MCU, RTOS, embedded Linux and heterogeneous systems, with on-demand references rather than unnecessary baseline prompt tokens.


## Skills

| Skill | What it does | Best time to invoke |
| --- | --- | --- |
| [`embedded-architect`](skills/embedded-architect/) | Architectural decisions for MCU, RTOS, Linux and heterogeneous systems; formal two-phase review and approval checkpoints | New products/subsystems, system partitioning, interfaces, architectural trade-offs |
| [`embedded-developer`](skills/embedded-developer/) | Implements and debugs MCU/low-level embedded software, C/C++, HAL, interrupts, drivers, RTOS and BSP components | Write, optimize, review or repair firmware and drivers |
| [`embedded-qa`](skills/embedded-qa/) | Plans and performs host tests, static analysis, Renode/Robot Framework emulation, HIL and hardware verification | Independent testing, fault injection, acceptance evidence, regressions |

The architect chooses review depth: **full two-phase architecture review**, **bounded architecture delta**, or **fast path** for minor fixes. On full reviews it first produces a scored architecture plan (hardware efficiency, complexity, maintainability, real-time, robustness), records **Proceed / Revise / Reject**, and requests **explicit approval** before implementing modules. Phase 2 then follows **interface -> implementation -> actual verification -> checkpoint** for each dependency-ordered module. A bounded batch may continue without repeated pauses only when the user explicitly authorizes it. See [reasoning workflow](skills/embedded-architect/references/reasoning-workflow.md) and [evaluation matrix](skills/embedded-architect/references/architecture-evaluation.md).

## Install into Codex, Claude Code, Grok Build and Hermes

Use the repository `skills/` directory as the source of truth. **Run all commands below from the root of this extracted/cloned repository.** Python 3.10+ and standard library only are sufficient. This installer copies the complete skill folder, including `references/`, `scripts/` and `assets/`, and leaves existing installations untouched unless `--overwrite` is explicitly set.

### Install into a firmware project (cross-platform)

```powershell
# PowerShell - replace with the path to YOUR firmware repository
python scripts/install_skills.py --agent codex  --scope project --project-dir 'C:\Work\Firmware'
python scripts/install_skills.py --agent claude  --scope project --project-dir 'C:\Work\Firmware'
python scripts/install_skills.py --agent grok    --scope project --project-dir 'C:\Work\Firmware'
python scripts/install_skills.py --agent hermes  --scope project --project-dir 'C:\Work\Firmware'
```

Use `--dry-run` to preview paths, `--skill embedded-architect` to install only one skill (repeat `--skill` for more), and `--overwrite` to intentionally replace existing directories. On macOS/Linux, pass your firmware repository path as appropriate.

| Agent / product | Project-local destination | User-global destination | Discovery / invocation |
| --- | --- | --- | --- |
| **OpenAI Codex CLI / IDE** | `<firmware-repo>/.agents/skills/<name>/` | `~/.agents/skills/<name>/` | Codex discovers skills in those locations; explicitly request `embedded-architect` or select the skill |
| **Anthropic Claude Code** | `<firmware-repo>/.claude/skills/<name>/` | `~/.claude/skills/<name>/` | Start a new session; invoke `/embedded-architect`, `/embedded-developer` or `/embedded-qa` |
| **xAI Grok Build CLI** | `<firmware-repo>/.grok/skills/<name>/` | `~/.grok/skills/<name>/` | Invoke `/embedded-architect` etc. in **Grok Build**. This is not an install path for the Grok.com chat UI |
| **Nous Hermes Agent** | `<firmware-repo>/.hermes/skills/<name>/` | `~/.hermes/skills/<name>/` | Trust the project once, then start a new session and use `/embedded-architect` etc. |

These are **different agent runtimes**. A skill folder is not automatically installed into every agent merely because another agent can see it. If you want the same project to work in all four tools, run the installer once per `--agent`. To install user-wide instead, use:

```powershell
# Install all three into the user's personal Codex skill directory
python scripts/install_skills.py --agent codex --scope user
# Same pattern with --agent claude, grok, or hermes
```

#### Codex

Project skills use `.agents/skills`; user skills use `~/.agents/skills`. If you need just one capability:

```powershell
python scripts/install_skills.py --agent codex --scope project --project-dir 'C:\Work\Firmware' --skill embedded-developer
```

Start/restart the Codex session to refresh discovery if it was already running. See [Codex skills documentation](https://developers.openai.com/codex/skills).

#### Claude Code

Claude Code reads `.claude/skills/<name>/SKILL.md` (project) and `~/.claude/skills/` (personal). Invoke e.g. `/embedded-architect` for a structured design review, or let Claude select the skill based on its description. Note that **Claude.ai hosted Skill uploads are a separate installation surface**; the individual ZIPs in `dist/` are appropriate when a hosted UI requests a single skill ZIP. See [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

#### Grok Build (xAI)

Grok Build supports `.grok/skills/<name>/SKILL.md` (project or personal). The installer targets **Grok Build CLI**, not the consumer Grok website/mobile chat. Verify the currently installed Grok Build version supports skills before relying on project discovery. See [Grok Build skills guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/08-skills.md).

#### Hermes Agent (NousResearch)

After installing into the firmware project's `.hermes/skills/`, run the following **inside the firmware Git checkout**:

```powershell
hermes skills trust
hermes skills list
```

Then begin a new Hermes session; a trusted project makes the skill names invocable. For user scope, install into `~/.hermes/skills/`. **After this repository is published**, Hermes can also install direct from a GitHub skill tap:

```text
hermes skills tap add OWNER/embedded-agent-skills
hermes skills install OWNER/embedded-agent-skills/skills/embedded-architect
hermes skills install OWNER/embedded-agent-skills/skills/embedded-developer
hermes skills install OWNER/embedded-agent-skills/skills/embedded-qa
```

Replace `OWNER` with your actual GitHub owner. See the [Hermes skills reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md).

### Verification and duplicate names

Confirm the installed `SKILL.md` frontmatter matches the folder name. If you previously installed `embedded-systems-architect`, `embedded-architecture`, `embedded-firmware` or `embedded-firmware-developer`, uninstall the obsolete copies so two similarly described skills do not compete for activation. In each supported agent, invoke a simple task such as "Review the architecture of this firmware with `embedded-architect` and stop at the architecture approval gate." Skill behavior depends on the agent's filesystem and runtime permissions; installing a skill never installs Renode, compiler toolchains, debug probes or SDKs.

## Publishing and live CI badge

1. Create a GitHub repository, for example `OWNER/embedded-agent-skills`.
2. Push **the contents** of this repository to its default branch; keep `skills/`, `.github/`, `scripts/`, `maintenance/` and `tests/` at the repository root.
3. Allow GitHub Actions to create pull requests in **Settings > Actions > General** (subject to organization policies). Workflows already request the required `contents: write` and `pull-requests: write` token permissions.
4. Run **Actions > Check primary embedded sources > Run workflow** and **Actions > Validate embedded skills > Run workflow** to verify both workflows in your repository.
5. Once the validation workflow has actually succeeded, replace the static **CI configured** badge above with this live badge, substituting `OWNER`:

```markdown
[![Validate embedded skills](https://github.com/OWNER/embedded-agent-skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/OWNER/embedded-agent-skills/actions/workflows/validate-skills.yml)
```

Example initial push (from repository root):

```powershell
git init -b main
git add .
git commit -m 'Initial embedded agent skills'
git remote add origin https://github.com/OWNER/embedded-agent-skills.git
git push -u origin main
```

**No remote repository is created by the ZIP.** Replace `OWNER` before running these commands. The bundled `dist/<name>/skill.zip` packages are individual installable skills; the top-level repository ZIP is meant to be extracted and committed, not installed as one skill.

> **CI badge meaning:** GitHub Actions is *configured*, not asserted to have passed on a remote GitHub repository. After publishing, optionally replace it with the live Actions status badge for your actual `OWNER/REPO` (see [Publishing](#publishing-and-live-ci-badge)).

## Upstream monitoring

`.github/workflows/upstream-review.yml` runs on Mondays at 08:23 UTC and supports manual dispatch. It tracks the **16 monitored upstream sources** defined in [`maintenance/sources.json`](maintenance/sources.json), including curated public skills and official Renode, Zephyr, FreeRTOS, ESP-IDF, STM32C0 and Torizon sources. Baselines are in [`maintenance/reviewed-revisions.json`](maintenance/reviewed-revisions.json).

- **File watches:** compare verified branch SHA changes against monitored paths. Irrelevant changes yield no PR. Missing/incomplete comparisons are flagged for manual review.
- **Release watches:** detect relevant newest stable releases rather than all development commits.
- **Meaningful change:** generate/update `maintenance/reviews/upstream-changes.md`, propose reviewed revision-baseline updates, and open/update the same **draft PR**. Nothing is copied into an active skill automatically.
- **Governance:** human review classifies each change **adopt / reject / defer**. New upstream instructions are untrusted; verify vendor documentation and target SDK compatibility. No inference/model API is called.

See [UPSTREAM_POLICY.md](maintenance/UPSTREAM_POLICY.md) for the constraints and state handling. Note that bot-created PRs made using `GITHUB_TOKEN` may not trigger independent downstream CI on their own; the upstream workflow includes pre-PR validation for this reason.

## Public repositories and acknowledgments

This project draws on publicly available embedded-development skills, testing workflows, and official SDK/tooling repositories. The projects below informed the design or serve as ongoing technical references. **Inclusion here is an acknowledgment, not a claim of affiliation, endorsement, or permission to reuse code outside its license.** This project's original two-phase architecture reasoning workflow also draws on the author's earlier, privately supplied `embedded-systems-architect` skill.

### Community skill projects and verification patterns

| Source repository | Reference area |
| --- | --- |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | General embedded-systems workflow, firmware implementation and skill structure |
| [rovinax/embedded-skills](https://github.com/rovinax/embedded-skills) | Architecture, C style, RTOS, ISR, drivers and embedded documentation |
| [ezrover/ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill) | ESP32-specific development conventions and target pitfalls |
| [ziphercx/ESP32-Agent-Skill](https://github.com/ziphercx/ESP32-Agent-Skill) | Additional ESP32 workflow and peripheral references |
| [alexex1993/mcu-skills](https://github.com/alexex1993/mcu-skills) | Board-specific MCU profiles and hardware-aware development guidance |
| [zhinkgit/embeddedskills](https://github.com/zhinkgit/embeddedskills) | Build, flashing, debugging and toolchain integration patterns |
| [captainluzik/oh-my-embedded](https://github.com/captainluzik/oh-my-embedded) | Embedded engineering, firmware debugging and review tooling |
| [creatifcoding/gbg](https://github.com/creatifcoding/gbg) | Project-specific Renode launch and virtual UART workflows; patterns adapted selectively |
| [Agile-V/agile_v_skills](https://github.com/Agile-V/agile_v_skills) | Verification evidence, simulation traceability and emulation-versus-hardware boundaries |

### Official frameworks, emulation and vendor sources

| Source repository | Reference area |
| --- | --- |
| [renode/renode](https://github.com/renode/renode) | Renode emulator capabilities, releases and automated virtual testing |
| [espressif/esp-idf](https://github.com/espressif/esp-idf) | ESP-IDF releases and target-specific embedded development behavior |
| [FreeRTOS/FreeRTOS-Kernel](https://github.com/FreeRTOS/FreeRTOS-Kernel) | FreeRTOS kernel releases, scheduling and concurrency behavior |
| [zephyrproject-rtos/zephyr](https://github.com/zephyrproject-rtos/zephyr) | Zephyr releases, board support and RTOS integration |
| [STMicroelectronics/STM32CubeC0](https://github.com/STMicroelectronics/STM32CubeC0) | STM32C0 HAL/CMSIS device definitions and peripheral interfaces |
| [torizon/torizoncore-builder](https://github.com/torizon/torizoncore-builder) | TorizonCore Builder and embedded Linux image customization |
| [toradex/meta-toradex-torizon](https://github.com/toradex/meta-toradex-torizon) | Torizon Yocto layers and Linux integration |

### Moderated upstream synchronization

**We intend to keep the skills improving alongside these projects, with human moderation rather than blind synchronization.** Our [source manifest](maintenance/sources.json) tracks all 16 repositories, and the [upstream review workflow](.github/workflows/upstream-review.yml) is configured to check them weekly (or on demand):

1. **Detect without an LLM:** compare only configured source paths or new stable releases; ignore unrelated upstream activity.
2. **Open a draft PR when relevant:** record the upstream commits/releases, affected skills, and review evidence. No external instruction or code is automatically copied into a skill.
3. **Moderate every candidate improvement:** maintainers assess correctness, relevance to supported targets, compatibility, provenance and licensing; mark it **adopt / reject / defer**.
4. **Integrate deliberately:** accepted improvements require an authored patch, validation and appropriate regression evidence before approval and merge.

The CI review mechanism is **configured but is not active until this repository is published with GitHub Actions and pull-request permissions enabled**. Monitored sources can evolve independently; a published change is not automatically a suitable instruction for every MCU, RTOS, Linux BSP, or Renode model. See the detailed [upstream review policy](maintenance/UPSTREAM_POLICY.md).

**Thank you** to the owners, maintainers and contributors of all these repositories. Their publicly shared code, skills, documentation and engineering experience have helped make this project more useful and robust. We appreciate their ongoing contributions to the embedded-development community.

## Bounded QA contracts and source handoffs

During task segmentation, refine acceptance criteria with the user and existing
specialist evidence using the QA [task contract guide](skills/embedded-qa/references/task-qa-contracts.md).
Architects define input/output, integration and verification ownership; developers
preserve source-complete bundles; QA checks frozen inputs and reviewers reuse
unchanged evidence rather than repeating every matrix. Missing hardware becomes
an explicit bench gap, not an endless software-review loop.

The optional `skills/embedded-qa/scripts/verify_handoff.py` validates a retrieved
bundle's declared file hashes and required paths. It does not prove dependency
completeness, build success, hardware qualification or agent compliance. Source
publication uses the host runtime's attachment mechanism, not a vendor-specific
service. No scheduler settings, iteration limits or automatic retry policy are
changed by these skills.

## Testing and packaging

```powershell
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python -m unittest discover -s skills/embedded-qa/tests -v
python scripts/package_all.py
# Network and GitHub API token required for live source checks:
python scripts/check_upstream.py --dry-run
```

All three skills use minimal `SKILL.md` entrypoints and conditional references. QA evidence distinguishes host tests, virtual models, HIL and physical qualification. Validation of file structure and unit tests does **not** establish real target build, emulator availability or on-board verification.

## Provenance and security

The architecture approval process was adapted from the earlier `embedded-systems-architect` skill: evaluated design first, explicit decision/approval, interface-first modules, validated checkpoints. Its platform-specific hardcoded assumptions were replaced by conditional, exact-target checks. The upstream reference list records the inspected original projects, not inherited code execution authority. The repository includes original instructional material but no forced third-party license; choose a suitable license before public release.
