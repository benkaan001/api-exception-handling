import logging
import traceback # to format traceback message
from functools import wraps
from typing import Any, Callable

def create_logger(log_file_path: str = 'default_logger.log', log_level: int = logging.INFO) -> logging.Logger:
    """
    Creates a `logger` object that writes log messages to a file.

    ## Parameters:
    `log_file_path`: The path of the log file. Defaults to 'exc_logger.log'.
    `log_level`: The level at which the logger should log. Defaults to logging.INFO.

    ## Returns:
    Logger object: A Logger object that writes log messages to the specified file.

    - The logger object created by this function writes log messages to a file with the given path.
    - If no path is specified, it writes log messages to a file named 'exc_logger.log' in the current directory.
    - The log level determines which log messages are processed by the logger.
    - The default log level is INFO, which means that log messages with a level of
    INFO, WARNING, ERROR, or CRITICAL will be processed.

    - You can use the logger object to write log messages to the specified log file using methods like
        - `logger.info()`,
        - `logger.warning()`,
        - `logger.error()`, and
        - `logger.critical()`.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler() # create a steam handler to put the output on the terminal as well
    stream_handler.setFormatter(formatter) # use the same format

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def log_exceptions(logger: logging.Logger) -> Callable[[Any], Any]:
    """
    A decorator function that logs any exceptions raised by the decorated function.

    ## Parameters:
    logger: The logger object to use for logging the exceptions. Default create_logger(exc_logger.log)

    ## Usage:
    1. Create a logger object using the `create_logger` function.
    2. Decorate the functions you want to log exceptions for using the `log_exceptions` decorator.
    3. Call the decorated function as usual.

    ## Example:

    1. Create a logger object

        logger = create_logger('my_logger')

    2. Create a function to decorate

        @log_exceptions(logger)
        def my_function():
            raise ValueError('Something went wrong!')

    3. Call the function

        my_function()

    - The `log_exceptions` decorator logs any exceptions raised by the decorated function
    using the specified logger object.

    - It also re-raises the exception so that it can be handled by the caller,
    while still allowing the exception to be logged.
    """
    def decorator_log_exceptions(func):
        @wraps(func)
        def wrapper_log_exceptions(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                traceback_message = traceback.format_exc()
                modified_traceback_message = traceback_message.split(',')[:3]
                error_message = f"Exception in {func.__name__}: {e}\
                                \n{modified_traceback_message}"
                logger.error(error_message)
                raise # would halt the application
        return wrapper_log_exceptions
    return decorator_log_exceptions