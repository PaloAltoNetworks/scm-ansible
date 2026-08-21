"""Integration tests for scm_ipsec_tunnel — full CRUD lifecycle with dependencies."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ike_crypto_profile
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ike_gateway
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ipsec_tunnel

logger = logging.getLogger(__name__)
run_ike_crypto = make_runner(scm_ike_crypto_profile, "scm_ike_crypto_profile")
run_ike_gateway = make_runner(scm_ike_gateway, "scm_ike_gateway")
run_ipsec_tunnel = make_runner(scm_ipsec_tunnel, "scm_ipsec_tunnel")

FOLDER = "Remote Networks"


class TestIPsecTunnelsLifecycle:
    """Test IPsec tunnel with dependency chain: IKE Crypto Profile -> IKE Gateway -> IPsec Tunnel."""

    @pytest.fixture(autouse=True)
    def setup_dependencies(self, run_id):
        """Create IKE Crypto Profile and IKE Gateway before tests, cleanup after."""
        crypto_name = f"an-ikecrypto-{run_id}"
        gateway_name = f"an-ikegw-{run_id}"

        # Create IKE Crypto Profile
        crypto_result = run_ike_crypto(build_params({
            "state": "present",
            "name": crypto_name,
            "folder": FOLDER,
            "hash": ["sha256"],
            "dh_group": ["group14"],
            "encryption": ["aes-256-cbc"],
        }))
        if crypto_result.get("failed"):
            pytest.skip(f"Cannot create IKE Crypto Profile: {crypto_result.get('msg')}")

        # Create IKE Gateway
        gateway_result = run_ike_gateway(build_params({
            "state": "present",
            "name": gateway_name,
            "folder": FOLDER,
            "authentication": {"pre_shared_key": {"key": "secret123"}},
            "peer_address": {"ip": "2.2.2.4"},
            "peer_id": {"type": "ipaddr", "id": "10.3.3.4"},
            "local_id": {"type": "ipaddr", "id": "10.3.4.4"},
            "protocol": {
                "ikev1": {"ike_crypto_profile": crypto_name, "dpd": {"enable": True}},
                "ikev2": {"ike_crypto_profile": crypto_name, "dpd": {"enable": True}},
            },
        }))
        if gateway_result.get("failed"):
            # Cleanup crypto profile
            run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": FOLDER}))
            pytest.skip(f"Cannot create IKE Gateway: {gateway_result.get('msg')}")

        self.crypto_name = crypto_name
        self.gateway_name = gateway_name

        yield

        # Cleanup in reverse order
        run_ike_gateway(build_params({"state": "absent", "name": gateway_name, "folder": FOLDER}))
        run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": FOLDER}))

    def test_01_create(self, run_id):
        """Create IPsec tunnel using the IKE gateway dependency."""
        result = run_ipsec_tunnel(build_params({
            "state": "present",
            "name": f"an-ipsectun-{run_id}",
            "folder": FOLDER,
            "anti_replay": True,
            "copy_tos": False,
            "enable_gre_encapsulation": False,
            "auto_key": {
                "ike_gateway": [{"name": self.gateway_name}],
                "ipsec_crypto_profile": "PaloAlto-Networks-IPSec-Crypto",
            },
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the IPsec tunnel."""
        result = run_ipsec_tunnel(build_params({
            "state": "absent",
            "name": f"an-ipsectun-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_ipsec_tunnel(build_params({
            "state": "absent",
            "name": f"an-ipsectun-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
