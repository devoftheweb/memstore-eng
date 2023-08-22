import unittest
from server.server import Server
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
        response = self.client.send_command("PUT key1 value1")
        self.assertEqual(response['status'], 'Ok')

        response = self.client.send_command("GET key1")
        self.assertEqual(response['status'], 'Ok')
        self.assertEqual(response['result'], 'value1')

        # Additional tests for other commands...

    def tearDown(self):
        self.client.disconnect()
        self.server.stop()
        self.server_thread.join()

if __name__ == "__main__":
    unittest.main()
