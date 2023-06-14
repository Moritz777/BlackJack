from player_class import Player
from session import session


class control:
    def __init__(self):
        self.session_list = []
        self.my_initial_session = session()
        self.session_list.append(self.my_initial_session)

    def choose_session(self,player):
        if len(self.session_list[-1].player_list) == 7:
            new_session = session()
            self.session_list.append(new_session)
            self.session_list[-1].player_list.append(player)
        else:
            self.session_list[-1].player_list.append(player)


    def create_new_player(self, username):
        new_player = Player(username)


