from typing import List, Dict, Any
from server.data_store.sharding.shard import Shard

class ShardingManager:
    def __init__(self, shards: List[Shard]) -> None:
        """
        Initializes the ShardingManager with a given list of shards.

        Args:
            shards (List[Shard]): The list of Shard objects that will handle data storage.

        Attributes:
            shards (List[Shard]): A list of Shard objects used for sharding the data.
        """
        self.shards = shards

    def get_shard(self, key: str) -> Shard:
        """
        Determines which shard is responsible for a given key.

        Args:
            key (str): The key for which the responsible shard needs to be determined.

        Returns:
            Shard: The shard object responsible for the given key.
        """
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]

    def get_all_storages(self) -> Dict[str, Any]:
        """
        Retrieves all the key-value pairs stored across all shards.

        Returns:
            Dict[str, Any]: A dictionary containing all key-value pairs stored across shards.
        """
        all_storage = {}
        for shard in self.shards:
            all_storage.update(shard.storage)
        return all_storage
