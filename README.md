# Python Multi-threaded Chat Server

This project is a command-line based chat application built in Python. It demonstrates a deep, practical understanding of fundamental computer science concepts including **network programming (sockets)**, **concurrency (threading)**, and **application-level protocols**.

This is a classic "fundamentals" project that proves an engineer can build systems from the ground up, not just use existing frameworks.

---

## How It Works

The application consists of two main components:

1.  **`server.py`**: A central server that listens for incoming connections. When a new client connects, the server spawns a dedicated **thread** to handle all communication with that client. This multi-threaded architecture allows the server to manage multiple clients simultaneously without blocking.
2.  **`client.py`**: An application that users run to connect to the server. The client also uses two threads: one to continuously listen for incoming messages from the server and another to accept user input for sending messages.

The communication follows a simple custom protocol over TCP sockets.

---

## Core Concepts Demonstrated

-   **Computer Networking (Block 3):**
    -   **Sockets:** The project uses Python's `socket` library to establish TCP connections between the client and server, demonstrating the foundation of most internet communication.
    -   **Client-Server Architecture:** It implements the classic client-server model where a central server provides a service to multiple clients.
    -   **TCP/IP:** The application relies on the reliable, connection-oriented nature of TCP for message delivery.

-   **Operating Systems (Block 3):**
    -   **Concurrency & Multithreading:** The server's ability to handle multiple clients at once is achieved through `threading`. This showcases an understanding of how to manage concurrent operations, a critical skill for building scalable applications.
    -   **Synchronization:** While simple, the use of `threading.Lock()` when modifying shared data (the `clients` and `usernames` lists) demonstrates an awareness of race conditions and the need for synchronization primitives.

-   **Programming Fundamentals (Block 1):**
    -   **Object-Oriented Principles:** The code is structured logically into functions that handle specific responsibilities.
    -   **Exception Handling:** The code uses `try...except` blocks to gracefully handle network errors like a client disconnecting unexpectedly (`ConnectionResetError`).

---

## How to Run

You will need two separate terminal windows to run this application.

### 1. Start the Server

In your first terminal:

```bash
# Navigate to the project directory
cd python-chat-server

# Run the server script
python server.py
```

The server will start and print `Waiting for connections...`.

### 2. Start a Client

In your second terminal:

```bash
# Navigate to the project directory
cd python-chat-server

# Run the client script
python client.py
```

The client will ask for your username. Enter one and press Enter. You are now connected!

### 3. Start More Clients

To see the multi-threaded chat in action, open a third (or fourth!) terminal and run `python client.py` again. Each new client will connect to the server, and messages sent from any client will be broadcast to all others.
