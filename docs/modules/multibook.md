# Multi-Book Accounting Module

This module applies when `multibook: true` for the selected environment in `docs/modules/netsuite-features.json`.

## Scope

Apply this module when implementing or modifying logic that can impact:

- Transaction posting behavior
- General ledger impact
- Revenue recognition behavior
- Currency behavior
- Accounting-related classifications
- Integrations that depend on posting outcomes

If the change is purely non-financial and cannot affect accounting outcomes, state why Multi-Book is not relevant.

## Required Questions

Before generating code that affects financial behavior, confirm:

- Which accounting books are in scope (primary only, or primary and secondary)
- Whether behavior must differ per book
- Whether any posting, recognition, or reclassification is book-specific

If answers are unknown, explicitly declare assumptions and generate a validation plan to confirm them.

## Invariants

1. Multi-Book behavior must be explicitly accounted for when `multibook: true`.
2. Primary-book behavior must not be assumed to represent all books.
3. Book-specific posting, recognition, and reporting differences must be validated per book.
4. Financial-impacting logic must define expected behavior per applicable accounting book.

## Engineering Rules

### SuiteScript

- If the script changes transaction fields that can affect posting, document the expected posting impact.
- If the script reads posting results, document which book results are expected and why.
- If the script is expected to behave identically across books, explicitly state that as a requirement.

### Integrations

- If integrations consume GL impact, revenue schedules, or accounting outputs, confirm whether the integration is book-aware.
- If the integration is not book-aware, document how Multi-Book differences are handled.

### SuiteQL

- When querying accounting-related outcomes, explicitly document which book context is intended.
- Avoid implicit assumptions about posting results being single-book.

## QA and UAT Validation Steps

When Multi-Book is in scope, include a validation section:

### Multi-Book Validation

- Validate expected behavior in primary book.
- Validate expected behavior in each applicable secondary book.
- Validate that posting impact and downstream reporting are consistent with the specification.
- Validate that any saved searches, reports, or exports used operationally still reconcile per book.

## Deployment and Admin Notes

- Document any role permissions required to view book-specific results.
- Document any setup dependencies that differ between books.
- Document rollback considerations per book.
