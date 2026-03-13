# SuiteTax Module
This module applies when `suitetax: true` for the selected environment in `docs/modules/netsuite-features.json`.

## Scope
Apply this module when implementing or modifying logic that can impact:
* Transaction creation or updates (Sales Orders, Invoices, Vendor Bills, Expense Reports)
* Tax calculation, tax overrides, or external tax data imports
* Entity tax registrations or Subsidiary nexuses
* Integrations (REST, SOAP, CSV) that pass financial or tax data
* Custom reporting or SuiteQL queries retrieving tax amounts

If the change is purely non-financial and does not interact with transaction line items or taxes, state why SuiteTax is not relevant.

## Required Questions
Before generating code that interacts with transactions or taxes, confirm:
* **Calculation Authority:** Will the NetSuite SuiteTax Engine calculate the taxes, or will the integration push pre-calculated exact tax amounts (requiring `Tax Details Override`)?
* **Transaction Type:** Is the transaction an Expense Report? (Expense Reports do not auto-calculate taxes in SuiteTax and require explicit tax mapping).
* **Jurisdiction/Use Case:** Are US Purchase Taxes (Use Tax) involved? (These are not auto-provisioned and require specific override configurations).

If answers are unknown, explicitly declare assumptions and generate a validation plan to confirm them.

## Invariants
1. **Legacy Deprecation:** Legacy tax fields (e.g., line-level `taxcode`, `taxrate`, `taxamount`) are inaccessible. Any script or integration attempting to read or write to these fields will throw a null pointer exception.
2. **Sublist Architecture:** All tax data resides on the `Tax Details` sublist, not on the main transaction item lines.
3. **Reference Linking:** A single item line can have multiple tax lines. Every line on the `Tax Details` sublist must be linked to its corresponding item/expense line using the `Tax Details Reference` string.
4. **Override Strictness:** If passing pre-calculated taxes from an external system, `Tax Details Override` must be set to true, and all tax columns (`Tax Type`, `Tax Code`, `Tax Basis`, `Tax Rate`, `Tax Amount`) become mandatory.

## Engineering Rules

### SuiteScript
* Never use `record.getSublistValue` or `record.setSublistValue` for legacy tax fields on the `item` or `expense` sublists.
* When reading tax data, iterate through the `taxdetails` sublist and map taxes back to items using the `taxdetailsreference`.
* If modifying tax amounts via script, you must check the `taxdetailsoverride` box. Modifying tax lines without the override checked will result in the engine overwriting your changes upon save.

### Integrations (REST / Web Services / CSV)
* **Approach A (Engine Calculates):** Ensure payloads omit all explicit legacy tax fields. Send `Net Amount` on the item line and allow NetSuite to calculate `Tax Amount` and `Gross Amount`.
* **Approach B (External Override):** Ensure payload explicitly maps:
  * Header: `Nexus Override` = true (and provide Nexus), `Tax Details Override` = true.
  * Item Sublist: Provide `Tax Details Reference`.
  * Tax Details Sublist: Provide `Tax Details Reference`, `Tax Type`, `Tax Code`, `Tax Basis` (Net Amount), `Tax Rate`, and exact `Tax Amount`.
* **Expense Reports Exception:** For Expense Reports, you must manually explicitly map the nexus and all tax details in the payload; the tax engine does not auto-populate these.

### SuiteQL
* Do not query legacy transaction line tax columns.
* Query the new SuiteTax tables for tax reporting.
* Always validate the schema for the `Tax Details` sublist tables using the metadata helper before generating the query.

## QA and UAT Validation Steps
When SuiteTax is in scope, include a validation section:

### SuiteTax Validation
* Verify that no legacy tax fields are referenced in the script or payload.
* Create a test transaction via the script/integration and confirm it saves without tax-related null pointer exceptions.
* If using **Tax Details Override**: Confirm that the exact tax amount provided by the external system is preserved and that NetSuite did not recalculate or round the amount upon saving.
* If testing **Expense Reports**: Verify that the transaction is recognized as taxable and that the Nexus and Tax Registration fields successfully populated.
* Verify that the Gross Amount mathematically aligns with the provided Tax Basis (Net Amount) + Tax Amount.

## Deployment and Admin Notes
* **Permissions:** Document that the integration role or executing user MUST have at least the **Edit** level of the "Tax Details Tab" permission. Without this, the script or API will be blocked from using the override or editing tax lines.
* **Feature Enablement:** Note that SuiteTax is a non-reversible feature.
* **External Setup Dependencies:** If integrating US Purchase Taxes via an external system (like Mesh), document the administrative requirement to manually create a generic 0% Tax Type and Tax Code in NetSuite for the integration to map to.
