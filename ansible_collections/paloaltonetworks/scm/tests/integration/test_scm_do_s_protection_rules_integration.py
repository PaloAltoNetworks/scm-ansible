"""Integration tests for scm_do_s_protection_rules — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_do_s_protection_rules

logger = logging.getLogger(__name__)
run_module = make_runner(scm_do_s_protection_rules, "scm_do_s_protection_rules")

_FIELDS = dict(
    action=None, description=None, destination=None,
    disabled=None, from_=None, log_setting=None, name=None,
    negate_destination=None, negate_source=None, protection=None,
    schedule=None, service=None, source=None, source_user=None,
    tag=None, to_=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="do_s_protection_rules requires position parameter and complex rule setup")
class TestDoSProtectionRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-dosrule-{run_id}",
            action={"protect": {}},
            destination=["any"],
            from_=["any"],
            service=["any"],
            source=["any"],
            to_=["any"],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestDoSProtectionRulesLifecycle._created_id = result["data"]["id"]

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-dosrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-dosrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
