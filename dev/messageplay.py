#!/usr/bin/python3

import socket
import struct
import sys
import time
from threading import Thread

BFFR = 4096
users = {}
sockets = {}
nicks = {}

def accepting():
    while True:
        client_cnxn, client_addr = sock.accept()
        print(f'-=- Connected... to {client_addr}')
        sockets[client_cnxn] = client_addr

        Thread(target=handle_clients, args=(client_cnxn, )).start()


def handle_clients(client_cnxn):
    client_cnxn.send(b'-=- Enter nickname: @')
    user = client_cnxn.recv(1)
    user_name = unpack_msg(client_cnxn)
    users[sockets[client_cnxn]] = user_name

    while True:
        data = client_cnxn.recv(BFFR)

        if not data:
            #TODO: Run through connected sockets, clean up list.
            del sockets[client_cnxn]
            print(sockets)
            break

        data_router(client_cnxn, data)
        # data = client_cnxn.recv(4)
        # buff = recv_pkt(client_cnxn, data, 4)
        # msg_short = client_cnxn.recv(buff)
        # # print(msg_short)

        # client_cnxn.send(data)


def data_router(client_cnxn, data):
    # Server client communication codes.

    if data[0] == 85: # 85 = 'U' Prefix in bytes.
        """Checks if user exists in user dict."""

        EXISTS_MSG = b'U0001True'
        NO_EXISTS_MSG = b'U0005False'
        
        data = data[5:] # Remove prefixes.
        print(data)
        user_exists, user_addr = check_user(data)
        if user_exists:
            print('User found.')
            data = EXISTS_MSG + user_addr
        else:
            print('User not found.')
            data = NO_EXISTS_MSG

        client_cnxn.send(data)
    else:
        
        # data = client_cnxn.recv(4096)
        for sock in sockets:
            if sockets[sock] != sockets[client_cnxn]:
                # print(sock)
                try:
                    sock.send(data)
                except:
                    pass


def recv_pkt(client_cnxn, data, n):
    return int(data[:n])

def check_user(user_select):
    """Checks if user exists. If so, returns user and address."""
    for addr, user in users.items():
        print(f'user: {user}')
        print(f'selected: {user_select}')
        if user == user_select:
            print('match!')
            match = True
            user_addr = addr
            break
        else: 
            print('no match')
            match = False
            user_addr = None       
    print(f'match: {match}')
    print(f'recip-addy: {user_addr}')
    return match, user_addr

def unpack_msg(client_cnxn):
        #1
        """Unpacks prefix for file size, and returns trimmed message as bytes.
        
        This method does not read the message type. Call receiver() before
                invoking this method. Once the input has been routed, this
                helper function is called to unpack the already sorted user
                inputs. 
        """

        sz_pfx = client_cnxn.recv(4)
        buffer = _pfxtoint(client_cnxn, sz_pfx, 4)
        trim_msg = client_cnxn.recv(buffer)

        return trim_msg

def _pfxtoint(client_cnxn, data, n=4):
    #1
    """Converts size prefix data to int."""
    return int(data[:n])


def countdown(secs=90, msg='-+- Try again in '):
    # util
    ERASE_LINE = '\x1b[2K'
    t = secs
    while t >= 0:
        print(f'{msg}{t}\r', end="")
        sys.stdout.write(ERASE_LINE)
        time.sleep(1)
        t -= 1
    exit()

addy = ('127.0.0.1', 1515)
sock = socket.socket()
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addy)
except Exception as e:
        print(f'-x- {e}')
        countdown(90)

sock.listen(5)
print('-=- Listening...')
Thread(target=accepting).start()
