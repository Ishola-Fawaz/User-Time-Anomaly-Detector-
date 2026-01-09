import sqlite3
import random
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../database.db')

def create_connection():
    return sqlite3.connect(DB_PATH)

def setup_db():
    conn = create_connection()
    c = conn.cursor()
    # Re-create table for fresh start
    c.execute('DROP TABLE IF EXISTS logs')
    c.execute('''
        CREATE TABLE logs (
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

def generate_normal_data(user_id, start_hour, end_hour, days=30):
    conn = create_connection()
    c = conn.cursor()
    
    base_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    print(f"Generating data for {user_id} between {start_hour}:00 and {end_hour}:00...")
    
    for i in range(days):
        day = base_date + datetime.timedelta(days=i)
        
        # 1-3 logins per day
        res = random.randint(1, 3)
        for _ in range(res):
            # Pick a random hour in the window
            hour = random.randint(start_hour, end_hour - 1)
            minute = random.randint(0, 59)
            
            # Add some variance (std dev ~ 1 hour)
            # Clip to 0-23
            
            ts = day.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Simulated data
            ip = '192.168.1.1' # Normal IP
            location = 'New York, USA'
            status = 'success'
            details = ''
            
            c.execute('INSERT INTO logs (user_id, timestamp, status, ip_address, location, details) VALUES (?, ?, ?, ?, ?, ?)',
                      (user_id, ts.isoformat(), status, ip, location, details))
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_db()
    
    # User A: Office worker (9 AM - 5 PM)
    generate_normal_data('user_a', 9, 17)
    
    # User B: Night shift (10 PM - 4 AM) -> 22 to 28 (modulo 24 handled below? No, simplifed for now)
    # Let's do 22 to 2 (next day) manually or just say 18-24
    generate_normal_data('user_b', 18, 23) 
    
    print("Data generation complete.")
