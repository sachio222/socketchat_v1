#!/usr/bin/ python3

"""SOCKETCHAT SECURE by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with sec-client.py and chat via the cli.
-+- Libraries required.

"""

import os
import sys
import time
import socket
from threading import Thread
from chat_util import ping, xfer, room

from encryption.fernet import Cipher

BUFFSIZE = 4096  # Upped for encryption
ERASE_LINE = '\x1b[2K'


class Chime:
    # Ring my bell, ring my bell
    def __init__(self):
        self.muted = False

    def play(self):
        if not self.muted:
            sys.stdout.write("\a")
            sys.stdout.flush()
        else:
            return


def welcome_msg():

    # Sned @user handle
    while True:
        handle = input("-+- Enter your handle:\n-+- @")
        if handle:
            break
    client.send(handle.encode())

    # Get message from server
    from_server = client.recv(BUFFSIZE)
    print(f"\x1b[4;32;40m{from_server.decode()}\x1b[0m")


def receive():
    # Incoming broadcasts!!
    while True:
        try:
            incoming = client.recv(BUFFSIZE)

            try:
                handle, cip_msg = cipher.split(incoming)
                plain_text = cipher.decrypt(cip_msg).decode()  # To str
                incoming = f'{handle}: {plain_text}'

            except:
                incoming = incoming.decode()  # Fallback

            if not incoming:
                break

            # Clear line when new text comes in (otherwise it'll glitch out.)

            sys.stdout.write(ERASE_LINE)
            # sys.stdout.flush()

            # Bell
            chime.play()

            # Display with some sort of colors
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")

        except OSError:
            break


def send(msg=''):
    # Outgoing!!
    while msg != 'exit()':

        msg = input('')

        if msg == 'exit()' or msg == 'status()':
            # Passthru server side controls
            pass

        elif msg == 'sendfile()':
            # Send incoming image alert
            client.send(msg.encode())
            f_xfer.sender_prompt(client)
            # f_xfer.send_filesize(None, client)
            # print(decision)
            # f_xfer.xfer_file(None, client)
            # else:
            #     print('File transfer declined.')

        elif msg == 'mute()':
            chime.muted = True
            print(
                '\x1b[4;32;40m@YO: Silent mode. Turn on sound with unmute().\x1b[0m'
            )

        elif msg == 'unmute()':
            chime.muted = False
            print('\x1b[4;32;40m@YO: B00p! Turn sound off with mute().\x1b[0m')

        elif msg.lower() == 'ping':
            reply = pngsrvr.ping()
            print(f'\x1b[4;32;40m@YO: {reply}\x1b[0m')

        else:
            msg = cipher.encrypt(msg).decode()  #Decodes and then encodes again

        client.send(msg.encode())

    # Close on exit()
    client.close()
    print('Disconnected.')
    exit()


# Instantiate sound
chime = room.Chime()
cipher = Cipher()

if __name__ == '__main__':

    host = input('-+- Enter hostname of server: ')
    host = host or 'ubuntu'

    #TESTING#
    # host = '127.0.0.1'

    port = input('-+- Choose port: ')
    port = port or '12222'
    port = int(port)

    #TESING
    # port = 1414

    # Create ping object
    pngsrvr = ping.Server(host, port)

    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))  # Opens socket connect if server running.
    except:
        # TESTING
        print('Port not available. Try again.')
        exit()

    # Instantiate file transfer class
    f_xfer = xfer.FileXfer(client)

    welcome_msg()

    # Start send/receive threads
    receive_thread = Thread(target=receive)
    receive_thread.start()
    send_thread = Thread(target=send)
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    client.close()
