from typing import Any, Dict, Optional, List
from enum import Enum
from threading import RLock
from server.data_store.concurrency.locking import Lock, LockType
from server.data_store.sharding.shard import Shard


class Transaction:
    def __init__(self) -> None:
        self.changes: Dict[str, Any] = {}
        self.deleted_keys: set = set()
        self.pre_commit_state: Dict[str, Any] = {}

    def get(self, key: str, transaction_id: int) -> Optional[Any]:
        """Retrieves a value by key."""
        shard = self.get_shard(key)
        self.transaction_manager.acquire_lock(key, LockType.READ, transaction_id)
        return shard.storage.get(key, None)

    def put(self, key: str, value: Any, current_value: Any) -> None:
        if key not in self.changes:
            self.pre_commit_state[key] = current_value
        self.changes[key] = value
        if key in self.deleted_keys:
            self.deleted_keys.remove(key)

    def delete(self, key: str, current_value: Any) -> None:
        if key not in self.deleted_keys:
            self.pre_commit_state[key] = current_value
        self.deleted_keys.add(key)
        self.changes.pop(key, None)

    def rollback(self) -> None:
        self.changes.clear()
        self.deleted_keys.clear()
        self.pre_commit_state.clear()

    def commit(self, shards: List[Shard]) -> None:
        for shard in shards:
            for key, value in self.changes.items():
                shard.storage[key] = value
            for key in self.deleted_keys:
                shard.storage.pop(key, None)
        self.changes.clear()
        self.deleted_keys.clear()
        self.pre_commit_state.clear()

    def undo(self, shards: List[Shard]) -> None:
        for shard in shards:
            for key, value in self.pre_commit_state.items():
                if value is not None:
                    shard.storage[key] = value
                else:
                    shard.storage.pop(key, None)
