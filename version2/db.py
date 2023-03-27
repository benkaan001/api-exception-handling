import sqlite3

class SQLite:
    def __init__(self, file="application.db"):
        self.file = file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.close()

class NotFoundError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

def blog_list_to_json(blog_post):
    """ Converts the fetched data into a dictionary."""
    return {
        'id': blog_post[0],
        'published': blog_post[1],
        'title': blog_post[2],
        'content': blog_post[3],
        'public': bool(blog_post[4])
    }

def fetch_blogs():
    """ Returns all the public blogs."""
    try:
        with SQLite("application.db") as cur:
            # execute the query
            cur.execute('SELECT * FROM blogs WHERE public=1')

            # fetch the data and turn into a dict
            result = list(map(blog_list_to_json, cur.fetchall()))

            return result

    # in the case there is an exception, print out the exception and return an empty array
    except Exception as e:
        print(e)
        return []


def fetch_blog(id: str):
    """ Returns the blog belonging to the id passed."""
    try:
        with SQLite("application.db") as cur:

            # excecute query and fetch data
            cur.execute(f"SELECT * FROM blogs WHERE id='{id}'")
            result = cur.fetchone()

            # check if query returned a blog
            if result is None:
                raise NotFoundError(f"Unable to find blog with {id=}")

            data = blog_list_to_json(result)

            # check if user is authorized to view the blog
            if not data['public']:
                raise NotAuthorizedError(f"You are not allowed to view blog with {id=}.")

            return data
    except sqlite3.OperationalError as e:
        print(e)
        raise NotFoundError(f"Unable to find blog with {id=}.")
