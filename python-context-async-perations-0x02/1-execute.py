import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_path=":memory:"):
        self.query = query
        self.params = params or ()
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    db_path = "users.db"
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.executemany("INSERT INTO users (Name, age) VALUES (?, ?)", [
            ("Alpha", 30),
            ("Bravo", 22),
            ("Charlie", 28),
            ("Delta", 24)
        ])
        conn.commit()

    # Use the context manager to execute the query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params, db_path) as results:
        print(results)
