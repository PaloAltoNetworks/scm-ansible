# Palo Alto Networks SCM Ansible Collection

Ansible collection for managing Palo Alto Networks **Strata Cloud Manager** (SCM) resources.

This collection provides 240+ modules (122 CRUD + 120 read-only `_info` modules)
that map 1:1 to the SCM API, enabling infrastructure-as-code management of
security policies, network objects, and cloud-managed firewall configurations..

## Quick Start

Get up and running in 3 steps:

### 1. Install dependencies

```bash
pip install scm-python ansible-core
```

### 2. Configure authentication

Create a config file with your SCM service account credentials:

```bash
mkdir -p config
cat > config/scm-config.json << 'EOF'
{
  "client_id": "myaccount@1234567890.iam.panserviceaccount.com",
  "client_secret": "your-client-secret-here",
  "scope": "tsg_id:1234567890"
}
EOF
```

Then export the path so Ansible modules can find it (Ansible runs modules in
a temporary directory, so the config file must be referenced by absolute path):

```bash
export SCM_CONFIG_FILE="$(pwd)/config/scm-config.json"
```

### 3. Run a playbook

Save this as `address_example.yml`:

```yaml
---
- name: Manage addresses in Strata Cloud Manager
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create address
      paloaltonetworks.scm.scm_address:
        state: present
        name: "ansible-test-address"
        folder: "All"
        ip_netmask: "10.100.0.0/24"
        description: "Created by Ansible"
      register: create_result

    - name: Show created address
      ansible.builtin.debug:
        var: create_result.address

    - name: Update address
      paloaltonetworks.scm.scm_address:
        state: present
        name: "ansible-test-address"
        folder: "All"
        ip_netmask: "10.100.0.0/24"
        description: "Updated by Ansible"
      register: update_result

    - name: Show updated address
      ansible.builtin.debug:
        var: update_result.address

    - name: Get address by name
      paloaltonetworks.scm.scm_address:
        state: gathered
        name: "ansible-test-address"
        folder: "All"
      register: gathered_result

    - name: Show gathered address
      ansible.builtin.debug:
        var: gathered_result.address

    - name: List all addresses
      paloaltonetworks.scm.scm_address_info:
        folder: "All"
      register: list_result

    - name: Show addresses count
      ansible.builtin.debug:
        msg: "Found {{ '{{' }} list_result.total {{ '}}' }} addresses"

    - name: Delete address
      paloaltonetworks.scm.scm_address:
        state: absent
        name: "ansible-test-address"
        folder: "All"
      register: delete_result

    - name: Show delete result
      ansible.builtin.debug:
        var: delete_result
```

Run it:

```bash
ANSIBLE_COLLECTIONS_PATH=. ansible-playbook address_example.yml
```

Expected output:

```
TASK [Create address]      changed  {"address": {"id": "d6f9...", "name": "ansible-test-address", "ip_netmask": "10.100.0.0/24", ...}}
TASK [Update address]      changed  {"address": {"description": "Updated by Ansible", ...}}
TASK [Get address by name] ok       {"address": {"name": "ansible-test-address", ...}}
TASK [List all addresses]  ok       "Found 42 addresses"
TASK [Delete address]      changed  {"msg": "address deleted successfully"}
```

## Requirements

- Python 3.8+
- The `scm-python` Python package (the SCM Python SDK)

```bash
pip install scm-python
```

Ansible is **not required** for the modules to function (they can run standalone),
but is needed if you want to use them in playbooks.

```bash
pip install ansible-core
```

## Installation

Install the collection from the repository:

```bash
ansible-galaxy collection install paloaltonetworks.scm
```

Or include it in a `requirements.yml`:

```yaml
collections:
  - name: paloaltonetworks.scm
```

Or for development, clone the repository and set `ANSIBLE_COLLECTIONS_PATH` to point
to the directory containing `ansible_collections/`:

```bash
git clone https://github.com/paloaltonetworks/scm-ansible.git
cd scm-ansible
ANSIBLE_COLLECTIONS_PATH=. ansible-playbook your_playbook.yml
```

## Authentication

The modules authenticate to SCM using OAuth2 client credentials. You need:

