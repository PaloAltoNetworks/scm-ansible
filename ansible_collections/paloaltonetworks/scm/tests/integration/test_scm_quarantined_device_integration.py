"""Integration tests for scm_quarantined_device — skip (no name field, uses host_id)."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_quarantined_device

logger = logging.getLogger(__name__)
run_module = make_runner(scm_quarantined_device, "scm_quarantined_device")

_FIELDS = dict(host_id=None, serial_number=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires quarantined device infrastructure, no name field")
class TestQuarantinedDevicesLifecycle:

    def test_01_create(self, run_id):
        result = run_module(_params(state="present"))
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"

    def test_02_list(self, run_id):
        result = run_module(_params(state="gathered"))
        assert not result.get("failed"), f"List failed: {result.get('msg')}"

    def test_03_delete(self, run_id):
        result = run_module(_params(state="absent"))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"

    def test_04_delete_idempotent(self, run_id):
        result = run_module(_params(state="absent"))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
