import pyodbc

#DATABASE INFORMATION
server = 'provadis-it-ausbildung.de'
database = 'BlackJack03'
username = 'BlackJackUser03'
password = 'ProvadisBlackJackUser03__'
connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

def check_login(username, password):
    query = "SELECT hashpassword FROM user_data WHERE username = ?"
    tupel = (username)
    db_result = select_from_db(query, tupel)


# def get_capital(username):
#     query = "SELECT capital FROM user_data WHERE username = ?"
#     tupel = (username)
#     select_from_db(query, tupel)

def write_in_db(query):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    query = "INSERT INTO user_data (username, hashpassword, capital) VALUES (?, ?, ?)"
    cursor.execute(query, (nutzername, hashed_password, capital))
    conn.commit()

    cursor.close()
    conn.close()

def select_from_db(query, tupel):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(query, tupel) # erst Statement, dann alle Parameter als Tupel, wodurch "?" ersetzt werden
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

check_login("Peter", "xxx")