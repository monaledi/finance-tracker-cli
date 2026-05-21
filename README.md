# Personal Finance Tracker CLI

A command-line personal finance tracker built with Python and SQLite.

Users can:
- Add transactions
- List transactions
- Delete transactions
- Filter transactions
- View financial summaries
- Generate monthly spending reports

---

## Technologies

- Python 3
- SQLite3
- Raw SQL

---

## Features

- Automatic SQLite database creation
- Seed/demo data on first run
- Modular project structure
- Input validation
- SQL filtering and reporting
- JOIN, GROUP BY, ORDER BY queries

---

## Project Structure

```text
finance-tracker-cli/
│
├── main.py
├── database.py
├── transactions.py
├── README.md
└── .gitignore
```

---

## Run the Project

```bash
python main.py
```

---

## Example CLI

```text
=== Personal Finance Tracker ===

1. List Transactions
2. Add Transaction
3. Summary
4. Delete Transaction
5. Filter Transactions
6. Monthly Report
7. Exit
```

---

## SQL Concepts Used

- CREATE TABLE
- INSERT INTO
- SELECT
- DELETE
- JOIN
- GROUP BY
- ORDER BY
- Aggregate functions
- Date filtering