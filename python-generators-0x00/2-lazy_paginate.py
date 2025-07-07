import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users starting from the given offset.
    
    Returns:
        list of dicts: Each dict represents a user row.
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
        cursor.execute(
            "SELECT id, name, age FROM users LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def lazy_paginate(page_size):
    """
    Generator to lazily fetch users page by page.
    
    Yields:
        list[dict]: Next page of users
    """
    offset = 0
    while True:  # ← Only loop used
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# --- Example usage ---
if __name__ == "__main__":
    for page in lazy_paginate(page_size=100):
        print(f"Fetched {len(page)} users.")

