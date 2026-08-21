"""Integration tests for scm_certificate — full CRUD lifecycle."""

import json
import logging

import pytest

from helpers import build_params, make_runner

from ansible_collections.paloaltonetworks.scm.plugins.modules import scm_certificate

logger = logging.getLogger(__name__)
run_module = make_runner(scm_certificate, "scm_certificate")

FOLDER = "Prisma Access"


class TestCertificatesLifecycle:
    """Test Certificate CRUD operations."""

    def test_01_create(self, run_id):
        """Create a self-signed certificate."""
        result = run_module(build_params({
            "state": "present",
            "folder": FOLDER,
            "certificate_name": f"an-cert-{run_id}",
            "common_name": f"an-cert-{run_id}.example.com",
            "algorithm": {"rsa_number_of_bits": 2048},
            "digest": "sha256",
            "signed_by": "Root CA",
        }))
        logger.info(f"CREATE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Create failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_02_delete(self, run_id):
        """Delete the certificate."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-cert-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"DELETE: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Delete failed: {result.get('msg')}"
        assert result["changed"] is True

    def test_03_delete_idempotent(self, run_id):
        """Delete again - should be idempotent."""
        result = run_module(build_params({
            "state": "absent",
            "name": f"an-cert-{run_id}",
            "folder": FOLDER,
        }))
        logger.info(f"IDEMPOTENT: {json.dumps(result, indent=2, default=str)}")
        assert not result.get("failed"), f"Idempotent failed: {result.get('msg')}"
        assert result["changed"] is False
