# API Exception Handling

This repository is a guide that walks you through how to handle exceptions using a basic API that communicates with a SQLite database. It includes four versions, each with their own set of enhancements.

## Version 1

The first version of the API implements the following steps:

1. Identify potential error scenarios
2. Separate library-specific errors
3. Handle low-level errors
4. Raise errors suitable to the level above
5. Add custom exception types

## Version 2

The second version of the API implements the following steps:

- Automate the database creation and run it as the main program
- Integrate Context Manager

```
class SQLite:
    def __init__(self, file="my_application.db"):
        self.file = file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.close()
```

## Version 3

The third version of the API implements the following steps:

- Create a `retry()` decorator to retry database connection in case of a failure
- Create a `log_exceptions()` decorator to log errors and exceptions during data fetching.
```
@retry(sqlite3.OperationalError, tries=3, delay=1, backoff=2)
def create_database() -> None:
    with sqlite3.connect('application.db') as conn:
        cur = conn.cursor()

        cur.execute('''CREATE TABLE blogs
                    (id text NOT NULL PRIMARY KEY,
                    date TEXT,
                    title TEXT,
                    content TEXT,
                    public INTEGER)''')

        cur.execute("INSERT INTO blogs VALUES ('first-blog', '2021-03-07', 'My first blog' ,'Some content', 1)")

        cur.execute("INSERT INTO blogs VALUES ('private-blog', '2021-03-07', 'Secret blog' ,'This is a secret', 0)")


        conn.commit()

```

```
@app.route('/blogs/<id>')
@log_exceptions()
def get_blog(blog_id):
    try:
        return jsonify(fetch_blog(blog_id))
    except NotFoundError:
        abort(404, description="Resource not found.")
    except NotAuthorizedError:
        abort(403, description="Access denied.")

```

## Version 4

The fourth version refactors the code to demonstrate `monadic error handling` concepts with the `Result` type from the `returns` library. The `Result` type is a monadic data type that represents the outcome of a computation that may succeed or fail. The `Success` subclass holds the result of the computation, while the `Failure` subclass and holds the exception.

The updated version of the `@log_exceptions` decorator now logs exceptions to `version4_logs.log` file.

Each version is contained within its own directory and is documented in a separate markdown file.