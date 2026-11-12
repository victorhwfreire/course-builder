---
description: Orchestrate the 12 course-builder subagents through 4 phases (spec-parse, ementa, repo/kit, aulas, QA) to turn a module.spec.yaml into a full course-module artifact bundle, with 2 HITL gates and PreToolUse hooks as guardrails. Modes repo-bugs, projeto-pitch, debate-caso and estudo-dirigido.
argument-hint: [path/to/module.spec.yaml]
---

# /course-builder:build-module — course-builder orchestrator

You are the orchestrator of the `course-builder` plugin. The human invoked `/course-builder:build-module <spec-path>` with `$ARGUMENTS`. Follow the phases below in order. **Command directs, Agent decides, Skill executes**: you dispatch subagents and enforce gates; you do not author artifacts yourself.

## Inputs

- **Spec path:** `$ARGUMENTS` (the path the human passed, e.g. `examples/module-spec.ia-devs-mod3.yaml`). If `$ARGUMENTS` is empty, stop and ask the human for a spec path.
- **Output dir:** `out/<modulo>/` (derive `<modulo>` in Phase 0).
- **Baseline path (optional):** the path to known-good module artifacts (the real ementa, repo, etc.) used by `qa-reviewer` for drift measurement. The human supplies it, or omits it — there is **no built-in default**, because the baseline lives wherever the reference module happens to be on that machine. If omitted, `qa-reviewer` skips drift-vs-baseline and records a note in `qa-report.md` (every other check still runs).
- **Plugin root:** the directory that holds this plugin's `commands/`, `agents/`, `schemas/`, `scripts/` and `assets/` (`${CLAUDE_PLUGIN_ROOT}` when the runtime sets it). Resolve it to an absolute path in Phase 0; mode `estudo-dirigido` agents need it to reach `scripts/scaffold_preparacao.py`, `assets/preparacao/` and `assets/exemplo-2026-2-a/`.

<!-- claude:despacho:inicio -->
## Dispatch mechanics (applies to every phase)

