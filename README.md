# NetScope: Multi-Client TCP Communication System

NetScope is a Python-based networking project that demonstrates private communication between multiple clients and a central server using TCP sockets and multithreading.

The server receives messages from connected clients and can send private responses to individual clients without exposing their messages to other connected clients.

## Features

- **TCP Communication:** Reliable communication using TCP sockets.
- **Multi-Client Support:** Handles multiple clients simultaneously.
- **Multithreading:** Manages each client connection using separate threads.
- **Private Messaging:** Client messages are received by the server without being broadcast to other clients.
- **Server-to-Client Communication:** The server can send messages to specific clients.
- **Client Isolation:** Clients do not receive other clients' messages or connection notifications.
- **Connection Management:** Supports client disconnection and server shutdown.

## Technologies Used

- Python 3
- TCP/IP Networking
- Socket Programming
- Multithreading

## Project Structure

```text
NetScope/
├── server.py
├── client.py
├── README.md
└── .gitignore
```

To connect multiple clients, open additional terminals and run the client program in each terminal.

## Server Commands

| Command | Description |
|---|---|
| `/list` | Displays connected client IDs on the server terminal. |
| `/msg ID message` | Sends a private message to a specific client. |
| `/all message` | Broadcasts a message to all connected clients. |
| `/quit` | Shuts down the server. |

### Example

To send a private message to Client 2, enter the following in the server terminal:

```text
/msg 2 Hello! Your request has been received.
```

Only Client 2 will receive the message.

## How It Works

1. The server creates a TCP socket and listens for incoming connections.
2. Clients connect to the server using its IP address and port number.
3. The server assigns a unique ID to each connected client.
4. Each client communicates with the server through its TCP connection.
5. The server receives and processes messages from individual clients.
6. The server can send private responses to specific clients using their assigned IDs.
7. Multithreading allows the server to handle multiple client connections concurrently.

## Learning Objectives

This project demonstrates the fundamentals of:

- Client-server architecture
- TCP socket programming
- IP addresses and port numbers
- Concurrent client handling
- Thread-based network programming
- Private message routing
- Connection establishment and termination

## Future Enhancements

- Username-based client identification
- Client authentication
- Encrypted communication using TLS
- Message history and logging
- Graphical user interface
- File transfer between clients and the server

## Author

**Mohammed Akmal**

B.Tech Computer Science and Engineering  
Puducherry Technological University

## License

This project is intended for educational purposes and for learning computer networking concepts.
