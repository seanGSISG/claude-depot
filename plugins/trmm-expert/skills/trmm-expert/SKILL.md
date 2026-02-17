---
name: trmm-expert
description: "Answer questions about Tactical RMM (TRMM) — an open-source remote monitoring and management platform. Covers architecture, installation, agent deployment (Windows/Linux/macOS), MeshCentral integration, scripting (PowerShell/Python/Bash/Deno), script variables, custom fields, keystore, automated checks, tasks, automation policies, maintenance mode, alerting, email/SMS notifications, webhooks, REST API, global settings, overrides, permissions, Django admin, URL actions, user interface, software management, web terminal, management commands, reporting (Enterprise), SSO (Enterprise), third-party integrations (Bitdefender, Zammad), SNMP checks, BitLocker key retrieval, remote background sessions, and troubleshooting FAQ."
---

## Overview

Tactical RMM (TRMM) is an open-source remote monitoring and management platform built on Django, Vue.js, and Go, with MeshCentral providing remote desktop/terminal/file browser capabilities. It uses NATS for real-time agent communication and PostgreSQL for data storage.

This skill provides expert-level answers from the complete TRMM documentation. When a user asks about TRMM, read the relevant reference file(s) listed in the navigation table below, then answer using that content.

## Domain Concept Map

**Organizational hierarchy:** Client > Site > Agent. Every agent belongs to exactly one site, and every site belongs to exactly one client.

**Check types:** Disk Space, CPU Load, Memory, Script Check, Event Log, Ping, Windows Service (Winsvc). Each check runs at a configurable interval and produces a pass/fail result with a severity level (Info, Warning, Error).

**Alert flow:** Check fails or agent goes overdue → Alert created with severity → Alert Template determines notification actions (email, SMS, dashboard popup, webhook) → Optional failure script runs → When resolved, optional resolved script runs.

**Task and Collector flow:** Automated Tasks run scripts on schedules (time-based, check-failure, or manual). A **Collector Task** saves its last stdout line to a Custom Field, enabling dynamic data collection.

**Custom Fields** are user-defined fields on Agent, Site, or Client objects. They are referenced in scripts as `{{agent.FieldName}}`, `{{site.FieldName}}`, or `{{client.FieldName}}`. The **Global Key Store** provides `{{global.key_name}}` variables available to all scripts.

**Automation Policy inheritance:** Global → Client → Site → Agent. Each level can block inheritance from the level above. Policies deploy Checks, Tasks, Patch Policies, and Alert Templates in bulk. An **Enforced** policy overwrites conflicting agent-level checks.

**Script variable syntax:** `{{model.field}}` — e.g., `{{agent.hostname}}`, `{{agent.site.name}}`, `{{client.name}}`. Nested relations work. Everything between `{{ }}` is case-sensitive.

## Reference Navigation

Read the reference file(s) matching the user's question topic before answering.

| Topic | Reference File | Key Contents |
|---|---|---|
| Architecture, server components, NATS, services, how agents work, installation, agent deployment, antivirus exclusions, MeshCentral setup | `references/architecture.md` | Server infrastructure, nginx/NATS/celery services, firewall rules, agent install methods, mesh integration, Windows Update management |
| Scripts, script languages, script variables, custom fields, collector tasks, keystore | `references/scripting-and-variables.md` | PowerShell/Python/Bash/Deno support, `{{model.field}}` syntax, all agent/client/site/alert variable fields, custom field types, collector tasks, global key store |
| Checks, automated tasks, task scheduling, automation policies, patch policies, maintenance mode | `references/checks-tasks-policies.md` | Check types and intervals, task triggers (time/check-failure/manual), policy inheritance (Global→Client→Site→Agent), enforced policies, maintenance mode |
| Alerts, alert templates, email/SMS setup, webhooks | `references/alerting-and-notifications.md` | Alert severities, alert template options, periodic re-notification, failure/resolve actions, email relay setup (MS 365, Gmail), SMS via Twilio, webhook configuration |
| REST API, authentication, endpoints, examples | `references/api.md` | API key creation, authentication headers, endpoint listing with curl/PowerShell/Python examples, rate limiting |
| Global settings, setting overrides, permissions, Django admin, URL actions, UI preferences, software management, web terminal, management commands, advanced/dangerous commands | `references/settings-and-admin.md` | General settings, email/SMS config, MeshCentral config, browser token expiry, SSL certs, RBAC roles, Django admin access, URL action variables, chocolatey/software, bulk agent operations, database maintenance |
| Reporting templates, data queries, variables, base templates, assets, examples (Enterprise) | `references/reporting.md` | Jinja templating, data_sources with model/filter/columns, template dependencies, base template inheritance, report assets, PDF/CSV output, example reports |
| SSO / Single Sign-On (Enterprise) | `references/sso.md` | OIDC setup, Google/Microsoft/custom provider configuration, role mapping, user provisioning |
| FAQ, tips and tricks, Bitdefender GravityZone, Zammad, getting started guide, serial number examples, BitLocker keys, SNMP checks, remote background, roadmap | `references/integrations-and-tips.md` | Common troubleshooting, AV exclusion patterns, monitoring endpoints, third-party deployment guides, SNMP with pysnmplib, BitLocker key collection, remote terminal/file browser, development roadmap |

