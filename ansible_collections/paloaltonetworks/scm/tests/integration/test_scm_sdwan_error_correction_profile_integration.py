"""Integration tests for scm_sdwan_error_correction_profile — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_sdwan_error_correction_profile

logger = logging.getLogger(__name__)
run_module = make_runner(scm_sdwan_error_correction_profile, "scm_sdwan_error_correction_profile")

_FIELDS = dict(activation_threshold=None, mode=None, name=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestSdwanErrorCorrectionProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-sdwanerr-{run_id}",
            activation_threshold=2,
            mode={"forward_error_correction": {
                "ratio": "10% (20:2)",
                "recovery_duration": 1000,
            }},
            folder="All",
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestSdwanErrorCorrectionProfilesLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_create_idempotent(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-sdwanerr-{run_id}",
            activation_threshold=2,
            mode={"forward_error_correction": {
                "ratio": "10% (20:2)",
                "recovery_duration": 1000,
            }},
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"an-sdwanerr-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert "found" in result["msg"]

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-sdwanerr-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-sdwanerr-{run_id}",
            folder="All",
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
