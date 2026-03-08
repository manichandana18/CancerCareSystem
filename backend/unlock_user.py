from secure_database import SecureDatabase
import sqlite3

db = SecureDatabase()
conn = sqlite3.connect(db.db_path)
cursor = conn.cursor()

target_email = "24eg107a62@anurag.edu.in"
cursor.execute("SELECT user_id, email_encrypted FROM users")
rows = cursor.fetchall()

unlocked = False
for user_id, email_enc in rows:
    decrypted_email = db._decrypt_data(email_enc)
    if decrypted_email.lower() == target_email.lower():
        cursor.execute("UPDATE users SET account_locked = 0, login_attempts = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        print(f"✅ Successfully unlocked account: {user_id} ({decrypted_email})")
        unlocked = True
        break

if not unlocked:
    print(f"❌ User with email {target_email} not found in database.")

conn.close()