## Cross-Reference Guide

Some questions span multiple domains. Load files in the order shown:

| Question Pattern | Files to Load (in order) |
|---|---|
| "How do I set up email/SMS alerts?" | alerting-and-notifications.md → settings-and-admin.md (Global Settings section) |
| "How do I write a script using custom fields?" | scripting-and-variables.md |
| "How do I create a report with agent data?" | reporting.md → scripting-and-variables.md (for variable syntax) |
| "How do I deploy agents?" | architecture.md (Agent Installation section) |
| "How do I automate patching?" | checks-tasks-policies.md (Automation Policies section) → architecture.md (Windows Update Management) |
| "How do I set up webhooks for alerts?" | alerting-and-notifications.md (Webhooks section) |
| "How do I use the API to manage agents?" | api.md |
| "How do I configure SSO?" | sso.md → settings-and-admin.md (Permissions section) |
| "How do I run scripts on check failure?" | checks-tasks-policies.md → scripting-and-variables.md |
| "How do I collect data into custom fields?" | scripting-and-variables.md (Custom Fields + Collector Tasks) → checks-tasks-policies.md (Automated Tasks) |
| "How do I set up SNMP monitoring?" | integrations-and-tips.md (SNMP Checks section) |
| "How do I use maintenance mode?" | checks-tasks-policies.md (Maintenance Mode section) |

## Key Syntax Quick Reference

**Agent variables** (use in script arguments or env vars):
- `{{agent.hostname}}`, `{{agent.public_ip}}`, `{{agent.local_ips}}`
- `{{agent.operating_system}}`, `{{agent.plat}}`, `{{agent.version}}`
- `{{agent.site.name}}`, `{{agent.site.client.name}}`
- `{{agent.logged_in_username}}`, `{{agent.needs_reboot}}`

**Custom fields** (case-sensitive, spaces allowed):
- `{{agent.My Field Name}}`, `{{client.AV_KEY}}`, `{{site.no_patching}}`

**Global keystore:** `{{global.key_name}}`

**Alert template variables** (only in failure/resolve actions):
- `{{alert.message}}`, `{{alert.severity}}`, `{{alert.alert_type}}`
- `{{alert.agent.hostname}}`, `{{alert.site.name}}`, `{{alert.client.name}}`
- `{{alert.get_result.stdout}}`, `{{alert.get_result.stderr}}`

**Reporting data queries** (YAML in variables editor):
```yaml
data_sources:
    agents:
        model: agent
        filter:
            site__client_id: '{{ client.id }}'
        columns:
            - hostname
            - operating_system
            - last_seen
```

**Jinja loops in reports:**
```
{% for item in data_sources.agents %}
{{ item.hostname }} - {{ item.operating_system }}
{% endfor %}
```

## Searching Large References

For `reporting.md` (~1200 lines), use Grep to find specific topics:
- Data query filters: search for `filter:` or `model:`
- Jinja syntax: search for `{% ` or `{{ `
- Specific models: search for the model name (e.g., `model: agent`)

For `settings-and-admin.md` (~700 lines), search by section:
- Email setup: search for `Email` or `SMTP`
- Permissions: search for `Role` or `Permission`
- Management commands: search for the command name or `python manage.py`

For `architecture.md` (~1100 lines):
- Services: search for `systemctl` or the service name (e.g., `nats`, `celery`)
- Agent install: search for `install` or `deployment`

## Important Caveats

- **Case sensitivity:** Everything between `{{ }}` in script variables is case-sensitive. `{{agent.Hostname}}` will NOT work; use `{{agent.hostname}}`.
- **API trailing slashes:** All TRMM API endpoints require a trailing slash (e.g., `/agents/`). Omitting it returns a redirect or error.
- **Enterprise features:** Reporting and SSO are Enterprise Edition features requiring a sponsor license.
- **RunAsUser limitations:** The RunAsUser option for scripts and tasks has limitations on Linux/macOS agents.
- **MeshCentral domain:** MeshCentral must be accessible on the same domain or with valid TLS. Agent communication depends on mesh connectivity.
- **Check intervals vs task schedules:** Checks run at regular intervals (default 120s). Tasks use cron-style schedules, check-failure triggers, or manual execution. Don't confuse the two.
- **Backslash escaping:** In custom fields, `\` is an escape character. Use `\\` for literal backslashes.
- **Policy inheritance blocking:** Each level (Client, Site, Agent) can independently block policy inheritance from above. An "Enforced" policy overrides agent-level settings regardless.
