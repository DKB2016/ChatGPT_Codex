# Platform Snippet Matrix

| Platform | Python Snippets | IaC Snippets |
|---|---|---|
| IOS XE | `ios_xe/restconf_interfaces.py`, `ios_xe/netconf_hostname.py` | Ansible `push_base_config.yml`, Terraform `providers/iosxe` |
| NX-OS | `nx_os/nxapi_show_version.py` | Ansible role `base_config` |
| IOS XR | `ios_xr/netconf_get_bgp.py` | NETCONF workflow can be adapted with Ansible `netconf_config` modules |
| Catalyst Center | `dnac/device_inventory.py` | Can be integrated in Ansible via `uri` modules and token reuse |
| Meraki | `meraki/get_org_networks.py` | Terraform `providers/meraki` module usage |
| SD-WAN vManage | `sdwan/vmanage_device_list.py` | IaC pipeline pattern via API-driven Python and Ansible orchestration |
| PAN-OS (adjacent enterprise platform) | Existing repo guide + Terraform `providers/panos` | Terraform module `panos_security_rule` |

## Exam-Centered Skill Areas Covered

- APIs and controllers
- Data modeling and parsing
- Python for network automation
- Infrastructure as Code fundamentals
- Validation/testing patterns
