"""Regenerate skills/estonia/INDEX.yaml from each SKILL.md's frontmatter.

Walks <skills_dir>/*/SKILL.md, parses YAML frontmatter, skips the 'estonia'
router directory itself, and writes a sorted list of skill records to the
output file. Run from repo root: python scripts/build_index.py
"""

from pathlib import Path

import yaml


ROUTER_DIR_NAME = "estonia"
LIST_FIELDS_COMMA = {"audience", "auth_required"}
LIST_FIELDS_PIPE = {"freshness_sources"}


def _parse_frontmatter(skill_md: Path) -> dict:
    # utf-8-sig silently strips a leading UTF-8 BOM if present.
    text = skill_md.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        raise ValueError(f"{skill_md}: missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{skill_md}: malformed frontmatter")
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"{skill_md}: invalid YAML in frontmatter: {exc}") from exc


def _normalize_metadata(metadata: dict) -> dict:
    out = {}
    for key, value in metadata.items():
        if key in LIST_FIELDS_COMMA and isinstance(value, str):
            out[key] = [item.strip() for item in value.split(",") if item.strip()]
        elif key in LIST_FIELDS_PIPE and isinstance(value, str):
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
        try:
            name = fm["name"]
        except KeyError:
            raise ValueError(f"{skill_md}: missing required 'name' field in frontmatter") from None
        entries.append({
            "name": name,
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
