#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
import time

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_page(url: str) -> str:
    # Check if the page content is already cached in Redis
    cached_html_content = redis_client.get(url)
    if cached_html_content is not None:
        # Increment URL access count
        redis_client.incr(f"count:{url}")
        return cached_html_content

    # If not cached, fetch the HTML content using requests
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content in Redis with an expiration time of 10 seconds
    redis_client.setex(url, 10, html_content)

    # Increment URL access count
    redis_client.incr(f"count:{url}")

    return html_content

# Test the get_page function with caching and URL access count tracking
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

    # Access the URL multiple times to test caching and tracking
    for _ in range(5):
        start_time = time.time()
        content = get_page(url)
        print(f"URL content fetched in {time.time() - start_time:.2f} seconds")

    # Print the URL access count
    url_access_count = redis_client.get(f"count:{url}")
    print(f"{url} accessed {url_access_count} times")

