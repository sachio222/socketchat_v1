"""SOCKETCHAT by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with client.py and chat via the cli.
-+- Works out of the box with Python3. No libraries needed.

For encrypted chat, use sec-client.py (requires addl libraries).
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

        nick = client.recv(BUFFSIZE)
        nicks[client] = nick
        addresses[client] = addr

        # Announce new guest
        announce_msg = f"{nick.decode()} is in the house!"
        broadcast(b'YO', None, announce_msg.encode())
        # from_client = b''
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):

    while True:
        data = client.recv(BUFFSIZE)  # Store incoming as data.
        addr = addresses[client]
        nick = nicks[client]

        if not data or data == b'exit()':
            break

        from_client = data
        broadcast(nick, addr, from_client)
        # print(f'{addr}: {from_client.decode()}')
        print(f'@{nick.decode()}: {from_client.decode()}')


    print(f'YO {nicks[client].decode()} has left the chat.') # local print
    broadcast(b'YO', None, f'{nicks[client].decode()} has left the chat.'.encode())

    client.close()
    del nicks[client]
    exit()
    print('Client disconnected.')


def broadcast(nick, addr, from_client):

    msg = f'@{nick.decode()}: {from_client.decode()}'

    for socket in nicks:
        if socket.getpeername() != addr:
            socket.send(msg.encode(enc))


enc = 'utf8'
addresses = {}
nicks = {}

welcome_msg = "\n=+= You're in. Welcome to the underground. =+="

if __name__ == '__main__':

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make object

    BUFFSIZE = 2048
    MAX_CNXN = 5

    host = socket.gethostname()
    try:
        ip = socket.gethostbyname(host)
    except:
        ip = socket.gethostbyname('localhost')
        
    print(f'-+- Starting server on host: {host}')
    print(f'-+- Host IP: {ip}')
    port = input('-+- Choose port: ')
    port = int(port)

    try:
        serv.bind((host, port))  # bind to host as socket server.
    except:
        serv.bind((host, port))  # bind to host as socket server.

    serv.listen(MAX_CNXN)  # listen for data.
    print("-+- Waiting for connections...")

    incoming_thread = Thread(target=accept_incoming_connections)
    incoming_thread.start()

    incoming_thread.join()
    serv.close()
