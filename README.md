# course-builder

A reusable Claude Code plugin that turns a `module.spec.yaml` into a full course-module artifact bundle by orchestrating 12 subagents, 3 skills and 2 `PreToolUse` hooks via a single `/course-builder:build-module` command. Four modes, chosen by `tipo_avaliacao`:

| Mode | What the module gets |
|---|---|
| `repo-bugs` (default) | ementa, student git repo with planted **verified** bugs, lesson plans, Gamma slide instructions, 1st-person instructor scripts, HTML portal |
| `projeto-pitch` | the same lessons plus a group proposal + pitch project kit |
| `debate-caso` | lessons in 4 blocks with 7 architectural cases debated in groups |
| `estudo-dirigido` | expository lessons on one fictional case with an executable kit; one single-source Python file per lesson rendered by bundled generators into deck text, script, plan, flowcharts, study guide PDF, monitor guide, interactive guide and professor guide; real demo runs recorded; general guide and class README |

It is generic (not hard-coded to any course) and dogfoods itself: `examples/module-spec.ia-devs-mod3.yaml` recreates Module 3 of "IA para Devs" (CESAR 2026), and `examples/module-spec.sistemas-ia-2026-2-a.yaml` describes M3 and M4 of class 2026.2-A of "Sistemas com IA para Devs" (CESAR School, Nov 2026), the module the `estudo-dirigido` mode was extracted from.

## Install

This is a local plugin. The manifest at `.claude-plugin/plugin.json` declares metadata; all components are **auto-discovered** at conventional paths:

- `commands/` — the `/course-builder:build-module` slash command
- `agents/` — 12 subagents: `trend-researcher`, `ementa-architect` (piloto v1), `repo-scaffolder`, `bug-smith`, `exercise-author`, `lesson-planner`, `instructor-scriptwriter`, `portal-assembler`, `qa-reviewer`, and, for `estudo-dirigido`, `case-kit-builder`, `demo-recorder`, `guide-author`
- `skills/` — 3 skills: `cesar-html-style`, `first-person-roteiro`, `aula-fonte-unica` (the contract of the `estudo-dirigido` mode)
- `hooks/hooks.json` — 2 `PreToolUse` hooks: `block-real-secret-prefixes`, `block-destructive-git` (guardrails, not HITL gates)

Not auto-discovered, used by the `estudo-dirigido` agents through the plugin root:

- `assets/preparacao/` — the generators (`construir_aula.py`, `figuras.py`, `exportar_figuras.py`, `construir_estudo.py`, `construir_monitor.py`, `construir_professor.py`, `construir_guia_modulos.py`, `guias/gerar_guia.py` + `motor.js`, …); its `README.md` says what each one reads, writes and checks
- `assets/exemplo-2026-2-a/` — one complete lesson of 2026.2-A as reference (lesson source, professor speech, interactive guide content, `turma.py`, case kit README)
- `scripts/scaffold_preparacao.py` — copies the generators into `out/<modulo>/preparacao/` and writes `turma.py` from the spec

**Fastest (dev/test, current session only):**

```powershell
claude --plugin-dir .
```

**Persistent (local marketplace):** the sibling folder `../ia-devs-marketplace` is the catalog (`ia-devs-local`); `../ia-devs-marketplace/sincronizar_plugin.py` copies this folder into it. Then:

```powershell
/plugin marketplace add <path-to-ia-devs-marketplace>
/plugin install course-builder@ia-devs-local
```

Verify after install:

```powershell
claude plugin validate .
```

**Codex:** `python -B scripts/portar_codex.py <codex plugin folder>` regenerates the Codex port (`$build-module`) from this source.

## Run

In a Claude Code session where the plugin is loaded:

```
/course-builder:build-module examples/module-spec.ia-devs-mod3.yaml
/course-builder:build-module examples/module-spec.sistemas-ia-2026-2-a.yaml
```

The command runs from the **session's current working directory** — runtime artifacts are written to `out/<modulo>/` relative to that cwd (gitignored). `<modulo>` derives from `spec.curso.codigo` (e.g. `IH-261`, `2026.2-A`).

The orchestrator dispatches the agents in 4 phases with 2 HITL gates:

| Phase | Agents (in order) | Gate |
|-------|-------------------|------|
| 0 — spec-parse | (orchestrator validates against schema) | **HITL #1** — stop on invalid spec |
| 1 — ementa | `trend-researcher` (if `pesquisar_tendencias`) → `ementa-architect` | piloto v1 green check |
| 2 — repo/kit | `repo-scaffolder` → `bug-smith` → `exercise-author` · `estudo-dirigido`: `repo-scaffolder` → `case-kit-builder` | — |
| 3 — aulas | `lesson-planner` → `instructor-scriptwriter` → `portal-assembler` · `estudo-dirigido`: `lesson-planner` → `demo-recorder` → `exercise-author` → `instructor-scriptwriter` → `guide-author` → `portal-assembler` | — |
| 4 — QA | `qa-reviewer` (drift vs baseline) | **HITL #2** — pause for human greenlight |

In `estudo-dirigido`, publishing the pages as Artifacts and pushing the class repository happen only after HITL #2, each on explicit request; `demo-recorder` runs the base tool with the instructor's account (budget-capped), or records that the demonstrations were not rehearsed.

Plugin agents are namespaced `course-builder:<slug>`; the orchestrator dispatches them by that namespaced name. Hooks fire automatically as guardrails (block real secret prefixes and destructive git ops); they are **not** HITL gates.

## Spec

- Schema: [`schemas/module.spec.schema.json`](schemas/module.spec.schema.json)
- Examples: [`examples/module-spec.ia-devs-mod3.yaml`](examples/module-spec.ia-devs-mod3.yaml), [`examples/module-spec.sistemas-ia-2026-2-a.yaml`](examples/module-spec.sistemas-ia-2026-2-a.yaml)

Required fields: `curso` (with `nome`), `publico_alvo`, `aulas` (non-empty, each with `numero`, `titulo`, non-empty `topicos`). Mode-specific: `projeto` for `projeto-pitch`; `estrutura_aula` and `casos_debate` for `debate-caso`; `turma`, `caso`, `ferramenta_base` and per-lesson `data` and `pergunta` for `estudo-dirigido` (optional there: `aulas[].modulo`, `modulo_nome`, `monitor`, `ementas`, `execucoes_reais`).

`ferramenta_base.versao` is a concrete version floor consumed by `bug-smith` (pins bugs + repros) and `qa-reviewer` (drift detection) to mitigate tool-rot.

## Self-dogfood

```powershell
python scripts/dogfood-validate.py
```

Structurally validates the plugin: every example spec vs schema, all 12 agent frontmatters (name/description/tools, no omit-trap), command cross-references, skill resolution, `hooks/hooks.json` + script presence, `plugin.json` manifest shape, and, for `estudo-dirigido`, that the generator kit compiles and `scaffold_preparacao.py` turns the 2026.2-A spec into a `turma.py`. Pair with `claude plugin validate` for the official manifest check.
