"""
Shared helpers for SCM Ansible integration tests.

Provides:
- Ansible stub (FakeAnsibleModule) so tests run without ansible-core
- Credential detection (env vars, config files)
- Generic run_module() factory for invoking any module's main()
"""

import json
import os
import sys
import types
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Ansible stub — provides AnsibleModule without requiring ansible-core
# ---------------------------------------------------------------------------
class _ExitJson(Exception):
    """Raised by exit_json to capture successful module results."""
    def __init__(self, **kwargs):
        self.result = kwargs


class _FailJson(Exception):
    """Raised by fail_json to capture module failures."""
    def __init__(self, **kwargs):
        self.result = kwargs


class FakeAnsibleModule:
    """Minimal AnsibleModule replacement for integration testing."""
    def __init__(self, argument_spec=None, supports_check_mode=False,
                 mutually_exclusive=None, required_if=None):
        self.params = {}
        self.check_mode = False

    def exit_json(self, **kwargs):
        raise _ExitJson(**kwargs)

    def fail_json(self, **kwargs):
        raise _FailJson(**kwargs)

    def log(self, msg):
        """Accept log messages silently (mirrors real AnsibleModule.log)."""
        pass


# Install the ansible stub before any module is imported
if "ansible" not in sys.modules:
    _ansible = types.ModuleType("ansible")
    _ansible_mu = types.ModuleType("ansible.module_utils")
    _ansible_mub = types.ModuleType("ansible.module_utils.basic")
    _ansible_mub.AnsibleModule = FakeAnsibleModule
    _ansible_mu.basic = _ansible_mub
    _ansible.module_utils = _ansible_mu
    sys.modules["ansible"] = _ansible
    sys.modules["ansible.module_utils"] = _ansible_mu
    sys.modules["ansible.module_utils.basic"] = _ansible_mub


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TARGET_FOLDER = "Prisma Access"
REPO_ROOT = Path(__file__).resolve().parents[5]        # scm-ansible/
COLLECTION_ROOT = Path(__file__).resolve().parents[2]  # ansible_collections/.../scm/
RUN_ID = uuid.uuid4().hex[:6]

_MOD_BASE = "ansible_collections.paloaltonetworks.scm.plugins.modules"


# ---------------------------------------------------------------------------
# Credential detection
# ---------------------------------------------------------------------------
def _find_config_file() -> str | None:
    """Find SCM config file and return its absolute path, or None."""
    config_file = os.environ.get("SCM_CONFIG_FILE")
    if config_file and Path(config_file).is_file():
        return str(Path(config_file).resolve())

    for base in [REPO_ROOT, COLLECTION_ROOT]:
        local_config = base / "config" / "scm-config.json"
        if local_config.is_file():
            return str(local_config.resolve())

    return None


def has_credentials() -> bool:
    """Check if SCM credentials are available via any supported method."""
    if os.environ.get("SCM_CLIENT_ID") and os.environ.get("SCM_CLIENT_SECRET"):
        return True

    config_path = _find_config_file()
    if config_path:
        try:
            cfg = json.loads(Path(config_path).read_text())
            if cfg.get("client_id") and cfg.get("client_secret"):
                # Set SCM_CONFIG_FILE so the SDK can also find it
                os.environ["SCM_CONFIG_FILE"] = config_path
                return True
        except (json.JSONDecodeError, OSError):
            pass

    return False


# ---------------------------------------------------------------------------
# Module runner factory
# ---------------------------------------------------------------------------
def make_runner(module_ref, module_name):
    """Create a run_module() function for the given Ansible module."""
    mod_path = f"{_MOD_BASE}.{module_name}"

    def run_module(params: dict) -> dict:
        mod = FakeAnsibleModule()
        mod.params = params
        with patch(f"{mod_path}.AnsibleModule", return_value=mod):
            try:
                module_ref.main()
            except _ExitJson as exc:
                return exc.result
            except _FailJson as exc:
                return {**exc.result, "failed": True}
        pytest.fail("main() did not call exit_json or fail_json")

    return run_module


def build_params(specific_params, has_containers=True):
    """Build a full params dict with meta fields set to None."""
    params = {
        "state": "present",
        "client_id": None,
        "client_secret": None,
        "tsg_id": None,
        "id": None,
    }
    if has_containers:
        params.update({
            "folder": None,
            "snippet": None,
            "device": None,
        })
    params.update(specific_params)
    return params
