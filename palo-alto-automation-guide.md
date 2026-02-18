# Palo Alto Firewall Automation Blueprint (Python + Ansible)

This guide gives you a practical, production-oriented roadmap for automating Palo Alto firewalls in four core areas:

1. **Configuration automation**
2. **Network testing and validation**
3. **Backups and recovery readiness**
4. **Operational controls** (the “what you might be missing” layer)

---

## 1) Core Architecture You Should Adopt

Use a **GitOps-style workflow**:

- **Source of truth:** Git repository (YAML/JSON/Jinja templates + inventories)
- **Execution:** CI pipeline (GitHub Actions/GitLab/Jenkins) + Ansible Runner/AWX
- **Control plane:** PAN-OS API (REST/XML) via modules + Python SDK
- **Validation:** pre-checks, post-checks, policy simulation, synthetic traffic tests
- **Audit:** change ticket ID + commit SHA tied to every push

### Recommended stack

- **Ansible**
  - `paloaltonetworks.panos` collection for idempotent config tasks
  - Dynamic inventory or grouped inventory by device group/environment
- **Python**
  - `pan-os-python` (formerly pandevice) for advanced logic/workflows
  - `requests` for API calls where modules are insufficient
  - `pytest` for automation unit/integration checks
- **Secrets**
  - HashiCorp Vault / cloud secret manager / Ansible Vault
- **State + artifacts**
  - Backup configs and test outputs stored in object storage (S3/Blob/GCS)

---

## 2) Configuration Automation Patterns

### A. Use intent files (not ad-hoc playbooks)

Define firewall intent as data:

- Address objects
- Service objects
- Security rules
- NAT rules
- Zones / interfaces / virtual routers
- Device settings (NTP, DNS, logging)

Keep intent separated by environment:

- `inventory/prod/` and `inventory/nonprod/`
- `vars/device_group/*.yml`

### B. Enforce idempotent and staged deployment

For each change:

1. **Candidate config only** (no immediate commit)
2. **Validate** (API validation / commit check)
3. **Commit with comment** (ticket + user + SHA)
4. **Optional push to HA peer / Panorama managed devices**

### C. Recommended Ansible play flow

- Gather baseline facts
- Pre-change snapshot backup
- Apply object/rule diffs
- Run commit-check
- Commit
- Post-change policy/API validation
- Post-change network tests

---

## 3) Network Testing Automation (Often Underbuilt)

Don’t stop at “module succeeded.” Add **network outcome tests**:

### A. Control-plane validation

- API health, mgmt interface reachability
- HA state sanity (active/passive expected roles)
- Commit status clear of errors

### B. Data-plane / policy validation

- Use test clients (or synthetic probes) to verify allowed/denied traffic paths
- Validate expected NAT translation
- Validate route selection (where relevant)
- Confirm log generation and SIEM ingestion for key rule hits

### C. Regression packs

Build repeatable tests per application flow:

- `allow`: app A -> app B over TCP/443
- `deny`: segment X cannot reach admin subnet
- `inspect`: URL filtering / threat profile action

Output machine-readable reports (JSON/JUnit XML) and fail pipeline on policy regressions.

---

## 4) Backup and Recovery Automation

At minimum, automate all three:

1. **Running/candidate config export**
2. **Device state export** (if applicable)
3. **Panorama snapshots** (if Panorama-managed)

### Frequency and retention

- Nightly full backup
- Pre-change and post-change backups
- Retention example: daily 30d, weekly 12w, monthly 12m

### Backup integrity checks

- Verify non-empty file and checksum
- Parse XML/JSON for validity
- Periodic restore drill in lab to confirm recoverability

Store backups immutably when possible (WORM/object lock).

---

## 5) What You’re Probably Missing (High-Value Additions)

### A. Policy-as-code guardrails

Implement gates before merge/deploy:

- No `any:any:any` for high-risk zones
- Mandatory logging on deny rules
- Rule naming convention + owner + expiry metadata
- Block shadowed/overlapping risky rules

### B. Drift detection

Scheduled job:

- Pull live config
- Compare to Git desired state
- Open ticket/PR if drift appears

### C. Rule lifecycle automation

- Add `owner`, `created`, `expiry`, `ticket` tags/comments
- Auto-report stale/unused rules
- Auto-stage disable + removal workflow (with approvals)

### D. Compliance mapping

Map controls to CIS/NIST/ISO requirements and produce evidence automatically:

- Last backup timestamp
- Last restore test timestamp
- Last successful policy test run
- Last drift report

### E. Observability and SLOs

Track automation SLOs:

- Change success rate
- Mean commit time
- Post-change incident rate
- Backup success rate
- Drift MTTR

---

## 6) Suggested Repository Layout

```text
firewall-automation/
  inventories/
    prod/
    nonprod/
  group_vars/
  roles/
    panos_objects/
    panos_policies/
    panos_nat/
    panos_commit/
    validation/
  playbooks/
    deploy.yml
    validate.yml
    backup.yml
    drift.yml
  intent/
    objects/
    policies/
    nat/
  scripts/
    panos_precheck.py
    panos_postcheck.py
    policy_regression.py
  tests/
    test_intent_schema.py
    test_policy_guards.py
  docs/
    runbooks/
```

---

## 7) Practical Workflow You Can Implement This Month

### Phase 1 (Week 1): Baseline and Safety

- Create inventory + connectivity checks
- Implement nightly backup playbook
- Add pre-change snapshot in deployment playbook
- Standardize commit comments/tags

### Phase 2 (Week 2): Deterministic Config Deployment

- Move objects/rules into intent files
- Implement idempotent Ansible roles for objects + rules + commit
- Add pipeline lint + schema validation

### Phase 3 (Week 3): Automated Validation

- Add post-change control-plane checks
- Add synthetic allow/deny tests for critical apps
- Fail pipeline on failed validation

### Phase 4 (Week 4): Governance

- Add policy-as-code checks
- Implement drift detection job
- Add stale rule report and monthly cleanup workflow

---

## 8) Example Guardrail Checklist (Deploy Gate)

Before commit/push, automation should enforce:

- Change ticket provided
- Backup completed successfully
- Config validates cleanly
- No blocked policy patterns detected
- HA status healthy (if HA pair)
- Post-change tests passed

If any fail: auto-rollback/stop and page operator.

---

## 9) Python + Ansible Division of Responsibility

Use **Ansible** for:

- Declarative configuration and orchestration
- Standardized repeatable tasks
- Environment-based rollout logic

Use **Python** for:

- Advanced validation logic
- Drift analytics and rule usage analysis
- Custom policy simulation/report generation
- Integrations (CMDB, ticketing, SIEM APIs)

This split keeps deployments maintainable while letting you code deeper logic where needed.

---

## 10) Minimal Next Steps (Actionable)

1. Build `backup.yml` with nightly scheduled run + checksum verification.
2. Build `deploy.yml` with pre-backup → apply intent → commit-check → commit.
3. Build `validate.yml` with API/HA checks + 3 critical path traffic tests.
4. Add CI gates for lint/schema/policy guardrails.
5. Add drift job and weekly drift report.

If you want, the next iteration can be a concrete starter pack:

- Ansible role skeleton (`paloaltonetworks.panos`)
- Example intent schema
- Python validation script template
- CI pipeline template (GitHub Actions/GitLab)
