"""Shared pytest fixtures for SCM Ansible integration tests."""

import os
import sys

# Ensure the integration test directory is on sys.path so helpers can be imported
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from helpers import RUN_ID, has_credentials


@pytest.fixture(scope="session", autouse=True)
def require_credentials():
    """Skip all tests if no SCM credentials are available."""
    if not has_credentials():
        pytest.skip(
            "No SCM credentials found. Set SCM_CLIENT_ID/SCM_CLIENT_SECRET env vars, "
            "or SCM_CONFIG_FILE, or create config/scm-config.json"
        )


@pytest.fixture(scope="session")
def run_id():
    """Unique ID for this test run (shared across all test files)."""
    return RUN_ID