| Parameter         | Description                                    |
|-------------------|------------------------------------------------|
| `client_id`       | Service account client ID                      |
| `client_secret`   | Service account client secret                  |
| `tsg_id`          | Tenant Service Group ID                        |

Obtain these from the Strata Cloud Manager portal under **Settings > Identity & Access > Service Accounts**.

Credentials are resolved in priority order: **module parameter > environment variable > config file**.

### Option 1: Config File with SCM_CONFIG_FILE (recommended)

Create a JSON config file and export its absolute path. This is recommended because
Ansible modules execute in a temporary directory, so a relative path like
`config/scm-config.json` won't be found at runtime.

```bash
export SCM_CONFIG_FILE="/path/to/config/scm-config.json"
```

The file format (same as scm-go and scm-python):

```json
{
  "client_id": "myaccount@1234567890.iam.panserviceaccount.com",
  "client_secret": "your-client-secret-here",
  "scope": "tsg_id:1234567890"
}
```

The `scope` field uses the format `tsg_id:<your-tsg-id>`. You can also use a plain
`tsg_id` field instead of `scope`.

### Option 2: Environment Variables

Set these environment variables before running your playbook:

```bash
export SCM_CLIENT_ID="myaccount@1234567890.iam.panserviceaccount.com"
export SCM_CLIENT_SECRET="your-client-secret-here"
export SCM_TSG_ID="1234567890"
```

When environment variables are set, you can omit credentials from tasks:

```yaml
- name: Create an address object
  paloaltonetworks.scm.scm_address:
    state: present
    name: "web-server-1"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
```

### Option 3: Inline Credentials

Pass credentials directly in each task (useful for Ansible Vault integration):

```yaml
- name: Create an address object
  paloaltonetworks.scm.scm_address:
    client_id: "{{ vault_scm_client_id }}"
    client_secret: "{{ vault_scm_client_secret }}"
    tsg_id: "{{ vault_scm_tsg_id }}"
    state: present
    name: "web-server-1"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
```

To use Ansible Vault, encrypt your credentials:

```bash
ansible-vault encrypt_string 'your-client-secret-here' --name 'vault_scm_client_secret'
```

Then reference vault variables in `group_vars/all.yml` or your playbook.

## Usage

Every module supports three states:

| State       | Description                                            |
|-------------|--------------------------------------------------------|
| `present`   | Create the resource if it doesn't exist, update if it does |
| `absent`    | Delete the resource if it exists                       |
| `gathered`  | Retrieve the resource without making changes           |

### Container Parameters

Most resources must be scoped to a container. Exactly one of these should be specified:

| Parameter  | Description                           |
|------------|---------------------------------------|
| `folder`   | The folder name (e.g., `"Shared"`, `"Prisma Access"`) |
| `snippet`  | The snippet name                      |
| `device`   | The device name                       |

### Complete Workflow Example

This example shows every operation on a single address object — create, idempotent
re-run, update, gather by name, get by ID, list, and delete — with the expected
output from each step.

#### Step 1: Create an address

```yaml
- name: Create a web server address
  paloaltonetworks.scm.scm_address:
    state: present
    name: "web-server-1"
    description: "Production web server"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
    tag:
      - "production"
      - "web"
  register: create_result
```

Output:
```json
{
  "changed": true,
  "address": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "web-server-1",
    "description": "Production web server",
    "ip_netmask": "10.0.1.100/32",
    "folder": "Shared",
    "tag": ["production", "web"]
  },
  "msg": "address created successfully"
}
```

#### Step 2: Run the same task again (idempotency)

Running the exact same task produces no changes. The module fetches the existing
object, compares all fields, and finds nothing differs:

```yaml
- name: Create a web server address (re-run)
  paloaltonetworks.scm.scm_address:
    state: present
    name: "web-server-1"
    description: "Production web server"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
    tag:
      - "production"
      - "web"
  register: idempotent_result
```

Output (`changed: false` — no API call was made):
```json
{
  "changed": false,
  "address": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "web-server-1",
    "description": "Production web server",
    "ip_netmask": "10.0.1.100/32",
    "folder": "Shared",
    "tag": ["production", "web"]
  },
  "msg": "address already up to date"
}
```

