import socket

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 1121))
server_socket.listen(5)
print('waiting...')

while True:
    client_socket, addr = server_socket.accept()
    with open('VSCode-darwin-stable.zip', 'rb') as f:
        client_socket.sendfile(f, 0)
    print('file received')
    client_socket.close()
