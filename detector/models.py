# Simple stub for now, or use SQLAlchemy
import sqlite3

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp DATETIME,
            status TEXT,
            ip_address TEXT,
            location TEXT,
            details TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS blocked_ips (
            ip_address TEXT PRIMARY KEY,
            blocked_at DATETIME,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

class Log:
    pass
