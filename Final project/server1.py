import socket
import threading
import os
from os.path import isfile, join, getsize
from signal import signal, SIGINT
import sys

HEADER = 64
PORT = 2021
R_PORT = 2022
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
R_ADDR = (SERVER,R_PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

SERVER_FOLDER = 'server_folder'

clients = []
usernames = []


def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.\n")

    connected = True
    while connected:
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message = client.recv(1024).decode(FORMAT)
        message_split = message.split()
        msg = message_split[0]
        
        if msg == 'DISCONNECT':
            client.send("OK".encode(FORMAT))
            recv_sock.connect(R_ADDR)
            recv_sock.send("DISCONNECT".encode(FORMAT))
            recv_sock.close()
            index = clients.index(client)
            clients.remove(client)
            usernames.remove(usernames[index])
            connected = False

        elif msg == 'QUIT':
            index = clients.index(client)
            clients.remove(client)
            usernames.remove(usernames[index])
            connected = False
            client.close()
            
        elif msg == 'LU':
            list_of_users = ""
            for i in range(len(usernames)):
                list_of_users += usernames[i] + ' '
            client.send(list_of_users.encode(FORMAT))
            

        elif msg == 'MESSAGE':
            if message_split[1] in usernames:
                try:
                    recv_sock.connect(R_ADDR)
                except Exception as e:
                    print('Couldnt deliver message: ', e)
                    client.send('ERROR: Connection to receiving thread failed'.encode(FORMAT))
                    recv_sock.close()
                    continue
                msg = message.replace(message_split[1], '')
                print(msg)
                recv_sock.send(msg.encode(FORMAT))
                print(f'{message_split[1]} received a message')
            else:
                client.send(f"{message_split[1]} is not online".encode(FORMAT))            

        elif msg == 'LF':
            files_in_server = os.listdir(SERVER_FOLDER)
            if len(files_in_server) == 0:
                client.send("Server folder is empty!".encode(FORMAT))
            else:
                filesInServer = ""
                for i in range(len(files_in_server)):
                    filesInServer+=files_in_server[i] + ' '
                client.send(filesInServer.encode(FORMAT))

        elif msg == 'READ':
            fileName = message_split[1]
            spath = SERVER_FOLDER + '/' + fileName
            if fileName not in os.listdir(SERVER_FOLDER):
                client.send("ERROR".encode(FORMAT))
            else:
                client.send("OK".encode(FORMAT))
                full_content = ""
                with open(f"{spath}", "r") as file:
                    content = file.readlines()
                for i in range(len(content)):
                    full_content += content[i] + " q%q "
                client.send(full_content.encode(FORMAT))
            

        elif msg == 'WRITE':
            fileName = message_split[1]
            if fileName not in os.listdir(SERVER_FOLDER):
                client.send("OK".encode(FORMAT))
                content = client.recv(1024).decode(FORMAT)
                full_content = ""
                for i in range(len(content)):
                    full_content+=content[i]
                full_text = full_content.split(' q%q ')
                all_content = ""
                for i in range(len(full_text)):
                    all_content += full_text[i]
                files = os.listdir(SERVER_FOLDER)
                filepath = os.path.join(SERVER_FOLDER, fileName)
                with open(filepath, "w") as file:
                    file.writelines(all_content.strip())
                client.send("File uploaded".encode(FORMAT)) 
            else:
                client.send("ERROR".encode(FORMAT))
                
        elif msg == 'OVERWRITE':
            fileName = message_split[1]
            client.send('OK'.encode(FORMAT))
            content = client.recv(2048).decode(FORMAT)                                                                                                                                                                                                                                      
            full_content = ""
            for i in range(len(content)):
                full_content+=content[i]
            full_text = full_content.split(' q%q ')
            all_content = ""
            for i in range(len(full_text)):
                all_content += full_text[i]
            all_content = all_content.strip()
            files = os.listdir(SERVER_FOLDER)
            filepath = os.path.join(SERVER_FOLDER, fileName) 
            with open(filepath, "w") as file:
                file.writelines(all_content)
            client.send("File updated...".encode(FORMAT))

        elif msg == 'OVERREAD':
            fileName = message_split[1]
            spath = SERVER_FOLDER + '/' + fileName
            if fileName not in os.listdir(SERVER_FOLDER):
                client.send("ERROR".encode(FORMAT))
            else:
                client.send("OK".encode(FORMAT))
                full_content = ""
                with open(f"{spath}", "r") as file:
                    content = file.readlines()
                for i in range(len(content)):
                    full_content += content[i] + " q%q "
                client.send(full_content.encode(FORMAT))
        

        elif msg == 'APPEND':
            fileName = message_split[1]
            if fileName in os.listdir(SERVER_FOLDER):
                client.send('OK'.encode(FORMAT))
                content = client.recv(1024).decode(FORMAT)
                full_content = "\n"
                for i in range(len(content)):
                    full_content += content[i] 
                filepath = os.path.join(SERVER_FOLDER, fileName) 
                with open(filepath, "a") as file:
                    file.write(full_content)
                client.send('Content is added...'.encode(FORMAT))
            else:
                client.send("ERROR".encode(FORMAT))
            

        elif msg == 'APPENDFILE':
            srcFile = message_split[1]
            dstFile = message_split[2]
            if dstFile in os.listdir(SERVER_FOLDER):
                client.send('OK'.encode(FORMAT))        
                full_content = client.recv(1024).decode(FORMAT)
                filepath = os.path.join(SERVER_FOLDER, dstFile) 
                with open(filepath, "a") as file:
                    file.write(full_content)
                client.send('File added...'.encode(FORMAT))
            else:
                client.send('ERROR'.encode(FORMAT))

def sigint_handler(sig, frame):
    global res
    print(f"Server received SIGINT signal...")
    res = 0
    sys.exit(0)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    signal(SIGINT, sigint_handler)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(R_ADDR)
        s.listen()
        s.settimeout(1.0)
        res = 0

    while True:
        client, addr = server.accept()
        message = client.recv(1024).decode(FORMAT)
        message_split = message.split()
        if message_split[1] not in usernames:
            usernames.append(message_split[1])
            clients.append(client)
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.start()
            client.send("OK".encode(FORMAT))
        else:
            client.send("ERROR".encode(FORMAT))
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")
print("[STARTING] server is starting...")
start()
