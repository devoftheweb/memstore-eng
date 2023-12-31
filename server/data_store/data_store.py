from typing import Any, Optional, List
from server.data_store.transactions.transaction import LockType
from server.data_store.transactions.transaction_manager import TransactionManager
from server.data_store.sharding.sharding_manager import ShardingManager
from server.data_store.sharding.shard import Shard


class DataStore:
    def __init__(self, shards: List[Shard] = None, caching_strategy=None) -> None:
        """
        Initializes the main storage, active transaction list, and sharding manager.

        Args:
            shards (List[Shard], optional): List of Shard objects for sharding. Defaults to 10 shards.
            caching_strategy: Optional caching strategy for caching key/value pairs.

        Attributes:
            transaction_manager (TransactionManager): Manages the transactions within the data store.
            sharding_manager (ShardingManager): Manages the sharding logic.
            caching_strategy: Caching strategy for managing cache.
        """
        self.transaction_manager = TransactionManager()
        self.sharding_manager = ShardingManager(shards or [Shard() for _ in range(10)])
        self.caching_strategy = caching_strategy


    def get_shard(self, key: str) -> Shard:
        """
        Get the shard responsible for the given key.

        Args:
            key (str): The key for which to find the responsible shard.

        Returns:
            Shard: The shard responsible for the key.
        """
        return self.sharding_manager.get_shard(key)


    def put(self, key: str, value: Any, transaction_id: int) -> None:
        """
        Adds or updates a key/value pair in the datastore.

        Args:
            key (str): The key to add or update.
            value (Any): The value to associate with the key.
            transaction_id (int): The ID of the transaction under which this operation falls.
        """
        shard = self.get_shard(key)
        self.transaction_manager.acquire_lock(key, LockType.WRITE, transaction_id)
        current_value = shard.storage.get(key)
        transaction = self.transaction_manager.transactions[transaction_id]
        transaction.put(key, value, current_value)
        if self.caching_strategy:
            self.caching_strategy.add_to_cache(key, value)


    def get(self, key: str, transaction_id: int) -> Optional[Any]:
        """
        Retrieves a value by key from the datastore.

        Args:
            key (str): The key to look up.
            transaction_id (int): The ID of the transaction under which this operation falls.

        Returns:
            Optional[Any]: The value associated with the key, or None if the key is not in the datastore.
        """
        shard = self.get_shard(key)
        self.transaction_manager.acquire_lock(key, LockType.READ, transaction_id)
        transaction = self.transaction_manager.transactions.get(transaction_id)
        if transaction:
            return transaction.changes.get(key, shard.storage.get(key, None))
        return shard.storage.get(key, None)


    def delete(self, key: str, transaction_id: int) -> None:
        """
        Deletes a value by key from the datastore.

        Args:
            key (str): The key to delete.
            transaction_id (int): The ID of the transaction under which this operation falls.
        """
        shard = self.get_shard(key)
        self.transaction_manager.acquire_lock(key, LockType.WRITE, transaction_id)
        current_value = shard.storage.get(key)
        transaction = self.transaction_manager.transactions[transaction_id]
        transaction.delete(key, current_value)
        if self.caching_strategy:
            self.caching_strategy.remove_from_cache(key)


    def show_all(self) -> dict:
        """
        Returns a dictionary containing all key-value pairs and their associated transaction IDs.

        Returns:
            dict: All key-value pairs in the datastore.
        """
        all_data = {}
        for shard in self.sharding_manager.shards:
            for key, value in shard.storage.items():
                transaction_id = self.transaction_manager.get_transaction_id_for_key(key)
                all_data[key] = {'value': value, 'transaction_id': transaction_id}
        return all_data


    def commit_all_transactions(self) -> None:
        """Commits all active transactions."""
        with self.transaction_manager.lock:
            self.transaction_manager.commit_all(self.sharding_manager.shards)

    def start_transaction(self) -> int:
        """
        Begins a new transaction.

        Returns:
            int: The ID of the new transaction.
        """
        transaction_id = self.transaction_manager.begin()
        return transaction_id

    def commit_transaction(self, transaction_id: int) -> None:
        """
        Commits the current transaction.

        Args:
            transaction_id (int): The ID of the transaction to commit.
        """
        with self.transaction_manager.lock:
            transaction = self.transaction_manager.transactions.get(transaction_id)
            if transaction:
                self.transaction_manager.commit(transaction_id, self.sharding_manager.shards)

    def rollback_transaction(self, transaction_id: int) -> None:
        """
        Rolls back the current transaction, undoing all its changes.

        Args:
            transaction_id (int): The ID of the transaction to roll back.
        """
        with self.transaction_manager.lock:
            transaction = self.transaction_manager.transactions.get(transaction_id)
            if transaction:
                transaction.undo(self.sharding_manager.shards)  # Pass the shards here
                self.transaction_manager.rollback(transaction_id)
