=============================================
Palo Alto Networks SCM Collection Changelog
=============================================

test0.0.0.1
======

Release Summary
---------------

Initial release of the Palo Alto Networks Strata Cloud Manager (SCM) Ansible Collection.

New Modules
-----------

**Objects**

- ``scm_address`` - Manage IP addresses, FQDNs, and IP ranges
- ``scm_address_info`` - Retrieve address objects
- ``scm_address_group`` - Manage static and dynamic address groups
- ``scm_address_group_info`` - Retrieve address groups
- ``scm_applißation`` - Manage application definitions
- ``scm_application_info`` - Retrieve application definitions
- ``scm_application_filter`` - Manage application filter criteria
- ``scm_application_filter_info`` - Retrieve application filters
- ``scm_application_group`` - Manage application groups
- ``scm_application_group_info`` - Retrieve application groups
- ``scm_external_dynamic_list`` - Manage external dynamic lists (EDLs)
- ``scm_external_dynamic_list_info`` - Retrieve external dynamic lists
- ``scm_hip_object`` - Manage Host Information Profile objects
- ``scm_hip_object_info`` - Retrieve HIP objects
- ``scm_hip_profile`` - Manage HIP profiles
- ``scm_hip_profile_info`` - Retrieve HIP profiles
- ``scm_region`` - Manage region definitions
- ``scm_region_info`` - Retrieve regions
- ``scm_schedule`` - Manage schedule objects
- ``scm_schedule_info`` - Retrieve schedules
- ``scm_service`` - Manage TCP/UDP service definitions
- ``scm_service_info`` - Retrieve service objects
- ``scm_service_group`` - Manage service groups
- ``scm_service_group_info`` - Retrieve service groups
- ``scm_tag`` - Manage tag objects
- ``scm_tag_info`` - Retrieve tags
- ``scm_dynamic_user_group`` - Manage dynamic user groups
- ``scm_dynamic_user_group_info`` - Retrieve dynamic user groups

**Security Policy**

- ``scm_security_rule`` - Manage security policy rules
- ``scm_security_rule_info`` - Retrieve security rules
- ``scm_nat_rule`` - Manage NAT policy rules
- ``scm_nat_rule_info`` - Retrieve NAT rules
- ``scm_decryption_rule`` - Manage decryption policy rules
- ``scm_decryption_rule_info`` - Retrieve decryption rules
- ``scm_authentication_rule`` - Manage authentication policy rules
- ``scm_authentication_rule_info`` - Retrieve authentication rules
- ``scm_application_override_rule`` - Manage application override rules
- ``scm_application_override_rule_info`` - Retrieve application override rules
- ``scm_pbf_rule`` - Manage policy-based forwarding rules
- ``scm_pbf_rule_info`` - Retrieve PBF rules
- ``scm_dos_protection_rule`` - Manage DoS protection rules
- ``scm_dos_protection_rule_info`` - Retrieve DoS protection rules
- ``scm_qos_rule`` - Manage QoS policy rules
- ``scm_qos_rule_info`` - Retrieve QoS rules

**Security Profiles**

- ``scm_anti_spyware_profile`` - Manage anti-spyware profiles
- ``scm_anti_spyware_profile_info`` - Retrieve anti-spyware profiles
- ``scm_dns_security_profile`` - Manage DNS security profiles
- ``scm_dns_security_profile_info`` - Retrieve DNS security profiles
- ``scm_decryption_profile`` - Manage decryption profiles
- ``scm_decryption_profile_info`` - Retrieve decryption profiles
- ``scm_file_blocking_profile`` - Manage file blocking profiles
- ``scm_file_blocking_profile_info`` - Retrieve file blocking profiles
- ``scm_url_access_profile`` - Manage URL filtering profiles
- ``scm_url_access_profile_info`` - Retrieve URL access profiles
- ``scm_vulnerability_protection_profile`` - Manage vulnerability protection profiles
- ``scm_vulnerability_protection_profile_info`` - Retrieve vulnerability protection profiles
- ``scm_wildfire_anti_virus_profile`` - Manage WildFire antivirus profiles
- ``scm_wildfire_anti_virus_profile_info`` - Retrieve WildFire profiles
- ``scm_dos_protection_profile`` - Manage DoS protection profiles
- ``scm_dos_protection_profile_info`` - Retrieve DoS protection profiles
- ``scm_profile_group`` - Manage security profile groups
- ``scm_profile_group_info`` - Retrieve profile groups

**Network Configuration**

- ``scm_ethernet_interface`` - Manage ethernet interfaces
- ``scm_ethernet_interface_info`` - Retrieve ethernet interfaces
- ``scm_loopback_interface`` - Manage loopback interfaces
- ``scm_loopback_interface_info`` - Retrieve loopback interfaces
- ``scm_tunnel_interface`` - Manage tunnel interfaces
- ``scm_tunnel_interface_info`` - Retrieve tunnel interfaces
- ``scm_vlan_interface`` - Manage VLAN interfaces
- ``scm_vlan_interface_info`` - Retrieve VLAN interfaces
- ``scm_aggregate_interface`` - Manage aggregate interfaces
- ``scm_aggregate_interface_info`` - Retrieve aggregate interfaces
- ``scm_layer2_subinterface`` - Manage Layer 2 subinterfaces
- ``scm_layer2_subinterface_info`` - Retrieve Layer 2 subinterfaces
- ``scm_layer3_subinterface`` - Manage Layer 3 subinterfaces
- ``scm_layer3_subinterface_info`` - Retrieve Layer 3 subinterfaces
- ``scm_dhcp_interface`` - Manage DHCP interfaces
- ``scm_dhcp_interface_info`` - Retrieve DHCP interfaces
- ``scm_security_zone`` - Manage security zones
- ``scm_security_zone_info`` - Retrieve security zones
- ``scm_ike_gateway`` - Manage IKE gateways
- ``scm_ike_gateway_info`` - Retrieve IKE gateways
- ``scm_ike_crypto_profile`` - Manage IKE crypto profiles
- ``scm_ike_crypto_profile_info`` - Retrieve IKE crypto profiles
- ``scm_ipsec_tunnel`` - Manage IPsec tunnels
- ``scm_ipsec_tunnel_info`` - Retrieve IPsec tunnels
- ``scm_ipsec_crypto_profile`` - Manage IPsec crypto profiles
- ``scm_ipsec_crypto_profile_info`` - Retrieve IPsec crypto profiles
- ``scm_remote_network`` - Manage remote networks
- ``scm_remote_network_info`` - Retrieve remote networks
- ``scm_service_connection`` - Manage service connections
- ``scm_service_connection_info`` - Retrieve service connections
- ``scm_dns_proxy`` - Manage DNS proxies
- ``scm_dns_proxy_info`` - Retrieve DNS proxies
- ``scm_logical_router`` - Manage logical routers
- ``scm_logical_router_info`` - Retrieve logical routers

