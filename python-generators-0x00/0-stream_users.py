#!/usr/bin/python3
"""
0-stream_users.py

Defines a generator function to stream user data rows one by one from the MySQL user_data table.
"""
import mysql.connector
from seed import connect_to_prodev


def stream_users():
    """
    Generator that yields each user row as a dict from the user_data table.
    Uses a dictionary cursor and a single loop over the result set.
    """
    # Connect to the ALX_prodev database
    conn = connect_to_prodev()
    if not conn:
        return
    # Create a cursor that returns rows as dictionaries
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    # Single loop to yield rows one by one
    for row in cursor:
        yield row
    # Clean up
    cursor.close()
    conn.close()

