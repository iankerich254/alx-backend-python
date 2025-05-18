#!/usr/bin/python3
"""
1-batch_processing.py

Defines generators to stream user data in batches and process each batch,
filtering users over the age of 25.
"""
import mysql.connector
from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """
    Generator that yields successive batches (lists) of rows from user_data.
    Each batch is a list of dicts (with keys user_id, name, email, age).
    """
    conn = connect_to_prodev()
    if not conn:
        return
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data;")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Processes each batch of users and prints only those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:
                print(user)

