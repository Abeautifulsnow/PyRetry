import logging
import random
import time
from functools import partial
from typing import Callable, Union, Tuple, Optional, NewType, Any

from .compat import decorator

logging_logger = logging.getLogger(__name__)
T_Exception = NewType('T_Exception', Exception)


def __retry_internal(
        f: Callable,
        exceptions: Union[T_Exception, Tuple[T_Exception, ...]] = Exception,
        tries: int = -1,
        delay: int = 0,
        max_delay: Optional[int] = None,
        backoff: int = 1,
        jitter: Union[int, Tuple[int, ...]] = 0,
        logger: Optional[logging.Logger] = logging_logger
) -> Optional[Callable]:
    """
    Executes a function and retries it if it failed.

    :param f: the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    _tries, _delay = tries, delay

    while _tries:
        try:
            return f()
        except exceptions as e:
            _tries -= 1
            if not _tries:
                raise

            if logger:
                logger.warning(f'{e}, retrying in {_delay} seconds...')

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay:
                _delay = min(_delay, max_delay)


def retry(
        exceptions: Union[T_Exception, Tuple[T_Exception, ...]] = Exception,
        tries: int = -1,
        delay: int = 0,
        max_delay: Optional[int] = None,
        backoff: int = 1,
        jitter: Union[int, Tuple[int, ...]] = 0,
        logger: Optional[logging.Logger] = logging_logger
) -> Callable:
    """Returns a retry decorator.

    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: a retry decorator.
    """
    @decorator
    def retry_decorator(f: Callable, *fargs, **fkwargs):
        args = fargs if fargs else []
        kwargs = fkwargs if fkwargs else {}
        return __retry_internal(
            partial(f, *args, **kwargs),
            exceptions,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            logger
        )

    return retry_decorator


def retry_call(
        f: Callable,
        fargs: Optional[Any] = None,
        fkwargs: Optional[Any] = None,
        exceptions: Union[T_Exception, Tuple[T_Exception, ...]] = Exception,
        tries: int = -1,
        delay: int = 0,
        max_delay: Optional[int] = None,
        backoff: int = 1,
        jitter: Union[int, Tuple[int, ...]] = 0,
        logger: Optional[logging.Logger] = logging_logger
) -> Callable:
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: -1 (infinite).
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :returns: the result of the f function.
    """
    args = fargs if fargs else []
    kwargs = fkwargs if fkwargs else {}
    return __retry_internal(
        partial(f, *args, **kwargs),
        exceptions,
        tries,
        delay,
        max_delay,
        backoff,
        jitter,
        logger
    )
