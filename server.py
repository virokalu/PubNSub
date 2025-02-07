import socket
import sys
import threading

# Stores connected clients categorized as Publishers or Subscribers
subscribers = {}
publishers = []
lock = threading.Lock()


def handle_client(client_socket, client_role, topic):
    global subscribers, publishers

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message or message.strip().lower() == "terminate":
                print(f"{client_role} disconnected.")
                break

            if client_role == "PUBLISHER":
                print(f"Publisher: {message}")
                broadcast_to_subscribers(message, topic)

            if client_role == "SUBSCRIBER":
                print(f"Subscriber: {message}")

        except ConnectionResetError:
            break

        except KeyboardInterrupt:
            print("\nClient disconnected.")

    # Remove the client when they disconnect
    with lock:
        if client_role == "SUBSCRIBER":
            subscribers[topic].remove(client_socket)
        elif client_role == "PUBLISHER":
            publishers.remove(client_socket)

    client_socket.close()


def broadcast_to_subscribers(message, topic):
    with lock:
        if topic in subscribers:
            for subscriber in subscribers[topic]:
                try:
                    subscriber.sendall(message.encode())
                except:
                    subscribers[topic].remove(subscriber)


def start_server(port_number):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port_number))
    server_socket.listen(5)
    print(f"Server started on port {port_number}. Waiting for a connection...")

    while True:
        client_socket, addr = server_socket.accept()

        # Receive client type (PUBLISHER or SUBSCRIBER) and the topic
        client_info = client_socket.recv(1024).decode().strip()
        client_type, topic = client_info.split(" ")

        if client_type not in ["PUBLISHER", "SUBSCRIBER"]:
            client_socket.sendall("Invalid role. Use PUBLISHER or SUBSCRIBER.".encode())
            client_socket.close()
            continue

        if type is None:
            client_socket.sendall("Enter your Topic/ Subject.".encode())
            client_socket.close()

        print(f"Client connected from {addr} as a {client_type} to {topic}")

        with lock:
            if client_type == "SUBSCRIBER":
                if topic not in subscribers:
                    subscribers[topic] = []
                subscribers[topic].append(client_socket)
            elif client_type == "PUBLISHER":
                publishers.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_type, topic))
        thread.start()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