- Dispatch each subagent via the subagent/`Task` tool, passing: **agent name** (from `agents/<name>.md`), the **spec path** (absolute), the **output dir** (absolute), the **plugin root** (absolute, mode `estudo-dirigido`), and — for `qa-reviewer` only — the **baseline path**. **Plugin agents are namespaced:** pass the Task tool the namespaced name `course-builder:<slug>` (e.g. `course-builder:ementa-architect`, `course-builder:bug-smith`, `course-builder:qa-reviewer`), not the bare slug — plugin-shipped agents register under the plugin name and a bare-name lookup will fail.
- One agent per dispatch. Wait for each agent to return before dispatching the next (the phases are sequential; handoffs are ordered).
- **Agents do NOT commit.** No agent runs `git`. Git is handled by the human (or by you, only after Gate HITL #2 greenlight and only if the human asks). This is a hard rule.
- **Report progress per phase** to the human: which agent ran, what artifact(s) it produced, and any flags it raised. Keep the human oriented — a one-line status per dispatch is enough.
- **Hooks are guardrails, not HITL gates.** The two `PreToolUse` hooks (`block-real-secret-prefixes`, `block-destructive-git`) fire automatically on dangerous tool calls during agent execution and block them with exit 2. They are **safety guardrails**, not human-in-the-loop decision points. Do not conflate them with the 2 HITL gates below. The only HITL gates are **Phase 0** (spec-parse) and **Phase 4** (qa-reviewer).
<!-- claude:despacho:fim -->

---

## Phase 0 — spec-parse  (Gate HITL #1)

1. **Read** the spec at `$ARGUMENTS`. If the file does not exist or cannot be parsed, stop and surface the error to the human.
2. **Validate** the spec against `schemas/module.spec.schema.json`. Use a JSON-schema validator via `Bash` (e.g. `python -m jsonschema` or `ajv`), or a structural validation pass that checks every `required` field and constraint in the schema. If the spec is **invalid** (missing required fields, wrong types, empty `aulas`, etc.):
   - **STOP.** This is **Gate HITL #1** (spec-parse). Per `spec.filosofia.hitl_so_grave`, a malformed spec propagates errors through the entire bundle — this is a **grave** path, so HITL is justified here.
   - Surface every validation error to the human with the field path and the schema constraint violated. Do **not** proceed to Phase 1, and do **not** dispatch any agent. Wait for the human to fix the spec and re-run `/build-module`.
   - Note: `ementa-architect` also writes `spec-gaps.md` for **softer** gaps (optional fields, thin content) discovered during its own coverage check — those are **not** the Phase-0 gate. Hard schema-invalidity is the Phase-0 gate; soft gaps are handled in Phase 1.
3. If the spec is valid, **derive `<modulo>`** from `spec.curso.codigo` (e.g. `IH-261`) if present, otherwise from the spec filename stem. Create the output dir `out/<modulo>/`.
4. **Copy** the spec into `out/<modulo>/module.spec.yaml` — this is the canonical contract every downstream agent reads. (Do not mutate the human's original spec file.)

Report: spec valid, `<modulo>` derived, output dir created, canonical spec copied.

---

## Phase 1 — ementa  (piloto v1)

5. **Conditional — trend-researcher:** if `spec.pesquisar_tendencias: true`, dispatch `trend-researcher` with the spec path + output dir. It produces `out/<modulo>/tendencias.md`. If `spec.pesquisar_tendencias: false`, **skip** this dispatch (the `ementa-architect` will derive the tendências section from `spec.aulas[*].topicos` and mark that external research did not run).
6. **Dispatch `ementa-architect`** with the spec path + output dir. It produces `out/<modulo>/ementa.md` + `out/<modulo>/ementa.html` (and `out/<modulo>/spec-gaps.md` if it finds soft gaps).
7. **Piloto v1 check (hard gate before Phase 2):** `ementa-architect` is the **first agent that must be green end-to-end** — it is the plugin's piloto v1. Before dispatching any Phase 2 agent, verify:
   - `out/<modulo>/ementa.md` exists and contains all **13 fixed sections** in order.
   - `out/<modulo>/ementa.html` exists, links `estilo.css` relatively, and has the `:root` accent from `spec.branding.cor_acento`.
   - If `spec-gaps.md` was produced, read it and surface its contents to the human (soft gaps, not a stop — but the human should know).
   - If `ementa-architect` failed or its output is missing/malformed, **STOP and report**. Do **not** continue to Phase 2 on a broken ementa — every downstream agent depends on a coherent ementa.
   - *(Mode `estudo-dirigido`)* When every file in `spec.ementas` already exists (paths relative to the output dir), `ementa-architect` reads them instead of writing `ementa.md`; the check is then that those files exist and that `spec-gaps.md`, if any, was surfaced.

Report: trend-researcher skipped or produced `tendencias.md`; ementa-architect produced `ementa.md` + `ementa.html` (+ `spec-gaps.md` if any); piloto v1 green or stop.

---

## Phase 2 — repo dos alunos / kit de projeto

**Branch on `spec.tipo_avaliacao`** (default `repo-bugs` when the field is absent). The four modes are mutually exclusive; dispatch only the branch that matches.

### Mode `repo-bugs` (default) — dispatch in this exact order (sequencing per each agent's handoff notes):

8. **`repo-scaffolder`** — scaffolds `out/<modulo>/repo-alunos/main/` + `out/<modulo>/repo-alunos/gabaritos/README.md`. Pass spec path + output dir.
9. **`bug-smith`** — plants verified, reproducible bugs in `main/`, writes correct versions in `gabaritos/`, registers each in `gabaritos/bug-manifest.md` with the `ferramenta_base.versao` version-pin header, writes repro tests in `main/testes/`. Pass spec path + output dir.
10. **`exercise-author`** — writes student-facing enunciados in `main/exercicios/aula-<n>/` (referencing bugs indirectly, never leaking gabaritos) and `gabaritos/rubricas.md` (instrutor-facing, not an autograder). Pass spec path + output dir.

### Mode `projeto-pitch` — dispatch in this order, **SKIPPING `bug-smith`**:

8. **`repo-scaffolder`** (projeto-pitch mode) — scaffolds `out/<modulo>/repo-alunos/projeto/` (README brief + `templates/` + `dados/` + `entregaveis/`, all placeholders) and `out/<modulo>/repo-alunos/instrutor/README.md` (instructor-only). No `main/`/`gabaritos/` bug tree. Pass spec path + output dir.
9. **`bug-smith` — SKIP.** Do **not** dispatch it: `projeto-pitch` has no planted bugs (bug-smith has a mode guard that no-ops if dispatched by mistake). Report one line: "bug-smith pulado: tipo_avaliacao=projeto-pitch".
10. **`exercise-author`** (projeto-pitch mode) — fills `projeto/README.md` (the real project brief from `spec.projeto` + ementa), the three `projeto/templates/` files, and `instrutor/rubricas.md` (instrutor-facing rubric from `spec.projeto.rubrica`, weights sum 100%). Pass spec path + output dir.

### Mode `debate-caso` — dispatch only `exercise-author`, **SKIPPING both `repo-scaffolder` and `bug-smith`**:

8. **`repo-scaffolder` — SKIP.** Do **not** dispatch it: `debate-caso` has no student repo (repo-scaffolder has a mode guard that no-ops if dispatched by mistake). Report one line: "repo-scaffolder pulado: tipo_avaliacao=debate-caso".
9. **`bug-smith` — SKIP.** Do **not** dispatch it, same reasoning. Report one line: "bug-smith pulado: tipo_avaliacao=debate-caso".
10. **`exercise-author`** (debate-caso mode) — writes `out/<modulo>/casos/aula-<n>/caso-<k>.md` (exactly 7 per aula, student-facing, from `spec.aulas[n].casos_debate`) and `out/<modulo>/casos/instrutor/aula-<n>-notas-debate.md` (instructor-facing debate notes). Pass spec path + output dir. It is the **only** Phase-2 agent dispatched in this mode.

### Mode `estudo-dirigido` — dispatch in this order, **SKIPPING `bug-smith`**; `exercise-author` moves to Phase 3:

Every agent of this mode follows the skill `aula-fonte-unica` (one source per lesson, deterministic generators, nothing invented). Pass the plugin root to each one.

K1. **`repo-scaffolder`** (estudo-dirigido mode) — runs `scripts/scaffold_preparacao.py`, which copies the generators into `out/<modulo>/preparacao/` and writes `preparacao/turma.py` from the spec; creates `material-alunos/<caso.pasta>/` and the base of the class repository in `repo-turma/`.
K2. **`bug-smith` — SKIP.** Report one line: "bug-smith pulado: tipo_avaliacao=estudo-dirigido".
K3. **`case-kit-builder`** — builds the executable case kit in `material-alunos/<caso.pasta>/` (data, inputs with answer key, tools and scripts every demonstration and practice uses; destructive actions simulated; no real credentials), runs every script that does not call the model, and writes `preparacao/kit-manifest.md`.

Report per dispatch: artifact(s) produced + any flags (e.g. `não-verificado` bugs in the manifest for `repo-bugs`; skipped bug-smith for `projeto-pitch`; skipped repo-scaffolder + bug-smith for `debate-caso`; for `estudo-dirigido`, the kit commands left unverified and why).

---

## Phase 3 — aulas

Dispatch in this exact order:

11. **`lesson-planner`** — produces `out/<modulo>/aulas/aula-<n>/plano.md` per aula. Pass spec path + output dir.
12. **`instructor-scriptwriter`** — produces `out/<modulo>/aulas/aula-<n>/roteiro.md` (1st-person, no 2nd-person imperative leaks) per aula. Pass spec path + output dir.
13. **`portal-assembler`** — produces `out/<modulo>/portal/` linking ementa, aulas, repo. It runs **last**. If it reports **missing dependencies** (e.g. a `plano.md` or `roteiro.md` absent for some aula), re-dispatch the failed prior agent (`lesson-planner` for missing planos, `instructor-scriptwriter` for missing roteiros), then re-dispatch `portal-assembler`. Cap re-dispatch at one retry per missing dependency; if the dependency is still missing, stop and report.

Report per dispatch: artifact(s) produced; note any re-dispatch.

### Mode `estudo-dirigido` — replaces steps 11–13 above

Each agent covers every lesson of the spec before the next one starts. Every source lives in `out/<modulo>/preparacao/`; every rendered file comes from a generator, never from an agent writing it by hand.

E1. **`lesson-planner`** — writes `preparacao/aulas/<id>.py` (`META`, `SLIDES`, `PARTE2`, `PLANO`, `MONITOR`) on the fixed grid of the skill, with the break and monitor slots from `spec.turma`; runs `construir_aula`, `exportar_figuras` and `construir_monitor` until they pass.
E2. **`demo-recorder`** — tests the base tool login, runs the `PARTE2` commands of every lesson on a copy of the kit (budget-capped), keeps the raw outputs in `preparacao/ensaio/<id>/`, records the outputs the interactive guide will show in `preparacao/guias/execucoes.json` + `pedidos.json`, and writes `preparacao/execucoes-relatorio.md` with what was expected, what happened and an `ajustar-fonte` list. If `spec.execucoes_reais` is false or the login fails, it records that the demonstrations were not rehearsed and runs nothing. These runs use the instructor's account: say so in the progress report.
E3. **Conditional re-dispatch of `lesson-planner`** — only if `execucoes-relatorio.md` has `ajustar-fonte` items; once.
E4. **`exercise-author`** — writes the `ESTUDO` of every source (concepts, glossary, three step-by-step practices in the base tool, self-check, primary-source readings), runs `construir_estudo` (PDF) and opens the practice pages.
E5. **`instructor-scriptwriter`** — writes `preparacao/professor/fala_<id>.py` (3 to 5 paragraphs per slide, acts with per-step minutes that add up to the slide, commands copied from `PARTE2`, preparation, contingency, references) and runs `construir_professor` until it passes.
E6. **`guide-author`** — writes `preparacao/guias/conteudo_<id>.py`, adapts the case-specific tools once (`guias/agente_caso.js` and `agente_caso.py`, injected into `motor.js` by the generator), and runs `guias/gerar_guia`. Only outputs present in `execucoes.json` appear as recorded.
E7. **`portal-assembler`** — fills `GUIA_MODULOS` in `turma.py`, runs `construir_guia_modulos`, and writes the root `README.md` (lessons, grid, monitors, what each lesson has, before each lesson, how to regenerate, pages to publish). No `portal/index.html` in this mode.

If a generator keeps failing after the owning agent's second attempt, stop and report the generator's error list; do not let an agent edit a generator to make a check pass.

---

## Phase 4 — QA  (Gate HITL #2)

14. **Dispatch `qa-reviewer`** with the spec path + output dir + **baseline path** (only if the human supplied one). If no baseline was given, dispatch `qa-reviewer` without one — it skips drift-vs-baseline and records a note. In mode `repo-bugs`, `qa-reviewer` re-verifies planted bugs against the pinned `ferramenta_base.versao`; in mode `projeto-pitch` it skips bug re-verification (no bugs) and instead checks project-kit coherence (rubric weights sum 100%, brief traces to `spec.projeto`, `instrutor/` not leaked); in mode `debate-caso` it skips bug re-verification and instead checks the debate-block coherence (exactly 7 `caso-<k>.md` per aula with no leaked analysis, instructor debate notes complete, `estrutura_aula.blocos` minutes summing to `duracao_min`, and `slide_max` — if set — respected by every `slides-gamma.md`); in mode `estudo-dirigido` it skips bug re-verification and instead runs `construir_tudo.py`, checks every HTML at 390 and 1280 px, opens the PDF practice pages, traces every command to `kit-manifest.md`, every model output to `execucoes.json` or the rehearsal, every number to a primary source, and flags unrehearsed demonstrations as a warning. It measures drift vs the baseline when provided (dogfood-as-eval: drift from a known-good baseline = a **plugin regression**, not just a module difference), runs coherence checks, and produces `out/<modulo>/qa-report.md` with a verdict (SHIPPABLE / NÃO-SHIPPABLE / SHIPPABLE-COM-RESERVAS) and findings by severity.
15. **Gate HITL #2 (hard pause):** after `qa-reviewer` returns, **STOP**. Surface `qa-report.md` to the human — the verdict, the blocker/warning/note counts, and the drift section. **Do NOT auto-ship.** Do NOT declare the module shipped. Do NOT commit. Per `spec.filosofia.hitl_so_grave`, shipping a wrong module to students is a **grave and irreversible** path — HITL is justified here even though the rest of the pipeline is automated. The module is only "shipped" once a human reads the report and gives explicit greenlight.

Report: `qa-report.md` produced; verdict + counts surfaced; orchestrator paused for human greenlight.

---

## After Gate HITL #2 greenlight (only on human request)

If the human reviews `qa-report.md` and says to ship:
- If there are **blockers**, do not ship — the human must either fix them (re-dispatch the offending agent) or explicitly accept the risk. Re-dispatch the agent that owns the blocker; then re-dispatch `qa-reviewer` to re-run.
- If there are only **warnings/notes** and the human greenlights, the module is shipped.
- Git: only if the human asks. Agents never committed; you (or the human) handle the commit now, after greenlight.

### Mode `estudo-dirigido` — publishing (each step only on explicit human request)

- **Pages:** each HTML page (interactive guide, monitor guide, professor guide, general guide) is published as a private Artifact. Extract the publishable body with `python -B preparacao/guias/extrair_corpo.py <canonical.html> <body.html>`, publish the body, and after any later change confirm with `--comparar` that the published body still equals the canonical one. Record each URL in the README table. Sharing is the human's decision; never share on your own.
- **Class repository:** `python -B preparacao/copiar_para_repositorio.py <clone>` copies the case kit and the study PDFs into a clone of `spec.turma.repositorio`. Show the human the diff (`git status`), then commit and push only with explicit approval, never with force.
- **Before each lesson:** remind the human that the demonstrations need the rehearsal in `PARTE2` ("Antes da aula") on the day, whatever `execucoes-relatorio.md` says.

---

## Usage example

```
/course-builder:build-module examples/module-spec.ia-devs-mod3.yaml
```

This dogfoods the plugin: the example spec recreates Module 3 of "IA para Devs" (CESAR 2026). If you have the real Module 3 artifacts locally, pass that directory as the baseline so `qa-reviewer` can measure drift during Phase 4; otherwise drift-vs-baseline is skipped (all other checks still run).

```
/course-builder:build-module examples/module-spec.sistemas-ia-2026-2-a.yaml
```

Mode `estudo-dirigido`: the example spec describes M3 and M4 of class 2026.2-A of "Sistemas com IA para Devs" (CESAR School, Nov 2026). Its real output folder (`2026.2-A`, with `preparacao/`, `M3/`, `M4/`, `material-alunos/`) is the baseline.

---

## Quick reference — phase → agent dispatch order

| Phase | Agent (in order) | Gate |
|-------|------------------|------|
| 0 — spec-parse | (no agent; orchestrator validates) | **HITL #1** — stop on invalid spec |
| 1 — ementa | `trend-researcher` (if `pesquisar_tendencias: true`) → `ementa-architect` | piloto v1 check |
| 2 — repo/projeto/casos/kit | `repo-bugs`: `repo-scaffolder` → `bug-smith` → `exercise-author` · `projeto-pitch`: `repo-scaffolder` → ~~`bug-smith`~~ (skip) → `exercise-author` · `debate-caso`: ~~`repo-scaffolder`~~ (skip) → ~~`bug-smith`~~ (skip) → `exercise-author` · `estudo-dirigido`: `repo-scaffolder` → ~~`bug-smith`~~ (skip) → `case-kit-builder` | — |
| 3 — aulas | `lesson-planner` → `instructor-scriptwriter` → `portal-assembler` (re-dispatch on missing dep) · `estudo-dirigido`: `lesson-planner` → `demo-recorder` → (`lesson-planner` if `ajustar-fonte`) → `exercise-author` → `instructor-scriptwriter` → `guide-author` → `portal-assembler` | — |
| 4 — QA | `qa-reviewer` (with baseline path) | **HITL #2** — pause for human greenlight |

<!-- claude:ganchos:inicio -->
Hooks (`block-real-secret-prefixes`, `block-destructive-git`) = **guardrails**, fire automatically during agent execution, **not** HITL gates.
<!-- claude:ganchos:fim -->