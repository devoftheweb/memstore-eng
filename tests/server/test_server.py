import unittest
from server.core.server import Server
from client.client import Client
import threading


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = Server(port=9000)  # Different port for testing
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.start()

        self.client = Client(port=9000)
        self.client.connect()

    def test_commands(self):
        """Tests sending various commands to the server."""

        # Test BEGIN command
        response = self.client.send_command("BEGIN")
        transaction_id1 = response['transaction_id']
        self.assertIsNotNone(transaction_id1)

        # Test PUT command
        response = self.client.send_command(f"PUT key1 value1 {transaction_id1}")
        self.assertEqual(response['status'], 'Ok')

        # Test GET command
        response = self.client.send_command(f"GET key1 {transaction_id1}")
        self.assertEqual(response['status'], 'Ok')
        self.assertEqual(response['result'], 'value1')

        # Test ROLLBACK command
        response = self.client.send_command(f"ROLLBACK {transaction_id1}")
        self.assertEqual(response['status'], 'Ok')

        # Test DEL command
        response = self.client.send_command(f"DEL key1 {transaction_id1}")
        self.assertEqual(response['status'], 'Ok')

        # Test COMMIT command
        response = self.client.send_command(f"COMMIT {transaction_id1}")
        self.assertEqual(response['status'], 'Ok')

        # Test COMMITALL command
        response = self.client.send_command("COMMITALL")
        self.assertEqual(response['status'], 'Ok')

        # Test SHOWALL command
        response = self.client.send_command("SHOWALL")
        self.assertEqual(response['status'], 'Ok')
        self.assertIsNotNone(response['data'])  # Assuming the server returns the data

    def tearDown(self):
        self.client.disconnect()
        self.server.stop()
        self.server_thread.join()


if __name__ == "__main__":
    unittest.main()
