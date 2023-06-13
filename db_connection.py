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
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query, tupel)
    conn.commit()
    cursor.close()
    conn.close()

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
    :return: True, wenn übergebenes Passwort == DB-Passwort des übergebenen Users, ansonsten False
    """
    query = "SELECT hashpassword FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)
    if (len(db_result) == 0): return False
    return (db_result[0][0] == hashed_password)

def create_new_user(username, hashed_password):
    """
    Erstellt den User in der DB und setzt das Startkapital auf 5000 Cent.
    """
    startCapital = 5000
    query = "INSERT INTO user_data (username, hashpassword, capital) VALUES (?, ?, ?)"
    tupel = (username, hashed_password, startCapital)
    insert_into_db(query, tupel)