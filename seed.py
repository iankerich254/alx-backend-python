#!/usr/bin/python3
"""
Seed script for ALX_prodev database and user_data table.
"""
import mysql.connector
from mysql.connector import errorcode
import csv

def connect_db():
    """Connect to MySQL server (no specific database)."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # update with your MySQL root password
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev DEFAULT CHARACTER SET 'utf8' ")
        print("Database ALX_prodev created or exists already")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # update as needed
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    table_def = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "user_id VARCHAR(36) NOT NULL, "n"
        "name VARCHAR(255) NOT NULL, "
        "email VARCHAR(255) NOT NULL, "
        "age DECIMAL(5,2) NOT NULL, "
        "PRIMARY KEY (user_id), "
        "INDEX idx_user_id (user_id)"
        ") ENGINE=InnoDB"
    )
    try:
        cursor.execute(table_def)
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data (ignoring duplicates)."""
    cursor = connection.cursor()
    insert_stmt = (
        "INSERT IGNORE INTO user_data (user_id, name, email, age) "
        "VALUES (%s, %s, %s, %s)"
    )
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = (row['user_id'], row['name'], row['email'], row['age'])
            try:
                cursor.execute(insert_stmt, data)
            except mysql.connector.Error as err:
                print(f"Error inserting row {row}: {err}")
    connection.commit()
    print("Data inserted (duplicates ignored)")
    cursor.close()

