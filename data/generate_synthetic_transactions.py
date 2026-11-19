
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
def validate_transaction_amount(amount):
    if amount is None:
        return False

    if amount <= 0:
        return False

    return True

print("\n--- Transaction Amount Function Test ---")

print(validate_transaction_amount(Decimal("100.00")))
print(validate_transaction_amount(Decimal("0.00")))
print(validate_transaction_amount(Decimal("-25.00")))
print(validate_transaction_amount(None))

def round_currency(amount):
    return amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

transactions = [
    {
        "transaction_id": 1001,
        "account_id": "ACC001",
        "transaction_date": "2026-11-01",
        "transaction_type": "Deposit",
        "original_amount": Decimal("100.005"),
        "status": "Completed"
    },
    {
        "transaction_id": 1002,
        "account_id": "ACC001",
        "transaction_date": "2026-11-02",
        "transaction_type": "Withdrawal",
        "original_amount": Decimal("25.555"),
        "status": "Completed"
    },
    {
        "transaction_id": 1003,
        "account_id": "ACC002",
        "transaction_date": "2026-11-03",
        "transaction_type": "Deposit",
        "original_amount" : Decimal("200.00"),
        "status": "Pending"
    },
    {
        "transaction_id": 1004,
        "account_id": "ACC002",
        "transaction_date": "2026-11-04",
        "transaction_type": "Withdrawal",
        "original_amount": Decimal("50.00"),
        "status": "Failed"
    }
]

# Validate all transaction amounts using reusable function
print("\n--- SmartBank Transaction Amount Validation ---")

for transaction in transactions:
    is_valid = validate_transaction_amount(
        transaction["original_amount"]
    )

    result = "PASS" if is_valid else "FAIL"

    print(
        f"Transaction {transaction['transaction_id']}: {result}"
    )
    
    if transaction["original_amount"] is None:
        transaction["transaction_amount"] = None
    else:
        transaction["transaction_amount"] = round_currency(
            transaction["original_amount"]
        )

df = pd.DataFrame(transactions)

print(df)
# Filter completed transactions
completed_df = df[df["status"] == "Completed"]

# Calculate deposits
deposits = sum(
    completed_df.loc[
        completed_df["transaction_type"] == "Deposit",
        "transaction_amount"
    ],
    Decimal("0.00")
)

# Calculate withdrawals
withdrawals = sum(
    completed_df.loc[
        completed_df["transaction_type"] == "Withdrawal",
        "transaction_amount"
    ],
    Decimal("0.00")
)

# Calculate net amount
net_amount = deposits - withdrawals

print("\n--- SmartBank Financial KPIs ---")
print("Total Deposits:", deposits)
print("Total Withdrawals:", withdrawals)
print("Net Amount:", net_amount)


import sqlite3

# Create SmartBank SQLite database
conn = sqlite3.connect("data/smartbank.db")
cursor = conn.cursor()

# Create transaction table
cursor.execute("DROP TABLE IF EXISTS transactions")

cursor.execute("""
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id TEXT,
    transaction_date TEXT,
    transaction_type TEXT,
    original_amount TEXT,
    transaction_amount_cents INTEGER,
    status TEXT
)
""")

# Insert transaction records
records = []

for transaction in transactions:

    if transaction["transaction_amount"] is None:
        print(
            f"REJECTED: Transaction "
            f"{transaction['transaction_id']} has no amount"
        )
        continue

    posted_cents = int(
        transaction["transaction_amount"] * 100
    )

    records.append((
        transaction["transaction_id"],
        transaction["account_id"],
        transaction["transaction_date"],
        transaction["transaction_type"],
        str(transaction["original_amount"]),
        posted_cents,
        transaction["status"]
    ))

cursor.executemany("""
INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?)
""", records)

conn.commit()
# Negative Test: Duplicate Transaction Insertion

print("\n--- Duplicate Transaction Test ---")

try:
    cursor.execute("""
        INSERT INTO transactions VALUES (
            1001,
            'ACC001',
            '2026-11-05',
            'Deposit',
            '100.00',
            10000,
            'Completed'
        )
    """)
    conn.commit()
    print("FAIL: Duplicate transaction was accepted")

except sqlite3.IntegrityError:
    conn.rollback()
    print("PASS: Duplicate transaction was rejected")

