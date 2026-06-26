#!/usr/bin/env python3
"""Deterministic visual-quality lint for Agent Design outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TEXT_EXTENSIONS = {
    ".astro",
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".mdx",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
}

SEVERITY_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    severity: str
    pattern: re.Pattern[str]
    message: str


@dataclass
class Finding:
    file: str
    line: int
    rule_id: str
    severity: str
    message: str
    excerpt: str


RULES = [
    Rule(
        "dead-anchor",
        "high",
        re.compile(r"""href\s*=\s*["']#["']""", re.I),
        "Replace dead href=\"#\" links with real destinations or disabled states.",
    ),
    Rule(
        "missing-img-alt",
        "high",
        re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.I),
        "Meaningful images need alt text.",
    ),
    Rule(
        "viewport-height",
        "high",
        re.compile(r"\bh-screen\b|height\s*:\s*100vh\b", re.I),
        "Use min-height: 100dvh for viewport sections to avoid mobile viewport jumps.",
    ),
    Rule(
        "window-alert",
        "high",
        re.compile(r"\bwindow\.alert\s*\(|\balert\s*\(", re.I),
        "Use inline, contextual error or success states instead of alert dialogs.",
    ),
    Rule(
        "z-index-max",
        "medium",
        re.compile(r"\bz-\[?9999\]?|z-index\s*:\s*9999\b", re.I),
        "Use a small z-index scale instead of arbitrary 9999 values.",
    ),
    Rule(
        "ai-purple-gradient",
        "medium",
        re.compile(
            r"from-(purple|violet|fuchsia)[-\w/:\[\]]*\s+to-(blue|cyan|indigo)|"
            r"#(7c3aed|8b5cf6|9333ea|a855f7|6366f1)\b|"
            r"\b(purple|violet)-[5-9]00\b",
            re.I,
        ),
        "Check whether purple/blue AI gradients are intentional brand choices.",
    ),
    Rule(
        "generic-copy",
        "medium",
        re.compile(
            r"\b(elevate|unleash|next-gen|game-chang(?:er|ing)|delve|tapestry|"
            r"seamless|powerful solution|transformative platform)\b",
            re.I,
        ),
        "Replace generic AI copy with specific product language.",
    ),
    Rule(
        "placeholder-names",
        "medium",
        re.compile(r"\b(Acme|Jane Doe|John Doe|Lorem ipsum|Nexus|NovaCore|SmartFlow)\b", re.I),
        "Replace placeholder names and Latin copy with believable content.",
    ),
    Rule(
        "three-card-default",
        "medium",
        re.compile(r"\b(grid-cols-3|md:grid-cols-3|lg:grid-cols-3)\b", re.I),
        "Three equal columns can be generic. Confirm the layout is deliberate.",
    ),
    Rule(
        "dead-button",
        "medium",
        re.compile(r"<button\b(?![^>]*type=)", re.I),
        "Buttons should usually declare type to avoid accidental form submits.",
    ),
    Rule(
        "external-font-link",
        "low",
        re.compile(r"fonts\.googleapis\.com|fonts\.gstatic\.com", re.I),
        "Prefer self-hosted fonts or framework font loaders for production.",
    ),
    Rule(
        "inter-default",
        "low",
        re.compile(r"\bInter\b", re.I),
        "Inter is fine when intentional, but avoid using it as an unexamined default.",
    ),
]


def iter_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix.lower() in TEXT_EXTENSIONS:
            yield target
        return

    for path in target.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            if any(part in {"node_modules", ".git", "dist", "build", ".next"} for part in path.parts):
                continue
            yield path


def scan_file(path: Path, root: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")

    findings: list[Finding] = []
    line_starts = [0]
    for match in re.finditer("\n", text):
        line_starts.append(match.end())

    for rule in RULES:
        for match in rule.pattern.finditer(text):
            line = 1
            for idx, start in enumerate(line_starts):
                if start > match.start():
                    break
                line = idx + 1
            line_text = text.splitlines()[line - 1].strip() if text.splitlines() else ""
            findings.append(
                Finding(
                    file=str(path.relative_to(root)),
                    line=line,
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    message=rule.message,
                    excerpt=line_text[:180],
                )
            )
    return findings


def summarize(findings: list[Finding]) -> dict[str, int]:
    counts = {"high": 0, "medium": 0, "low": 0}
    for finding in findings:
        counts[finding.severity] += 1
    return counts


def print_markdown(findings: list[Finding]) -> None:
    counts = summarize(findings)
    print("# Agent Design Audit")
    print()
    print(f"High: {counts['high']} | Medium: {counts['medium']} | Low: {counts['low']}")
    print()
    if not findings:
        print("No deterministic design-audit findings.")
        return
    for finding in findings:
        print(
            f"- [{finding.severity.upper()}] {finding.file}:{finding.line} "
            f"`{finding.rule_id}` - {finding.message}"
        )
        print(f"  `{finding.excerpt}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan UI source for common AI-design and UX issues.")
    parser.add_argument("target", help="File or directory to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    parser.add_argument(
        "--fail-on",
        choices=["none", "low", "medium", "high"],
        default="high",
        help="Exit non-zero when findings at this severity or higher are present.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 2

    root = target if target.is_dir() else target.parent
    findings: list[Finding] = []
    for path in iter_files(target):
        findings.extend(scan_file(path.resolve(), root.resolve()))

    findings.sort(key=lambda item: (SEVERITY_RANK[item.severity] * -1, item.file, item.line))

    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    else:
        print_markdown(findings)

    fail_rank = SEVERITY_RANK[args.fail_on]
    if fail_rank and any(SEVERITY_RANK[finding.severity] >= fail_rank for finding in findings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
