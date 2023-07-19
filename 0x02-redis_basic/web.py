#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

# Connect to Redis
store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.setex(cached_key, 10, html)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text

# Test the get_page function with caching and URL access count tracking
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

    # Access the URL multiple times to test caching and tracking
    for _ in range(5):
        content = get_page(url)
        print("URL content fetched")

    # Print the URL access count
    count_key = "count:" + url
    url_access_count = store.get(count_key)
    print(f"{url} accessed {url_access_count} times")
