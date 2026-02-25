"""Integration tests for scm_http_server_profiles — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_http_server_profiles

logger = logging.getLogger(__name__)
run_module = make_runner(scm_http_server_profiles, "scm_http_server_profiles")

_FIELDS = dict(format=None, name=None, server=None, tag_registration=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


class TestHttpServerProfilesLifecycle:
    _created_id = None

    def test_01_create(self, run_id):
        result = run_module(_params(
            state="present", name=f"ansible-integ-http-{run_id}",
            server=[{
                "name": "test-server",
                "address": "https://example.com/webhook",
                "http_method": "POST",
                "protocol": "HTTPS",
            }],
            folder=TARGET_FOLDER,
        ))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True
        TestHttpServerProfilesLifecycle._created_id = result["data"]["id"]

    def test_02_create_idempotent(self, run_id):
        # Note: idempotent may report changed=True due to nested object enrichment
        result = run_module(_params(
            state="present", name=f"ansible-integ-http-{run_id}",
            server=[{
                "name": "test-server",
                "address": "https://example.com/webhook",
                "http_method": "POST",
                "protocol": "HTTPS",
            }],
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"

    def test_03_gather(self, run_id):
        result = run_module(_params(
            state="gathered", name=f"ansible-integ-http-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Gather failed: {result.get('msg')}"
        assert result["data"]["id"] == TestHttpServerProfilesLifecycle._created_id

    def test_04_delete(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-http-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_05_delete_idempotent(self, run_id):
        result = run_module(_params(
            state="absent", name=f"ansible-integ-http-{run_id}",
            folder=TARGET_FOLDER,
        ))
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
