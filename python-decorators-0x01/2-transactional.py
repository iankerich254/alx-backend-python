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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
