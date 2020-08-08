#!/usr/bin/python3
"""Encryptochat 2.0
"""

import os
import sys
import socket
from threading import Thread, Lock

from chatutils import utils
from chatutils.xfer import FileXfer
from chatutils.chatio import ChatIO


class Client(ChatIO):

    def __init__(self):
        super(Client, self).__init__()
        self.message_type = 'M'
        self.msg = ''

    #===================== SENDING METHODS =====================#
    def sender(self):
        #0
        """Accepts user input, checks type, and begins sending to recip.

        Accepts input, and checks if it's a command. If it's prefixed with a '/'
                Then it is routed to the inp_ctrl_handler where different
                controls are mapped. If it doesn't begin with '/', it's treated
                as a generic message. 
        """
        while True:
            self.msg = input('')
            if self.msg:
                if self.msg[0] == '/':
                    typ_pfx = 'C'
                    self.inp_ctrl_handler(self.msg)
                else:
                    typ_pfx = self.message_type
                    self.pack_n_send(serv_sock, typ_pfx, self.msg)
            else:
                self.msg = ''


    def inp_ctrl_handler(self, msg):
        #0
        """Sorts through input control messages and calls controller funcs."""
        if type(msg) == bytes:
            msg.decode()

        if msg == '/help':
            # Print help menu
            path = 'config/helptxt.txt'
            utils.print_from_file(path)
            
        elif msg == '/sendfile':
            # For sending file. Call send dialog.
            # Send as controller file to server and recipient.
            # self.pack_n_send(serv_sock, 'C', '/sendfile')

            path = xfer.sender_prompt()
            user = xfer.user_prompt(serv_sock)

            # For username lookup.
            # Send U-type message to server with user as message.
            # if path and user:
            #     path
                # Send U flag.
                # serv_sock.send(b'T')


        else:
            print('-!- Command not recognized.')

    #===================== RECEIVING METHODS =====================#
    def receiver(self):
        #1
        """A Threaded socket that calls a function to check message type."""
        while True:
            typ_pfx = serv_sock.recv(1)
            if not typ_pfx:
                serv_sock.close()
                print("-!- Aw, snap. Server's disconnected.")
                break
            self._inb_typ_hndlr(typ_pfx)

    def _inb_typ_hndlr(self, typ_pfx):
        #0
        """Called by Receiver. Routes messages based on message type.
        
        Checks messages for type. M is standard message. F is sending a file.
                C is for a controller message. A is for file acceptance. Routes
                every type to a dedicated handler.
        
        """
        typ_pfx = typ_pfx.decode().upper()

        if typ_pfx == 'M':
            # Standard message type.
            self._m_hndlr()
        elif typ_pfx == 'F':
            # For sending files.
            self._f_hndlr()
        elif typ_pfx == 'C':
            # For controller input.
            self._c_hndlr()
        elif typ_pfx == 'A':
            # For dialog messages for file sending.
            self._a_hndlr()
        elif typ_pfx == 'U':
            # User Found
            self._u_hndlr()
        elif typ_pfx == 'V':
            # User Found
            self._v_hndlr()
        elif typ_pfx == 'X':
            # Transfer file.
            self._x_hndlr()
        else:
            print('-x- Unknown message type error.')

    def _m_hndlr(self):
        #0
        """Standard message. Unpacks message, and prints to own screen."""
        trim_msg = self.unpack_msg(serv_sock)
        self.print_message(trim_msg)

    def _f_hndlr(self):
        #0
        """File Recipient. Prompts to accept or reject. Sends response."""

        # Incoming filename and filesize.
        incoming_f_sz = self.unpack_msg(serv_sock)
        print(incoming_f_sz.decode())
        print('-?- Do you want to accept this file? (Y/N)'
             )  #  TODO <-- come from server
        choice = input('>>')
        # print("Sending here, ths is fine")
        self.pack_n_send(serv_sock, 'A', choice)

        # Accept file
        if choice == 'n':
            pass
        elif choice == 'y':
            # Bring in the file!!
            pass

    def _c_hndlr(self):
        #0
        """Control messages from another user. Not displayed."""

        trim_msg = self.unpack_msg(serv_sock)

    def _a_hndlr(self):
        #0
        """Recipient Acceptance. Yes or no"""

        choice = self.unpack_msg(serv_sock)
        print(choice)
        print("sending")
        if choice.decode().lower() == 'y':
            print('sending')
            with open('image.jpg', 'rb') as f:
                # Sends message to send file.
                serv_sock.send(b'X')
                serv_sock.sendfile(f, 0)
        elif choice.lower() == 'n':
                # Sends message that file transfer is over.
            self.pack_n_send(serv_sock, 'M', '-=- Transfer Cancelled.')

    def _u_hndlr(self):
        """Receives server response from user lookup.
        
        After the server looks up a user, it sends its response as a U-type.
        The U type message either prompts the recipient if the exist, or asks
        the sender to re-enter their user choice.

        """
        user_exists = self.unpack_msg(serv_sock)

        if user_exists == "False":
            print("didn't find em. Try again.")
            self.message_type = 'U'

        if user_exists == "True":
            print('we found em go do next thing.')
            self.message_type = 'M'

        # user_exists = self.unpack_msg(serv_sock).decode()
        # print("-=- Checking recipient...")
        # print(f'user exists: {user_exists}')

        # if user_exists:
        #     # filesize = self.get_filesize('image.jpg', serv_sock)
        #     filesize = 78404
        #     msg = f"{filesize}"
        #     self.pack_n_send(serv_sock, 'F', msg)
        # else:
        #     print("User does not exist. Try again or type 'cancel'")
        #     return

    def _v_hndlr(self):
        pass


    def _x_hndlr(self):
        """File sender. Transfer handler."""

        chunk = serv_sock.recv(BFFR)
        
        xfer.write_to_path(chunk, 'file(2).txt')
        # bytes_recd = len(chunk)

        # with open('image[2].jpg', 'wb') as f:
        #     while bytes_recd < 78223:
        #         f.write(chunk)
        #         chunk = serv_sock.recv(BFFR)
        #         bytes_recd += len(chunk)

    def start(self):
        self.t1 = Thread(target=self.receiver)
        self.t2 = Thread(target=self.sender)
        self.t1.start()
        self.t2.start()
        self.lock = Lock()


if __name__ == "__main__":

    BFFR = 4096
    host = '127.0.0.1'
    # port = int(input('-=- Port, please: '))

    # DEBUG
    port = 1515

    xfer = FileXfer()
    channel = Client()

    serv_sock = socket.socket()
    serv_sock.connect((host, port))

    print(f'-+- Connected to {host}')
    # name = serv_sock.recv(BFFR)
    # print(name.decode())

    channel.start()
