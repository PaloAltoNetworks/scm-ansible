"""Integration tests for scm_layer3_subinterface — full CRUD lifecycle with parent interface."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ethernet_interface
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_layer3_subinterface

logger = logging.getLogger(__name__)
run_ethernet = make_runner(scm_ethernet_interface, "scm_ethernet_interface")
run_layer3_subinterface = make_runner(scm_layer3_subinterface, "scm_layer3_subinterface")

FOLDER = "All"


class TestLayer3SubinterfacesLifecycle:
    """Test Layer3 Subinterface with parent ethernet interface."""

    @pytest.fixture(autouse=True)
    def setup_parent_interface(self, run_id):
        """Create a Layer3 parent ethernet interface before tests."""
        parent_name = f"$an-l3parent-{run_id}"

        # Create Layer3 parent ethernet interface
        parent_result = run_ethernet(build_params({
            "state": "present",
            "name": parent_name,
            "folder": FOLDER,
            "comment": "L3 parent interface for subinterface test",
            "link_duplex": "full",
            "link_speed": "auto",
            "link_state": "up",
            "layer3": {},
        }))
        if parent_result.get("failed"):
            pytest.skip(f"Cannot create L3 parent interface: {parent_result.get('msg')}")

        self.parent_name = parent_name

        yield

        # Cleanup parent interface
        run_ethernet(build_params({
            "state": "absent",
            "name": parent_name,
            "folder": FOLDER,
        }))

    def test_01_create(self, run_id):
        """Create layer3 subinterface using the parent ethernet interface."""
        vlan_tag = 400
        subif_name = f"{self.parent_name}.{vlan_tag}"

        result = run_layer3_subinterface(build_params({
            "state": "present",
            "name": subif_name,
            "folder": FOLDER,
            "parent_interface": self.parent_name,
            "tag": vlan_tag,
            "mtu": 1400,
            "comment": "Test L3 subinterface",
            "ip": [{"name": "192.168.10.1/24"}],
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the layer3 subinterface."""
        vlan_tag = 400
        subif_name = f"{self.parent_name}.{vlan_tag}"

        result = run_layer3_subinterface(build_params({
            "state": "absent",
            "name": subif_name,
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        vlan_tag = 400
        subif_name = f"{self.parent_name}.{vlan_tag}"

        result = run_layer3_subinterface(build_params({
            "state": "absent",
            "name": subif_name,
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
