import mysql.connector
import uuid
import csv

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

# 1. Connect to MySQL server (no database specified)
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # adjust if needed
            password=''   # adjust if needed
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create the ALX_prodev database if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Database {DB_NAME} created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    finally:
        cursor.close()

# 3. Connect to ALX_prodev database
def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # adjust if needed
            password='',  # adjust if needed
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 4. Create the user_data table if it does not exist
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = (
        f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ("
        "user_id CHAR(36) PRIMARY KEY, "
        "name VARCHAR(255) NOT NULL, "
        "email VARCHAR(255) NOT NULL, "
        "age DECIMAL(5,2) NOT NULL, "
        "INDEX idx_user_id (user_id)"
        ");"
    )
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table {TABLE_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        exit(1)
    finally:
        cursor.close()

# 5. Insert data from CSV if not exists
def insert_data(connection, csv_file_path):
    cursor = connection.cursor()
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uid = row.get('user_id') or str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            # Insert ignoring duplicates
            insert_query = (
                f"INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age) "
                f"VALUES (%s, %s, %s, %s);"
            )
            try:
                cursor.execute(insert_query, (uid, name, email, age))
            except mysql.connector.Error as err:
                print(f"Error inserting row {uid}: {err}")
        connection.commit()
    cursor.close()
    print(f"Data from {csv_file_path} inserted successfully.")

# 6. Generator to stream rows one by one
def stream_user_data(connection, batch_size=100):
    """
    Generator that yields rows from the user_data table in batches.
    Use MySQL server-side cursor to avoid loading all rows at once.
    """
    cursor = connection.cursor(buffered=False)
    cursor.execute(f"SELECT user_id, name, email, age FROM {TABLE_NAME};")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()

# Example usage of the generator
if __name__ == '__main__':
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, 'user_data.csv')

            print("Streaming rows one by one:")
            for record in stream_user_data(conn, batch_size=50):
                print(record)

            conn.close()

