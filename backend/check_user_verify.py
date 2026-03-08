from secure_database import SecureDatabase
import sqlite3

db = SecureDatabase()
conn = sqlite3.connect(db.db_path)
cursor = conn.cursor()

target_email = "manichandana7002@gmail.com"
cursor.execute("SELECT user_id, email_encrypted, account_locked, login_attempts FROM users")
rows = cursor.fetchall()

print(f"DEBUG: Total users in DB: {len(rows)}")
found = False
for user_id, email_enc, locked, attempts in rows:
    try:
        decrypted_email = db._decrypt_data(email_enc)
        print(f"DEBUG: User in DB: '{decrypted_email}' (Length: {len(decrypted_email)})")
        if target_email.lower().strip() == decrypted_email.lower().strip():
            print(f"✅ FOUND MATCHING USER")
            print(f"ID: {user_id}")
            print(f"Locked: {locked}")
            print(f"Attempts: {attempts}")
            found = True
    except Exception as e:
        print(f"Error decrypting user {user_id}: {e}")

if not found:
    print(f"❌ No exact match found for '{target_email}'")

conn.close()
