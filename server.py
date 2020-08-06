#!/usr/bin/ python3
"""SOCKETCHAT by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with client.py and chat via the cli.
-+- Works out of the box with Python3. No libraries needed.

For encrypted chat, use sec-client.py (requires addl libraries).
"""

import socket
import struct
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
        client.settimeout(None)

        # Announcce new guest
        announce_msg = f"{nick.decode()} is in the house! "
        broadcast(b'YO', addr, announce_msg.encode())

        # Tell me who's in here
        room_status = room.get_status(addresses, nicks)
        broadcast(b'YO', None, room_status, 'all')

        # from_client = b''
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    while True:
        try:
            data = client.recv(BUFFSIZE)  # Store incoming as data.

            addr = addresses[client]
            nick = nicks[client]

        except socket.timeout as err:
            print(f"-=- socket.timeout: {err}")
            break
        except socket.error as err:
            print(f"-=- socket.error: {err}")
            break

        if not data or data == b'exit()':
            break

        elif data == b'status()':
            # TODO: Move this to function or Room class methood
            # Challenge: broadcast isn't available from roomclass method
            # don't want too many tiny functions like (get_status in this code)
            # maybe an input controller that handles incoming keywords
            # Tell me who's in here
            room_status = room.get_status(addresses, nicks)
            broadcast(b'YO', addr, room_status, 'all')

        elif data == b'sendfile()':
            filesize = client.recv(BUFFSIZE)

            # While last thing to come through was actually filesize.
            # This means the send method is initiated properly.
            try:
                while int(filesize.decode()):
                    waiting_msg = (f'Waiting for user to accept transfer...')
                    broadcast(b'YO-xfer', addr, waiting_msg.encode(), 'self')

                    choice = input(
                        f'Accept file of size {filesize.decode()}? (Y or N) >> '
                    )

                    # User accepted file
                    if choice.lower() == 'y':
                        data = b''

                        f_xfer.receive_file(data, BUFFSIZE, filesize, client)

                        success_msg = (
                            f'{filesize.decode()}b successfully transfered, dawg.'
                        )
                        broadcast(b'YO-xfer', addr, success_msg.encode(),
                                  'self')
                        break
                    elif choice.lower() == 'n':
                        print('sendfile() cancelled.')
                        cancel_msg = (
                            'Recipient has declined transfer request.')
                        broadcast(b'YO-xfer', addr, cancel_msg.encode(), 'self')
                        print(cancel_msg)
                        break
            except:
                print('sendfile() cancelled.')

        msg_from_client = data
        broadcast(nick, addr, msg_from_client)
        # print(f'{addr}: {from_client.decode()}')
        print(f'@{nick.decode()}: {msg_from_client.decode()}')

    print(f'YO {nicks[client].decode()} has left the chat.')  # local print
    broadcast(b'YO', None,
              f'{nicks[client].decode()} has left the chat.'.encode(), 'all')

    client.shutdown(socket.SHUT_RDWR)
    client.close()

    # Clean up
    del nicks[client]
    del addresses[client]
    # people.remove(nicks[addr].decode())

    exit()
    print('Client disconnected.')


def broadcast(send_from_nick, addr, msg_from_client, target='others'):
    """
    Inputs
        send_from_nick: (str) Display handle.
        addr: (address) Sender's address
        msg_from_client: (str)
        target: (str) Options: 'others', 'self', 'all'
    """
    msg = f'@{send_from_nick.decode()}: {msg_from_client.decode()}'

    for socket in nicks:
        if target == 'others':  # Everyone but sender
            if socket.getpeername() != addr:
                socket.send(msg.encode())

        elif target == 'self':  # Sender only
            if socket.getpeername() == addr:
                socket.send(msg.encode())

        elif target == 'all':  # Everyone
            socket.send(msg.encode())

        else:
            raise Exception("Valid options are 'all', 'self', 'others'")


BUFFSIZE = 4096
MAX_CNXN = 5

addresses = {}
nicks = {}
people = []

welcome_msg = "\n=+= You're in. Welcome to the underground. =+="

#Instantiate
room = room.Room()

if __name__ == '__main__':

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make object

    # Instantiate transfer Class
    f_xfer = xfer.FileXfer()
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

    serv.settimeout(None)
    print("-+- Waiting for connections...")

    serv.listen(MAX_CNXN)  # listen for data.

    incoming_thread = Thread(target=accept_incoming_connections)
    incoming_thread.start()

    incoming_thread.join()
    serv.close()
