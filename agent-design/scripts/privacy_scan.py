#!/usr/bin/env python3
"""Scan the repository for high-risk public-release hygiene issues."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".next",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "output",
    "playwright-report",
    "test-results",
    "website",
}

SKIP_FILES = {
    "package-lock.json",
}

BINARY_EXTENSIONS = {
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".webp",
    ".zip",
}


@dataclass(frozen=True)
class Rule:
    rule_id: str
    pattern: re.Pattern[str]
    message: str


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    rule_id: str
    message: str
    excerpt: str


RULES = [
    Rule(
        "api-key",
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "Possible API key or token.",
    ),
    Rule(
        "secret-assignment",
        re.compile(
            r"""(?ix)
            \b(api[_-]?key|secret|password|auth[_-]?token|access[_-]?token|refresh[_-]?token|cookie)
            \b\s*[:=]\s*["']?[A-Za-z0-9_./+=:@-]{12,}
            """
        ),
        "Possible credential assignment.",
    ),
    Rule(
        "private-key",
        re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
        "Private key block should never be committed.",
    ),
    Rule(
        "windows-user-path",
        re.compile(r"\b[A-Z]:\\Users\\[^\\\s]+", re.I),
        "Local Windows user path should not appear in public files.",
    ),
    Rule(
        "posix-user-path",
        re.compile(r"\b/(?:Users|home)/[A-Za-z0-9._-]+"),
        "Local POSIX user path should not appear in public files.",
    ),
    Rule(
        "synology-path",
        re.compile(r"\bSynologyDrive\b", re.I),
        "Private sync-folder path should not appear in public files.",
    ),
]


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        yield path


def scan_file(path: Path, root: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")

    findings: list[Finding] = []
    lines = text.splitlines()
    for line_number, line in enumerate(lines, start=1):
        for rule in RULES:
            if rule.pattern.search(line):
                findings.append(
                    Finding(
                        file=str(path.relative_to(root)),
                        line=line_number,
                        rule_id=rule.rule_id,
                        message=rule.message,
                        excerpt=line.strip()[:180],
                    )
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for high-risk public repo hygiene issues.")
    parser.add_argument("target", nargs="?", default=".", help="Repository directory to scan.")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    if not root.exists():
        print(f"Target does not exist: {root}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    for path in iter_files(root):
        findings.extend(scan_file(path.resolve(), root))

    if findings:
        print("Privacy scan failed:")
        for finding in findings:
            print(
                f"- {finding.file}:{finding.line} `{finding.rule_id}` - "
                f"{finding.message} [{finding.excerpt}]"
            )
        return 1

    print("Privacy scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
