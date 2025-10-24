# 🌐 Network Chat Application

A Python chat app demonstrating fundamental networking concepts using **TCP** (reliable messages) and **UDP** (fast status updates).

---

## 🎯 What It Does

- Real-time multi-user chat using **TCP** protocol
- Fast presence updates using **UDP** protocol
- Demonstrates client-server architecture and socket programming
- Educational code with detailed comments explaining networking concepts

---

## 📚 Network Concepts Covered

- **TCP**: Connection-oriented, reliable delivery (chat messages)
- **UDP**: Connectionless, fast transmission (status updates, heartbeats)
- **Socket Programming**: Creating, binding, connecting sockets
- **Multi-threading**: Handling multiple concurrent clients
- **Client-Server Architecture**: Server manages connections and broadcasts messages

---

## 🛠️ Requirements

- Python 3.6+
- No external dependencies (uses standard library only)

---

## 🚀 Quick Start

### 1. Start the Server
```bash
python server.py
```

### 2. Start Client(s) (in separate terminals)
```bash
python client.py
```

### 3. Enter username and start chatting!

---

## 💬 Client Commands

- `<message>` - Send chat message (TCP)
- `/status <status>` - Change status (UDP)
- `/typing` - Send typing indicator (UDP)
- `/quit` - Exit chat

**Example:**
```bash
[You] Hello everyone!
[You] /status Away
[You] /quit
```

---

## 📁 Project Files

- `config.py` - Configuration (ports, buffer sizes)
- `server.py` - Server handling TCP + UDP
- `client.py` - Client using both protocols

---

## 🌐 Chat with Remote Computers

### Enable LAN Access:

1. **In `config.py`, change:**
   ```python
   HOST = '0.0.0.0'  # Instead of '127.0.0.1'
   ```

2. **Find server's IP address:**
   - Linux/Mac: `ifconfig` or `ip addr`
   - Windows: `ipconfig`

3. **Clients connect using server's IP:**
   - Modify `HOST` in client's `config.py` to server's IP
   - Example: `HOST = '192.168.1.100'`

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Start server before clients |
| "Address already in use" | Wait 30 seconds or change ports in `config.py` |
| Can't connect from other PCs | Set `HOST = '0.0.0.0'` and check firewall |

---

## 🎓 Learning Tips

- Read code comments - they explain each networking concept
- Try running multiple clients to see concurrent connections
- Watch server console to see UDP messages (status, heartbeats)
- Experiment with TCP vs UDP by modifying the code

---

## 🔧 Extension Ideas

- Add encryption (TLS/SSL)
- Private messaging between users
- File transfer over TCP
- GUI interface (Tkinter/PyQt)
- Message history/database
- Authentication system

---

## 📖 Key Takeaways

**TCP vs UDP:**
- TCP = Reliable, ordered, slower (use for critical data)
- UDP = Fast, unreliable, lower overhead (use for real-time updates)

**Real-world usage:**
- Video calls: UDP (audio/video) + TCP (chat)
- Online games: UDP (positions) + TCP (game state)
- This app: TCP (messages) + UDP (presence)

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the server terminal for graceful shutdown.

---

**Happy Learning! 🚀**
