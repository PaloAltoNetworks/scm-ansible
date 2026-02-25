"""Integration tests for scm_auto_tag_actions — Create/Delete lifecycle.

This resource has limited CRUD: Create, Delete, Fetch only (no Get/Update).
"""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_auto_tag_actions

logger = logging.getLogger(__name__)
run_module = make_runner(scm_auto_tag_actions, "scm_auto_tag_actions")

_FIELDS = dict(
    actions=None, description=None, filter=None,
    log_type=None, name=None, quarantine=None, send_to_panorama=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="auto_tag_actions has complex nested Pydantic models that require special handling")
class TestAutoTagActionsLifecycle:

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-ata-{run_id}",
            log_type="traffic",
            filter="All Logs",
            actions=[{
                "name": "test-action",
                "type": "tagging",
                "action": "add-tag",
                "target": "source-address",
                "tags": ["test-tag"],
            }],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-ata-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_03_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-ata-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_04_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-ata-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
