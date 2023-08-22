from typing import Any, Dict, Optional
from server.transaction import Transaction


class DataStore:
    def __init__(self) -> None:
        """Initializes the main storage and active transaction list."""
        self.storage: Dict[str, Any] = {}
        self.active_transaction: Optional[Transaction] = None

    def start_transaction(self) -> None:
        """Begins a new transaction."""
        self.active_transaction = Transaction()

    def commit_transaction(self) -> None:
        """Commits the current transaction."""
        if self.active_transaction:
            self.active_transaction.commit(self.storage)
            self.active_transaction = None

    def rollback_transaction(self) -> None:
        """Discards changes in the current transaction."""
        if self.active_transaction:
            self.active_transaction.rollback()
            self.active_transaction = None

    def put(self, key: str, value: Any) -> None:
        """Adds or updates a key/value pair.

        Args:
            key (str): The key to add or update.
            value (Any): The value to associate with the key.
        """
        if self.active_transaction:
            self.active_transaction.put(key, value)
        else:
            self.storage[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value by key.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[Any]: The value associated with the key, or None if not found.
        """
        if self.active_transaction:
            return self.active_transaction.get(key, self.storage)
        return self.storage.get(key, None)

    def delete(self, key: str) -> None:
        """Deletes a value by key.

        Args:
            key (str): The key to delete.
        """
        if self.active_transaction:
            self.active_transaction.delete(key)
        else:
            self.storage.pop(key, None)
