import sqlite3
import base64

def try_xor(data, key):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

db_path = 'cancercare_secure.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT email_encrypted FROM users LIMIT 1")
row = cursor.fetchone()
if row:
    enc = row[0]
    print(f"Encrypted email: {enc}")
    
    # Try Base64
    try:
        dec = base64.b64decode(enc).decode('utf-8')
        print(f"Base64 Decoded: {dec}")
    except:
        pass

conn.close()
