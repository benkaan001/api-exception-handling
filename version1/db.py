import sqlite3

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
        # connect to the db
        con = sqlite3.connect('application.db')
        cur = con.cursor()

        # execute the query
        cur.execute('SELECT * FROM blogs WHERE public=1')

        # fetch the data and turn into a dict
        result = list(map(blog_list_to_json, cur.fetchall()))

        return result

    # in the case there is an exception, print out the exception and return an empty array
    except Exception as e:
        print(e)
        return []

    finally:
        # close the connection
        con.close()


def fetch_blog(id: str):
    """ Returns the blog belonging to the id passed."""
    try:
        # connect to the db
        con = sqlite3.connect('application.db')
        cur = con.cursor()

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
    finally:
        # close the connection
        con.close()
