#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis
redis_store = redis.Redis()

def data_cacher(method: Callable) -> Callable:
    '''Decorator to cache the output of fetched data and track URL access.'''
    @wraps(method)
    def invoker(url: str) -> str:
        '''Wrapper function to manage caching and tracking.'''
        # Track the number of times the URL is accessed
        redis_store.incr(f'count:{url}')
        
        # Try to get the cached result
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # Fetch the data if not cached
        result = method(url)
        
        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Fetches and returns the content of a URL, caching and tracking the request.'''
    return requests.get(url).text

# Example usage
if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'
    content = get_page(url)
    print(content[:200])  # Print the first 200 characters to verify
