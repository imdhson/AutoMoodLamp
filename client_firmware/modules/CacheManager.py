class CacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._cache = {}
        return cls._instance

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value