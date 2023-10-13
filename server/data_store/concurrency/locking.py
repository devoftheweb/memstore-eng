from enum import Enum
from threading import RLock
from typing import Any, Dict


class LockType(Enum):
    """
    Enum to specify the type of lock.

    Attributes:
        READ (int): A read lock.
        WRITE (int): A write lock.
    """
    READ = 1
    WRITE = 2


class Lock:
    def __init__(self):
        """
        Initializes a Lock object with an empty set of holders and a reentrant lock.

        Attributes:
            type (LockType or None): Specifies the type of the lock (READ/WRITE). None if no lock is held.
            holders (set): A set of transaction IDs that currently hold this lock.
            lock (RLock): A reentrant lock for acquiring and releasing locks.
        """
        self.type = None
        self.holders = set()
        self.lock = RLock()

    def acquire(self, lock_type: LockType, transaction_id: int):
        """
        Acquires a lock of a given type for a given transaction ID.

        Args:
            lock_type (LockType): The type of lock to be acquired (READ/WRITE).
            transaction_id (int): The transaction ID for which the lock is being acquired.

        Raises:
            Exception: If a lock upgrade from READ to WRITE is attempted by a different transaction.
        """
        with self.lock:
            if lock_type == LockType.WRITE and self.type == LockType.READ and transaction_id not in self.holders:
                raise Exception("Cannot upgrade lock")
            self.type = lock_type
            self.holders.add(transaction_id)

    def release(self, transaction_id: int):
        """
        Releases a lock for a given transaction ID.

        Args:
            transaction_id (int): The transaction ID for which the lock is being released.
        """
        with self.lock:
            self.holders.discard(transaction_id)
            if not self.holders:
                self.type = None
