import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}
clients_lock = threading.Lock()
next_client_id = 1
running = threading.Event()
running.set()


def send_message(client, message):
    """Send one newline-delimited message safely."""
    try:
        with client["send_lock"]:
            client["conn"].sendall(
                (message + "\n").encode("utf-8")
            )
        return True
    except OSError:
        return False


def broadcast(message, exclude=None):
    """Send a message to all connected clients."""
    with clients_lock:
        targets = list(clients.items())

    for client_id, client in targets:
        if client_id != exclude:
            if not send_message(client, message):
                print(f"Could not send to Client {client_id}.")


def handle_client(client_id, client):
    conn = client["conn"]
    address = client["address"]

    print(f"Client {client_id} connected from {address}")

    try:
        with conn.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                message = line.rstrip("\r\n")

                if message == "/quit":
                    send_message(client, "You have left the chat.")
                    break

                if not message:
                    continue

                print(f"\n[Private Message from Client {client_id}]: {message}")

    except (OSError, UnicodeError) as error:
        print(f"Client {client_id} error: {error}")

    finally:
        with clients_lock:
            clients.pop(client_id, None)

        try:
            conn.close()
        except OSError:
            pass

        print(f"Client {client_id} disconnected.")


def accept_clients(server):
    global next_client_id

    while running.is_set():
        try:
            conn, address = server.accept()
            conn.settimeout(None)

            with clients_lock:
                client_id = next_client_id
                next_client_id += 1

                client = {
                    "conn": conn,
                    "address": address,
                    "send_lock": threading.Lock()
                }

                clients[client_id] = client

            send_message(
                client,
                f"Welcome! Your client ID is {client_id}."
            )

            threading.Thread(
                target=handle_client,
                args=(client_id, client),
                daemon=True
            ).start()

        except OSError:
            if running.is_set():
                print("Error accepting a client connection.")
            break


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()

        print("=" * 45)
        print("        TWO-WAY TCP CHAT")
        print("=" * 45)
        print(f"Server listening on port {PORT}")
        print("Commands:")
        print("  /list                 List connected clients")
        print("  /msg ID message       Message one client")
        print("  /all message          Broadcast to everyone")
        print("  /quit                 Stop the server")
        print("Any other text is broadcast to everyone.")
        print("=" * 45)

        threading.Thread(
            target=accept_clients,
            args=(server,),
            daemon=True
        ).start()

        while running.is_set():
            try:
                message = input("Server> ").strip()
            except EOFError:
                break

            if not message:
                continue

            if message == "/quit":
                break

            elif message == "/list":
                with clients_lock:
                    ids = list(clients.keys())

                print("Connected clients:", ids if ids else "None")

            elif message.startswith("/msg "):
                parts = message.split(" ", 2)

                if len(parts) < 3 or not parts[1].isdigit():
                    print("Usage: /msg ID message")
                    continue

                client_id = int(parts[1])

                with clients_lock:
                    target = clients.get(client_id)

                if target:
                    if send_message(
                        target,
                        f"[Server, private]: {parts[2]}"
                    ):
                        print(f"Message sent to Client {client_id}.")
                    else:
                        print("Failed to send message.")
                else:
                    print("Client ID not found.")

            elif message.startswith("/all "):
                broadcast(f"[Server]: {message[5:]}")
                print("Broadcast sent.")

            else:
                broadcast(f"[Server]: {message}")
                print("Broadcast sent.")

    except OSError as error:
        print(f"Server error: {error}")

    finally:
        running.clear()

        try:
            server.close()
        except OSError:
            pass

        with clients_lock:
            connected_clients = list(clients.values())
            clients.clear()

        for client in connected_clients:
            try:
                client["conn"].shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

            try:
                client["conn"].close()
            except OSError:
                pass

        print("Server stopped.")


if __name__ == "__main__":
    start_server()