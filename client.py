import socket
import sys
import threading


def receive_messages(client_socket):
    while True:
        try:
            messageReceived = client_socket.recv(1024).decode()
            if not messageReceived:
                break  # Exit if the server is closed
            print(f"\nReceived: {messageReceived}")  # Display received message
        except:
            break  # Exit on error


def start_client(server_ip_address, server_port_number, client_type, topic):
    global message
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip_address, server_port_number))

    # Send the role (PUBLISHER / SUBSCRIBER) to the server
    client_socket.send(f"{client_type} {topic}".encode())

    if client_type == "SUBSCRIBER":
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            if client_type == "SUBSCRIBER":
                message = input()  # Get user input
            elif client_type == "PUBLISHER":
                message = input(f"Enter message - {topic} : ")  # Get user input
            client_socket.send(message.encode())  # Send message to server
            if message.lower() == "terminate":
                break  # Exit loop if user types "terminate"
    except KeyboardInterrupt:
        print("\nClient disconnected.")

    client_socket.close()  # Close socket on exit


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python client.py <server_ip> <server_port> <role> <topic>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4]

    if role not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Invalid role! Choose PUBLISHER or SUBSCRIBER.")
        sys.exit(1)

    start_client(server_ip, server_port, role, topic)
