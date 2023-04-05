import sqlite3

con = sqlite3.connect('./data/application.db')

cur = con.cursor()

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
con.commit()

# close connection
con.close()