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
    # utf-8-sig silently strips a leading UTF-8 BOM if present.
    text = skill_md.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        raise ValidationError(f"{skill_md}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValidationError(f"{skill_md}: malformed frontmatter")
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ValidationError(f"{skill_md}: invalid YAML in frontmatter: {exc}") from exc


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
