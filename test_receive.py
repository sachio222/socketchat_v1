import socket

CHUNK_SIZE = 8 * 1024

sock = socket.socket()
print('Opened...')
sock.connect(('127.0.0.1', 1121))
print('connected')
chunk = sock.recv(CHUNK_SIZE)
print('receiving i guess?')
while chunk:
    chunk = sock.recv(CHUNK_SIZE)
    with open('newfile', 'ab') as f:
        f.write(chunk)
    print('received nothing')
sock.close()
