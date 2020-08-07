import os
from . import utils
from .chatio import ChatIO



class FileXfer(ChatIO):
    """FileXfer 2.0 - For file transfer, sending and receiving."""

    def __init__(self):
        super(FileXfer, self).__init__()

    def sender_prompts(self, path='', user=''):
        while True:
            path = self._get_path(path)
            if not path:
                break
            user = self._get_user(user)
            if not user:
                break

            break
        return path, user

    def _get_path(self, path):
        """Validate if selected file exists. 

        Input:
            path: (string) a file location.

        Returns:
            path: (str or path??) a path to an existing file.
        """

        print("-=- Send file to recipient. (Type 'cancel' at any time to return to chat.)")
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

        return path

    def _get_user(self, nick):
        """ Returns valid recipient for file send."""

        ### TODO: Finish this.

        while not self._valid_recip(nick):
            
            user = input('-=- Send to: @')
            
            if self._user_did_cancel(nick):
                nick = None
                break
            
            elif not self._valid_recip(nick):
                print("x-x Maybe pick someone in this room?")

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