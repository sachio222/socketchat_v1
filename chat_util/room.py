class Room():
    def __init__(self):
        pass

    def get_status(self, addresses, nicks):
        people = []
        for addr in addresses:
            person = nicks[addr].decode()
            people.append(f'@{person}') 

        ppl_qty = len(people)
        ppl_lst = ', '.join(people)

        # Outputs
        # @YO: 4 online - @Jake, @toof, @veronica, @pizzanator
        room_status = f'{ppl_qty} online - {ppl_lst}'
        
        return room_status.encode() # to bytes

        