"""Integration tests for scm_qos_rules — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_qos_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_qos_rule, "scm_qos_rule")

_FIELDS = dict(
    action=None, application=None, description=None,
    dscp_tos=None, name=None, position=None, schedule=None, source=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestQoSRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-qosrule-{run_id}",
            position="pre",
            action={"class": "1"},
            description="Test QoS rule for Ansible testing",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestQoSRulesLifecycle._created_id = result["qos_rule"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-qosrule-{run_id}",
            position="pre",
            action={"class": "1"},
            description="Test QoS rule for Ansible testing",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-qosrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-qosrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-qosrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
