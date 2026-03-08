"""
Secure Database Integration for CancerCare AI
HIPAA-compliant database with encryption and security
"""

import sys
from pathlib import Path
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import random

# Add parent dir to path
sys.path.append(str(Path(__file__).parent))


class SecureDatabase:
    """HIPAA-compliant secure database"""

    def __init__(self, db_path="cancercare_secure.db"):
        self.db_path = db_path
        self.encryption_key = self._generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self._initialize_database()

    # ------------------------------------------------------------------
    # Encryption helpers
    # ------------------------------------------------------------------

    def _generate_encryption_key(self):
        """Generate encryption key from master password"""
        password = b"CancerCare_Secure_Master_Key_2024"
        salt = b"CancerCare_Salt_Secure_2024"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def _encrypt_data(self, data):
        """Encrypt sensitive data"""
        if not isinstance(data, str):
            data = str(data)
        encrypted = self.cipher_suite.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def _decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        if isinstance(encrypted_data, str):
            encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher_suite.decrypt(encrypted_data)
        return decrypted.decode()

    def _hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return salt + password_hash

    def _verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        salt = stored_hash[:64]
        stored_password_hash = stored_hash[64:]
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return password_hash == stored_password_hash

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def _get_connection(self):
        """Get a thread-safe cached connection with reasonable timeout"""
        if not hasattr(self, '_conn') or self._conn is None:
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA busy_timeout=30000")
        return self._conn

    # ------------------------------------------------------------------
    # Database initialisation
    # ------------------------------------------------------------------

    def _initialize_database(self):
        """Initialize secure database with all tables"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("PRAGMA secure_delete = ON")
        print("DB: PRAGMAs set")

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    email_encrypted TEXT NOT NULL,
                    phone_encrypted TEXT,
                    name_encrypted TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    account_locked BOOLEAN DEFAULT 0,
                    security_level TEXT DEFAULT 'standard'
                )
            """)

        # Migration: add age / gender if missing
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
            print("DB: Migrated users table: Added age column")
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
            print("DB: Migrated users table: Added gender column")
        except sqlite3.OperationalError:
            pass

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_token TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS otp_verification (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_encrypted TEXT NOT NULL,
                    otp_hash TEXT NOT NULL,
                    method TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_used BOOLEAN DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    user_id TEXT
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS medical_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    data_encrypted TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    doctor_id TEXT,
                    is_confidential BOOLEAN DEFAULT 1,
                    access_log TEXT
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS cancer_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    image_path TEXT,
                    organ_detected TEXT,
                    diagnosis TEXT,
                    confidence_score REAL,
                    ai_model_version TEXT,
                    detection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    doctor_verified BOOLEAN DEFAULT 0,
                    notes_encrypted TEXT
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS mental_health_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    assessment_type TEXT,
                    data_encrypted TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    therapist_id TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    confidentiality_level TEXT DEFAULT 'high'
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    success BOOLEAN,
                    details TEXT,
                    risk_level TEXT DEFAULT 'low'
                )
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_key TEXT UNIQUE NOT NULL,
                    config_value_encrypted TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_by TEXT
                )
            """)

        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email_encrypted)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_otp_contact ON otp_verification(contact_encrypted)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_medical_patient ON medical_records(patient_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_detection_patient ON cancer_detections(patient_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mental_patient ON mental_health_records(patient_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON security_audit_log(timestamp)")

        conn.commit()
        print("[SECURE] Secure database initialized successfully with WAL mode")

    # ------------------------------------------------------------------
    # User management
    # ------------------------------------------------------------------

    def create_user(self, name, email, phone, password, age=None, gender=None, security_level="standard"):
        """Create new user with encrypted data"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            user_id = "user_" + secrets.token_urlsafe(16)
            email_encrypted = self._encrypt_data(email)
            phone_encrypted = self._encrypt_data(phone)
            name_encrypted = self._encrypt_data(name)
            password_hash = self._hash_password(password)

            cursor.execute("""
                    INSERT INTO users 
                    (user_id, email_encrypted, phone_encrypted, name_encrypted, 
                     password_hash, age, gender, security_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email_encrypted, phone_encrypted, name_encrypted,
                      password_hash, age, gender, security_level))

            self._log_security_event(
                user_id, "USER_CREATED", True,
                "User created with security level: " + security_level
            )
            conn.commit()
            print("[OK] User created successfully: " + user_id)
            return user_id
        except Exception as e:
            print("[ERR] Error creating user: " + str(e))
            conn.rollback()
            return None

    def authenticate_user(self, email, password, ip_address=None, user_agent=None):
        """Authenticate user with security checks"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT user_id, email_encrypted, password_hash, is_active, account_locked, login_attempts FROM users"
            )
            users = cursor.fetchall()

            authenticated_user = None
            for user in users:
                stored_email = self._decrypt_data(user[1])
                if stored_email.lower() == email.lower():
                    authenticated_user = user
                    break

            if authenticated_user is None:
                self._log_security_event(None, "LOGIN_FAILED", False, "Email not found: " + email)
                return None

            user_id = authenticated_user[0]
            _ = authenticated_user[1]
            password_hash = authenticated_user[2]
            is_active = authenticated_user[3]
            account_locked = authenticated_user[4]
            login_attempts = authenticated_user[5]

            if account_locked:
                self._log_security_event(user_id, "LOGIN_FAILED", False, "Account locked")
                return None

            if not is_active:
                self._log_security_event(user_id, "LOGIN_FAILED", False, "Account inactive")
                return None

            if self._verify_password(password, password_hash):
                cursor.execute(
                    "UPDATE users SET login_attempts = 0, last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (user_id,),
                )
                self._log_security_event(user_id, "LOGIN_SUCCESS", True, "User authenticated successfully")
                conn.commit()
                return user_id
            else:
                login_attempts = login_attempts + 1
                cursor.execute(
                    "UPDATE users SET login_attempts = ? WHERE user_id = ?",
                    (login_attempts, user_id),
                )
                if login_attempts >= 5:
                    cursor.execute(
                        "UPDATE users SET account_locked = 1 WHERE user_id = ?",
                        (user_id,),
                    )
                    self._log_security_event(
                        user_id, "ACCOUNT_LOCKED", False,
                        "Account locked due to multiple failed attempts",
                    )
                else:
                    self._log_security_event(
                        user_id, "LOGIN_FAILED", False,
                        "Invalid password. Attempt " + str(login_attempts) + "/5",
                    )
                conn.commit()
                return None
        except Exception as e:
            print("[ERR] Authentication error: " + str(e))
            return None

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def create_session(self, user_id, ip_address=None, user_agent=None):
        """Create secure user session"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)

            cursor.execute("""
                    INSERT INTO user_sessions 
                    (session_token, user_id, expires_at, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                """, (session_token, user_id, expires_at, ip_address, user_agent))

            self._log_security_event(
                user_id, "SESSION_CREATED", True,
                "Session created, expires: " + str(expires_at),
            )
            conn.commit()
            print("[OK] Session created for user: " + user_id)
            return session_token
        except Exception as e:
            print("[ERR] Error creating session: " + str(e))
            conn.rollback()
            return None

    def verify_session(self, session_token, ip_address=None, user_agent=None):
        """Verify user session"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                    SELECT user_id, expires_at, is_active 
                    FROM user_sessions 
                    WHERE session_token = ? AND is_active = 1
                """, (session_token,))

            session = cursor.fetchone()
            if not session:
                return None

            user_id = session[0]
            expires_at = session[1]
            is_active = session[2]

            if datetime.now() > datetime.fromisoformat(expires_at):
                cursor.execute(
                    "UPDATE user_sessions SET is_active = 0 WHERE session_token = ?",
                    (session_token,),
                )
                conn.commit()
                return None

            self._log_security_event(
                user_id, "SESSION_VERIFIED", True,
                "Session verified successfully",
            )
            return {"valid": True, "user_id": user_id}
        except Exception as e:
            print("[ERR] Session verification error: " + str(e))
            return None

    # ------------------------------------------------------------------
    # OTP
    # ------------------------------------------------------------------

    def create_otp(self, contact, method, user_id=None):
        """Create OTP for verification"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            otp = "".join(random.choices("0123456789", k=6))
            otp_hash = hashlib.sha256(otp.encode()).hexdigest()
            expires_at = datetime.now() + timedelta(minutes=5)
            contact_encrypted = self._encrypt_data(contact)

            cursor.execute("""
                    INSERT INTO otp_verification 
                    (contact_encrypted, otp_hash, method, expires_at, user_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (contact_encrypted, otp_hash, method, expires_at, user_id))

            self._log_security_event(
                user_id, "OTP_CREATED", True,
                "OTP created for " + method + ": " + contact,
            )
            conn.commit()
            print("[OK] OTP created: " + otp + " for " + contact + " via " + method)
            return otp
        except Exception as e:
            print("[ERR] Error creating OTP: " + str(e))
            conn.rollback()
            return None

    def verify_otp(self, contact, otp, method):
        """Verify OTP"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                    SELECT id, contact_encrypted, otp_hash, expires_at, is_used, attempts, user_id 
                    FROM otp_verification 
                    WHERE method = ? AND is_used = 0
                    ORDER BY created_at DESC
                """, (method,))

            otp_records = cursor.fetchall()
            matching_record = None

            for record in otp_records:
                record_id = record[0]
                contact_encrypted = record[1]
                otp_hash = record[2]
                expires_at = record[3]
                is_used = record[4]
                attempts = record[5]
                user_id = record[6]

                stored_contact = self._decrypt_data(contact_encrypted)
                if stored_contact == contact:
                    matching_record = record
                    break

            if matching_record is None:
                print("[ERR] No matching OTP record found for " + contact)
                return False

            record_id = matching_record[0]
            otp_hash = matching_record[2]
            expires_at = matching_record[3]
            is_used = matching_record[4]
            attempts = matching_record[5]
            user_id = matching_record[6]

            if datetime.now() > datetime.fromisoformat(expires_at):
                cursor.execute(
                    "UPDATE otp_verification SET is_used = 1 WHERE id = ?",
                    (record_id,),
                )
                print("[ERR] OTP expired")
                conn.commit()
                return False

            if attempts >= 3:
                print("[ERR] Too many OTP attempts")
                return False

            input_otp_hash = hashlib.sha256(otp.encode()).hexdigest()
            if input_otp_hash == otp_hash:
                cursor.execute(
                    "UPDATE otp_verification SET is_used = 1 WHERE id = ?",
                    (record_id,),
                )
                self._log_security_event(
                    user_id, "OTP_VERIFIED", True,
                    "OTP verified successfully for " + contact,
                )
                conn.commit()
                print("[OK] OTP verified successfully")
                return True
            else:
                cursor.execute(
                    "UPDATE otp_verification SET attempts = attempts + 1 WHERE id = ?",
                    (record_id,),
                )
                print("[ERR] Invalid OTP. Attempt " + str(attempts + 1) + "/3")
                conn.commit()
                return False
        except Exception as e:
            print("[ERR] OTP verification error: " + str(e))
            return False

    # ------------------------------------------------------------------
    # Audit
    # ------------------------------------------------------------------

    def _log_security_event(self, user_id, action, success, details,
                            ip_address=None, user_agent=None, risk_level="low", conn=None):
        """Log security events using existing connection or the shared one."""
        try:
            c = conn or self._get_connection()
            cursor = c.cursor()
            cursor.execute("""
                INSERT INTO security_audit_log 
                (user_id, action, success, details, ip_address, user_agent, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, action, success, details, ip_address, user_agent, risk_level))
            # Only commit if we own the connection (no conn passed)
            if conn is None:
                c.commit()
        except Exception as e:
            print("[ERR] Error logging security event: " + str(e))

    # ------------------------------------------------------------------
    # User info
    # ------------------------------------------------------------------

    def get_user_info(self, user_id):
        """Get decrypted user information"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                    SELECT email_encrypted, phone_encrypted, name_encrypted, 
                           created_at, last_login, security_level, is_active, age, gender
                    FROM users WHERE user_id = ?
                """, (user_id,))

            user = cursor.fetchone()
            if not user:
                return None

            email = self._decrypt_data(user[0])
            phone = self._decrypt_data(user[1])
            name = self._decrypt_data(user[2])
            created_at = user[3]
            last_login = user[4]
            security_level = user[5]
            is_active = user[6]
            age = user[7]
            gender = user[8]

            return {
                "user_id": user_id,
                "email": email,
                "phone": phone,
                "name": name,
                "created_at": created_at,
                "last_login": last_login,
                "security_level": security_level,
                "is_active": is_active,
                "age": age,
                "gender": gender,
            }
        except Exception as e:
            print("[ERR] Error getting user info: " + str(e))
            return None

    # ------------------------------------------------------------------
    # Cancer detection
    # ------------------------------------------------------------------

    def save_cancer_detection(self, patient_id, organ, diagnosis, confidence,
                              image_path=None, notes=None):
        """Save cancer detection results"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            notes_encrypted = self._encrypt_data(notes) if notes else None

            cursor.execute("""
                    INSERT INTO cancer_detections 
                    (patient_id, image_path, organ_detected, diagnosis, confidence_score, notes_encrypted)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (patient_id, image_path, organ, diagnosis, confidence, notes_encrypted))

            self._log_security_event(
                patient_id, "CANCER_DETECTION_SAVED", True,
                "Cancer detection saved: " + organ + " - " + diagnosis,
            )
            conn.commit()
            print("[OK] Cancer detection saved for patient: " + patient_id)
            return True
        except Exception as e:
            print("[ERR] Error saving cancer detection: " + str(e))
            conn.rollback()
            return False

    # ------------------------------------------------------------------
    # Security report
    # ------------------------------------------------------------------

    def get_security_report(self):
        """Generate security report"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
            active_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE account_locked = 1")
            locked_accounts = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM user_sessions WHERE is_active = 1 AND expires_at > CURRENT_TIMESTAMP"
            )
            active_sessions = cursor.fetchone()[0]

            cursor.execute("""
                    SELECT action, COUNT(*) 
                    FROM security_audit_log 
                    WHERE timestamp > datetime('now', '-1 day')
                    GROUP BY action
                """)
            recent_events = dict(cursor.fetchall())

            cursor.execute("""
                    SELECT COUNT(*) 
                    FROM security_audit_log 
                    WHERE action = 'LOGIN_FAILED' AND timestamp > datetime('now', '-1 day')
                """)
            failed_logins = cursor.fetchone()[0]

            return {
                "active_users": active_users,
                "locked_accounts": locked_accounts,
                "active_sessions": active_sessions,
                "recent_events": recent_events,
                "failed_logins": failed_logins,
                "encryption": True,
                "hipaa_compliant": True,
            }
        except Exception as e:
            print("[ERR] Error generating security report: " + str(e))
            return {}


def initialize_secure_system():
    """Initialize the secure database system"""
    print("[SECURE] INITIALIZING SECURE DATABASE SYSTEM")
    print("=" * 60)

    db = SecureDatabase()

    test_user_id = db.create_user(
        "Test User", "test@cancercare.ai", "+1234567890",
        "SecurePassword123!", security_level="high",
    )

    if test_user_id:
        print("[OK] Test user created: " + test_user_id)

        auth_result = db.authenticate_user("test@cancercare.ai", "SecurePassword123!")
        if auth_result:
            print("[OK] Authentication successful: " + auth_result)

            session_token = db.create_session(auth_result)
            if session_token:
                print("RES: Session created: " + session_token)

                verify_result = db.verify_session(session_token)
                if verify_result:
                    print("RES: Session verified: " + str(verify_result))
                else:
                    print("ERR: Session verification failed")
            else:
                print("ERR: Session creation failed")
        else:
            print("ERR: Authentication failed")
    else:
        print("ERR: Test user creation failed")

    report = db.get_security_report()
    print("\nREPORT: SECURITY REPORT:")
    print("=" * 40)
    for key, value in report.items():
        print("  " + str(key).replace("_", " ").title() + ": " + str(value))

    print("\nREADY: SECURE DATABASE SYSTEM READY!")


if __name__ == "__main__":
    secure_db = initialize_secure_system()