# Palo Alto Networks SCM Ansible Collection

Ansible collection for managing Palo Alto Networks **Strata Cloud Manager** (SCM) resources.

This collection provides 120+ modules that map 1:1 to the SCM API, enabling
infrastructure-as-code management of security policies, network objects, and
cloud-managed firewall configurations.

## Requirements

- Python 3.8+
- The `pan-scm-sdk` Python package (the SCM Python SDK)

```bash
pip install pan-scm-sdk
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

## Authentication

The modules authenticate to SCM using OAuth2 client credentials. You need:

| Parameter         | Description                                    |
|-------------------|------------------------------------------------|
| `client_id`       | Service account client ID                      |
| `client_secret`   | Service account client secret                  |
| `tsg_id`          | Tenant Service Group ID                        |

Obtain these from the Strata Cloud Manager portal under **Settings > Identity & Access > Service Accounts**.

### Option 1: Environment Variables (recommended)

Set these environment variables before running your playbook:

```bash
export SCM_CLIENT_ID="myaccount@1234567890.iam.panserviceaccount.com"
export SCM_CLIENT_SECRET="your-client-secret-here"
export SCM_TSG_ID="1234567890"
```

When environment variables are set, you can omit credentials from tasks:

```yaml
- name: Create an address object
  paloaltonetworks.scm.scm_addresses:
    state: present
    name: "web-server-1"
    ip_netmask: "10.0.1.100/32"
    folder: "Shared"
```

### Option 2: Config File

Create a JSON config file at `config/scm-config.json` relative to the collection root,
or set the `SCM_CONFIG_FILE` environment variable to point to it:

```bash
export SCM_CONFIG_FILE="/path/to/scm-config.json"
```

The file format:

```json
{
  "client_id": "myaccount@1234567890.iam.panserviceaccount.com",
  "client_secret": "your-client-secret-here",
  "scope": "tsg_id:1234567890"
}
```

### Option 3: Inline Credentials

Pass credentials directly in each task (useful for Ansible Vault integration):

```yaml
- name: Create an address object
  paloaltonetworks.scm.scm_addresses:
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

### Playbook Examples

#### Create an address object

```yaml
---
- name: Manage SCM address objects
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create a web server address
      paloaltonetworks.scm.scm_addresses:
        state: present
        name: "web-server-1"
        description: "Production web server"
        ip_netmask: "10.0.1.100/32"
        folder: "Shared"
        tag:
          - "production"
          - "web"

    - name: Create a network range
      paloaltonetworks.scm.scm_addresses:
        state: present
        name: "internal-network"
        description: "Internal network range"
        ip_range: "10.0.0.1-10.0.0.254"
        folder: "Shared"
```

#### Manage address groups

```yaml
    - name: Create an address group
      paloaltonetworks.scm.scm_address_groups:
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
      paloaltonetworks.scm.scm_security_rules:
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

#### Create tags

```yaml
    - name: Create tags
      paloaltonetworks.scm.scm_tags:
        state: present
        name: "production"
        color: "Red"
        comments: "Production resources"
        folder: "Shared"
```

#### Create service objects

```yaml
    - name: Create a custom service
      paloaltonetworks.scm.scm_services:
        state: present
        name: "custom-app-port"
        description: "Custom application port"
        protocol:
          tcp:
            port: "8443"
        folder: "Shared"

    - name: Create a service group
      paloaltonetworks.scm.scm_service_groups:
        state: present
        name: "web-services"
        members:
          - "custom-app-port"
          - "service-http"
          - "service-https"
        folder: "Shared"
```

#### Gather existing resources

```yaml
    - name: Get address details
      paloaltonetworks.scm.scm_addresses:
        state: gathered
        name: "web-server-1"
        folder: "Shared"
      register: addr_info

    - name: Show result
      ansible.builtin.debug:
        var: addr_info.data
```

#### Delete a resource

```yaml
    - name: Remove an address
      paloaltonetworks.scm.scm_addresses:
        state: absent
        name: "old-server"
        folder: "Shared"
