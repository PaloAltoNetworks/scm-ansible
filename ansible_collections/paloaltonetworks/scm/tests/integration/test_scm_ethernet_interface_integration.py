"""Integration tests for scm_ethernet_interface — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ethernet_interface

logger = logging.getLogger(__name__)
run_module = make_runner(scm_ethernet_interface, "scm_ethernet_interface")

_FIELDS = dict(
    comment=None, ha=None, layer2=None, layer3=None,
    link_duplex=None, link_speed=None, link_state=None,
    name=None, poe=None, tap=None, virtual_wire=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestEthernetInterfacesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"$an-ethif-{run_id}",
            folder="All",
            comment="Test Ethernet Interface",
            link_duplex="full",
            link_speed="auto",
            link_state="up",
            layer2={},
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"$an-ethif-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"$an-ethif-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
