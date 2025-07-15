import sqlite3
import functools

# Step 1: Define the decorator
def with_db_connection(func):
    @functools.wraps(func)  # preserves function name and docstring
    def wrapper(*args, **kwargs):
        # Step 2: Open the database connection
        conn = sqlite3.connect('users.db')

        try:
            # Step 3: Call the original function and pass in the connection
            return func(conn, *args, **kwargs)
        finally:
            # Step 4: Always close the connection afterward
            conn.close()
    return wrapper

# Step 5: Apply the decorator
@with_db_connection
def get_user_by_id(conn, user_id):
    # Step 6: Use the passed-in connection to execute a query
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Step 7: Call the decorated function without worrying about connection management
user = get_user_by_id(user_id=1)
print(user)
