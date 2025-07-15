import sqlite3
import functools
from datetime import datetime

# Step 1: Create the decorator function
def log_queries(func):
    @functools.wraps(func)  # preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        # Step 2: Get the query from either args or kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]
        else:
            query = "UNKNOWN QUERY"

        # Step 3: Log the query before it's executed
        print(f"[LOG] Executing SQL Query: {query}")

        # Step 4: Call the original function and return its result
        return func(*args, **kwargs)
    
    return wrapper

# This function will be wrapped by our decorator
@log_queries
def fetch_all_users(query):
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Execute the provided SQL query
    cursor.execute(query)

    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()
    return results

# 
When this runs, it will also log the query before execution
users = fetch_all_users(query="SELECT * FROM users")
