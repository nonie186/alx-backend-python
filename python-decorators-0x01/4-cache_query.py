import time
import sqlite3
import functools

# Global cache dictionary to store query results
query_cache = {}

# Database connection decorator (reuse from earlier tasks)
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Caching decorator that stores results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None

        if query in query_cache:
            print(f"[CACHE] Returning cached result for query: {query}")
            return query_cache[query]
        
        print(f"[CACHE MISS] Query not cached. Executing: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result  # Cache the result
        return result
    return wrapper

# Function to fetch users, caching the result
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — runs query and caches it
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — loads result from cache, avoids DB hit
users_again = fetch_users_with_cache(query="SELECT * FROM users")

