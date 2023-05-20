import socket
import threading

HEADER = 64
PORT = 5050
SERVER = ''  # server = get the ip address of this computer by host name
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "discon"

# looks for IPV4 address and streams and waits
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    messages = []
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{addr}] {msg}')
            conn.send("message recieved".encode(FORMAT))
    conn.close()


def start():
    server.listen()  # listening for new connections
    print(f"[LISTEINGING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        """ waits for new connection on server, 
            when connection is true stores address and what port it came from on addr 
            and store it as an object in conn that allows user to send back feedback"""

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')


print("[STARTING] server is starting...")
start()
