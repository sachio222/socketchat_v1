"""
import socket

# Create a socket object
# family: Address Format Internet
# type: Socket Stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Once a socket exists, we just open and close the connection. 

# Connect to an IP with port, could be URL. 
sock.connect(('0.0.0.0', 8080))

# Send some data.
sock.send('Twenty-five bytes to send')

# Receive up to 4096 bytes from a peer
sock.recv(4096)

# Close the socket connection, no transmission.
sock.close()


"""

import socket
from threading import Thread


def accept_incoming_connections():
    # Accept the connections.
    while True:
        client, addr = serv.accept()
        print(f"Connected to {addr}")

        # Send welcome message.
        client.send(welcome_msg.encode(enc))

        handle = client.recv(BUFFSIZE)
        handles[client] = handle
        addresses[client] = addr

        # Announce new guest
        announce_msg = f"{handle.decode()} is in the house!"
        broadcast(b'YO', None, announce_msg.encode())
        # from_client = b''
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    # print('all:', addresses)
    # print(handles)

    while True:
        data = client.recv(BUFFSIZE)  # Store incoming as data.
        addr = addresses[client]
        handle = handles[client]

        if not data:
            break
        from_client = data
        broadcast(handle, addr, from_client)
        # print(f'{addr}: {from_client.decode()}')
        print(f'@{handle.decode()}: {from_client.decode()}')
    client.close()
    del handles[client]
    exit()
    print('Client disconnected.')


def broadcast(handle, addr, from_client):

    msg = f'@{handle.decode()}: {from_client.decode()}'

    for socket in handles:
        if socket.getpeername() != addr:
            socket.send(msg.encode(enc))


enc = 'utf8'
addresses = {}
handles = {}

welcome_msg = "\n=+= You're in. Welcome to the underground. =+="

if __name__ == '__main__':

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make object

    BUFFSIZE = 2048
    HOST = socket.gethostname()
    IP = socket.gethostbyname(HOST)
    MAX_CNXN = 5

    print(f'-+- Starting server on host: {HOST}')
    print(f'-+- Host IP: {IP}')
    PORT = input('-+- Choose port: ')
    PORT = int(PORT)

    try:
        serv.bind((HOST, PORT))  # bind to host as socket server.
    except:
        serv.bind((HOST, PORT))  # bind to host as socket server.

    serv.listen(MAX_CNXN)  # listen for data.
    print("-+- Waiting for connections...")

    incoming_thread = Thread(target=accept_incoming_connections)
    incoming_thread.start()

    incoming_thread.join()
    serv.close()
