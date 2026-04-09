# CCNP Automation Core Snippet Repository

This repository is a **comprehensive, exam-aligned snippet bank** for the automation domains of Cisco CCNP Enterprise core studies (plus adjacent practical IaC workflows used by enterprise teams).

It is intentionally organized for rapid lab usage:

- **Python automation snippets** across major Cisco-centric platforms
- **IaC snippets** using Ansible and Terraform-style workflows
- **Test and validation snippets** for pre/post checks
- **Reusable helpers** for JSON/YAML, API auth, retries, and structured output

## Platform Coverage

The snippet set includes practical examples for:

- Cisco IOS XE (CLI + NETCONF + RESTCONF)
- Cisco NX-OS (CLI + NX-API style request patterns)
- Cisco IOS XR (NETCONF + model-driven examples)
- Cisco Catalyst Center / DNA Center APIs
- Cisco Meraki Dashboard API
- Cisco SD-WAN (vManage API workflow)
- Cross-platform common tooling patterns

Additionally included:

- Ansible playbooks/roles for multi-platform config and backups
- Terraform-style provider/module stubs for repeatable network provisioning
- Policy and validation snippets you can wire into CI pipelines

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Run any snippet directly once you export credentials through environment variables.

## Suggested Study Workflow

1. Read `docs/ccnp-automation-core-study-map.md`.
2. Start in `snippets/python/common/` and `snippets/python/testing/`.
3. Practice one platform at a time (`ios_xe`, `nx_os`, `ios_xr`, etc.).
4. Recreate each Python workflow with IaC playbooks in `snippets/iac/ansible/`.
5. Use Terraform module stubs to understand state-driven provisioning patterns.

## Safety Notes

- All snippets are templates; validate in a lab before touching production.
- Never hardcode secrets in files. Use env vars or a secret manager.
- Add RBAC and logging for every API token used.
