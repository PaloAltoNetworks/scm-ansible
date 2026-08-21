"""Integration tests for scm_dos_protection_rule — CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_dos_protection_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_dos_protection_rule, "scm_dos_protection_rule")

FOLDER = "All"


@pytest.mark.skip(reason="dos_protection_rule API requires from/to as objects - model has from/to as string arrays causing 400 Bad Request")
class TestDoSProtectionRulesLifecycle:
    """Test DoS Protection Rule CRUD operations."""

    def test_01_create(self, run_id):
        """Create a DoS protection rule."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-dosrule-{run_id}",
            "folder": FOLDER,
            "var_from": ["any"],
            "to": ["any"],
            "source": ["any"],
            "destination": ["any"],
            "service": ["any"],
            "protection": {},
            "action": {"protect": {}},
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the DoS protection rule."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-dosrule-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-dosrule-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
