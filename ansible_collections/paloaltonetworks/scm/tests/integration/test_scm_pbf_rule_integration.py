"""Integration tests for scm_pbf_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_pbf_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_pbf_rule, "scm_pbf_rule")

_FIELDS = dict(
    action=None, application=None, description=None, destination=None,
    enforce_symmetric_return=None, name=None, schedule=None,
    service=None, source=None, source_user=None, tag=None, var_from=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestPbfRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-pbf-{run_id}",
            var_from={"zone": ["trust"]},
            source=["192.168.10.0/24"],
            destination=["192.168.10.0/24"],
            application=["web-browsing"],
            service=["service-http"],
            action={"discard": {}},
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestPbfRulesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-pbf-{run_id}",
            var_from={"zone": ["trust"]},
            source=["192.168.10.0/24"],
            destination=["192.168.10.0/24"],
            application=["web-browsing"],
            service=["service-http"],
            action={"discard": {}},
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-pbf-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-pbf-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-pbf-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
