def check_login(username, password):
    query = "SELECT hashpassword FROM user_data WHERE username = ?"

def connect_to_db(username, hashed_password):
