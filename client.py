#!/usr/bin/python3

"""SOCKETCHAT by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with client.py and chat via the cli.
-+- Works out of the box with Python3. No libraries needed.
"""

import os
import sys
import socket
from threading import Thread
from chat_util import ping

BUFFSIZE = 4096  # Upped for encryption
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class Chime:
    # Ring my bell, ring my bell
    def __init__(self):
        self.muted = False

    def play(self):
        if not self.muted:
            sys.stdout.write("\a")
        else:
            return


def welcome_msg():

    # Sned @user handle
    while True:
        handle = input("-+- Enter your handle:\n@")
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
            incoming = incoming.decode()

            if not incoming:
                print('You got disconnected, Foo. Get back in there!')
                break

            # Clear line when new text comes in (otherwise it'll glitch out.)
            sys.stdout.write(ERASE_LINE)

            # Bell
            chime.play()

            # Display with some sort of colors
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")

        except OSError:
            break


def send(msg=''):
    # Outgoing!!
    while msg != 'exit()':
        try:
            if msg == 'mute()':
                chime.muted = True
                print(
                    '\x1b[4;32;40m@YO: Silent mode. Turn on sound with unmute().\x1b[0m'
                )

            elif msg == 'unmute()':
                chime.muted = False
                print(
                    '\x1b[4;32;40m@YO: B00p! Turn sound off with mute().\x1b[0m'
                )

            elif msg.lower() == 'ping':
                reply = pngsrvr.ping()
                print(f'\x1b[4;32;40m@YO: {reply}\x1b[0m')

            msg = input('')
            client.send(msg.encode())

        except OSError:
            break
    # Close on exit()

    client.close()
    print('Disconnected.')
    exit()


# Instantiate sound
chime = Chime()

if __name__ == '__main__':

    host = input('-+- Enter hostname of server: ')
    host = host or 'ubuntu'

    port = input('-+- Choose port: ')
    port = port or '12222'
    port = int(port)

    # Create ping object
    pngsrvr = ping.Server(host, port)

    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))  # Opens socket connect if server running.
    except:
        client.connect((host, port))  # For debug

    welcome_msg()

    # Start send/receive threads
    receive_thread = Thread(target=receive)
    receive_thread.start()
    send_thread = Thread(target=send)
    send_thread.start()
