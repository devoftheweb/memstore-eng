from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    def __init__(self, capacity: int) -> None:
        """Initializes an LRU cache with the given capacity.

        Args:
            capacity (int): The maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get_from_cache(self, key: str) -> Optional[Any]:
        value = self.cache.pop(key, None)
        if value is not None:
            self.cache[key] = value
        return value

    def add_to_cache(self, key: str, value: Any) -> None:
        # If the key is already in the cache, remove it
        if key in self.cache:
            self.cache.pop(key)

        # If the cache is at capacity, remove the least recently used item
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)

        # Add the key-value pair to the cache
        self.cache[key] = value

    def remove_from_cache(self, key: str) -> None:
        self.cache.pop(key, None)

    def clear_cache(self) -> None:
        """Clears the cache."""
        self.cache.clear()
