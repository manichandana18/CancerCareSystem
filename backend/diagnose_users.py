import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from secure_database import SecureDatabase

def diagnose():
    db = SecureDatabase()
    print("--- Database Diagnosis ---")
    
    # Check users
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, email_encrypted, account_locked, login_attempts FROM users")
        users = cursor.fetchall()
        
        print(f"Total users: {len(users)}")
        for u in users:
            email = db._decrypt_data(u[1])
            print(f"User ID: {u[0]}, Email: {email}, Locked: {u[2]}, Attempts: {u[3]}")

if __name__ == "__main__":
    diagnose()
