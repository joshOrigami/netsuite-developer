---
name: netsuite-developer
short_description: Disciplined NetSuite development with metadata awareness and QA verification.
description: Disciplined NetSuite SuiteScript 2.1, SuiteQL, SDF, and integration development with optional metadata provider contract and QA verification steps.
author: Joshua Meiri, Origami Precision, LLC
license: CC-BY-4.0
copyright: 2026 Joshua Meiri, Origami Precision, LLC
---

# NetSuite Developer Skill

## Purpose

This skill enforces disciplined, schema-aware, production-safe NetSuite development.

It applies to:

- SuiteScript 2.1
- SuiteQL
- REST Record API
- Integrations
- SuiteCloud Development Framework (SDF)
- Metadata-driven development via optional provider contract

This skill complements the NetSuite Constitutions.

Constitution defines invariants.  
This skill defines implementation discipline and operational verification.

---

# Core Operating Principles

1. Never assume schema.  
2. Never swallow errors.  
3. Never guess environment.  
4. Never rely on undocumented behavior.  
5. Never deploy without validation.  

If metadata is available, use it.  
If metadata is not available, ask before guessing.

---

# Canonical References

When authoritative clarification is required, prefer the following official Oracle documentation.

SuiteScript Best Practices  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/part_N3360914.html  

General Development Best Practices  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_N3361037.html  

Optimizing SuiteScript Performance  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4460387617.html  

Logging Guidelines  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4430384449.html  

SuiteCloud CLI project:deploy and validate  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_156044636320.html  

REST Record Service Guide  
https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/chapter_1540810168.html  

When in doubt, prefer these references over memory.
Do not invent undocumented behavior.

---

# Metadata Provider Contract

Metadata is optional but preferred.

If a `.netsuite-metadata/` folder exists:

- Enumerate subfolders.
- Treat each subfolder as an environment.
- Do not assume SB, QA, PROD.
- Accept any folder name.
- Require explicit selection if multiple exist.
- Never default silently when multiple exist.
- Persist selection for the session.
- Never mix environments.

Required files per environment:

- `manifest.json`
- `record_index.json`
- `records/<record>.json`

If metadata exists:

- Use it.
- Do not hallucinate fields.
- Do not invent joins.
- Do not assume record types.

If metadata does not exist:

- Ask clarifying questions before generating schema-dependent code.

---

# Metadata Helper Usage

The metadata helper provides deterministic schema lookup and must be used whenever record schema, fields, joins, or SuiteQL table mappings are needed.

## Tool Location

The helper script must live in the workspace at:

- `tools/query_metadata.py`

It is invoked from the project root using the active Python interpreter.

## Output Contract

- Output is structured JSON only.
- No prose.
- Do not infer or hallucinate schema when metadata is available.
- If the helper returns an error JSON, do not proceed with schema-dependent generation until resolved.

## Environment Selection

If multiple environments exist under `.netsuite-metadata/`, the user must choose an environment folder name that exists.

Rules:

- Never assume SB, QA, PROD.
- Never default silently when multiple environment folders exist.
- Echo the chosen environment in all schema-dependent responses.

The helper must be called with either:

- `--env <ENV_FOLDER_NAME>`

Or the project must include:

- `.netsuite-metadata/active_env.json` with `{ "active_env": "<ENV_FOLDER_NAME>" }`

## When the helper must be used

Always use the helper for:

- Field existence checks for SuiteQL or SuiteScript
- Record table mappings
- Join path selection when metadata provides references
- Suggesting non-trivial SuiteQL
- Any code generation that depends on the account’s actual customization state

If metadata does not exist, ask clarifying questions before generating schema-dependent logic.

## Supported Commands

List records:

    python tools/query_metadata.py --env QA list-records

Get a record definition:

    python tools/query_metadata.py --env QA get-record salesorder

List fields for a record:

    python tools/query_metadata.py --env QA list-fields salesorder

Find a field across all records:

    python tools/query_metadata.py --env QA find-field createfrom

Suggest SuiteQL for a record and field list:

    python tools/query_metadata.py --env QA suggest-suiteql salesorder --fields tranid,entity,createdfrom

## How to interpret results

