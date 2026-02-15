# Bring Your Own Metadata

This project is provider-neutral.

[origami lens](https://origamilens.com/) is one metadata provider, but any system can be used if it exports a compatible schema package.

This document defines the public, portable contract for a metadata export package that can be consumed by:

- `tools/query_metadata.py`
- the `netsuite-developer` Codex Skill

## Design goals

- Deterministic, schema-aware development for SuiteQL and SuiteScript 2.x
- Multi-environment support with arbitrary names such as SB, QA, PROD, UAT
- Provider-neutral contract
- No business data and no personally identifiable information

## Key terms

- Environment (ENV): the folder name chosen by the user such as SB, QA, PROD, UAT
- Metadata provider: any system that outputs this contract
- Contract: JSON describing records, fields, relationships, and capabilities

## User flow

1. Export a ZIP for a specific NetSuite account context, application context, and environment context
2. Extract the ZIP into a project folder at:

   `.netsuite-metadata/<ENV>/`

3. Run the helper using the selected environment:

   `python tools/query_metadata.py --env <ENV> ...`

4. The Codex Skill consults the helper output before generating schema-dependent logic

## Package format

### Download artifact

- One ZIP file
- Filename should include:
  - account identifier
  - environment name
  - export timestamp
  - provider name

Example filename pattern:

- `netsuite-metadata_<accountId>_<env>_<utcTimestamp>_<provider>.zip`

Timestamp format:

- ISO 8601 basic with Zulu, for example `20260213T213000Z`

### ZIP contents

The ZIP must contain exactly one top-level folder matching the environment name.

Example:

    QA/
      manifest.json
      record_index.json
      relationship_index.json
      script_deployments.json
      records/
        transaction.json
        salesorder.json
        customer.json
        customrecord_foo.json

When extracted into a repo, it becomes:

    .netsuite-metadata/
      QA/
        manifest.json
        record_index.json
        relationship_index.json
        script_deployments.json
        records/
          ...

## Contract files

### 1. manifest.json

Purpose: provenance, compatibility, and context.

Required fields:

```json
{
  "contract_version": "1.0.0",
  "provider": {
    "name": "provider-name",
    "version": "X.Y.Z"
  },
  "source": {
    "system": "netsuite",
    "account_id": "1234567",
    "account_name": "ACME",
    "environment": "QA"
  },
  "app_context": {
    "app_id": "your-app-id",
    "app_version": "X.Y.Z",
    "export_scope": "schema_only",
    "feature_flags": []
  },
  "exported_at": "2026-02-13T21:30:00Z",
  "data_classification": "schema_only",
  "notes": "No transactional data. No PII."
}
```

Rules:

- `source.environment` must equal the top folder name
- `app_context.export_scope` must remain `schema_only` for this contract version
- `exported_at` must be UTC

### 2. record_index.json

Purpose: discoverability and lookup.

Required structure:

```json
{
  "records": [
    {
      "record_key": "transaction",
      "record_type": "transaction",
      "record_family": "standard",
      "label": "Transaction",
      "file": "records/transaction.json"
    }
  ]
}
```

Rules:

- `file` must be a relative path inside the environment folder
- `record_key` must be unique in the array

### 3. records/<record_key>.json

Purpose: record schema and relationship hints.

Required structure:

```json
{
  "record_key": "salesorder",
  "record_type": "salesorder",
  "label": "Sales Order",
  "record_family": "standard",
  "primary_table": {
    "suiteql_table": "transaction",
    "suiteql_type_filter": "SalesOrd"
  },
  "fields": {
    "id": {
      "label": "Internal ID",
      "field_type": "integer",
      "nullable": false,
      "suiteql_column": "id"
    },
    "entity": {
      "label": "Customer",
      "field_type": "record_ref",
      "nullable": true,
      "suiteql_column": "entity",
      "ref": {
        "target_record_key": "customer",
        "relationship": "many_to_one"
      }
    }
  },
  "line_tables": [
    {
      "line_key": "item",
      "suiteql_table": "transactionline",
      "join": {
        "left_table": "transaction",
        "left_column": "id",
        "right_table": "transactionline",
        "right_column": "transaction"
      }
    }
  ],
  "capabilities": {
    "suiteql": true,
    "rest_record": true,
    "sdf": true
  }
}
```

Field type enumeration for v1:

- integer
- number
- text
- date
- datetime
- boolean
- select
- record_ref
- multi_select
- json

Rules:

- `suiteql_column` is required for any field where `capabilities.suiteql` is true
- For record references, `ref.target_record_key` is required

### 4. relationship_index.json

Optional but recommended.

Purpose: precomputed join paths.

Structure:

```json
{
  "relationships": [
    {
      "from_record_key": "salesorder",
      "from_field_id": "entity",
      "to_record_key": "customer",
      "join": {
        "from_table": "transaction",
        "from_column": "entity",
        "to_table": "customer",
        "to_column": "id"
      }
    }
  ]
}
```

## Determinism requirements

- For the same inputs, output should be stable except timestamps
- Record keys must be stable and diff-friendly
- Paths inside the ZIP must be relative
- Do not include hidden operating system artifacts

## Validation requirements

Before producing the ZIP, a provider should validate:

- `manifest.json` exists and parses
- `record_index.json` exists and parses
- every file referenced by `record_index.json` exists and parses
- no duplicate `record_key` values exist
- `field_type` values conform to the enumeration
- relationship references point to valid record keys when present

## Compatibility requirements

The helper expects:

- `.netsuite-metadata/<ENV>/manifest.json`
- `.netsuite-metadata/<ENV>/record_index.json`
- `.netsuite-metadata/<ENV>/records/*.json`

The skill behavior depends on:

- environment selection
- schema lookup by `record_key`
- field existence checks
- join hints

