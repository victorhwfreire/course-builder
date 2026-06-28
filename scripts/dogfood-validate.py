#!/usr/bin/env python3
"""Structural dogfood validation for the course-builder plugin.

Checks (no live agent dispatch):
  1. Example spec validates against schemas/module.spec.schema.json.
  2. Every agents/*.md has valid YAML frontmatter with name, description, tools.
  3. commands/build-module.md references all 9 agent names and no phantom ones.
  4. Skill names referenced by agents (cesar-html-style, first-person-roteiro)
     resolve to skills/<name>/SKILL.md.
  5. Hook scripts referenced by settings.json.example exist.

Exit code 0 = all checks pass, !=0 = failures found.
"""
import sys, re, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures = []
warnings = []

def fail(msg): failures.append(msg)
def warn(msg): warnings.append(msg)

# --- 1. Schema validation -------------------------------------------------
try:
    import yaml
    import jsonschema
except ImportError as e:
    fail(f"missing python dep: {e}")
    yaml = None

if yaml:
    schema_path = ROOT / "schemas" / "module.spec.schema.json"
    spec_path = ROOT / "examples" / "module-spec.ia-devs-mod3.yaml"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(spec)
        print(f"[OK] schema: example spec validates against {schema_path.name}")
    except jsonschema.ValidationError as e:
        fail(f"schema: example spec FAILS — {e.message} (at {list(e.absolute_path)})")
    except Exception as e:
        fail(f"schema: could not validate — {e}")

# --- 2. Agent frontmatter -------------------------------------------------
EXPECTED_AGENTS = [
    "trend-researcher", "ementa-architect", "repo-scaffolder", "bug-smith",
    "exercise-author", "lesson-planner", "instructor-scriptwriter",
    "portal-assembler", "qa-reviewer",
]
agent_dir = ROOT / "agents"
found_agents = []
for md in sorted(agent_dir.glob("*.md")):
    name = md.stem
    found_agents.append(name)
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        fail(f"agent {name}: no YAML frontmatter block")
        continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        fail(f"agent {name}: frontmatter not parseable — {e}")
        continue
    missing = [f for f in ("name", "description", "tools") if f not in fm or not fm[f]]
    if missing:
        fail(f"agent {name}: frontmatter missing/empty {missing}")
        continue
    if fm["name"] != name:
        warn(f"agent {name}: frontmatter name={fm['name']!r} != filename stem")
    # Claude Code accepts `tools` as either a YAML list or a comma-separated
    # string (the canonical CC form, e.g. `tools: Read, Write, Glob, Grep`).
    # Normalize both to a list of tool names.
    tools = fm["tools"]
    if isinstance(tools, str):
        tools_list = [t.strip() for t in tools.split(",") if t.strip()]
    elif isinstance(tools, list):
        tools_list = [str(t).strip() for t in tools if t]
    else:
        fail(f"agent {name}: 'tools' is neither list nor string "
             f"(got {type(tools).__name__})")
        continue
    if not tools_list:
        fail(f"agent {name}: 'tools' parsed to empty list — would grant NO tools")
        continue
    # The classic trap: omitting `tools` grants ALL tools. A single literal
    # '*' or the word 'all' is suspicious.
    if tools_list == ["*"] or tools_list == ["all"]:
        warn(f"agent {name}: 'tools' is wildcard — grants ALL tools (the omit-trap)")
    print(f"[OK] agent {name}: frontmatter valid (tools: {tools_list})")

missing_agents = set(EXPECTED_AGENTS) - set(found_agents)
extra_agents = set(found_agents) - set(EXPECTED_AGENTS)
if missing_agents:
    fail(f"agents: missing expected agent files: {sorted(missing_agents)}")
if extra_agents:
    warn(f"agents: unexpected extra agent files: {sorted(extra_agents)}")