- If `matches` is empty in `find-field`, the field is not present in metadata. Ask the user whether the field name is correct or whether metadata export is stale.
- If a record is not found in `record_index.json`, do not guess. Ask the user to export that record type or confirm naming.
- If a field lacks `suiteql_column`, do not invent one. Ask the user to refresh export or confirm the mapping.

## Non-trivial SuiteQL rule

Before producing a non-trivial SuiteQL query:

- Use the helper to confirm the record and fields exist in the selected environment.
- Use `suggest-suiteql` as a baseline when available.
- Then apply Skill rules such as: explicit WHERE clause, no SELECT *, aliasing, NVL for JSON-sensitive outputs, and a QA test plan.

---

## Schema-Dependent Logic Rule

Metadata must be consulted for ALL schema-dependent operations, including:

- SuiteQL generation
- SuiteScript record.load, record.create, record.submitFields
- record.setValue and getValue field usage
- Sublist access via getSublistValue or setSublistValue
- search.create column definitions
- REST field mappings
- Custom record and custom field usage

If metadata is available, do not:

- Assume a field exists
- Guess a sublist id
- Invent a custom field id
- Infer a join path without metadata confirmation

If metadata is missing, explicitly ask the user before proceeding.

---

# Environment Discipline

Valid environments are any folder under `.netsuite-metadata/`.

Examples:

- SB
- QA
- PROD
- UAT
- CLIENTA-PROD

Rules:

- Always confirm environment when metadata exists.
- Echo environment in responses.
- Never cross-reference metadata from two environments.
- If only one exists, use it.
- Never default silently when multiple exist.

---

## Optional Modules

This Skill supports optional feature modules stored in:

- `docs/modules/`

Feature enablement can be declared per environment using:

- `docs/modules/netsuite-features.json`

### How to Apply Optional Modules

1. Ask for the target environment if not provided.
2. Look up the matching `env_key` entry in `docs/modules/netsuite-features.json`.
3. For each feature module:
   - If the feature key exists and is `true`, apply the module rules.
   - If the feature key exists and is `false`, do not apply the module rules.
   - If the feature key is missing, treat the feature state as unknown and ask only if the current task touches that feature surface area.

Absence of a feature key never implies `false`.

### Module Map (Examples)

Feature modules are convention-based and extensible.

If a feature flag is set to `true` in `docs/modules/netsuite-features.json`,
the corresponding module file in `docs/modules/` should be applied.

Module Naming Convention:

- Feature key: lowercase, snake_case
- Module file: same name as feature key
- Location: docs/modules/<feature>.md

Examples:

- `"multibook": true` → apply `docs/modules/multibook.md`
- `"arm": true` → apply `docs/modules/arm.md`
- `"suitebilling": true` → apply `docs/modules/suitebilling.md`

Developers may add additional feature modules following the same pattern:

- Feature key in `netsuite-features.json`
- Matching module file in `docs/modules/`
- Module defines additional invariants and validation rules

The core Skill does not restrict module creation.

### Environment Mapping

The user must provide an environment name that matches an `env_key` value (for example: `SB1`, `QA`, `PROD`). If the environment is not found in the features file, treat all feature states as unknown and ask only when relevant.

### Output Requirements When a Module Applies

When a module applies, the generated output must include:

- Feature-specific assumptions and invariants
- Feature-specific QA and UAT validation steps
- Any deployment or admin considerations introduced by the feature

### Module Applicability Declaration

When optional feature modules are enabled for the selected environment,
every non-trivial script must include a Module Applicability block.

This declaration clarifies whether the script:

- Is impacted by the enabled module
- Is intentionally not impacted by the enabled module
- Requires validation under the enabled module

This applies even if no functional defect exists.

The purpose is to eliminate ambiguity and prevent assumption drift.

---

#### Required Format (Script Header Comment)

Each script must include a structured comment block:

```javascript
/**
 * Module Applicability
 *
 * Developed In:
 *   - Account: <ACCOUNT_ENV_USED_FOR_DEVELOPMENT>
 *
 * Intended Deployment:
 *   - Account: <TARGET_ACCOUNT_ENV>
 *
 * Multi-Book:
 *   - Applicable: Yes | No
 *   - Rationale:
 *   - Validation Notes:
  *
 * SuiteBilling:
 *   - Applicable: Yes | No
 *   - Rationale:
 *   - Validation Notes:
 *
 * ...
 *
 */
```

---

#### Rules

