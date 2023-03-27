## TO-DOs:

### 1. Automate the db creation and run it as the main program.

### 2.Integrate Context Manager

A context manager can be implemented in Python by defining an object that has two methods:

- `__enter__()`: When the with statement is used, the `__enter__()` method is called, which sets up the resource and returns it to the caller.

- `__exit__()`: When the block inside the with statement is exited, the `__exit__()` method is called, which releases the resource and handles any exceptions that may have occurred.

```
    with open('my_file.txt', 'r') as f:
        data = f.read()
```

In this code, the `open()` function returns a file object, which is used as a context manager to read the contents of the file. The `with` statement ensures that the file is properly closed when the block is exited, even if an exception occurs.

```
import sqlite3

with sqlite3.connect('example.db') as conn:
    # Perform database operations here
```

In this code, the `connect()` method returns a `Connection` object, which is used as a context manager to perform database operations. When the block inside the `with` statement is exited, the Connection object's `__exit__()` method is called, which automatically closes the connection and frees any associated resources.

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

Here's how the code works:

- The `__init__` method is called when a new SQLite object is created. It initializes the file attribute to the name of the SQLite database file to use. If no file is specified, it defaults to "my_application.db".
- The `__enter__` method is called when the context manager is entered. It creates a new SQLite connection to the database file specified in the file attribute, and returns a `cursor object` that can be used to execute SQL statements on the database. The cursor object is returned so that it can be used inside the with block.
- The `__exit__` method is called when the context manager is exited. It closes the SQLite connection to the database.

- Here's an example of how this context manager can be used:

```
with SQLite("your_application.db") as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS your_table ...")
    cursor.execute("INSERT INTO your_table ...")
```


Finally, Context managers can also be used to implement more complex behavior, such as transaction management or thread synchronization. The `contextlib` module in Python provides utilities for working with context managers, including the `@contextmanager` decorator, which can be used to define a context manager as a generator function.