Note: Even if the API returns tags as `["web", "production"]` (different order),
the module treats it as equal because list comparison is order-insensitive.

#### Step 3: Update the address

Change the description and add a tag. The module detects the difference and
calls the update API:

```yaml
- name: Update the web server address
  paloaltonetworks.scm.scm_address:
    state: present
    name: "web-server-1"
    description: "Production web server - updated"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
    tag:
      - "production"
      - "web"
      - "updated"
  register: update_result
```

Output:
```json
{
  "changed": true,
  "address": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "web-server-1",
    "description": "Production web server - updated",
    "ip_netmask": "10.0.1.100/32",
    "folder": "Shared",
    "tag": ["production", "web", "updated"]
  },
  "msg": "address updated successfully"
}
```

#### Step 4: Gather by name (using the CRUD module)

Retrieve a single object by name without making any changes. Uses `state: gathered`
on the CRUD module:

```yaml
- name: Gather address details by name
  paloaltonetworks.scm.scm_address:
    state: gathered
    name: "web-server-1"
    folder: "Shared"
  register: gathered_result

- name: Show the object
  ansible.builtin.debug:
    var: gathered_result.address
```

Output:
```json
{
  "changed": false,
  "address": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "web-server-1",
    "description": "Production web server - updated",
    "ip_netmask": "10.0.1.100/32",
    "folder": "Shared",
    "tag": ["production", "web", "updated"]
  },
  "msg": "address found"
}
```

#### Step 5: Get by name (using the _info module)

The `_info` module is read-only and returns results in a list format.
Pass `name` to fetch a single object by name:

```yaml
- name: Get address by name using info module
  paloaltonetworks.scm.scm_address_info:
    name: "web-server-1"
    folder: "Shared"
  register: info_by_name
```

Output (note: returns a list with one item):
```json
{
  "addresses": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "web-server-1",
      "description": "Production web server - updated",
      "ip_netmask": "10.0.1.100/32",
      "folder": "Shared",
      "tag": ["production", "web", "updated"]
    }
  ],
  "total": 1
}
```

#### Step 6: Get by ID (using the _info module)

If you have the UUID (e.g., from a previous create), you can fetch directly by ID:

```yaml
- name: Get address by ID
  paloaltonetworks.scm.scm_address_info:
    id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  register: info_by_id
```

Output:
```json
{
  "addresses": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "web-server-1",
      "description": "Production web server - updated",
      "ip_netmask": "10.0.1.100/32",
      "folder": "Shared",
      "tag": ["production", "web", "updated"]
    }
  ],
  "total": 1
}
```

#### Step 7: List all addresses in a folder

Omit `name` and `id` to list all objects in a container. Supports pagination
with `limit` and `offset`, or set `gather_all: true` to auto-paginate:

```yaml
- name: List all addresses in the Shared folder
  paloaltonetworks.scm.scm_address_info:
    folder: "Shared"
    limit: 50
  register: all_addresses

- name: Show how many addresses were returned
  ansible.builtin.debug:
    msg: "Found {{ '{{' }} all_addresses.total {{ '}}' }} addresses"

- name: List ALL addresses (auto-paginate through every page)
  paloaltonetworks.scm.scm_address_info:
    folder: "Shared"
    gather_all: true
  register: every_address
```

Output (abbreviated):
```json
{
  "addresses": [
    {"id": "aaa-111", "name": "web-server-1", "ip_netmask": "10.0.1.100/32", ...},
    {"id": "bbb-222", "name": "db-server-1", "ip_netmask": "10.0.2.100/32", ...},
    {"id": "ccc-333", "name": "app-server-1", "ip_netmask": "10.0.3.100/32", ...}
  ],
  "total": 3
}
```

#### Step 8: Delete the address

```yaml
- name: Delete the web server address
  paloaltonetworks.scm.scm_address:
    state: absent
    name: "web-server-1"
    folder: "Shared"
  register: delete_result
```

Output:
```json
{
  "changed": true,
  "address": {},
  "msg": "address deleted successfully"
}
```

