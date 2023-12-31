import unittest
from server.data_store.data_store import DataStore
from server.data_store.sharding.shard import Shard

class TestDataStore(unittest.TestCase):

    def setUp(self):
        # Creating shards and initializing DataStore with them
        shards = [Shard() for _ in range(10)]  # Example: 10 shards
        self.data_store = DataStore(shards)
        print("Shards created and DataStore initialized")

    def test_put_and_get(self):
        transaction_id = self.data_store.start_transaction()
        self.data_store.put("key1", "value1", transaction_id)
        self.data_store.commit_transaction(transaction_id)

        transaction_id = self.data_store.start_transaction()
        value = self.data_store.get("key1", transaction_id)
        self.data_store.commit_transaction(transaction_id)

        self.assertEqual(value, "value1")
        print("PUT and GET - Test passed")

    def test_put_and_delete(self):
        transaction_id = self.data_store.start_transaction()
        self.data_store.put("key2", "value2", transaction_id)
        self.data_store.commit_transaction(transaction_id)

        transaction_id = self.data_store.start_transaction()
        self.data_store.delete("key2", transaction_id)
        self.data_store.commit_transaction(transaction_id)

        transaction_id = self.data_store.start_transaction()
        value = self.data_store.get("key2", transaction_id)
        self.data_store.commit_transaction(transaction_id)

        self.assertIsNone(value)
        print("PUT and DEL - Test passed")

if __name__ == '__main__':
    unittest.main()
