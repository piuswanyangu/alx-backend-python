import sqlite3
import functools

#  Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query provided.")

        # Execute the original function
        result = func(*args, **kwargs)
        print("[LOG] Query execution completed.\n")
        return result
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#  Example usage
users = fetch_all_users(query="SELECT * FROM users")
