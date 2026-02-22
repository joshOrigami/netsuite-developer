# Advanced Revenue Management Module

This module applies when `arm: true` for the selected environment in `docs/modules/netsuite-features.json`.

## Scope

Apply this module when implementing or modifying logic that can impact:

- Revenue Arrangements
- Revenue Elements
- Revenue Plans
- Revenue Rules
- Standalone Selling Price (SSP) allocation
- Revenue recognition timing or schedules

If the change cannot affect revenue recognition, state why ARM is not relevant.

## Required Questions

Before generating code that impacts revenue recognition, confirm:

- Which transaction types are in scope
- Whether ARM is responsible for recognition in this account
- Whether the change affects allocation, arrangement creation, or plan creation

If answers are unknown, explicitly declare assumptions and generate a validation plan to confirm them.

## Invariants

1. Any change that impacts revenue-related fields must explicitly state expected downstream effects on Revenue Arrangements, Revenue Elements, and Revenue Plans.
2. Do not modify ARM-managed records unless the specification explicitly requires it and the impact is documented.
3. ARM-impacting changes must be validated end-to-end: transaction input → arrangement and element correctness → plan creation → recognition schedule behavior.

## Engineering Rules

### SuiteScript

- If writing to fields used by ARM, document the impact on arrangement creation or updates.
- Avoid modifying ARM-managed records unless explicitly required and documented.
- Prefer configuration-driven ARM behavior over hard-coded overrides when feasible.

### Integrations

- If integrations set revenue-related fields, document which fields ARM consumes and how idempotency is preserved.
- If integrations create transactions that trigger ARM, include reconciliation steps to confirm arrangements and plans.

### SuiteQL

- Do not guess joins between ARM records. Use validated schema references.
- When providing SuiteQL for ARM reporting or validation, include a QA validation plan that checks:
  - arrangement creation
  - element correctness
  - plan creation
  - recognition schedule correctness

## QA and UAT Validation Steps

When ARM is in scope, include a validation section:

### ARM Validation

- Create or identify a test transaction that triggers ARM.
- Confirm expected Revenue Arrangement is created or updated.
- Confirm Revenue Elements are correct and aligned with the specification.
- Confirm Revenue Plans are created with correct dates, amounts, and rules.
- Confirm recognition schedule and posting behavior match expected outcomes.
- Confirm any changes do not break historical recognition or reporting.

## Deployment and Admin Notes

- Document any ARM configuration dependencies.
- Document any roles required to view ARM records.
- Document rollback and data correction strategy if arrangements or plans are impacted.
