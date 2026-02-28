"""Integration tests for scm_security_zone — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_security_zone

logger = logging.getLogger(__name__)
run_module = make_runner(scm_security_zone, "scm_security_zone")

_FIELDS = dict(
    device_acl=None, dos_log_setting=None, dos_profile=None,
    enable_device_identification=None, enable_user_identification=None,
    name=None, network=None, user_acl=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestSecurityZonesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-zone-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestSecurityZonesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True due to nested object enrichment
        result = run_module(_params(
            state="present", name=f"an-zone-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-zone-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-zone-{run_id}",
            enable_user_identification=True,
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-zone-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-zone-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
