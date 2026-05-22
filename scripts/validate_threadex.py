#!/usr/bin/env python3
"""Static smoke checks for the Threadex plugin package."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


REQUIRED_SKILLS = ["clarify", "specify", "goal-draft", "verify", "review", "compound"]
REQUIRED_AGENTS = [
    "code-explorer",
    "docs-researcher",
    "gap-auditor",
    "worker",
    "verifier",
    "code-reviewer",
]
FORBIDDEN_CALL_PATTERNS = [
    r"\$hoyeon[-\w]*",
    r"(?<!team-attention)/hoyeon[-\w]*",
    r"name\s*=\s*['\"]hoyeon-",
    r"^name:\s*hoyeon-",
]


def fail(message: str) -> None:
    raise SystemExit(f"threadex validation failed: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing {path}")
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(f"{path} is missing YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    manifest = json.loads(read(root / ".codex-plugin" / "plugin.json"))
    if manifest.get("name") != "threadex":
        fail("plugin name must be threadex")
    if manifest.get("skills") != "./skills/":
        fail("manifest skills path must be ./skills/")
    if manifest.get("repository") != "https://github.com/jaehoonE7877/threadex":
        fail("repository metadata must point to jaehoonE7877/threadex")

    smoke = json.loads(read(root / "smoke" / "smoke_cases.json"))
    smoke_skills = {case["name"]: case for case in smoke["skills"]}
    smoke_agents = {case["name"]: case for case in smoke["subagents"]}

    for skill in REQUIRED_SKILLS:
        skill_path = root / "skills" / skill / "SKILL.md"
        text = read(skill_path)
        fields = parse_frontmatter(text, skill_path)
        if fields.get("name") != skill:
            fail(f"{skill_path} frontmatter name must be {skill}")
        desc = fields.get("description", "")
        if not desc.startswith("Use when"):
            fail(f"{skill} description must start with 'Use when'")
        if len(desc) > 700:
            fail(f"{skill} description is too long for reliable trigger matching")
        if "## Subagent Handoff" not in text:
            fail(f"{skill} must document Subagent Handoff")
        if not (root / "skills" / skill / "agents" / "openai.yaml").exists():
            fail(f"{skill} is missing agents/openai.yaml metadata")
        if skill not in smoke_skills:
            fail(f"{skill} missing smoke case")
        for agent in smoke_skills[skill]["expected_agents"]:
            if agent not in text:
                fail(f"{skill} smoke expects {agent}, but SKILL.md does not mention it")

    for agent in REQUIRED_AGENTS:
        agent_path = root / "codex" / "agents" / f"{agent}.toml"
        data = tomllib.loads(read(agent_path))
        if data.get("name") != agent:
            fail(f"{agent_path} name must be {agent}")
        instructions = data.get("developer_instructions", "")
        if "Contract:" not in instructions:
            fail(f"{agent} must include an explicit contract")
        if agent not in smoke_agents:
            fail(f"{agent} missing subagent smoke case")

    for route in smoke["routing"]:
        skill_text = read(root / "skills" / route["skill"] / "SKILL.md")
        if route["agent"] not in skill_text:
            fail(f"routing {route['skill']} -> {route['agent']} not documented in skill")

    all_text = "\n".join(
        p.read_text(encoding="utf-8")
        for p in root.rglob("*")
        if p.is_file()
        and ".git" not in p.parts
        and p.name != "validate_threadex.py"
        and p.suffix in {".md", ".json", ".toml", ".yaml"}
    )
    for pattern in FORBIDDEN_CALL_PATTERNS:
        if re.search(pattern, all_text, re.M):
            fail(f"forbidden copied Hoyeon invocation or adapter name found: {pattern}")

    goal_text = read(root / "skills" / "goal-draft" / "SKILL.md")
    if "4000" not in goal_text:
        fail("goal-draft skill must enforce the 4000 character limit")
    if "does not implement or replace `/goal`" not in goal_text:
        fail("goal-draft must state that /goal is a built-in Codex feature")

    print("Threadex validation passed")


if __name__ == "__main__":
    main()
