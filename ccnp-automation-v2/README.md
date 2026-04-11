# CCNP Automation Exam v2 Repository Blueprint

This folder is a **ready-to-clone repo skeleton** for a CCNP Automation exam v2 study/lab project.

It is organized by exam section and gives you **Python + Ansible + Terraform** artifacts in each section so you can practice every automation workflow in multiple tools.

## Repository Layout

- `docs/exam-task-matrix.md` — maps exam sections to repeatable lab tasks.
- `sections/01_network_fundamentals/` — model-driven basics, parsing, idempotency checks.
- `sections/02_apis_protocols/` — REST, NETCONF, RESTCONF, auth/token handling.
- `sections/03_development_design/` — package design, tests, linting, reusable libraries.
- `sections/04_configuration_management/` — Ansible-first config management and compliance.
- `sections/05_infrastructure_automation/` — Terraform-driven provisioning and lifecycle.

## How to Use

1. Copy `ccnp-automation-v2` into its own Git repository.
2. Fill in device credentials via environment variables or a vault.
3. Implement each task in the matrix with all three approaches where applicable:
   - Python SDK/API
   - Ansible playbook/role
   - Terraform resource/module
4. Add CI checks (`ruff`, `pytest`, `ansible-lint`, `terraform validate`).

## Recommended Next Steps

- Add a `requirements.txt`, `pyproject.toml`, and `.pre-commit-config.yaml`.
- Add a lab inventory (`ansible/inventory/hosts.yml`) and Terraform state backend.
- Add one branch per exam section and track completion in pull requests.
