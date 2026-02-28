"""Integration tests for scm_logical_router — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_logical_router

logger = logging.getLogger(__name__)
run_module = make_runner(scm_logical_router, "scm_logical_router")

_FIELDS = dict(name=None, routing_stack=None, vrf=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestLogicalRoutersLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-lrouter-{run_id}",
            routing_stack="advanced",
            vrf=[{
                "name": "default",
                "routing_table": {
                    "ip": {
                        "static_route": [{
                            "name": "default-route",
                            "destination": "0.0.0.0/0",
                            "admin_dist": 10,
                            "nexthop": {"ip_address": "198.18.1.1"},
                        }]
                    }
                }
            }],
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestLogicalRoutersLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-lrouter-{run_id}",
            routing_stack="advanced",
            vrf=[{
                "name": "default",
                "routing_table": {
                    "ip": {
                        "static_route": [{
                            "name": "default-route",
                            "destination": "0.0.0.0/0",
                            "admin_dist": 10,
                            "nexthop": {"ip_address": "198.18.1.1"},
                        }]
                    }
                }
            }],
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-lrouter-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-lrouter-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-lrouter-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
