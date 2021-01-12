CACHE_SERVERS = {
    "default": {
        "type": "memcached",
        "host": "127.0.0.1",
        'key_prefix': 'memcached.demo_fast_api.',
        "port": 11211,
        "default_timeout": 604800
    }
}

ISS = "http://localhost:8001"
