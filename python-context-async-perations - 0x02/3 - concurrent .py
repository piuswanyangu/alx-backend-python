# # Run multiple database queries concurrently using asyncio.gather.

# Instructions:

# Use the aiosqlite library to interact with SQLite asynchronously. To learn more about it, click here.

# Write two asynchronous functions: async_fetch_users() and async_fetch_older_users() that fetches all users and users older than 40 respectively.

# Use the asyncio.gather() to execute both queries concurrently.

# Use asyncio.run(fetch_concurrently()) to run the concurrent fetch

import asyncio
import aiosqlite

# --- Step 1: Setup database with sample data ---
async def setup_database():
    async with aiosqlite.connect("async_test.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER
            )
        """)
        await db.execute("DELETE FROM users")  # Clear old data
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 25),
            ("Bob", 45),
            ("Charlie", 35),
            ("Diana", 50),
            ("Evan", 42)
        ])
        await db.commit()


# --- Step 2: Async functions to fetch users ---
async def async_fetch_users():
    async with aiosqlite.connect("async_test.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("\nAll users:")
            for row in rows:
                print(row)
            return rows


async def async_fetch_older_users():
    async with aiosqlite.connect("async_test.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows


# --- Step 3: Run both queries concurrently ---
async def fetch_concurrently():
    # Run both async functions at the same time
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results


# --- Step 4: Run the whole program ---
if __name__ == "__main__":
    asyncio.run(setup_database())     # Set up sample DB first
    asyncio.run(fetch_concurrently()) # Run concurrent queries
