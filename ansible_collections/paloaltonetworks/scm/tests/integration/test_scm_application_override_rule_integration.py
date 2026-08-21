"""Integration tests for scm_application_override_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_application_override_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_application_override_rule, "scm_application_override_rule")

_FIELDS = dict(
    application=None, description=None, destination=None,
    disabled=None, var_from=None, group_tag=None, name=None,
    negate_destination=None, negate_source=None, port=None,
    position=None, protocol=None, source=None, tag=None, to=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestApplicationOverrideRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-appoverrule-{run_id}",
            position="pre",
            application="web-browsing",
            destination=["any"],
            var_from=["any"],
            port="8080",
            protocol="tcp",
            source=["any"],
            to=["any"],
            description="Test app override rule for Ansible testing",
            folder="All",  # Use "All" folder for app override rules per SDK tests
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        # Store ID if present (may not be returned by SDK due to readOnly exclusion)
        TestApplicationOverrideRulesLifecycle._created_id = result["application_override_rule"].get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-appoverrule-{run_id}",
            position="pre",
            application="web-browsing",
            destination=["any"],
            var_from=["any"],
            port="8080",
            protocol="tcp",
            source=["any"],
            to=["any"],
            description="Test app override rule for Ansible testing",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-appoverrule-{run_id}",
            position="pre",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-appoverrule-{run_id}",
            position="pre",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-appoverrule-{run_id}",
            position="pre",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
