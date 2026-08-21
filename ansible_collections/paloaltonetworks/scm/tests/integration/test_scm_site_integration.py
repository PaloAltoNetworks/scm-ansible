"""Integration tests for scm_site — full CRUD lifecycle with dependencies."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ike_crypto_profile
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ike_gateway
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_ipsec_tunnel
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_remote_network
from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_site

logger = logging.getLogger(__name__)
run_ike_crypto = make_runner(scm_ike_crypto_profile, "scm_ike_crypto_profile")
run_ike_gateway = make_runner(scm_ike_gateway, "scm_ike_gateway")
run_ipsec_tunnel = make_runner(scm_ipsec_tunnel, "scm_ipsec_tunnel")
run_remote_network = make_runner(scm_remote_network, "scm_remote_network")
run_site = make_runner(scm_site, "scm_site")

RN_FOLDER = "Remote Networks"


class TestSitesLifecycle:
    """Test Site with full dependency chain."""

    @pytest.fixture(autouse=True)
    def setup_dependencies(self, run_id):
        """Create IKE Crypto Profile -> IKE Gateway -> IPsec Tunnel -> Remote Network."""
        crypto_name = f"an-ikecrypto-site-{run_id}"
        gateway_name = f"an-ikegw-site-{run_id}"
        tunnel_name = f"an-ipsectun-site-{run_id}"
        rn_name = f"an-rn-site-{run_id}"

        # Create IKE Crypto Profile
        crypto_result = run_ike_crypto(build_params({
            "state": "present",
            "name": crypto_name,
            "folder": RN_FOLDER,
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
            "folder": RN_FOLDER,
            "authentication": {"pre_shared_key": {"key": "secret123"}},
            "peer_address": {"ip": "2.2.2.8"},
            "peer_id": {"type": "ipaddr", "id": "10.3.3.8"},
            "local_id": {"type": "ipaddr", "id": "10.3.4.8"},
            "protocol": {
                "ikev1": {"ike_crypto_profile": crypto_name, "dpd": {"enable": True}},
                "ikev2": {"ike_crypto_profile": crypto_name, "dpd": {"enable": True}},
            },
        }))
        if gateway_result.get("failed"):
            run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": RN_FOLDER}))
            pytest.skip(f"Cannot create IKE Gateway: {gateway_result.get('msg')}")

        # Create IPsec Tunnel
        tunnel_result = run_ipsec_tunnel(build_params({
            "state": "present",
            "name": tunnel_name,
            "folder": RN_FOLDER,
            "anti_replay": True,
            "copy_tos": False,
            "enable_gre_encapsulation": False,
            "auto_key": {
                "ike_gateway": [{"name": gateway_name}],
                "ipsec_crypto_profile": "PaloAlto-Networks-IPSec-Crypto",
            },
        }))
        if tunnel_result.get("failed"):
            run_ike_gateway(build_params({"state": "absent", "name": gateway_name, "folder": RN_FOLDER}))
            run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": RN_FOLDER}))
            pytest.skip(f"Cannot create IPsec Tunnel: {tunnel_result.get('msg')}")

        # Create Remote Network
        rn_result = run_remote_network(build_params({
            "state": "present",
            "name": rn_name,
            "folder": RN_FOLDER,
            "region": "us-west-2",
            "spn_name": "us-west-dakota",
            "license_type": "FWAAS-AGGREGATE",
            "ipsec_tunnel": tunnel_name,
        }))
        if rn_result.get("failed"):
            run_ipsec_tunnel(build_params({"state": "absent", "name": tunnel_name, "folder": RN_FOLDER}))
            run_ike_gateway(build_params({"state": "absent", "name": gateway_name, "folder": RN_FOLDER}))
            run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": RN_FOLDER}))
            pytest.skip(f"Cannot create Remote Network: {rn_result.get('msg')}")

        self.crypto_name = crypto_name
        self.gateway_name = gateway_name
        self.tunnel_name = tunnel_name
        self.rn_name = rn_name

        yield

        # Cleanup in reverse order
        run_remote_network(build_params({"state": "absent", "name": rn_name, "folder": RN_FOLDER}))
        run_ipsec_tunnel(build_params({"state": "absent", "name": tunnel_name, "folder": RN_FOLDER}))
        run_ike_gateway(build_params({"state": "absent", "name": gateway_name, "folder": RN_FOLDER}))
        run_ike_crypto(build_params({"state": "absent", "name": crypto_name, "folder": RN_FOLDER}))

    def test_01_create(self, run_id):
        """Create site using the remote network dependency."""
        result = run_site(build_params({
            "state": "present",
            "name": f"an-site-{run_id}",
            "folder": "All",
            "city": "San Jose",
            "country": "US",
            "members": [{
                "name": self.rn_name,
                "mode": "active",
                "remote_network": self.rn_name,
            }],
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the site."""
        result = run_site(build_params({
            "state": "absent",
            "name": f"an-site-{run_id}",
            "folder": "All",
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_site(build_params({
            "state": "absent",
            "name": f"an-site-{run_id}",
            "folder": "All",
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
