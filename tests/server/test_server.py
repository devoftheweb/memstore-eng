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

        # Example of starting a transaction
        response = self.client.send_command("BEGIN")
        transaction_id = response['transaction_id']  # Assuming the server returns a transaction ID

        response = self.client.send_command(f"PUT key1 value1 {transaction_id}")
        self.assertEqual(response['status'], 'Ok')

        response = self.client.send_command(f"GET key1 {transaction_id}")
        self.assertEqual(response['status'], 'Ok')
        self.assertEqual(response['result'], 'value1')

    def tearDown(self):
        self.client.disconnect()
        self.server.stop()
        self.server_thread.join()


if __name__ == "__main__":
    unittest.main()
