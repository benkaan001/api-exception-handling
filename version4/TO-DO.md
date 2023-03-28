## T0-DOs:

Use `monadic error handling` concepts with the ``Result`` type from `returns` library's `returns.result` module so that the script fetches a blog from the database and verifies whether the blog is public or not.

The scrip now requires the installation of `returns` library.

    - The returns library (pip install returns)

## Explanation:

The script defines four functions:

- `fetch_blog`: takes a blog_id argument and returns a `Result` object that either contains a dictionary representing the blog or an error. It uses the flow function from the `returns.pipeline` module to chain several operations together.

- `fetch_blog_from_db`: takes a blog_id argument and fetches the corresponding blog from the database using the SQLite class. It returns a dictionary representing the blog if it exists, or raises a `NotFoundError` if it does not.

- `blog_to_dict`: takes a dictionary representing a blog as input and converts it into a `Blog` object.

- `verify_access`: takes a `Blog` object as input and verifies whether the blog is public or not. If it is not public, it raises a `NotAuthorizedError`.

These functions use monadic error handling concepts with the `Result` type to handle errors and propagate them through the program.

The `fetch_blog_from_db`, `blog_to_dict`, and `verify_access` functions are all decorated with the `@safe` decorator from the returns library, which catches any exceptions that may occur and returns them as errors in the `Result` object.

The `SQLite` class is used to connect to a SQLite3 database and provides a context manager interface for executing SQL queries.

## Output:

```
<Success: {'id': 'first-blog', 'published': '2021-03-07', 'title': 'My first blog', 'content': 'Some content', 'public': True}>

<Failure: You are not allowed to access blog with blog_id='private-blog'>

<Failure: Unable to find blog with blog_id='wrong-blog'.>
```

## Conclusion:

This is a good example of how monadic error handling concepts can be applied to a real-world program, using the `Result` type from the `returns.result` module. By using this approach, the code is more robust and composable, and easier to reason about.