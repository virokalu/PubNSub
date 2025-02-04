import socket
import sys
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break  # Exit if the server is closed
            print(f"\nReceived: {message}")  # Display received message
        except:
            break  # Exit on error


def start_client(server_ip_address, server_port_number, role):
    global message
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, server_port_number))

    # Send the role (PUBLISHER / SUBSCRIBER) to the server
    client_socket.send(role.encode())

    if role == "SUBSCRIBER":
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            if role == "SUBSCRIBER":
                message = input()  # Get user input
            elif role == "PUBLISHER":
                message = input("Enter message: ")  # Get user input
            client_socket.send(message.encode())  # Send message to server
            if message.lower() == "terminate":
                break  # Exit loop if user types "terminate"
    except KeyboardInterrupt:
        print("\nClient disconnected.")

    client_socket.close()  # Close socket on exit


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python client.py <server_ip> <server_port> <role>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Invalid role! Choose PUBLISHER or SUBSCRIBER.")
        sys.exit(1)

    start_client(server_ip, server_port, role)
