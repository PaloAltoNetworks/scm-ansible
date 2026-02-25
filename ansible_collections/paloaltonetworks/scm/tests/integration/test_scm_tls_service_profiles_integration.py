"""Integration tests for scm_tls_service_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_tls_service_profiles

logger = logging.getLogger(__name__)
run_module = make_runner(scm_tls_service_profiles, "scm_tls_service_profiles")

_FIELDS = dict(certificate=None, name=None, protocol_settings=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestTlsServiceProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-tls-{run_id}",
            certificate="Forward-Trust-CA",
            protocol_settings={"keyxchg_algo_rsa": True},
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestTlsServiceProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-tls-{run_id}",
            certificate="Forward-Trust-CA",
            protocol_settings={"keyxchg_algo_rsa": True},
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-tls-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-tls-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-tls-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
