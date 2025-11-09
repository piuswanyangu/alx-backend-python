import sqlite3
import functools

# Dictionary to store cached query results
query_cache = {}

# Decorator to provide a database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Returning cached result...")
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print("Query executed and result cached.")
        return result
    return wrapper

# Function that fetches users
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# --- Usage ---
users = fetch_users_with_cache(query="SELECT * FROM users")  # Executes query & caches
users_again = fetch_users_with_cache(query="SELECT * FROM users")  # Returns cached result

print(users)
print(users_again)
