# Fiscal Calendars Module

This module applies when `fiscalcalendars: true` for the selected environment in `docs/modules/netsuite-features.json`.

This module assumes the Multiple Calendars feature is enabled in a OneWorld account.

Fiscal Calendars primarily impact **derived accounting values**, not transaction creation.

---

## Core Principle

Posting Period is a derived value:

    Transaction Date → Subsidiary → Assigned Fiscal Calendar → Derived Posting Period

Do not assume:

- January = Period 1
- Month-end = Period-end
- All subsidiaries share the same fiscal year
- Calendar year boundaries define financial year boundaries

All period logic must be calendar-aware.

---

## Scope

Apply this module when implementing or modifying logic that impacts:

- Posting period derivation
- Accounting date handling
- Financial reporting logic
- Retained earnings rollover assumptions
- Intercompany journal automation
- Consolidation logic
- Period-based validation
- Backfills into historical periods

If the change does not interact with posting periods, explicitly state why.

---

## Primary Impact Areas

### 1. Derived Posting Period

Active posting period options are restricted by:

- The subsidiary's assigned fiscal calendar
- The fiscal year structure (e.g., July 1 start)
- Period close state

Scripts must derive posting periods from:

- Transaction date
- Subsidiary
- Fiscal calendar

Never hardcode accounting period internal IDs.

---

### 2. Financial Reporting & Retained Earnings

Fiscal calendars determine:

- Financial year boundaries
- Retained earnings rollover timing
- Income statement vs balance sheet period grouping

Scripts impacting financial reporting must:

- Respect fiscal year-end defined by the subsidiary’s calendar
- Avoid assuming calendar-year rollovers

---

### 3. Intercompany & Multi-Subsidiary Logic

Different subsidiaries may have:

- Different fiscal year start dates
- Different year-end boundaries

When generating:

- Intercompany journal entries
- Cross-subsidiary automation
- Consolidation logic

The script must handle potential differences in fiscal year boundaries.

---

### 4. 4-4-5 and 52/53 Week Calendars

If using 4-4-5 or 52/53 week calendars:

- Period boundaries may not align with month start or end
- Month-end date math will fail

SuiteScripts must rely on:

- The `accountingperiod` record
- Derived posting period logic
- Period lookup, not date arithmetic

Never calculate posting periods using month-end assumptions.

---

## Engineering Rules

### SuiteScript

- If updating `trandate`, re-verify or re-derive `postingperiod`.
- If explicitly setting `postingperiod`, validate:
  - It belongs to the subsidiary’s fiscal calendar
  - It is open
  - It is valid for the transaction type
- When searching `accountingperiod`, filter by:
  - Fiscal calendar
  - Subsidiary context when relevant

Avoid:

- Hardcoded period IDs
- Month-based assumptions
- Cross-subsidiary period reuse without validation

---

### Integrations

If integrations create or update posting transactions:

- Document which date drives posting.
- Confirm how NetSuite derives posting period.
- Define explicit behavior when:
  - The derived period is closed
  - The period belongs to a different fiscal year
- Ensure retries do not result in posting into unintended periods.

---

### SuiteQL

When querying accounting periods:

- Filter by fiscal calendar where applicable.
- Validate that returned periods match the intended subsidiary context.
- Do not assume period numbering consistency across calendars.

Include QA validation steps tied to fiscal calendar correctness.

---

## QA and UAT Validation Steps

When fiscal calendars are in scope, include:

### Fiscal Calendar Validation

- Validate posting in an open period for Subsidiary A.
- Validate posting in an open period for Subsidiary B (with different fiscal year start if applicable).
- Validate behavior at fiscal year boundary.
- Validate behavior when derived period is closed.
- Validate that financial reports reflect correct fiscal grouping.
- If 4-4-5 or 52/53 week calendar is used, validate boundary behavior explicitly.

---

## Error Handling Requirements

Closed or invalid period scenarios must:

- Fail explicitly
- Log:
  - Subsidiary
  - Transaction date
  - Derived posting period
  - Fiscal calendar context
- Document resolution path

No silent fallback to a different period.

---

## Deployment and Admin Notes

- Document fiscal calendar assumptions per subsidiary.
- Document dependencies on open periods.
- Do not recommend reopening closed periods as a default resolution.
- Include rollback considerations for mis-posted transactions.