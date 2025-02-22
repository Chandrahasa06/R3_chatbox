import socket
import threading

class Peer:
    STATIC_PEERS = [("10.206.4.122", 1255), ("10.206.5.228", 6555)]
    
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.peers = {}  # Active peers stored as {(ip, port): name}
        
        # Start server in a separate thread
        threading.Thread(target=self.start_server, daemon=True).start()
        
        # Initialize connections with static peers
        self.initialize_static_peers()

    def start_server(self):
        """Start server to receive incoming messages."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", self.port))
        server_socket.listen(5)
        print(f"🟢 Server running on port {self.port}...")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        """Handle messages from a peer."""
        try:
            data = client_socket.recv(1024).decode()
            if data:
                sender_ip, sender_port, sender_name, message = data.split(" ", 3)
                sender_port = int(sender_port)

                if message.strip().lower() == "exit":
                    if (sender_ip, sender_port) in self.peers:
                        del self.peers[(sender_ip, sender_port)]
                        print(f"🔴 {sender_name} ({sender_ip}:{sender_port}) disconnected.")
                else:
                    self.peers[(sender_ip, sender_port)] = sender_name
                    print(f"📩 [{sender_name} ({sender_ip}:{sender_port})]: {message}")
                    
                    if message.strip().lower() == "connect":
                        self.send_message(sender_ip, sender_port, "connect_ack")
                    
                    if message.strip().lower() == "connect_ack":
                        print(f"✅ {sender_name} ({sender_ip}:{sender_port}) is now an active peer.")

            client_socket.close()
        except Exception as e:
            print(f"⚠️ Error handling client {addr}: {e}")

    def send_message(self, target_ip, target_port, message):
        """Send a message to another peer."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((target_ip, target_port))
            formatted_message = f"{socket.gethostbyname(socket.gethostname())} {self.port} {self.name} {message}"
            client_socket.sendall(formatted_message.encode())
            client_socket.close()

            if message.strip().lower() == "exit":
                if (target_ip, target_port) in self.peers:
                    del self.peers[(target_ip, target_port)]
                    print(f"🔴 Disconnected from {target_ip}:{target_port}.")
        except Exception:
            print(f"⚠️ Unable to send message to {target_ip}:{target_port}. Removing from active peers.")
            if (target_ip, target_port) in self.peers:
                del self.peers[(target_ip, target_port)]

    def verify_peers(self):
        """Check if known peers are still online."""
        inactive_peers = []
        for (ip, port) in list(self.peers.keys()):
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(2)
                test_socket.connect((ip, port))
                test_socket.close()
            except Exception:
                inactive_peers.append((ip, port))

        for peer in inactive_peers:
            del self.peers[peer]
            print(f"🔴 {peer[0]}:{peer[1]} removed due to inactivity.")

    def list_active_peers(self):
        """Show currently active peers."""
        self.verify_peers()
        
        if self.peers:
            print("\n🟢 Active Peers:")
            for (ip, port), name in self.peers.items():
                print(f"- {name} ({ip}:{port})")
        else:
            print("\n⚠️ No active peers available.")

    def connect_to_peers(self):
        """Send connection requests to all known peers."""
        self.verify_peers()

        if not self.peers:
            print("⚠️ No peers available for connection.")
            return

        for (ip, port) in list(self.peers.keys()):
            self.send_message(ip, port, "connect")

        print("✅ Connection requests sent to all active peers.")
    
    def initialize_static_peers(self):
        """Connect to predefined static peers."""
        for ip, port in self.STATIC_PEERS:
            self.send_message(ip, port, "connect")
        print("✅ Static peer connections attempted.")
    
    def menu(self):
        """Display menu options."""
        while True:
            print("\n🔹 ==== Menu ==== 🔹")
            print("1️⃣ Send a message")
            print("2️⃣ Query active peers")
            print("3️⃣ Connect to active peers")
            print("0️⃣ Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                target_ip = input("📤 Enter recipient IP: ")
                target_port = int(input("📤 Enter recipient port: "))
                message = input("💬 Message: ")
                self.send_message(target_ip, target_port, message)

            elif choice == "2":
                self.list_active_peers()

            elif choice == "3":
                self.connect_to_peers()

            elif choice == "0":
                print("👋 Shutting down...")
                break

            else:
                print("⚠️ Invalid option, try again.")

if __name__ == "__main__":
    print("** TEAM R3 **")
    name = input("👤 Enter your name: ")
    port = int(input("🔢 Choose your port number: "))
    peer = Peer(name, port)
    peer.menu()
