from typing import Any, Dict, Optional, List
from enum import Enum
from threading import RLock
from server.data_store.concurrency.locking import Lock, LockType
from server.data_store.sharding.shard import Shard


class TransactionManager:
    def __init__(self):
        self.current_transaction_id = 0
        self.transactions = {}
        self.locks = {}
        self.lock = RLock()

    def begin(self) -> int:
        """Begins a new transaction and returns the transaction ID."""
        transaction_id = self._generate_transaction_id()
        self.transactions[transaction_id] = Transaction()
        return transaction_id

    def _generate_transaction_id(self) -> int:
        """Generates a new unique transaction ID."""
        self.current_transaction_id += 1
        return self.current_transaction_id

    def commit(self, transaction_id: int, shards: List[Shard]):
        with self.lock:
            transaction = self.transactions.get(transaction_id)
            if transaction:
                transaction.commit(shards)
                self._release_locks(transaction_id)

    def rollback(self, transaction_id: int):
        with self.lock:
            transaction = self.transactions.get(transaction_id)
            if transaction:
                transaction.rollback()
                self._release_locks(transaction_id)

    def _release_locks(self, transaction_id: int):
        for lock in self.locks.values():
            lock.release(transaction_id)

    def acquire_lock(self, key: str, lock_type: LockType, transaction_id: int):
        with self.lock:
            lock = self.locks.get(key)
            if lock is None:
                lock = Lock()
                self.locks[key] = lock
            lock.acquire(lock_type, transaction_id)


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
