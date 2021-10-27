import socket
import threading

HEADER = 64
PORT = 2021
PORT2 = 2022
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
ADDR2 = (SERVER, PORT2)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
usernames = []

def func():
    server2.bind(ADDR2)
    

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.\n")

    connected = True
    while connected:
        msg = client.recv(1024).decode(FORMAT)
        if msg == 'DISCONNECT!':
            connected = False
            
        elif msg == 'USERS':
            for i in range(len(usernames)):
                client.send(usernames[i].encode(FORMAT))

        elif msg == 'send':
            usr = client.recv(1024).decode(FORMAT)
            usrMessage = client.recv(1024).decode(FORMAT)
            for i in range(len(usernames)):
                if usernames[i] == usr:
                    clients[i].send(usrMessage.encode(FORMAT))
                    print(f"Message was send to {usernames[i]}")
                    client.send("Sended!".encode(FORMAT))
                else:
                    client.send("{usr} is not online!!!".encode(FORMAT))
            print(f"{usr}: {usrMessage}")
                    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, addr = server.accept()
        
        username = client.recv(1024).decode(FORMAT)
        
        usernames.append(username)
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}\n")
print("[STARTING] server is starting...")
start()
