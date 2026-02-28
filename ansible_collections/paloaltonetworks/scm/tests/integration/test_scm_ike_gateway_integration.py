"""Integration tests for scm_ike_gateway — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ike_gateway

logger = logging.getLogger(__name__)
run_module = make_runner(scm_ike_gateway, "scm_ike_gateway")

_FIELDS = dict(
    authentication=None, local_id=None, name=None,
    peer_address=None, peer_id=None, protocol=None,
    protocol_common=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires complex VPN setup with peer addresses")
class TestIkeGatewaysLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-ikegw-{run_id}",
            authentication={"pre_shared_key": {"key": "secret123"}},
            peer_address={"ip": "1.1.1.1"},
            protocol={"ikev1": {"ike_crypto_profile": "default"}, "version": "ikev1"},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-ikegw-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-ikegw-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