```

#### Manage security profiles

```yaml
    - name: Create anti-spyware profile
      paloaltonetworks.scm.scm_anti_spyware_profiles:
        state: present
        name: "strict-anti-spyware"
        description: "Strict anti-spyware profile"
        folder: "Shared"

    - name: Create URL access profile
      paloaltonetworks.scm.scm_url_access_profiles:
        state: present
        name: "default-url-filtering"
        description: "Default URL filtering profile"
        folder: "Shared"

    - name: Create a profile group
      paloaltonetworks.scm.scm_profile_groups:
        state: present
        name: "strict-security"
        spyware:
          - "strict-anti-spyware"
        url_filtering:
          - "default-url-filtering"
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
ansible-doc paloaltonetworks.scm.scm_addresses
ansible-doc paloaltonetworks.scm.scm_security_rules
ansible-doc paloaltonetworks.scm.scm_tags
```

### Objects

| Module | Description |
|--------|-------------|
| `scm_addresses` | IP addresses, FQDNs, and IP ranges |
| `scm_address_groups` | Static and dynamic address groups |
| `scm_applications` | Application definitions |
| `scm_application_filters` | Application filter criteria |
| `scm_application_groups` | Application groups |
| `scm_external_dynamic_lists` | External dynamic lists (EDLs) |
| `scm_hip_objects` | Host Information Profile objects |
| `scm_hip_profiles` | HIP profiles |
| `scm_regions` | Region definitions |
| `scm_schedules` | Schedule objects |
| `scm_services` | TCP/UDP service definitions |
| `scm_service_groups` | Service groups |
| `scm_tags` | Tag objects |
| `scm_dynamic_user_groups` | Dynamic user groups |

### Security Policy

| Module | Description |
|--------|-------------|
| `scm_security_rules` | Security policy rules |
| `scm_nat_rules` | NAT policy rules |
| `scm_decryption_rules` | Decryption policy rules |
| `scm_authentication_rules` | Authentication policy rules |
| `scm_application_override_rules` | Application override rules |
| `scm_pbf_rules` | Policy-based forwarding rules |
| `scm_do_s_protection_rules` | DoS protection rules |
| `scm_qo_s_rules` | QoS policy rules |

### Security Profiles

| Module | Description |
|--------|-------------|
| `scm_anti_spyware_profiles` | Anti-spyware profiles |
| `scm_dns_security_profiles` | DNS security profiles |
| `scm_decryption_profiles` | Decryption profiles |
| `scm_file_blocking_profiles` | File blocking profiles |
| `scm_url_access_profiles` | URL filtering profiles |
| `scm_vulnerability_protection_profiles` | Vulnerability protection profiles |
| `scm_wild_fire_anti_virus_profiles` | WildFire antivirus profiles |
| `scm_do_s_protection_profiles` | DoS protection profiles |
| `scm_profile_groups` | Security profile groups |

### Network Configuration

| Module | Description |
|--------|-------------|
| `scm_ethernet_interfaces` | Ethernet interfaces |
| `scm_loopback_interfaces` | Loopback interfaces |
| `scm_tunnel_interfaces` | Tunnel interfaces |
| `scm_vlan_interfaces` | VLAN interfaces |
| `scm_aggregate_interfaces` | Aggregate interfaces |
| `scm_layer2_subinterfaces` | Layer 2 subinterfaces |
| `scm_layer3_subinterfaces` | Layer 3 subinterfaces |
| `scm_dhcp_interfaces` | DHCP interfaces |
| `scm_security_zones` | Security zones |
| `scm_ike_gateways` | IKE gateways |
| `scm_ike_crypto_profiles` | IKE crypto profiles |
| `scm_i_psec_tunnels` | IPsec tunnels |
| `scm_i_psec_crypto_profiles` | IPsec crypto profiles |
| `scm_remote_networks` | Remote networks |
| `scm_service_connections` | Service connections |
| `scm_dns_proxies` | DNS proxies |
| `scm_logical_routers` | Logical routers |

### SD-WAN

| Module | Description |
|--------|-------------|
| `scm_sdwan_rules` | SD-WAN rules |
| `scm_sdwan_path_quality_profiles` | Path quality profiles |
| `scm_sdwan_error_correction_profiles` | Error correction profiles |
| `scm_sdwan_traffic_distribution_profiles` | Traffic distribution profiles |
| `scm_traffic_steering_rules` | Traffic steering rules |
| `scm_bandwidth_allocations` | Bandwidth allocations |

### Authentication & Identity

| Module | Description |
|--------|-------------|
| `scm_authentication_profiles` | Authentication profiles |
| `scm_authentication_portals` | Authentication portals |
| `scm_authentication_sequences` | Authentication sequences |
| `scm_certificate_profiles` | Certificate profiles |
| `scm_certificates` | Certificate management |
| `scm_kerberos_server_profiles` | Kerberos server profiles |
| `scm_ldap_server_profiles` | LDAP server profiles |
| `scm_radius_server_profiles` | RADIUS server profiles |
| `scm_saml_server_profiles` | SAML server profiles |
| `scm_tacacs_server_profiles` | TACACS+ server profiles |
| `scm_local_users` | Local user accounts |
| `scm_local_user_groups` | Local user groups |
| `scm_mfa_servers` | Multi-factor auth servers |
| `scm_scep_profiles` | SCEP profiles |
| `scm_tls_service_profiles` | TLS service profiles |

### Logging & Monitoring

| Module | Description |
|--------|-------------|
| `scm_log_forwarding_profiles` | Log forwarding profiles |
| `scm_http_server_profiles` | HTTP server profiles |
| `scm_http_header_profiles` | HTTP header profiles |
| `scm_syslog_server_profiles` | Syslog server profiles |

### System Settings

| Module | Description |
|--------|-------------|
| `scm_folders` | Folder management |
| `scm_snippets` | Snippet management |
| `scm_labels` | Label management |
| `scm_variables` | Variable definitions |
| `scm_general_settings` | General system settings |
| `scm_url_categories` | Custom URL categories |
| `scm_auto_tag_actions` | Auto-tagging actions |

## Troubleshooting

### "The scm Python SDK is required"

Install the SDK:

```bash
pip install pan-scm-sdk
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
