#!/usr/bin/ python3

import socket
import sys
import time
from threading import Thread

import chatutils.xfer as xfer
import chatutils.utils as utils
from chatutils.chatio import ChatIO

BFFR = 4096
sockets = {}
nicks_by_sock = {}
addrs_by_nick = {}

sox = {}

class Server(ChatIO):
    def __init__(self):
        super(Server, self).__init__()


    def accepting(self):
        # Accept connections.
        while True:
            client_cnxn, client_addr = sock.accept()
            print(f'-+- Connected... to {client_addr}')
            sockets[client_cnxn] = client_addr  # Create cnxn:addr pairings.
            Thread(target=self.handle_clients, args=(client_cnxn,)).start()


    def handle_clients(self, client_cnxn):
        # Get username.
        user_name = self.init_client_data(client_cnxn)
        self.pack_n_send(client_cnxn, 'M', f"{user_name} is in the house!")

        # Start listening.
        while True:
            data = client_cnxn.recv(BFFR)  # Receive data as chunks.

            if not data:
                #TODO: Run through connected sockets, clean up list.
                del (addrs_by_nick[nicks_by_sock[client_cnxn]])
                print('addrs_by_nick: ', addrs_by_nick)
                del (nicks_by_sock[client_cnxn])
                print('nicks_by_sock: ', nicks_by_sock)
                del (sockets[client_cnxn])  # remove address
                print('sockets: ', sockets)

                break

            self.data_router(client_cnxn, data)


    def data_router(self, client_cnxn, data):
        # Server client communication codes.

        # Send confirm dialog to recip if user is sending file.
        if data[0] == "/".encode():
            print('controller')

            # Drain socket of controller message so it doesn't print.
            self.unpack_msg(client_cnxn)

        # U-type handler
        if data[0] == 85: # 85 = U
            print('raw U data', data)

            user = self.remove_pfx(data) # Clean already recv'd data.
            print('user', user)
            user_exists, _ = self.lookup_user(client_cnxn, user)

            self.pack_n_send(client_cnxn, 'U', str(user_exists))

        else:
            for sock in sockets:
                if sockets[sock] != sockets[client_cnxn]:
                    # print(sock)
                    try:
                        sock.send(data)

                    except:
                        pass
        
        # General print to server.
        print(data)


    def recv_pkt(self, client_cnxn, data, n):
        return int(data[:n])


    def file_confirm_prompt(self, client_cnxn, data):
        """Checks if user exists in user dict."""

        data = data[5:]  # Remove prefixes.
        user_exists, user_addr = self.lookup_user(client_cnxn, data)
        if user_exists:
            EXISTS_MSG = '-=- Waiting for user to accept.'
            data = EXISTS_MSG
            user_addr = user_addr
        else:
            data = ''

        return data


    def lookup_user(self, sock, user_query):
        #YUP
        """Checks if user exists. If so, returns user and address.

        Args: 
            sock: (socket) Incoming socket object (from sender)
            user_query: (str) Name of user to look up.
        
        Returns
            match: (bool) True if user found
            user_addr: (str) ip:port of user.
        """
        match = False
        user_addr = None

        try:
            user_query = user_query.decode()
        except:
            pass
        
        for nick, addr in addrs_by_nick.items():
            if addr != sockets[sock]:  # Avoid self match.

                if nick == user_query:
                    print(f'Found {nick}')
                    match = True
                    user_addr = addr
                    print(f'recip-addy: {user_addr}')
                    
                    break

                else:
                    print(f'User {user_query} not found.') 
        
        print(f'match: {match}')
        return match, user_addr


    def init_client_data(self, sock):
        """Sets nick and addr of user."""
        unique = False
        PROMPT = '-+- Enter nickname:'

        self.pack_n_send(sock, 'M', PROMPT)
        while not unique:
            # sock.recv(1)  # Shed first byte.
            user_name = self.unpack_msg(sock, shed_byte=True).decode()

            if user_name not in nicks_by_sock.values():
                nicks_by_sock[sock] = user_name  # Create socket:nick pair.
                addrs_by_nick[user_name] = sockets[sock]  # Create nick:addr pair.
                unique = True
            else:
                ERR = f"=!= They're already here! Pick something else:"
                print(ERR)
                self.pack_n_send(sock, 'M', ERR)

        # TODO: Fix formatting.
        return user_name

if __name__ == "__main__":

    server = Server()

    addy = ('127.0.0.1', 1515)
    sock = socket.socket()
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(addy)
    except Exception as e:
        print(f'-x- {e}')
        utils.countdown(90)

    sock.listen(5)
    print('-+- Listening...')
    Thread(target=server.accepting).start()
