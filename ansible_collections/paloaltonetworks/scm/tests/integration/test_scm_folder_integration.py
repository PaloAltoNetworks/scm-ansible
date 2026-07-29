"""Integration tests for scm_folder — CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_folder

logger = logging.getLogger(__name__)
run_module = make_runner(scm_folder, "scm_folder")


@pytest.mark.skip(reason="folder API returns 500 Internal Server Error")
class TestFoldersLifecycle:
    """Test Folder CRUD operations."""

    def test_01_create(self, run_id):
        """Create a folder."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-folder-{run_id}",
            "parent": "Shared",
            "description": "Integration test folder",
        }, has_containers=False))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_create_idempotent(self, run_id):
        """Create again - should be idempotent."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-folder-{run_id}",
            "parent": "Shared",
            "description": "Integration test folder",
        }, has_containers=False))
        logger.info(f"IDEMPOTENT CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent create failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        """Gather the folder."""
        result = run_module(build_params({
            "state": "gathered",
            "name": f"an-folder-{run_id}",
        }, has_containers=False))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"

    def test_04_update(self, run_id):
        """Update the folder description."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-folder-{run_id}",
            "parent": "Shared",
            "description": "Updated integration test folder",
        }, has_containers=False))
        logger.info(f"UPDATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        """Delete the folder."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-folder-{run_id}",
        }, has_containers=False))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-folder-{run_id}",
        }, has_containers=False))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
