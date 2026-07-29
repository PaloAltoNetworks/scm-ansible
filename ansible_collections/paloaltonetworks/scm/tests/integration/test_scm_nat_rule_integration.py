"""Integration tests for scm_nat_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_nat_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_nat_rule, "scm_nat_rule")

_FIELDS = dict(
    active_active_device_binding=None, description=None,
    destination=None, destination_translation=None,
    disabled=None, var_from=None, name=None, nat_type=None,
    position=None, service=None, source=None, source_translation=None,
    tag=None, to=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestNatRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-natrule-{run_id}",
            position="pre",
            var_from=["any"],
            to=["untrust"],
            source=["any"],
            destination=["any"],
            service="service-https",
            nat_type="ipv4",
            destination_translation={"translated_address": "10.1.1.10", "translated_port": 443, "dns_rewrite": {"direction": "reverse"}},
            source_translation={"dynamic_ip_and_port": {"translated_address": ["10.1.1.20", "10.2.2.23"]}},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestNatRulesLifecycle._created_id = result["nat_rule"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-natrule-{run_id}",
            position="pre",
            var_from=["any"],
            to=["untrust"],
            source=["any"],
            destination=["any"],
            service="service-https",
            nat_type="ipv4",
            destination_translation={"translated_address": "10.1.1.10", "translated_port": 443, "dns_rewrite": {"direction": "reverse"}},
            source_translation={"dynamic_ip_and_port": {"translated_address": ["10.1.1.20", "10.2.2.23"]}},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-natrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-natrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-natrule-{run_id}",
            position="pre",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
