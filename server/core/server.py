import socket
import threading
import json
from server.data_store.data_store import DataStore
from server.core.command_parser import CommandParser
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
        """Handles a single client connection, reading commands and responding."""
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
        try:
            action, params, transaction_id = self.command_parser.parse_command(command_str)

            # Handle the BEGIN command to start a transaction
            if action == "BEGIN":
                transaction_id = self.data_store.start_transaction()
                return {'status': 'Ok', 'transaction_id': transaction_id}

            # Validate transaction_id for commands that require it
            if action in ["PUT", "GET", "DEL", "COMMIT", "ROLLBACK"]:
                if transaction_id is None or transaction_id not in self.data_store.transaction_manager.transactions:
                    return {'status': 'Error', 'mesg': f'Invalid transaction ID {transaction_id}'}

            # Handle other commands using the transaction_id
            if action == "PUT":
                self.data_store.put(params['key'], params['value'], transaction_id)
                return {'status': 'Ok'}
            elif action == "GET":
                result = self.data_store.get(params['key'], transaction_id)
                return {'status': 'Ok', 'result': result}
            elif action == "DEL":
                self.data_store.delete(params['key'], transaction_id)
                return {'status': 'Ok'}
            elif action == "START":
                self.data_store.start_transaction(transaction_id)
                return {'status': 'Ok'}
            elif action == "SHOWALL":
                all_data = self.data_store.show_all()
                return {'status': 'Ok', 'data': all_data}
            elif action == "COMMIT":
                self.data_store.commit_transaction(transaction_id)
                return {'status': 'Ok'}
            elif action == "COMMITALL":
                self.data_store.commit_all_transactions()
                return {'status': 'Ok'}
            elif action == "ROLLBACK":
                self.data_store.rollback_transaction(transaction_id)
                return {'status': 'Ok'}
            else:
                return {'status': 'Error', 'mesg': 'Unknown command'}
        except ValueError as e:
            return {'status': 'Error', 'mesg': str(e)}

    def stop(self) -> None:
        self.running = False
        # Create a temporary socket to unblock the accept() call in the server's main loop
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_socket.connect((self.host, self.port))
        temp_socket.close()
        self.server_socket.close()
        print("Server stopped")
