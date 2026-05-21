import sqlite3

from database import connect_db, create_tables, populate_data
from datetime import datetime

#function to list transactions

def list_transactions():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""SELECT t.id, t.date, t.description, t.amount, t.type, c.name 
                   FROM transactions AS t 
                   JOIN categories AS c 
                   ON t.category_id = c.id 
                   ORDER BY t.date """)

    rows = cursor.fetchall()


    display_transactions(rows)

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

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO transactions (date, description, amount, type, category_id) 
                   VALUES (?, ?, ?, ?, ?)""", (date, description, amount, transaction_type, category))

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


def execute_filter(column_name, filter_type):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(f"""SELECT t.id, t.date, t.description, t.amount, t.type, c.name 
                           FROM transactions AS t 
                           JOIN categories AS c ON t.category_id = c.id 
                           WHERE {column_name} = ? ORDER BY t.date""", (filter_type,))

    rows = cursor.fetchall()
    connection.close()

    display_transactions(rows)
    


#function for filter transactions
def filter_transactions():

    print("Filter Transactions \n1. Filter by type \n2. Filter by category \n")

    choice = input("Choose filter option: ")

    match choice:

        case "1":
            transaction_type = input("Enter type (income/expense): ")

            execute_filter("t.type" ,transaction_type)

        case "2":
            print("\n1. Food \n2. Transport \n3. Salary \n4. Entertainment \n")
            category_id = input("Enter category ID: ")

            connection = connect_db()
            cursor = connection.cursor()

            
            execute_filter("t.category_id" ,category_id)

            rows = cursor.fetchall()
            connection.close()

            display_transactions(rows)

        case _:
            print("Invalid filter option. \n")


#function that displays transactions to save time instead of repeating
def display_transactions(rows):

    if len(rows) == 0:
        print("No transactions found.")
        return

    print("ID | Date       | Description            | Amount   | Type    | Category")
    print("-" * 75)

    for row in rows:
        print(f"{row[0]:<2} | {row[1]:<10} | {row[2]:<22} | €{row[3]:<7.2f} | {row[4]:<7} | {row[5]}")


#function that shows monthy report
def monthly_report():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""SELECT c.name, SUM(t.amount) AS total_spent 
                   FROM transactions AS t 
                   JOIN categories AS c ON t.category_id = c.id 
                   WHERE t.type = 'expense' AND strftime('%Y-%m', t.date) = strftime('%Y-%m', 'now') 
                   GROUP BY c.name 
                   ORDER BY total_spent DESC""")

    rows = cursor.fetchall()
    connection.close()

    if len(rows) == 0:
        print("No expenses found for the current month.\n")
        return

    print("Monthly Spending Report\nCategory        | Total Spent")
    print("-" * 35)

    for row in rows:
        print(f"{row[0]:<15} | €{row[1]:.2f}")