"""Integration tests for scm_application — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_application

logger = logging.getLogger(__name__)
run_module = make_runner(scm_application, "scm_application")

_FIELDS = dict(
    able_to_transfer_file=None, alg_disable_capability=None,
    category=None, consume_big_bandwidth=None, data_ident=None,
    default=None, description=None, evasive_behavior=None,
    file_type_ident=None, has_known_vulnerability=None, name=None,
    no_appid_caching=None, parent_app=None, pervasive_use=None,
    prone_to_misuse=None, risk=None, signature=None, subcategory=None,
    tcp_half_closed_timeout=None, tcp_time_wait_timeout=None,
    tcp_timeout=None, technology=None, timeout=None,
    tunnel_applications=None, tunnel_other_application=None,
    udp_timeout=None, used_by_malware=None, virus_ident=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestApplicationsLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-app-{run_id}",
            category="business-systems",
            subcategory="ics-protocols",
            technology="client-server",
            risk="1",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestApplicationsLifecycle._created_id = result["application"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True because the API returns
        # enriched fields (defaults like timeout, tcp_timeout, etc.)
        result = run_module(_params(
            state="present", name=f"an-app-{run_id}",
            category="business-systems",
            subcategory="ics-protocols",
            technology="client-server",
            risk="1",
            description=f"Integration test {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-app-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["application"]["id"] == TestApplicationsLifecycle._created_id

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-app-{run_id}",
            category="business-systems",
            subcategory="ics-protocols",
            technology="client-server",
            risk="2",
            description=f"Updated {run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-app-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-app-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
