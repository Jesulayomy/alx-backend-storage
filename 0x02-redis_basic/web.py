#!/usr/bin/env python3
""" This module showcases expiring web caches """
import redis
import requests
from functools import wraps
from typing import Callable


redDb = redis.Redis()


def dCache(method: Callable) -> Callable:
    """ Temporarily left the countr """

    @wraps(method)
    def cover(url) -> str:
        """ Wrapper for the get_page and iscariot"""

        redDb.incr(f'count:{url}')
        result = redDb.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redDb.set(f'count:{url}', 0)
        redDb.setex(f'result:{url}', 10, result)
        return result
    return cover


@dCache
def get_page(url: str) -> str:
    """ Return url content so you can see if you qualify"""

    return requests.get(url).text
