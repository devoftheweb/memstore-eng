from server.server import Server
from client.client import Client

def start_server():
    print("Starting server...")
    server = Server()
    server.start()

def connect_client():
    print("Connecting client...")
    client = Client()
    client.connect()
    while True:
        command_str = input("Enter command (or 'exit' to disconnect): ")
        if command_str.lower() == 'exit':
            client.disconnect()
            break
        response = client.send_command(command_str)
        print("Response:", response)

def main():
    while True:
        print("\nMain Menu:")
        print("1. Start Server")
        print("2. Connect Client")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            start_server()
        elif choice == '2':
            connect_client()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
