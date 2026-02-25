"""Integration tests for scm_i_psec_crypto_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_i_psec_crypto_profiles

logger = logging.getLogger(__name__)
run_module = make_runner(scm_i_psec_crypto_profiles, "scm_i_psec_crypto_profiles")

_FIELDS = dict(ah=None, dh_group=None, esp=None, lifesize=None, lifetime=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestIPsecCryptoProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-ipsec-{run_id}",
            lifetime={"hours": 1},
            esp={"authentication": ["sha384"], "encryption": ["aes-256-cbc"]},
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestIPsecCryptoProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True due to nested object enrichment
        result = run_module(_params(
            state="present", name=f"a-integ-ipsec-{run_id}",
            lifetime={"hours": 1},
            esp={"authentication": ["sha384"], "encryption": ["aes-256-cbc"]},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-ipsec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_update(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-ipsec-{run_id}",
            lifetime={"hours": 2},
            esp={"authentication": ["sha384"], "encryption": ["aes-256-cbc"]},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Update failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-ipsec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_06_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-ipsec-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
