"""Integration tests for scm_subscribed_tenants — skip (no name field)."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_subscribed_tenants

logger = logging.getLogger(__name__)
run_module = make_runner(scm_subscribed_tenants, "scm_subscribed_tenants")

_FIELDS = dict(snippet_id=None, snippet_name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires snippet sharing infrastructure, no name field")
class TestSubscribedTenantsLifecycle:

    def test_01_create(self, run_id):
        result = run_module(_params(state="present", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"

    def test_02_delete(self, run_id):
        result = run_module(_params(state="absent", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(state="absent", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
