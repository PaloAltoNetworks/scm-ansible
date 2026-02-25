"""Integration tests for scm_internal_dns_servers — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_internal_dns_servers

logger = logging.getLogger(__name__)
run_module = make_runner(scm_internal_dns_servers, "scm_internal_dns_servers")

_FIELDS = dict(domain_name=None, name=None, primary=None, secondary=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestInternalDnsServersLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-idns-{run_id}",
            domain_name=["example.com"], primary="8.8.8.8",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestInternalDnsServersLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-idns-{run_id}",
            domain_name=["example.com"], primary="8.8.8.8",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-idns-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result.get("data", {}).get("id") == TestInternalDnsServersLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-idns-{run_id}",
            domain_name=["example.com"], primary="8.8.4.4",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"UPDATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_update_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-idns-{run_id}",
            domain_name=["example.com"], primary="8.8.4.4",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"UPDATE-IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_06_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-idns-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_07_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-idns-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"DELETE-IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
