"""Integration tests for scm_anti_spyware_signature — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_anti_spyware_signature

logger = logging.getLogger(__name__)
run_module = make_runner(scm_anti_spyware_signature, "scm_anti_spyware_signature")

_FIELDS = dict(
    bugtraq=None, comment=None, cve=None, default_action=None,
    direction=None, reference=None, severity=None, signature=None,
    threat_id=None, threatname=None, vendor=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestAntiSpywareSignaturesLifecycle:
    _created_id = None
    # Use threat_id in valid range: 15000-18000 or 6900001-7000000
    _threat_id = "6900100"

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present",
            threat_id=TestAntiSpywareSignaturesLifecycle._threat_id,
            threatname=f"an-aspysig-{run_id}",
            comment="Test anti-spyware signature for Ansible testing",
            severity="medium",
            direction="client2server",
            signature={"standard": [{"name": "std-sig-1", "scope": "protocol-data-unit"}]},
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestAntiSpywareSignaturesLifecycle._created_id = result["anti_spyware_signature"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present",
            threat_id=TestAntiSpywareSignaturesLifecycle._threat_id,
            threatname=f"an-aspysig-{run_id}",
            comment="Test anti-spyware signature for Ansible testing",
            severity="medium",
            direction="client2server",
            signature={"standard": [{"name": "std-sig-1", "scope": "protocol-data-unit"}]},
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered",
            threatname=f"an-aspysig-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent",
            threatname=f"an-aspysig-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent",
            threatname=f"an-aspysig-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
