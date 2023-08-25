from typing import List, Dict, Any
from server.data_store.sharding.shard import Shard

class ShardingManager:
    def __init__(self, shards: List[Shard]) -> None:
        """Initializes the sharding manager with a set of shards."""
        self.shards = shards

    def get_shard(self, key: str) -> Shard:
        """Determines the shard for a given key."""
        shard_id = hash(key) % len(self.shards)
        return self.shards[shard_id]

    def get_all_storages(self) -> Dict[str, Any]:
        """Returns all storage across shards."""
        all_storage = {}
        for shard in self.shards:
            all_storage.update(shard.storage)
        return all_storage
