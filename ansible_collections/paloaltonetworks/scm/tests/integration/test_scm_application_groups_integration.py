"""Integration tests for scm_application_groups — full CRUD lifecycle.

Uses built-in application names as members (no setup required).
"""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_application_groups

logger = logging.getLogger(__name__)
run_module = make_runner(scm_application_groups, "scm_application_groups")

_FIELDS = dict(members=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestApplicationGroupsLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appgrp-{run_id}",
            members=["web-browsing", "ssl"],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestApplicationGroupsLifecycle._created_id = result["data"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appgrp-{run_id}",
            members=["web-browsing", "ssl"],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-appgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["data"]["id"] == TestApplicationGroupsLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appgrp-{run_id}",
            members=["web-browsing", "ssl", "dns"],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-appgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-appgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
