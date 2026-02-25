"""Integration tests for scm_remote_networks — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_remote_networks

logger = logging.getLogger(__name__)
run_module = make_runner(scm_remote_networks, "scm_remote_networks")

_FIELDS = dict(
    ecmp_load_balancing=None, ecmp_tunnels=None, ipsec_tunnel=None,
    license_type=None, name=None, protocol=None, region=None,
    secondary_ipsec_tunnel=None, spn_name=None, subnets=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires IPsec tunnel and region infrastructure")
class TestRemoteNetworksLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-rn-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestRemoteNetworksLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-rn-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-rn-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
