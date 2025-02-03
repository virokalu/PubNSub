import socket
import sys


def start_client(server_ip_address, server_port_number):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, server_port_number))
    print(f"Connected to server at {server_ip_address}:{server_port_number}")

    while True:
        message = input("Enter message: ")
        client_socket.sendall(message.encode())
        if message.strip().lower() == "terminate":
            break

    client_socket.close()
    print("Client disconnected.")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <SERVER_PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    start_client(server_ip, server_port)
