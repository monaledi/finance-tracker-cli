import sqlite3

DB_NAME = "finance_tracker.db"



# database connection

def connect_db():
    connection = sqlite3.connect(DB_NAME)
    return connection



# setup for database  - Aware sql is in bad format but easier for me to read it like this :)

def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, description TEXT, amount REAL NOT NULL, type TEXT NOT NULL, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories(id) ) """)

    connection.commit()
    connection.close()


#populating data is the database is empty

def populate_data():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    if category_count == 0:
        cursor.executemany("""INSERT INTO categories (name) VALUES (?) """, 
        [
            ("Food",),
            ("Transport",),
            ("Salary",),
            ("Entertainment",)
        ])

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]

    if transaction_count == 0:
        cursor.executemany("""
            INSERT INTO transactions (date, description, amount, type, category_id) VALUES (?, ?, ?, ?, ?)""", 
            [
                ("2026-05-01", "Salary", 2500.00, "income", 3),
                ("2026-05-02", "Groceries", 45.50, "expense", 1),
                ("2026-05-03", "Bus ticket", 3.20, "expense", 2),
                ("2026-05-04", "Cinema", 14.00, "expense", 4),
                ("2026-05-05", "Freelance work", 300.00, "income", 3),
                ("2026-05-06", "Lunch", 12.50, "expense", 1),
                ("2026-05-07", "Train ticket", 29.90, "expense", 2),
                ("2026-05-08", "Concert", 35.00, "expense", 4),
                ("2026-05-09", "Coffee", 4.20, "expense", 1),
                ("2026-05-10", "Monthly transport pass", 49.00, "expense", 2)
            ])

    connection.commit()
    connection.close()
