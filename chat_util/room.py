#!/usr/bin/ python3

import sys


class Room():
    """Returns room details"""

    def __init__(self):
        pass

    def get_status(self, addresses, nicks):
        """Returns people in the room when called, and outputs to channel"""
        people = []
        for addr in addresses:
            person = nicks[addr].decode()
            people.append(f'@{person}')

        ppl_qty = len(people)
        ppl_lst = ', '.join(people)

        # Outputs
        # @YO: 4 online - @Jake, @toof, @veronica, @pizzanator
        room_status = f'{ppl_qty} online - {ppl_lst}'

        return room_status.encode()  # to bytes


class Chime:
    # Ring my bell, ring my bell
    def __init__(self):
        self.muted = False

    def play(self):
        if not self.muted:
            sys.stdout.write("\a")
            sys.stdout.flush()
        else:
            return
