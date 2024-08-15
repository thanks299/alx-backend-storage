#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        '''
        # Increment the count for the URL
        count = redis_store.incr(f'count:{url}')
        
        # Fetch cached result if available
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # Otherwise, fetch the result from the method
        result = method(url)
        
        # Cache the result and set expiration time
        redis_store.set(f'count:{url}', count)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
