"""Integration tests for scm_authentication_portal — full CRUD lifecycle with dependencies."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_profile
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_portal

logger = logging.getLogger(__name__)
run_auth_profile = make_runner(scm_authentication_profile, "scm_authentication_profile")
run_auth_portal = make_runner(scm_authentication_portal, "scm_authentication_portal")

FOLDER = "All"
TEST_REDIRECT_HOST = "192.168.255.1"


@pytest.mark.skip(reason="authentication_portal is a singleton - existing portal blocks creation")
class TestAuthenticationPortalsLifecycle:
    """Test Authentication Portal with authentication profile dependency."""

    @pytest.fixture(autouse=True)
    def setup_auth_profile(self, run_id):
        """Create authentication profile before tests."""
        profile_name = f"an-authprof-portal-{run_id}"

        # Create authentication profile
        profile_result = run_auth_profile(build_params({
            "state": "present",
            "name": profile_name,
            "folder": FOLDER,
            "allow_list": ["all"],
            "method": {"local_database": {}},
        }))
        if profile_result.get("failed"):
            pytest.skip(f"Cannot create auth profile: {profile_result.get('msg')}")

        self.profile_name = profile_name

        yield

        # Cleanup auth profile
        run_auth_profile(build_params({
            "state": "absent",
            "name": profile_name,
            "folder": FOLDER,
        }))

    def test_01_create(self, run_id):
        """Create authentication portal using the auth profile dependency."""
        # First delete any existing portal (singleton per folder)
        run_auth_portal(build_params({
            "state": "absent",
            "folder": FOLDER,
            "redirect_host": TEST_REDIRECT_HOST,
        }))

        # Now create
        result = run_auth_portal(build_params({
            "state": "present",
            "folder": FOLDER,
            "redirect_host": TEST_REDIRECT_HOST,
            "authentication_profile": self.profile_name,
            "gp_udp_port": 10,
            "idle_timer": 10,
            "timer": 12,
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the authentication portal."""
        result = run_auth_portal(build_params({
            "state": "absent",
            "folder": FOLDER,
            "redirect_host": TEST_REDIRECT_HOST,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_auth_portal(build_params({
            "state": "absent",
            "folder": FOLDER,
            "redirect_host": TEST_REDIRECT_HOST,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
