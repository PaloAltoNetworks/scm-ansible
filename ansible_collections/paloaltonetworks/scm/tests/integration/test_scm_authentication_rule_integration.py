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
    name=None, negate_destination=None, negate_source=None, service=None,
    source=None, source_hip=None, source_user=None, tag=None, timeout=None,
    to=None, var_from=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires position parameter for rules")
class TestAuthenticationRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-authrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-authrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-authrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
