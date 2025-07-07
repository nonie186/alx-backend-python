import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, csv_file_path):
    cursor = connection.cursor()
    with open(csv_file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()

# ✅ Add this generator function
def stream_rows(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
