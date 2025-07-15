import sqlite3
import functools

# Connection handler decorator 
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection into the decorated function
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# NEW: Transaction management decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Begin transaction implicitly
            result = func(conn, *args, **kwargs)

            # If no errors, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # On error, rollback changes
            conn.rollback()
            print(f"[ERROR] Transaction failed and was rolled back: {e}")
            raise e  # re-raise so the error can be handled or reported upstream
    return wrapper

# Apply both decorators
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Call function with decorators handling connection and transaction
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
