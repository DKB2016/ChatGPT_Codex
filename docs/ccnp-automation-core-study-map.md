# CCNP Automation Core Study Map (Python + IaC)

Use this map to focus on exam-relevant automation skills in a structured sequence.

## 1) Data and Serialization

- Parse/emit JSON, YAML, XML
- Transform API payloads into strongly typed Python objects
- Validate schema with Pydantic-style models or jsonschema

Start with:

- `snippets/python/common/json_yaml_xml_patterns.py`

## 2) API Consumption and Authentication

- Token lifecycle management
- REST patterns (GET/POST/PUT/PATCH/DELETE)
- Error handling, retries, timeouts, pagination

Start with:

- `snippets/python/common/http_client_with_retry.py`

## 3) Platform Workflows

- IOS XE: RESTCONF + NETCONF + CLI fallback
- NX-OS: NX-API payloads and CLI parsing
- IOS XR: model-driven NETCONF operations
- DNA Center: intent APIs, inventory, compliance-style checks
- Meraki: org/network device and config retrieval
- SD-WAN: auth/token/session and policy/device actions

## 4) IaC and Idempotent Operations

- Ansible inventory and role-driven playbooks
- Candidate intent as data (`group_vars`, host vars)
- Terraform modules for declarative resources and repeatability

## 5) Validation and Testing

- Pre-check/post-check scripts
- Assertions on state and routing/policy intent
- Unit tests for parsing functions

Start with:

- `snippets/python/testing/pre_post_validation.py`
- `snippets/python/testing/test_parsers.py`

## 6) Recommended Lab Objectives

1. Pull live interface state from two platform types.
2. Apply a small idempotent config change with Ansible.
3. Validate post-change state in Python.
4. Roll back if assertion fails.
5. Capture artifacts in JSON for audit.