1. If a module is enabled in `netsuite-features.json`, it must be declared.
2. If not applicable, state why.
3. If applicable, reference:
   - impacted logic
   - validation steps
   - deployment considerations
4. Silence is non-compliant when modules are enabled.

---

#### Severity Classification for Module Review

- High: Functional violation of enabled module invariant.
- Medium: Potential behavioral ambiguity under enabled module.
- Low: Missing explicit module applicability declaration.

---

#### Environment Handling Guidance

Module applicability is feature-based, not environment-ID-based.

Do not duplicate blocks per environment.

Use:

- Developed In → environment used during implementation
- Intended Deployment → target production environment

The declaration provides traceability without hardcoding environment logic into the script.

---

# Code Structure and Documentation Discipline

All generated code must be self-documenting and maintainable.

## Function Docstrings

Every function definition must include a docstring immediately above the function declaration:

- Purpose
- Inputs
- Outputs
- Governance considerations if relevant
- Side effects
- Assumptions

Example (SuiteScript 2.1):

/**
 * Computes total invoice amounts grouped by customer, subsidiary, and currency.
 *
 * @param {Object} context - Map/Reduce context object.
 * @returns {void}
 *
 * Governance:
 * - Uses SuiteQL query.
 * - Expected to process under 5000 governance units per map execution.
 *
 * Assumptions:
 * - Subsidiary filtering applied in query.
 * - Null currency values handled using NVL.
 */

Docstrings are mandatory for:

- Entry points (getInputData, map, reduce, summarize)
- Entry points must include governance expectations and execution context explicitly
- Helper functions
- Utility functions

## Complex Logic Comments

Any non-trivial control structure must include a comment explaining intent.

This includes:

- Nested if statements
- Loops with conditional branching
- try/catch blocks
- Multi-step transformations
- Data reshaping logic
- Aggregation logic

Example:

// Ensure we only process invoices in Approved status to avoid draft totals
if (status === 'CustInvc:A') {
    ...
}

Example:

// Catch and rethrow to preserve stack while ensuring error is logged for review
try {
   ...
} catch (e) {
   log.error({ title: 'Map Phase Failure', details: e });
   throw e;
}

Comments must explain WHY the logic exists, not restate the code.

---

# Plug-in Implementation Rule

If implementing or modifying a NetSuite Plug-in:

- Explicitly declare the plug-in type.
- Document lifecycle impact.
- Document upgrade considerations.
- Document interaction with native NetSuite behavior.
- Include regression validation steps.
- Apply elevated deployment review discipline.

Plug-ins modify platform behavior and require stricter safeguards.

---

# SuiteQL Rules

## Non-Trivial Query Definition

A query is non-trivial if it:

- Joins tables
- Uses date filters
- Filters by subsidiary
- Uses createfrom lineage
- Uses systemnote
- Uses aggregation
- Is intended for reuse
- Impacts reporting or integration

## Required Output For Non-Trivial Queries

Must include:

1. The SuiteQL query.
2. A short QA test plan for the selected environment.

---

# QA Test Plan Structure

Must include:

- Environment name
- Role used
- Row count expectation
- 3 to 5 manual record validations in UI
- Edge case checks
- Performance expectation

Edge case examples:

- Null join fields
- Date boundary
- Multi-subsidiary
- Multi-currency
- Created From lineage
- Inactive or deleted records

---

# Null Handling Rule

SuiteQL does not return null fields in JSON payloads.

When output is consumed by JSON-based integrations:

- Use `NVL` to force deterministic values.

Example:

```sql
NVL(t.memo, 'n/a') AS memo,
NVL(t.createdfrom, 0) AS createdfrom
```

Never assume null keys will exist in JSON output.

---

# BUILTIN.DF Usage Rule

Prefer `BUILTIN.DF()` when:

- Only display value is required.
- Avoiding unnecessary joins.
- Performance is improved.

Avoid `BUILTIN.DF()` when:

- Multiple fields are required from joined table.
- Explicit join clarity is preferred.

# Column Selection Rule
- Never use `SELECT *`.
- Always alias tables.

---

# Error Handling Discipline

Never swallow errors.

Bad:

```javascript
try {
   ...
} catch (e) {
}
```

Acceptable:

```javascript
try {
   ...
} catch (e) {
   log.error({ title: 'Unexpected Error', details: e });
   throw e;
}
```

