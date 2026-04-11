# CCNP Automation v2 Task Matrix

Use this matrix to ensure each exam section includes Python, Ansible, and Terraform deliverables.

| Section | Python Task | Ansible Task | Terraform Task |
|---|---|---|---|
| 01 Network Fundamentals | Collect structured device facts and render JSON reports | Gather facts and assert baseline values | Define provider configuration and data sources for inventory |
| 02 APIs & Protocols | Build NETCONF/RESTCONF/API client scripts with retries | Use API modules and URI tasks for token + config workflows | Model API-backed resources and reusable variables |
| 03 Development & Design | Build reusable package + unit tests + type hints | Create reusable roles and templated tasks | Create reusable modules with standardized inputs/outputs |
| 04 Configuration Management | Generate intended configs and run diff checks | Enforce idempotent state, backups, and compliance checks | Represent desired state and detect drift with plan/apply |
| 05 Infrastructure Automation | Orchestrate multi-domain workflow in Python CLI pipeline | Chain playbooks for provisioning + validation + rollback | Provision VLANs/interfaces/policies via modules and workspaces |

## Completion Definition

A section is complete when:

- Python script runs successfully in lab and exports machine-readable output.
- Ansible playbook is idempotent (`changed=0` on second run for steady state).
- Terraform shows stable plan after apply (no unexpected drift).
