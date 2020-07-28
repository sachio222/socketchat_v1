#!/usr/bin/python3

import os
import time
import socket


class FileXfer():
    """For file transfer, sending and receiving."""

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
                conf = input(
                    f'-+- Confirm send to {recip}: {path}\n-+- (Y or N) >> ')
                if conf.lower() == 'y':
                    #
                    # Here: Send accept prompt to client.
                    #
                    self.send_filesize(path, client_socket)
                    # HERE: encrypt file
                    print('waiting')
                    # data = client_socket.recv(2048)
                    # print('done')
                    self.xfer_file(path, client_socket)
                    break

                elif conf.lower() == 'n':
                    self._user_did_cancel('cancel')
                    break

            break

    def recip_prompt(self, path, filesize):
        """Prompts to show file recipient."""

        print(f'Accept {path} of size {filesize} bytes? | (y or n) \n')
        input('>> ')

    def send_filesize(self, path, client_socket):
        """Calculates filesize of a path and sends integer."""

        with open('image.jpg', 'rb') as f:
            self.filesize = os.path.getsize(f)

        client_socket.send(str(self.filesize).encode())  # HackyAF
        return self.filesize

    def xfer_file(self, path, server_socket):
        """Opens file at path, sends to server_socket."""

        with open(path, 'rb') as f:
            server_socket.sendfile(f, 0, self.filesize)

    def receive_file(self, data, BUFFSIZE, filesize, client):
        """Download file transfer from server."""

        try:
            data = client.recv(BUFFSIZE)
            bytes_recd = len(data)
            print("STARTING=========")

            # target_path = self._set_target_path()

            with open('image(2).jpg', 'wb') as f:
                while bytes_recd < int(filesize):
                    f.write(data)
                    data = client.recv(BUFFSIZE)
                    bytes_recd = bytes_recd + len(data)
                    print(bytes_recd)
                    print(data)
                    if data == b'':
                        raise RuntimeError("socket connection broken")

        except ValueError:
            pass
        print("FINISHED==========")
        # sock.close()

    def _get_path(self, path):
        """Validate if selected file exists. 

        Input:
            path: (string) a file location.

        Returns:
            path: (str or path??) a path to an existing file.
        """

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

    def _set_target_path(self):
        """Adds number if file with same name exists."""

        ### TODO: Finish this.
        target_path = ''

        return target_path

    def _get_recip(self, nick):
        """ Returns valid recipient for file send."""

        ### TODO: Finish this.

        while not self._valid_recip(nick):
            nick = input("-+- Recipient's handle?: @")

            if self._user_did_cancel(nick):
                nick = ''
                break

            elif not self._valid_recip(nick):
                print("x-x Maybe pick someone in this room?")

        return nick

    def _valid_recip(self, nick):
        """Returns true if username matches member in room."""

        ### TODO: Finish this.

        if nick:
            return True
            
        else:
            return False

    def _user_did_cancel(self, inp_str):
        """Returns true if inp_str is canceled, and shows message. """

        if inp_str.lower() == 'cancel':
            print('x-x Send file cancelled. Continue chatting.')
            return True

        else:
            return False
