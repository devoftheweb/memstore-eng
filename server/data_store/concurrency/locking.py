from enum import Enum
from threading import RLock
from typing import Any, Dict, Optional


class LockType(Enum):
    READ = 1
    WRITE = 2


class Lock:
    def __init__(self):
        self.type = None
        self.holders = set()
        self.lock = RLock()

    def acquire(self, lock_type: LockType, transaction_id: int):
        with self.lock:
            if lock_type == LockType.WRITE and self.type == LockType.READ and transaction_id not in self.holders:
                raise Exception("Cannot upgrade lock")
            self.type = lock_type
            self.holders.add(transaction_id)

    def release(self, transaction_id: int):
        with self.lock:
            self.holders.discard(transaction_id)
            if not self.holders:
                self.type = None
