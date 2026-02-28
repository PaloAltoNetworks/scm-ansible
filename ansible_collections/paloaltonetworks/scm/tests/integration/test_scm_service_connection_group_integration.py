"""Integration tests for scm_service_connection_group — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_service_connection_group

logger = logging.getLogger(__name__)
run_module = make_runner(scm_service_connection_group, "scm_service_connection_group")

_FIELDS = dict(disable_snat=None, name=None, pbf_only=None, target=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires existing service connections")
class TestServiceConnectionGroupsLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-svcconngrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestServiceConnectionGroupsLifecycle._created_id = result.get("data", {}).get("id")

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-svcconngrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-svcconngrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
