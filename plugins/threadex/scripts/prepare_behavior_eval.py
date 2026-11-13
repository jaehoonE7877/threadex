#!/usr/bin/env python3
"""Prepare a blind behavior trial; this script does not judge model behavior."""

from __future__ import annotations

import argparse
import json
import shutil
import tomllib
from pathlib import Path, PurePosixPath


def load_cases(root: Path) -> list[dict]:
    data = json.loads((root / "smoke/behavior_cases.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("cases"), list):
        raise ValueError("behavior cases require schema_version 1 and a cases list")
    cases = data["cases"]
    seen = set()
    known_skills = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    for case in cases:
        case_id = case.get("id", "")
        if not isinstance(case_id, str) or not case_id or not all(
            char in "abcdefghijklmnopqrstuvwxyz0123456789_" for char in case_id
        ) or case_id in seen:
            raise ValueError("behavior case IDs must be unique snake_case names")
        seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError(f"{case_id}: missing prompt")
        checks = case.get("checks")
        if not isinstance(checks, list) or not checks or not all(
            isinstance(check, str) and check.strip() for check in checks
        ):
            raise ValueError(f"{case_id}: missing observable checks")
        skills = case.get("expected_skills")
        if not isinstance(skills, list) or not all(skill in known_skills for skill in skills):
            raise ValueError(f"{case_id}: unknown expected skill")
        files = case.get("files")
        if not isinstance(files, dict):
            raise ValueError(f"{case_id}: files must be an object")
        for name, content in files.items():
            path = PurePosixPath(name)
            if (not name or path.is_absolute() or ".." in path.parts
                    or "\\" in name or str(path) != name
                    or any(part.startswith(".") for part in path.parts)
                    or not isinstance(content, str)):
                raise ValueError(f"{case_id}: unsafe fixture path or content: {name}")
    if not cases:
        raise ValueError("at least one behavior case is required")
    return cases


def prepare(root: Path, case_id: str, output: Path) -> Path:
    root, output = root.resolve(), output.resolve()
    case = next((item for item in load_cases(root) if item["id"] == case_id), None)
    if case is None:
        raise ValueError(f"unknown case: {case_id}")
    if output == root or root in output.parents:
        raise ValueError("put evaluation artifacts outside the plugin package")
    # Never reuse a trial directory: previous output could bias or overwrite a run.
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / "workspace"
    workspace.mkdir()
    for name, content in case["files"].items():
        path = workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    skills = output / "skills"
    shutil.copytree(root / "skills", skills)
    catalog = []
    for path in sorted(skills.glob("*/SKILL.md")):
        description = next(line.split(":", 1)[1].strip() for line in
                           path.read_text(encoding="utf-8").splitlines()
                           if line.startswith("description:"))
        catalog.append(f"- $threadex:{path.parent.name}: {description} ({path})")
    agents = output / "agents"
    shutil.copytree(root / "codex/agents", agents)
    agent_catalog = []
    for path in sorted(agents.glob("*.toml")):
        contract = tomllib.loads(path.read_text(encoding="utf-8"))
        agent_catalog.append(f"- {contract['name']}: {contract['description']} ({path})")
    request = (
        f"Work only in {workspace}. Treat this as a real user task. "
        "Use the supplied skill catalog when a skill applies, reading its SKILL.md. "
        "The copied skills and agent contracts may be read but not modified. "
        "Do not inspect other trials or the source plugin's smoke cases. "
        "Do not use external services. Return the actual task result.\n\n"
        "Available skills:\n" + "\n".join(catalog) + "\n\n"
        "Optional agent contracts:\n" + "\n".join(agent_catalog) + "\n\n"
        "These files do not install or register custom roles. When delegation is warranted "
        "and available, give a fresh-context agent the matching copied contract and a bounded "
        "task within this workspace. The child must read and follow that contract. "
        "Do not assume a preinstalled role uses this copy. If delegation is unavailable, "
        "follow the skill's fallback and disclose the limitation.\n\n"
        "User request:\n" + case["prompt"] + "\n"
    )
    (output / "request.md").write_text(request, encoding="utf-8")
    return output / "request.md"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="case ID from smoke/behavior_cases.json")
    parser.add_argument("output", type=Path, help="new directory outside the package")
    parser.add_argument("--plugin", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(prepare(args.plugin, args.case, args.output))
    except (ValueError, FileExistsError) as error:
        parser.exit(1, f"behavior trial preparation failed: {error}\n")


if __name__ == "__main__":
    main()
