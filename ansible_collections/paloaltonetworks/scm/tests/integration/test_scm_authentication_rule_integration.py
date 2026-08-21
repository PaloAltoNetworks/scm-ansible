"""Integration tests for scm_authentication_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_authentication_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_authentication_rule, "scm_authentication_rule")

_FIELDS = dict(
    authentication_enforcement=None, category=None, description=None,
    destination=None, destination_hip=None, disabled=None, group_tag=None,
    hip_profiles=None, log_authentication_timeout=None, log_setting=None,
    name=None, negate_destination=None, negate_source=None, position=None,
    service=None, source=None, source_hip=None, source_user=None, tag=None,
    timeout=None, to=None, var_from=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestAuthenticationRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-authrule-{run_id}",
            position="pre",
            destination=["any"],
            var_from=["any"],
            service=["any"],
            source=["any"],
            to=["any"],
            timeout=1000,
            description="Test authentication rule for Ansible testing",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestAuthenticationRulesLifecycle._created_id = result["authentication_rule"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-authrule-{run_id}",
            position="pre",
            destination=["any"],
            var_from=["any"],
            service=["any"],
            source=["any"],
            to=["any"],
            timeout=1000,
            description="Test authentication rule for Ansible testing",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-authrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-authrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-authrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
