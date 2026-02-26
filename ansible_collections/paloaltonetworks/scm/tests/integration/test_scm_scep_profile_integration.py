"""Integration tests for scm_scep_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_scep_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_scep_profile, "scm_scep_profile")

_FIELDS = dict(
    algorithm=None, ca_identity_name=None, certificate_attributes=None,
    digest=None, fingerprint=None, name=None, scep_ca_cert=None,
    scep_challenge=None, scep_client_cert=None, scep_url=None, subject=None,
    use_as_digital_signature=None, use_for_key_encipherment=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestScepProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-scep-{run_id}",
            scep_url="https://scep.example.com/",
            ca_identity_name="Default",
            digest="sha256",
            subject="CN=$USERNAME",
            algorithm={"rsa": {"rsa_nbits": "2048"}},
            scep_challenge={"fixed": "mypassword123"},
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestScepProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True due to secret in scep_challenge
        result = run_module(_params(
            state="present", name=f"a-integ-scep-{run_id}",
            scep_url="https://scep.example.com/",
            ca_identity_name="Default",
            digest="sha256",
            subject="CN=$USERNAME",
            algorithm={"rsa": {"rsa_nbits": "2048"}},
            scep_challenge={"fixed": "mypassword123"},
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-scep-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-scep-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-scep-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
