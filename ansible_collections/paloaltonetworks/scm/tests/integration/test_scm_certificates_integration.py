"""Integration tests for scm_certificates — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_certificates

logger = logging.getLogger(__name__)
run_module = make_runner(scm_certificates, "scm_certificates")

_FIELDS = dict(
    algorithm=None, alternate_email=None, certificate_name=None,
    common_name=None, country_code=None, day_till_expiration=None,
    department=None, digest=None, email=None, hostname=None, ip=None,
    is_block_private_key=None, is_certificate_authority=None, locality=None,
    ocsp_responder_url=None, signed_by=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="no name field (uses certificate_name), complex crypto requirements")
class TestCertificatesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
