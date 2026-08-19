# Palo Alto Networks SCM Ansible Collection

The `paloaltonetworks.scm` collection provides modules and plugins to manage
and query Palo Alto Networks **Strata Cloud Manager** (SCM).

This collection covers the following aspects of Strata Cloud Manager:

- NGFW & Prisma Access — security policy, network objects, profiles, interfaces
- Authentication & Identity — profiles, certificates, server profiles

SCM API documentation can be found at: https://pan.dev/ 

## Release Notes

### 0.0.1-beta.1

#### FEATURES

* Initial release of the Palo Alto Networks Strata Cloud Manager (SCM) Ansible Collection.

**Objects**

* module/scm_address: Manage IP addresses, FQDNs, and IP ranges
* module/scm_address_info: Retrieve address objects
* module/scm_address_group: Manage static and dynamic address groups
* module/scm_address_group_info: Retrieve address groups
* module/scm_application: Manage application definitions
* module/scm_application_filter: Manage application filter criteria
* module/scm_application_group: Manage application groups
* module/scm_external_dynamic_list: Manage external dynamic lists (EDLs)
* module/scm_hip_object: Manage Host Information Profile objects
* module/scm_hip_profile: Manage HIP profiles
* module/scm_region: Manage region definitions
* module/scm_schedule: Manage schedule objects
* module/scm_service: Manage TCP/UDP service definitions
* module/scm_service_group: Manage service groups
* module/scm_tag: Manage tag objects
* module/scm_dynamic_user_group: Manage dynamic user groups

**Security Policy**

* module/scm_security_rule: Manage security policy rules
* module/scm_nat_rule: Manage NAT policy rules
* module/scm_decryption_rule: Manage decryption policy rules
* module/scm_authentication_rule: Manage authentication policy rules
* module/scm_application_override_rule: Manage application override rules
* module/scm_pbf_rule: Manage policy-based forwarding rules
* module/scm_dos_protection_rule: Manage DoS protection rules
* module/scm_qos_rule: Manage QoS policy rules

**Security Profiles**

* module/scm_anti_spyware_profile: Manage anti-spyware profiles
* module/scm_dns_security_profile: Manage DNS security profiles
* module/scm_decryption_profile: Manage decryption profiles
* module/scm_file_blocking_profile: Manage file blocking profiles
* module/scm_url_access_profile: Manage URL filtering profiles
* module/scm_vulnerability_protection_profile: Manage vulnerability protection profiles
* module/scm_wildfire_anti_virus_profile: Manage WildFire antivirus profiles
* module/scm_dos_protection_profile: Manage DoS protection profiles
* module/scm_profile_group: Manage security profile groups

**Network Configuration**

* module/scm_ethernet_interface: Manage ethernet interfaces
* module/scm_loopback_interface: Manage loopback interfaces
* module/scm_tunnel_interface: Manage tunnel interfaces
* module/scm_vlan_interface: Manage VLAN interfaces
* module/scm_aggregate_interface: Manage aggregate interfaces
* module/scm_layer2_subinterface: Manage Layer 2 subinterfaces
* module/scm_layer3_subinterface: Manage Layer 3 subinterfaces
* module/scm_dhcp_interface: Manage DHCP interfaces
* module/scm_security_zone: Manage security zones
* module/scm_ike_gateway: Manage IKE gateways
* module/scm_ike_crypto_profile: Manage IKE crypto profiles
* module/scm_ipsec_tunnel: Manage IPsec tunnels
* module/scm_ipsec_crypto_profile: Manage IPsec crypto profiles
* module/scm_remote_network: Manage remote networks
* module/scm_service_connection: Manage service connections
* module/scm_dns_proxy: Manage DNS proxies
* module/scm_logical_router: Manage logical routers

**Authentication & Identity**

* module/scm_authentication_profile: Manage authentication profiles
* module/scm_authentication_portal: Manage authentication portals
* module/scm_authentication_sequence: Manage authentication sequences
* module/scm_certificate_profile: Manage certificate profiles
* module/scm_certificate: Manage certificates
* module/scm_kerberos_server_profile: Manage Kerberos server profiles
* module/scm_ldap_server_profile: Manage LDAP server profiles
* module/scm_radius_server_profile: Manage RADIUS server profiles
* module/scm_saml_server_profile: Manage SAML server profiles
* module/scm_tacacs_server_profile: Manage TACACS+ server profiles
* module/scm_local_user: Manage local user accounts
* module/scm_local_user_group: Manage local user groups
* module/scm_mfa_server: Manage multi-factor auth servers
* module/scm_scep_profile: Manage SCEP profiles
* module/scm_tls_service_profile: Manage TLS service profiles

**Logging & Monitoring**

* module/scm_log_forwarding_profile: Manage log forwarding profiles
* module/scm_http_server_profile: Manage HTTP server profiles
* module/scm_http_header_profile: Manage HTTP header profiles
* module/scm_syslog_server_profile: Manage syslog server profiles

**System Settings**

* module/scm_folder: Manage folders
* module/scm_snippet: Manage snippets
* module/scm_label: Manage labels
* module/scm_variable: Manage variables
* module/scm_general_setting: Manage general system settings
* module/scm_url_category: Manage custom URL categories
* module/scm_auto_tag_action: Manage auto-tagging actions

## Example Usage

Install the collection:

```bash
ansible-galaxy collection install paloaltonetworks.scm
```

Configure authentication and run a playbook:

```bash
export SCM_CLIENT_ID="myaccount@1234567890.iam.panserviceaccount.com"
export SCM_CLIENT_SECRET="your-client-secret-here"
export SCM_TSG_ID="1234567890"
```

```yaml
- name: Manage addresses in Strata Cloud Manager
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Create address
      paloaltonetworks.scm.scm_address:
        state: present
        name: "web-server-1"
        ip_netmask: "10.0.1.100/32"
        folder: "Shared"
```

## Authentication Parameter Priority

Credentials are resolved in the following order:

1. Parameters set directly in the task
2. Environment variables (`SCM_CLIENT_ID`, `SCM_CLIENT_SECRET`, `SCM_TSG_ID`)
3. Config file specified by `SCM_CONFIG_FILE`

## Debugging

To see detailed API request and response information, increase Ansible verbosity:

```bash
ansible-playbook site.yml -vvv
```

## Warranty

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

THIS SOFTWARE IS RELEASED AS A PROOF OF CONCEPT FOR EXPERIMENTAL PURPOSES ONLY. USE IT AT OWN RISK. THIS SOFTWARE IS NOT SUPPORTED.

## Support

This collection is released under an as-is, best effort, support policy. These modules should be seen as community supported and Palo Alto Networks will contribute our expertise as and when possible. We do not provide technical support or help in using or troubleshooting the components of the project through our normal support options such as Palo Alto Networks support teams, or ASC (Authorized Support Centers) partners and backline support options. The underlying product used by the modules is still supported, but the support is only for the product functionality and not for help in deploying or using the collection itself. Unless explicitly tagged, all projects or work posted in our GitHub repository (at https://github.com/PaloAltoNetworks) or sites other than our official Downloads page on https://support.paloaltonetworks.com are provided under the best effort policy.
