# SmartBank Financial BI & Reporting Dashboard

## KPI Definitions

### KPI-001 — Total Transactions

**KPI Name:** Total Transactions

**Business Definition:**  
The total number of transactions included within the selected reporting period and applicable dashboard filters.

**Calculation:**

```text
Total Transactions = COUNT(Transaction ID)
```

**Example:**

If the selected reporting period contains 125 transactions:

```text
Total Transactions = 125
```

**QA Validation Rule:**

The following values should reconcile when the same reporting period and filters are applied:

- SQL transaction count
- API transaction count
- Dashboard Total Transactions KPI
- Transaction table record count

**Expected Result:**  
All applicable layers should return the same transaction population and count.

**Important Business Rule:**  
The transaction date and reporting-period boundary rules must be defined consistently across SQL, API, and dashboard calculations.

**Test Risk:**  
A mismatch may indicate an incorrect date filter, missing transaction records, duplicate records, incorrect API filtering, or an incorrect dashboard calculation.
### KPI-002 — Total Transaction Amount

**KPI Name:** Total Transaction Amount

**Business Definition:**  
The total monetary value of all transactions included within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Total Transaction Amount = SUM(Transaction Amount)
```

**Example:**
If the selected transactions have amounts of $100, $250, and $150:

```text
Total Transaction Amount = $500
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL transaction amount
- API transaction amount
- Dashboard Total Transaction Amount KPI
- Transaction table transaction amounts

**Expected Result:**  
All applicable layers should calculate the same total transaction amount.

**Important Business Rule:**  
Only transactions included within the selected reporting period and applicable filters should contribute to the total amount.

**Test Risk:**  
A mismatch may indicate missing transactions, duplicate records, incorrect filtering, incorrect transaction amounts, rounding issues, or an incorrect dashboard calculation.
### KPI-003 — Completed Transactions

**KPI Name:** Completed Transactions

**Business Definition:**  
The total number of transactions with a status of **Completed** within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Completed Transactions = COUNT(Transaction ID)
WHERE Transaction Status = 'Completed'
```

**Example:**
If 1,000 transactions occurred and 950 have a status of `Completed`:

```text
Completed Transactions = 950
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL count of Completed transactions
- API count of Completed transactions
- Dashboard Completed Transactions KPI
- Transaction table count of Completed records

**Expected Result:**  
All applicable layers should return the same count of Completed transactions.

**Important Business Rule:**  
Only transactions with an exact status of `Completed` should be included in this KPI.

**Test Risk:**  
A mismatch may indicate incorrect status filtering, missing transactions, duplicate records, incorrect date filtering, or an incorrect dashboard calculation.
### KPI-004 — Failed Transactions

**KPI Name:** Failed Transactions

**Business Definition:**  
The total number of transactions with a status of **Failed** within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Failed Transactions = COUNT(Transaction ID)
WHERE Transaction Status = 'Failed'
```

**Example:**
If 1,000 transactions occurred and 50 have a status of `Failed`:

```text
Failed Transactions = 50
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL count of Failed transactions
- API count of Failed transactions
- Dashboard Failed Transactions KPI
- Transaction table count of Failed records

**Expected Result:**  
All applicable layers should return the same count of Failed transactions.

**Important Business Rule:**  
Only transactions with an exact status of `Failed` should be included in this KPI.

**Test Risk:**  
A mismatch may indicate incorrect status filtering, missing transactions, duplicate records, incorrect date filtering, or an incorrect dashboard calculation.

**QA Investigation:**  
When failed transaction counts are identified, QA should be able to trace failed transactions to their transaction ID and investigate the associated failure reason or API response.
## NULL Handling and Data Quality Rules

### NULL-001 — Identify NULL Transaction Status

**Purpose:**  
QA should identify transactions where the transaction status is `NULL`.

**SQL Validation:**
```sql
SELECT COUNT(*) AS Null_Status_Count
FROM transactions
WHERE transaction_status IS NULL;
```

**Expected Result:**  
The query should identify the total number of transactions where `transaction_status` is `NULL`.

---

### NULL-002 — Total NULL Values

QA should validate the number of `NULL` values in important transaction fields.

**Example:**
```sql
SELECT
    COUNT(*) AS Total_Rows,
    COUNT(transaction_id) AS Transaction_ID_Count,
    COUNT(transaction_status) AS Status_Count
FROM transactions;
```

Because `COUNT(column)` does not count `NULL` values, the difference can help identify missing data.

For example:

```text
Total Rows              = 1,000
Transaction ID Count    = 1,000
Status Count            = 980
NULL Status Values     = 20
```

Therefore:

```text
NULL Status Values = Total Rows - Status Count
                   = 1,000 - 980
                   = 20
```

---

### NULL-003 — COALESCE Handling

QA should validate how the dashboard or SQL logic handles `NULL` values.

**Example:**
```sql
SELECT
    transaction_id,
    COALESCE(transaction_status, 'Unknown') AS transaction_status
FROM transactions;
```

If `transaction_status` is `NULL`, `COALESCE` replaces it with:

```text
Unknown
```

