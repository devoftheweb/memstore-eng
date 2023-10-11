from typing import Any, Dict, Optional, List
from threading import RLock
from server.data_store.concurrency.locking import Lock, LockType
from server.data_store.sharding.shard import Shard
from server.data_store.transactions.transaction import Transaction


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

    def get_transaction_id_for_key(self, key: str) -> Optional[int]:
        """
        Returns the transaction ID associated with a given key, if any.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        for transaction_id, transaction in self.transactions.items():
            if key in transaction.changes or key in transaction.deleted_keys:
                return transaction_id
        return None

    def commit_all(self, shards: List[Shard]):
        with self.lock:
            for transaction_id in list(self.transactions.keys()):
                self.commit(transaction_id, shards)

    def acquire_lock(self, key: str, lock_type: LockType, transaction_id: int):
        with self.lock:
            lock = self.locks.get(key)
            if lock is None:
                lock = Lock()
                self.locks[key] = lock
            lock.acquire(lock_type, transaction_id)