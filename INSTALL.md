# Installation Guide

## Requirements
- Python 3.9+
- VSCode
- OpenAI Codex Extension

Verify Python:
    python --version

## Install Skill
Place SKILL.md into:
    <project-root>/.codex/skills/netsuite-developer/

## Install Python Helper
Place:
    <project-root>/tools/query_metadata.py
inside your project root.

## Metadata Structure
.netsuite-metadata/<ENV>/
    manifest.json
    record_index.json
    records/

## Test Python Helper
python tools/query_metadata.py --env QA list-records

## Optional Modules

Modules extend enforcement for enabled NetSuite features.

### Module Files

Place module files under:

    docs/modules/

Examples:

    docs/modules/multibook.md
    docs/modules/arm.md
    docs/modules/suitebilling.md
    docs/modules/fiscalcalendars.md

### Feature Enablement File

Create:

    docs/modules/netsuite-features.json

Example structure:

{
  "schema_version": "1.0",
  "defaults": {
    "assume_unknown_when_missing": true
  },
  "environments": [
    {
      "env_key": "SB1",
      "account_id": "123456_SB1",
      "features": {
        "multibook": true,
        "arm": true,
        "suitebilling": true,
        "fiscalcalendars": true
      }
    }
  ]
}

Rules:

- true = module applied
- false = module not applied
- missing key = unknown (not implicitly false)
- missing environment = unknown

---

## Proprietary Modules

You may maintain private modules:

- Company-specific invariants
- Client-specific enforcement rules
- Regulatory requirements

These do not need to be public.

The core Skill supports modular extension without restriction.
