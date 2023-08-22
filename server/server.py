import socket
import threading
import json
from server.data_store import DataStore
from server.command_parser import CommandParser
from typing import Any, Dict


class Server:
    def __init__(self, host: str = 'localhost', port: int = 8000) -> None:
        """Initializes the server with the given host and port."""
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_store = DataStore()
        self.command_parser = CommandParser()
        self.running = False

    def start(self) -> None:
        """Starts the server, listens for client connections, and processes commands."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"Server started on {self.host}:{self.port}")

        while self.running:
            client_socket, address = self.server_socket.accept()
            print(f"New connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket: socket.socket) -> None:
        """Handles a single client connection, reading commands and responding.

        Args:
            client_socket (socket.socket): The client socket connection.
        """
        with client_socket:
            while True:
                command_str = client_socket.recv(1024).decode('utf-8').strip()
                if not command_str:
                    break

                response = self.process_command(command_str)
                client_socket.send(json.dumps(response).encode('utf-8'))

    def process_command(self, command_str: str) -> Dict[str, Any]:
        """Processes a command, executing the appropriate action on the data store.

        Args:
            command_str (str): The command string to process.

        Returns:
            Dict[str, Any]: The response to the client.
        """
        try:
            action, params = self.command_parser.parse_command(command_str)
            if action == "PUT":
                self.data_store.put(params['key'], params['value'])
                return {'status': 'Ok'}
            elif action == "GET":
                result = self.data_store.get(params['key'])
                return {'status': 'Ok', 'result': result}
            elif action == "DEL":
                self.data_store.delete(params['key'])
                return {'status': 'Ok'}
            elif action == "START":
                self.data_store.start_transaction()
                return {'status': 'Ok'}
            elif action == "COMMIT":
                self.data_store.commit_transaction()
                return {'status': 'Ok'}
            elif action == "ROLLBACK":
                self.data_store.rollback_transaction()
                return {'status': 'Ok'}
            else:
                return {'status': 'Error', 'mesg': 'Unknown command'}

        except ValueError as e:
            return {'status': 'Error', 'mesg': str(e)}

    def stop(self) -> None:
        """Stops the server."""
        self.running = False
        self.server_socket.close()
        print("Server stopped")
