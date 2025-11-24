# server.py
# Chat server implementing both TCP and UDP protocols

import socket
import threading
import time
from config import *

class ChatServer:
    def __init__(self):
        # ==== SOCKET PROGRAMMING CONCEPT ====
        # Creating sockets - endpoints for network communication
        
        # TCP Socket: SOCK_STREAM = connection-oriented, reliable
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # AF_INET = IPv4, SOCK_STREAM = TCP protocol
        
        # UDP Socket: SOCK_DGRAM = connectionless, unreliable but fast
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # SOCK_DGRAM = UDP protocol (datagram-based)
        
        # Store connected clients: {socket: username}
        self.clients = {}
        self.clients_lock = threading.Lock()  # Thread-safe access to shared data
        
    def start(self):
        """Start both TCP and UDP servers"""
        
        # ==== BINDING CONCEPT ====
        # Binding associates a socket with a specific IP address and port number
        # This tells the OS: "route packets for this port to this socket"
        
        self.tcp_socket.bind((HOST, TCP_PORT))
        self.udp_socket.bind((HOST, UDP_PORT))
        
        # ==== TCP LISTENING CONCEPT ====
        # listen() puts the socket in "server mode" - ready to accept connections
        # Parameter 5 = backlog queue size (max pending connections)
        self.tcp_socket.listen(5)
        
        print(f"🚀 Chat Server Started!")
        print(f"📡 TCP Server listening on {HOST}:{TCP_PORT}")
        print(f"📡 UDP Server listening on {HOST}:{UDP_PORT}")
        print(f"\n{'='*50}")
        print("Network Concepts Demonstrated:")
        print("1. TCP: Reliable, connection-oriented (chat messages)")
        print("2. UDP: Fast, connectionless (presence updates)")
        print("3. Multi-threading: Concurrent client handling")
        print("4. Client-Server Architecture")
        print(f"{'='*50}\n")
        
        # Start UDP listener in separate thread
        udp_thread = threading.Thread(target=self.handle_udp, daemon=True)
        udp_thread.start()
        
        # Start accepting TCP connections
        self.accept_connections()
    
    def accept_connections(self):
        """Accept incoming TCP connections (main server loop)"""
        while True:
            try:
                # ==== TCP THREE-WAY HANDSHAKE ====
                # accept() blocks until a client connects
                # When client calls connect(), TCP does:
                # 1. Client -> Server: SYN
                # 2. Server -> Client: SYN-ACK
                # 3. Client -> Server: ACK
                # Then accept() returns the established connection
                
                client_socket, address = self.tcp_socket.accept()
                print(f"🔌 New TCP connection from {address}")
                
                # ==== MULTI-THREADING CONCEPT ====
                # Create a new thread for each client to handle concurrent connections
                # This allows multiple clients to chat simultaneously
                client_thread = threading.Thread(
                    target=self.handle_tcp_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                print(f" Error accepting connection: {e}")
    
    def handle_tcp_client(self, client_socket, address):
        """Handle individual TCP client (chat messages)"""
        username = None
        
        try:
            # First message should be the username
            username = client_socket.recv(TCP_BUFFER).decode(ENCODING)
            
            # Store client in thread-safe manner
            with self.clients_lock:
                self.clients[client_socket] = username
            
            print(f" User '{username}' joined from {address}")
            
            # Broadcast join message to all clients
            join_msg = f"[SERVER] {username} joined the chat!"
            self.broadcast_tcp(join_msg, exclude=client_socket)
            
            # ==== TCP RELIABLE TRANSMISSION ====
            # TCP guarantees: delivery, order, error-checking
            # recv() blocks until data arrives
            while True:
                message = client_socket.recv(TCP_BUFFER).decode(ENCODING)
                
                if not message:
                    # Empty message means client disconnected gracefully
                    break
                
                # Format and broadcast message
                formatted_msg = f"[{username}] {message}"
                print(f"{formatted_msg}")
                self.broadcast_tcp(formatted_msg, exclude=client_socket)
                
        except ConnectionResetError:
            print(f"{username or address} disconnected abruptly")
        except Exception as e:
            print(f"Error with client {username or address}: {e}")
        finally:
            # Clean up
            with self.clients_lock:
                if client_socket in self.clients:
                    username = self.clients.pop(client_socket)
            
            client_socket.close()
            
            if username:
                leave_msg = f"[SERVER] {username} left the chat."
                print(f"{leave_msg}")
                self.broadcast_tcp(leave_msg)
    
    def broadcast_tcp(self, message, exclude=None):
        """Send message to all connected TCP clients"""
        with self.clients_lock:
            dead_sockets = []
            
            for client_socket in self.clients:
                if client_socket != exclude:
                    try:
                        # ==== TCP SEND CONCEPT ====
                        # send() transmits data over established TCP connection
                        # TCP handles: segmentation, acknowledgment, retransmission
                        client_socket.send(message.encode(ENCODING))
                    except:
                        # Mark for removal if send fails
                        dead_sockets.append(client_socket)
            
            # Remove dead connections
            for sock in dead_sockets:
                self.clients.pop(sock, None)
    
    def handle_udp(self):
        """Handle UDP messages (presence, status, typing indicators)"""
        print("UDP handler started for presence updates\n")
        
        while True:
            try:
                # ==== UDP DATAGRAM RECEPTION ====
                # recvfrom() receives one complete datagram (packet)
                # UDP doesn't establish connections - each packet is independent
                # Returns: (data, sender_address)
                
                data, address = self.udp_socket.recvfrom(UDP_BUFFER)
                message = data.decode(ENCODING)
                
                # ==== UDP CHARACTERISTICS ====
                # - No connection setup (faster)
                # - No delivery guarantee (packets may be lost)
                # - No ordering guarantee (packets may arrive out of order)
                # - Lower overhead (no ACKs, retransmissions)
                
                # Parse UDP message format: "TYPE:USERNAME:DATA"
                parts = message.split(':', 2)
                if len(parts) >= 2:
                    msg_type = parts[0]
                    username = parts[1]
                    data = parts[2] if len(parts) > 2 else ''
                    
                    # Handle different UDP message types
                    if msg_type == UDP_MSG_TYPES['JOIN']:
                        print(f"UDP: {username} is online ({address})")
                    
                    elif msg_type == UDP_MSG_TYPES['LEAVE']:
                        print(f"UDP: {username} went offline")
                    
                    elif msg_type == UDP_MSG_TYPES['TYPING']:
                        print(f"UDP: {username} is typing...")
                        # In a real app, broadcast this to other clients
                    
                    elif msg_type == UDP_MSG_TYPES['HEARTBEAT']:
                        # Periodic heartbeat to detect disconnections
                        print(f"UDP: Heartbeat from {username}")
                    
                    elif msg_type == UDP_MSG_TYPES['STATUS']:
                        print(f"UDP: {username} status changed to '{data}'")
                
            except Exception as e:
                print(f"UDP Error: {e}")
    
    def shutdown(self):
        """Gracefully shutdown the server"""
        print("\nShutting down server...")
        
        # Close all client connections
        with self.clients_lock:
            for client_socket in list(self.clients.keys()):
                client_socket.close()
        
        # Close server sockets
        self.tcp_socket.close()
        self.udp_socket.close()
        print("Server shutdown complete")

# Main execution
if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()