import mysql.connector
from mysql.connector import Error

# ✅ Helper function to fetch a single page of users
def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='YourPasswordHere',  # Replace with your password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
            cursor.execute(query, (page_size, offset))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows

    except Error as e:
        print(f"Database error: {e}")
        return []

# ✅ Generator that yields one page at a time lazily
def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ Yield a page of users
        offset += page_size

# Testing
#!/usr/bin/python3
from itertools import islice
lazy_paginate = __import__('2-lazy_paginate').lazy_paginate

# Print first 2 pages of 3 users each
for page in islice(lazy_paginate(3), 2):
    for user in page:
        print(user)
