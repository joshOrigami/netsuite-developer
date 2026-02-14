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

