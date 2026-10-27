import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000


def receive_messages(reader):
    try:
        for message in reader:
            print(f"\n{message.rstrip()}")
            print("You> ", end="", flush=True)

    except (OSError, UnicodeError) as error:
        print(f"\nReceive error: {error}")

    finally:
        print("\nServer disconnected.")
        client_running.clear()


client_running = threading.Event()
client_running.set()


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_HOST, SERVER_PORT))

        print("=" * 40)
        print("       NETSCOPE TCP CHAT CLIENT")
        print("=" * 40)
        print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
        print("Type messages to chat.")
        print("Type /quit to leave.")
        print("=" * 40)

        with client, client.makefile(
            "r", encoding="utf-8"
        ) as reader:

            receiver = threading.Thread(
                target=receive_messages,
                args=(reader,),
                daemon=True
            )
            receiver.start()

            while client_running.is_set():
                try:
                    message = input("You> ")
                except EOFError:
                    break

                if not client_running.is_set():
                    break

                try:
                    client.sendall(
                        (message + "\n").encode("utf-8")
                    )
                except OSError:
                    print("Unable to send. Connection may be closed.")
                    break

                if message == "/quit":
                    break

    except (ConnectionRefusedError, socket.timeout, OSError) as error:
        print(f"Connection error: {error}")

    finally:
        client_running.clear()

        try:
            client.close()
        except OSError:
            pass

        print("Client closed.")


if __name__ == "__main__":
    start_client()
