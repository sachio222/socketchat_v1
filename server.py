"""SOCKETCHAT by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with client.py and chat via the cli.
-+- Works out of the box with Python3. No libraries needed.

For encrypted chat, use sec-client.py (requires addl libraries).
"""

import socket
from threading import Thread
from chat_util import room, xfer


def accept_incoming_connections():
    # Accept the connections.
    while True:
        client, addr = serv.accept()
        print(f"Connected to {addr}")

        # Send welcome message.
        client.send(welcome_msg.encode())

        nick = client.recv(BUFFSIZE)
        nicks[client] = nick
        addresses[client] = addr

        # Announce new guest
        announce_msg = f"{nick.decode()} is in the house! "
        broadcast(b'YO', addr, announce_msg.encode())

        # Tell me who's in here
        room_status = room.get_status(addresses, nicks)
        broadcast(b'YO', None, room_status, 'all')

        # from_client = b''
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    while True:
        data = client.recv(BUFFSIZE)  # Store incoming as data.
        addr = addresses[client]
        nick = nicks[client]

        if not data or data == b'exit()':
            break

        elif data == b'status()':
            # TODO: Move this to function or Room class methood
            # Challenge: broadcast isn't available from roomclass method
            # don't want too many tiny functions like (get_status in this code)
            # maybe an input controller that handles incoming keywords
            # Tell me who's in here
            room_status = room.get_status(addresses, nicks)
            broadcast(b'YO', addr, room_status, 'self')

        elif data == b'sendfile()':
            filesize = client.recv(BUFFSIZE)
            while isinstance(filesize, int):
                print(filesize)
                # waiting_msg = (f'Waiting for user to accept transfer...')
                # broadcast(b'YO-xfer', addr, waiting_msg.encode(), 'self')
                choice = input(f'Accept file of size {filesize.decode()}? (y or n)')

                # User accepted file
                if choice == 'y':
                    f_xfer.receive_file(data, BUFFSIZE, filesize, client)
                success_msg = (
                    f'{filesize.decode()}b successfully transfered, dawg.')
                broadcast(b'YO-xfer', addr, success_msg.encode(), 'self')
            
            print('sendfile() cancelled.')
            # broadcast('YO:', addr, filesize, 'self')

        from_client = data
        broadcast(nick, addr, from_client)
        # print(f'{addr}: {from_client.decode()}')
        print(f'@{nick.decode()}: {from_client.decode()}')

    print(f'YO {nicks[client].decode()} has left the chat.')  # local print
    broadcast(b'YO', None,
              f'{nicks[client].decode()} has left the chat.'.encode(), 'all')

    client.shutdown()
    client.close()

    # Clean up
    del nicks[client]
    del addresses[client]
    # people.remove(nicks[addr].decode())

    exit()
    print('Client disconnected.')


def broadcast(nick, addr, msg_from_client, target='others'):
    """
    Inputs
        nick: (str) Display handle.
        addr: (address) Sender's address
        msg_from_client: (str)
        target: (str) Options: 'others', 'self', 'all'
    """
    msg = f'@{nick.decode()}: {msg_from_client.decode()}'

    for socket in nicks:
        if target == 'others':
            if socket.getpeername() != addr:
                socket.send(msg.encode())

        elif target == 'self':
            if socket.getpeername() == addr:
                socket.send(msg.encode())
        
        elif target == 'all':
            socket.send(msg.encode())
        
        else:
            raise Exception("Valid options are 'all', 'self', 'others'")



# def broadcast_self(nick, addr, from_client):

#     msg = f'@{nick.decode()}: {from_client.decode()}'

#     for socket in nicks:
#         if socket.getpeername() == addr:
#             socket.send(msg.encode())


BUFFSIZE = 4096
MAX_CNXN = 10

addresses = {}
nicks = {}
people = []

welcome_msg = "\n=+= You're in. Welcome to the underground. =+="

#Instantiate
room = room.Room()

if __name__ == '__main__':

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make object

    # Instantiate transfer Class
    f_xfer = xfer.FileXfer(serv)

    host = socket.gethostname()
    try:
        ip = socket.gethostbyname(host)
    except:
        ip = socket.gethostbyname('localhost')

    print(f'-+- Starting server on host: {host}')
    print(f'-+- Host IP: {ip}')
    port = input('-+- Choose port: ')

    port = port or 12222
    port = int(port)

    try:
        serv.bind((host, port))  # bind to host as socket server.
    except:
        #TESTING
        print("Port not available. Try again in a minute.")
        exit()

    serv.listen(MAX_CNXN)  # listen for data.
    print("-+- Waiting for connections...")

    incoming_thread = Thread(target=accept_incoming_connections)
    incoming_thread.start()

    incoming_thread.join()
    serv.shutdown()
    serv.close()
