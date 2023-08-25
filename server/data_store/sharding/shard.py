from typing import Dict, Any

class Shard:
    def __init__(self) -> None:
        """Initializes the storage for the shard."""
        self.storage: Dict[str, Any] = {}
