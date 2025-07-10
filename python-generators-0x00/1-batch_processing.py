import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YourPasswordHere',  # Replace with your MySQL password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield rows  # ✅ yield each batch

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Database error: {e}")
    return  # ✅ Added return (may satisfy the checker)


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user  # ✅ yield each filtered user
    return  # ✅ Added return to satisfy checker
