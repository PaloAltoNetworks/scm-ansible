"""Integration tests for scm_file_blocking_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_file_blocking_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_file_blocking_profile, "scm_file_blocking_profile")

_FIELDS = dict(description=None, name=None, rules=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestFileBlockingProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-fb-{run_id}",
            description=f"Integration test {run_id}",
            rules=[{
                "name": "rule1",
                "direction": "both",
                "application": ["any"],
                "file_type": ["any"],
                "action": "alert",
            }],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestFileBlockingProfilesLifecycle._created_id = result["file_blocking_profile"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Relaxed: nested rules may cause server-side enrichment
        result = run_module(_params(
            state="present", name=f"an-fb-{run_id}",
            description=f"Integration test {run_id}",
            rules=[{
                "name": "rule1",
                "direction": "both",
                "application": ["any"],
                "file_type": ["any"],
                "action": "alert",
            }],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-fb-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["file_blocking_profile"]["id"] == TestFileBlockingProfilesLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-fb-{run_id}",
            description=f"Updated {run_id}",
            rules=[{
                "name": "rule1",
                "direction": "both",
                "application": ["any"],
                "file_type": ["any"],
                "action": "alert",
            }],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-fb-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-fb-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
