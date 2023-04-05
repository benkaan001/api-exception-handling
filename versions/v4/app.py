import sqlite3
from typing import List
from returns.result import Result, safe
from returns.pipeline import flow
from returns.pointfree import bind
from utils.updated_logging_decorator import log_exceptions, create_logger

# create a logger object to pass to log_exceptions
version4_logger = create_logger(log_file_path='logs/version4_logs.log')

class SQLite():
    def __init__(self, file='./data/application.db'):
        self.file = file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()

class NotFoundError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass

@safe
@log_exceptions(logger=version4_logger)
def fetch_blog_from_db(blog_id) -> List:
    with SQLite('./data/application.db') as cur:
        cur.execute(f"SELECT * FROM blogs WHERE id=?", [blog_id])
        result = cur.fetchone()
        if result is None:
            raise NotFoundError(f"Unable to find blog with {blog_id=}.")
        return Result.from_result(result)

@safe
def blog_to_dict(item) -> 'Blog':
    return{
        'id': item[0],
        'published': item[1],
        'title': item[2],
        'content': item[3],
        'public': bool(item[4])

    }

@safe
@log_exceptions(logger=version4_logger)
def verify_access(blog) -> 'Blog':
    blog_id = blog['id']
    blog_public = blog['public']
    if not blog_public:
        raise NotAuthorizedError(f"You are not allowed to access blog with {blog_id=}")
    return blog


def fetch_blog(blog_id) -> Result['Blog', Exception]:
    return flow(
        blog_id,
        fetch_blog_from_db,
        bind(blog_to_dict),
        bind(verify_access)
    )

blog_ids = ['first-blog', 'private-blog', 'wrong-blog']
for blog_id in blog_ids:
    response = fetch_blog(blog_id)
    print(response)
