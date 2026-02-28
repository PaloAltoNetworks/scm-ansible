"""Integration tests for scm_layer2_subinterface — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_layer2_subinterface

logger = logging.getLogger(__name__)
run_module = make_runner(scm_layer2_subinterface, "scm_layer2_subinterface")

_FIELDS = dict(
    comment=None, name=None, tag=None,
)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="requires real device hardware and parent interface")
class TestLayer2SubinterfacesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"an-l2subif-{run_id}",
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-l2subif-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"an-l2subif-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
