# SmartBank Financial BI & Reporting Dashboard

## BI Data Dictionary

### Field: `transaction_id`

**Business Name:**  
Transaction ID

**Purpose:**  
Uniquely identifies each transaction in the SmartBank transaction dataset.

**Data Type:**  
Integer or String/UUID, depending on the final database implementation.

**Required:**  
Yes

**NULL Allowed:**  
No

**Business Rule:**  
Each transaction should have a unique `transaction_id`.

**QA Validation:**

QA should verify:

- `transaction_id` is not NULL.
- `transaction_id` is unique.
- Every transaction has a valid identifier.
- The same transaction ID is consistent across the database, API, and dashboard transaction table.

**SQL Validation — NULL Values:**
```sql
SELECT COUNT(*) AS Null_Transaction_IDs
FROM transactions
WHERE transaction_id IS NULL;
```

**Expected Result:**
```text
Null_Transaction_IDs = 0
```

**SQL Validation — Duplicate IDs:**
```sql
SELECT
    transaction_id,
    COUNT(*) AS ID_Count
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;
```

**Expected Result:**

No rows should be returned.

**QA Risk:**  
NULL or duplicate transaction IDs can cause incorrect transaction counts, duplicate dashboard records, inaccurate KPI calculations, and unreliable transaction-level reconciliation.
### Field: `transaction_date`

**Business Name:**  
Transaction Date

**Purpose:**  
Stores the date and time when the transaction occurred. This field is used for reporting-period filters, time-based analysis, and dashboard trend calculations.

**Data Type:**  
DATETIME / TIMESTAMP

**Required:**  
Yes

**NULL Allowed:**  
No

**Business Rule:**  
Every valid transaction should have a transaction date.

**QA Validation:**

QA should verify:

- `transaction_date` is not NULL.
- The value is a valid date/time.
- The date can be used correctly for reporting-period filters.
- Transactions are included or excluded correctly based on the selected date range.
- The same transaction date is consistent across the database, API, and dashboard.

**SQL Validation — NULL Values:**
```sql
SELECT COUNT(*) AS Null_Transaction_Dates
FROM transactions
WHERE transaction_date IS NULL;
```

**Expected Result:**
```text
Null_Transaction_Dates = 0
```

**SQL Validation — Future Dates:**

```sql
SELECT *
FROM transactions
WHERE transaction_date > GETDATE();
```

**Expected Result:**

No rows should be returned unless future-dated transactions are intentionally supported by the business requirement.

**SQL Validation — Reporting Period:**

Example: transactions from the last 30 days:

```sql
SELECT *
FROM transactions
WHERE transaction_date >= DATEADD(DAY, -30, GETDATE());
```

**QA Risk:**  
NULL, invalid, future, or incorrectly filtered transaction dates can cause inaccurate dashboard KPIs, incorrect time-period calculations, missing transactions, or incorrect trend charts.
## Financial Transaction Data Standards

### Financial Amount Precision

| Rule | Standard |
|---|---|
| Storage type | `DECIMAL(19,4)` |
| Authoritative value | Stored value |
| Calculation | Preserve stored precision |
| Aggregation | Aggregate before rounding |
| Dashboard display | 2 decimal places |
| QA reconciliation | Validate underlying values before display rounding |
| FLOAT | Not used for authoritative monetary values |

> **Example:** `10.005 + 10.005 + 10.005 = 30.015`, displayed as **$30.02** after aggregation and rounding.

### Core Transaction Fields

| Field | Business Name | Data Type | Required | NULL | Key QA Validation |
|---|---|---|---|---|---|
| `transaction_id` | Transaction ID | Integer/String | Yes | No | Unique, not NULL |
| `transaction_date` | Transaction Date | DATETIME/TIMESTAMP | Yes | No | Valid date, reporting-period filtering |
| `account_id` | Account ID | Integer/String | Yes | No | Valid account reference |
| `customer_id` | Customer ID | Integer/String | Yes | No | Valid customer reference |
| `transaction_type` | Transaction Type | VARCHAR | Yes | No | Valid business value |
| `transaction_amount` | Transaction Amount | DECIMAL(19,4) | Yes | No | Precision, scale, aggregation, reconciliation |
| `status` | Transaction Status | VARCHAR | Yes | No | Valid status; KPI filtering |
| `quantity` | Quantity | DECIMAL(19,6) | No | Yes | Supports fractional quantities |
| `unit_price` | Unit Price | DECIMAL(19,6) | No | Yes | Precision and calculation validation |
| `security_id` | Security ID | Integer/String | No | Yes | Valid security reference |

### Financial QA Rules

- Monetary calculations must use exact decimal values.
- Do not use floating-point values as the authoritative financial value.
- Rounding must occur at the defined business/presentation boundary.
- SQL, API, Pandas, and dashboard results must reconcile to the same underlying financial value.
- NULL and zero must be handled according to the applicable business rule.
