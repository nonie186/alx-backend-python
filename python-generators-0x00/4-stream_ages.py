import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="YOUR_USER",
        password="YOUR_PASSWORD",
        database="YOUR_DB",
        cursorclass=mysql.connector.cursor.DictCursor
    )
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM users")
        for row in cursor:  # ← 1st (and only) loop
            yield row['age']
    finally:
        conn.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute average age.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # ← 2nd loop
        total += age
        count += 1
    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")


# --- Run script ---
if __name__ == "__main__":
    calculate_average_age()
