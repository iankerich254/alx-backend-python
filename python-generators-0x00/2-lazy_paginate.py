#!/usr/bin/python3
"""
2-lazy_paginate.py

Implements lazy pagination for the user_data table using a generator.
Provides both paginate_users and lazy_paginate functions.
"""
import seed


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.

    Args:
        page_size (int): Number of records per page.
        offset (int): Number of records to skip.

    Returns:
        list[dict]: List of user records as dicts.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT user_id, name, email, age FROM user_data "
        f"LIMIT {page_size} OFFSET {offset}"  
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily fetches and yields pages of users.

    Uses a single loop to request the next page only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

