import db_connection


class Player:

    def __init__(self, username):
        self.username = username
        self.wants_to_play = False
        self.credit = self.loadData()

    def loadData(self):
        return db_connection.get_credit(self.username)

