import os
from . import utils
from .chatio import ChatIO



class FileXfer(ChatIO):
    """FileXfer 2.0 - For file transfer, sending and receiving."""

    def __init__(self):
        super(FileXfer, self).__init__()
        self.filesize = None

    def sender_prompts(self, sock, path='', user=''):
        while True:
            
            # Get filepath and filesize.
            path, self.filesize = self._get_file_info(path)
            if not path:
                break
            
            # Get user.
            user = self._get_username(sock)
            if not user:
                break
            
            break

        return path, user

    def recip_prompt(self, sock, filename=None, filesize=None, user=None):
        """Sends filename and filesize. Prompts user to accept file transfer.
        
        Args:
            filename: (str) The name of the incoming file.
            filesize: (int) Size of incoming file in bytes.
        """

        print('Here is your prompt to accept.')

    def _get_file_info(self, path):
        """Validate if selected file exists, and get filesize.

        Input:
            path: (string) a file location.

        Returns:
            path: (str or path??) a path to an existing file.
            filesize: (int) bytes of file at path
        """
        
        filesize = None

        print("-=- Send file to recipient (or type cancel).")
        while not os.path.exists(path):
            path = input("-=- Input filepath >> ")

            if self._user_did_cancel(path):
                path = ''
                break

            elif not os.path.exists(path):
                print("x-x File or path doesn't exist. Check yer work, bud.")

            else:
                # remove absolute path if there is one
                path = os.path.basename(path)
                filesize = os.path.getsize(path)

        return path, filesize

    def _get_username(self, sock, user=''):
        """ Returns valid recipient for file send."""

        while not user:
            user = input('-=- Send to >> @')

            if self._user_did_cancel(user):
                user = ''
                break
            
            print(f'-=- Looking up {user}...')

        return user

    def _user_did_cancel(self, inp_str):
        """Returns true if inp_str is canceled, and shows message. """

        if inp_str.lower() == 'cancel':
            print('x-x Send file cancelled. Continue chatting.')
            return True

        else:
            return False

    def write_to_path(self, chunk, path):
        # Dynamically set socket size.
        main, ext = utils.split_path_ext(path)
        # Open socket
        print("Receiving dawg!")
        if os.path.exists(path):
            path = f"{main}(1).{ext}"

        with open(path, 'wb') as f:
            f.write(chunk)

    

    #### SERVER METHODS ###

    # def waiting_for_accept(self, client_cnxn, user):
        # """Checks if user exists in user dict."""

        # EXISTS_MSG = '-=- Waiting for user to accept.'

        # return 