# SQL KPI validation
query = """
SELECT
    transaction_type,
    SUM(transaction_amount_cents) AS total_cents
FROM transactions
WHERE status = 'Completed'
GROUP BY transaction_type
"""

results = cursor.execute(query).fetchall()

print("\n--- SQL BI Validation ---")

for transaction_type, total_cents in results:
    amount = Decimal(total_cents) / Decimal("100")
    print(transaction_type, amount)
    
# Test: Pending to Completed status transition

cursor.execute("""
UPDATE transactions
SET status = 'Completed'
WHERE transaction_id = 1003
""")

conn.commit()

print("\nTransaction 1003 status updated to Completed")


# Step 1: Capture account balance BEFORE duplicate attempt

balance_before = cursor.execute("""
SELECT
    SUM(CASE
        WHEN transaction_type = 'Deposit'
            THEN transaction_amount_cents
        WHEN transaction_type = 'Withdrawal'
            THEN -transaction_amount_cents
        ELSE 0
    END)
FROM transactions
WHERE account_id = 'ACC001'
AND status = 'Completed'
""").fetchone()[0]

# Step 2: Attempt to insert a duplicate transaction

print("\n--- Duplicate Transaction Test ---")

try:
    cursor.execute("""
        INSERT INTO transactions VALUES (
            1001,
            'ACC001',
            '2026-11-05',
            'Deposit',
            '100.00',
            10000,
            'Completed'
        )
    """)
    conn.commit()
    print("FAIL: Duplicate transaction was accepted")

except sqlite3.IntegrityError:
    conn.rollback()
    print("PASS: Duplicate transaction was rejected")


# Step 3: Capture account balance AFTER duplicate attempt

balance_after = cursor.execute("""
SELECT
    SUM(CASE
        WHEN transaction_type = 'Deposit'
            THEN transaction_amount_cents
        WHEN transaction_type = 'Withdrawal'
            THEN -transaction_amount_cents
        ELSE 0
    END)
FROM transactions
WHERE account_id = 'ACC001'
AND status = 'Completed'
""").fetchone()[0]

print(
    "Balance after rejected transaction:",
    Decimal(balance_after) / Decimal("100")
)


# Step 4: Verify balance was not changed

print("\n--- Transaction Integrity Test ---")

# Verify failed transaction is excluded from account balance

failed_transaction = cursor.execute("""
SELECT transaction_amount_cents
FROM transactions
WHERE transaction_id = 1004
AND status = 'Failed'
""").fetchone()

print("\n--- Failed Transaction Validation ---")
# Verify failed withdrawal does not reduce posted balance

acc002_balance = cursor.execute("""
SELECT SUM(
    CASE
        WHEN transaction_type = 'Deposit'
            THEN transaction_amount_cents
        WHEN transaction_type = 'Withdrawal'
            THEN -transaction_amount_cents
        ELSE 0
    END
)
FROM transactions
WHERE account_id = 'ACC002'
AND status = 'Completed'
""").fetchone()[0]

print("\n--- Failed Withdrawal Balance Test ---")

if acc002_balance == 20000:
    print("PASS: ACC002 balance remains $200.00")
else:
    print("FAIL: Unexpected ACC002 balance:", acc002_balance)
if failed_transaction:
    print("PASS: Transaction 1004 is marked Failed")
    print("PASS: Failed transaction is excluded from posted balance")
else:
    print("FAIL: Failed transaction validation")

if balance_before == balance_after:
    print("PASS: Rejected transaction did not change account balance")
else:
    print("FAIL: Account balance changed after rejected transaction")

balance_before = cursor.execute("""
SELECT
    SUM(CASE
        WHEN transaction_type = 'Deposit'
        THEN transaction_amount_cents
        WHEN transaction_type = 'Withdrawal'
        THEN -transaction_amount_cents
        ELSE 0
    END)
FROM transactions
WHERE account_id = 'ACC001'
AND status = 'Completed'
""").fetchone()[0]

updated_records = cursor.execute("""
SELECT
    transaction_type,
    transaction_amount_cents,
    status
FROM transactions
""").fetchall()

updated_df = pd.DataFrame(
    updated_records,
    columns=[
        "transaction_type",
        "transaction_amount_cents",
        "status"
    ]
)

# Calculate Python KPIs using updated data

completed_df = updated_df[
    updated_df["status"] == "Completed"
]

