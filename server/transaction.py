from typing import Any, Dict, Optional


class Transaction:
    def __init__(self) -> None:
        """Initializes the transaction with an empty change log."""
        self.changes: Dict[str, Any] = {}
        self.deleted_keys: set = set()

    def put(self, key: str, value: Any) -> None:
        """Adds or updates a change in the transaction.

        Args:
            key (str): The key to add or update.
            value (Any): The value to associate with the key.
        """
        self.changes[key] = value
        if key in self.deleted_keys:
            self.deleted_keys.remove(key)

    def get(self, key: str, data_store: Dict[str, Any]) -> Optional[Any]:
        """Retrieves a value considering the changes in the transaction.

        Args:
            key (str): The key to retrieve.
            data_store (Dict[str, Any]): The main data store.

        Returns:
            Optional[Any]: The value considering the transaction changes, or None if not found.
        """
        if key in self.changes:
            return self.changes[key]
        if key in self.deleted_keys:
            return None
        return data_store.get(key, None)

    def delete(self, key: str) -> None:
        """Deletes a value considering the changes in the transaction.

        Args:
            key (str): The key to delete.
        """
        self.deleted_keys.add(key)
        self.changes.pop(key, None)

    def commit(self, data_store: Dict[str, Any]) -> None:
        """Applies the changes to the given data storage.

        Args:
            data_store (Dict[str, Any]): The main data store to apply the changes to.
        """
        for key, value in self.changes.items():
            data_store[key] = value
        for key in self.deleted_keys:
            data_store.pop(key, None)

    def rollback(self) -> None:
        """Clears the changes."""
        self.changes.clear()
        self.deleted_keys.clear()
