import os
import sys
import socket
from threading import Thread

ENC = 'utf8'
BUFFSIZE = 2048
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


class Chime:

    def __init__(self):
        self.muted = False

    def play(self):
        if not self.muted:
            sys.stdout.write("\a")
        else:
            return


def welcome_msg():

    # Get handle
    while True:
        handle = input("Enter your handle:\n@")
        if handle:
            break

    client.send(handle.encode(ENC))

    from_server = client.recv(BUFFSIZE)
    print(f"\x1b[4;32;40m{from_server.decode()}\x1b[0m")


def receive():
    while True:
        try:
            incoming = client.recv(BUFFSIZE)
            incoming = incoming.decode()
            sys.stdout.write(ERASE_LINE)

            # Bell
            chime.play()
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")

        except OSError:
            break


def send(msg=''):
    while msg != 'exit()':
        if msg == 'mute()':
            chime.muted = True
        elif msg == 'unmute()':
            chime.muted = False

        msg = input('')
        client.send(msg.encode(ENC))

    client.close()
    print('Disconnected.')
    exit()


chime = Chime()

if __name__ == '__main__':

    HOST = input('-+- Enter hostname of server: ')
    if not HOST:
        HOST = 'ubuntu'

    PORT = input('-+- Choose port: ')
    if not PORT:
        PORT = 12222
    else:
        PORT = int(PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))  # Opens socket connect if server running.
    except:
        client.connect((HOST, PORT))  # Opens socket connect if server running.

    welcome_msg()

    receive_thread = Thread(target=receive)
    receive_thread.start()
    send_thread = Thread(target=send)
    send_thread.start()
