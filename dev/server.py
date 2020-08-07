#!/usr/bin/ python3

import socket
import sys
import time
from threading import Thread

import chatutils.utils as utils
from chatutils.chatio import ChatIO

BFFR = 4096
sockets = {}
nicks_by_sock = {}
addrs_by_nick = {}

sox = {}


def accepting():
    # Accept connections.
    while True:
        client_cnxn, client_addr = sock.accept()
        print(f'-+- Connected... to {client_addr}')
        sockets[client_cnxn] = client_addr  # Create cnxn:addr pairings.
        Thread(target=handle_clients, args=(client_cnxn,)).start()


def handle_clients(client_cnxn):
    # Get username.
    user_name = init_client_data(client_cnxn)
    pack_n_send(client_cnxn, 'M', f"{user_name} is in the house!")

    # Start listening.
    while True:
        data = client_cnxn.recv(BFFR)  # Receive data as chunks.

        if not data:
            #TODO: Run through connected sockets, clean up list.
            del (addrs_by_nick[nicks_by_sock[client_cnxn]])
            print('addrs_by_nick: ', addrs_by_nick)
            del (nicks_by_sock[client_cnxn])
            print('nicks_by_sock: ', nicks_by_sock)
            del (sockets[client_cnxn])  # remove address
            print('sockets: ', sockets)

            break

        data_router(client_cnxn, data)


def data_router(client_cnxn, data):
    # Server client communication codes.

    # Send confirm dialog to recip if user is sending file.
    if data[0] == "/".encode():
        print('controller')
        # Don't print
        drain_socket = unpack_msg(client_cnxn)

    if data[0] == 85:  # 85 = 'U' Prefix in bytes.
        data = file_confirm_prompt(client_cnxn, data)
        pack_n_send(client_cnxn, 'U', data)

    else:
        for sock in sockets:
            if sockets[sock] != sockets[client_cnxn]:
                # print(sock)
                try:
                    sock.send(data)

                except:
                    pass

    print(data)


def recv_pkt(client_cnxn, data, n):
    return int(data[:n])


def file_confirm_prompt(client_cnxn, data):
    """Checks if user exists in user dict."""

    data = data[5:]  # Remove prefixes.
    user_exists, user_addr = check_user(client_cnxn, data)
    if user_exists:
        print(f'Found {data.decode()}')
        EXISTS_MSG = 'Waiting for user to accept.'
        data = EXISTS_MSG
        user_addr = user_addr
    else:
        print(f'User {data.decode()} not found.')
        data = ''

    return data


def check_user(sock, user_select):
    """Checks if user exists. If so, returns user and address."""
    match = False
    user_addr = None

    user_select = user_select.decode()
    for nick, addr in addrs_by_nick.items():
        print(f'user: {nick}')
        print(f'selected: {user_select}')

        if addr != sockets[sock]:  # Avoid self match.

            if nick == user_select:
                print('Match!')
                match = True
                user_addr = addr
                break

            else:
                print('No match')

            print(f'match: {match}')
            print(f'recip-addy: {user_addr}')

    return match, user_addr


def pack_n_send(sock, typ_pfx, msg):
    #1
    """Called by Sender. Adds message type, length prefixes and sends"""
    len_pfx = len(msg)
    len_pfx = str(len_pfx).rjust(4, '0')
    packed_msg = f'{typ_pfx}{len_pfx}{msg}'
    sock.send(packed_msg.encode())


def unpack_msg(client_cnxn, shed_byte=False):
    #1
    """Unpacks prefix for file size, and returns trimmed message as bytes.
        
        This method does not read the message type. Call receiver() before
                invoking this method or remove the first byte before reading.
                Once the input has been routed, this helper function is called
                to unpack the user inputs. 
        """

    if shed_byte:  # Removes prefix
        client_cnxn.recv(1)

    sz_pfx = client_cnxn.recv(4)
    buffer = _pfxtoint(client_cnxn, sz_pfx, 4)
    trim_msg = client_cnxn.recv(buffer)

    return trim_msg


def _pfxtoint(client_cnxn, data, n=4):
    #1
    """Converts size prefix data to int."""
    return int(data[:n])


def init_client_data(sock):
    """Sets nick and addr of user."""
    unique = False
    PROMPT = '-+- Enter nickname:'

    pack_n_send(sock, 'M', PROMPT)
    while not unique:
        # sock.recv(1)  # Shed first byte.
        user_name = unpack_msg(sock, shed_byte=True).decode()

        if user_name not in nicks_by_sock.values():
            nicks_by_sock[sock] = user_name  # Create socket:nick pair.
            addrs_by_nick[user_name] = sockets[sock]  # Create nick:addr pair.
            unique = True
        else:
            ERR = f"=!= They're already here! Pick something else:"
            print(ERR)
            pack_n_send(sock, 'M', ERR)

    # TODO: Fix formatting.
    return user_name


addy = ('127.0.0.1', 1515)
sock = socket.socket()
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addy)
except Exception as e:
    print(f'-x- {e}')
    utils.countdown(90)

sock.listen(5)
print('-+- Listening...')
Thread(target=accepting).start()
