# Ansible Collection CI/CD Test Strategy

This document explains the two-tier testing strategy for the `paloaltonetworks.scm` Ansible collection.

## Overview

We use a **two-tier testing approach**:

| Workflow | Trigger | Runtime | Purpose |
|----------|---------|---------|---------|
| **Module Tests (Fast)** | Every push/PR | ~30-45 min | Fast feedback during development |
| **Playbook Tests (Full)** | Manual / merge to main | ~100-120 min | Full integration validation |

## Why Two Workflows?

### The Problem: Ansible Playbook Overhead

Each `ansible-playbook` invocation incurs significant overhead:

```
Per playbook execution:
├── New Python process spawn      (~2 sec)
├── Ansible runtime loading       (~3 sec)
├── Module imports                (~2 sec)
├── Playbook YAML parsing         (~1 sec)
├── SCM client initialization     (~2 sec)
├── OAuth authentication          (~5-10 sec)
├── Actual API calls (CRUD)       (~20-35 sec)
└── Process teardown              (~1 sec)
────────────────────────────────────────────
Total per playbook:               ~40-60 sec
```

**With ~100 playbooks running sequentially:**
- API work: ~35 sec × 100 = ~58 min (actual value)
- Overhead: ~25 sec × 100 = ~42 min (waste)
- **Total: ~100 min**

### Evidence from CI Logs

From GitHub Actions run (July 2026):

```
2026-07-22T00:40:30 - Started playbook tests
2026-07-22T00:41:33 - scm_address :: PASS          (~63 sec)
2026-07-22T00:42:33 - scm_address_group :: PASS    (~60 sec)
2026-07-22T00:43:34 - scm_aggregate_interface :: PASS
...
2026-07-22T02:10:34 - TIMEOUT after 90 minutes (only 79 of ~100 completed)
```

Each playbook consistently takes ~60 seconds, regardless of API complexity.

### Why Can't We Parallelize?

The SCM backend uses XML-based configuration. Parallel API calls cause:
- Configuration conflicts
- Race conditions
- Inconsistent state

**Parallel execution is not an option.**

### Industry Standard

Major Ansible collections (AWS, Azure, GCP, Kubernetes) use pytest for CI/CD:

| Collection | CI Testing | Playbook Tests |
|------------|------------|----------------|
| amazon.aws | pytest + molecule | Manual/optional |
| azure.azcollection | pytest | Manual |
| google.cloud | pytest | Manual |
| kubernetes.core | pytest | Manual |

Playbooks are tested manually or in nightly runs, not on every PR.

## Solution: Pytest Module Tests

Pytest runs all tests in a **single process** with a **shared SDK client**:

```python
@pytest.fixture(scope="session")
def scm_client():
    return Scm()  # OAuth happens ONCE

def test_scm_address(scm_client):
    # Uses shared client - no re-auth
    api = scm_client.objects.AddressesApi(...)
    api.create_addresses(...)
    api.delete_addresses(...)

def test_scm_tag(scm_client):
    # Still uses same client
    ...
```

**Runtime comparison:**

| Approach | Calculation | Total |
|----------|-------------|-------|
| Playbooks | 100 × 60 sec | ~100 min |
| Pytest | 15 sec setup + (100 × 35 sec API) | ~35-45 min |

**~60% faster** with pytest.

## What Each Workflow Tests

### Module Tests (Fast) - `test.yml`

Tests the **module Python code** directly:

- Argument parsing and validation
- State handling (present/absent/gathered)
- Idempotency logic
- SDK integration
- Field mapping
- Error handling

**Does NOT test:**
- Playbook YAML syntax
- Ansible variable interpolation
- Full Ansible runtime behavior

### Playbook Tests (Full) - `playbook-tests.yml`

Tests the **complete user experience**:

- Playbook YAML structure
- Ansible variable handling
- Full runtime integration
- Example playbook correctness

## Developer Workflow

```
1. Developer creates PR
   └── Module Tests (Fast) runs automatically
       └── ~30-45 min for feedback

2. Code review passes, ready to merge
   └── Manually trigger "Playbook Tests (Full)"
       └── Go to Actions → Playbook Tests (Full) → Run workflow
       └── ~100-120 min for full validation

3. Playbook tests pass
   └── Merge to develop

4. Merge to main
   └── Playbook Tests (Full) runs automatically
```

## How to Trigger Manual Playbook Tests

### GitHub UI

1. Navigate to **Actions** tab
2. Select **"Playbook Tests (Full)"** workflow
3. Click **"Run workflow"** button
4. Select branch (usually your PR branch)
5. Optionally add a reason
6. Click **"Run workflow"**

### GitHub CLI

```bash
gh workflow run playbook-tests.yml --ref <branch-name>
```

### API

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/PaloAltoNetworks/scm-ansible/actions/workflows/playbook-tests.yml/dispatches \
  -d '{"ref":"develop"}'
```

## Troubleshooting

### Module Tests Failing

1. Check if it's an SDK issue (also failing in scm-python CI?)
2. Check module logic in `plugins/modules/<resource>.py`
3. Run locally:
   ```bash
   cd ansible_collections/paloaltonetworks/scm
   pytest tests/integration/test_<resource>.py -v
   ```

### Playbook Tests Failing

1. Check if Module Tests pass (if not, fix module first)
2. Check example playbook syntax in `examples/<resource>.yml`
3. Run locally:
   ```bash
   export SCM_CONFIG_FILE=/path/to/config.json
   export ANSIBLE_COLLECTIONS_PATH=$(pwd)
   ansible-playbook examples/scm_address.yml
   ```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "object already exists" | Leftover from previous run | Clean up in SCM console |
| Pydantic validation error | SDK model mismatch | Check scm-python version |
| Timeout | Too many playbooks | Increase timeout or reduce list |
| OAuth failure | Expired/invalid credentials | Check GitHub secrets |

## Configuration

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `SCM_AUTH_URL` | OAuth2 authentication URL |
| `SCM_CLIENT_ID` | OAuth2 client ID |
| `SCM_CLIENT_SECRET` | OAuth2 client secret |
| `SCM_HOST` | SCM API host |
| `SCM_PROTOCOL` | `https` |
| `SCM_SCOPE` | OAuth2 scope |
| `SCM_TSG_ID` | Tenant Service Group ID |
| `SCM_SKIP_VERIFY_CERTIFICATE` | `true` or `false` |

### Local Testing

1. Create config file:
   ```json
   {
     "auth_url": "https://auth.example.com",
     "client_id": "your-client-id",
     "client_secret": "your-secret",
     "host": "api.example.com",
     "protocol": "https",
     "scope": "your-scope",
     "logging": "debug"
   }
   ```

2. Set environment:
   ```bash
   export SCM_CONFIG_FILE=/path/to/config.json
   ```

3. Run tests:
   ```bash
   # Pytest (fast)
   cd ansible_collections/paloaltonetworks/scm
   pytest tests/integration/ -v

   # Single playbook
   ANSIBLE_COLLECTIONS_PATH=$(pwd)/.. ansible-playbook examples/scm_address.yml
   ```

## Summary

| Aspect | Module Tests | Playbook Tests |
|--------|--------------|----------------|
| **Trigger** | Automatic (push/PR) | Manual / merge to main |
| **Runtime** | ~30-45 min | ~100-120 min |
| **Tests** | Module Python code | Full Ansible experience |
| **Use case** | Development feedback | Pre-merge validation |
| **Overhead** | Minimal (single process) | High (process per playbook) |

This strategy provides **fast feedback for developers** while ensuring **full validation before merge**.
