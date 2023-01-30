import socket
import threading

HEADER = 2048
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
NEW_MESSAGE = '!new_msg'
NO_MESSAGE = '!no_msg'
HELP_MESSAGE = '!help'
DISCONNECT_MESSAGE = '!dc'
GAME_MESSAGE = '!game'
active_users = threading.active_count() - 1

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
        except:
            client_disconnection(addr)
            break
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == HELP_MESSAGE:
                send_to_client(conn, f"{DISCONNECT_MESSAGE} - disconnect from server"\
                    f"\n{GAME_MESSAGE} - lists games that can be played".encode(FORMAT))
            elif msg == DISCONNECT_MESSAGE:
                send_to_client(conn, "You disconnected from server.".encode(FORMAT))
                client_disconnection(addr)
                break
            elif msg == GAME_MESSAGE:
                send_to_client(conn, f"Games Available:\n!wc - word chain".encode(FORMAT))

            print(f"[{addr}] {msg}")
            conn.send(NO_MESSAGE.encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        global active_users
        active_users += 1
        print(f"[ACTIVE] {active_users}")

def client_disconnection(addr):
    print(f"[DISCONNECTION] {addr} disconnected.")
    global active_users
    active_users -= 1
    print(f"[ACTIVE] {active_users}")

def send_to_client(conn, msg):
    conn.send(NEW_MESSAGE.encode(FORMAT))
    conn.send(msg)

def game():
    pass

print("[STARTING] server is starting...")
start()