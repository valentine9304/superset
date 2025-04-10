import time
from functools import wraps
from hashlib import md5


cache = {}

CACHE_TIMEOUT = 5 * 60


def generate_cache_key(key_prefix, extra=""):
    key = key_prefix + extra
    return md5(key.encode('utf-8')).hexdigest()


def cache_result(key_prefix):
    """Декоратор для кэширования результата запроса."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            extra = kwargs.get('id', '')
            cache_key = generate_cache_key(key_prefix, str(extra))

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


def clear_cache_key(key_prefix, extra=""):
    """Удаляет конкретный кэш по точному ключу."""
    cache_key = generate_cache_key(key_prefix, extra)
    if cache_key in cache:
        del cache[cache_key]
        print(f"Cleared cache for key: {key_prefix} {extra}")
    else:
        print(f"No cache found for key: {key_prefix} {extra}")


def clear_cache_by_prefix(key_prefix):
    """Удалить все кэшированные записи по префиксу."""
    keys_to_delete = [key for key in cache if key.startswith(md5(key_prefix.encode('utf-8')).hexdigest()[:8])]
    for key in keys_to_delete:
        del cache[key]
    print(f"Cleared {len(keys_to_delete)} cache entries with prefix '{key_prefix}'")
