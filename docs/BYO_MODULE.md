# Bring Your Own Modules (BYO Modules)

The netsuite-developer Skill supports modular feature enforcement.

Modules allow teams to extend the Skill with additional invariants tied to NetSuite features.

---

## What Is a Module

A module is a Markdown file located under:

    docs/modules/

Each module:

- Defines feature-specific invariants
- Adds QA validation requirements
- Adds deployment and admin guidance
- Expands enforcement when feature is enabled

A module does not have to strictly be a NetSuite feature, it can be a localization or even an internal standard.

---

## Feature Enablement File

Modules are activated using:

    docs/modules/netsuite-features.json

Example:

{
  "schema_version": "1.0",
  "defaults": {
    "assume_unknown_when_missing": true
  },
  "environments": [
    {
      "env_key": "QA",
      "account_id": "123456_QA",
      "features": {
        "multibook": true,
        "arm": true,
        "suitebilling": false,
        "fiscalcalendars": true
      }
    }
  ]
}

Semantics:

- true → apply module
- false → do not apply
- missing key → unknown
- missing environment → unknown

---

## Naming Convention

Feature key:

    snake_case

Module file:

    docs/modules/<feature_key>.md

Examples:

    multibook → docs/modules/multibook.md
    fiscalcalendars → docs/modules/fiscalcalendars.md

---

## Adding a New Module

1. Create:

    docs/modules/<feature_key>.md

2. Add feature flag to:

    docs/modules/netsuite-features.json

3. Define:

- Scope
- Required questions
- Invariants
- Engineering rules
- QA steps
- Deployment notes

---

## Proprietary Modules

Modules may be:

- Public
- Private
- Client-specific
- Regulatory-specific

The system does not require modules to be public.

You may deploy internal enforcement packs without sharing them externally.

---

## Module Applicability Discipline

When modules are enabled for an environment, scripts must declare:

- Applicable modules
- Non-applicable modules with rationale
- Validation notes

This eliminates assumption drift and enforces deterministic engineering.
