#!/usr/bin/env python3
"""Static smoke checks for the Threadex plugin package."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path


REQUIRED_SKILLS = ["clarify", "specify", "goal-draft", "verify", "review", "compound"]
REQUIRED_AGENTS = [
    "code-explorer",
    "docs-researcher",
    "gap-auditor",
    "verifier",
    "code-reviewer",
]
EXPECTED_AGENT_MODELS = {
    "code-explorer": "gpt-5.4-mini",
    "docs-researcher": "gpt-5.4-mini",
    "gap-auditor": "gpt-5.5",
    "verifier": "gpt-5.5",
    "code-reviewer": "gpt-5.5",
}
COMPOUND_REQUIRED_TERMS = [
    ".threadex/learnings/ledger.json",
    ".threadex/learnings/index.json",
    "docs/learnings/{YYYY-MM-DD}-{short-title}.md",
    "source",
    "human_doc",
    "problem",
    "cause",
    "rule",
    "evidence",
    "tags",
    "created_at",
    "Next specify defaults",
]
SPECIFY_REQUIRED_LEARNING_TERMS = [
    ".threadex/learnings/index.json",
    ".threadex/learnings/ledger.json",
    "human_doc",
    "Prior Learnings Applied",
]
CLARIFY_REQUIRED_BOUNDARY_TERMS = [
    "Decision progress",
    "remaining decision axes",
    "Sufficient for specify",
    "Do not draft requirements",
]
SPECIFY_REQUIRED_OPEN_DECISION_TERMS = [
    "Blocking",
    "Non-blocking defaults",
    "before `goal-draft` or implementation",
]
COMPOUND_REQUIRED_CONVENTION_TERMS = [
    "local naming conventions",
    "AGENTS.md",
    "nearby `docs/learnings/` filenames",
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


def parse_semver(value: str | None, label: str) -> tuple[int, int, int]:
    if value is None:
        fail(f"{label} is missing")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if not match:
        fail(f"{label} must be a semver like 0.3.6")
    return tuple(int(part) for part in match.groups())


def git_output(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def tag_version(tag: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def validate_manifest_version(root: Path, version: str) -> None:
    manifest_semver = parse_semver(version, "manifest version")

    expected_version = os.environ.get("THREADEX_RELEASE_VERSION")
    if expected_version:
        expected_semver = parse_semver(expected_version, "THREADEX_RELEASE_VERSION")
        if manifest_semver != expected_semver:
            fail(
                "manifest version must match THREADEX_RELEASE_VERSION "
                f"({version} != {expected_version})"
            )

    latest_tags = git_output(root, "tag", "--list", "v[0-9]*")
    tag_versions = [
        parsed
        for tag in (latest_tags or "").splitlines()
        if (parsed := tag_version(tag)) is not None
    ]
    if tag_versions and manifest_semver < max(tag_versions):
        latest = ".".join(str(part) for part in max(tag_versions))
        fail(f"manifest version {version} is older than latest git tag v{latest}")

    head_tags = git_output(root, "tag", "--points-at", "HEAD")
    head_versions = [
        parsed
        for tag in (head_tags or "").splitlines()
        if (parsed := tag_version(tag)) is not None
    ]
    worktree_status = git_output(root, "status", "--porcelain")
    worktree_is_clean = worktree_status == ""
    if head_versions and worktree_is_clean and manifest_semver != max(head_versions):
        head_version = ".".join(str(part) for part in max(head_versions))
        fail(f"manifest version {version} must match HEAD release tag v{head_version}")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    manifest = json.loads(read(root / ".codex-plugin" / "plugin.json"))
    if manifest.get("name") != "threadex":
        fail("plugin name must be threadex")
    validate_manifest_version(root, manifest.get("version"))
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
        if skill != "goal-draft" and "## Subagent Handoff" not in text:
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
        if data.get("sandbox_mode") != "read-only":
            fail(f"{agent} must use read-only sandbox_mode")
        if data.get("model") != EXPECTED_AGENT_MODELS[agent]:
            fail(f"{agent} model must be {EXPECTED_AGENT_MODELS[agent]}")
        if agent not in smoke_agents:
            fail(f"{agent} missing subagent smoke case")

    for route in smoke["routing"]:
        skill_text = read(root / "skills" / route["skill"] / "SKILL.md")
        if route["agent"] not in skill_text:
            fail(f"routing {route['skill']} -> {route['agent']} not documented in skill")

    compound_text = read(root / "skills" / "compound" / "SKILL.md")
    for required in COMPOUND_REQUIRED_TERMS:
        if required not in compound_text:
            fail(f"compound is missing learning pipeline contract: {required}")
    for required in COMPOUND_REQUIRED_CONVENTION_TERMS:
        if required not in compound_text:
            fail(f"compound is missing local convention contract: {required}")
    for support_file in [
        root / "skills" / "compound" / "references" / "problem-types.md",
        root / "skills" / "compound" / "templates" / "LEARNING_TEMPLATE.md",
    ]:
        if not support_file.exists():
            fail(f"compound missing support file: {support_file.name}")

    clarify_text = read(root / "skills" / "clarify" / "SKILL.md")
    for required in CLARIFY_REQUIRED_BOUNDARY_TERMS:
        if required not in clarify_text:
            fail(f"clarify is missing boundary/progress contract: {required}")

    specify_text = read(root / "skills" / "specify" / "SKILL.md")
    for required in SPECIFY_REQUIRED_LEARNING_TERMS:
        if required not in specify_text:
            fail(f"specify is missing learning reuse contract: {required}")
    for required in SPECIFY_REQUIRED_OPEN_DECISION_TERMS:
        if required not in specify_text:
            fail(f"specify is missing open decision handoff contract: {required}")

    goal_text = read(root / "skills" / "goal-draft" / "SKILL.md")
    if "4000" not in goal_text:
        fail("goal-draft skill must enforce the 4000 character limit")
    if "name: draft-codex-goal" in goal_text:
        fail("goal-draft must keep the skill name as goal-draft")
    if "# Draft Codex Goal" not in goal_text:
        fail("goal-draft must preserve the copied draft-codex-goal content")
    for required in [
        "Six-Slot Contract",
        "Domain Routing",
        "Clarifying Questions",
        "Drafting Rules",
        "references/domain_defaults.md",
        "references/slot_checklist.md",
        "references/style_overlay.md",
    ]:
        if required not in goal_text:
            fail(f"goal-draft is missing draft-codex-goal contract: {required}")
    for ref_name in ["domain_defaults.md", "slot_checklist.md", "style_overlay.md"]:
        if not (root / "skills" / "goal-draft" / "references" / ref_name).exists():
            fail(f"goal-draft missing reference file: {ref_name}")

    print("Threadex validation passed")


if __name__ == "__main__":
    main()
