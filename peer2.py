import socket
import threading
import select

# Global variables
active_peers = set()
active_peers_lock = threading.Lock()

def send_message(target_ip, target_port, my_ip, my_port, team_name, message):
    """Send a message to a specified peer."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, target_port))
            s.sendall(f"{my_ip}:{my_port} {team_name} {message}".encode())
    except Exception as e:
        print(f"⚠️ Error sending message to {target_ip}:{target_port} - {e}")

def handle_client(client_socket):
    """Handle incoming messages from a peer."""
    try:
        message = client_socket.recv(1024).decode().strip()
        if message:
            parts = message.split(" ", 2)
            if len(parts) == 3:
                sender_info, team_name, msg = parts
                sender_ip, sender_port = sender_info.split(":")
                sender_port = int(sender_port)
                
                with active_peers_lock:
                    if msg.lower() == "exit":
                        active_peers.discard((sender_ip, sender_port))
                        print(f"❌ Peer {sender_ip}:{sender_port} has disconnected.")
                    else:
                        active_peers.add((sender_ip, sender_port))
                        print(f"📩 [MESSAGE RECEIVED] From {team_name} ({sender_ip}:{sender_port}): {msg}")
    except Exception as e:
        print(f"⚠️ Error handling client message: {e}")
    finally:
        client_socket.close()

def server_listener(my_ip, my_port):
    """Server function to listen for incoming messages."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((my_ip, my_port))
        server_socket.listen(5)
        print(f"🚀 Server listening on port {my_port}")
        
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()

def query_peers():
    """Query and display the list of connected peers."""
    with active_peers_lock:
        if active_peers:
            print("Connected Peers:")
            for peer in active_peers:
                print(f"{peer[0]}:{peer[1]}")
        else:
            print("No connected peers.")

def connect_to_peers(my_ip, my_port, team_name):
    """Connect to all known active peers and establish a persistent connection."""
    with active_peers_lock:
        for peer in active_peers.copy():
            target_ip, target_port = peer
            send_message(target_ip, target_port, my_ip, my_port, team_name, "connect")
            print(f"🔗 Connected to peer {target_ip}:{target_port}")

def main():
    """Main function to handle user inputs and start the server."""
    team_name = input("Enter your name: ")
    my_port = int(input("Enter your port number: "))
    my_ip = "127.0.0.1"  # Running on localhost
    
    threading.Thread(target=server_listener, args=(my_ip, my_port), daemon=True).start()
    
    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            target_ip = input("Enter recipient’s IP address: ")
            target_port = int(input("Enter recipient’s port number: "))
            message = input("Enter your message: ")
            send_message(target_ip, target_port, my_ip, my_port, team_name, message)
        elif choice == "2":
            query_peers()
        elif choice == "3":
            connect_to_peers(my_ip, my_port, team_name)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
