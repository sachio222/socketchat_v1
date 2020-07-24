import sys
import socket
from threading import Thread

enc = 'utf8'
BUFFSIZE = 2048

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def welcome_msg():

    # Get handle
    while True:
        handle = input("Enter your handle:\n@")
        if handle:
            break

    client.send(handle.encode(enc))

    from_server = client.recv(BUFFSIZE)
    print(f"\x1b[4;32;40m{from_server.decode()}\x1b[0m\n")


def receive():
    while True:
        try:
            incoming = client.recv(BUFFSIZE)
            incoming = incoming.decode()
            sys.stdout.write(ERASE_LINE)
            print(f"\r\x1b[1;33;40m{incoming}\x1b[0m")
            Thread(target=send).start()
        except OSError:
            break


def send(msg=''):
    while msg != 'exit()':
        msg = input('')
        client.send(msg.encode(enc))

    client.close()
    print('Disconnected.')
    exit()


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
