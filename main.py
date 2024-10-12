from random import randint
import mysql.connector as sql


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
    while not name.strip():
        name = input("Name cannot be empty. Please enter your name: ")
    phone = input("Enter phone number: ")
    while not phone.strip():
        phone = input("Phone number cannot be empty. Please enter your phone number: ")
    address = input("Enter address: ")
    while not address.strip():
        address = input("Address cannot be empty. Please enter your address: ")
    initial_balance = float(input("Enter initial deposit (>=0): "))
    while not initial_balance:
        initial_balance = input(
            "Initial deposit cannot be empty. Please enter your initial deposit: "
        )
    account_number = random_number()
    query = "INSERT INTO Account (name,account_number, phone_number, address, balance) VALUES (%s, %s, %s, %s, %s)"
    values = (name, account_number, phone, address, initial_balance)
    cursor.execute(query, values)
    connection.commit()
    print(f"Account created successfully! \nYour Account number is {account_number}")


def deposit_money():
    account_number = int(input("Enter account number: "))
    amount = float(input("Enter deposit amount: "))
    query = "UPDATE Account SET balance = balance + %s WHERE account_number = %s"  # Update balance
    cursor.execute(query, (amount, account_number))
    query = "INSERT INTO Transaction (account_number, transaction_type, amount, transaction_date) VALUES (%s, 'Deposit', %s, NOW())"  # Log transaction
    cursor.execute(query, (account_number, amount))
    connection.commit()
    print("Deposit successful!")


def withdraw_money():
    account_number = int(input("Enter account number: "))
    amount = float(input("Enter withdrawal amount: "))
    query = (
        "SELECT balance FROM Account WHERE account_number = %s"  # Check current balance
    )
    cursor.execute(query, (account_number,))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        # Update balance
        query = "UPDATE Account SET balance = balance - %s WHERE account_number = %s"
        cursor.execute(query, (amount, account_number))
        query = "INSERT INTO Transaction (account_number, transaction_type, amount, transaction_date) VALUES (%s, 'Withdraw', %s, NOW())"  # Log transaction
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


def transfer_money():
    senders_address = int(input("Enter the account number of sender: "))
    recievers_address = int(input("Enter the account number of reciever: "))
    amount_to_transfer = int(input("Enter the money to be transfered: "))
    query = "select balance from account where account_number=%s"
    cursor.execute(query, (senders_address,))
    balance = cursor.fetchone()[0]
    if balance >= amount_to_transfer:
        query = "update account set balance = balance - %s where account_number=%s"
        cursor.execute(query, (amount_to_transfer, senders_address))
        query = "insert into transfer (account_number, transaction_type, amount, transaction_date) values (%s,'Withdraw',%s,now())"
        cursor.execute(query, (senders_address, amount_to_transfer))
        query = "update account set balance = balance + %s where account_number=%s"
        cursor.execute(query, (amount_to_transfer, recievers_address))
        query = "insert into transfer (account_number, transaction_type, amount, transaction_date) values (%s,'Deposit',%s,now())"
        cursor.execute(query, (recievers_address, amount_to_transfer))
        connection.commit()
        print("Transfer successful")


def close_account():
    account_number = int(input("Enter account number: "))
    query = "DELETE FROM Transaction WHERE account_number = %s"  # Delete transactions
    cursor.execute(query, (account_number,))
    query = "DELETE FROM Account WHERE account_number = %s"  # Delete account
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
            print("Thank you visit again")
            break
        else:
            print("Invalid choice!")


try:
    menu()
except (KeyboardInterrupt, ValueError) as e:
    print(e)