# --- 3. Command cross-references ------------------------------------------
cmd_path = ROOT / "commands" / "build-module.md"
if cmd_path.exists():
    cmd_text = cmd_path.read_text(encoding="utf-8")
    referenced = set()
    for name in EXPECTED_AGENTS:
        # look for the agent name as a token (in backticks, or plain)
        if re.search(rf"\b{re.escape(name)}\b", cmd_text):
            referenced.add(name)
    not_ref = set(EXPECTED_AGENTS) - referenced
    if not_ref:
        fail(f"command: does not reference agents: {sorted(not_ref)}")
    print(f"[OK] command: references {len(referenced)}/9 agents")
else:
    fail("command: commands/build-module.md missing")

# --- 4. Skill references resolve ------------------------------------------
SKILLS_REFERENCED = {"cesar-html-style", "first-person-roteiro"}
for skill in SKILLS_REFERENCED:
    sk = ROOT / "skills" / skill / "SKILL.md"
    if not sk.exists():
        fail(f"skill {skill}: SKILL.md missing at {sk}")
    else:
        # check the skill name frontmatter matches
        t = sk.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", t, re.DOTALL)
        if m:
            try:
                sfm = yaml.safe_load(m.group(1))
                if sfm.get("name") != skill:
                    warn(f"skill {skill}: frontmatter name={sfm.get('name')!r}")
                else:
                    print(f"[OK] skill {skill}: SKILL.md present, name matches")
            except Exception as e:
                warn(f"skill {skill}: frontmatter not parseable — {e}")
        else:
            warn(f"skill {skill}: no frontmatter block")

# cross-check: agents that list 'Skill' in tools should reference a real skill
skill_tool_agents = []
for md in sorted(agent_dir.glob("*.md")):
    t = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.DOTALL)
    if not m: continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception:
        continue
    tools = fm.get("tools", [])
    if isinstance(tools, str):
        tools = [t.strip() for t in tools.split(",") if t.strip()]
    if isinstance(tools, list) and "Skill" in tools:
        skill_tool_agents.append(md.stem)
print(f"[INFO] agents with Skill tool: {skill_tool_agents}")
for a in skill_tool_agents:
    body = (agent_dir / f"{a}.md").read_text(encoding="utf-8")
    refs = [s for s in SKILLS_REFERENCED if s in body]
    if not refs:
        warn(f"agent {a}: has 'Skill' in tools but references no known skill "
             f"({sorted(SKILLS_REFERENCED)}) in its body")

# --- 5. Hook scripts exist + settings.json.example refs -------------------
settings_path = ROOT / "settings.json.example"
if settings_path.exists():
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"settings.json.example: not valid JSON — {e}")
        settings = {}
    # collect referenced script paths
    refs = set()
    raw = settings_path.read_text(encoding="utf-8")
    for m in re.finditer(r"hooks/scripts/[\w.-]+\.sh", raw):
        refs.add(m.group(0))
    for r in sorted(refs):
        p = ROOT / r
        if not p.exists():
            fail(f"hook script referenced in settings.json.example not found: {r}")
        else:
            print(f"[OK] hook script exists: {r}")
else:
    fail("settings.json.example missing")

# --- plugin.json sanity ---------------------------------------------------
pj = ROOT / ".claude-plugin" / "plugin.json"
try:
    plugin = json.loads(pj.read_text(encoding="utf-8"))
    for key in ("commands", "agents", "skills", "hooks"):
        if key not in plugin:
            warn(f"plugin.json: missing '{key}' pointer")
    print(f"[OK] plugin.json valid (name={plugin.get('name')}, "
          f"version={plugin.get('version')})")
except Exception as e:
    fail(f"plugin.json: invalid — {e}")

# --- report ---------------------------------------------------------------
print("\n" + "=" * 60)
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
if failures:
    print(f"FAILURES ({len(failures)}):")
    for f in failures:
        print(f"  - {f}")
    print(f"\nDOGFOOD: {len(failures)} failure(s), {len(warnings)} warning(s)")
    sys.exit(1)
print(f"\nDOGFOOD: PASS — 0 failures, {len(warnings)} warning(s)")
sys.exit(0)