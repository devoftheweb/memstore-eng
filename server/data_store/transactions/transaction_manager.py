from typing import Any, Dict, Optional, List
from threading import RLock
from server.data_store.concurrency.locking import Lock, LockType
from server.data_store.sharding.shard import Shard
from server.data_store.transactions.transaction import Transaction


class TransactionManager:
    def __init__(self) -> None:
        """
        Initializes the TransactionManager with an empty list of transactions and locks.

        Attributes:
            current_transaction_id (int): The current transaction ID, incremented each time a new transaction starts.
            transactions (dict): A dictionary mapping transaction IDs to Transaction objects.
            locks (dict): A dictionary mapping keys to Lock objects.
            lock (RLock): A reentrant lock for synchronizing access to transactions and locks.
        """
        self.current_transaction_id = 0
        self.transactions = {}
        self.locks = {}
        self.lock = RLock()

    def begin(self) -> int:
        """
        Begins a new transaction and returns the transaction ID.

        Returns:
            int: The ID of the new transaction.
        """
        transaction_id = self._generate_transaction_id()
        self.transactions[transaction_id] = Transaction()
        return transaction_id

    def _generate_transaction_id(self) -> int:
        """
        Generates a new unique transaction ID and returns it.

        Returns:
            int: The new transaction ID.
        """
        self.current_transaction_id += 1
        return self.current_transaction_id

    def commit(self, transaction_id: int, shards: List[Shard]) -> None:
        """
        Commits a transaction.

        Args:
            transaction_id (int): The ID of the transaction to commit.
            shards (List[Shard]): The list of shards affected by the transaction.
        """
        with self.lock:
            transaction = self.transactions.get(transaction_id)
            if transaction:
                transaction.commit(shards)
                self._release_locks(transaction_id)

    def rollback(self, transaction_id: int) -> None:
        """
        Rolls back a transaction, undoing all its changes.

        Args:
            transaction_id (int): The ID of the transaction to roll back.
        """
        with self.lock:
            transaction = self.transactions.get(transaction_id)
            if transaction:
                transaction.rollback()
                self._release_locks(transaction_id)

    def _release_locks(self, transaction_id: int) -> None:
        """
        Releases all locks held by a transaction.

        Args:
            transaction_id (int): The ID of the transaction whose locks are to be released.
        """
        for lock in self.locks.values():
            lock.release(transaction_id)

    def get_transaction_id_for_key(self, key: str) -> Optional[int]:
        """
        Returns the transaction ID associated with a given key, if any.

        Args:
            key (str): The key to look up.

        Returns:
            Optional[int]: The ID of the transaction associated with the key, or None if there is no such transaction.
        """
        for transaction_id, transaction in self.transactions.items():
            if key in transaction.changes or key in transaction.deleted_keys:
                return transaction_id
        return None

    def commit_all(self, shards: List[Shard]) -> None:
        """
        Commits all active transactions.

        Args:
            shards (List[Shard]): The list of shards affected by the transactions.
        """
        with self.lock:
            for transaction_id in list(self.transactions.keys()):
                self.commit(transaction_id, shards)

    def acquire_lock(self, key: str, lock_type: LockType, transaction_id: int) -> None:
        """
        Acquires a lock of a certain type on a key for a transaction.

        Args:
            key (str): The key to lock.
            lock_type (LockType): The type of lock to acquire (READ or WRITE).
            transaction_id (int): The ID of the transaction for which to acquire the lock.
        """
        with self.lock:
            lock = self.locks.get(key)
            if lock is None:
                lock = Lock()
                self.locks[key] = lock
            lock.acquire(lock_type, transaction_id)
