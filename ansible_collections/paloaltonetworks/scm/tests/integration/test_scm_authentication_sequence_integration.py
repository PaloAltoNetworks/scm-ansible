"""Integration tests for scm_authentication_sequence — full CRUD lifecycle.

Requires creating a prerequisite authentication profile first.
"""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_sequence
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_authentication_sequence, "scm_authentication_sequence")
run_auth_profile = make_runner(scm_authentication_profile, "scm_authentication_profile")

_FIELDS = dict(
    authentication_profiles=None, name=None, use_domain_find_profile=None,
)

_PROFILE_FIELDS = dict(
    allow_list=None, lockout=None, method=None, multi_factor_auth=None,
    name=None, single_sign_on=None, user_domain=None, username_modifier=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


def _profile_params(**overrides):
    return build_params({**_PROFILE_FIELDS, **overrides})


class TestAuthenticationSequencesLifecycle:
    _created_id = None
    _profile_name = None

    def test_00_setup_auth_profile(self, run_id):
        """Create prerequisite authentication profile."""
        TestAuthenticationSequencesLifecycle._profile_name = f"a-integ-authprof-{run_id}"
        result = run_auth_profile(_profile_params(
            state="present",
            name=TestAuthenticationSequencesLifecycle._profile_name,
            allow_list=["all"],
            method={"local_database": {}},
            folder="All",
        ))
        logger.info(f"SETUP AUTH PROFILE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Auth profile setup failed: {result.get('msg')}"

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-authseq-{run_id}",
            authentication_profiles=[TestAuthenticationSequencesLifecycle._profile_name],
            use_domain_find_profile=False,
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestAuthenticationSequencesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-authseq-{run_id}",
            authentication_profiles=[TestAuthenticationSequencesLifecycle._profile_name],
            use_domain_find_profile=False,
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-authseq-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-authseq-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-authseq-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_06_cleanup_auth_profile(self, run_id):
        """Delete prerequisite authentication profile."""
        result = run_auth_profile(_profile_params(
            state="absent",
            name=TestAuthenticationSequencesLifecycle._profile_name,
            folder="All",
        ))
        logger.info(f"CLEANUP AUTH PROFILE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Auth profile cleanup failed: {result.get('msg')}"
