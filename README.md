# course-builder

A reusable Claude Code plugin that turns a `module.spec.yaml` into a full course-module artifact bundle — syllabus/ementa, a student git repo with planted **verified** bugs, lesson plans, Gamma slide instructions, 1st-person instructor scripts, and an HTML instructor portal — by orchestrating 9 subagents, 2 skills and 2 `PreToolUse` hooks via a single `/build-module` command.

It is generic (not hard-coded to any course) and dogfoods itself: the example spec in `examples/` recreates Module 3 of the "IA para Devs" course (CESAR 2026).

## Install

Add this repository as a Claude Code plugin (marketplace or local path). The manifest at `.claude-plugin/plugin.json` declares the four plugin surfaces:

- `commands/` — the `/build-module` slash command
- `agents/` — 9 subagents (syllabus-architect, trend-researcher, repo-scaffolder, bug-smith, lesson-planner, slide-instructor, script-writer, portal-assembler, qa-reviewer)
- `skills/` — 2 skills (bug-verification, gamma-deck)
- `hooks/` — 2 `PreToolUse` hooks (gate destructive ops, enforce artifact-first)

## Run

```
claude /build-module examples/module-spec.ia-devs-mod3.yaml
```

Generated modules land in `out/<curso>/<module>/` (gitignored).

## Spec

- Schema: [`schemas/module.spec.schema.json`](schemas/module.spec.schema.json)
- Example: [`examples/module-spec.ia-devs-mod3.yaml`](examples/module-spec.ia-devs-mod3.yaml)

Required fields: `curso` (with `nome`), `publico_alvo`, `aulas` (non-empty, each with `numero`, `titulo`, non-empty `topicos`). Optional: `ferramenta_base` (defaults `nome: Claude Code`), `filosofia` (both flags default `true`), `branding` (defaults derived from `curso`), `pesquisar_tendencias` (default `true`).

`ferramenta_base.versao` is a concrete version floor consumed by `bug-smith` and `qa-reviewer` to mitigate tool-rot.