import functools
import logging
from typing import Callable


def decorator(caller: Callable):
    """ Turns caller into a decorator.
    Unlike decorator module, function signature is not preserved.

    :param caller: caller(f, *args, **kwargs)
    """
    def decor(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return caller(f, *args, **kwargs)
        return wrapper
    return decor


class NullHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        pass
