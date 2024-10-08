import mysql.connector as sql
from random import randint


def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection"""
    connection = None
    try:
        connection = sql.connect(
            host=host_name, user=user_name, password=user_password, database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


host = "localhost"
passwd = "1234"
db = "BankManagementSystem"
usr = "root"

connection = create_connection(host, usr, passwd, db)
cursor = connection.cursor()


def random_number():
    num = 0
    for i in range(5):
        num = num * 10 + randint(1, 9)
    return num


def create_account():
    name = input("Enter account holder's name: ")
    phone = input("Enter phone number: ")
    address = input("Enter address: ")
    initial_balance = float(input("Enter initial deposit (>=0): "))
    account_number = random_number()
    query = "INSERT INTO Account (name,account_number, phone_number, address, balance) VALUES (%s, %s, %s, %s, %s)"
    values = (name, account_number, phone, address, initial_balance)
    cursor.execute(query, values)
    connection.commit()
    print(f"Account created successfully! \nYour Account number is {account_number}")


def deposit_money():
    account_number = int(input("Enter account number: "))
    amount = float(input("Enter deposit amount: "))

    # Update balance
    query = "UPDATE Account SET balance = balance + %s WHERE account_number = %s"
    cursor.execute(query, (amount, account_number))

    # Log transaction
    query = "INSERT INTO Transaction (account_number, transaction_type, amount, transaction_date) VALUES (%s, 'Deposit', %s, NOW())"
    cursor.execute(query, (account_number, amount))
    connection.commit()
    print("Deposit successful!")


def withdraw_money():
    account_number = int(input("Enter account number: "))
    amount = float(input("Enter withdrawal amount: "))

    # Check current balance
    query = "SELECT balance FROM Account WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        # Update balance
        query = "UPDATE Account SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (amount, account_number))

        # Log transaction
        query = "INSERT INTO Transaction (account_number, transaction_type, amount, transaction_date) VALUES (%s, 'Withdraw', %s, NOW())"
        cursor.execute(query, (account_number, amount))
        connection.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient balance!")


def check_balance():
    account_number = int(input("Enter account number: "))
    query = "SELECT balance FROM account WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    balance = cursor.fetchone()[0]
    print(f"The balance is {balance}")


def transaction_history():
    account_number = int(input("Enter account number: "))
    query = "SELECT * from Transaction where account_number =%s ORDER BY transaction_date DESC"
    cursor.execute(query, (account_number,))
    transactions = cursor.fetchall()
    for transaction in transactions:
        print(transaction)


def close_account():
    account_number = int(input("Enter account number: "))
    # Delete transactions
    query = "DELETE FROM Transaction WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    # Delete account
    query = "DELETE FROM Account WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    connection.commit()
    print("Account closed successfully!")


# ------------Menu----------
def menu():
    while True:
        print("\nBank Account Management System")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. Close Account")
        print("7. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            create_account()
        elif choice == 2:
            deposit_money()
        elif choice == 3:
            withdraw_money()
        elif choice == 4:
            check_balance()
        elif choice == 5:
            transaction_history()
        elif choice == 6:
            close_account()
        elif choice == 7:
            break
        else:
            print("Invalid choice!")


menu()
