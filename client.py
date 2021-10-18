import socket

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT!"
CONNECT_MESSAGE = "CONNECTED!"
PORT = 2021
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

status = True

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

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
    command = input("Write a command (please type connect or quit): ")
    command_split = command.split()
    com1 = command_split[0]

    if com1 == 'connect':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        send(CONNECT_MESSAGE)
        send("Hello Server! I am a client.\n")
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
