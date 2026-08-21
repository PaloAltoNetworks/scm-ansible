"""Integration tests for scm_qos_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_qos_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_qos_profile, "scm_qos_profile")

_FIELDS = dict(aggregate_bandwidth=None, class_bandwidth_type=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestQoSProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-qos-{run_id}",
            class_bandwidth_type={
                "mbps": {
                    "var_class": [
                        {"name": "class1", "priority": "low"},
                        {
                            "name": "class2", "priority": "real-time",
                            "class_bandwidth": {"egress_guaranteed": 10, "egress_max": 20},
                        },
                    ]
                }
            },
            aggregate_bandwidth={"egress_guaranteed": 300, "egress_max": 1000},
            folder="Service Connections",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestQoSProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-qos-{run_id}",
            class_bandwidth_type={
                "mbps": {
                    "var_class": [
                        {"name": "class1", "priority": "low"},
                        {
                            "name": "class2", "priority": "real-time",
                            "class_bandwidth": {"egress_guaranteed": 10, "egress_max": 20},
                        },
                    ]
                }
            },
            aggregate_bandwidth={"egress_guaranteed": 300, "egress_max": 1000},
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-qos-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-qos-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-qos-{run_id}",
            folder="Service Connections",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
