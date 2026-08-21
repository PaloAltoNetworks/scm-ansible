"""Integration tests for scm_authentication_setting — singleton device setting lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_setting

logger = logging.getLogger(__name__)
run_module = make_runner(scm_authentication_setting, "scm_authentication_setting")

_FIELDS = dict(authentication=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestAuthenticationSettingsLifecycle:
    """Test singleton device setting: gather and update only (no create/delete)."""

    def test_01_gather(self, run_id):
        """Gather the singleton setting - it should always exist."""
        result = run_module(_params(
            state="gathered",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        # Singleton should always exist
        assert result.get("authentication_setting"), "Singleton setting should exist"

    def test_02_update(self, run_id):
        """Update the singleton setting (no-op update to verify API works)."""
        result = run_module(_params(
            state="present",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"UPDATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"

    def test_03_update_idempotent(self, run_id):
        """Update again - should be idempotent (no change)."""
        result = run_module(_params(
            state="present",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        # Second update should not report changed
        assert not result.get("changed"), "Update should be idempotent"
