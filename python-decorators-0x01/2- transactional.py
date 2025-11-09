import sqlite3
import functools

# Decorator to provide a database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect("users.db")
        try:
            # Call the function and pass the connection
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Close the connection
            conn.close()
    return wrapper

# Decorator to manage transactions automatically
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no exceptions
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception
    return wrapper

# Example function using both decorators
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Updated user {user_id} email to {new_email}")

# Call the function
update_user_email(user_id=1, new_email='mike@gmail.com')
