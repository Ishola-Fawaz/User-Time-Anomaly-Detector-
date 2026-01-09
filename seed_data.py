import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd
from detector.core import process_login
from detector.models import DB_NAME, init_db

def seed_database():
    print("Initializing Database...")
    init_db()
    
    # Clear existing logs for a fresh start
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM logs")
    c.execute("DELETE FROM blocked_ips")
    conn.commit()
    conn.close()
    print("Cleared existing logs.")

    start_date = datetime.now() - timedelta(days=7)
    roles = ['student', 'guard', 'admin']
    
    total_entries = 0
    
    for i in range(8): # 7 days + today
        current_day = start_date + timedelta(days=i)
        date_str = current_day.strftime('%Y-%m-%d')
        print(f"Generating logs for {date_str}...")
        
        # --- STUDENT LOGS (Day: 08-17) ---
        # Generate 15 normal, 2 abnormal
        for _ in range(15):
            # Normal: 08:00 to 17:00
            hour = random.randint(8, 16) 
            minute = random.randint(0, 59)
            ts = f"{date_str} {hour:02d}:{minute:02d}:00"
            process_login({'user_id': 'student', 'timestamp': ts, 'success': True, 'ip': '192.168.1.10'})
            total_entries += 1
            
        for _ in range(2):
            # Abnormal: 20:00 - 23:00
            hour = random.randint(20, 23)
            minute = random.randint(0, 59)
            ts = f"{date_str} {hour:02d}:{minute:02d}:00"
            process_login({'user_id': 'student', 'timestamp': ts, 'success': True, 'ip': '192.168.1.10'})
            total_entries += 1

        # --- GUARD LOGS (Night: 18-06) ---
        # Generate 10 normal, 1 abnormal
        for _ in range(10):
            # Normal: 18:00 to 05:00 next day (handle simplified as just hours)
            # We pick hours: 18,19,20,21,22,23,00,01,02,03,04,05
            hours = [18,19,20,21,22,23,0,1,2,3,4,5]
            hour = random.choice(hours)
            minute = random.randint(0, 59)
            ts = f"{date_str} {hour:02d}:{minute:02d}:00"
            process_login({'user_id': 'guard', 'timestamp': ts, 'success': True, 'ip': '10.0.0.5'})
            total_entries += 1

        for _ in range(1):
             # Abnormal: 10:00 - 14:00
            hour = random.randint(10, 14)
            minute = random.randint(0, 59)
            ts = f"{date_str} {hour:02d}:{minute:02d}:00"
            process_login({'user_id': 'guard', 'timestamp': ts, 'success': True, 'ip': '10.0.0.5'})
            total_entries += 1

        # --- ADMIN LOGS (Anytime) ---
        for _ in range(5):
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            ts = f"{date_str} {hour:02d}:{minute:02d}:00"
            process_login({'user_id': 'admin', 'timestamp': ts, 'success': True, 'ip': '192.168.1.99'})
            total_entries += 1

    print(f"--- FISHED ---")
    print(f"Generated {total_entries} entries.")
    print("Database populated successfully.")

if __name__ == "__main__":
    seed_database()
