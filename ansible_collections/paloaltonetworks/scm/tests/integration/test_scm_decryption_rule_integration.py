"""Integration tests for scm_decryption_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_decryption_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_decryption_rule, "scm_decryption_rule")

_FIELDS = dict(
    action=None, category=None, description=None, destination=None,
    destination_hip=None, disabled=None, from_=None, log_fail=None,
    log_setting=None, log_success=None, name=None,
    negate_destination=None, negate_source=None, profile=None,
    service=None, source=None, source_hip=None, source_user=None,
    tag=None, to_=None, type=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="decryption_rules requires position parameter and complex rule setup")
class TestDecryptionRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-decrule-{run_id}",
            action="no-decrypt",
            category=["any"],
            destination=["any"],
            from_=["any"],
            service=["any"],
            source=["any"],
            source_user=["any"],
            to_=["any"],
            type={"ssl_forward_proxy": {}},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestDecryptionRulesLifecycle._created_id = result["decryption_rule"]["id"]

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-decrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-decrule-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
