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
EXPECTED_AGENT_CONFIGS = {
    "code-explorer": {"model": "gpt-5.6-terra", "effort": "low"},
    "docs-researcher": {"model": "gpt-5.6-terra", "effort": "low"},
    "gap-auditor": {"model": "gpt-5.6-sol", "effort": "high"},
    "verifier": {"model": "gpt-5.6-sol", "effort": "high"},
    "code-reviewer": {"model": "gpt-5.6-sol", "effort": "high"},
}
EXPECTED_ROUTE_PAIRS = {
    ("clarify", "gap-auditor"),
    ("specify", "gap-auditor"),
    ("verify", "verifier"),
    ("review", "code-reviewer"),
    ("compound", "docs-researcher"),
}
EXPECTED_SKILL_AGENTS = {
    "clarify": {"code-explorer", "docs-researcher", "gap-auditor"},
    "specify": {"code-explorer", "docs-researcher", "gap-auditor"},
    "goal-draft": set(),
    "verify": {"verifier"},
    "review": {"code-reviewer"},
    "compound": {"docs-researcher"},
}


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
    skill_cases = smoke.get("skills", [])
    agent_cases = smoke.get("subagents", [])
    routes = smoke.get("routing", [])

    skill_names = [case.get("name") for case in skill_cases]
    if len(skill_names) != len(set(skill_names)):
        fail("smoke skill names must be unique")
    if set(skill_names) != set(REQUIRED_SKILLS):
        fail("smoke skills must exactly match the required skill set")

    agent_names = [case.get("name") for case in agent_cases]
    if len(agent_names) != len(set(agent_names)):
        fail("smoke subagent names must be unique")
    if set(agent_names) != set(REQUIRED_AGENTS):
        fail("smoke subagents must exactly match the required agent set")

    smoke_skills = {case["name"]: case for case in skill_cases}
    smoke_agents = {case["name"]: case for case in agent_cases}

    route_pairs = {(route.get("skill"), route.get("agent")) for route in routes}
    if len(route_pairs) != len(routes):
        fail("smoke routing pairs must be unique")
    if route_pairs != EXPECTED_ROUTE_PAIRS:
        fail("smoke routing must exactly match the Threadex skill-agent routes")

    for skill in REQUIRED_SKILLS:
        skill_path = root / "skills" / skill / "SKILL.md"
        text = read(skill_path)
        fields = parse_frontmatter(text, skill_path)
        if fields.get("name") != skill:
            fail(f"{skill_path} frontmatter name must be {skill}")
        desc = fields.get("description", "")
        if not desc.startswith("Use when"):
            fail(f"{skill} description must start with 'Use when'")
        if len(desc) > 240:
            fail(f"{skill} description is too long for reliable trigger matching")
        metadata_path = root / "skills" / skill / "agents" / "openai.yaml"
        metadata = read(metadata_path)
        if not re.search(r"(?m)^\s*allow_implicit_invocation:\s*true\s*$", metadata):
            fail(f"{skill} metadata must allow implicit invocation")
        default_prompt_line = next(
            (
                line.strip()
                for line in metadata.splitlines()
                if line.strip().startswith("default_prompt:")
            ),
            None,
        )
        if default_prompt_line is None:
            fail(f"{skill} metadata must define default_prompt")
        default_prompt = default_prompt_line.split(":", 1)[1].strip().strip('"\'')
        invocation_pattern = rf"(?<![A-Za-z0-9_:-])\$threadex:{re.escape(skill)}(?![A-Za-z0-9_-])"
        if not re.search(invocation_pattern, default_prompt):
            fail(f"{skill} metadata default prompt must use its namespaced invocation")

        case = smoke_skills[skill]
        for field in ["explicit", "natural", "expected_output"]:
            value = case.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(f"{skill} smoke field {field} must be a non-empty string")
        required_terms = case.get("required_terms")
        if not isinstance(required_terms, list) or not required_terms:
            fail(f"{skill} smoke case must include required_terms")
        for term in required_terms:
            if not isinstance(term, str) or not term:
                fail(f"{skill} required_terms must contain non-empty strings")
            if term not in text:
                fail(f"{skill} is missing smoke contract term: {term}")
        explicit = case["explicit"]
        if not re.match(rf"^\$threadex:{re.escape(skill)}(?:\s|$)", explicit):
            fail(f"{skill} explicit smoke must use $threadex:{skill}")
        expected_agents = case.get("expected_agents")
        if not isinstance(expected_agents, list):
            fail(f"{skill} expected_agents must be a list")
        if len(expected_agents) != len(set(expected_agents)):
            fail(f"{skill} expected_agents must be unique")
        if set(expected_agents) != EXPECTED_SKILL_AGENTS[skill]:
            fail(f"{skill} expected_agents do not match the skill contract")
        for agent in expected_agents:
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
        expected = EXPECTED_AGENT_CONFIGS[agent]
        if data.get("model") != expected["model"]:
            fail(f"{agent} model must be {expected['model']}")
        if data.get("model_reasoning_effort") != expected["effort"]:
            fail(f"{agent} reasoning effort must be {expected['effort']}")

        case = smoke_agents[agent]
        spawn_smoke = case.get("spawn_smoke")
        if not isinstance(spawn_smoke, str) or not spawn_smoke.strip():
            fail(f"{agent} spawn_smoke must be a non-empty string")
        required_terms = case.get("required_terms")
        if not isinstance(required_terms, list) or not required_terms:
            fail(f"{agent} smoke case must include required_terms")
        for term in required_terms:
            if not isinstance(term, str) or not term:
                fail(f"{agent} required_terms must contain non-empty strings")
            if term not in instructions:
                fail(f"{agent} is missing smoke contract term: {term}")

    for route in routes:
        handoff = route.get("handoff")
        if not isinstance(handoff, str) or not handoff.strip():
            fail(f"routing {route.get('skill')} -> {route.get('agent')} needs a handoff")
        skill_text = read(root / "skills" / route["skill"] / "SKILL.md")
        if route["agent"] not in skill_text:
            fail(f"routing {route['skill']} -> {route['agent']} not documented in skill")

    for support_file in [
        root / "skills" / "compound" / "references" / "problem-types.md",
        root / "skills" / "compound" / "references" / "persistence-schema.md",
        root / "skills" / "compound" / "templates" / "LEARNING_TEMPLATE.md",
    ]:
        read(support_file)

    for ref_name in ["domain_defaults.md", "slot_checklist.md", "style_overlay.md"]:
        read(root / "skills" / "goal-draft" / "references" / ref_name)

    print("Threadex validation passed")


if __name__ == "__main__":
    main()