**SD-WAN**

- ``scm_sdwan_rule`` - Manage SD-WAN rules
- ``scm_sdwan_rule_info`` - Retrieve SD-WAN rules
- ``scm_sdwan_path_quality_profile`` - Manage path quality profiles
- ``scm_sdwan_path_quality_profile_info`` - Retrieve path quality profiles
- ``scm_sdwan_error_correction_profile`` - Manage error correction profiles
- ``scm_sdwan_error_correction_profile_info`` - Retrieve error correction profiles
- ``scm_sdwan_traffic_distribution_profile`` - Manage traffic distribution profiles
- ``scm_sdwan_traffic_distribution_profile_info`` - Retrieve traffic distribution profiles
- ``scm_traffic_steering_rule`` - Manage traffic steering rules
- ``scm_traffic_steering_rule_info`` - Retrieve traffic steering rules
- ``scm_bandwidth_allocation`` - Manage bandwidth allocations
- ``scm_bandwidth_allocation_info`` - Retrieve bandwidth allocations

**Authentication & Identity**

- ``scm_authentication_profile`` - Manage authentication profiles
- ``scm_authentication_profile_info`` - Retrieve authentication profiles
- ``scm_authentication_portal`` - Manage authentication portals
- ``scm_authentication_portal_info`` - Retrieve authentication portals
- ``scm_authentication_sequence`` - Manage authentication sequences
- ``scm_authentication_sequence_info`` - Retrieve authentication sequences
- ``scm_certificate_profile`` - Manage certificate profiles
- ``scm_certificate_profile_info`` - Retrieve certificate profiles
- ``scm_certificate`` - Manage certificates
- ``scm_certificate_info`` - Retrieve certificates
- ``scm_kerberos_server_profile`` - Manage Kerberos server profiles
- ``scm_kerberos_server_profile_info`` - Retrieve Kerberos server profiles
- ``scm_ldap_server_profile`` - Manage LDAP server profiles
- ``scm_ldap_server_profile_info`` - Retrieve LDAP server profiles
- ``scm_radius_server_profile`` - Manage RADIUS server profiles
- ``scm_radius_server_profile_info`` - Retrieve RADIUS server profiles
- ``scm_saml_server_profile`` - Manage SAML server profiles
- ``scm_saml_server_profile_info`` - Retrieve SAML server profiles
- ``scm_tacacs_server_profile`` - Manage TACACS+ server profiles
- ``scm_tacacs_server_profile_info`` - Retrieve TACACS+ server profiles
- ``scm_local_user`` - Manage local user accounts
- ``scm_local_user_info`` - Retrieve local users
- ``scm_local_user_group`` - Manage local user groups
- ``scm_local_user_group_info`` - Retrieve local user groups
- ``scm_mfa_server`` - Manage multi-factor auth servers
- ``scm_mfa_server_info`` - Retrieve MFA servers
- ``scm_scep_profile`` - Manage SCEP profiles
- ``scm_scep_profile_info`` - Retrieve SCEP profiles
- ``scm_tls_service_profile`` - Manage TLS service profiles
- ``scm_tls_service_profile_info`` - Retrieve TLS service profiles

**Logging & Monitoring**

- ``scm_log_forwarding_profile`` - Manage log forwarding profiles
- ``scm_log_forwarding_profile_info`` - Retrieve log forwarding profiles
- ``scm_http_server_profile`` - Manage HTTP server profiles
- ``scm_http_server_profile_info`` - Retrieve HTTP server profiles
- ``scm_http_header_profile`` - Manage HTTP header profiles
- ``scm_http_header_profile_info`` - Retrieve HTTP header profiles
- ``scm_syslog_server_profile`` - Manage syslog server profiles
- ``scm_syslog_server_profile_info`` - Retrieve syslog server profiles

**System Settings**

- ``scm_folder`` - Manage folders
- ``scm_folder_info`` - Retrieve folders
- ``scm_snippet`` - Manage snippets
- ``scm_snippet_info`` - Retrieve snippets
- ``scm_label`` - Manage labels
- ``scm_label_info`` - Retrieve labels
- ``scm_variable`` - Manage variables
- ``scm_variable_info`` - Retrieve variables
- ``scm_general_setting`` - Manage general system settings
- ``scm_general_setting_info`` - Retrieve general settings
- ``scm_url_category`` - Manage custom URL categories
- ``scm_url_category_info`` - Retrieve URL categories
- ``scm_auto_tag_action`` - Manage auto-tagging actions
- ``scm_auto_tag_action_info`` - Retrieve auto-tag actions
