import time
from functools import wraps

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """
    A decorator that allows retrying a function call in case of a specified exception.

    Parameters:
    -----------
    ExceptionToCheck : Exception or tuple of Exceptions
        The exception(s) that should trigger a retry of the decorated function.
    tries : int, optional
        The maximum number of times the function should be retried, defaults to 4.
    delay : int, optional
        The delay in seconds between retries, defaults to 3.
    backoff : int, optional
        The factor by which the delay should increase after each retry, defaults to 2.
    logger : logging.Logger, optional
        A logger object to be used for logging retry attempts, defaults to None.

    Returns:
    --------
    The wrapped function.

    Example:
    --------
    >>> @retry(ValueError, tries=3, delay=2, backoff=2)
    ... def my_function():
    ...     print("Calling my_function")
    ...     raise ValueError("oops!")
    ...
    >>> my_function()
    # waits 2 seconds and retries up to 3 times before failing with the ValueError exception
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = f"{str(e)}, Retrying in {mdelay} seconds..."
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry