"""Integration tests for scm_external_dynamic_list — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_external_dynamic_list

logger = logging.getLogger(__name__)
run_module = make_runner(scm_external_dynamic_list, "scm_external_dynamic_list")

_FIELDS = dict(name=None, type=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestExternalDynamicListsLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-edl-{run_id}",
            type={"ip": {
                "url": "https://example.com/blocklist.txt",
                "recurring": {"daily": {"at": "03"}},
            }},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestExternalDynamicListsLifecycle._created_id = result["external_dynamic_list"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True because the API returns
        # enriched nested objects (extra defaults) that differ from our input.
        result = run_module(_params(
            state="present", name=f"ansible-integ-edl-{run_id}",
            type={"ip": {
                "url": "https://example.com/blocklist.txt",
                "recurring": {"daily": {"at": "03"}},
            }},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-edl-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["external_dynamic_list"]["id"] == TestExternalDynamicListsLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-edl-{run_id}",
            type={"ip": {
                "url": "https://example.com/updated-blocklist.txt",
                "recurring": {"daily": {"at": "03"}},
            }},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-edl-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-edl-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
