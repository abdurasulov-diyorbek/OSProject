import socket
from threading import Thread, Lock
import time
import sys
import os

HEADER = 64
FORMAT = 'utf-8'
PORT = 2021
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
R_PORT = 2022
R_ADDR = (SERVER, R_PORT)

CLIENT_FOLDER = 'client_folder'

clientLock = Lock()
    
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
            client.send(f"CONNECT {com2}".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            if response == "ERROR":
                print("This Username is not available. Please choose another one..")
                status = False
                connected = False
            elif response == "OK":
                connected = True
                
            while connected:
                clientLock.acquire()
                print("\nYou are connected to the server!!!")
                command = input("Write a command: ")
                if not connected:
                    clientLock.release()
                    break
                command_split = command.split()
                com1 = command_split[0]
                
                if com1 == 'disconnect':
                    client.send('DISCONNECT'.encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    if response == "OK":
                        print('You are disconnected from the SERVER!!!')
                        connected = False
                        client.close()
                    else:
                        print("Something went wrong...")
                        
                elif com1 == 'quit':
                    client.send('QUIT'.encode(FORMAT))
                    connected = False
                    status = False
                    
                elif com1 == 'quit':
                    status = False
                    connected = False
                elif com1 == 'lu':
                    client.send('LU'.encode(FORMAT))
                    print(client.recv(1024).decode(FORMAT))
                    
                elif com1 == 'lf':
                    client.send('LF'.encode(FORMAT))
                    print(client.recv(1024).decode(FORMAT))
                          
                elif com1 == 'send':
                    msg = command[command.find('“') + 1:command.find('”')]
                    send_msg = 'MESSAGE {}\n{} {}'.format(command_split[1], str(len(msg)), msg)
                    client.send(send_msg.encode(FORMAT))
                    client.settimeout(2)
                    try:
                        print(client.recv(1024).decode(FORMAT))
                    except socket.timeout:
                        print('Message has been sent')
                    
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
                clientLock.release()
                time.sleep(1)
                
        elif command == 'quit':
            status = False

        elif com3 != SERVER:
            print("You are using wrong IP address")
        else:
            print("Error: Command not found")
         
    print("Disconnected...")

def receiving():
    
    r_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    r_client.bind((SERVER, R_PORT))
    r_client.listen()

    while True:
        server_s, server_addr = r_client.accept()
        response = server_s.recv(1024).decode(FORMAT)

        if response == "DISCONNECT":
            clientLock.acquire()
            print('Disconnected...')
            r_client.close()
            clientLock.release()
            r_client.close()
            

        elif response:
            size = int(response.split()[1])
            message = response[-size:]
            size -= len(response)
            
            while size > 0:
                response = serv_sock.recv(1024).decode()
                message += response
                size -= 1024
            clientLock.acquire()
            print('YOU ARE RECEIVED A MESSAGE\n', message)
            clientLock.release()
            time.sleep(0.1)
            r_client.close()

        else:
            break
    
sendingThread = Thread(target = sending)
sendingThread.start()

receivingThread = Thread(target = receiving)
receivingThread.start()

sendingThread.join()
receivingThread.join()


