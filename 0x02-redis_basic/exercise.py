#!/usr/bin/env python3
""" This exercise covers redis-py basics """
import redis
from functools import wraps
from typing import Any, Callable, Optional, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """ Counts the calls of a cache class """

    @wraps(method)
    def cover(self, *args, **kwargs) -> Any:
        """ Starts the parent method and increase its counter """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return cover


def call_history(method: Callable) -> Callable:
    """ Tracks the call details of a Cache method in a Cache class."""
    @wraps(method)
    def cover(self, *args, **kwargs) -> Any:
        """
            Calls the invoker method
        """
        input = '{}:inputs'.format(method.__qualname__)
        output = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output, output)
        return output
    return cover


def replay(fn: Callable) -> None:
    """ Display calling progress and history """

    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    input = '{}:inputs'.format(fxn_name)
    output = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(input, 0, -1)
    fxn_outputs = redis_store.lrange(output, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """ An instance of the Redis client """

    def __init__(self) -> None:
        """ initialzation function for redis """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Returnes a stored key """

        dKey = str(uuid4())
        self._redis.set(dKey, data)
        return dKey

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Extracts value from redis """

        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Gets a string from redis """
        ans = self._redis.get(key)
        return ans.decode('utf-8')

    def get_int(self, key: str) -> int:
        """ Gets ain integer from remote dict """

        ans = self._redis.get(key)
        try:
            ans = int(ans.decode("utf-8"))
        except Exception:
            ans = 0
        return ans
