import sqlite3
from retry_decorator import retry

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



