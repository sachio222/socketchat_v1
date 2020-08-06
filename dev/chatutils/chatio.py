import os
import sys
import socket
from threading import Thread


class ChatIO():
    def __init__(self):
        self.LEN_PFX_LEN = 4

    def pack_n_send(self, sock, typ_pfx, msg):
        #1
        """Called by Sender. Adds message type, length prefixes and sends
        
        typ_pfx: (Type prefix) 1 byte. tells recipient how to handle message. 
        len_pfx: (Length prefix) 4 bytes. tells socket when to stop receiving message.

        Example packet:
            M0005Hello - Message type, 5 characters, "Hello"
        """

        len_pfx = len(msg)
        len_pfx = str(len_pfx).rjust(self.LEN_PFX_LEN, '0')
        packed_msg = f'{typ_pfx}{len_pfx}{msg}'
        sock.send(packed_msg.encode())

    def unpack_msg(self, sock):
        #1
        """Unpacks prefix for file size, and returns trimmed message as bytes.
        
        This method does not read the message type. Call receiver() before
                invoking this method. Once the input has been routed, this
                helper function is called to unpack the already sorted user
                inputs. 
        """

        sz_pfx = sock.recv(self.LEN_PFX_LEN)
        buffer = self._pfxtoint(sock, sz_pfx, n=self.LEN_PFX_LEN)
        trim_msg = sock.recv(buffer)

        return trim_msg  # As bytes

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

