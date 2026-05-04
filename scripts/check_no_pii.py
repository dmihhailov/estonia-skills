"""Scan the repo for accidentally-committed Estonian PII patterns.

Greps text files for:
- Estonian isikukood: 11 digits starting with 1-6.
- Estonian IBAN-shaped strings: EE + 18 digits.

An allowlist file (.pii-allowlist at repo root) of regexes permits known
synthetic placeholders. Run from repo root:
    python scripts/check_no_pii.py
Exits 0 if clean, non-zero on any finding.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path


PERSONAL_CODE_RE = re.compile(r"\b[1-6]\d{10}\b")
IBAN_RE = re.compile(r"\bEE\d{18}\b")
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".py", ".txt"}


@dataclass(frozen=True)
class PIIFinding:
    file: str
    line: int
    match: str


def _is_allowlisted(value: str, allowlist_patterns: list[str]) -> bool:
    return any(re.search(pat, value) for pat in allowlist_patterns)


def _load_allowlist(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def scan(root: Path, allowlist_patterns: list[str]) -> list[PIIFinding]:
    findings: list[PIIFinding] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        if any(part in {".git", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for match in PERSONAL_CODE_RE.findall(line) + IBAN_RE.findall(line):
                if not _is_allowlisted(match, allowlist_patterns):
                    findings.append(PIIFinding(file=str(path), line=lineno, match=match))
    return findings


def main(repo_root: Path) -> int:
    allowlist = _load_allowlist(repo_root / ".pii-allowlist")
    findings = scan(repo_root, allowlist_patterns=allowlist)
    for f in findings:
        print(f"PII: {f.file}:{f.line}: {f.match}", file=sys.stderr)
    if findings:
        return 1
    print("OK: no PII patterns found")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parent.parent))
