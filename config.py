# config.py
# Shared configuration for the chat application

# Server configuration
HOST = '127.0.0.1'  # Localhost - use '0.0.0.0' to accept connections from any IP
TCP_PORT = 5555     # Port for TCP chat messages
UDP_PORT = 5556     # Port for UDP presence/status updates

# Message encoding
ENCODING = 'utf-8'

# Buffer sizes
TCP_BUFFER = 1024   # TCP receive buffer size
UDP_BUFFER = 512    # UDP datagram size (smaller for quick updates)

# UDP message types (for demonstration of different UDP use cases)
UDP_MSG_TYPES = {
    'JOIN': 'USER_JOIN',
    'LEAVE': 'USER_LEAVE',
    'TYPING': 'TYPING',
    'HEARTBEAT': 'HEARTBEAT',
    'STATUS': 'STATUS_UPDATE'
}

# Status options
STATUS_OPTIONS = ['Available', 'Away', 'Busy', 'Do Not Disturb']