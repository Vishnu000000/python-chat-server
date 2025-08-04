import socket
import threading

def receive_messages(client_socket):
    """
    This function runs in a thread and continuously listens for messages
    from the server.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'GET_USERNAME':
                # The server is asking for our username
                client_socket.send(username.encode('utf-8'))
            else:
                # Print any other message received from the server
                print(message)
        except (ConnectionResetError, ConnectionAbortedError):
            # The connection to the server was lost
            print("Disconnected from the server.")
            client_socket.close()
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()
            break

def send_messages(client_socket):
    """
    This function runs in a thread and waits for the user to type a message,
    then sends it to the server.
    """
    while True:
        try:
            message = input("")
            # Prepend the username to the message for identification
            full_message = f"{username}: {message}"
            client_socket.send(full_message.encode('utf-8'))
        except EOFError: # Happens on Ctrl+D
            print("You have left the chat.")
            client_socket.close()
            break
        except Exception as e:
            print(f"An error occurred while sending: {e}")
            client_socket.close()
            break

# --- Main Execution ---
if __name__ == "__main__":
    # Get the username from the user
    username = input("Enter your username: ")

    # Create a TCP socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # --- Configuration ---
    # The server's IP address and port to connect to
    HOST = '127.0.0.1'
    PORT = 65432

    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to chat server as {username}.")

        # Start a thread for receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        # Start a thread for sending messages
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()
    
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")
