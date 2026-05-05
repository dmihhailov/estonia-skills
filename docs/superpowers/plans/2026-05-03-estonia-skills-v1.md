# estonia-skills v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build v1 of `estonia-skills` — a public, MIT-licensed Claude Code plugin with one router skill, three atomic skills (annual personal income tax filing, opening an OÜ as an e-Resident, residence registration for newcomers), Python validators, and CI — ready to publish on GitHub.

**Architecture:** Anthropic Agent Skills (agentskills.io v1 spec) packaged as a Claude Code plugin via `.claude-plugin/{plugin,marketplace}.json`. Skills auto-discovered by pointing `plugin.json`'s `skills` field at `./skills/`. Index schema lives in each skill's `metadata` frontmatter; `scripts/build_index.py` regenerates `skills/estonia/INDEX.yaml` from the frontmatter. Three Python validators (build_index, validate_frontmatter, check_no_pii) run in CI. Skills never hardcode legal/financial info — they always re-fetch from authoritative gov sources at runtime.

**Tech Stack:** Python 3.11+ (PyYAML, pytest), GitHub Actions, JSON, YAML, Markdown.

**Reference:** Spec at `docs/superpowers/specs/2026-05-03-estonia-skills-design.md`.

---

## File Structure

```
estonia-skills/
├── .gitignore                                                  # Task 1
├── LICENSE                                                     # Task 1
├── README.md                                                   # Task 1 (placeholder), Task 11 (full)
├── PRIVACY.md                                                  # Task 11
├── CONTRIBUTING.md                                             # Task 11
├── pyproject.toml                                              # Task 2
├── requirements-dev.txt                                        # Task 2
├── .claude-plugin/
│   ├── plugin.json                                             # Task 3
│   └── marketplace.json                                        # Task 3
├── scripts/
│   ├── build_index.py                                          # Task 4 — regenerates INDEX.yaml
│   ├── validate_frontmatter.py                                 # Task 5 — schema check
│   └── check_no_pii.py                                         # Task 6 — PII grep
├── tests/
│   ├── __init__.py                                             # Task 2
│   ├── conftest.py                                             # Task 2
│   ├── fixtures/                                               # Task 4 (test SKILL.md fixtures)
│   ├── test_build_index.py                                     # Task 4
│   ├── test_validate_frontmatter.py                            # Task 5
│   └── test_check_no_pii.py                                    # Task 6
├── skills/
│   ├── estonia/                                                # Task 7 — router
│   │   ├── SKILL.md
│   │   ├── INDEX.yaml                                          # generated
│   │   └── references/
│   │       ├── disclaimer.md
│   │       ├── eid-primer.md
│   │       └── glossary.md
│   ├── tax-filing-individual/                                  # Task 8
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   ├── ou-open-e-resident/                                     # Task 9
│   │   ├── SKILL.md
│   │   └── references/sources.md
│   └── residence-registration/                                 # Task 10
│       ├── SKILL.md
│       └── references/sources.md
└── .github/
    └── workflows/
        └── validate.yml                                        # Task 12
```

---

## Task 1: Repo skeleton (LICENSE, .gitignore, README placeholder)

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `README.md`

- [ ] **Step 1: Create `.gitignore`**

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.venv/
venv/

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
*.swp
```

- [ ] **Step 2: Create `LICENSE` (MIT, 2026)**

```
MIT License

Copyright (c) 2026 estonia-skills contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Create `README.md` placeholder**

```markdown
# estonia-skills

Modular Claude skills for Estonian bureaucracy (taxes, OÜ company formation, residence registration, and more).

> **Status:** in development. Full README forthcoming.

This repository is **not affiliated** with the Republic of Estonia or any of its agencies.
For the official Estonian government assistant mesh, see [Bürokratt](https://burokratt.ee).

See [`docs/superpowers/specs/2026-05-03-estonia-skills-design.md`](docs/superpowers/specs/2026-05-03-estonia-skills-design.md) for design.
```

- [ ] **Step 4: Verify**

Run: `ls -la`
Expected: `.gitignore`, `LICENSE`, `README.md` all present.

- [ ] **Step 5: Commit**

```bash
git add .gitignore LICENSE README.md
git commit -m "Add repo skeleton (LICENSE, .gitignore, README placeholder)"
```

---

## Task 2: Python tooling (pyproject, dev deps, test scaffolding)

**Files:**
- Create: `pyproject.toml`
- Create: `requirements-dev.txt`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[project]
name = "estonia-skills"
version = "0.1.0"
description = "Modular Claude skills for Estonian bureaucracy"
requires-python = ">=3.11"
license = { text = "MIT" }

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["scripts"]
```

- [ ] **Step 2: Create `requirements-dev.txt`**

```
pyyaml>=6.0
pytest>=8.0
```

- [ ] **Step 3: Create `tests/__init__.py`** (empty file — makes tests a package)

```
```

- [ ] **Step 4: Create `tests/conftest.py`**

```python
"""Shared pytest fixtures for estonia-skills tests."""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"
```

- [ ] **Step 5: Install dev dependencies**

Run: `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt`
Expected: pip succeeds, prints "Successfully installed pyyaml-* pytest-*".

- [ ] **Step 6: Verify pytest runs (no tests yet — exit code 5 is expected)**

Run: `. .venv/bin/activate && pytest`
Expected: `no tests ran` (exit code 5).

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml requirements-dev.txt tests/
git commit -m "Add Python tooling (pyproject, pytest, dev deps)"
```

---

## Task 3: Plugin manifests (`.claude-plugin/{plugin,marketplace}.json`)

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create `.claude-plugin/plugin.json`**

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "estonia-skills",
  "version": "0.1.0",
  "description": "Modular Claude skills for Estonian bureaucracy — taxes, OÜ, residence, identity",
  "license": "MIT",
  "homepage": "https://github.com/dmitrim/estonia-skills",
  "repository": "https://github.com/dmitrim/estonia-skills",
  "keywords": ["estonia", "civic", "bureaucracy", "tax", "e-residency"],
  "skills": "./skills/"
}
```

(Replace `dmitrim` with the actual GitHub owner if different.)

- [ ] **Step 2: Create `.claude-plugin/marketplace.json`**

```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "estonia-skills",
  "owner": { "name": "Dmitri Mihhailov" },
  "plugins": [
    {
      "name": "estonia-skills",
      "source": "./",
      "description": "Modular Claude skills for Estonian bureaucracy",
      "version": "0.1.0",
      "license": "MIT",
      "category": "productivity",
      "keywords": ["estonia", "civic", "tax", "e-residency"]
    }
  ]
}
```

- [ ] **Step 3: Validate JSON parses**

Run: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/
git commit -m "Add plugin and marketplace manifests"
```

---

## Task 4: `build_index.py` (TDD)

**Files:**
- Create: `tests/fixtures/skills/sample-skill/SKILL.md`
- Create: `tests/fixtures/skills/another-skill/SKILL.md`
- Create: `tests/fixtures/skills/estonia/SKILL.md`
- Create: `tests/test_build_index.py`
- Create: `scripts/build_index.py`

`build_index.py` walks a skills directory, parses each `SKILL.md`'s frontmatter, builds a sorted list of skill records (skipping the `estonia` router itself), and writes the result to `skills/estonia/INDEX.yaml`.

- [ ] **Step 1: Create test fixture skills**

Create `tests/fixtures/skills/sample-skill/SKILL.md`:

```markdown
---
name: sample-skill
description: A sample skill for testing
license: MIT
metadata:
  audience: "citizen,resident"
  life_event: "meta"
  service_domain: "tax"
  cadence: "annual"
  difficulty: "self-serve"
  auth_required: "smart-id"
  authoritative_lang: "et"
  freshness_sources: "https://example.com/a|https://example.com/b"
  last_verified: "2026-05-03"
  version: "1.0.0"
---

# Sample skill body
```

