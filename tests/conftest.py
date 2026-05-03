"""Shared pytest fixtures for estonia-skills tests."""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"
