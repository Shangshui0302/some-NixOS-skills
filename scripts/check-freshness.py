#!/usr/bin/env python3
"""Report locked-input and documentation-review freshness without editing files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


UTC = dt.timezone.utc


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def locked_inputs(lock: dict, names: set[str], label: str) -> dict[str, dict]:
    nodes = lock.get("nodes")
    if not isinstance(nodes, dict):
        raise ValueError(f"{label} has no nodes object")

    result = {}
    for name in sorted(names):
        node = nodes.get(name)
        if not isinstance(node, dict) or not isinstance(node.get("locked"), dict):
            raise ValueError(f"{label} is missing locked input {name!r}")
        locked = node["locked"]
        revision = locked.get("rev")
        if not isinstance(revision, str) or not revision:
            raise ValueError(f"{label} input {name!r} has no locked revision")
        result[name] = {
            "rev": revision,
            "narHash": locked.get("narHash"),
            "lastModified": locked.get("lastModified"),
            "type": locked.get("type"),
            "owner": locked.get("owner"),
            "repo": locked.get("repo"),
        }
    return result


def as_date(value: str, label: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be YYYY-MM-DD: {value!r}") from error


def validate_manifest(root: Path, manifest: dict, today: dt.date) -> tuple[list[dict], set[str]]:
    if manifest.get("schema") != 1:
        raise ValueError("freshness manifest schema must be 1")
    default_interval = manifest.get("default_review_interval_days", 30)
    if not isinstance(default_interval, int) or default_interval < 1:
        raise ValueError("default_review_interval_days must be a positive integer")

    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("freshness manifest must contain a non-empty sources list")

    root = root.resolve()
    reports = []
    inputs = set()
    ids = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each freshness source must be an object")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id or source_id in ids:
            raise ValueError(f"source id must be unique and non-empty: {source_id!r}")
        ids.add(source_id)

        url = source.get("url")
        parsed_url = urlparse(url) if isinstance(url, str) else None
        if parsed_url is None or parsed_url.scheme != "https" or not parsed_url.netloc:
            raise ValueError(f"{source_id}: url must be an HTTPS URL")

        reviewed = as_date(source.get("last_reviewed", ""), f"{source_id}.last_reviewed")
        interval = source.get("review_interval_days", default_interval)
        if not isinstance(interval, int) or interval < 1:
            raise ValueError(f"{source_id}.review_interval_days must be positive")

        references = source.get("references", [])
        if not isinstance(references, list) or not all(isinstance(item, str) for item in references):
            raise ValueError(f"{source_id}.references must be a string list")
        for reference in references:
            path = (root / reference).resolve()
            try:
                path.relative_to(root)
            except ValueError as error:
                raise ValueError(f"{source_id}: reference escapes repository: {reference}") from error
            if not path.is_file():
                raise ValueError(f"{source_id}: missing reference: {reference}")

        input_name = source.get("input")
        if input_name is not None:
            if not isinstance(input_name, str) or not input_name:
                raise ValueError(f"{source_id}.input must be a non-empty string")
            inputs.add(input_name)

        due_on = reviewed + dt.timedelta(days=interval)
        reports.append(
            {
                "id": source_id,
                "url": url,
                "input": input_name,
                "last_reviewed": reviewed.isoformat(),
                "review_due": due_on.isoformat(),
                "due": today >= due_on,
                "references": references,
            }
        )
    return reports, inputs


def build_report(root: Path, lock_path: Path, manifest_path: Path, candidate_path: Path | None) -> dict:
    today = dt.datetime.now(UTC).date()
    manifest = load_json(manifest_path)
    source_reports, input_names = validate_manifest(root, manifest, today)
    current_lock = load_json(lock_path)
    current_inputs = locked_inputs(current_lock, input_names, "current lock")

    candidate_inputs = None
    input_drift = []
    if candidate_path is not None:
        candidate_lock = load_json(candidate_path)
        candidate_inputs = locked_inputs(candidate_lock, input_names, "candidate lock")
        for name in sorted(input_names):
            old = current_inputs[name]
            new = candidate_inputs[name]
            if old != new:
                input_drift.append(
                    {
                        "input": name,
                        "current": old,
                        "candidate": new,
                    }
                )

    attention = bool(input_drift) or any(source["due"] for source in source_reports)
    return {
        "schema": 1,
        "generated_at": dt.datetime.now(UTC).isoformat(),
        "status": "attention" if attention else "current",
        "current_lock": str(lock_path),
        "inputs": current_inputs,
        "candidate_lock": str(candidate_path) if candidate_path else None,
        "candidate_inputs": candidate_inputs,
        "input_drift": input_drift,
        "sources": source_reports,
    }


def render_human(report: dict) -> str:
    lines = [f"freshness status: {report['status']}"]
    for name, value in report["inputs"].items():
        modified = value.get("lastModified")
        modified_text = (
            dt.datetime.fromtimestamp(modified, UTC).isoformat() if isinstance(modified, int) else "unknown"
        )
        lines.append(f"locked input {name}: {value['rev']} ({modified_text})")
    for drift in report["input_drift"]:
        lines.append(
            f"input drift {drift['input']}: {drift['current']['rev']} -> {drift['candidate']['rev']}"
        )
    for source in report["sources"]:
        state = "due" if source["due"] else "ok"
        lines.append(
            f"documentation {source['id']}: {state}; reviewed {source['last_reviewed']}; "
            f"next review {source['review_due']}; {source['url']}"
        )
    return "\n".join(lines)


def append_github_summary(path: Path, report: dict) -> None:
    lines = ["## Freshness report", "", f"- Status: `{report['status']}`"]
    for name, value in report["inputs"].items():
        lines.append(f"- Locked `{name}`: `{value['rev']}`")
    for drift in report["input_drift"]:
        lines.append(
            f"- Candidate `{drift['input']}`: `{drift['current']['rev']}` -> `{drift['candidate']['rev']}`"
        )
    for source in report["sources"]:
        marker = "review due" if source["due"] else "review current"
        lines.append(f"- `{source['id']}`: {marker}; {source['url']}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--lock", type=Path, help="current flake.lock (default: ROOT/flake.lock)")
    parser.add_argument("--manifest", type=Path, help="freshness manifest (default: ROOT/docs/freshness-sources.json)")
    parser.add_argument("--candidate-lock", type=Path, help="optional lock generated by nix flake update")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    parser.add_argument("--github-summary", type=Path, help="append a compact report to a GitHub Actions summary")
    parser.add_argument("--fail-on-attention", action="store_true", help="exit 2 when drift or review due is found")
    parser.add_argument("--fail-on-due", action="store_true", help="exit 2 only when a documentation review is due")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    lock_path = (args.lock or root / "flake.lock").resolve()
    manifest_path = (args.manifest or root / "docs/freshness-sources.json").resolve()
    candidate_path = args.candidate_lock.resolve() if args.candidate_lock else None
    try:
        report = build_report(root, lock_path, manifest_path, candidate_path)
    except ValueError as error:
        print(f"freshness error: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_human(report))
    if args.github_summary:
        append_github_summary(args.github_summary, report)
    if args.fail_on_attention and report["status"] != "current":
        return 2
    if args.fail_on_due and any(source["due"] for source in report["sources"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
