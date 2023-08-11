# PyRetry

A nice decorator tool for retrying tasks when they failed. Forked from [retry](https://github.com/invl/retry)

## Test cases

```text
╰─± pytest -v
========================================================================== test session starts ==========================================================================
platform darwin -- Python 3.10.12, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Users/dapeng/.virtualenvs/py310/bin/python
cachedir: .pytest_cache
rootdir: /Users/dapeng/Desktop/code/Git/PyRetry
plugins: anyio-3.7.1
collected 9 items                                                                                                                                                       

tests/test_retry.py::test_retry PASSED                                                                                                                            [ 11%]
tests/test_retry.py::test_tries_inf PASSED                                                                                                                        [ 22%]
tests/test_retry.py::test_tries_minus1 PASSED                                                                                                                     [ 33%]
tests/test_retry.py::test_max_delay PASSED                                                                                                                        [ 44%]
tests/test_retry.py::test_fixed_jitter PASSED                                                                                                                     [ 55%]
tests/test_retry.py::test_retry_call PASSED                                                                                                                       [ 66%]
tests/test_retry.py::test_retry_call_2 PASSED                                                                                                                     [ 77%]
tests/test_retry.py::test_retry_call_with_args PASSED                                                                                                             [ 88%]
tests/test_retry.py::test_retry_call_with_kwargs PASSED                                                                                                           [100%]

=========================================================================== 9 passed in 0.10s ===========================================================================
```