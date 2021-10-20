import socket

HEADER = 64
PORT = 2021
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.\n")

        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
            
                print(f"[{addr}] {msg}")
                conn.send("Server received your msg...".encode(FORMAT))

        conn.close()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}\n")

print("[STARTING] server is starting...")
start()

