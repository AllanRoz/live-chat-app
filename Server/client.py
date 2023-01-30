import socket

HEADER = 2048
PORT = 5051
FORMAT = 'utf-8'
NEW_MESSAGE = '!new_msg'
NO_MESSAGE = '!no_msg'
DISCONNECT_MESSAGE = '!dc'
NOTHING_MESSAGE = '!nothing'
SERVER = '192.168.0.156'
ADDR = (SERVER, PORT)
user_input = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    if client.recv(HEADER).decode(FORMAT) == NEW_MESSAGE:
        print(client.recv(HEADER).decode(FORMAT))

try:
    while user_input != DISCONNECT_MESSAGE:
        user_input = input("Type your message: ")
        send(user_input)
except:
    send(DISCONNECT_MESSAGE)