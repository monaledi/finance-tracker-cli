
from database import create_tables, populate_data
from transactions import list_transactions, add_transaction, summary, delete_transaction, filter_transactions, monthly_report



#command line interface function

def run_cli():
    while True:

        print("\n=== Personal Finance Tracker === \n1. List Transactions \n2. Add Transaction \n3. Summary \n4. Delete Transaction \n5. Filter Transactions \n6. Monthly Report \n7. Exit \n")


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
                filter_transactions()
           case "6":
                monthly_report()
           case "7":
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