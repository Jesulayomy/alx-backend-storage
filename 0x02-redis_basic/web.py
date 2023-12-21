#!/usr/bin/env python3
""" This module showcases expiring web caches """
import redis
import requests
import time
from functools import wraps
from typing import Callable


def dCache(expiration=10):
    def decorator(func):
        @wraps(func)
        def wrapper(url):

            cached_html = r.get(url)
            if cached_html:
                return cached_html.decode('utf-8')

            html_content = func(url)

            r.setex(url, expiration, html_content)
            count_key = f'count:{url}'
            r.incr(count_key)

            return html_content
        return wrapper
    return decorator


@dCache
def get_page(url: str) -> str:
    """ Return url content so you can see if you qualify"""

    return requests.get(url).text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"

    r = redis.Redis()
    print("Fetching page...")
    start_time = time.time()
    content = get_page(url)
    end_time = time.time()
    print("Page content:", content)
    print("Time taken:", end_time - start_time, "seconds")

    print("Fetching page...")
    start_time = time.time()
    content = get_page(url)
    end_time = time.time()
    print("Page content:", content)
    print("Time taken:", end_time - start_time, "seconds")
