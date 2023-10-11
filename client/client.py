import socket
import json
from typing import Any, Dict

class Client:
    def __init__(self, host: str = 'localhost', port: int = 8000) -> None:
        """Initializes the client with the server's host and port."""
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """Connects to the server."""
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_command(self, command_str: str) -> Dict[str, Any]:
        """Sends a command to the server and receives a response.

        Args:
            command_str (str): The command string to send.

        Returns:
            Dict[str, Any]: The response from the server.
        """
        self.client_socket.send(command_str.encode('utf-8'))
        response_str = self.client_socket.recv(1024).decode('utf-8').strip()
        print("Raw response from Client:", response_str)
        try:
            return json.loads(response_str)
        except json.JSONDecodeError:
            print("Error decoding response:", response_str)
            return None
        # return json.loads(response_str)

    def disconnect(self) -> None:
        """Disconnects from the server."""
        self.client_socket.close()
        print("Disconnected from server")
