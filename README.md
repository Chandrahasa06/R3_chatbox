# 📌 Peer-to-Peer Messaging System

## Team R3
## Members
1.Rachakonda Chandrahasa (230001065) <br>
2.Reena Meena (230003057) <br>
3.Rahul Kumar (230001066) <br>

## 🔷 Overview
This is a simple **Peer-to-Peer (P2P) networking system** that allows users to exchange messages over a local network (LAN) or across predefined static peers. The system maintains a list of active peers, verifies connections, and automatically removes inactive nodes.

### 🚀 Features
- **P2P Communication**: Send and receive messages directly between peers.
- **Active Peer Discovery**: Detects and maintains a list of active peers.
- **Automatic Peer Cleanup**: Removes inactive peers from the list.
- **Connection to Static Peers**: Allows predefined nodes to establish connections automatically.
- **Threaded Server**: Handles multiple incoming connections concurrently.
- **Interactive Menu**: Provides an easy-to-use console interface.

---
## 🛠 Installation
### Prerequisites
Ensure you have **Python 3.x** installed. You can check using:
```bash
python --version
```

### Running the Peer Program
1. Clone this repository or copy the `peer.py` file.
2. Open a terminal and navigate to the script's directory.
3. Run the script using:
   ```bash
   python peer.py
   ```
4. Enter your **name** and **port number** when prompted.
5. The server will start listening for incoming connections.

---
## 🔹 Usage
### **1️⃣ Sending Messages**
- Choose **Option 1** from the menu.
- Enter the recipient's **IP address** and **port**.
- Type your message and send it.

### **2️⃣ Viewing Active Peers**
- Choose **Option 2** to see currently active peers.
- Inactive peers will be automatically removed.

### **3️⃣ Connecting to Known Peers**
- Choose **Option 3** to send connection requests to all known peers.
- Peers that acknowledge the connection will be marked as **active**.

### **4️⃣ Exiting the Program**
- Choose **Option 0** to exit and shut down your server.

---
## 📜 How It Works
### **🔹 Server & Client**
- The script starts a **server** that listens for incoming messages.
- When a message is received, it extracts **sender details** and stores them in the active peer list.

### **🔹 Peer Management**
- Peers are tracked in a dictionary `{(IP, port): name}`.
- If a peer sends an `exit` message, it is removed from the list.
- Every connection attempt is verified, and **inactive peers are removed** automatically.

### **🔹 Static Peers**
- The system initializes connections with predefined **static peers**.
- This ensures a baseline connectivity in a distributed network.

---
## 📌 Example Walkthrough
### **📍 Peer 1 (IP: 192.168.1.10, Port: 5000)**
```plaintext
TEAM R3
👤 Enter your name: Alice
🔢 Choose your port number: 5000
🟢 Server running on port 5000...
🔹 ==== Menu ==== 🔹
1️⃣ Send a message
2️⃣ Show active peers
3️⃣ Connect to known peers
0️⃣ Exit
Enter your choice: 1
📤 Enter recipient IP: 192.168.1.20
📤 Enter recipient port: 5001
💬 Message: Hello, Peer!
✅ Message sent to 192.168.1.20:5001
```

### **📍 Peer 2 (IP: 192.168.1.20, Port: 5001)**
```plaintext
TEAM R3
👤 Enter your name: Bob
🔢 Choose your port number: 5001
🟢 Server running on port 5001...
📩 [Alice (192.168.1.10:5000)]: Hello, Peer!
```

---
## 📌 License
This project is open-source and free to use for learning and development purposes. 🚀
