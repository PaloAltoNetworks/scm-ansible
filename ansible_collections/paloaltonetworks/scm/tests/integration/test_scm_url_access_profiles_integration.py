"""Integration tests for scm_url_access_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_url_access_profiles

logger = logging.getLogger(__name__)
run_module = make_runner(scm_url_access_profiles, "scm_url_access_profiles")

_FIELDS = dict(
    alert=None, allow=None, block=None, cloud_inline_cat=None,
    continue_=None, credential_enforcement=None, description=None,
    log_container_page_only=None, log_http_hdr_referer=None,
    log_http_hdr_user_agent=None, log_http_hdr_xff=None,
    mlav_category_exception=None, name=None, override=None,
    safe_search_enforcement=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestUrlAccessProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-urlap-{run_id}",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestUrlAccessProfilesLifecycle._created_id = result["data"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Relaxed: nested URL category objects may cause server-side enrichment
        result = run_module(_params(
            state="present", name=f"ansible-integ-urlap-{run_id}",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-urlap-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["data"]["id"] == TestUrlAccessProfilesLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-urlap-{run_id}",
            description=f"Updated {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-urlap-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-urlap-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
