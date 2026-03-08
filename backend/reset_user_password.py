from secure_database import SecureDatabase
import sqlite3

db = SecureDatabase()
target_email = "manichandana7002@gmail.com"
new_password = "Password123!" # Temporary password

with sqlite3.connect(db.db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email_encrypted FROM users")
    rows = cursor.fetchall()
    
    found_user_id = None
    for user_id, email_enc in rows:
        if db._decrypt_data(email_enc).lower().strip() == target_email.lower().strip():
            found_user_id = user_id
            break
    
    if found_user_id:
        new_hash = db._hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ?, login_attempts = 0, account_locked = 0 WHERE user_id = ?", 
                     (new_hash, found_user_id))
        conn.commit()
        print(f"✅ Password for {target_email} has been reset to: {new_password}")
    else:
        print(f"❌ User {target_email} not found.")
