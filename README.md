# Haus Engineering: In-Memory Key/Value Data Server
Author: Jose Morales


## Introduction

This project implements an in-memory key/value data store server that supports transactions. The server can accept multiple clients and handle commands to add, retrieve, update, and delete key/value pairs, as well as manage transactions.

## File structure

```bash
client/: Directory containing client-related components.
    -->client.py: Contains a class for client connections.
    
server/: Main directory containing server components.
    --> server.py: Contains the main server class handling client connections and dispatching commands.
    --> command_parser.py: Contains a class to parse and validate client commands.
    --> data_store.py: Contains the main class for the in-memory key-value store, managing transactions.
    --> transaction.py: Contains the class for handling individual transactions.

tests/: Directory containing unit tests.
  test_server.py: Unit tests for the server class.
  test_command_parser.py: Unit tests for the command parser class.
  test_data_store.py: Unit tests for the data store and transaction classes.
```

## Installation

1. Clone the repository or download the source code.
2. Ensure you have Python 3.x installed.
3. Navigate to the project directory in your terminal.
4. Run the server and client as described in the Usage section below.

## Usage

1. Run the Server. The server will start, and you can connect clients to it.

```bash
python server/server.py
```

2. Run a Client

You can use the `Client` class in the `client/client.py` file to connect to the server, send commands, and receive responses.

```python
from client.client import Client

client = Client()
client.connect()
response = client.send_command("PUT key1 value1")
print(response)  # Output: {'status': 'Ok'}
client.disconnect()
```

## Classes Overview


## Classes Overview

- `Server`: Accepts client connections, reads commands, and dispatches them to the appropriate handlers.
- `CommandParser`: Parses and validates client commands, translating them into actionable requests.
- `DataStore`: Manages the in-memory key-value store, supports basic CRUD operations, and controls transactions.
- `Transaction`: Manages an individual transaction, including tracking changes and allowing commits and rollbacks.
- `Client`: Used by clients to connect to the server, send commands, and receive responses.


## License

This project is open source and available under the MIT License. 