import socket
import threading
import json
from server.data_store.data_store import DataStore
from server.core.command_parser import CommandParser
from typing import Any, Dict


class Server:
    def __init__(self, host: str = 'localhost', port: int = 8000) -> None:
        """
        Initializes the server with the given host and port.

        Args:
            host (str): The host address on which the server will run. Default is 'localhost'.
            port (int): The port number on which the server will listen. Default is 8000.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_store = DataStore()
        self.command_parser = CommandParser()
        self.running = False

    def start(self) -> None:
        """
        Starts the server, listens for client connections, and processes commands.
        The server will continue running until the `self.running` is set to False.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1)  # Set a timeout of 1 second
        self.running = True
        print(f"Server started on {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"New connection from {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except socket.timeout:
                pass  # Ignore timeout exceptions; just continue checking self.running

        print("Server loop has ended")  # Debug message to confirm the loop has ended

    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handles a single client connection, reading commands and responding.

        Args:
            client_socket (socket.socket): The client socket to communicate with.
        """
        with client_socket:
            while True:
                command_str = client_socket.recv(1024).decode('utf-8').strip()
                print(f"Received command: {command_str}")
                if not command_str:
                    break

                response = self.process_command(command_str)
                print("Server response:", response)
                client_socket.send(json.dumps(response).encode('utf-8'))

    def process_command(self, command_str: str) -> Dict[str, Any]:
        """
        Processes a command string and returns a response dictionary.

        Args:
            command_str (str): The command string to process.

        Returns:
            Dict[str, Any]: A dictionary containing the response status and any additional data.
        """
        try:
            action, params, transaction_id = self.command_parser.parse_command(command_str)
            # The actual command processing logic here...
            # (omitted for brevity)
        except ValueError as e:
            return {'status': 'Error', 'mesg': str(e)}

    def stop(self) -> None:
        """
        Stops the server. It performs the necessary clean-up to ensure all resources are released properly.
        """
        self.running = False
        # Create a temporary socket to unblock the accept() call in the server's main loop
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect((self.host, self.port))
        temp_socket.close()
        self.server_socket.close()
        print("Server stopped")