Create `tests/fixtures/skills/another-skill/SKILL.md`:

```markdown
---
name: another-skill
description: Another sample skill
license: MIT
metadata:
  audience: "e-resident"
  life_event: "starting-business"
  service_domain: "business"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "e-residency-card"
  authoritative_lang: "et"
  freshness_sources: "https://example.com/x"
  last_verified: "2026-04-01"
  version: "1.0.0"
---

# Another skill body
```

Create `tests/fixtures/skills/estonia/SKILL.md` (the router — should be skipped by build_index):

```markdown
---
name: estonia
description: Router skill
license: MIT
metadata:
  audience: "citizen,resident,e-resident,non-resident-founder,expat-newcomer"
  life_event: "meta"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "none"
  authoritative_lang: "et"
  freshness_sources: ""
  last_verified: "2026-05-03"
  version: "1.0.0"
---

# Router body
```

- [ ] **Step 2: Write the first failing test**

Create `tests/test_build_index.py`:

```python
"""Tests for scripts/build_index.py."""

from pathlib import Path
import yaml
from build_index import build_index


def test_build_index_parses_single_skill(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    names = [entry["name"] for entry in data["skills"]]
    assert "sample-skill" in names
    assert "another-skill" in names
```

- [ ] **Step 3: Run test, expect failure (no implementation yet)**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: ImportError or ModuleNotFoundError on `from build_index import build_index`.

- [ ] **Step 4: Write minimal `scripts/build_index.py` to pass**

```python
"""Regenerate skills/estonia/INDEX.yaml from each SKILL.md's frontmatter.

Walks <skills_dir>/*/SKILL.md, parses YAML frontmatter, skips the 'estonia'
router directory itself, and writes a sorted list of skill records to the
output file. Run from repo root: python scripts/build_index.py
"""

import sys
from pathlib import Path

import yaml


ROUTER_DIR_NAME = "estonia"
LIST_FIELDS = {"audience", "auth_required"}
PIPE_LIST_FIELDS = {"freshness_sources"}


def _parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{skill_md}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{skill_md}: malformed frontmatter")
    return yaml.safe_load(parts[1]) or {}


def _normalize_metadata(metadata: dict) -> dict:
    out = {}
    for key, value in metadata.items():
        if key in LIST_FIELDS and isinstance(value, str):
            out[key] = [item.strip() for item in value.split(",") if item.strip()]
        elif key in PIPE_LIST_FIELDS and isinstance(value, str):
            out[key] = [item.strip() for item in value.split("|") if item.strip()]
        else:
            out[key] = value
    return out


def build_index(skills_dir: Path, output: Path) -> None:
    entries = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == ROUTER_DIR_NAME:
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = _parse_frontmatter(skill_md)
        entries.append({
            "name": fm["name"],
            "description": fm.get("description", "").strip(),
            "metadata": _normalize_metadata(fm.get("metadata", {})),
        })

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(
            {"skills": entries},
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    build_index(repo_root / "skills", repo_root / "skills" / "estonia" / "INDEX.yaml")
    print(f"Wrote {repo_root / 'skills' / 'estonia' / 'INDEX.yaml'}")
```

- [ ] **Step 5: Run test, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: 1 passed.

- [ ] **Step 6: Add test for skipping router**

Append to `tests/test_build_index.py`:

```python
def test_build_index_skips_router(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    names = [entry["name"] for entry in data["skills"]]
    assert "estonia" not in names
```

- [ ] **Step 7: Run, expect pass (the skip is already implemented)**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: 2 passed.

- [ ] **Step 8: Add test for sorted output (deterministic)**

Append to `tests/test_build_index.py`:

```python
def test_build_index_output_is_sorted_by_name(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    names = [entry["name"] for entry in data["skills"]]
    assert names == sorted(names)
```

- [ ] **Step 9: Run, expect pass (sorted iterdir gives sorted output)**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: 3 passed.

- [ ] **Step 10: Add test for list-field normalization**

Append:

```python
def test_build_index_splits_comma_lists(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    sample = next(e for e in data["skills"] if e["name"] == "sample-skill")
    assert sample["metadata"]["audience"] == ["citizen", "resident"]


def test_build_index_splits_pipe_lists(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    sample = next(e for e in data["skills"] if e["name"] == "sample-skill")
    assert sample["metadata"]["freshness_sources"] == [
        "https://example.com/a",
        "https://example.com/b",
    ]
```

- [ ] **Step 11: Run, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: 5 passed.

- [ ] **Step 12: Add test for missing-frontmatter error**

Append:

```python
import pytest


def test_build_index_raises_on_missing_frontmatter(tmp_path):
    bad_skill = tmp_path / "skills" / "broken" / "SKILL.md"
    bad_skill.parent.mkdir(parents=True)
    bad_skill.write_text("# No frontmatter here\n")
    output = tmp_path / "INDEX.yaml"

    with pytest.raises(ValueError, match="missing YAML frontmatter"):
        build_index(tmp_path / "skills", output)
```

- [ ] **Step 13: Run, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_build_index.py -v`
Expected: 6 passed.

- [ ] **Step 14: Commit**

```bash
git add scripts/build_index.py tests/test_build_index.py tests/fixtures/
git commit -m "Add build_index.py with TDD coverage"
```

---

## Task 5: `validate_frontmatter.py` (TDD)

**Files:**
- Create: `tests/test_validate_frontmatter.py`
- Create: `scripts/validate_frontmatter.py`

`validate_frontmatter.py` walks `skills/*/SKILL.md`, parses frontmatter, and checks every required field is present and within its allowed enum / format. Exits 0 if all pass, non-zero otherwise.

- [ ] **Step 1: Write the first failing test**

Create `tests/test_validate_frontmatter.py`:

```python
"""Tests for scripts/validate_frontmatter.py."""

import pytest
from pathlib import Path
from validate_frontmatter import validate_skill, ValidationError


def _skill_with(metadata_overrides: dict) -> dict:
    base_metadata = {
        "audience": "citizen",
        "life_event": "meta",
        "service_domain": "tax",
        "cadence": "annual",
        "difficulty": "self-serve",
        "auth_required": "smart-id",
        "authoritative_lang": "et",
        "freshness_sources": "https://example.com/a",
        "last_verified": "2026-05-03",
        "version": "1.0.0",
    }
    base_metadata.update(metadata_overrides)
    return {
        "name": "test-skill",
        "description": "Test description",
        "license": "MIT",
        "metadata": base_metadata,
    }


def test_validate_passes_on_complete_frontmatter():
    validate_skill(_skill_with({}))  # should not raise


def test_validate_rejects_missing_required_metadata_field():
    fm = _skill_with({})
    del fm["metadata"]["audience"]
    with pytest.raises(ValidationError, match="audience"):
        validate_skill(fm)
```

- [ ] **Step 2: Run, expect failure**

Run: `. .venv/bin/activate && pytest tests/test_validate_frontmatter.py -v`
Expected: ImportError on `validate_frontmatter`.

- [ ] **Step 3: Write minimal `scripts/validate_frontmatter.py`**

```python
"""Validate that every skills/*/SKILL.md has correct, complete frontmatter.

Run from repo root:
    python scripts/validate_frontmatter.py
