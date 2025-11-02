

# Import the database connection from seed.py
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database using LIMIT and OFFSET.
    Args:
        page_size (int): number of rows per page.
        offset (int): starting point for the page.
    Returns:
        list: rows from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads user data in pages.
    Uses only one loop and yields one page at a time.
    Stops when no more rows exist.
    """
    offset = 0
    while True:  #  Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break   # Stop if no more rows returned
        yield page  # Yield one page at a time
        offset += page_size
