"""Integration tests for scm_traffic_steering_rule — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_traffic_steering_rule

logger = logging.getLogger(__name__)
run_module = make_runner(scm_traffic_steering_rule, "scm_traffic_steering_rule")

_FIELDS = dict(
    action=None, category=None, destination=None, name=None,
    service=None, source=None, source_user=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestTrafficSteeringRulesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-tsr-{run_id}",
            action={"no-pbf": {}},
            service=["any"],
            source=["any"],
            folder="Service Connections",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestTrafficSteeringRulesLifecycle._created_id = result["traffic_steering_rule"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-tsr-{run_id}",
            action={"no-pbf": {}},
            service=["any"],
            source=["any"],
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-tsr-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-tsr-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-tsr-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
