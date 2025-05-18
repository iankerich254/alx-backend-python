#!/usr/bin/python3
"""
4-stream_ages.py

Implements a generator to stream user ages and computes the average age
without loading all records into memory.
"""
import seed


def stream_user_ages():
    """
    Generator that yields each user's age from the user_data table one by one.
    """
    conn = seed.connect_to_prodev()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data;")
    for (age,) in cursor:
        yield age
    cursor.close()
    conn.close()


def compute_average_age():
    """
    Calculates and prints the average age of users using the stream_user_ages generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age)
        count += 1
    if count > 0:
        average = total / count
        print(f"Average age of users: {average}")
    else:
        print("Average age of users: 0")


if __name__ == '__main__':
    compute_average_age()
