from typing import Any, Dict, Optional, List
from enum import Enum
from threading import RLock
from server.data_store.concurrency.locking import Lock, LockType
from server.data_store.sharding.shard import Shard


class Transaction:
    def __init__(self) -> None:
        """
        Initializes a new transaction with empty dictionaries for changes and pre-commit state,
        and an empty set for deleted keys.

        Attributes:
            changes (Dict[str, Any]): A dictionary of key-value changes made in this transaction.
            deleted_keys (set): A set of keys that have been deleted in this transaction.
            pre_commit_state (Dict[str, Any]): A dictionary to keep track of the state before any changes.
        """
        self.changes: Dict[str, Any] = {}
        self.deleted_keys: set = set()
        self.pre_commit_state: Dict[str, Any] = {}

    def put(self, key: str, value: Any, current_value: Any) -> None:
        """
        Adds or updates a key-value pair in the transaction.

        Args:
            key (str): The key to be put.
            value (Any): The value to be put.
            current_value (Any): The current value of the key before this operation.
        """
        if key not in self.changes:
            self.pre_commit_state[key] = current_value
        self.changes[key] = value
        if key in self.deleted_keys:
            self.deleted_keys.remove(key)

    def delete(self, key: str, current_value: Any) -> None:
        """
        Deletes a key-value pair from the transaction.

        Args:
            key (str): The key to be deleted.
            current_value (Any): The current value of the key before this operation.
        """
        if key not in self.deleted_keys:
            self.pre_commit_state[key] = current_value
        self.deleted_keys.add(key)
        self.changes.pop(key, None)

    def rollback(self) -> None:
        """
        Rolls back all the changes made in this transaction.
        """
        self.changes.clear()
        self.deleted_keys.clear()
        self.pre_commit_state.clear()

    def commit(self, shards: List[Shard]) -> None:
        """
        Commits all the changes and deletions made in this transaction to the given shards.

        Args:
            shards (List[Shard]): The list of shards to which the changes should be committed.
        """
        for shard in shards:
            for key, value in self.changes.items():
                shard.storage[key] = value
            for key in self.deleted_keys:
                shard.storage.pop(key, None)
        self.changes.clear()
        self.deleted_keys.clear()
        self.pre_commit_state.clear()

    def undo(self, shards: List[Shard]) -> None:
        """
        Undoes all the changes and deletions made in this transaction, reverting to the original state.

        Args:
            shards (List[Shard]): The list of shards from which the changes should be undone.
        """
        for shard in shards:
            for key, value in self.pre_commit_state.items():
                if value is not None:
                    shard.storage[key] = value
                else:
                    shard.storage.pop(key, None)
