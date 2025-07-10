import mysql.connector
from mysql.connector import Error

def stream_users():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YourPasswordHere',  # <-- replace with your actual MySQL root password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            for row in cursor:
                yield row  # ✅ Yield one row at a time

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while connecting to database: {e}")
