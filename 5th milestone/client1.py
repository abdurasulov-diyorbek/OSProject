import socket
from threading import Thread, Lock
import time
import sys
import os

HEADER = 64
FORMAT = 'utf-8'
PORT = 2021
SERVER = '192.168.57.2'
ADDR = (SERVER, PORT)
PORT2 = 2022
ADDR2 = (SERVER, PORT2)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CLIENT_FOLDER = 'client_folder'
    
def sending():
    status = True
    while status:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        command = input("Write a command (please type connect or quit): ")
        if command != 'quit':
            command_split = command.split()
            com1 = command_split[0]
            com2 = command_split[1]
            com3 = command_split[2]
        else:
            break

        if (com1 == 'connect' and com3 == SERVER):
            client.connect(ADDR)
            client.send(com2.encode(FORMAT))
            
            connected = True
            while connected:
                print("\nYou are connected to the server. List of commands: disconnect, quit, lu, send, lf, read, write.")
                command = input("Write a command: ")
                command_split = command.split()
                com1 = command_split[0]
                
                if com1 == 'disconnect':
                    client.send('DISCONNECT!'.encode(FORMAT))
                    print('You are disconnected from the SERVER!!!')
                    connected = False
                    client.close()
                elif com1 == 'quit':
                    client.send('QUIT'.encode(FORMAT))
                    connected = False
                    status = False
                    
                elif com1 == 'quit':
                    status = False
                    connected = False
                elif com1 == 'lu':
                    client.send('lu'.encode(FORMAT))
                    print(client.recv(1024).decode(FORMAT))
                    
                elif com1 == 'lf':
                    client.send('lf'.encode(FORMAT))
                    print(client.recv(1024).decode(FORMAT))
      
                elif com1 == 'send':
                    client.send('send'.encode(FORMAT))
                    com2 = command_split[1]
                    usrMessage = command_split[2]
                    client.send(com2.encode(FORMAT))
                    client.send(usrMessage.encode(FORMAT))
                    print('Received: ',client.recv(1024).decode(FORMAT))
                    print(client.recv(1024).decode(FORMAT))

                    
                elif com1 == 'read':
                    if command_split[1] not in os.listdir(CLIENT_FOLDER):
                        FILENAME = command_split[1]
                        client.send(f"READ {FILENAME}".encode(FORMAT))
                        Response = client.recv(1024).decode(FORMAT)
                        if Response == "ERROR":
                            print("Error: Server does not contain such a file")
                        elif Response == "OK":
                            content = client.recv(1024).decode(FORMAT)
                            full_content = content.split(' q%q ')
                            all_content = ""
                            for i in range(len(full_content)):
                                all_content +=full_content[i]
                            files = os.listdir(CLIENT_FOLDER)
                            filepath = os.path.join(CLIENT_FOLDER, command_split[1])
                            with open(filepath, "w") as file:
                                file.writelines(all_content.strip())
                            print("File uploaded") 
                    else:
                        print('Client already contains this file!')

    
                elif com1 == 'write':
                    FILENAME = command_split[1]
                    if FILENAME not in os.listdir(CLIENT_FOLDER):
                        print("Error: Client does not contain such a file")
                    else:
                        client.send(f"WRITE {FILENAME}".encode(FORMAT))
                        response = client.recv(1024).decode(FORMAT)
                        if response == "OK":
                            cpath = CLIENT_FOLDER
                            cpath += "/" + FILENAME
                            full_content = ""
                            with open(f"{cpath}", "r") as file:
                                content = file.readlines()
                            for i in range(len(content)):
                                full_content += content[i] + " q%q "
                            client.send(f"{full_content}".encode(FORMAT))
                            print(client.recv(1024).decode(FORMAT))
                        elif response == "ERROR":
                            print("Error: Server already contains such a file")
                        
                elif com1 == 'overwrite':
                    if command_split[1] not in os.listdir(CLIENT_FOLDER):
                        print("Error: Client does not contain such a file")
                    else:
                        client.send(f"OVERWRITE {command_split[1]}".encode(FORMAT))
                        response = client.recv(1024).decode(FORMAT)
                        if response == "OK":                     
                            cpath = CLIENT_FOLDER
                            cpath += "/" + command_split[1]
                            full_content = ""
                            with open(f"{cpath}", "r") as file:
                                content = file.readlines()
                            for i in range(len(content)):
                                full_content += content[i] + " q%q "
                            client.send(f"{full_content}".encode(FORMAT))
                            print(client.recv(1024).decode(FORMAT))

                elif com1 == 'overread':
                    client.send(f"OVERREAD {command_split[1]}".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    if response == "OK":
                        content = client.recv(1024).decode(FORMAT)
                        full_content = content.split(' q%q ')
                        all_content = ""
                        for i in range(len(full_content)):
                            all_content +=full_content[i]
                        files = os.listdir(CLIENT_FOLDER)
                        filepath = os.path.join(CLIENT_FOLDER, command_split[1])
                        with open(filepath, "w") as file:
                            file.writelines(all_content.strip())
                        print("File updated...")
                    else:
                        print('Server does not contain this file...')
                        
                elif com1 == 'append':
                    client.send(f'APPEND {command_split[-1]}'.encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    if response == "OK":
                        content = command.split('"')[1::2]
                        full_content = ''
                        for i in range(len(content)):
                            full_content += content[i] 
                        client.send(f'{content}'.encode(FORMAT))
                        print(client.recv(1024).decode(FORMAT))
                    else:
                        print("Error: Server has no such a file!")
    

                elif com1 == 'appendfile':
                    srcFile = command_split[1]
                    dstFile = command_split[2]
                    if srcFile in os.listdir(CLIENT_FOLDER):
                        client.send(f"APPENDFILE {srcFile} {dstFile}".encode(FORMAT))
                        response = client.recv(1024).decode(FORMAT)
                        if response == "OK":
                            filepath = os.path.join(CLIENT_FOLDER, srcFile) 
                            with open (f'{filepath}', "r") as file:
                                content = file.readlines()
                            full_content = "\n"
                            for i in range(len(content)):
                                full_content += content[i]
                            client.send(f'{full_content}'.encode(FORMAT))
                            print(client.recv(1024).decode(FORMAT))
                        else:
                            print("Error: Server folder has not such a file!!")
                    else:
                        print("Error: Client folder has not such a file!!")
                
                else:
                    print("Error: Command not found!")
                
        elif command == 'quit':
            status = False

        elif com3 != SERVER:
            print("You are using wrong IP address")
        else:
            print("Error: Command not found")
         
    print("Disconnected...")
    
sendingThread = Thread(target = sending)
sendingThread.start()

#receivingThread = Thread(target = receiving)
#receivingThread.start()



