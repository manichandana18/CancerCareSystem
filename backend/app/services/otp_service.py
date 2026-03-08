"""
OTP Service for CancerCare System
Handles OTP generation, storage, sending (Email/SMS), and verification
"""

import random
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from secure_database import SecureDatabase

class OTPService:
    """Service for managing OTP generation, storage, and delivery"""
    
    def __init__(self):
        self.db = SecureDatabase()
        self.otp_expiry_minutes = 10  # OTP expires in 10 minutes
        self.max_attempts = 3  # Maximum verification attempts
        
        # Email configuration (can be set via environment variables)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@cancercare.com")
        
    def generate_otp(self, length: int = 6) -> str:
        """Generate a random OTP"""
        return ''.join(random.choices('0123456789', k=length))
    
    def send_otp_email(self, recipient_email: str, otp: str) -> bool:
        """Send OTP via email"""
        try:
            # If SMTP credentials are not configured, print OTP to console
            if not self.smtp_username or not self.smtp_password:
                print(f"📧 [EMAIL OTP] To: {recipient_email}")
                print(f"🔐 Your CancerCare verification code is: {otp}")
                print(f"⏰ This code expires in {self.otp_expiry_minutes} minutes")
                print("⚠️  SMTP not configured - OTP printed to console for testing")
                return True
            
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Your CancerCare Verification Code"
            msg['From'] = self.from_email
            msg['To'] = recipient_email
            
            # Plain text version
            text = f"""
            Your CancerCare Verification Code
            
            Your verification code is: {otp}
            
            This code expires in {self.otp_expiry_minutes} minutes.
            
            If you didn't request this code, please ignore this email.
            
            ---
            CancerCare System
            """
            
            # HTML version
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .otp-box {{ background: white; border: 2px dashed #667eea; padding: 20px; text-align: center; margin: 20px 0; border-radius: 5px; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏥 CancerCare System</h1>
                        <p>Verification Code</p>
                    </div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>Your verification code is:</p>
                        <div class="otp-box">
                            <div class="otp-code">{otp}</div>
                        </div>
                        <p>This code expires in <strong>{self.otp_expiry_minutes} minutes</strong>.</p>
                        <p>If you didn't request this code, please ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>© {datetime.now().year} CancerCare System. All rights reserved.</p>
                        <p>This is an automated message, please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach both versions
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ OTP email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email OTP: {e}")
            # Fallback: print to console
            print(f"📧 [EMAIL OTP] To: {recipient_email}")
            print(f"🔐 Your CancerCare verification code is: {otp}")
            return False
    
    def send_otp_sms(self, phone_number: str, otp: str) -> bool:
        """Send OTP via SMS (placeholder - integrate with SMS service like Twilio)"""
        try:
            # For now, print to console
            # In production, integrate with SMS service like Twilio, AWS SNS, etc.
            print(f"📱 [SMS OTP] To: {phone_number}")
            print(f"🔐 Your CancerCare verification code is: {otp}")
            print(f"⏰ This code expires in {self.otp_expiry_minutes} minutes")
            print("⚠️  SMS service not configured - OTP printed to console for testing")
            
            # TODO: Integrate with SMS service
            # Example with Twilio:
            # from twilio.rest import Client
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body=f"Your CancerCare verification code is: {otp}",
            #     from_=twilio_phone,
            #     to=phone_number
            # )
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending SMS OTP: {e}")
            return False
    
    def create_and_send_otp(self, contact: str, method: str, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create OTP, store it, and send it via email or SMS
        
        Args:
            contact: Email address or phone number
            method: 'email' or 'phone'
            user_id: Optional user ID if OTP is for existing user
            
        Returns:
            OTP string if successful, None otherwise
        """
        try:
            # Generate OTP
            otp = self.generate_otp()
            
            # Store OTP in database
            stored_otp = self.db.create_otp(contact, method, user_id)
            
            if not stored_otp:
                print(f"❌ Failed to store OTP for {contact}")
                return None
            
            # Send OTP
            if method.lower() == "email":
                success = self.send_otp_email(contact, otp)
            elif method.lower() == "phone":
                success = self.send_otp_sms(contact, otp)
            else:
                print(f"❌ Invalid method: {method}. Use 'email' or 'phone'")
                return None
            
            if success:
                print(f"✅ OTP created and sent successfully to {contact} via {method}")
                return otp
            else:
                print(f"⚠️  OTP created but sending failed. OTP: {otp}")
                return otp  # Still return OTP for testing purposes
                
        except Exception as e:
            print(f"❌ Error in create_and_send_otp: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def verify_otp(self, contact: str, otp: str, method: str) -> bool:
        """
        Verify OTP entered by user
        
        Args:
            contact: Email address or phone number
            otp: OTP entered by user
            method: 'email' or 'phone'
            
        Returns:
            True if OTP is valid, False otherwise
        """
        try:
            return self.db.verify_otp(contact, otp, method)
        except Exception as e:
            print(f"❌ Error verifying OTP: {e}")
            return False
    
    def resend_otp(self, contact: str, method: str, user_id: Optional[str] = None) -> Optional[str]:
        """
        Resend OTP to user
        
        Args:
            contact: Email address or phone number
            method: 'email' or 'phone'
            user_id: Optional user ID
            
        Returns:
            New OTP string if successful, None otherwise
        """
        return self.create_and_send_otp(contact, method, user_id)