Rules:

- Always log error.
- Always preserve stack.
- Always ensure there is a review path.
- Scheduled and Map/Reduce must log summary errors.
- Integrations must surface errors upstream.

---

# Logging Rules

- Use `log.audit` for business events.
- Use `log.debug` only for temporary diagnostics.
- Do not log sensitive data.
- In production, logging must not be excessive.
- All unexpected errors must be reviewable.

---

# Script Deployment Discipline

When generating scripts, always include:

1. Script Type
2. Execution Context
3. Deployment notes
4. Required role
5. Error notification guidance

Include in header docstring:

- Expected execution role
- Governance considerations
- Whether it runs as Administrator
- Whether it should notify on error
- Whether it should run in specific contexts

Example docstring guidance:

- Runs as Scheduled Script
- Executes under integration role
- Email on error enabled
- Governance expected under 5000 units

Always consider:

- Deployment status
- Role restrictions
- Audience restrictions
- Context filtering
- Error email configuration
- Governance limits

---

# Integration Discipline

For REST integrations:

- Validate required fields.
- Do not assume defaults.
- Handle 429 and 503 properly.
- Respect rate limits.
- Never expose raw NetSuite errors externally.

CSV imports:

- Validate decimal separators.
- Validate date format.
- Validate encoding.
- Confirm subsidiary context.
- Validate multi-currency assumptions.

---

# SDF Discipline

Always:

- Use SuiteScript 2.1.
- Validate project before deploy.
- Confirm `deploy.xml`.
- Never assume local validation equals server validation.
- Treat `deploy.xml` as source of truth.
- Avoid manual file cabinet changes.

---

# Performance Guardrails

- Avoid N+1 search patterns.
- Limit columns.
- Filter early.
- Paginate large searches.
- Avoid loading entire datasets in memory.
- Use `search.runPaged()` where appropriate.
- Measure runtime for heavy operations.
- Explicitly filter subsidiary when relevant.

---

# Multi-Entity Safety

- Never assume single subsidiary.
- Never assume base currency.
- Never assume feature enablement.
- Always check role context.
- Always scope data intentionally.

---

# Vibe Coding Constraints

AI must not:

- Guess field names.
- Assume record types.
- Skip subsidiary logic.
- Ignore governance limits.
- Invent undocumented APIs.

If uncertain:

- Ask.
- Or consult metadata provider.
- Or consult canonical Oracle documentation.

---

# Deployment Safety Checklist

Before marking code production ready:

- Confirm QA validation performed.
- Confirm no swallowed errors.
- Confirm logs reviewable.
- Confirm deployment audience restricted.
- Confirm no debug logs left in production.
- Confirm governance impact understood.

---

# Documentation and Operational Readiness Discipline

Code generation is not complete until operational documentation exists.

For any non-trivial development (scripts, integrations, SuiteQL reporting logic, SDF deployments), the output must include structured operational documentation.

This documentation is part of the engineering deliverable.

---

## Required Documentation Artifacts

When generating production-ready code, include:

1. UAT Guide
2. Installation / Deployment / Admin Guide
3. End User Guide (if applicable)

If the change is internal-only infrastructure, explicitly state that an End User Guide is not required.

---

## 1. UAT Guide

The UAT Guide must include:

- Target environment
- Role used for testing
- Preconditions
- Step-by-step validation instructions
- Expected results
- Edge cases
- Negative test scenarios
- Multi-subsidiary and multi-currency considerations (if applicable)
- Governance expectations
- Rollback validation steps

The UAT guide must be actionable by a QA analyst without needing the developer present.

---

## 2. Installation / Deployment / Admin Guide

The Installation Guide must include:

- Script type
- Deployment ID
- Execution context
- Required roles and permissions
- Required features enabled
- Dependencies
- SDF project validation steps
- Deployment steps (SB → QA → PROD)
- Error identification guidance
- Error log review path
- Error notification configuration
- Summary log review expectations
- Governance monitoring expectations
- Post-deployment verification checklist
- Rollback procedure
- Confirm deployment status per environment (Testing in SB/QA, Released in PROD).
- Confirm audience restrictions applied correctly.
- Confirm Execute As Role aligns with least privilege principle.
- Confirm event type and execution context filters configured correctly.
- Confirm concurrency and queue settings for scheduled scripts.
- Confirm log level appropriate for production.

