# create a reusable context manager that takes a query as input and executes it, 
# managing both connection and the query execution

# Instructions:

# Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

# Ensure to use the__enter__() and the __exit__() methods

import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """Initialize with database name, query, and optional parameters."""
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.result = None

    def __enter__(self):
        """Open connection, execute the query, and return results."""
        print("Opening database connection...")
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()

        try:
            print(f"Executing query: {self.query}")
            cursor.execute(self.query, self.params)
            self.result = cursor.fetchall()
            return self.result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            self.result = None
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection when leaving the context."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        # Return False to allow exceptions (if any) to propagate
        return False


# ---  setup and usage ---
if __name__ == "__main__":
    # Create test database and insert data
    with sqlite3.connect("test1.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
                ("Alice", 22),
                ("Bob", 30),
                ("Charlie", 28),
                ("Diana", 19)
            ])
            conn.commit()

    # --- Use our reusable context manager ---
    with ExecuteQuery("test1.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
        print("\nUsers older than 25:")
        for row in results:
            print(row)
