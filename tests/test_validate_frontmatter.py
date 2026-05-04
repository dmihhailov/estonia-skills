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
