import sqlite3
import random

DB_NAME = "finance_tracker.db"



# database connection

def connect_db():
    connection = sqlite3.connect(DB_NAME)
    return connection



# setup for database 
def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   date TEXT NOT NULL, description TEXT, 
                   amount REAL NOT NULL, type TEXT NOT NULL, 
                   category_id INTEGER, 
                   FOREIGN KEY (category_id) 
                   REFERENCES categories(id) ) """)

    connection.commit()
    connection.close()


# function to stop repeating code in populate function match case
def generate_transaction_data(category, min, max, transaction_type):

    description = random.choice(category)

    amount = round(random.uniform(min, max), 2)

    return description, amount, transaction_type


#populating data is the database is empty

def populate_data():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    if category_count == 0:
        cursor.executemany("""
            INSERT INTO categories (name)
            VALUES (?)
        """, [
            ("Food",),
            ("Transport",),
            ("Salary",),
            ("Entertainment",)
        ])

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]

    if transaction_count == 0:

        food_transactions = [
            "Groceries",
            "Coffee",
            "Lunch",
            "Dinner",
            "Snacks"
        ]

        transport_transactions = [
            "Bus Ticket",
            "Train Ticket",
            "Uber",
            "Fuel",
            "Parking"
        ]

        salary_transactions = [
            "Salary",
            "Freelance Work",
            "Bonus",
            "Side Hustle"
        ]

        entertainment_transactions = [
            "Cinema",
            "Concert",
            "Netflix",
            "Gaming",
            "Bowling"
        ]

        transactions = []

        for _ in range(25):
            category = random.randint(1, 4)

            match category:
                case 1:
                    description, amount, transaction_type = generate_transaction_data(food_transactions, 5, 50, "expense")

                case 2:
                    description, amount, transaction_type = generate_transaction_data(transport_transactions, 3, 100, "expense")

                case 3:
                    description, amount, transaction_type = generate_transaction_data(salary_transactions, 500, 5000, "income")
            
                case 4:
                    description, amount, transaction_type = generate_transaction_data(entertainment_transactions, 10, 200, "expense")

            day = random.randint(1, 28)
            date = f"2026-05-{day:02d}"

            transactions.append(
                (date, description, amount, transaction_type, category)
            )

        cursor.executemany("""
            INSERT INTO transactions
            (date, description, amount, type, category_id)
            VALUES (?, ?, ?, ?, ?)""", transactions)

    connection.commit()
    connection.close()