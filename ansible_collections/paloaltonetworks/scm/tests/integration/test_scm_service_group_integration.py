"""Integration tests for scm_service_group — full CRUD lifecycle.

Depends on a service existing (created in test_01_setup).
"""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_service_group, scm_service

logger = logging.getLogger(__name__)
run_svc_group = make_runner(scm_service_group, "scm_service_group")
run_svc = make_runner(scm_service, "scm_service")

_SG_FIELDS = dict(members=None, name=None, tag=None)
_SVC_FIELDS = dict(description=None, name=None, protocol=None, tag=None)


def _sg_params(**overrides):
    return build_params({**_SG_FIELDS, **overrides})


def _svc_params(**overrides):
    return build_params({**_SVC_FIELDS, **overrides})


class TestServiceGroupsLifecycle:
    _created_id = None
    _svc_name = None

    def test_00_setup_service(self, run_id):
        """Create a prerequisite service for the group."""
        name = f"ansible-integ-svc-for-grp-{run_id}"
        TestServiceGroupsLifecycle._svc_name = name
        result = run_svc(_svc_params(
            state="present", name=name,
            protocol={"tcp": {"port": "7777"}},
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Setup service failed: {result.get('msg')}"

    def test_01_create(self, run_id):
        result = run_svc_group(_sg_params(
            state="present", name=f"ansible-integ-sgrp-{run_id}",
            members=[TestServiceGroupsLifecycle._svc_name],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestServiceGroupsLifecycle._created_id = result["service_group"]["id"]

    def test_02_create_idempotent(self, run_id):
        result = run_svc_group(_sg_params(
            state="present", name=f"ansible-integ-sgrp-{run_id}",
            members=[TestServiceGroupsLifecycle._svc_name],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_03_gather(self, run_id):
        result = run_svc_group(_sg_params(
            state="gathered", name=f"ansible-integ-sgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["service_group"]["id"] == TestServiceGroupsLifecycle._created_id

    def test_04_delete(self, run_id):
        result = run_svc_group(_sg_params(
            state="absent", name=f"ansible-integ-sgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_svc_group(_sg_params(
            state="absent", name=f"ansible-integ-sgrp-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False

    def test_99_teardown_service(self, run_id):
        """Clean up the prerequisite service."""
        run_svc(_svc_params(
            state="absent", name=TestServiceGroupsLifecycle._svc_name,
            folder=TARGET_FOLDER,
        ))
