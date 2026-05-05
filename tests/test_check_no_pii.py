"""Tests for scripts/check_no_pii.py."""

import pytest
from pathlib import Path
from check_no_pii import scan, PIIFinding


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def test_scan_finds_estonian_personal_code(tmp_path):
    _write(tmp_path, "skills/test/SKILL.md", "Example: 38001085718 is a personal code.")
    findings = scan(tmp_path, allowlist_patterns=[])
    assert any("38001085718" in f.match for f in findings)


def test_scan_skips_allowlisted_synthetic_value(tmp_path):
    _write(tmp_path, "skills/test/SKILL.md", "Example placeholder: 12345678901 — synthetic.")
    findings = scan(tmp_path, allowlist_patterns=["^12345678901$"])
    assert not findings


def test_scan_finds_iban_like_string(tmp_path):
    _write(tmp_path, "skills/test/SKILL.md", "Account: EE382200221020145685 (real-looking IBAN)")
    findings = scan(tmp_path, allowlist_patterns=[])
    assert any("EE382200221020145685" in f.match for f in findings)


def test_scan_ignores_obvious_non_match(tmp_path):
    _write(tmp_path, "skills/test/SKILL.md", "This file has no PII whatsoever.")
    findings = scan(tmp_path, allowlist_patterns=[])
    assert not findings
