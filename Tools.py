import hashlib

def hash_password(password):
    """
    Verschlüsselt das Passwort mit dem SHA-256 Algorithmus.
    :return: Gehashtes Passwort als 64-stellige Zeichenkette.
    """
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    return hashed_password