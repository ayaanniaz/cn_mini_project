# cn_mini_project

# Anonymous Multi-Chat Application (Python Version)

A multi-threaded client-server chat application built with Python.

## Features

- **Multi-threaded Server**: Handles multiple clients simultaneously using threading
- **Echo Functionality**: Server echoes messages back to clients
- **Word Reversal**: Client reverses the order of words in received messages
- **Anonymous Communication**: Clients are identified by connection number
- **Real-time Messaging**: Instant message delivery

## Architecture

### Server (`server.py`)
- Creates a TCP socket and binds to specified port (default: 1222)
- Listens for incoming client connections
- Spawns a new thread for each connected client
- Echoes received messages back to the client
- Tracks connected clients with unique IDs

### Client (`client.py`)
- Connects to the server via TCP socket
- Reads user input from console
- Sends messages to server
- Receives echoed messages and reverses word order
- Displays reversed messages to user

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

No installation required! Just download the Python files:
- `server.py`
- `client.py`

## Usage

### 1. Start the Server

```bash
# Using default port (1222)
python server.py

# Using custom port
python server.py 5000
```

### 2. Start Client(s)

Open new terminal windows for each client:

```bash
# Using default host and port
python client.py

# Using custom host and port
python client.py localhost 5000
```

### 3. Send Messages

Type your message in the client terminal and press Enter. The server will echo it back, and the client will display it with words reversed.

**Example:**

```
Client Input: Hello World from Python
Server Echo: Hello World from Python
Client Output: Python from World Hello
```

## Example Session

**Terminal 1 (Server):**
```
$ python server.py
Considering Port 1222
Server started on port 1222
Waiting for clients...
Client 1 Connected
Received from client 1: Hello World
Received from client 1: This is a test
Client 2 Connected
Received from client 2: Another client here
```

**Terminal 2 (Client 1):**
```
$ python client.py
Considering localhost and Port 1222
Connected to server at localhost:1222
Type your messages (Ctrl+C to quit):
Hello World
Received from Server: World Hello
This is a test
Received from Server: test a is This
```

**Terminal 3 (Client 2):**
```
$ python client.py
Considering localhost and Port 1222
Connected to server at localhost:1222
Type your messages (Ctrl+C to quit):
Another client here
Received from Server: here client Another
```

## Code Structure

### server.py
- `ClientThread` class: Handles individual client connections
- `main()` function: Sets up server socket and accepts connections

### client.py
- `reverse_string()` function: Reverses word order in strings
- `main()` function: Connects to server and handles message exchange

## Error Handling

- Connection errors are caught and reported
- Keyboard interrupts (Ctrl+C) are handled gracefully
- Client disconnections are detected and logged
- Socket errors are caught and displayed

## Stopping the Application

- **Server**: Press `Ctrl+C` in the server terminal
- **Client**: Press `Ctrl+C` in the client terminal

## Technical Details

- **Protocol**: TCP (Transmission Control Protocol)
- **Architecture**: Client-Server with multi-threading
- **Default Port**: 1222
- **Buffer Size**: 1024 bytes
- **Encoding**: UTF-8

## Troubleshooting

**Port already in use:**
```
Error starting server: [Errno 98] Address already in use
```
Solution: Use a different port or kill the process using the port

**Connection refused:**
```
Error connecting to server: [Errno 111] Connection refused
```
Solution: Ensure the server is running before starting clients