Running the delete again produces no change (idempotent):
```json
{
  "changed": false,
  "address": {},
  "msg": "address already absent"
}
```

### More Examples

#### Create address groups

```yaml
- name: Create an address group
  paloaltonetworks.scm.scm_address_group:
    state: present
    name: "web-servers"
    description: "All web server addresses"
    static:
      - "web-server-1"
      - "web-server-2"
    folder: "Shared"
```

#### Create security rules

```yaml
- name: Allow web traffic
  paloaltonetworks.scm.scm_security_rule:
    state: present
    name: "allow-web-traffic"
    description: "Allow HTTP/HTTPS to web servers"
    source:
      - "any"
    destination:
      - "web-servers"
    application:
      - "web-browsing"
      - "ssl"
    action: "allow"
    log_end: true
    folder: "Shared"
```

#### List security rules (with position)

Rule resources require a `position` parameter (`pre` or `post`):

```yaml
- name: List all pre-rules
  paloaltonetworks.scm.scm_security_rule_info:
    folder: "Shared"
    position: pre
  register: pre_rules

- name: List all post-rules
  paloaltonetworks.scm.scm_security_rule_info:
    folder: "Shared"
    position: post
  register: post_rules
```

#### Create tags and services

```yaml
- name: Create a tag
  paloaltonetworks.scm.scm_tag:
    state: present
    name: "production"
    color: "Red"
    comments: "Production resources"
    folder: "Shared"

- name: Create a custom service
  paloaltonetworks.scm.scm_service:
    state: present
    name: "custom-app-port"
    description: "Custom application port"
    protocol:
      tcp:
        port: "8443"
    folder: "Shared"
```

### Idempotency

All modules are idempotent. Running the same task twice produces no changes on the
second run. The module compares the desired state against the current API state and
only makes a change when fields actually differ.

List fields (tags, static members, source addresses, etc.) are compared
order-independently, so `["a", "b"]` and `["b", "a"]` are treated as equal.

### Check Mode

All modules support `--check` mode. When Ansible runs with `--check`, the module
reports what *would* change without making any API calls:

```bash
ansible-playbook site.yml --check
```

## Module Reference

All modules follow the naming convention `scm_<resource_name>`. Run
`ansible-doc paloaltonetworks.scm.<module_name>` for full parameter documentation:

```bash
ansible-doc paloaltonetworks.scm.scm_address
ansible-doc paloaltonetworks.scm.scm_security_rule
ansible-doc paloaltonetworks.scm.scm_tag
```

### Objects

| Module | Description |
|--------|-------------|
| `scm_address` | IP addresses, FQDNs, and IP ranges |
| `scm_address_group` | Static and dynamic address groups |
| `scm_application` | Application definitions |
| `scm_application_filter` | Application filter criteria |
| `scm_application_group` | Application groups |
| `scm_external_dynamic_list` | External dynamic lists (EDLs) |
| `scm_hip_object` | Host Information Profile objects |
| `scm_hip_profile` | HIP profiles |
| `scm_region` | Region definitions |
| `scm_schedule` | Schedule objects |
| `scm_service` | TCP/UDP service definitions |
| `scm_service_group` | Service groups |
| `scm_tag` | Tag objects |
| `scm_dynamic_user_group` | Dynamic user groups |

### Security Policy

| Module | Description |
|--------|-------------|
| `scm_security_rule` | Security policy rules |
| `scm_nat_rule` | NAT policy rules |
| `scm_decryption_rule` | Decryption policy rules |
| `scm_authentication_rule` | Authentication policy rules |
| `scm_application_override_rule` | Application override rules |
| `scm_pbf_rule` | Policy-based forwarding rules |
| `scm_dos_protection_rule` | DoS protection rules |
| `scm_qos_rule` | QoS policy rules |

### Security Profiles

| Module | Description |
|--------|-------------|
| `scm_anti_spyware_profile` | Anti-spyware profiles |
| `scm_dns_security_profile` | DNS security profiles |
| `scm_decryption_profile` | Decryption profiles |
| `scm_file_blocking_profile` | File blocking profiles |
| `scm_url_access_profile` | URL filtering profiles |
| `scm_vulnerability_protection_profile` | Vulnerability protection profiles |
| `scm_wildfire_anti_virus_profile` | WildFire antivirus profiles |
| `scm_dos_protection_profile` | DoS protection profiles |
| `scm_profile_group` | Security profile groups |

