
seed = __import__('seed')


def stream_user_ages():
    """
    Generator function to yield user ages one by one from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    #  Loop #1: yield ages one at a time
    for row in cursor:
        yield row['age']

    connection.close()


def calculate_average_age():
    """
    Uses the generator to compute the average age
    without loading all data into memory.
    """
    total_age = 0
    count = 0

    #  Loop #2: iterate over the generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Avoid division by zero
    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()
