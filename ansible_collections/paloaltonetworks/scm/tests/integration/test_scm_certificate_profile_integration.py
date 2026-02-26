"""Integration tests for scm_certificate_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_certificate_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_certificate_profile, "scm_certificate_profile")

_FIELDS = dict(
    block_expired_cert=None, block_timeout_cert=None,
    block_unauthenticated_cert=None, block_unknown_cert=None,
    ca_certificates=None, cert_status_timeout=None,
    crl_receive_timeout=None, domain=None, name=None,
    ocsp_receive_timeout=None, use_crl=None, use_ocsp=None,
    username_field=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestCertificateProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-certprof-{run_id}",
            ca_certificates=[{
                "name": "Forward-Trust-CA",
                "default_ocsp_url": "http://test.com",
                "ocsp_verify_cert": "Forward-Trust-CA",
                "template_name": "Forward-Trust-CA",
            }],
            folder="Shared",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestCertificateProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"a-integ-certprof-{run_id}",
            ca_certificates=[{
                "name": "Forward-Trust-CA",
                "default_ocsp_url": "http://test.com",
                "ocsp_verify_cert": "Forward-Trust-CA",
                "template_name": "Forward-Trust-CA",
            }],
            folder="Shared",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"a-integ-certprof-{run_id}",
            folder="Shared",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-certprof-{run_id}",
            folder="Shared",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"a-integ-certprof-{run_id}",
            folder="Shared",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
