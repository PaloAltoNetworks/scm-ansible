"""Integration tests for scm_dns_security_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_dns_security_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_dns_security_profile, "scm_dns_security_profile")

_FIELDS = dict(botnet_domains=None, description=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestDnsSecurityProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-dnssec-{run_id}",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestDnsSecurityProfilesLifecycle._created_id = result["dns_security_profile"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-dnssec-{run_id}",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-dnssec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["dns_security_profile"]["id"] == TestDnsSecurityProfilesLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-dnssec-{run_id}",
            description=f"Updated {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-dnssec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-dnssec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
