import socket
import threading
import time
import sys

HEADER = 64
FORMAT = 'utf-8'
PORT = 2021
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT2 = 2022
ADDR2 = (SERVER, PORT2)
client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    
def sending():
    status = True
    while status:
        connected = False
        command = input("Write a command (please type connect or quit): ")
        command_split = command.split()
        com1 = command_split[0]
        com2 = command_split[1]

        if com1 == 'connect':
            client.connect(ADDR)
            send(com2)
            connected = True
        elif com1 == 'quit':
            status = False
        else:
            print("Error: Command not found")
            
        while connected:
            print("\nYou are connected to the server. List of commands: disconnect, quit, lu, send, lf, read, write.")
            command = input("Write a command: ")
            command_split = command.split()
            com1 = command_split[0]
            
            if com1 == 'disconnect':
                send('DISCONNECT!')
                connected = False
            elif com1 == 'quit':
                status = False
                connected = False
            if com1 == 'lu':
                send('USERS')
                print(client.recv(1024).decode(FORMAT))
                
            elif com1 == 'send':
                send('send')
                com2 = command_split[1]
                usrMessage = command_split[2]
                send(com2)
                send(usrMessage)
                print('Received: ',client.recv(1024).decode(FORMAT))
                print(client.recv(1024).decode(FORMAT))
                
            elif command == 'lf':
                print("List Files")
            elif com1 == 'read':
                if command_split[1]=='exists':
                    print('Error: Client already consists that file.')
                    continue
                send('READ')
            elif com1 == 'write':
                 if command_split[1]=='exists':
                    print('Error: Client already consists that file.')
                    continue
                    send('WRITE')

            else:
                print("Error: Command not found!")
    print("Disconnected...")

def receiving():
    active = True:
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.bind(ADDR2)
        client2.listen()
        client2.settimeout(1.0)
        while True:
            try:
                conn, addr = client2.accept()
                data = conn.recv(1024)
            except timeout:
                continue
            except Exception as e:
                print(e)
                break
            else:
                print(data.decode())    
sendingThread = threading.Thread(target = sending)
sendingThread.start()

receivingThread = threading.Thread(target = receiving)
receivingThread.start()



