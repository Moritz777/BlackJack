import pyodbc

#DATABASE INFORMATION
server = 'provadis-it-ausbildung.de'
database = 'BlackJack03'
username = 'BlackJackUser03'
password = 'ProvadisBlackJackUser03__'
connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

def insert_into_db(query, tupel):
    """
    Stellt Verbindung zur DB her und führt übergebene INSERT-Abfrage aus.
    """
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, tupel)
        conn.commit()
        cursor.close()
        conn.close()
    except pyodbc.Error as ex:
        print("Fehler beim Ausführen des INSERT-Statements:")
        print(ex)

def select_from_db(query, tupel):
    """
    Stellt Verbindung zur DB her und führt übergebene SELECT-Abfrage aus.
    :return: Datensätze als Liste aus Tupels [(a,b),(x,y)]. Wenn keine Datensätze, dann []
    """
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query, tupel)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def check_login(username, hashed_password):
    """
    Sucht zu "username" das zugehörige Passwort in der DB und vergleicht es mit "hashed_password".
    :return: True, wenn Username in DB existiert UND das Passwort stimmt, ansonsten False
    """
    query = "SELECT hashpassword FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)
    if (len(db_result) == 0): return False # Benutzername existiert nicht
    return (db_result[0][0] == hashed_password) # Passwort stimmt oder stimmt nicht

def check_username(username):
    """
    Sucht nach "username" in der DB.
    :return: True, wenn Datensatz zum Username existiert, ansonsten False
    """
    query = "SELECT username FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)
    return (len(db_result) != 0) # Benutzername existiert / existiert nicht

def create_new_user(username, hashed_password, startCapital, first_name, last_name, birthday):
    """
    Erstellt den User in der DB.
    """
    query = "INSERT INTO user_data (username, hashpassword, capital, firstname, lastname, birthdate) VALUES (?, ?, ?, ?, ?, ?)"
    tupel = (username, hashed_password, startCapital, first_name, last_name, birthday)
    insert_into_db(query, tupel)


def get_credit(username):
    query = "SELECT capital FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)
    return db_result[0][0]


def check_admin(username):
    query = "SELECT is_admin FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)
    print(db_result[0][0])
    return db_result[0][0] is True


def get_all_players():
    query = "SELECT username,capital,firstname,lastname,birthdate,is_blocked FROM user_data WHERE is_admin IN (0, ?)"
    tupel = (1)
    db_result = select_from_db(query, tupel)
    return db_result

# UPDATE user_data
# SET birthdate = '2023-10-25', firstname = 'Erikkk', lastname = 'Beforeman'
# WHERE player_id = 23;

# player_id	int	NULL
# username	varchar	16
# hashpassword	varchar	64
# capital	int	NULL
# firstname	varchar	128
# lastname	varchar	128
# birthdate	varchar	10