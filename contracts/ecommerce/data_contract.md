# Data Contract: customer_nation

## Data Product Description
This data product contains comprehensive customer information, including personal details, contact information, account balance, and associated nation details, crucial for e-commerce operations and customer relationship management.

## Owner
*   **Name**: Gaurav Bole
*   **Email**: gauravbole2@gmail.com

## Tags
*   Customer
*   e-commerce
*   CRM
*   Personal Data
*   Account

## Schema

| Column Name | Type | Description | PII | Constraints |
| :---------- | :--- | :---------- | :-- | :---------- |
| `c_custkey` | number | Unique identifier for the customer. | Yes | Primary Key, Unique |
| `c_name` | varchar | Full name of the customer. | Yes | - |
| `c_address` | varchar | Physical address of the customer. | Yes | - |
| `c_nationkey` | number | Foreign key linking to the nation table, representing the customer's nation. | No | Foreign Key to `nation`.`n_nationkey` |
| `c_phone` | varchar | Customer's phone number. | Yes | - |
| `c_acctbal` | number | Current account balance of the customer. | No | - |
| `c_comments` | varchar | General comments or notes about the customer. This field may contain sensitive or personal information. | Yes | - |
| `n_names` | varchar | Name of the nation associated with the customer. | No | - |

## Data Refresh
*   **Frequency**: daily
*   **Method**: full_load
*   **Schedule**: `0 2 * * *`

## Service Level Agreement (SLA)
*   **Freshness**: Daily
*   **Delivery Window**: Between 2:00 AM and 3:00 AM UTC daily
*   **Availability**: Not specified
*   **Max Null Rate**: 1%
*   **Incident Response**:
    *   **Notify**: gauravbole2@gmail.com
    *   **Within**: 60 minutes

## Data Quality Rules

### Column: `c_custkey`
*   **Customer key not null**: `not_null`
*   **Customer key unique**: `unique`
*   **Customer key type check**: `expect_column_values_to_be_of_type` (logic: `number`)
*   **Customer key min value**: `expect_column_min_to_be_between` (min: `1.0`, max: `10000000.0`)

### Column: `c_name`
*   **Customer name not null**: `not_null`
*   **Customer name type check**: `expect_column_values_to_be_of_type` (logic: `varchar`)
*   **Customer name length**: `expect_column_value_lengths_to_be_between` (min: `2.0`, max: `100.0`)
*   **Customer name consistent casing**: `expect_column_values_to_have_consistent_casing` (logic: `title`)

### Column: `c_address`
*   **Customer address not null**: `not_null`
*   **Customer address type check**: `expect_column_values_to_be_of_type` (logic: `varchar`)
*   **Customer address length**: `expect_column_value_lengths_to_be_between` (min: `5.0`, max: `200.0`)

### Column: `c_nationkey`
*   **Nation key not null**: `not_null`
*   **Nation key type check**: `expect_column_values_to_be_of_type` (logic: `number`)
*   **Nation key foreign key**: `foreign_key` (logic: `{{ ref('dim_nations') | dbt_utils.get_column_values('n_nationkey') }}`)
*   **Nation key min value**: `expect_column_min_to_be_between` (min: `0.0`, max: `100.0`)

### Column: `c_phone`
*   **Phone not null**: `not_null`
*   **Phone type check**: `expect_column_values_to_be_of_type` (logic: `varchar`)
*   **Phone regex pattern**: `regex` (pattern: `^\d{2}-\d{3}-\d{3}-\d{4}$`)
*   **Phone length**: `expect_column_value_lengths_to_be_between` (min: `12.0`, max: `15.0`)

### Column: `c_acctbal`
*   **Account balance not null**: `not_null`
*   **Account balance type check**: `expect_column_values_to_be_of_type` (logic: `number`)
*   **Account balance range**: `range` (min: `-1000.0`, max: `100000.0`)
*   **Account balance mean**: `expect_column_mean_to_be_between` (min: `100.0`, max: `50000.0`)

### Column: `c_comments`
*   **Comments type check**: `expect_column_values_to_be_of_type` (logic: `varchar`)
*   **Comments length**: `expect_column_value_lengths_to_be_between` (min: `0.0`, max: `500.0`)

### Column: `n_names`
*   **Nation name not null**: `not_null`
*   **Nation name type check**: `expect_column_values_to_be_of_type` (logic: `varchar`)
*   **Nation name unique**: `unique`
*   **Nation name consistent casing**: `expect_column_values_to_have_consistent_casing` (logic: `title`)
*   **Nation distinct count**: `expect_column_distinct_count_to_be_greater_than` (min: `5.0`)

## Allowed Operations
*   read
*   write

## Contract Approval
*   **Approved**: Yes
*   **Approved By**: gauravbole2@gmail.com

## Retention Policy
*   **Type**: time-based
*   **Duration**: 7 years