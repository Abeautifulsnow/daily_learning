from django.core.cache import cache


def redis_cache(key, timeout):
    def __redis_cache(func):
        def wrapper(*args, **kwargs):
            # 判断缓存是否存在
            if cache.has_key(key):
                data = cache.get(key)
            else:
                data = func(*args, **kwargs)
                cache.set(key, data, timeout)
            return data
        return wrapper
    return __redis_cache
