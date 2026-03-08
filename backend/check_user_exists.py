from secure_database import SecureDatabase
import sqlite3

db = SecureDatabase()
conn = sqlite3.connect(db.db_path)
cursor = conn.cursor()

target_email = "24eg107a62@anurag.edu.in"
cursor.execute("SELECT user_id, email_encrypted, account_locked, login_attempts FROM users")
rows = cursor.fetchall()

print(f"Total users in DB: {len(rows)}")
found = False
for user_id, email_enc, locked, attempts in rows:
    decrypted_email = db._decrypt_data(email_enc).lower().strip()
    if target_email.lower().strip() == decrypted_email:
        print(f"✅ FOUND MATCHING USER")
        print(f"ID: {user_id}")
        print(f"Email: {decrypted_email}")
        print(f"Locked: {locked}")
        print(f"Attempts: {attempts}")
        found = True
    elif "anurag" in decrypted_email or "24eg" in decrypted_email:
        print(f"PARTIAL MATCH: {decrypted_email} (ID: {user_id})")

if not found:
    print(f"❌ No exact match found for {target_email}")

conn.close()
