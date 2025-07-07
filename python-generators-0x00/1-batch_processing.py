import mysql.connector   # or any PEP‑249 driver

def stream_users_in_batches(batch_size):
    """
    Generator that pulls rows from the `users` table in fixed‑size batches.

    Yields
    ------
    list[dict]   # each element is a batch (list) of rows represented as dicts
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="YOUR_USER",
        password="YOUR_PASSWORD",
        database="YOUR_DB",
        cursorclass=mysql.connector.cursor.DictCursor  # rows as dicts
    )
    try:
        cur   = conn.cursor()
        offset = 0
        while True:                                   # ← 1st (outer) loop
            cur.execute(
                "SELECT id, name, age FROM users LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            rows = cur.fetchall()
            if not rows:
                break
            yield rows                                # hand off a whole batch
            offset += batch_size
    finally:
        conn.close()


def batch_processing(batch_size):
    """
    Consumes the batches, filters users older than 25, and
    yields the filtered sub‑batches one at a time.
    """
    for batch in stream_users_in_batches(batch_size):  # ← 2nd (inner) loop
        filtered = [row for row in batch if row["age"] > 25]
        if filtered:
            yield filtered


# --- Example usage -------------------------------------------
if __name__ == "__main__":
    for result_batch in batch_processing(batch_size=500):
        print(f"Processed {len(result_batch)} users:", result_batch)

