"""Integration tests for scm_auto_tag_action — Create/Delete lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_auto_tag_action

logger = logging.getLogger(__name__)
run_module = make_runner(scm_auto_tag_action, "scm_auto_tag_action")

FOLDER = "Prisma Access"


@pytest.mark.skip(reason="auto_tag_action filter syntax validation is tenant-specific")
class TestAutoTagActionsLifecycle:
    """Test Auto Tag Action CRUD operations."""

    def test_01_create(self, run_id):
        """Create an auto tag action."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-autotag-{run_id}",
            "folder": FOLDER,
            "filter": "addr.src in 10.0.0.0/8",
            "log_type": "traffic",
            "actions": [{
                "name": "test-action",
                "type": {
                    "tagging": {
                        "action": "add-tag",
                        "tags": ["test-tag"],
                        "target": "source-address",
                    }
                },
            }],
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_gather(self, run_id):
        """Gather the auto tag action."""
        result = run_module(build_params({
            "state": "gathered",
            "name": f"an-autotag-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"

    def test_03_delete(self, run_id):
        """Delete the auto tag action."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-autotag-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_04_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-autotag-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
