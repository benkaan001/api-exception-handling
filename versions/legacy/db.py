import sqlite3

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
    # connect to the db
    con = sqlite3.connect('application.db')
    cur = con.cursor()

    # execute the query
    cur.execute('SELECT * FROM blogs WHERE public=1')

    # fetch the data and turn into a dict
    result = list(map(blog_list_to_json, cur.fetchall()))

    # close the connection
    con.close()

    return result

def fetch_blog(id: str):
    """ Returns the blog belonging to the id passed."""
    # connect to the db
    con = sqlite3.connect('./data/application.db')
    cur = con.cursor()

    # excecute query and fetch data
    cur.execute(f"SELECT * FROM blogs WHERE id='{id}'")
    result = cur.fetchone()

    data = blog_list_to_json(result)

    # close the connection
    con.close()

    return data