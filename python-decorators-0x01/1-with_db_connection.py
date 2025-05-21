from datetime import datetime
import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper_db_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            starttime = datetime.now()
            result = func(conn, *args, **kwargs)
            endtime = datetime.now()
            duration = (endtime - starttime).total_seconds()
            print(f"Query executed in {duration:.6f} seconds")
        finally:
            conn.close()
        return result
    return wrapper_db_connection

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