### Network Configuration

| Module | Description |
|--------|-------------|
| `scm_ethernet_interface` | Ethernet interfaces |
| `scm_loopback_interface` | Loopback interfaces |
| `scm_tunnel_interface` | Tunnel interfaces |
| `scm_vlan_interface` | VLAN interfaces |
| `scm_aggregate_interface` | Aggregate interfaces |
| `scm_layer2_subinterface` | Layer 2 subinterfaces |
| `scm_layer3_subinterface` | Layer 3 subinterfaces |
| `scm_dhcp_interface` | DHCP interfaces |
| `scm_security_zone` | Security zones |
| `scm_ike_gateway` | IKE gateways |
| `scm_ike_crypto_profile` | IKE crypto profiles |
| `scm_ipsec_tunnel` | IPsec tunnels |
| `scm_ipsec_crypto_profile` | IPsec crypto profiles |
| `scm_remote_network` | Remote networks |
| `scm_service_connection` | Service connections |
| `scm_dns_proxy` | DNS proxies |
| `scm_logical_router` | Logical routers |

### SD-WAN

| Module | Description |
|--------|-------------|
| `scm_sdwan_rule` | SD-WAN rules |
| `scm_sdwan_path_quality_profile` | Path quality profiles |
| `scm_sdwan_error_correction_profile` | Error correction profiles |
| `scm_sdwan_traffic_distribution_profile` | Traffic distribution profiles |
| `scm_traffic_steering_rule` | Traffic steering rules |
| `scm_bandwidth_allocation` | Bandwidth allocations |

### Authentication & Identity

| Module | Description |
|--------|-------------|
| `scm_authentication_profile` | Authentication profiles |
| `scm_authentication_portal` | Authentication portals |
| `scm_authentication_sequence` | Authentication sequences |
| `scm_certificate_profile` | Certificate profiles |
| `scm_certificate` | Certificate management |
| `scm_kerberos_server_profile` | Kerberos server profiles |
| `scm_ldap_server_profile` | LDAP server profiles |
| `scm_radius_server_profile` | RADIUS server profiles |
| `scm_saml_server_profile` | SAML server profiles |
| `scm_tacacs_server_profile` | TACACS+ server profiles |
| `scm_local_user` | Local user accounts |
| `scm_local_user_group` | Local user groups |
| `scm_mfa_server` | Multi-factor auth servers |
| `scm_scep_profile` | SCEP profiles |
| `scm_tls_service_profile` | TLS service profiles |

### Logging & Monitoring

| Module | Description |
|--------|-------------|
| `scm_log_forwarding_profile` | Log forwarding profiles |
| `scm_http_server_profile` | HTTP server profiles |
| `scm_http_header_profile` | HTTP header profiles |
| `scm_syslog_server_profile` | Syslog server profiles |

### System Settings

| Module | Description |
|--------|-------------|
| `scm_folder` | Folder management |
| `scm_snippet` | Snippet management |
| `scm_label` | Label management |
| `scm_variable` | Variable definitions |
| `scm_general_setting` | General system settings |
| `scm_url_category` | Custom URL categories |
| `scm_auto_tag_action` | Auto-tagging actions |

## Troubleshooting

### "The scm Python SDK is required"

Install the SDK:

```bash
pip install scm-python
```

### Authentication errors

1. Verify your credentials are correct and the service account is active.
2. Ensure the TSG ID matches the tenant you want to manage.
3. Check that environment variables are exported in the shell running Ansible:

```bash
env | grep SCM_
```

### "Error looking up ... by name"

This typically means the API returned a non-404 error during resource lookup.
Common causes:
- Invalid credentials (401/403)
- Service temporarily unavailable (503)
- Network connectivity issues

Check the error message for the HTTP status code and resolve accordingly.

### Resources not found after creation

SCM operations may require a config push before changes take effect on managed
devices. The Ansible modules manage the *candidate configuration* in SCM.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