Error handling guidance must include:

- Where errors are logged
- How they are surfaced
- Who is notified
- How to trace failures
- What to do if governance limits are exceeded

### Deployment Status Rule

Deployment status must be explicitly documented:

- Testing: Only script owner executes.
- Released: Available to permitted audience.

Never promote directly to Released without documented QA validation.
State intended status per environment (SB, QA, PROD).

### Audience Configuration Rule

Deployment documentation must explicitly state:

- Roles permitted
- Departments restricted (if applicable)
- Employees restricted (if applicable)
- Groups restricted (if applicable)

Do not leave audience overly broad.
If deployment is intentionally global, justify it.

### Execute As Role Rule

Deployment must explicitly document:

- Execute As Role
- Rationale for selected role
- Whether elevated privileges are required

Avoid unnecessary Administrator execution.
Privilege scope must match business requirement.

### Event Context Filtering Rule

For User Events and Client Scripts:

- Explicitly document event types enabled (create, edit, delete, view).
- Explicitly document execution contexts enabled (UI, Web Services, CSV, etc.).
- Avoid enabling unnecessary contexts.

Unfiltered context can cause duplicate execution or unintended behavior.

### Concurrency and Queue Configuration Rule

For Scheduled and Map/Reduce deployments:

- Document concurrency level.
- Document queue selection.
- Document rescheduling behavior.
- Document expected execution frequency.

Concurrency settings must align with governance and integration safety.

### Deployment Logging Configuration Rule

Deployment documentation must state:

- Intended log level for production.
- Whether debug logging is disabled.
- Log retention expectations.

Production deployments must not rely on excessive debug logging.


Never assume the administrator knows where to look.

---

## 3. End User Guide (If Applicable)

Required when:

- UI behavior changes
- New fields appear
- Workflows change
- Saved searches or reports are introduced
- New integrations alter user behavior

Must include:

- What changed
- Who is affected
- Step-by-step usage instructions
- Screens impacted
- Expected behavior
- Known limitations
- Frequently misunderstood behaviors

If no end user impact exists, explicitly state:

"No end-user documentation required. Change is system-level only."

---

## Documentation Output Structure

Documentation must be clearly separated from code and structured with headings:

- ## UAT Guide
- ## Installation and Deployment Guide
- ## End User Guide

Documentation must not be embedded inside code comments.

Documentation is part of the deliverable.

---

## Operational Discipline Rule

Code is not considered production-ready unless:

- QA validation steps exist
- Deployment instructions exist
- Error identification guidance exists
- Rollback path exists
- User impact is documented or explicitly ruled out

Engineering completeness includes operational clarity.

---

## Metadata Interaction Rule

If metadata is available:

- Reference environment explicitly in documentation.
- Confirm fields referenced in UAT steps exist.
- Confirm deployment contexts align with metadata environment.

Never generate documentation that contradicts selected metadata environment.

---

## Governance Awareness in Documentation

All UAT and Deployment guides must include:

- Governance unit expectations
- Execution context considerations
- Scheduled vs User Event vs Map/Reduce implications
- Performance considerations in multi-entity environments

Operational documentation must reflect real NetSuite constraints.

---

# Final Behavioral Rules

If metadata exists:

- Use it.
- Never override it.
- Never hallucinate around it.

If metadata does not exist:

- Ask.
- Clarify.
- Do not guess.

Every non-trivial SuiteQL must include:

- Explicit WHERE clause.
- Explicit columns.
- Explicit environment reference.
- QA validation plan.

This skill enforces disciplined NetSuite engineering aligned with:

- Constitution invariants
- Oracle official best practices
- Schema-aware development
- Production-safe deployment

---

# License and Disclaimer

This skill is licensed under the Creative Commons Attribution 4.0 International License (CC-BY-4.0).
https://creativecommons.org/licenses/by/4.0/

You are free to share and adapt this material provided proper attribution is given.

This material is provided "as-is" without warranty of any kind, express or implied, including but not limited to:

- Fitness for a particular purpose
- Non-infringement
- Production readiness
- Regulatory compliance

NetSuite is a trademark of Oracle Corporation and its affiliates.

Author: Joshua Meiri  
Origami Precision, LLC

