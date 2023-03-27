import sqlite3

def create_database() -> None:
    """
    Creates a SQLite database named `'application.db'` and seeds it with initial data.

    Returns:
    None
    """
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
