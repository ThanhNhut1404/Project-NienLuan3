# database.py
import sqlite3

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT,
            name TEXT,
            email TEXT,
            birthdate TEXT,
            gender TEXT,
            phone TEXT,
            face_encoding TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(user_id, name, email, birthdate, gender, phone, encoding_json):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (id, name, email, birthdate, gender, phone, face_encoding)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, email, birthdate, gender, phone, encoding_json))
    conn.commit()  # ✅ cần commit
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, face_encoding FROM users")
    rows = c.fetchall()
    conn.close()
    return [{'id': row[0], 'name': row[1], 'face_encoding': row[2]} for row in rows]

def user_exists(user_id, name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE id = ? AND name = ?", (user_id, name))
    result = c.fetchone()
    conn.close()
    return result is not None

def reset_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()

def reset_and_upgrade_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute('''
        CREATE TABLE users (
            id TEXT,
            name TEXT,
            email TEXT,
            birthdate TEXT,
            gender TEXT,
            phone TEXT,
            face_encoding TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()  # ✅ cần commit
    conn.close()
