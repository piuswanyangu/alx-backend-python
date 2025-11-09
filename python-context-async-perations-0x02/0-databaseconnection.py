# create a class based context manager to handle 
# opening and closing database connections automatically

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """Initialize with the database name."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open the database connection."""
        print("Opening database connection...")
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # returned object is accessible as `conn` inside the with block

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection automatically, even if an error occurs."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
        # Return False to propagate exceptions (default behavior)
        return False


# --- USING THE CONTEXT MANAGER ---
if __name__ == "__main__":
    # Create a temporary test database
    with DatabaseConnection("test.db") as conn:
        cursor = conn.cursor()
        
        # Create a table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
        """)
        
        # Insert sample data (only if table is empty)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
                ("Alice", "alice@gmail.com"),
                ("Bob", "bob@gmail.com"),
                ("Charlie", "charlie@gmail.com")
            ])
            conn.commit()

    # Now use the context manager again to read data
    with DatabaseConnection("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        print("\nUsers in database:")
        for row in rows:
            print(row)
