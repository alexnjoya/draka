import hashlib
import re
from GUI.services.db_service import DBService

class UserService:
    def __init__(self):
        self.db = DBService()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def signup(self, username, email, password):
        if not self.is_valid_email(email):
            return 'Invalid email format.'
        if not self.db.is_unique_email(email):
            return 'Email already exists.'
        if not self.db.is_unique_username(username):
            return 'Username already exists.'
        password_hash = self.hash_password(password)
        if self.db.signup_user(username, email, password_hash):
            return True
        return 'Signup failed. Please try again.'

    def login(self, email, password):
        password_hash = self.hash_password(password)
        return self.db.login_user(email, password_hash)

    def close(self):
        self.db.close() 