Exits 0 if all skills pass; non-zero otherwise.
"""

import re
import sys
from pathlib import Path

import yaml


REQUIRED_TOP_LEVEL = ("name", "description", "license", "metadata")
REQUIRED_METADATA = (
    "audience", "life_event", "service_domain", "cadence", "difficulty",
    "auth_required", "authoritative_lang", "freshness_sources",
    "last_verified", "version",
)
ALLOWED = {
    "audience": {"citizen", "resident", "e-resident", "non-resident-founder", "expat-newcomer"},
    "life_event": {
        "arriving", "starting-business", "employment", "family", "housing",
        "vehicle", "education", "healthcare", "retirement", "leaving", "death", "meta",
    },
    "service_domain": {"tax", "identity", "business", "social", "health", "justice", "property"},
    "cadence": {"one-off", "annual", "monthly", "on-demand"},
    "difficulty": {"self-serve", "accountant-recommended", "lawyer-recommended"},
    "auth_required": {"none", "smart-id", "mobile-id", "id-card", "e-residency-card"},
    "authoritative_lang": {"et", "en", "ru"},
}
LIST_FIELDS_COMMA = {"audience", "auth_required"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


class ValidationError(Exception):
    pass


def _parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValidationError(f"{skill_md}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValidationError(f"{skill_md}: malformed frontmatter")
    return yaml.safe_load(parts[1]) or {}


def validate_skill(fm: dict) -> None:
    for key in REQUIRED_TOP_LEVEL:
        if key not in fm:
            raise ValidationError(f"missing top-level field: {key}")

    metadata = fm.get("metadata") or {}
    for key in REQUIRED_METADATA:
        if key not in metadata:
            raise ValidationError(f"missing metadata field: {key}")

    for key, allowed in ALLOWED.items():
        value = metadata[key]
        items = (
            [v.strip() for v in value.split(",")] if key in LIST_FIELDS_COMMA
            else [value]
        )
        for item in items:
            if item not in allowed:
                raise ValidationError(f"{key}: '{item}' not in allowed values {sorted(allowed)}")

    if not DATE_RE.match(str(metadata["last_verified"])):
        raise ValidationError(f"last_verified must be YYYY-MM-DD, got: {metadata['last_verified']}")
    if not SEMVER_RE.match(str(metadata["version"])):
        raise ValidationError(f"version must be semver (X.Y.Z), got: {metadata['version']}")


def main(skills_dir: Path) -> int:
    failures: list[str] = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        try:
            validate_skill(_parse_frontmatter(skill_md))
        except ValidationError as exc:
            failures.append(f"{skill_md}: {exc}")

    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    if failures:
        return 1
    print(f"OK: validated {len(list(skills_dir.glob('*/SKILL.md')))} skill(s)")
    return 0


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    sys.exit(main(repo_root / "skills"))
```

- [ ] **Step 4: Run tests, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_validate_frontmatter.py -v`
Expected: 2 passed.

- [ ] **Step 5: Add tests for enum violations and format errors**

Append to `tests/test_validate_frontmatter.py`:

```python
def test_validate_rejects_unknown_audience_value():
    fm = _skill_with({"audience": "alien"})
    with pytest.raises(ValidationError, match="audience"):
        validate_skill(fm)


def test_validate_rejects_unknown_life_event():
    fm = _skill_with({"life_event": "vacation"})
    with pytest.raises(ValidationError, match="life_event"):
        validate_skill(fm)


def test_validate_accepts_multiple_audiences():
    fm = _skill_with({"audience": "citizen,resident,e-resident"})
    validate_skill(fm)  # should not raise


def test_validate_rejects_bad_date_format():
    fm = _skill_with({"last_verified": "May 3, 2026"})
    with pytest.raises(ValidationError, match="last_verified"):
        validate_skill(fm)


def test_validate_rejects_non_semver_version():
    fm = _skill_with({"version": "v1"})
    with pytest.raises(ValidationError, match="version"):
        validate_skill(fm)
```

- [ ] **Step 6: Run tests, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_validate_frontmatter.py -v`
Expected: 7 passed.

- [ ] **Step 7: Commit**

```bash
git add scripts/validate_frontmatter.py tests/test_validate_frontmatter.py
git commit -m "Add validate_frontmatter.py with TDD coverage"
```

---

## Task 6: `check_no_pii.py` (TDD)

**Files:**
- Create: `tests/test_check_no_pii.py`
- Create: `scripts/check_no_pii.py`
- Create: `.pii-allowlist`

`check_no_pii.py` greps the repo for Estonian personal-code patterns (`isikukood`: 11 digits starting with 1-6) and IBAN patterns. An allowlist file (`.pii-allowlist`, one regex per line) lets us permit clearly-synthetic examples (e.g., `12345678901`).

- [ ] **Step 1: Create `.pii-allowlist`**

```
# Synthetic / documentation-only values that should never trigger the PII check.
# One Python regex per line. Lines starting with # are ignored.
^12345678901$
^EE000000000000000000$
```

- [ ] **Step 2: Write failing tests**

Create `tests/test_check_no_pii.py`:

```python
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
```

- [ ] **Step 3: Run, expect failure**

Run: `. .venv/bin/activate && pytest tests/test_check_no_pii.py -v`
Expected: ImportError on `check_no_pii`.

- [ ] **Step 4: Implement `scripts/check_no_pii.py`**

```python
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
```

- [ ] **Step 5: Run tests, expect pass**

Run: `. .venv/bin/activate && pytest tests/test_check_no_pii.py -v`
Expected: 4 passed.

- [ ] **Step 6: Run the scanner against the repo (sanity check — no findings yet)**

Run: `. .venv/bin/activate && python scripts/check_no_pii.py`
Expected: `OK: no PII patterns found`, exit 0.

- [ ] **Step 7: Commit**

```bash
git add scripts/check_no_pii.py tests/test_check_no_pii.py .pii-allowlist
git commit -m "Add check_no_pii.py with TDD coverage and allowlist"
```

---

## Task 7: Router skill scaffolding (`skills/estonia/`)

**Files:**
- Create: `skills/estonia/references/disclaimer.md`
- Create: `skills/estonia/references/eid-primer.md`
- Create: `skills/estonia/references/glossary.md`
- Create: `skills/estonia/SKILL.md`
- Create: `skills/estonia/INDEX.yaml` (initially empty array — regenerated once atomic skills exist)

- [ ] **Step 1: Create `skills/estonia/references/disclaimer.md`**

```markdown
# Disclaimer

**This is AI-generated procedural guidance, not legal, tax, or medical advice.**

- Always verify against the authoritative Estonian government source linked in each skill.
- This repository is **not affiliated** with the Republic of Estonia, Maksu- ja Tolliamet (MTA), Politsei- ja Piirivalveamet (PPA), the e-Residency programme, or any other state authority.
- Estonian law is canonical in Estonian. English translations published by Riigi Teataja or government portals may lag the Estonian text by months — when guidance hinges on legal language, treat the Estonian-language source as authoritative and the translation as orientation only.
- When in doubt, consult a qualified accountant, lawyer, or notary.

This disclaimer is required by EU AI Act Art. 50 (transparency for AI-generated content). Skills referenced from this repository must not collect, store, or transmit personally identifiable information.
```

- [ ] **Step 2: Create `skills/estonia/references/eid-primer.md`**

```markdown
# Estonian eID — Smart-ID, Mobile-ID, ID-card

Most Estonian government transactions require authenticating with one of three electronic identity tools. A skill in this repository will walk a user up to the point of authentication and then hand off — skills do not impersonate users or transact on their behalf.

## Smart-ID
A mobile-app-based authentication and signing tool issued by SK ID Solutions. Available to citizens and residents of Estonia, Latvia, and Lithuania. Free for personal use. Works without a SIM card. https://www.smart-id.com

## Mobile-ID
A SIM-based authentication tool — the user's phone number itself becomes their digital ID. Requires support from the user's mobile operator. Estonian only. Issued via the operator + Politsei- ja Piirivalveamet (PPA).

## ID-card
The physical Estonian ID-card with an embedded chip. Requires a card reader connected to the user's computer. The legal default; every Estonian citizen and most residents have one. https://www.id.ee

## e-Residency card
A subset of the ID-card capability issued to non-residents who have applied for and received e-Residency. Allows e-Residents to authenticate to Estonian e-services and digitally sign documents, but does **not** confer residence, citizenship, or tax residency. https://www.e-resident.gov.ee

## When a skill says "log in with your eID"
The user picks whichever of the four they have available. Most government portals accept all four (or all three, depending on the user's residency status). Skills should phrase this as "log in with your Smart-ID, Mobile-ID, or ID-card" and let the user choose.
```

- [ ] **Step 3: Create `skills/estonia/references/glossary.md`**

```markdown
# Glossary — Estonian government terms

| Term | Meaning |
|---|---|
| `isikukood` | Estonian personal identification code: 11 digits encoding birth date, sex, and a checksum. The primary identifier for individuals across all Estonian e-services. **Never request this in a chat — instruct the user to provide it directly to the gov portal.** |
| `OÜ` | *Osaühing* — private limited company (LLC equivalent). Most common business form for small companies, including those founded by e-Residents. |
| `MTA` / `EMTA` | *Maksu- ja Tolliamet* — Estonian Tax and Customs Board. Operates `e-MTA`, the self-service portal for tax filings. |
| `PPA` | *Politsei- ja Piirivalveamet* — Police and Border Guard Board. Issues passports, ID-cards, residence permits. |
| `RIK` | *Registrite ja Infosüsteemide Keskus* — Centre of Registers and Information Systems. Operates the business registry (Äriregister). |
| `Äriregister` | Estonian business registry, run by RIK. Includes a free open-data dump and a paid live API. |
| `Riigi Teataja` | The official state gazette — primary publication of laws and legal acts. Has a free public API for retrieving acts. |
| `Riigikogu` | The Estonian Parliament. |
| `tuludeklaratsioon` | Annual personal income tax declaration. |
| `vanemahüvitis` | Parental benefit (paid leave compensation paid to one parent). |
| `Töötukassa` | Estonian Unemployment Insurance Fund. |
| `Sotsiaalkindlustusamet` | Social Insurance Board (pensions, family benefits, disability). |
| `rahvastikuregister` | Population register — official record of residents' addresses and core attributes. |
| `e-Residency` | A digital identity programme for non-residents allowing remote interaction with Estonian e-services. Does **not** confer residence, citizenship, or tax residency. |
| `Bürokratt` | Estonia's official government chatbot mesh. estonia-skills is **not** affiliated with Bürokratt. |
| `X-Road` (`x-tee`) | The Estonian inter-agency data exchange backbone. Membership-restricted; not directly callable from a skill. |
| `DigiDoc` | Desktop client for creating and verifying `.asice` / `.bdoc` digitally-signed document containers. |
```

- [ ] **Step 4: Create `skills/estonia/SKILL.md`** (router)

````markdown
---
name: estonia
description: |
  Router for Estonian bureaucracy questions. Use whenever the user asks about
  Estonian government procedures, taxes, business registration, residence,
  identity documents, e-Residency, passports, kindergarten enrolment, vehicle
  registration, healthcare, social benefits, or any other interaction with an
  Estonian state authority. Routes to the appropriate sub-skill based on
  audience and intent. Trigger words: "Estonia", "Eesti", "OÜ", "MTA", "EMTA",
  "e-Residency", "isikukood", "tuludeklaratsioon", "Töötukassa", "PPA", "Smart-ID".
license: MIT
metadata:
  audience: "citizen,resident,e-resident,non-resident-founder,expat-newcomer"
  life_event: "meta"
  service_domain: "identity"
  cadence: "on-demand"
  difficulty: "self-serve"
  auth_required: "none"
  authoritative_lang: "et"
  freshness_sources: ""
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Estonia — bureaucracy router

This skill is the entry point for Estonian government procedures. It does not give procedural advice itself; it routes to a sub-skill that does.

## Disclaimer

Before any procedural guidance, reproduce the key line from `references/disclaimer.md`:

> This is AI-generated procedural guidance, not legal, tax, or medical advice. Always verify against the authoritative Estonian government source. This repository is not affiliated with the Republic of Estonia.

## Routing logic

1. **Load the catalog.** Read `INDEX.yaml` (in this same skill directory). It lists every other skill in this repository with full metadata.

2. **Identify audience.** If the user's message does not make their audience clear, ask exactly one question:
   > Are you (a) an Estonian citizen or resident, (b) an e-Resident running an Estonian company, or (c) newly arrived or arriving in Estonia?

   If the user replies with their situation in plain language, infer the audience tag(s) and proceed.

3. **Filter the catalog.** Narrow `INDEX.yaml` entries to those whose `audience` overlaps with the user's audience and whose `service_domain` or trigger keywords match the user's intent.

4. **Branch on match count:**
   - **One match** — name the skill, summarize what it covers in one sentence, and ask: "Want me to walk you through it?" Do not auto-load.
   - **Multiple matches** — present a numbered list (max 5) with one-line descriptions. Let the user pick.
   - **Composite life event** (e.g., "I'm relocating to Estonia") — propose an ordered chain of skills with shared context. Confirm before chaining.

5. **Freshness check.** Before activating any sub-skill, look at its `last_verified` date. If it is more than 90 days before today, warn the user:
   > This skill was last verified on YYYY-MM-DD. Estonian government procedures can change; if anything below seems out of date, double-check against the authoritative source linked at the bottom of the skill.

6. **No PII into chat.** Never ask the user to paste their isikukood, account numbers, or any other personal identifier into the conversation. If a procedural step requires personal data, instruct the user to enter it directly into the relevant gov portal at the time of authentication.

## Reference material

- `references/disclaimer.md` — full disclaimer text and AI Act compliance language.
- `references/eid-primer.md` — Smart-ID, Mobile-ID, ID-card, e-Residency card explained.
- `references/glossary.md` — definitions of `isikukood`, `OÜ`, `MTA`, and other terms used across skills.

## Sub-skills available in v1

See `INDEX.yaml`. v1 ships:
- `tax-filing-individual` — annual personal income tax declaration via e-MTA.
- `ou-open-e-resident` — opening a private limited company (OÜ) as an e-Resident.
- `residence-registration` — registering one's place of residence as a newcomer.
````

- [ ] **Step 5: Generate `INDEX.yaml` (will be empty `skills: []` for now — atomic skills don't exist yet)**

Run: `. .venv/bin/activate && python scripts/build_index.py`
Expected: Writes `skills/estonia/INDEX.yaml` containing `skills: []`.

- [ ] **Step 6: Validate router frontmatter**

Run: `. .venv/bin/activate && python scripts/validate_frontmatter.py`
Expected: `OK: validated 1 skill(s)`, exit 0.

- [ ] **Step 7: Commit**

```bash
git add skills/estonia/
git commit -m "Add router skill (estonia) with disclaimer, eid-primer, glossary"
```

---

## Task 8: `tax-filing-individual` skill

**Files:**
- Create: `skills/tax-filing-individual/SKILL.md`
- Create: `skills/tax-filing-individual/references/sources.md`

This task requires fetching authoritative emta.ee pages to verify URLs and extract the current procedure structure. If WebFetch is blocked, the implementer must visit the pages in a browser and transcribe the structure.

- [ ] **Step 1: Verify the canonical URL for personal income tax filing**

Use WebFetch (or browser) on:
- `https://www.emta.ee/eraklient/tulu-deklareerimine`
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad`

Confirm both return 200 and contain content about personal income tax declaration. Note the section headings present on each page (you'll cite them in the body). If a URL has changed, find the current canonical path.

- [ ] **Step 2: Create `skills/tax-filing-individual/SKILL.md`**

````markdown
---
name: tax-filing-individual
description: |
  Walks an Estonian resident or citizen through filing the annual personal
  income tax declaration (tuludeklaratsioon) via e-MTA. Use when the user
  mentions: "tax return", "tuludeklaratsioon", "annual taxes", "MTA", "EMTA",
  "tax filing for individuals", "how much do I owe in taxes", or "when am I
  getting my tax refund". Always re-fetches current tax-year rates and
  deadlines from emta.ee — never quotes cached numbers.
license: MIT
metadata:
  audience: "citizen,resident"
  life_event: "meta"
  service_domain: "tax"
  cadence: "annual"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.emta.ee/eraklient/tulu-deklareerimine|https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Tax filing for individuals

## Disclaimer

This is AI-generated procedural guidance, not tax advice. Always verify against the authoritative emta.ee pages linked below. This repository is not affiliated with the Republic of Estonia or Maksu- ja Tolliamet.

## Freshness obligation

**Before quoting any tax rate, threshold, deadline, or fee, fetch the current pages at:**

- `https://www.emta.ee/eraklient/tulu-deklareerimine`
- `https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad`

**Do not quote any number or date from this skill body.** Numbers below (if any) are illustrative only — always replace them with what the live pages currently say.

## Step 1 — Disambiguate the user's situation

Ask the minimum necessary, in this order:

1. **Tax year.** "Which tax year are you filing for?" (Default: the previous calendar year. The Estonian tax year runs January 1 – December 31; declarations open in February.)
2. **Tax residency.** "Are you a tax resident of Estonia for that year?" (Tax residency is distinct from residence permit or citizenship — it usually means the person spent ≥183 days in Estonia in a 12-month period or has a permanent home there. If the user is unsure, point them at the residency-test section on emta.ee.)
3. **Income types.** "What kinds of income did you receive that year?" (Employment salary, business income/FIE, dividends, rental, capital gains, foreign income, etc.) Different income types route to different sections of the e-MTA pre-filled return.

## Step 2 — Walk through the e-MTA flow

1. Fetch the live emta.ee page above and identify the current section titled (in Estonian) "Kuidas deklaratsiooni esitada" or (in English) "How to file the declaration." Summarise the steps from that page in 6–10 bullets, in the user's chosen language.
2. Mention the current filing window (open and close dates) — fetched from the live page, not memorised.
3. Mention the current tax-rate table from the `maksumaarad` page (basic exemption, income tax rate, etc.) — again, fetched, not memorised.

Frame each step in terms the user can act on. Where possible, link to the specific gov page that explains the step in detail.

## Step 3 — Auth seam (where the skill ends)

End the procedural guidance with:

> Now log in to **e-MTA** at `https://maasikas.emta.ee/oma_ee/login` (or via `https://www.emta.ee/`) using your Smart-ID, Mobile-ID, or ID-card. Most income data will already be pre-filled. Review each section, add anything missing (foreign income, rental income, FIE income), confirm your bank account for any refund, and submit.

After this point, do not narrate the in-portal experience — the user is authenticated and the page itself guides them.

## Step 4 — Common pitfalls to flag

After the procedural walkthrough, surface these (verify each against the live page):

- Foreign income from EU and non-EU sources is treated differently — a treaty may apply.
- Cryptocurrency gains are declarable; the rules are on a separate emta.ee page (link it).
- If the user owes tax (rather than getting a refund), the payment deadline differs from the filing deadline.
- The basic exemption phases out above a certain income threshold — the live page has the current threshold.

## Sources

See `references/sources.md`.
````

- [ ] **Step 3: Create `skills/tax-filing-individual/references/sources.md`**

```markdown
# Sources — tax-filing-individual

All canonical URLs cited in this skill. The implementer must verify each URL returns 200 and contains the expected content; record the date of last check next to each URL.

| URL | Purpose | Last checked |
|---|---|---|
| https://www.emta.ee/eraklient/tulu-deklareerimine | Procedure overview | 2026-05-03 |
| https://www.emta.ee/eraklient/maksud-ja-tasumine/tulu-deklareerimine/maksumaarad | Current tax rates and thresholds | 2026-05-03 |
| https://maasikas.emta.ee/oma_ee/login | e-MTA self-service login | 2026-05-03 |
| https://www.emta.ee/eraklient/tulu-deklareerimine/krüptovara | Cryptocurrency gains rules | 2026-05-03 |

If a URL changes or returns non-200, update this table and bump `last_verified` in `SKILL.md`.
```

- [ ] **Step 4: Validate frontmatter**

Run: `. .venv/bin/activate && python scripts/validate_frontmatter.py`
Expected: `OK: validated 2 skill(s)`, exit 0.

- [ ] **Step 5: Regenerate INDEX.yaml**

Run: `. .venv/bin/activate && python scripts/build_index.py`
Expected: `skills/estonia/INDEX.yaml` now contains one entry for `tax-filing-individual`.

- [ ] **Step 6: PII check**

Run: `. .venv/bin/activate && python scripts/check_no_pii.py`
Expected: `OK: no PII patterns found`.

- [ ] **Step 7: Commit**

```bash
git add skills/tax-filing-individual/ skills/estonia/INDEX.yaml
git commit -m "Add tax-filing-individual skill"
```

---

## Task 9: `ou-open-e-resident` skill

**Files:**
- Create: `skills/ou-open-e-resident/SKILL.md`
- Create: `skills/ou-open-e-resident/references/sources.md`

- [ ] **Step 1: Verify canonical URLs**

Use WebFetch (or browser) on:
- `https://www.e-resident.gov.ee/start-a-company/`
- `https://ariregister.rik.ee/eng/application/start`

Confirm 200 and current procedure content. Note the actual section headings.

(Note: the previous spec URL `https://ariregister.rik.ee/eng/company-registration-portal`
returns 404; the canonical establishment path is `/eng/application/start`. The legacy
`https://ettevotjaportaal.rik.ee/index.py?chlang=eng` is no longer reachable — the
e-Business Register has subsumed the entrepreneur portal flow. The name-search URL
`/eng/name-search` is also 404 — use `/eng/name_query`. The marketplace URL
`https://www.e-resident.gov.ee/marketplace/` 301-redirects to
`https://marketplace.e-resident.gov.ee/`.)

- [ ] **Step 2: Create `skills/ou-open-e-resident/SKILL.md`**

````markdown
---
name: ou-open-e-resident
description: |
  Walks an e-Resident through opening a private limited company (osaühing, OÜ)
  remotely using the e-Residency digital ID. Use when the user mentions:
  "open OÜ", "open Estonian company", "register OÜ", "e-Residency company",
  "ariregister", "Company Registration Portal", "start a business in Estonia
  as a non-resident". Always re-fetches the current procedure from
  e-resident.gov.ee — never quotes cached fees or share-capital minimums.
license: MIT
metadata:
  audience: "e-resident,non-resident-founder"
  life_event: "starting-business"
  service_domain: "business"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "e-residency-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.e-resident.gov.ee/start-a-company/|https://ariregister.rik.ee/eng/application/start"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Open an OÜ as an e-Resident

## Disclaimer

This is AI-generated procedural guidance, not legal, tax, or accounting advice. Always verify against the authoritative pages linked below. This repository is not affiliated with the Republic of Estonia, the e-Residency programme, or Centre of Registers and Information Systems (RIK).

## Freshness obligation

**Before quoting any state fee, share capital minimum, processing time, or step, fetch the current pages at:**

- `https://www.e-resident.gov.ee/start-a-company/`
- `https://ariregister.rik.ee/eng/application/start`

**Numbers and procedural steps in this skill body are illustrative — always replace them with what the live pages currently say.**

## Step 1 — Confirm prerequisites

Ask the user, in order:

1. **Do you already hold an active e-Residency digital ID card?** If no, route them to the e-Residency application flow first — this skill assumes the card is in hand.
2. **Do you have a card reader and the latest DigiDoc4 client installed?** Smart-ID and Mobile-ID are not options here; OÜ registration requires the e-Residency ID-card and a hardware reader.
3. **Have you chosen a contact person and legal address in Estonia?** Most e-Residents use a third-party service provider for both. Mention that this is a service marketplace topic, not a state matter — the user picks a provider from `https://marketplace.e-resident.gov.ee/`.
4. **What's the company's intended name?** Mention that name availability can be checked at `https://ariregister.rik.ee/eng/name_query`.

## Step 2 — Walk through the Company Registration Portal procedure

1. Fetch `https://www.e-resident.gov.ee/start-a-company/` and summarise the current procedure in 6–10 numbered steps, in the user's chosen language. Pay particular attention to the contributed share capital question (some founders defer payment, others pay up front), and the differences for sole vs. multiple founders.
2. Fetch the relevant section on `https://ariregister.rik.ee/eng/application/start` and confirm the in-portal flow matches the description above.
3. State the current state fee (from the live page, not memorised).
4. State current processing time (from the live page).

## Step 3 — Auth seam

End procedural guidance with:

> Now sign in to the **e-Business Register (e-Äriregister)** at `https://ariregister.rik.ee/eng/application/start` with your e-Residency ID-card via the DigiDoc4 client. Fill in the application, sign, and pay the state fee. RIK will email you when the company is approved (typically within a business day).

## Step 4 — After registration

Surface these post-registration tasks (verify against the live page):

- Open a business bank account (Wise, LHV, and various fintechs are common; the e-Residency marketplace lists options).
- Register for VAT if anticipated turnover exceeds the current threshold (fetch the threshold from emta.ee).
- File the annual report after the first financial year ends.
- Set up accounting; many founders use service providers from the marketplace.

## Sources

See `references/sources.md`.
````

- [ ] **Step 3: Create `skills/ou-open-e-resident/references/sources.md`**

```markdown
# Sources — ou-open-e-resident

All canonical URLs cited in this skill. The implementer must verify each URL returns 200 and contains the expected content; record the date of last check next to each URL.

| URL | Purpose | Last checked |
|---|---|---|
| https://www.e-resident.gov.ee/start-a-company/ | Procedure overview for e-Residents | 2026-05-03 |
| https://ariregister.rik.ee/eng/application/start | e-Business Register / Company Registration Portal — establishment of a new legal person | 2026-05-03 |
| https://ariregister.rik.ee/eng/name_query | Company name availability check | 2026-05-03 |
| https://marketplace.e-resident.gov.ee/ | Service-provider marketplace (contact person, accounting, etc.) | 2026-05-03 |

If a URL changes or returns non-200, update this table and bump `last_verified` in `SKILL.md`.
```

- [ ] **Step 4: Validate, regenerate index, PII-check**

Run:
```bash
. .venv/bin/activate && \
  python scripts/validate_frontmatter.py && \
  python scripts/build_index.py && \
  python scripts/check_no_pii.py
```
Expected: all three commands exit 0; INDEX.yaml now lists 2 skills.

- [ ] **Step 5: Commit**

```bash
git add skills/ou-open-e-resident/ skills/estonia/INDEX.yaml
git commit -m "Add ou-open-e-resident skill"
```

---

## Task 10: `residence-registration` skill

**Files:**
- Create: `skills/residence-registration/SKILL.md`
- Create: `skills/residence-registration/references/sources.md`

- [ ] **Step 1: Verify canonical URLs**

Use WebFetch (or browser) on:
- `https://www.eesti.ee/en` — find the residence-registration page (path may have changed; search the site if the direct URL 404s).
- `https://www.politsei.ee/en` — find the residence-permit instructions for newcomers (relevant for non-EU/non-EEA expats).

Confirm 200 and content. Capture the canonical URLs.

- [ ] **Step 2: Create `skills/residence-registration/SKILL.md`**

````markdown
---
name: residence-registration
description: |
  Walks a newcomer to Estonia (EU/EEA citizen, third-country national, or
  returning resident) through registering their place of residence in the
  rahvastikuregister (population register). Use when the user mentions:
  "register address Estonia", "rahvastikuregister", "kohalik omavalitsus",
  "moving to Estonia", "place of residence", "elukoharegistreerimine".
  Distinguishes between place-of-residence registration (for everyone) and
  residence permits (for non-EU nationals). Always re-fetches current procedure
  from eesti.ee and politsei.ee.
license: MIT
metadata:
  audience: "expat-newcomer,resident"
  life_event: "arriving"
  service_domain: "identity"
  cadence: "one-off"
  difficulty: "self-serve"
  auth_required: "smart-id,mobile-id,id-card"
  authoritative_lang: "et"
  freshness_sources: "https://www.eesti.ee/en|https://www.politsei.ee/en"
  last_verified: "2026-05-03"
  version: "0.1.0"
---

# Residence registration

## Disclaimer

This is AI-generated procedural guidance, not legal advice. Always verify against the authoritative eesti.ee and politsei.ee pages linked below. This repository is not affiliated with the Republic of Estonia, Politsei- ja Piirivalveamet, or any local government.

## Freshness obligation

**Before quoting any deadline, fee, document list, or processing time, fetch the current pages at:**

- `https://www.eesti.ee/en` (find the current path for "registering place of residence")
- `https://www.politsei.ee/en` (find the current path for residence permits, if applicable)

## Step 1 — Two procedures, often confused

Clarify with the user which they need:

1. **Place-of-residence registration** (`elukoharegistreerimine`) — recording the user's address in the population register. Required for everyone living in Estonia for >3 months, regardless of citizenship. Free. Self-service.
2. **Residence permit** — only for non-EU/non-EEA nationals who need legal authorisation to reside. Issued by PPA. Has fees, document requirements, and processing time. Different procedure entirely.

EU/EEA citizens need #1 only (plus a "right of residence" registration at PPA after 3 months — fetch the current details from politsei.ee).

Non-EU/non-EEA citizens need both #2 (first) and then #1 (after arrival).

## Step 2 — Place-of-residence registration walkthrough

1. Fetch the live eesti.ee page and summarise the current registration procedure in 6–10 numbered steps, in the user's chosen language. Cover: who must register, document requirements, and the two channels (online vs. in-person at the local council).
2. Note that only the property owner (or someone with the owner's written consent) can register an address there — many newcomers forget this and assume a tenancy agreement is enough.

## Step 3 — Residence permit walkthrough (only if needed)

If the user is non-EU/non-EEA and needs a permit:

1. Fetch the live politsei.ee page and identify the relevant permit type (work, study, family reunification, long-term resident, etc.).
2. Summarise the application steps, document list, and current state fee in 6–10 bullets.
3. Note that most third-country applications must be filed at an Estonian embassy abroad **before** travel, not after arrival.

## Step 4 — Auth seam

For place-of-residence registration:

> Submit your registration online at the eesti.ee residence-registration page using your Smart-ID, Mobile-ID, or ID-card; or visit your local government office (`kohalik omavalitsus`) in person with your passport / ID and proof of right to use the address.

For residence permits:

> Apply at the relevant Estonian embassy abroad (or, if eligible, in person at a PPA service point in Estonia). The application flow itself is on the politsei.ee page; this skill ends at the start of that flow.

## Sources

See `references/sources.md`.
````

- [ ] **Step 3: Create `skills/residence-registration/references/sources.md`**

```markdown
# Sources — residence-registration

All canonical URLs cited in this skill. The implementer must verify each URL returns 200 and contains the expected content; record the date of last check next to each URL.

| URL | Purpose | Last checked |
|---|---|---|
| https://www.eesti.ee/en | State portal — find current residence-registration path here | 2026-05-03 |
| https://www.politsei.ee/en | PPA — residence permits and EU right of residence | 2026-05-03 |

If a URL changes or returns non-200, update this table and bump `last_verified` in `SKILL.md`.
```

- [ ] **Step 4: Validate, regenerate index, PII-check**

Run:
```bash
. .venv/bin/activate && \
  python scripts/validate_frontmatter.py && \
  python scripts/build_index.py && \
  python scripts/check_no_pii.py
```
Expected: all three exit 0; INDEX.yaml now lists 3 skills.

- [ ] **Step 5: Commit**

```bash
git add skills/residence-registration/ skills/estonia/INDEX.yaml
git commit -m "Add residence-registration skill"
```

---

## Task 11: Documentation (README, PRIVACY, CONTRIBUTING)

**Files:**
- Modify: `README.md` (replace placeholder with full content)
- Create: `PRIVACY.md`
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Replace `README.md`**

Use Edit on `README.md` (replace the entire placeholder content) with:

```markdown
# estonia-skills

Modular [Claude](https://claude.ai) skills for Estonian bureaucracy — taxes, OÜ company formation, residence registration, and more. Skills are written in the [agentskills.io v1](https://agentskills.io/specification) format and packaged as a Claude Code plugin.

> **Not affiliated with the Republic of Estonia.** For the official Estonian government assistant mesh, see [Bürokratt](https://burokratt.ee). This repo is a Claude-native complement, intended for users who already work in Claude.

## Install (Claude Code)

```
/plugin marketplace add dmitrim/estonia-skills
/plugin install estonia-skills@estonia-skills
/reload-plugins
```

(Replace `dmitrim` with the actual GitHub owner.)

After install, ask Claude things like:

- "How do I file my Estonian income tax return?"
- "I'm an e-Resident — how do I open an OÜ?"
- "I just moved to Estonia, do I need to register my address?"

The router skill `estonia` will pick up the question and route to the right sub-skill.

## What's in v1

| Skill | Audience | Covers |
|---|---|---|
| `tax-filing-individual` | citizens, residents | Annual personal income tax declaration via e-MTA |
| `ou-open-e-resident` | e-Residents, non-resident founders | Opening an OÜ remotely with e-Residency ID |
| `residence-registration` | expat newcomers, residents | Registering place of residence (and residence permits) |

Plus the `estonia` router skill that disambiguates the user's intent and dispatches.

## How freshness works

Every skill carries a `freshness_sources` list of authoritative gov URLs (emta.ee, e-resident.gov.ee, eesti.ee, politsei.ee, …). When activated, the skill instructs Claude to **re-fetch those pages before quoting any number, fee, or deadline**. Skill bodies do not hardcode tax rates, thresholds, or deadlines — those always come from the live page.

Each skill also carries a `last_verified` timestamp. The router warns the user when activating a skill that hasn't been verified in over 90 days.

## Authentication boundary

Skills walk the user up to the Estonian eID auth seam (Smart-ID, Mobile-ID, ID-card, or e-Residency card) and then hand off. Skills never request personal identifiers in chat, never store PII, and never transact on the user's behalf.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to add a skill. The short version:

1. Create `skills/<your-skill>/SKILL.md` with the standard frontmatter.
2. Add `skills/<your-skill>/references/sources.md` listing canonical URLs.
3. Run `python scripts/build_index.py` and `python scripts/validate_frontmatter.py`.
4. Open a PR.

Privacy rules in [`PRIVACY.md`](PRIVACY.md) are non-negotiable: no real PII in examples, no PII collection in skills.

## License

MIT — see [`LICENSE`](LICENSE).

## Design

Architecture and rationale: [`docs/superpowers/specs/2026-05-03-estonia-skills-design.md`](docs/superpowers/specs/2026-05-03-estonia-skills-design.md).
```

- [ ] **Step 2: Create `PRIVACY.md`**

```markdown
# Privacy rules for contributors

These are **non-negotiable**. CI enforces them where possible; reviewers enforce them where it can't.

## 1. Never embed real personally identifiable information

Skill bodies, examples, tests, fixtures, and documentation must never contain real:

- Estonian personal identification codes (`isikukood`)
- Bank account numbers (Estonian `EE...` IBANs or any other)
- Passport numbers, ID-card numbers, residence permit numbers
- Real names of real private individuals
- Real home addresses
- Real phone numbers
- Real email addresses (other than well-known role addresses like `info@example.gov`)

Use synthetic examples. The CI script `scripts/check_no_pii.py` greps for personal-code and IBAN patterns; if you have a clearly-synthetic placeholder (like `12345678901`) that the regex flags, add it to `.pii-allowlist`.

## 2. Skills must never request PII into the conversation

Skill bodies must phrase prompts like:

- ✅ "You'll need your isikukood for this step. Have it ready."
- ❌ "Paste your isikukood here so I can check the format."

The Estonian eID flow handles authentication directly between the user and the gov portal. Skills walk the user up to the auth seam and hand off — they do not intermediate identification, ever.

## 3. The repository is GDPR-clean

Skill bodies and code in this repository do not collect, store, or transmit personal data. Users running these skills locally inside Claude do not send personal data through this repository — Claude itself runs in their own client; this repo just provides instructions.

If a contributor has a use case that involves any kind of PII handling, the answer is: **don't build it as a skill in this repo.** Open an issue first.

## 4. Reporting

If you spot a privacy violation in this repository, open an issue tagged `privacy` or — if it's sensitive — email the owner listed in `marketplace.json`. PRs that remove violations will be merged immediately.
```

- [ ] **Step 3: Create `CONTRIBUTING.md`**

````markdown
# Contributing to estonia-skills

Thanks for considering a contribution. This repo aims to cover Estonian bureaucratic procedures comprehensively, accurately, and freshly. Pull requests welcome — especially new skills covering procedures not yet in v1.

## What makes a good skill

- **Procedural, not advisory.** Walks a user through "how to do X with the Estonian state." Avoids individualised legal/tax/medical opinions.
- **Audience-aware.** Tagged with one or more of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer`.
- **Freshness-correct.** Body never quotes specific numbers (rates, fees, deadlines) — those are always re-fetched from the URLs in `freshness_sources` at runtime.
- **Authentication-respecting.** Ends at the Estonian eID auth seam — does not transact on the user's behalf, does not request PII.

## Adding a new skill (six steps)

### 1. Create the directory

```
skills/<your-skill-name>/
├── SKILL.md
└── references/
    └── sources.md
```

`<your-skill-name>` must be lowercase kebab-case (e.g., `kindergarten-queue-tallinn`).

### 2. Write `SKILL.md` with the full frontmatter

Copy the frontmatter shape from any existing skill (e.g. `skills/tax-filing-individual/SKILL.md`). The required `metadata` fields are:

| Field | Allowed values |
|---|---|
| `audience` | comma-list of `citizen`, `resident`, `e-resident`, `non-resident-founder`, `expat-newcomer` |
| `life_event` | one of `arriving`, `starting-business`, `employment`, `family`, `housing`, `vehicle`, `education`, `healthcare`, `retirement`, `leaving`, `death`, `meta` |
| `service_domain` | one of `tax`, `identity`, `business`, `social`, `health`, `justice`, `property` |
| `cadence` | one of `one-off`, `annual`, `monthly`, `on-demand` |
| `difficulty` | one of `self-serve`, `accountant-recommended`, `lawyer-recommended` |
| `auth_required` | comma-list of `none`, `smart-id`, `mobile-id`, `id-card`, `e-residency-card` |
| `authoritative_lang` | `et`, `en`, or `ru` (almost always `et`) |
| `freshness_sources` | pipe-separated URL list — the URLs the skill body must re-fetch before quoting |
| `last_verified` | `YYYY-MM-DD` — today's date |
| `version` | semver (start with `0.1.0`) |

### 3. Write the body

Follow the standard structure:

1. **Disclaimer** — reproduce the key line from `skills/estonia/references/disclaimer.md`.
2. **Freshness obligation** — instruct Claude to fetch `freshness_sources` URLs before quoting.
3. **Disambiguation questions** — the minimum to scope the procedure to the user.
4. **Walkthrough** — step-by-step prose, ending at the eID auth seam.
5. **Sources** — pointer to `references/sources.md`.

### 4. Run validators locally

```bash
. .venv/bin/activate
python scripts/validate_frontmatter.py
python scripts/build_index.py
python scripts/check_no_pii.py
```

All three must exit 0.

### 5. Set `last_verified` to today

This is the date you actually fetched and read the gov pages cited in `freshness_sources`. **Don't lie about this.** It's the signal users have for trusting the skill.

### 6. Open a PR

PR template includes a checklist. Reviewers look for:

- All validators pass.
- The skill body genuinely re-fetches sources rather than memorising numbers.
- No PII in examples.
- Disclaimer present.
- Auth seam respected.
- `INDEX.yaml` updated (regenerate with `build_index.py`).

## Verifying an existing skill

If you spot a skill whose `last_verified` is more than 90 days old, re-check it:

1. Fetch each URL in `freshness_sources`. Confirm 200 and current content.
2. Check the procedure described in the skill body still matches the live page.
3. Update `last_verified` to today.
4. Open a PR.

This is the single highest-leverage contribution to the repo's long-term usefulness.

## Style

- Write skill bodies in clear English. Claude renders to the user's chosen language at runtime.
- Use Estonian terms (`isikukood`, `OÜ`, `tuludeklaratsioon`) but gloss them on first use.
- Cite the Estonian-language gov page as authoritative; English translations are orientation only.

## Code of conduct

Be respectful. Estonian bureaucracy can frustrate; the repo's job is to demystify, not to vent. Keep PRs and issues focused on the procedural content.
````

- [ ] **Step 4: Sanity check**

Run: `. .venv/bin/activate && python scripts/check_no_pii.py`
Expected: `OK: no PII patterns found`.

Run: `ls README.md PRIVACY.md CONTRIBUTING.md`
Expected: all three present.

- [ ] **Step 5: Commit**

```bash
git add README.md PRIVACY.md CONTRIBUTING.md
git commit -m "Add full README, PRIVACY, and CONTRIBUTING docs"
```

---

## Task 12: CI workflow

**Files:**
- Create: `.github/workflows/validate.yml`

The workflow runs three validators on every push and PR: frontmatter schema, INDEX.yaml is in sync, and no PII has slipped in.

- [ ] **Step 1: Create `.github/workflows/validate.yml`**

```yaml
name: validate

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest -v

      - name: Validate skill frontmatter
        run: python scripts/validate_frontmatter.py

      - name: Check INDEX.yaml is in sync
        run: |
          python scripts/build_index.py
          if ! git diff --exit-code skills/estonia/INDEX.yaml; then
            echo "INDEX.yaml is out of sync. Run 'python scripts/build_index.py' and commit." >&2
            exit 1
          fi

      - name: PII scan
        run: python scripts/check_no_pii.py
```

- [ ] **Step 2: Verify the workflow file is valid YAML**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/validate.yml')); print('OK')"`
Expected: `OK`.

- [ ] **Step 3: Run the same checks locally to confirm they all pass before pushing**

```bash
. .venv/bin/activate && \
  pytest -v && \
  python scripts/validate_frontmatter.py && \
  python scripts/build_index.py && \
  git diff --exit-code skills/estonia/INDEX.yaml && \
  python scripts/check_no_pii.py
```
Expected: every command exits 0; `git diff` shows no changes (INDEX.yaml is already in sync).

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/validate.yml
git commit -m "Add CI: pytest + frontmatter + INDEX sync + PII scan"
```

---

## Final verification

- [ ] **Step 1: Confirm full repo state**

Run: `tree -L 3 --gitignore -I '.git|.venv|__pycache__|*.egg-info'`
Expected: structure matches the file tree at the top of this plan.

- [ ] **Step 2: Run all checks one more time**

```bash
. .venv/bin/activate && \
  pytest -v && \
  python scripts/validate_frontmatter.py && \
  python scripts/build_index.py && \
  git diff --exit-code skills/estonia/INDEX.yaml && \
  python scripts/check_no_pii.py
```
Expected: green across the board.

- [ ] **Step 3: List commits to confirm clean history**

Run: `git log --oneline`
Expected: ~13 commits (1 spec + 12 task commits), each message short and descriptive.

- [ ] **Step 4: Push to GitHub** (only after user creates the remote repo)

The user will create `github.com/<owner>/estonia-skills`. Then:

```bash
git remote add origin git@github.com:<owner>/estonia-skills.git
git push -u origin main
```

After push, the user can install locally to test:

```
/plugin marketplace add <owner>/estonia-skills
/plugin install estonia-skills@estonia-skills
/reload-plugins
```

And then ask Claude something like "How do I file my Estonian taxes?" — the router skill should activate.

---

## Self-review notes

**Spec coverage check (against `docs/superpowers/specs/2026-05-03-estonia-skills-design.md`):**

| Spec section | Plan task(s) |
|---|---|
| Repo layout | Tasks 1, 2, 3, 7–10, 11, 12 (every file accounted for) |
| Plugin manifests | Task 3 |
| Skill frontmatter schema | Task 5 (`validate_frontmatter.py` enforces) |
| Skill body conventions | Tasks 7–10 (each skill body follows the same shape) |
| Router skill | Task 7 |
| v1 skills (3) | Tasks 8, 9, 10 |
| Runtime freshness | Tasks 8–10 (every skill body has explicit fetch instructions) |
| Meta-freshness (`last_verified`) | Task 5 (validator checks date format) + Task 7 (router warns when stale) |
| MIT license | Task 1 |
| Disclaimer | Task 7 (`disclaimer.md`) referenced from each skill body |
| `PRIVACY.md` | Task 11 |
| `CONTRIBUTING.md` | Task 11 |
| Bürokratt acknowledgement | Task 11 (README) |
| CI validators | Task 12 |
| `build_index.py`, INDEX.yaml | Task 4 + Task 12 (sync check) |

**v2/v3 features (link checking, AI freshness bot)** are explicitly deferred per the spec — not in this plan.

**No placeholders.** Every step has actual content. The four "fetch and summarise the live procedure" steps in Tasks 8–10 are research instructions, not placeholders — they specify the URL, the section to extract, and the output shape.

**Type/name consistency:**
- `build_index` (function) and `scripts/build_index.py` (file) match.
- `validate_skill` and `ValidationError` consistent across Task 5.
- `scan` and `PIIFinding` consistent across Task 6.
- `freshness_sources` field name used consistently throughout.
- `last_verified` field name used consistently throughout.
- All metadata enums match between Task 5 (validator) and Task 7+ (skill bodies).

**Deviations from spec (intentional):**
- The spec's repo-layout diagram named the script `build-index.py` (kebab-case). The plan implements it as `build_index.py` (snake_case) because Python module names must be valid identifiers — hyphens would break `from build_index import build_index`. The contributor-facing command in `CONTRIBUTING.md` and the README also use the snake_case form. If you want to update the spec for consistency, change `build-index.py` → `build_index.py` in two places: the repo-layout block and the contributing-flow numbered list.
