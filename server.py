import socket
import sys


def start_server(port_number):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port_number))
    server_socket.listen(5)

    print(f"Server started on port {port_number}. Waiting for a connection...")

    conn, addr = server_socket.accept()
    print(f"Client connected from {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data.strip().lower() == "terminate":
            print("Client disconnected.")
            break
        print(f"Client: {data}")

    conn.close()
    server_socket.close()
    print("Server shutting down.")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
