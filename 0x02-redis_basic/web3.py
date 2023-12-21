#!/usr/bin/env python3
import requests
import time
import redis
from functools import wraps

# Create a Redis connection
redis_conn = redis.Redis()

def cache_with_expiry(expiration):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cache_key = f'cache:{url}'
            count_key = f'count:{url}'
            
            # Check if the URL is in the cache
            cached_content = redis_conn.get(cache_key)
            if cached_content:
                redis_conn.incr(count_key)
                return cached_content.decode('utf-8')

            # If not in the cache, fetch the content and cache it
            response = requests.get(url)
            content = response.text
            redis_conn.setex(cache_key, expiration, content)
            redis_conn.incr(count_key)
            
            return content
        
        return wrapper
    return decorator

@cache_with_expiry(expiration=10)
def get_page(url: str) -> str:
    return requests.get(url).text

if __name__ == "__main__":
    # Test with Google
    for _ in range(5):
        content = get_page("http://google.com")
        print(content[:100])  # Print a snippet of the content
        time.sleep(2)
    
    google_count_key = 'count:http://google.com'
    google_access_count = redis_conn.get(google_count_key)
    if google_access_count:
        print(f"Access count for http://google.com: {google_access_count.decode('utf-8')}")
    else:
        print("Access count for http://google.com: Not available")

    # Test with slowwly.robertomurray.co.uk
    for _ in range(5):
        content = get_page("http://slowwly.robertomurray.co.uk/delay/1000")
        print(content[:100])  # Print a snippet of the content
        time.sleep(2)
    
    slowwly_count_key = 'count:http://slowwly.robertomurray.co.uk'
    slowwly_access_count = redis_conn.get(slowwly_count_key)
    if slowwly_access_count:
        print(f"Access count for http://slowwly.robertomurray.co.uk: {slowwly_access_count.decode('utf-8')}")
    else:
        print("Access count for http://slowwly.robertomurray.co.uk: Not available")
