"""SOCKETCHAT SECURE by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with sec-client.py and chat via the cli.
-+- Libraries required.

"""

import os
import sys
import socket
from threading import Thread
from cryptography.fernet import Fernet

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

class Cipher():
    def __init__(self):
        #self.generate_key()
        self.key = self.load_key()
        self.f = Fernet(self.key)

    def generate_key(self):
        self.key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)

    def load_key(self):
        return open('secret.key', 'rb').read()

    def encrypt(self, msg):
        msg = msg.encode() # byte encode
        enc_msg = self.f.encrypt(msg)
        return enc_msg

    def decrypt(self, msg):
        dec_msg = self.f.decrypt(msg)
        return dec_msg

    def split(self, raw_msg):
        """Separates message from raw_msg from server.

        Returns:
            handle: (str) user name
            cipher_msg: (bytes)
        """

        SEPARATOR = ': '
        raw_msg = msg.decode() # to str
        _split = msg.split(SEPARATOR)
        handle = _split[0]
        cipher_msg = _split[1].encode() # to bytes
        return handle, cipher_msg


def welcome_msg():

    # Sned @user handle
    while True:
        handle = input("Enter your handle:\n@")
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
            
            handle, cip_msg = cipher.split(incoming)

            try:
                plain_text = cipher.decrypt(cip_msg).decode() # To str
                incoming = f'{handle}{plain_text}' 
            except:
                incoming = incoming.decode() # Fallback

            # Clear line when new text comes in (otherwise it'll glitch out.)
            sys.stdout.write(ERASE_LINE)

            # Display with some sort of colors
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")

            # Bell
            chime.play()

        except OSError:
            break


def send(msg=''):
    # Outgoing!!
    while msg != 'exit()':
        if msg == 'mute()':
            chime.muted = True
        elif msg == 'unmute()':
            chime.muted = False
        else:
            msg = input('')
            msg = cipher.encrypt(msg)
            client.send(msg.encode())

    # Close on exit()
    client.close()
    print('Disconnected.')
    exit()


# Instantiate sound
chime = Chime()
cipher = Cipher()

if __name__ == '__main__':

    host = input('-+- Enter hostname of server: ')
    if not host:
        # Set default
        host = 'ubuntu'

    port = input('-+- Choose port: ')
    if not port:
        # Set default
        port = 12222
    else:
        port = int(port)

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
