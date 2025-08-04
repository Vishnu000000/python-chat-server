# File: server.py
# This is the core of the chat application. It's a server that listens for
# incoming connections and uses threading to handle multiple clients at once.

import socket
import threading

# --- Configuration ---
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MAX_CLIENTS = 10

# --- State ---
# Lists to keep track of connected clients and their usernames
clients = []
usernames = []

# --- Functions ---

def broadcast(message, _client):
    """
    Sends a message to all connected clients except the sender.
    """
    for client in clients:
        # We don't want to send the message back to the client who sent it
        if client != _client:
            try:
                client.send(message)
            except:
                # If sending fails, assume the client has disconnected
                print(f"Failed to send message. Removing client.")
                remove_client(client)

def handle_client(client):
    """
    This function runs in a separate thread for each client.
    It handles receiving messages from a client and broadcasting them.
    """
    while True:
        try:
            # Receive message from a client (up to 1024 bytes)
            message = client.recv(1024)
            if not message:
                # If no message is received, the client has likely disconnected
                remove_client(client)
                break
            
            # Broadcast the received message to all other clients
            broadcast(message, client)
        except (ConnectionResetError, BrokenPipeError):
            # Handle cases where the client connection is abruptly lost
            print(f"Client disconnected unexpectedly.")
            remove_client(client)
            break

def remove_client(client):
    """
    Removes a client from our lists and closes their connection.
    This function is synchronized with a lock to prevent race conditions
    when multiple threads try to modify the lists at the same time.
    """
    with threading.Lock():
        if client in clients:
            # Find the index of the client to remove their username as well
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            print(f"{username} has left the chat.")
            broadcast(f'{username} has left the chat.'.encode('utf-8'), None) # Inform others
            usernames.remove(username)

def start_server():
    """
    The main function to start the server, listen for connections,
    and spawn threads for new clients.
    """
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    # Start listening for incoming connections
    server_socket.listen(MAX_CLIENTS)

    print(f"Server started on {HOST}:{PORT}. Waiting for connections...")

    while True:
        try:
            # Accept a new connection
            # This is a blocking call; it waits until a client connects
            client_socket, address = server_socket.accept()
            print(f"New connection from {address}")

            # Ask the new client for their username
            client_socket.send('GET_USERNAME'.encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8')
            
            # Add the new client and username to our lists
            with threading.Lock():
                usernames.append(username)
                clients.append(client_socket)

            print(f"Username of the new client is {username}")
            broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)
            client_socket.send('Connected to the server!'.encode('utf-8'))

            # Start a new thread to handle this client
            # The target is the function that will run in the new thread
            # The args tuple contains the arguments to pass to the target function
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
        
        except KeyboardInterrupt:
            print("\nServer is shutting down.")
            for client in clients:
                client.close()
            server_socket.close()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            for client in clients:
                client.close()
            server_socket.close()
            break

# --- Main Execution ---
if __name__ == "__main__":
    start_server()
