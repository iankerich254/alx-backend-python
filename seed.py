import mysql.connector
import csv
import uuid

# Prototypes
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",  # replace with your MySQL username
        password="your_password"  # replace with your MySQL password
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",  # replace with your MySQL username
        password="your_password",  # replace with your MySQL password
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        # Check if user already exists
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, name, email, age)
            )
    connection.commit()
    cursor.close()

def read_csv(file_path):
    with open(file_path, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            yield row

# Main
if __name__ == "__main__":
    try:
        print("Connecting to MySQL...")
        conn = connect_db()
        create_database(conn)
        conn.close()

        print("Connecting to ALX_prodev...")
        conn_prodev = connect_to_prodev()
        create_table(conn_prodev)

        print("Inserting data from CSV...")
        data_generator = read_csv("user_data.csv")
        insert_data(conn_prodev, data_generator)

        print("Done.")
        conn_prodev.close()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

