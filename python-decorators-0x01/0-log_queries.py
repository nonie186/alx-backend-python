import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else '')
        print(f"Executing SQL Query: {query}")  # 👈 This logs the query
        return func(*args, **kwargs)
    return wrapper

# Function using the decorator
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')  # connects to the database
    cursor = conn.cursor()
    cursor.execute(query)               # executes the SQL query
    results = cursor.fetchall()        # fetches all the results
    conn.close()                       # closes the connection
    return results

# Call the function and see query logs
users = fetch_all_users(query="SELECT * FROM users")
print(users)  # display the result

