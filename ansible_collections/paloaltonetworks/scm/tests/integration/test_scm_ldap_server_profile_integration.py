"""Integration tests for scm_ldap_server_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ldap_server_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_ldap_server_profile, "scm_ldap_server_profile")

FOLDER = "All"


class TestLdapServerProfilesLifecycle:
    """Test LDAP Server Profile CRUD operations."""

    def test_01_create(self, run_id):
        """Create an LDAP server profile."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-ldap-{run_id}",
            "folder": FOLDER,
            "server": [{
                "name": "ldap-server-1",
                "address": "192.168.1.100",
                "port": 389,
            }],
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_create_idempotent(self, run_id):
        """Create again - should be idempotent."""
        result = run_module(build_params({
            "state": "present",
            "name": f"an-ldap-{run_id}",
            "folder": FOLDER,
            "server": [{
                "name": "ldap-server-1",
                "address": "192.168.1.100",
                "port": 389,
            }],
        }))
        logger.info(f"IDEMPOTENT CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent create failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        """Gather the LDAP server profile."""
        result = run_module(build_params({
            "state": "gathered",
            "name": f"an-ldap-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"

    def test_04_delete(self, run_id):
        """Delete the LDAP server profile."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-ldap-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-ldap-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
