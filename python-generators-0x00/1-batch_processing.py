

import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to fetch rows from users table in batches."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",  
        database="Alx_prodev"          
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    
    batch = []
    # Loop through each row, collecting them into batches
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch   # yield a batch when it reaches the batch size
            batch = []    # reset the batch list

    # Yield any remaining rows if total rows < batch_size
    if batch:
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """Processes each batch to filter users older than 25."""
    # Loop through batches
    for batch in stream_users_in_batches(batch_size):
        # Filter users older than 25
        filtered_users = [user for user in batch if user['age'] > 25]
        yield filtered_users


# Example test
if __name__ == "__main__":
    for filtered_batch in batch_processing(5):
        print("Filtered batch:")
        for user in filtered_batch:
            print(user)
