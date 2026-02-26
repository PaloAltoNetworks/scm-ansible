"""Integration tests for scm_service_setting — device settings lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_service_setting

logger = logging.getLogger(__name__)
run_module = make_runner(scm_service_setting, "scm_service_setting")

_FIELDS = dict(services=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="singleton device setting, requires device context")
class TestServiceSettingsLifecycle:
    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
