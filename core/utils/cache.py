# core/utils/cache.py
from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
from django.db.models import Model


def cache_key_generator(prefix, *args, **kwargs):
    """Generate a cache key from arguments"""
    key_parts = [prefix]

    for arg in args:
        if isinstance(arg, Model):
            key_parts.append(f"{arg.__class__.__name__}:{arg.pk}")
        elif isinstance(arg, (int, str, float, bool)):
            key_parts.append(str(arg))
        elif arg is None:
            key_parts.append("None")

    for key, value in sorted(kwargs.items()):
        key_parts.append(f"{key}:{value}")

    key_string = ":".join(key_parts)
    return f"eip:{hashlib.md5(key_string.encode()).hexdigest()}"


def cached_view(timeout=300):
    """Decorator to cache view responses"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Don't cache for authenticated users or POST requests
            if request.user.is_authenticated or request.method != 'GET':
                return view_func(request, *args, **kwargs)

            # Generate cache key from request
            path = request.get_full_path()
            cache_key = cache_key_generator('view', path)

            # Try to get from cache
            response = cache.get(cache_key)
            if response is not None:
                return response

            # Call the view function
            response = view_func(request, *args, **kwargs)

            # Cache the response
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)

            return response
        return wrapper
    return decorator


def cache_page_fragment(timeout=600):
    """Cache template fragments"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = cache_key_generator(
                'fragment', func.__name__, *args, **kwargs)
            result = cache.get(cache_key)

            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)

            return result
        return wrapper
    return decorator


def invalidate_cache(prefix=None, pattern=None):
    """Invalidate cache by prefix or pattern"""
    if settings.DEBUG:
        return

    try:
        if prefix:
            # Delete keys with prefix
            cache.delete_pattern(f"*{prefix}*")
        elif pattern:
            cache.delete_pattern(pattern)
    except:
        # Some cache backends don't support pattern deletion
        pass


def get_or_set_cache(key, func, timeout=300, *args, **kwargs):
    """Get from cache or set if not exists"""
    result = cache.get(key)
    if result is None:
        result = func(*args, **kwargs)
        cache.set(key, result, timeout)
    return result
