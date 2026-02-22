# SuiteBilling Module

This module applies when `suitebilling: true` for the selected environment in `docs/modules/netsuite-features.json`.

## Scope

Apply this module when implementing or modifying logic that can impact:

- Billing accounts
- Subscriptions
- Subscription line changes
- Billing schedules
- Usage-based billing inputs
- Renewals, amendments, cancellations
- Invoicing automation tied to subscription events

If the change cannot affect subscription-to-invoice behavior, state why SuiteBilling is not relevant.

## Required Questions

Before generating code that impacts billing behavior, confirm:

- Whether billing is subscription-driven in this account
- Which subscription lifecycle events are in scope (create, amend, renew, cancel)
- Whether usage-based billing is involved

If answers are unknown, explicitly declare assumptions and generate a validation plan to confirm them.

## Invariants

1. Any change that impacts subscriptions or subscription-related records must explicitly state the expected invoicing outcome.
2. Billing-impacting changes must be validated end-to-end: subscription event → billing schedule behavior → invoice generation.

## Engineering Rules

### SuiteScript

- If updating subscription records or related records, document downstream billing impact.
- Avoid hidden side effects that trigger unintended billing runs.
- Include idempotency protections when scripts are triggered by subscription events.

### Integrations

- If integrations create or update subscriptions, enforce idempotency and deduplication.
- Document how integration retries avoid duplicate billing or duplicate subscription changes.
- Include reconciliation steps to ensure invoices align with subscription state.

### SuiteQL

- Do not guess joins between subscription, billing, and invoice records. Use validated schema references.
- Include QA validation steps that confirm end-to-end billing correctness.

## QA and UAT Validation Steps

When SuiteBilling is in scope, include a validation section:

### SuiteBilling Validation

- Create or identify a test subscription scenario.
- Trigger the relevant lifecycle event (create, amend, renew, cancel).
- Confirm billing schedule behavior matches expectations.
- Confirm invoice generation behavior matches expectations.
- Confirm no duplicate invoices occur under retry or reprocessing scenarios.
- Confirm reporting and downstream integrations reconcile.

## Deployment and Admin Notes

- Document any SuiteBilling configuration dependencies.
- Document any scheduled processes that interact with billing runs.
- Document rollback strategy if billing or invoices are impacted.
