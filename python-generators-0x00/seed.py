import mysql.connector
import csv
import uuid

# STEP 2 DEFINE MY FUNCTION
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='pius',
        password='Pius@123'
    )

# create the database if it does not exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database created .")

# step 3 connect to the specific database
def connect_to_prodev():
    return mysql.connector.connect(
        host='localhost',
        user='pius',
        password='Pius@123',
        database='ALX_prodev'
    )

# step 4 creating table if it does not exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(3,0) NOT NULL
        )
    """)
    print("Table created .")

# step 5 insert data / populate
def insert_data(connection, data):
    cursor = connection.cursor()
    query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, data)
    connection.commit()

# step 6 populate the database (read from csv and insert)
def populate_from_csv(connection, csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            insert_data(connection, (user_id, name, email, age))
    print("Data successfully populated from CSV!")

# last step put it all together
if __name__ == "__main__":
    # step1 : connect to mysql server
    conn = connect_db()
    create_database(conn)
    conn.close()

    # step 2 connect to the database
    prodev_conn = connect_to_prodev()

    # step 3 create table
    create_table(prodev_conn)

    # step 4 populate / fill the data from csv
    populate_from_csv(prodev_conn, 'user_data.csv')

    prodev_conn.close()
    print("All done!")