deposits = sum(
    (
        Decimal(amount) / Decimal("100")
        for amount in completed_df.loc[
            completed_df["transaction_type"] == "Deposit",
            "transaction_amount_cents"
        ]
    ),
    Decimal("0.00")
)

withdrawals = sum(
    (
        Decimal(amount) / Decimal("100")
        for amount in completed_df.loc[
            completed_df["transaction_type"] == "Withdrawal",
            "transaction_amount_cents"
        ]
    ),
    Decimal("0.00")
)

net_amount = deposits - withdrawals

print("\n--- Updated Python Financial KPIs ---")
print("Deposits:", deposits)
print("Withdrawals:", withdrawals)
print("Net Amount:", net_amount)

# Calculate all financial KPIs directly in SQL
kpi_query = """
SELECT
    SUM(CASE WHEN transaction_type = 'Deposit'
        THEN transaction_amount_cents ELSE 0 END) AS deposits,
    SUM(CASE WHEN transaction_type = 'Withdrawal'
        THEN transaction_amount_cents ELSE 0 END) AS withdrawals
FROM transactions
WHERE status = 'Completed'
"""

sql_deposits, sql_withdrawals = cursor.execute(
    kpi_query
).fetchone()

sql_deposits = Decimal(sql_deposits) / Decimal("100")
sql_withdrawals = Decimal(sql_withdrawals) / Decimal("100")

sql_net = sql_deposits - sql_withdrawals

print("\n--- SQL Financial KPIs ---")
print("Deposits:", sql_deposits)
print("Withdrawals:", sql_withdrawals)
print("Net Amount:", sql_net)


# Automated Python vs SQL reconciliation

reconciliation_checks = [
    ("Deposits", deposits, sql_deposits),
    ("Withdrawals", withdrawals, sql_withdrawals),
    ("Net Amount", net_amount, sql_net)
]

print("\n--- Reconciliation Report ---")

all_passed = True

for kpi, python_value, sql_value in reconciliation_checks:

    status = "PASS" if python_value == sql_value else "FAIL"

    print(
        f"{kpi}: Python={python_value}, "
        f"SQL={sql_value}, Result={status}"
    )

    if status == "FAIL":
        all_passed = False

print(
    "\nOverall Result:",
    "PASSED" if all_passed else "FAILED"
)


# Data Quality Check: Duplicate Transaction IDs

transaction_ids = [
    transaction["transaction_id"]
    for transaction in transactions
]

duplicate_ids = [
    transaction_id
    for transaction_id in set(transaction_ids)
    if transaction_ids.count(transaction_id) > 1
]

if duplicate_ids:
    print("Duplicate Transaction ID Check: FAIL")
    print("Duplicate IDs:", duplicate_ids)
else:
    print("Duplicate Transaction ID Check: PASS")

# Data Quality Check: Missing Transaction Amounts

missing_amounts = [
    transaction["transaction_id"]
    for transaction in transactions
    if transaction["original_amount"] is None
]

if missing_amounts:
    print("Missing Amount Check: FAIL")
    print("Transactions with missing amounts:", missing_amounts)
else:
    print("Missing Amount Check: PASS")

# Data Quality Check: Invalid Transaction Status

valid_statuses = {"Completed", "Pending", "Failed"}

invalid_statuses = [
    transaction["transaction_id"]
    for transaction in transactions
    if transaction["status"] not in valid_statuses
]

if invalid_statuses:
    print("Transaction Status Check: FAIL")
    print("Invalid status in transactions:", invalid_statuses)
else:
    print("Transaction Status Check: PASS")
    # Data Quality Check: Negative Transaction Amounts

negative_amounts = [
    transaction["transaction_id"]
    for transaction in transactions
    if transaction["original_amount"] is not None
    and transaction["original_amount"] < 0
]

if negative_amounts:
    print("Negative Amount Check: FAIL")
    print("Transactions with negative amounts:", negative_amounts)
else:
    print("Negative Amount Check: PASS")
 # Data Quality Check: Zero Transaction Amounts

zero_amounts = [
    transaction["transaction_id"]
    for transaction in transactions
    if transaction["original_amount"] == Decimal("0.00")
]

if zero_amounts:
    print("Zero Amount Check: FAIL")
    print("Transactions with zero amounts:", zero_amounts)
else:
    print("Zero Amount Check: PASS")
         
conn.close()
