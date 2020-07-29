#!/usr/bin/ python3
"""SOCKETCHAT SECURE by J. Krajewski, 2020, All rights reserved.

-+- Spin up server.py, connect to it with sec-client.py and chat via the cli.
-+- Libraries required.

"""

import os
import sys
import time
import socket
import argparse
from threading import Thread, Lock
from encryption.fernet import Cipher
from chat_util import ping, xfer, room


class RoomIO():

    def __init__(self):
        self.msg = ''
        self.BFFR = 4096

    def welcome(self):
        while True:
            handle = input("-+- Enter your handle:\n-+- @")
            if handle:
                break

        self._xmit(handle.encode(), self.cli_sock)

        # Get message from server
        incoming = self.cli_sock.recv(self.BFFR)
        self._print_msg(incoming.decode(), 'green')

    def send(self):
        # Outgoing!!

        while self.msg != 'exit()':

            self.msg = input('')

            self.msg, bypass_e = self._msg_handler(self.msg)

            if self.is_encrypted:
                if not bypass_e:
                    self.msg = cipher.encrypt(self.msg)
                else:
                    self.msg = self.msg.encode()
            else:
                self.msg = self.msg.encode()

            self._xmit_with_lock(self.msg, self.cli_sock)

        # self.cli_sock.shutdown(socket.SHUT_RDWR)
        self.cli_sock.close()
        print('Disconnected')
        exit()

    def receive(self):

        while True:
            # Incoming!!
            incoming = self.cli_sock.recv(self.BFFR)

            if not incoming:
                self._print_msg('You got disconnected, Foo! Get back in there!',
                                'green')
                break
            if self.is_encrypted:
                try:
                    # Decrypt if encrypted.
                    incoming = self._decipher_incoming(incoming)

                except:
                    # Fb if message not encrypted.
                    incoming = incoming.decode()
            else:
                incoming = incoming.decode()

            self._print_msg(incoming, 'yellow')

        exit()

    def _xmit(self, bytes_data, sending_sock):
        sending_sock.send(bytes_data)

    def _xmit_with_lock(self, bytes_data, sending_sock):
        """Transmit with thread locking."""

        with lock:
            sending_sock.send(bytes_data)

    def _decipher_incoming(self, bytes_data):
        """If encrypted, decipher, return string."""

        handle, cip_msg = cipher.split(bytes_data)
        plain_text = cipher.decrypt(cip_msg).decode()  # To str
        return f'{handle}: {plain_text}'

    def _print_msg(self, str_data, style='yellow'):
        """Show string on screen."""

        # Clear line when new text comes in (otherwise it'll glitch out).
        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(ERASE_LINE)

        chime.play()

        if style == 'yellow':
            print(f"\r\x1b[1;33;40m{str_data}\x1b[0m")

        elif style == 'green':
            print(f"\x1b[4;32;40m{str_data}\x1b[0m")

    def _msg_handler(self, msg):

        # Send these commands as plaintext to server.
        bypass = True

        if msg == 'status()' or msg == "exit()":
            pass

        elif msg == 'sendfile()':
            f_xfer.sender_prompt(self.cli_sock)

        elif msg == 'mute()':
            chime.muted = True
            confirm_msg = '@YO: Silent mode. Turn on sound with unmute().'
            self._print_msg(confirm_msg, 'green')

        elif msg == 'unmute()':
            chime.muted = False
            confirm_msg = "B00p! Turn sound off with mute()."
            self._print_msg(confirm_msg, 'green')

        elif msg == 'ping()' or msg == 'ping':
            reply = pngsrvr.ping()
            self._print_msg(reply, 'green')

        else:
            # Do not send through plaintext.
            bypass = False

        return msg, bypass

    def start(self, cli_sock, is_encrypted=True):
        self.is_encrypted = is_encrypted
        self.cli_sock = cli_sock
        self.welcome()
        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        send_thread = Thread(target=self.send)
        send_thread.start()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Lightweight encrypted chat.',
                                     epilog='Going under...')

    parser.add_argument('-g',
                        '--goober',
                        help='Goober chat, or no encryption.',
                        action='store_false',
                        dest='is_encrypted')

    addr_group = parser.add_mutually_exclusive_group()

    addr_group.add_argument(
        '-f',
        '--full-address',
        help='Input full address. eg: xxx.xxx.xxx.xxx:######',
        action='store',
        type=str,
        dest='addr')
    addr_group.add_argument(
        '-H',
        '--host',
        help='Input host name or address. eg: xxx.xxx.xxx.xxx',
        action='store',
        type=str,
        dest='host')

    parser.add_argument('-P',
                        '--port',
                        help='Input port number.',
                        action='store',
                        type=int,
                        dest='port')

    args = parser.parse_args()

    if not args.addr:
        if not args.host:
            host = input('-+- Enter hostname of server: ')
            host = host or 'ubuntu'
        else:
            host = args.host
            print(f'-+- Hostname: {host}')

        if not args.port:
            port = input('-+- Choose port: ')
            port = port or '12222'
            port = int(port)
        else:
            port = args.port
            print(f'-+- Port: {port}')

    # else:
    #     try:
    #         addr = args.addr
    #         addr = addr.split(':')
    #         host = addr[0]
    #         port = int(addr[1])

    #     except:
    #         pass

    #TESTING#
    # host = '127.0.0.1'
    # port = 1414

    # Create ping object
    pngsrvr = ping.Server(host, port)
    chime = room.Chime()
    cipher = Cipher()
    channel = RoomIO()
    f_xfer = xfer.FileXfer()

    # Create client socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock = Lock()
        cli_sock.connect((host, port))  # Connect to server addy.
        channel.start(cli_sock, args.is_encrypted)

    except:
        # TODO: descriptive errors
        print("Connection not successful. Try again.")
        # cli_sock.shutdown(socket.SHUT_RDWR)
        cli_sock.close()
        exit()
