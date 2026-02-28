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
    disabled=None, from_=None, group_tag=None, name=None,
    negate_destination=None, negate_source=None, port=None,
    protocol=None, source=None, tag=None, to_=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="application_override_rules requires position parameter and complex rule setup")
class TestApplicationOverrideRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-appoverrule-{run_id}",
            application="web-browsing",
            destination=["any"],
            from_=["any"],
            port="8080",
            protocol="tcp",
            source=["any"],
            to_=["any"],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestApplicationOverrideRulesLifecycle._created_id = result["application_override_rule"]["id"]

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-appoverrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-appoverrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
