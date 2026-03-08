import sqlite3
import hashlib
import secrets
import os
from pathlib import Path
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from secure_database import SecureDatabase

def reset_password(email, new_password):
    db = SecureDatabase()
    
    # 1. Find user by email
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, email_encrypted FROM users")
    users = cursor.fetchall()
    
    target_user_id = None
    for user_id, email_enc in users:
        decrypted_email = db._decrypt_data(email_enc).strip()
        if decrypted_email.lower() == email.lower().strip():
            target_user_id = user_id
            break
    
    if not target_user_id:
        print(f"❌ User {email} not found")
        conn.close()
        return False
    
    # 2. Hash new password
    new_hash = db._hash_password(new_password)
    
    # 3. Update database
    cursor.execute("UPDATE users SET password_hash = ?, login_attempts = 0, account_locked = 0 WHERE user_id = ?", (new_hash, target_user_id))
    conn.commit()
    conn.close()
    
    print(f"✅ Password for {email} reset to: {new_password}")
    return True

if __name__ == "__main__":
    reset_password("test@cancercare.ai", "CancerCare2024!")
