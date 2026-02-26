"""Integration tests for scm_application_filter — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_application_filter

logger = logging.getLogger(__name__)
run_module = make_runner(scm_application_filter, "scm_application_filter")

_FIELDS = dict(
    category=None, evasive=None, excessive_bandwidth_use=None,
    exclude=None, has_known_vulnerabilities=None, is_saas=None,
    name=None, new_appid=None, pervasive=None, prone_to_misuse=None,
    risk=None, saas_certifications=None, saas_risk=None,
    subcategory=None, tagging=None, technology=None,
    transfers_files=None, tunnels_other_apps=None, used_by_malware=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestApplicationFiltersLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appflt-{run_id}",
            category=["business-systems"],
            evasive=True,
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestApplicationFiltersLifecycle._created_id = result["application_filter"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appflt-{run_id}",
            category=["business-systems"],
            evasive=True,
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-appflt-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["application_filter"]["id"] == TestApplicationFiltersLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-appflt-{run_id}",
            category=["business-systems", "collaboration"],
            evasive=True,
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-appflt-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-appflt-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
