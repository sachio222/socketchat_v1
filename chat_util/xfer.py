#!/usr/bin/python3

import socket
import os

CHUNK_SIZE = 4096
# path = 'image.jpg'
path = 'VSCode-darwin-stable.zip'

class SendFile():
    def __init__(self, client_socket):
        # self.client_socket = client_socket
        pass
    
    def sender_prompt(self, client_socket):
        while True:
            path = input("Input filepath or type 'cancel':\n >> ")
            if path == 'cancel':
                print('Send file cancelled. Continue chatting.')
                break
            else:
                if os.path.exists(path):
                    # remove absolute path if there is
                    path = os.path.basename(path)
                else:
                    print("File or path doesn't exist. Check yer work, bud.")
                    break

                conf = input(f'Confirm send: \n- {path} | (y or n): ')
                if conf.lower() == 'y':
                    # check if file exists
                
                    # encrypt file
                    print('Sending...')
                    self.send_filesize(path, client_socket)
                    self.xfer_file(path, client_socket)
                    break
                
                elif conf.lower() == 'n':
                    print('Send file cancelled. Continue chatting.')
                    break
    
    def send_filesize(self, path, client_socket):
        with open('image.jpg', 'rb') as f:
            self.filesize = os.path.getsize('image.jpg')
        
        client_socket.send(str(self.filesize).encode()) # HackyAF
        return self.filesize

    def xfer_file(self, path, client_socket):
        # This is fine. It's just going to start pouring in the data. 
        with open('image.jpg', 'rb') as f:
            client_socket.sendfile(f, 0, self.filesize)
            # client_socket.send(f'filesize is: {filesize}'.encode())
        # client_socket.close()


    def receive_file(self, data, BUFFSIZE, filesize, client):
        # Begin to overwrite
        try:
            data = client.recv(BUFFSIZE)
            bytes_recd = len(data)
            print("STARTING=========")
            # print(data)
            with open('image(2).jpg','wb') as f:
                # f.write(data) 
                while bytes_recd < int(filesize):
                    f.write(data)
                    data = client.recv(BUFFSIZE)
                    if data == b'':
                        raise RuntimeError("socket connection broken")
                    bytes_recd = bytes_recd + len(data)
                    print(bytes_recd)
                    # with open('image(2).jpg', 'ab') as f:
                    
        except ValueError:
            pass
        print("FINISHED==========")
        # sock.close()
                    