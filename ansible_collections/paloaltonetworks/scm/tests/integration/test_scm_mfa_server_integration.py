"""Integration tests for scm_mfa_server — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_mfa_server

logger = logging.getLogger(__name__)
run_module = make_runner(scm_mfa_server, "scm_mfa_server")

_FIELDS = dict(mfa_cert_profile=None, mfa_vendor_type=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires MFA vendor and cert configuration")
class TestMfaServersLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-mfa-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-mfa-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-mfa-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
