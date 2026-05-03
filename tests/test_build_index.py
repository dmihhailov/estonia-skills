"""Tests for scripts/build_index.py."""

from pathlib import Path

import pytest
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


def test_build_index_skips_router(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    names = [entry["name"] for entry in data["skills"]]
    assert "estonia" not in names


def test_build_index_output_is_sorted_by_name(tmp_path, fixtures_dir):
    skills_dir = fixtures_dir / "skills"
    output = tmp_path / "INDEX.yaml"

    build_index(skills_dir, output)

    data = yaml.safe_load(output.read_text())
    names = [entry["name"] for entry in data["skills"]]
    assert names == sorted(names)


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


def test_build_index_raises_on_missing_frontmatter(tmp_path):
    bad_skill = tmp_path / "skills" / "broken" / "SKILL.md"
    bad_skill.parent.mkdir(parents=True)
    bad_skill.write_text("# No frontmatter here\n")
    output = tmp_path / "INDEX.yaml"

    with pytest.raises(ValueError, match="missing YAML frontmatter"):
        build_index(tmp_path / "skills", output)
