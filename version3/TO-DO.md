## TO-DOs:

### 1.Decorate `create_database()` with `retry()`

```
@retry(sqlite3.OperationalError, tries=3, delay=1, backoff=2)
def create_database() -> None:
    with sqlite3.connect('../application.db') as conn:
        cur = conn.cursor()

        # Create table
        cur.execute('''CREATE TABLE blogs
                    (id text NOT NULL PRIMARY KEY,
                    date TEXT,
                    title TEXT,
                    content TEXT,
                    public INTEGER)''')

        # Seed db
        cur.execute("INSERT INTO blogs VALUES ('first-blog', '2021-03-07', 'My first blog' ,'Some content', 1)")
        cur.execute("INSERT INTO blogs VALUES ('private-blog', '2021-03-07', 'Secret blog' ,'This is a secret', 0)")

        # commit changes
        conn.commit()

```

This example is using `sqlite3.OperationalError` as the `ExceptionToCheck` parameter, and setting `tries=3`, `delay=1`, and `backoff=2`, which means that the `create_database` function will be retried up to 3 times with a delay of 1 second between retries, and the delay will be doubled after each retry. If the `sqlite3.OperationalError` exception is still raised after 3 tries, the exception will be propagated to the caller of the `create_database` function.