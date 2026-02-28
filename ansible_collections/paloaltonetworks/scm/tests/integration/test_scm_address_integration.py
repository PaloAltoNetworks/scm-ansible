"""Integration tests for scm_address — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_address

logger = logging.getLogger(__name__)
run_module = make_runner(scm_address, "scm_address")

# All fields this module accepts (set unused ones to None)
_FIELDS = dict(
    description=None, fqdn=None, ip_netmask=None,
    ip_range=None, ip_wildcard=None, name=None, tag=None,
)


def _params(**overrides):
    p = build_params({**_FIELDS, **overrides}, has_containers=True)
    return p


class TestAddressesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-addr-{run_id}",
            ip_netmask="10.99.0.1/32", description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        assert result["address"]["name"] == f"an-addr-{run_id}"
        TestAddressesLifecycle._created_id = result["address"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-addr-{run_id}",
            ip_netmask="10.99.0.1/32", description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather_by_name(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-addr-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"GATHER: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["address"]["id"] == TestAddressesLifecycle._created_id

    def test_04_gather_by_id(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-addr-{run_id}",
            id=TestAddressesLifecycle._created_id,
        ))
        logger.info(f"GATHER-BY-ID: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Gather-by-ID failed: {result.get('msg')}"
        assert result["address"]["id"] == TestAddressesLifecycle._created_id

    def test_05_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-addr-{run_id}",
            ip_netmask="10.99.0.1/32", description=f"Updated {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"UPDATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_update_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-addr-{run_id}",
            ip_netmask="10.99.0.1/32", description=f"Updated {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"UPDATE-IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_07_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-addr-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_08_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-addr-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"DELETE-IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_09_gather_after_delete(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-addr-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"GATHER-DELETED: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed")
        assert "not found" in result["msg"]
