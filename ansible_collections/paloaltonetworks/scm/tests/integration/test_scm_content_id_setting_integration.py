"""Integration tests for scm_content_id_setting — singleton device setting lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_content_id_setting

logger = logging.getLogger(__name__)
run_module = make_runner(scm_content_id_setting, "scm_content_id_setting")

_FIELDS = dict(content_id=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestContentIdSettingsLifecycle:
    """Test singleton device setting: gather and update only (no create/delete)."""

    @pytest.fixture(autouse=True)
    def ensure_singleton_exists(self, run_id):
        """Ensure singleton exists - create if not found, skip if create fails."""
        result = run_module(_params(state="gathered", folder=TARGET_FOLDER))
        if not result.get("content_id_setting"):
            # Try to create it
            create_result = run_module(_params(
                state="present",
                folder=TARGET_FOLDER,
                content_id={},
            ))
            if create_result.get("failed"):
                pytest.skip(f"Cannot create content_id_setting: {create_result.get('msg')}")

    def test_01_gather(self, run_id):
        """Gather the singleton setting."""
        result = run_module(_params(
            state="gathered",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result.get("content_id_setting"), "Singleton setting should exist"

    def test_02_update(self, run_id):
        """Update the singleton setting."""
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
        assert not result.get("changed"), "Update should be idempotent"
