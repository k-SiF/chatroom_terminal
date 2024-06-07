import hashlib
import os

USER_DATA_FILE = 'users.txt'
FORMAT = 'utf-8'

class User:
    def __init__(self, username, conn):
        self.username = username
        self.conn = conn
        self.permission_level = 1  # Default permission level

    def get_username(self):
        return self.username

    def set_permission_level(self, level):
        self.permission_level = level

    def get_permission_level(self):
        return self.permission_level

    def send_message(self, message):
        try:
            self.conn.sendall(message.encode(FORMAT))
        except Exception as e:
            print(f"Error sending message: {e}")

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode(FORMAT)).hexdigest()

    @staticmethod
    def register(username, password):
        hashed_password = User.hash_password(password)
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f'{username},{hashed_password},1\n')  # Default permission level is 1

    @staticmethod
    def authenticate(username, password):
        hashed_password = User.hash_password(password)
        if not os.path.exists(USER_DATA_FILE):
            return False, None
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username, stored_password, permission_level = line.strip().split(',')
                if stored_username == username and stored_password == hashed_password:
                    return True, int(permission_level)
        return False, None