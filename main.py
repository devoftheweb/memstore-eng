from server.core.server import Server
from client.client import Client
import threading


def start_server():
    """
    Starts the server in a new thread.

    Prints a message to indicate the server is starting and initiates the server.
    """
    print("Starting server...")
    server = Server()
    threading.Thread(target=server.start).start()


def connect_client():
    """
    Connects a client to the server and handles user input for commands.

    Prints a message to indicate the client is connecting.
    Continuously reads commands from the user until 'exit' is entered.
    """
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
    """
    Main function to control the program flow.

    Displays a menu for the user to either start the server, connect a client, or exit the program.
    """
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
