import hashlib
import pyodbc

server = 'provadis-it-ausbildung.de'
database = 'BlackJack03'
username = 'BlackJackUser03'
password = 'ProvadisBlackJackUser03__'
connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

class User:
    def __init__(self, userid, username, hash_password, capital):
        self.userid = userid
        self.username = username
        self.hash_password = hash_password
        self.capital = capital

    def change_username(self, new_username):
        self.username = new_username