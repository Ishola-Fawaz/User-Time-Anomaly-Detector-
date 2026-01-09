import sys
import os

# Ensure we can import detector.core
sys.path.append(os.getcwd())

from detector.core import process_login

def test_login(role, hour, expected_status):
    # Mock a login event
    event = {
        'user_id': role,
        'timestamp': f'2024-01-01 {hour:02d}:00:00',
        'ip': '127.0.0.1',
        'success': True
    }
    
    result = process_login(event)
    status = result['status']
    
    print(f"Role: {role:<10} | Time: {hour:02d}:00 | Expected: {expected_status:<15} | Actual: {status:<15} | {'PASS' if status == expected_status else 'FAIL'}")
    if status != expected_status:
        print(f"   -> Details: {result}")

print("--- Running Verification Tests ---")
# Student: 8-17
test_login('student', 14, 'normal_login')    # 2 PM - OK
test_login('student', 20, 'abnormal_login')  # 8 PM - FAIL

# Guard: 18-6
test_login('guard', 20, 'normal_login')      # 8 PM - OK
test_login('guard', 0, 'normal_login')       # 0 AM - OK
test_login('guard', 2, 'normal_login')       # 2 AM - OK
test_login('guard', 10, 'abnormal_login')    # 10 AM - FAIL

# Admin: 0-24
test_login('admin', 3, 'normal_login')       # 3 AM - OK
test_login('admin', 15, 'normal_login')      # 3 PM - OK

print("--- Done ---")
