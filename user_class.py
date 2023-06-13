import db_connection


class User:
    def __init__(self, username, hash_password, capital):
        self.userid = None
        self.username = username
        self.hash_password = hash_password
        self.capital = 5000
        db_connection.create_new_user(username, hash_password, capital)

    def change_username(self, new_username):
        self.username = new_username
