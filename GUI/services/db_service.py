import psycopg2
from config.settings import DB_CONFIG
from psycopg2 import sql

class DBService:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()
        self._ensure_users_table()
 
    def _ensure_users_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL,
                UNIQUE(username)
            )
        ''')
        self.conn.commit()

    def signup_user(self, username, email, password_hash):
        try:
            self.cur.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)', (username, email, password_hash))
            self.conn.commit()
            return True
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False

    def login_user(self, email, password_hash):
        self.cur.execute('SELECT * FROM users WHERE email=%s AND password_hash=%s', (email, password_hash))
        return self.cur.fetchone() is not None

    def is_unique_email(self, email):
        self.cur.execute('SELECT 1 FROM users WHERE email=%s', (email,))
        return self.cur.fetchone() is None

    def is_unique_username(self, username):
        self.cur.execute('SELECT 1 FROM users WHERE username=%s', (username,))
        return self.cur.fetchone() is None

    def close(self):
        self.cur.close()
        self.conn.close() 