import sqlite3
from flask import g

DATABASE = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def initialize_database():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        ''')
        conn.commit()

def add_user(username, email, password_hash):
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.OperationalError as e:
        print("OperationalError in add_user:", e)
        return False

def _row_to_dict(row):
    if row is None:
        return None
    return {
        'id': row['id'],
        'username': row['username'],
        'email': row['email'],
        'password_hash': row['password_hash']
    }

def get_user_by_username(username):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    return _row_to_dict(user)

def get_user_by_email(email):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    return _row_to_dict(user)
