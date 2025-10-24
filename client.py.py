import socket
import sys


def reverse_string(s):
    """Reverse the order of words in a string"""
    words = s.split()
    reversed_words = words[::-1]
    return ' '.join(reversed_words)


def main():
    # Default host and port
    host = 'localhost'
    port = 1222
    
    # Parse command line arguments
    if len(sys.argv) != 3:
        print("Considering localhost and Port 1222", file=sys.stderr)
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
    
    # Create socket and connect to server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")
        print("Type your messages (Ctrl+C to quit):")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)
    
    # Send and receive messages
    try:
        while True:
            # Read input from user
            message = input()
            
            if not message:
                continue
            
            # Send message to server
            client_socket.send(f"{message}\n".encode('utf-8'))
            
            # Receive echo from server
            response = client_socket.recv(1024).decode('utf-8').strip()
            
            # Reverse the words and display
            reversed_response = reverse_string(response)
            print(f"Received from Server: {reversed_response}")
            
    except KeyboardInterrupt:
        print("\nDisconnecting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
