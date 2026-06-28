# course-builder

A reusable Claude Code plugin that turns a `module.spec.yaml` into a full course-module artifact bundle — ementa (syllabus), a student git repo with planted **verified** bugs, lesson plans, Gamma slide instructions, 1st-person instructor scripts, and an HTML instructor portal — by orchestrating 9 subagents, 2 skills and 2 `PreToolUse` hooks via a single `/course-builder:build-module` command.

It is generic (not hard-coded to any course) and dogfoods itself: the example spec in `examples/` recreates Module 3 of the "IA para Devs" course (CESAR 2026).

## Install

This is a local plugin. The manifest at `.claude-plugin/plugin.json` declares metadata; all components are **auto-discovered** at conventional paths:

- `commands/` — the `/course-builder:build-module` slash command
- `agents/` — 9 subagents: `trend-researcher`, `ementa-architect` (piloto v1), `repo-scaffolder`, `bug-smith`, `exercise-author`, `lesson-planner`, `instructor-scriptwriter`, `portal-assembler`, `qa-reviewer`
- `skills/` — 2 skills: `cesar-html-style`, `first-person-roteiro`
- `hooks/hooks.json` — 2 `PreToolUse` hooks: `block-real-secret-prefixes`, `block-destructive-git` (guardrails, not HITL gates)

**Fastest (dev/test, current session only):**

```powershell
claude --plugin-dir .
```

**Persistent (local marketplace):** create a `.claude-plugin/marketplace.json` in a parent catalog dir listing this plugin, then:

```powershell
/plugin marketplace add <path-to-catalog>
/plugin install course-builder@<marketplace-name>
```

Verify after install:

```powershell
claude plugin validate .
```

## Run

In a Claude Code session where the plugin is loaded:

```
/course-builder:build-module examples/module-spec.ia-devs-mod3.yaml
```

The command runs from the **session's current working directory** — runtime artifacts are written to `out/<modulo>/` relative to that cwd (gitignored). For the dogfood spec, `<modulo>` derives from `spec.curso.codigo` (e.g. `IH-261`).

The orchestrator dispatches the 9 agents in 4 phases with 2 HITL gates:

| Phase | Agents (in order) | Gate |
|-------|-------------------|------|
| 0 — spec-parse | (orchestrator validates against schema) | **HITL #1** — stop on invalid spec |
| 1 — ementa | `trend-researcher` (if `pesquisar_tendencias`) → `ementa-architect` | piloto v1 green check |
| 2 — repo | `repo-scaffolder` → `bug-smith` → `exercise-author` | — |
| 3 — aulas | `lesson-planner` → `instructor-scriptwriter` → `portal-assembler` | — |
| 4 — QA | `qa-reviewer` (drift vs baseline) | **HITL #2** — pause for human greenlight |

Plugin agents are namespaced `course-builder:<slug>`; the orchestrator dispatches them by that namespaced name. Hooks fire automatically as guardrails (block real secret prefixes and destructive git ops); they are **not** HITL gates.

## Spec

- Schema: [`schemas/module.spec.schema.json`](schemas/module.spec.schema.json)
- Example (dogfood): [`examples/module-spec.ia-devs-mod3.yaml`](examples/module-spec.ia-devs-mod3.yaml)

Required fields: `curso` (with `nome`), `publico_alvo`, `aulas` (non-empty, each with `numero`, `titulo`, non-empty `topicos`, `duracao_min`), `ferramenta_base` (`nome`, `versao`), `filosofia` (`artifact_first`, `hitl_so_grave`), `branding` (`org`, `cor_acento`). Optional: `pesquisar_tendencias` (default `true`).

`ferramenta_base.versao` is a concrete version floor consumed by `bug-smith` (pins bugs + repros) and `qa-reviewer` (drift detection) to mitigate tool-rot.

## Self-dogfood

```powershell
python scripts/dogfood-validate.py
```

Structurally validates the plugin: example spec vs schema, all 9 agent frontmatters (name/description/tools, no omit-trap), command cross-references, skill resolution, `hooks/hooks.json` + script presence, and `plugin.json` manifest shape. Pair with `claude plugin validate` for the official manifest check.