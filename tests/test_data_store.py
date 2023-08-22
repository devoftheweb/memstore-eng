import unittest
from server.data_store import DataStore


class TestDataStore(unittest.TestCase):

    def test_crud_without_transaction(self):
        """Tests adding, updating, and retrieving key/value pairs without transactions."""
        store = DataStore()
        store.put("key1", "value1")
        self.assertEqual(store.get("key1"), "value1")
        store.put("key1", "value2")
        self.assertEqual(store.get("key1"), "value2")

    def test_delete_without_transaction(self):
        """Tests deleting keys without transactions."""
        store = DataStore()
        store.put("key1", "value1")
        store.delete("key1")
        self.assertIsNone(store.get("key1"))

    def test_transaction_commit_rollback(self):
        """Tests starting, committing, and rolling back a transaction."""
        store = DataStore()
        store.put("key1", "value1")
        store.start_transaction()
        store.put("key1", "value2")
        self.assertEqual(store.get("key1"), "value2")
        store.commit_transaction()
        self.assertEqual(store.get("key1"), "value2")

        store.start_transaction()
        store.put("key1", "value3")
        self.assertEqual(store.get("key1"), "value3")
        store.rollback_transaction()
        self.assertEqual(store.get("key1"), "value2")

    def test_crud_within_transaction(self):
        """Tests adding, updating, and retrieving key/value pairs within a transaction."""
        store = DataStore()
        store.start_transaction()
        store.put("key1", "value1")
        self.assertEqual(store.get("key1"), "value1")
        store.put("key1", "value2")
        self.assertEqual(store.get("key1"), "value2")
        store.commit_transaction()
        self.assertEqual(store.get("key1"), "value2")

    def test_delete_within_transaction(self):
        """Tests deleting keys within a transaction."""
        store = DataStore()
        store.put("key1", "value1")
        store.start_transaction()
        store.delete("key1")
        self.assertIsNone(store.get("key1"))
        store.commit_transaction()
        self.assertIsNone(store.get("key1"))


if __name__ == "__main__":
    unittest.main()
