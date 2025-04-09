import time
from functools import wraps
from hashlib import md5
from flask import request

cache = {}

CACHE_TIMEOUT = 5 * 60


def cache_result(key_prefix):
    """Декоратор для кэширования результа запроса. Если направляется тот же
    самый запрос в течение 5 минут, то данные беруться из кэша."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_args = request.args
            cache_key = key_prefix

            if request_args:
                cache_key += f"{request_args.get('start_date')}_{request_args.get('end_date')}_{request_args.get('limit', 'default')}"

            cache_key = md5(cache_key.encode('utf-8')).hexdigest()

            cached_data = cache.get(cache_key)
            if cached_data:
                cache_timestamp, result = cached_data
                if time.time() - cache_timestamp < CACHE_TIMEOUT:
                    print("Using cached result")
                    return result

            result = func(*args, **kwargs)
            cache[cache_key] = (time.time(), result)
            print("Caching new result")
            return result
        return wrapper
    return decorator
