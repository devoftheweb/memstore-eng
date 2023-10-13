from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    def __init__(self, capacity: int) -> None:
        """
        Initializes an LRU (Least Recently Used) cache with the given capacity.

        Args:
            capacity (int): The maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get_from_cache(self, key: str) -> Optional[Any]:
        """
        Retrieves the value associated with the given key from the cache.

        Args:
            key (str): The key to look up in the cache.

        Returns:
            Optional[Any]: The value associated with the key, or None if the key is not in the cache.
        """
        value = self.cache.pop(key, None)
        if value is not None:
            self.cache[key] = value  # Move the accessed item to the end to show it was recently used
        return value

    def add_to_cache(self, key: str, value: Any) -> None:
        """
        Adds a key-value pair to the cache.

        Args:
            key (str): The key to add.
            value (Any): The value to associate with the key.
        """
        # Remove the key if it's already in the cache
        if key in self.cache:
            self.cache.pop(key)

        # Evict the least recently used item if the cache reaches its capacity
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Removes the first item

        # Add the key-value pair to the cache
        self.cache[key] = value

    def remove_from_cache(self, key: str) -> None:
        """
        Removes a key-value pair from the cache.

        Args:
            key (str): The key to remove.
        """
        self.cache.pop(key, None)

    def clear_cache(self) -> None:
        """
        Clears all key-value pairs from the cache.
        """
        self.cache.clear()
