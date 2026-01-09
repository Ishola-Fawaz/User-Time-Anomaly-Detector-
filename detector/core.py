import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
from detector.models import DB_NAME

# Mock IP Location DB
GEO_DB = {
    '192.168.1.1': 'New York, USA',
    '10.0.0.1': 'London, UK',
    '127.0.0.1': 'Localhost'
}

# START: Simple Role-Based Windows for Demonstration
# This is explicitly hardcoded so it's easy to explain in a presentation.
# Format: 'username': (Start_Hour_24h, End_Hour_24h)
USER_WINDOWS = {
    'student': (8, 17),    # Day access only (8 AM - 5 PM)
    'guard': (18, 6),      # Night shift only (6 PM - 6 AM)
    'admin': (0, 24)       # All day access
}

def get_location(ip):
    return GEO_DB.get(ip, 'Unknown Location')

def load_data():
    """ 
    Previously used for training baselines. 
    Now just a placeholder or for basic DB checks if needed.
    """
    return {}

def get_recent_logs(user_id=None, limit=50):
    conn = sqlite3.connect(DB_NAME)
    try:
        if user_id:
            query = "SELECT user_id, timestamp, status, ip_address, location, details FROM logs WHERE user_id = ? ORDER BY id DESC LIMIT ?"
            params = (user_id, limit)
        else:
            query = "SELECT user_id, timestamp, status, ip_address, location, details FROM logs ORDER BY id DESC LIMIT ?"
            params = (limit,)
            
        df = pd.read_sql_query(query, conn, params=params)
        if df.empty: return []
        return df.to_dict('records')
    except:
        return []
    finally:
        conn.close()

def is_ip_blocked(ip):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM blocked_ips WHERE ip_address = ?", (ip,))
    row = c.fetchone()
    conn.close()
    return row is not None

def block_ip(ip, reason="Brute Force Detected"):
    if is_ip_blocked(ip): return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO blocked_ips (ip_address, blocked_at, reason) VALUES (?, ?, ?)", 
              (ip, datetime.now(), reason))
    conn.commit()
    conn.close()
    print(f"BLOCKED IP: {ip}")

def check_brute_force(ip):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Check last 5 logs for this IP
    c.execute("SELECT status FROM logs WHERE ip_address = ? ORDER BY id DESC LIMIT 5", (ip,))
    rows = c.fetchall()
    conn.close()
    
    if not rows: return False

    failures = 0
    for r in rows:
        if r[0] == 'failed':
            failures += 1
        else:
            break
            
    if failures >= 3:
        block_ip(ip)
        return True
    return False

def process_login(event):
    """
    Process a login event with strictly defined rules.
    """
    user_id = event.get('user_id', 'unknown')
    ip = event.get('ip', '127.0.0.1')
    success = event.get('success', True)
    timestamp_str = event.get('timestamp')
    
    # 1. Check if Blocked
    if is_ip_blocked(ip):
        return {"status": "blocked", "msg": "IP is blocked."}

    # 2. Determine Log Status & Details
    location = get_location(ip)
    final_status = 'success' if success else 'failed'
    violation_details = ""
    score = 0.0

    if not success:
        # Check Brute Force
        if check_brute_force(ip):
            final_status = "blocked"
            violation_details = "Brute force attempts exceeded limit"
    else:
        # Security Checks: STRICT TIME WINDOW ONLY
        # This removes the "black box" statistical Z-score.
        
        ts = pd.to_datetime(timestamp_str)
        login_hour = ts.hour
        
        # Get window for user, default to standard business hours (9-5) if unknown
        window = USER_WINDOWS.get(user_id, (9, 17))
        start_h, end_h = window
        
        is_outside = False
        
        # Logic to check if time is within start_h and end_h
        if start_h < end_h:
            # Standard day window (e.g., 8 to 17)
            # Valid if: start <= hour < end
            if not (start_h <= login_hour < end_h):
                is_outside = True
        else:
            # Crosses midnight (e.g., 18 to 6)
            # Valid if: hour >= start OR hour < end
            if not (login_hour >= start_h or login_hour < end_h):
                is_outside = True

        if is_outside:
            final_status = "abnormal_login"
            score = 10.0 # Max risk score
            violation_details = f"Login prohibited: Outside assigned hours ({start_h}:00 - {end_h}:00)"
        else:
            final_status = "normal_login"
            score = 0.0
            violation_details = "Authorized login: Within assigned hours"


    # 3. Log to Database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs (user_id, timestamp, status, ip_address, location, details) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, timestamp_str, final_status, ip, location, violation_details))
    conn.commit()
    conn.close()

    return {
        "status": final_status,
        "score": score,
        "details": {"violation": violation_details} if violation_details else {},
        "msg": violation_details or "Login processed successfully"
    }
