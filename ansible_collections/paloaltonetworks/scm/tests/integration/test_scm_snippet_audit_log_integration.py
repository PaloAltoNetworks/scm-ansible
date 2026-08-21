"""Integration tests for scm_snippet_audit_log — read-only resource."""

import json
import logging

import pytest

from helpers import TARGET_FOLDER, build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_snippet_audit_log

logger = logging.getLogger(__name__)
run_module = make_runner(scm_snippet_audit_log, "scm_snippet_audit_log")

_FIELDS = dict(action=None, details=None, donor_created=None, donor_tenant_name=None, donor_tsg=None, recipient_tenant_name=None, recipient_tsg=None, snippet_uuid=None, version=None)


def _params(**overrides):
    return build_params({**_FIELDS, **overrides})


@pytest.mark.skip(reason="read-only resource, no CRUD operations")
class TestSnippetAuditLogsLifecycle:

    def test_01_list(self, run_id):
        result = run_module(_params(state="gathered", folder=TARGET_FOLDER))
        assert not result.get("failed"), f"List failed: {result.get('msg')}"
