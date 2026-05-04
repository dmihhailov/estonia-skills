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


def test_validate_accepts_yaml_list_audience():
    """A contributor may write audience as a YAML-native list, not a comma string."""
    fm = _skill_with({"audience": ["citizen", "resident"]})
    validate_skill(fm)  # should not raise


def test_validate_rejects_invalid_value_in_comma_list():
    """Each item in a comma-separated list must independently be in the allowed set."""
    fm = _skill_with({"auth_required": "smart-id,bogus"})
    with pytest.raises(ValidationError, match="auth_required"):
        validate_skill(fm)


def test_validate_rejects_missing_top_level_field():
    """Top-level fields (license, name, description, metadata) are also required."""
    fm = _skill_with({})
    del fm["license"]
    with pytest.raises(ValidationError, match="license"):
        validate_skill(fm)


def test_parse_frontmatter_raises_on_malformed_yaml(tmp_path):
    from validate_frontmatter import _parse_frontmatter

    bad_skill = tmp_path / "SKILL.md"
    bad_skill.write_text("---\nname: [unclosed\n---\n# body\n")

    with pytest.raises(ValidationError, match="invalid YAML in frontmatter"):
        _parse_frontmatter(bad_skill)
