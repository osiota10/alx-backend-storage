#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import time
from functools import lru_cache

# Dictionary to track URL access count
url_access_count = {}


def get_page(url: str) -> str:
    # Increment URL access count
    url_access_count[f"count:{url}"] = url_access_count.get(f"count:{url}", 0) + 1

    # Use requests to fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    return html_content


# Use lru_cache decorator to cache the result with an expiration time of 10 seconds
@lru_cache(maxsize=None, typed=True)
def cached_get_page(url: str) -> str:
    return get_page(url)


# Test the get_page function with caching and URL access count tracking
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

    # Access the URL multiple times to test caching
    for _ in range(5):
        start_time = time.time()
        content = cached_get_page(url)
        print(f"URL content fetched in {time.time() - start_time} seconds")

    # Print the URL access count
    print(url_access_count)



@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    return res.text
