import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT!"
CONNECT_MESSAGE = "CONNECT!"

status = True


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length +=b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while status:
    connected = False
    command = input("Write a command: ")
    command_split = command.split()
    com1 = command_split[0]

    if com1 == 'connect':
        send(CONNECT_MESSAGE)
        connected = True
    elif com1 == 'quit':
        status = False
    else:
        print("Error: Command not found")
    
    
    while connected:
        send("Hello Server!!!")
        command = input("Write a command: ")
        command_split = command.split()
        com1 = command_split[0]
        
        if com1 == 'disconnect':
            send(DISCONNECT_MESSAGE)
            connected = False
        elif com1 == 'quit':
            status = False
            connected = False
        elif com1 == 'lu':
            print("List of users...")
        elif com1 == 'send':
            send('Message')
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
