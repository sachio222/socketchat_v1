#!/usr/bin/python3

import socket
import os

class FileXfer():
    """For file transfer, sending and receiving.
    """
    def __init__(self, client_socket):
        pass

    def sender_prompt(self, client_socket, path='', recip=''):
        """For the sender, takes in filepath and send confirmation.
        """
        while True:
            path = self._get_path(path)
            if not path:
                break

            recip = self._get_recip(recip)
            if not recip:
                break
        
            while True:
                conf = input(f'-+- Confirm send to {recip}: {path}\n-+- (y or n): ')
                if conf.lower() == 'y':
                    #
                    # Here: Send accept prompt to client. 
                    #
                    self.send_filesize(path, client_socket)
                    # encrypt file
                    self.xfer_file(path, client_socket)
                    # break

                elif conf.lower() == 'n':
                    self._user_did_cancel('cancel')
                    break

            break

        print('chat awy')
        

    def recip_prompt(self, path, filesize):
        print(f'Accept {path} of size {filesize} bytes? | (y or n) \n')
        input('>> ')

    def send_filesize(self, path, client_socket):
        with open('image.jpg', 'rb') as f:
            self.filesize = os.path.getsize('image.jpg')

        client_socket.send(str(self.filesize).encode())  # HackyAF
        return self.filesize

    def xfer_file(self, path, client_socket):
        # This is fine. It's just going to start pouring in the data.
        with open('image.jpg', 'rb') as f:
            client_socket.sendfile(f, 0, self.filesize)
            # client_socket.send(f'filesize is: {filesize}'.encode())
        # client_socket.close()

    def receive_file(self, data, BUFFSIZE, filesize, client):
        try:
            data = client.recv(BUFFSIZE)
            bytes_recd = len(data)
            print("STARTING=========")
            with open('image(2).jpg', 'wb') as f:
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
    
    def _get_path(self, path):
        print("-+- Send file to recipient. (Type 'cancel' at any time.)")
        while not os.path.exists(path):
            path = input("-+- Input filepath >> ")

            if self._user_did_cancel(path):
                path = ''
                break

            elif not os.path.exists(path):
                print("x-x File or path doesn't exist. Check yer work, bud.")

            else:
                # remove absolute path if there is one
                path = os.path.basename(path)
        
        return path

    def _get_recip(self, nick):
        while not self._valid_recip(nick):
            nick = input("-+- Recipient's handle?: @")

            if self._user_did_cancel(nick):
                nick = ''
                break

            elif not self._valid_recip(nick):
                print("x-x Maybe pick someone in this room?")

        return nick

    def _user_did_cancel(self, inp_str):
        if inp_str.lower() == 'cancel':
            print('x-x Send file cancelled. Continue chatting.')
            return True
        else:
            return False

    def _valid_recip(self, nick):
        # check if nick is real.
        if nick:
            return True
        else:
            return False
