import os
import sys
import socket
from threading import Thread


class ChatIO():
    def __init__(self):
        self.LEN_PFX_LEN = 4

    def pack_n_send(self, sock, typ_pfx, msg):
        #1
        """Called by sender. Adds message type and length prefixes and sends.
        
        typ_pfx: (Type prefix) 1 byte. tells recipient how to handle message. 
        len_pfx: (Length prefix) 4 bytes. tells socket when to stop receiving message.

        Args
            sock: (socket) Sending socket. Used with send method.
            typ_pfx: (str) A single char message type prefix read by the
                            recieving socket.
            msg: (str) Message that is sent.

        Example packet:
            b'M0005Hello' - Message type, 5 characters, "Hello"
            msg[0] - Message type
            msg[1:4] - Message length
            msg[5:] - Message
        """

        len_pfx = len(msg)
        len_pfx = str(len_pfx).rjust(self.LEN_PFX_LEN, '0')
        packed_msg = f'{typ_pfx}{len_pfx}{msg}'
        sock.send(packed_msg.encode())

    def unpack_msg(self, sock, shed_byte=False):
        #1
        """Unpacks prefix for file size, and returns trimmed message as bytes.
        
        This method does not read the message type. Call receiver() before
        invoking this method or else remove the first byte before reading with
        shed_byte=True. Once the input has been routed, this helper function is
        called to unpack the already sorted user inputs. 

        Args
            sock: (socket) Listening socket. Used with recv.
            shed_byte: (bool) Remove the 1st byte (type prefix)

        Returns
            trim_msg: (bytes) Message without prefixes.
        """

        if shed_byte:  # Removes type prefix
            sock.recv(1)

        sz_pfx = sock.recv(self.LEN_PFX_LEN)
        buffer = self._pfxtoint(sock, sz_pfx, n=self.LEN_PFX_LEN)
        trim_msg = sock.recv(buffer)

        return trim_msg # As bytes

    def _pfxtoint(self, client_cnxn, data, n=4):
        #1
        """Converts size prefix data to int."""
        return int(data[:n])

    def print_message(self, msg, style='yellow'):
        #1
        """Print message to screen.
        TODO
            add fun formatting.
            
        """

        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(ERASE_LINE)

        if type(msg) == bytes:
            msg = msg.decode()

        print(f'\r{msg}')


    def remove_pfx(self, data, n=5):
        # Accepts bytes input, chops off prefix and returns plain message as bytes.
        return data[5:]