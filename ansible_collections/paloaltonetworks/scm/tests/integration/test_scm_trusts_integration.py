"""Integration tests for scm_trusts — skip (no name field)."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_trusts

logger = logging.getLogger(__name__)
run_module = make_runner(scm_trusts, "scm_trusts")

_FIELDS = dict(donor_tenant_name=None, psk=None, recipient_tenant_name=None, trust_id=None, tsg=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires multi-tenant trust infrastructure, no name field")
class TestTrustsLifecycle:

    def test_01_create(self, run_id):
        result = run_module(_params(state="present", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"

    def test_02_delete(self, run_id):
        result = run_module(_params(state="absent", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(state="absent", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
