import hashlib
import pyodbc

from user_class import User

server = 'provadis-it-ausbildung.de'
database = 'BlackJack03'
username = 'BlackJackUser03'
password = 'ProvadisBlackJackUser03__'
connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

capital = 5678


def connect_sql(nutzername, hashed_password):

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    query = "INSERT INTO user_data (username, hashpassword, capital) VALUES (?, ?, ?)"
    cursor.execute(query, (nutzername, hashed_password, capital))
    conn.commit()

    cursor.close()
    conn.close()

def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password

def userRegistry():
    while True:
        username = input("Username: ")
        user_password = input("Passwort: ")
        user_password_repeat = input("Passwort wiederholen: ")
        if (user_password == user_password_repeat):
            hashed_password = hash_password(user_password)
            #user_object = User()
            connect_sql(username, hashed_password)
            print("erfolgreich")
            break
        else:
            print("Passwörter stimmen nicht überein. Bitte Versuche es erneut.")

def userLogin():
    username = input("Username: ")
    user_password = input("Passwort: ")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = "SELECT hashpassword FROM user_data WHERE username = ?"
    cursor.execute(query, (username))

    result = cursor.fetchone()

    if(result[0] == hash_password(user_password)):
        print(username + " angemeldet")
    else:
        print("Ihr Nutzer und Passwort stimmen nicht überein Sie Hund")

    conn.close()

def test():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    query = "SELECT * FROM user_data WHERE username = ?"
    cursor.execute(query, username)

    result = cursor.fetchone()
    print(result)


# NUR KONSOLENLOGIK
if __name__ == "__main__":
    #test()
    # Anmeldung
    while True:
        print("Registrieren: 1 | Anmelden: 2")
        option = input()

        if option == "1":
            userRegistry()
            break
        elif option == "2":
            userLogin()
            break
        else:
            print("Gib 1 oder 2 ein jesus christ")

    # current_user = "Eymen"

    # aabb = User(8, "Erik", "abcd", 5000)
    # a.change_username("Peter")
    # print(a.username)

# Funktionstest
# a = check_login("Sven", "5")
# b = check_login("Sven", "6")
# print(a, b)
