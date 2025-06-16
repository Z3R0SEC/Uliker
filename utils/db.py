import sqlite3

DB_FILE = "session.db"

def DBconn():
    con = sqlite3.connect(DB_FILE, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def init():
    conn = DBconn()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, uid TEXT, name TEXT, photo TEXT, token TEXT, cookie TEXT)')
    conn.commit()
    conn.close()

def check(email):
    conn = DBconn()
    return conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

def upsert(email, password, uid, name, photo, token, cookie):
    conn = DBconn()
    user = check(email)

    if user:
        conn.execute(
            'UPDATE users SET password = ?, uid = ?, name = ?, photo = ?, token = ?, cookie = ? WHERE email = ?',
            (password, uid, name, photo, token, cookie, email)
        )
    else:
        conn.execute(
            'INSERT INTO users (email, password, uid, name, photo, token, cookie) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (email, password, uid, name, photo, token, cookie)
        )
    conn.commit()
    conn.close()

def tokens():
    conn = DBconn()
    cursor = conn.execute('SELECT token FROM users WHERE token IS NOT NULL')
    tokens = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tokens
