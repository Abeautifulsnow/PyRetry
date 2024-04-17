import logging
import random
import time
from functools import partial
from typing import Any, Callable, NewType, Optional, TypeVar, Union

from .compat import decorator

logging_logger = logging.getLogger(__name__)
formatter = "%(asctime)s - %(name)s - L%(lineno)d - %(levelname)s - %(message)s"
logging.basicConfig(format=formatter)

T_Exception = NewType("T_Exception", Exception)
T_I_F = TypeVar("T_I_F", bound=Union[int, float])


def __retry_internal(
    f: Callable,
    exceptions: Union[T_Exception, tuple[T_Exception, ...]] = Exception,
    tries: int = -1,
    delay: int = 0,
    max_delay: Optional[int] = None,
    backoff: int = 1,
    jitter: Union[T_I_F, tuple[T_I_F, ...]] = 0,
    logger: Optional[logging.Logger] = logging_logger,
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
    _delay = delay

    while tries != 0:
        try:
            return f()
        except exceptions as e:
            tries -= 1 if tries > 0 else 0
            if tries == 0:
                raise

            if logger:
                logger.warning(f"{e}, retrying in {_delay} seconds...")

            time.sleep(_delay)
            jitter_value = (
                random.uniform(*jitter) if isinstance(jitter, tuple) else jitter
            )
            _delay = (
                min(_delay * backoff + jitter_value, max_delay)
                if max_delay
                else _delay * backoff + jitter_value
            )


def retry(
    exceptions: Union[T_Exception, tuple[T_Exception, ...]] = Exception,
    tries: int = -1,
    delay: int = 0,
    max_delay: Optional[int] = None,
    backoff: int = 1,
    jitter: Union[T_I_F, tuple[T_I_F, ...]] = 0,
    logger: Optional[logging.Logger] = logging_logger,
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
    def retry_decorator(f: Callable, *f_args, **f_kwargs):
        args = f_args or []
        kwargs = f_kwargs or {}
        return __retry_internal(
            partial(f, *args, **kwargs),
            exceptions,
            tries,
            delay,
            max_delay,
            backoff,
            jitter,
            logger,
        )

    return retry_decorator


def retry_call(
    f: Callable,
    f_args: Optional[Any] = None,
    f_kwargs: Optional[Any] = None,
    exceptions: Union[T_Exception, tuple[T_Exception, ...]] = Exception,
    tries: int = -1,
    delay: int = 0,
    max_delay: Optional[int] = None,
    backoff: int = 1,
    jitter: Union[T_I_F, tuple[T_I_F, ...]] = 0,
    logger: Optional[logging.Logger] = logging_logger,
) -> Callable:
    """
    Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param f_args: the positional arguments of the function to execute.
    :param f_kwargs: the named arguments of the function to execute.
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
    args = f_args if f_args else []
    kwargs = f_kwargs if f_kwargs else {}
    return __retry_internal(
        partial(f, *args, **kwargs),
        exceptions,
        tries,
        delay,
        max_delay,
        backoff,
        jitter,
        logger,
    )
