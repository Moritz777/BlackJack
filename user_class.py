import db_connection


class User:
    def __init__(self, username, hash_password, first_name, last_name, birthday_formatted):
        self.userid = None
        self.username = username
        self.hash_password = hash_password
        self.capital = 5000
        self.first_name= first_name
        self.last_name = last_name
        self.birthday = birthday_formatted
        db_connection.create_new_user(self.username, self.hash_password, self.capital, self.first_name, self.last_name, self.birthday)

    def change_username(self, new_username):
        self.username = new_username
