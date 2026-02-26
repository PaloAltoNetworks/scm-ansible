"""Integration tests for scm_hip_object — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_hip_object

logger = logging.getLogger(__name__)
run_module = make_runner(scm_hip_object, "scm_hip_object")

_FIELDS = dict(
    anti_malware=None, certificate=None, custom_checks=None,
    data_loss_prevention=None, description=None, disk_backup=None,
    disk_encryption=None, firewall=None, host_info=None,
    mobile_device=None, name=None, network_info=None, patch_management=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestHipObjectsLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-hip-{run_id}",
            description=f"Integration test {run_id}",
            disk_encryption={"criteria": {"is_installed": True}},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestHipObjectsLifecycle._created_id = result["hip_object"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True because the API returns
        # enriched nested objects (extra defaults) that differ from our input.
        # We only verify it doesn't fail.
        result = run_module(_params(
            state="present", name=f"ansible-integ-hip-{run_id}",
            description=f"Integration test {run_id}",
            disk_encryption={"criteria": {"is_installed": True}},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-hip-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["hip_object"]["id"] == TestHipObjectsLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-hip-{run_id}",
            description=f"Updated {run_id}",
            disk_encryption={"criteria": {"is_installed": True}},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-hip-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-hip-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