**Example:**

| Transaction ID | Original Status | COALESCE Result |
|---|---|---|
| 1001 | Completed | Completed |
| 1002 | Failed | Failed |
| 1003 | NULL | Unknown |

**QA Rule:**  
`NULL` values should not be silently converted to `Completed` or `Failed`. The business rule should explicitly define how missing values are represented.

**Expected Result:**  
The dashboard, API, and SQL validation should handle `NULL` values consistently.
### KPI-005 — Success Rate %

**KPI Name:** Success Rate %

**Business Definition:**  
The percentage of transactions that were successfully completed within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Success Rate % = (Completed Transactions / Total Transactions) × 100
```

**Example:**

If there are:

```text
Total Transactions     = 1,000
Completed Transactions = 950
```

Then:

```text
Success Rate % = (950 / 1,000) × 100
               = 95%
```

**SQL Example:**
```sql
SELECT
    COUNT(CASE
        WHEN transaction_status = 'Completed'
        THEN transaction_id
    END) * 100.0 / NULLIF(COUNT(transaction_id), 0) AS Success_Rate_Percent
FROM transactions;
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL calculated Success Rate %
- API calculated Success Rate %
- Dashboard Success Rate % KPI

**Expected Result:**  
The calculated percentage should match across applicable layers, subject to the agreed rounding rule.

**NULL and Zero-Division Rule:**  
`NULLIF` should prevent a division-by-zero error when there are no transactions in the selected reporting period.

```sql
NULLIF(COUNT(transaction_id), 0)
```

If there are zero transactions, the Success Rate should be handled according to the defined business rule rather than producing a SQL division-by-zero error.

**Important Business Rule:**  
Only transactions with status `Completed` should be counted as successful transactions.

**Test Risk:**  
A mismatch may indicate incorrect status filtering, incorrect transaction counts, division-by-zero handling, rounding differences, incorrect date filtering, or an incorrect dashboard calculation.
### KPI-006 — Average Transaction Amount

**KPI Name:** Average Transaction Amount

**Business Definition:**  
The average monetary value of transactions included within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text id="0g9kno"
Average Transaction Amount = Total Transaction Amount / Total Transactions
```

**Example:**

If:

```text id="6u3i4m"
Total Transaction Amount = $50,000
Total Transactions       = 1,000
```

Then:

```text id="31p3jh"
Average Transaction Amount = $50,000 / 1,000
                           = $50
```

**SQL Example:**
```sql id="8x1vjc"
SELECT
    AVG(transaction_amount) AS Average_Transaction_Amount
FROM transactions;
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL average transaction amount
- API average transaction amount
- Dashboard Average Transaction Amount KPI

**Expected Result:**  
The calculated average should match across applicable layers, subject to the agreed rounding rule.

**NULL Handling Rule:**  
`AVG()` ignores `NULL` values. QA should verify that this behavior is understood and consistent with the business requirement.

For example:

```text id="w7c5zn"
Transaction Amounts:
$100
$200
NULL
$300
```

SQL `AVG()` calculates:

```text id="e3fr7n"
($100 + $200 + $300) / 3 = $200
```

The `NULL` value is not treated as `$0`.

**QA Risk:**  
A mismatch may indicate incorrect NULL handling, incorrect filtering, duplicate records, incorrect transaction amounts, rounding differences, or an incorrect dashboard calculation.
### KPI-007 — Failed Transaction Rate %

**KPI Name:** Failed Transaction Rate %

**Business Definition:**  
The percentage of transactions that have a status of **Failed** within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Failed Transaction Rate % = (Failed Transactions / Total Transactions) × 100
```

**Example:**

If:

```text
Total Transactions  = 1,000
Failed Transactions = 50
```

Then:

```text
Failed Transaction Rate % = (50 / 1,000) × 100
                          = 5%
```

**SQL Example:**
```sql
SELECT
    COUNT(CASE
        WHEN transaction_status = 'Failed'
        THEN transaction_id
    END) * 100.0
    / NULLIF(COUNT(transaction_id), 0) AS Failed_Rate_Percent
FROM transactions;
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL calculated Failed Transaction Rate %
- API calculated Failed Transaction Rate %
- Dashboard Failed Transaction Rate % KPI

**Expected Result:**  
The calculated percentage should match across applicable layers, subject to the agreed rounding rule.

**NULL and Zero-Division Rule:**  
`NULLIF` should prevent a division-by-zero error when the selected reporting period contains zero transactions.

**Important Business Rule:**  
Only transactions with status `Failed` should be counted as failed transactions.

**QA Risk:**  
A mismatch may indicate incorrect status filtering, incorrect transaction counts, NULL handling issues, division-by-zero handling, rounding differences, or an incorrect dashboard calculation.
### KPI-008 — Completed Transaction Amount

**KPI Name:** Completed Transaction Amount

