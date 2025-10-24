import socket
import threading
import sys

class ClientThread(threading.Thread):
    """Thread to handle individual client connections"""
    
    def __init__(self, client_socket, client_number):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_number = client_number
        
    def run(self):
        """Handle client communication"""
        try:
            print(f"Client {self.client_number} Connected")
            
            # Keep connection alive and echo messages
            while True:
                # Receive message from client
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                print(f"Received from client {self.client_number}: {message}")
                
                # Send echo back to client
                self.client_socket.send(message.encode('utf-8'))
                
        except Exception as e:
            print(f"Error with client {self.client_number}: {e}")
        finally:
            print(f"Client {self.client_number} Disconnected")
            self.client_socket.close()


def main():
    # Default port
    port = 1222
    
    # Parse command line arguments
    if len(sys.argv) != 2:
        print("Considering Port 1222", file=sys.stderr)
    else:
        port = int(sys.argv[1])
    
    # Create server socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))
        server_socket.listen(5)
        print(f"Server started on port {port}")
        print("Waiting for clients...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    
    client_count = 0
    
    # Accept clients in infinite loop
    while True:
        try:
            client_socket, address = server_socket.accept()
            client_count += 1
            
            # Create and start new thread for client
            client_thread = ClientThread(client_socket, client_count)
            client_thread.start()
            
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            break
        except Exception as e:
            print(f"Error accepting client: {e}")
    
    server_socket.close()


if __name__ == "__main__":
    main()
