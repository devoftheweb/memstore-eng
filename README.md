# In-Memory Key/Value Data Store
Author: [Jose Morales](https://www.linkedin.com/in/moralesdev/)

## Introduction ⚡

High-performance in-memory key/value data store server. 

The following concepts are implemented: modular codebase, concurrency control, transactional consistency, sharding, LRU caching, and more.



### Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Functionality](#functionality)
4. [File Structure](#file-structure)
5. [Classes Overview](#classes-overview)
6. [Unit testing](#unit-testing)
6. [Features and Assumptions](#features-and-assumptions)
7. [License](#license)

## Installation

```bash
git clone https://github.com/devoftheweb/memstore-eng.git
py --version
cd path/to/repo
```

## Usage

### 1) `Client` class

1. Start the Server: `py main.py`

2. Run a Client:

Use the `Client` class in the `client/client.py` file to connect to the server, send commands, and receive responses.

```python
from client.client import Client

client = Client()
client.connect()

# Sending a BEGIN command to create a transaction
response = client.send_command("BEGIN")
transaction_id = response['transaction_id']
print(f"Transaction started with ID: {transaction_id}")

# PUT command to add a key-value pair
response = client.send_command(f"PUT key1 value1 {transaction_id}")
print(response['status'])  # Output: {'status': 'Ok'}

# Disconnect
client.disconnect()
```

### 2) CLI

1. Navigate to project directory root
2. Run `python main.py`
3. Start the server by pressing `1`:
```bash
Main Menu:
1. Start Server
2. Connect Client
3. Exit
Select an option:
```
4. Open new shell, navigate to folder, `py main.py`, then press `2`
5. Example command flow in Client CLI:
```bash
BEGIN
PUT nameofkey value999 1
GET nameofkey 1
BEGIN 
PUT house large 2
PUT house small 2
ROLLBACK 2
DEL 2
COMMITALL
SHOWALL
```

![Starting server, connecting client](assets/server-host.png)

## Functionality 

- `BEGIN`: creates a `transaction_id`
- `PUT [key] [value] [id]`: adds a key
- `GET [key] [id]`: retrieves key value
- `ROLLBACK [id]`: rolls back key to prior value
- `DEL [id]`: deletes key from store
- `COMMIT [id]`: commit a transaction
- `COMMITALL`: commits all changes and transactions
- `SHOWALL`: prints all the keys/values and transaction id's currently in store

## File structure

```bash
client/: 
    client.py: Class for client connections.
    
server/:
    core/:
        server.py: Core server functionality.
        command_parser.py: Parse and validate client commands.
        
    caching/:
        caching_strategy.py:
        
    data_store/:
        concurrency/:
            locking.py: Locking mechanism
        sharding/:
            shard.py: Class representing a shard in sharding mechanism.
            sharding_manager.py:  Manages shards.
        transactions/:
            transaction.py: Handling individual transactions.
            transaction_mananger.py: Manage transactions.
        data_store.py: Main data store logic and operations.

tests/:
    data_store/:
        test_command_parser.py: Unit tests for the command parser class.
        test_data_store.py: Unit tests for the data store and transaction classes.
    
    server/:
        test_server.py: Unit tests for the server class.

main.py: CLI
```

## Classes Overview 

- `CommandParser`: Parses and validates client commands.
- `Client`: Used by clients to connect to the server, send commands, and receive responses.
- `Server`: Accepts client connections, reads commands, and dispatches them to the appropriate handlers.
- `Transaction`: Manages an individual transaction, including tracking changes and allowing commits and rollbacks.
- `Shard`: Represents a shard within the sharding mechanism.
- `ShardingManager`: Manages the shards in the system, distributing keys among shards, and retrieving the appropriate shard for a given key.
- `DataStore`: Manages the in-memory key-value store, supports basic CRUD operations, and controls transactions.

## Unit testing

```
cd tests
py data_store/test_data_store.py
py server/test_command_parser.py
py server/test_server.py
```

## Features and Assumptions 

- ✅ Concurrency Control: 2PL for Multiple Clients
- ✅ Transactional Consistency: Multi-Client
- ✅ Command Parsing
- ✅ Sharding
- ✅ LRU Caching
- ✅ Server-Client Architecture
- ✅ Modular codebase
- ✅ Unit testing
- ✅ UTF-8 Encoding

Assumptions made are:

In a production environment, we would have authentication, authorization, and other important features.

- **Single Machine Deployment**:
  - Implementation does not include authentication, encryption, or other security measures that would be necessary for a public-facing server.
- **In-Memory Storage**:
  - Data does not persist between server restarts. Speed is prioritized over persistence. In-memory storage allows for faster access times.

## License

This project is open source and available under the MIT License. 