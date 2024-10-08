import mysql.connector as sql
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection"""
    connection = None
    try:
        connection = sql.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_sql_file(connection, sql_file_path):
    """Read and execute SQL file"""
    cursor = connection.cursor()
    try:
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            sql_commands = sql_script.split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            connection.commit()
            print(f"Executed SQL file '{sql_file_path}' successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Connection parameters
host = "localhost"      # Replace with your MySQL host
user = "root"  # Replace with your MySQL username
password = "1234"  # Replace with your MySQL password
database = "BankManagementSystem"  # Replace with your MySQL database name

# Create a connection
connection = create_connection(host, user, password, database)

# Path to your SQL file
sql_file_path = './SQL commands.sql'

# Execute SQL file
if connection is not None and connection.is_connected():
    execute_sql_file(connection, sql_file_path)

    # Close the connection after execution
    connection.close()
    print("MySQL connection is closed")
