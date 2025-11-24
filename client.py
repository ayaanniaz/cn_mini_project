# client.py
# Chat client implementing both TCP and UDP protocols

import socket
import threading
import time
import sys
from config import *

class ChatClient:
    def __init__(self, username):
        self.username = username
        
        # ==== CREATING CLIENT SOCKETS ====
        # TCP socket for reliable chat messages
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # UDP socket for quick presence/status updates
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.running = False
        
    def connect(self):
        """Connect to the chat server"""
        try:
            # ==== TCP CONNECTION ESTABLISHMENT ====
            # connect() initiates the TCP three-way handshake:
            # 1. Client sends SYN to server
            # 2. Server responds with SYN-ACK
            # 3. Client sends ACK
            # After this, connection is ESTABLISHED
            
            print(f"🔌 Connecting to server at {HOST}:{TCP_PORT}...")
            self.tcp_socket.connect((HOST, TCP_PORT))
            print("TCP connection established!")
            
            # Send username as first message
            self.tcp_socket.send(self.username.encode(ENCODING))
            
            # ==== UDP - NO CONNECTION ====
            # UDP doesn't have connect() in the traditional sense
            # It's connectionless - we just send datagrams to an address
            # But we can use connect() to set a default destination
            self.udp_socket.connect((HOST, UDP_PORT))
            
            self.running = True
            
            # Send UDP presence announcement
            self.send_udp_message(UDP_MSG_TYPES['JOIN'], self.username)
            
            print(f"\n{'='*50}")
            print("Network Concepts You're Using:")
            print("• TCP: Your chat messages (reliable delivery)")
            print("• UDP: Your status updates (fast, may be lost)")
            print("• Ports: TCP:{} for chat, UDP:{} for presence".format(TCP_PORT, UDP_PORT))
            print(f"{'='*50}\n")
            
            # Start receiver thread for incoming TCP messages
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            # Start heartbeat thread for UDP
            heartbeat_thread = threading.Thread(target=self.send_heartbeat, daemon=True)
            heartbeat_thread.start()
            
            # Start sending messages
            self.send_messages()
            
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?")
        except Exception as e:
            print(f"Connection error: {e}")
    
    def receive_messages(self):
        """Receive messages from server (TCP)"""
        while self.running:
            try:
                # ==== TCP RECEIVING ====
                # recv() blocks until data arrives
                # TCP ensures: data arrives in order, no duplicates, no corruption
                message = self.tcp_socket.recv(TCP_BUFFER).decode(ENCODING)
                
                if message:
                    print(f"\n{message}")
                    print(f"[You] ", end='', flush=True)
                else:
                    # Empty message means server closed connection
                    print("\nDisconnected from server")
                    self.running = False
                    break
                    
            except Exception as e:
                if self.running:
                    print(f"\nError receiving message: {e}")
                break
    
    def send_messages(self):
        """Send messages to server (TCP)"""
        print("💬 You can start chatting! Type your message and press Enter.")
        print("Commands: '/status <status>' to change status, '/quit' to exit\n")
        
        while self.running:
            try:
                message = input(f"[You] ")
                
                if not message:
                    continue
                
                # Handle commands
                if message.startswith('/quit'):
                    print("Leaving chat...")
                    self.disconnect()
                    break
                
                elif message.startswith('/status'):
                    # Change status via UDP (fast, non-critical update)
                    parts = message.split(' ', 1)
                    if len(parts) > 1:
                        status = parts[1]
                        self.send_udp_message(UDP_MSG_TYPES['STATUS'], self.username, status)
                        print(f"Status changed to: {status}")
                    else:
                        print(f"Usage: /status <{'/'.join(STATUS_OPTIONS)}>")
                    continue
                
                elif message.startswith('/typing'):
                    # Simulate typing indicator via UDP
                    self.send_udp_message(UDP_MSG_TYPES['TYPING'], self.username)
                    print("Typing indicator sent via UDP")
                    continue
                
                # ==== TCP SENDING ====
                # send() transmits data reliably
                # TCP handles: packet loss, reordering, flow control, congestion control
                self.tcp_socket.send(message.encode(ENCODING))
                
            except KeyboardInterrupt:
                print("\nInterrupted. Leaving chat...")
                self.disconnect()
                break
            except Exception as e:
                print(f"Error sending message: {e}")
                break
    
    def send_udp_message(self, msg_type, username, data=''):
        """Send UDP message for presence/status updates"""
        try:
            # ==== UDP SENDING ====
            # sendto() sends a datagram without establishing connection
            # Format: "TYPE:USERNAME:DATA"
            # UDP characteristics:
            # - Sent immediately (no connection setup delay)
            # - May be lost (no retransmission)
            # - May arrive out of order
            # - Lower overhead than TCP
            
            message = f"{msg_type}:{username}:{data}"
            self.udp_socket.send(message.encode(ENCODING))
            
        except Exception as e:
            print(f"UDP send error: {e}")
    
    def send_heartbeat(self):
        """Send periodic UDP heartbeat to server"""
        # ==== UDP USE CASE: HEARTBEAT ====
        # Heartbeats are perfect for UDP because:
        # - Sent frequently (every 5 seconds)
        # - Loss of one heartbeat is acceptable
        # - Low overhead is important
        # - Speed > Reliability
        
        while self.running:
            time.sleep(5)  # Send heartbeat every 5 seconds
            if self.running:
                self.send_udp_message(UDP_MSG_TYPES['HEARTBEAT'], self.username)
    
    def disconnect(self):
        """Disconnect from server"""
        if self.running:
            self.running = False
            
            # Send leave notification via UDP
            self.send_udp_message(UDP_MSG_TYPES['LEAVE'], self.username)
            
            # ==== CLOSING CONNECTIONS ====
            # TCP: close() initiates connection teardown (FIN packets)
            # UDP: close() just releases the socket (no connection to close)
            
            try:
                self.tcp_socket.close()
            except:
                pass
            
            try:
                self.udp_socket.close()
            except:
                pass
            
            print("✅ Disconnected from server")
            sys.exit(0)

# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("NETWORK CHAT CLIENT")
    print("=" * 50)
    
    username = input("Enter your username: ").strip()
    
    if not username:
        print("Username cannot be empty!")
        sys.exit(1)
    
    client = ChatClient(username)
    client.connect()