
import mysql.connector

def stream_users():
    #  Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123", 
        database="Alx_prodev"
    )

    cursor = conn.cursor()

    # 2️Execute the query
    cursor.execute("SELECT * FROM user_data")

    # 3️ Use a generator to yield rows one by one
    for row in cursor:
        yield row   # generator returns one row at a time

    # 4️ Clean up
    cursor.close()
    conn.close()