**Business Definition:**  
The total monetary value of transactions with a status of **Completed** within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text id="4p0d2k"
Completed Transaction Amount =
SUM(Transaction Amount)
WHERE Transaction Status = 'Completed'
```

**Example:**

If the transactions are:

| Transaction ID | Amount | Status |
|---|---:|---|
| T001 | $100 | Completed |
| T002 | $250 | Completed |
| T003 | $150 | Failed |
| T004 | $200 | Completed |

Then:

```text id="l1yp6d"
Completed Transaction Amount = $100 + $250 + $200
                             = $550
```

The `$150` Failed transaction is excluded.

**SQL Example:**
```sql id="p6qf5c"
SELECT
    SUM(CASE
        WHEN transaction_status = 'Completed'
        THEN transaction_amount
        ELSE 0
    END) AS Completed_Transaction_Amount
FROM transactions;
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL Completed Transaction Amount
- API Completed Transaction Amount
- Dashboard Completed Transaction Amount KPI
- Sum of Completed transaction amounts in the transaction table

**Expected Result:**  
All applicable layers should return the same completed transaction amount, subject to the agreed rounding and NULL-handling rules.

**NULL Handling Rule:**  
QA should verify how `NULL` transaction amounts are handled. A `NULL` amount should not automatically be interpreted as a valid `$0` transaction unless that is explicitly defined by the business requirement.

**Important Business Rule:**  
Only transactions with status `Completed` should contribute to this KPI.

**QA Risk:**  
A mismatch may indicate incorrect status filtering, missing or duplicate transactions, NULL amount handling, incorrect transaction amounts, date-filter issues, rounding differences, or an incorrect dashboard calculation.
### KPI-009 — Failed Transaction Amount

**KPI Name:** Failed Transaction Amount

**Business Definition:**  
The total monetary value of transactions with a status of **Failed** within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Failed Transaction Amount =
SUM(Transaction Amount)
WHERE Transaction Status = 'Failed'
```

**Example:**

| Transaction ID | Amount | Status |
|---|---:|---|
| T001 | $100 | Completed |
| T002 | $250 | Failed |
| T003 | $150 | Failed |
| T004 | $200 | Completed |

Then:

```text
Failed Transaction Amount = $250 + $150
                          = $400
```

**SQL Example:**
```sql
SELECT
    SUM(CASE
        WHEN transaction_status = 'Failed'
        THEN transaction_amount
        ELSE 0
    END) AS Failed_Transaction_Amount
FROM transactions;
```

**QA Validation Rule:**  
The following values should reconcile when the same reporting period and filters are applied:
- SQL Failed Transaction Amount
- API Failed Transaction Amount
- Dashboard Failed Transaction Amount KPI
- Sum of Failed transaction amounts in the transaction table

**Expected Result:**  
All applicable layers should return the same failed transaction amount, subject to the agreed rounding and NULL-handling rules.

**NULL Handling Rule:**  
QA should verify how `NULL` transaction amounts are handled. A `NULL` amount should not automatically be interpreted as `$0` unless this is explicitly defined by the business requirement.

**Important Business Rule:**  
Only transactions with status `Failed` should contribute to this KPI.

**QA Reconciliation Rule:**

When the reporting population contains only `Completed` and `Failed` transactions:

```text
Total Transaction Amount =
Completed Transaction Amount + Failed Transaction Amount
```

QA should validate this relationship using SQL and compare the result with the dashboard.

**QA Risk:**  
A mismatch may indicate incorrect status filtering, missing or duplicate transactions, NULL amount handling, incorrect transaction amounts, date-filter issues, rounding differences, or an incorrect dashboard calculation.
### KPI-010 — Transaction Amount by Status

**KPI Name:** Transaction Amount by Status

**Business Definition:**  
The total monetary value of transactions grouped by transaction status within the selected reporting period and applicable dashboard filters.

**Calculation:**
```text
Transaction Amount by Status = SUM(Transaction Amount)
GROUP BY Transaction Status
```

**SQL Example:**
```sql
SELECT
    transaction_status,
    SUM(transaction_amount) AS total_amount
FROM transactions
GROUP BY transaction_status;
```

**Example Result:**

| Transaction Status | Total Amount |
|---|---:|
| Completed | $75,000 |
| Failed | $5,000 |
| Pending | $2,500 |

**QA Validation Rule:**  
QA should compare the SQL results against:
- Dashboard chart values
- API response values
- Transaction table values

The status categories and their corresponding amounts should match across all applicable layers.

**Expected Result:**  
Each transaction status should display the correct total transaction amount.

**NULL Handling Rule:**  
QA should identify transactions where `transaction_status IS NULL` and verify that the dashboard handles them according to the defined business rule.

For example:

```sql
SELECT
    COALESCE(transaction_status, 'Unknown') AS transaction_status,
    SUM(transaction_amount) AS total_amount
FROM transactions
GROUP BY COALESCE(transaction_status, 'Unknown');
```

**QA Reconciliation Rule:**

The sum of all status-level transaction amounts should equal the overall transaction amount when all transaction statuses are included:

```text
Total Transaction Amount =
Sum of Transaction Amount by Status
```

**QA Risk:**  
A mismatch may indicate missing status categories, incorrect grouping, NULL handling issues, duplicate records, incorrect aggregation, filtering problems, or incorrect dashboard chart calculations.
