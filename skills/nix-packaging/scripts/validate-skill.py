#!/usr/bin/env python3
"""Small, dependency-free structural check for this skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "## Progress checklist",
    "## Freshness gate",
    "## Validation",
    "## Anti-patterns",
    "## Delivery format",
)


def error(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    root = args.skill_dir.resolve()
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        error(f"missing {skill_file}")
        return 1

    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    failures: list[str] = []

    if len(lines) > 500:
        failures.append(f"SKILL.md has {len(lines)} lines; limit is 500")
    if not text.startswith("---\n"):
        failures.append("SKILL.md must start with YAML frontmatter")
    else:
        marker = text.find("\n---\n", 4)
        if marker < 0:
            failures.append("frontmatter is not closed")
        else:
            frontmatter = text[4:marker]
            if not re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE):
                failures.append("frontmatter is missing name")
            if not re.search(r"^description:\s*", frontmatter, re.MULTILINE):
                failures.append("frontmatter is missing description")

    if "[TODO" in text or "[todo" in text.lower():
        failures.append("placeholder TODO remains")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            failures.append(f"missing required section: {heading}")

    for relative in re.findall(r"(?:references|scripts)/[A-Za-z0-9._/-]+", text):
        candidate = root / relative.rstrip("`'.,)")
        if not candidate.exists():
            failures.append(f"referenced path does not exist: {relative}")

    evals_file = root / "evals" / "evals.json"
    if not evals_file.is_file():
        failures.append("missing evals/evals.json")
    else:
        try:
            payload = json.loads(evals_file.read_text(encoding="utf-8"))
            cases = payload.get("cases")
            if not isinstance(cases, list) or len(cases) < 3:
                failures.append("evals.json must contain at least three cases")
            else:
                for index, case in enumerate(cases):
                    if not isinstance(case, dict) or not case.get("id") or not case.get("prompt"):
                        failures.append(f"eval case {index} needs id and prompt")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"cannot parse evals/evals.json: {exc}")

    if failures:
        for failure in failures:
            error(failure)
        return 1

    print(f"ok: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
