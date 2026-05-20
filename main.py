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



#function to list transactions

def list_transactions():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""SELECT t.id, t.date, t.description, t.amount, t.type, c.name FROM transactions AS t JOIN categories AS c ON t.category_id = c.id ORDER BY t.date """)

    rows = cursor.fetchall()


    print("ID | Date       | Description            | Amount   | Type    | Category")
    print("-" * 75)
    for row in rows:
        print(f"{row[0]:<2} | {row[1]:<10} | {row[2]:<22} | €{row[3]:<7.2f} | {row[4]:<7} | {row[5]}")

    connection.close()


# add transaction function
def add_transaction():

    category = 0
    transaction_type = ""

    print("\n1. Food \n2. Transport \n3. Salary \n4. Entertainment")

    choice = input("Select a category: \n")

    match choice:

        case "1":
            category = 1
            transaction_type = "expense"

        case "2":
            category = 2
            transaction_type = "expense"

        case "3":
            category = 3
            transaction_type = "income"

        case "4":
            category = 4
            transaction_type = "expense"

        case _:
            print("Invalid option.")
            return

    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO transactions (date, description, amount, type, category_id) VALUES (?, ?, ?, ?, ?)""", (date, description, amount, transaction_type, category))

    connection.commit()
    connection.close()

    print("Transaction added successfully. \n")
    

#summary function
def summary():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""SELECT SUM(amount) FROM transactions WHERE type = 'income'""")
    total_income = cursor.fetchone()[0]

    cursor.execute("""SELECT SUM(amount) FROM transactions WHERE type = 'expense'""")
    total_expenses = cursor.fetchone()[0]

    if total_income is None:
        total_income = 0

    if total_expenses is None:
        total_expenses = 0

    net_balance = total_income - total_expenses

    print(f"\n=== Summary === \nTotal Income:   €{total_income:.2f} \nTotal Expenses:   €{total_expenses:.2f} \nNet Balance:    €{net_balance:.2f}")

    connection.close()


#delete function
def delete_transaction():

    list_transactions()

    try:
        transaction_id = int(input("\nEnter transaction ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM transactions WHERE id = ?""", (transaction_id,))
    connection.commit()

    if cursor.rowcount == 0:
        print("Transaction not found. \n")

    else:
        print("Transaction deleted successfully. \n")

    connection.close()


#command line interface function

def run_cli():
    while True:

        print("\n=== Personal Finance Tracker === \n1. List Transactions \n2. Add Transaction \n3. Summary \n4. Delete Transaction \n5. Exit \n")


        choice = input("Choose an option: ")

        match choice:
           case "1":
                list_transactions()
           case "2":
                add_transaction()
           case "3":
                summary()
           case "4":
                delete_transaction()
           case "5":
                print("Bye Bye \n")
                break
           case _:
                print("Invalid option.")
            


#main - like using it due to c++

def main():
    create_tables()
    populate_data()
    run_cli()


if __name__ == "__main__":
    main()