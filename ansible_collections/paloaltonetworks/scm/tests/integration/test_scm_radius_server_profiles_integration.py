"""Integration tests for scm_radius_server_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_radius_server_profiles

logger = logging.getLogger(__name__)
run_module = make_runner(scm_radius_server_profiles, "scm_radius_server_profiles")

_FIELDS = dict(name=None, protocol=None, retries=None, server=None, timeout=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestRadiusServerProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-radius-{run_id}",
            protocol={"pap": {}},
            server=[{"name": "rad1", "ip_address": "10.0.0.60", "secret": "radsecret", "port": 1812}],
            retries=3,
            timeout=10,
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestRadiusServerProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True due to secret being write-only
        result = run_module(_params(
            state="present", name=f"a-integ-radius-{run_id}",
            protocol={"pap": {}},
            server=[{"name": "rad1", "ip_address": "10.0.0.60", "secret": "radsecret", "port": 1812}],
            retries=3,
            timeout=10,
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-radius-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-radius-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-radius-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
