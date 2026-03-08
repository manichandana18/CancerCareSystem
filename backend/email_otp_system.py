import smtplib
import random
import string
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Email configuration (using Gmail SMTP)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'cancercare.ai@gmail.com',  # Replace with your email
    'sender_password': 'your-app-password',      # Replace with app password
}

# Temporary storage for OTPs (in production, use Redis/Database)
otp_storage = {}

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_email_otp(recipient_email, otp):
    """Send OTP email to recipient"""
    try:
        # Create email message
        message = MIMEMultipart()
        message["From"] = EMAIL_CONFIG['sender_email']
        message["To"] = recipient_email
        message["Subject"] = "CancerCare AI - Email Verification Code"
        
        # Email body
        body = f"""
        🏥 CancerCare AI - Email Verification
        
        Your verification code is: {otp}
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        
        🎗️ CancerCare AI Team
        Supporting cancer patients with technology
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        server.sendmail(EMAIL_CONFIG['sender_email'], recipient_email, message.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

@app.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to user's email"""
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'})
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP with timestamp (expires in 10 minutes)
    otp_storage[email] = {
        'otp': otp,
        'timestamp': time.time(),
        'attempts': 0
    }
    
    # Send email
    if send_email_otp(email, otp):
        return jsonify({
            'success': True, 
            'message': 'OTP sent to your email',
            'debug_otp': otp  # Remove this in production
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'Failed to send OTP. Please try again.'
        })

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify user's OTP input"""
    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')
    
    if not email or not user_otp:
        return jsonify({'success': False, 'message': 'Email and OTP are required'})
    
    # Check if OTP exists for this email
    if email not in otp_storage:
        return jsonify({'success': False, 'message': 'OTP not found or expired'})
    
    stored_data = otp_storage[email]
    
    # Check if OTP is expired (10 minutes)
    if time.time() - stored_data['timestamp'] > 600:
        del otp_storage[email]
        return jsonify({'success': False, 'message': 'OTP expired. Please request a new one.'})
    
    # Check if too many attempts
    if stored_data['attempts'] >= 3:
        del otp_storage[email]
        return jsonify({'success': False, 'message': 'Too many attempts. Please request a new OTP.'})
    
    # Verify OTP
    if user_otp == stored_data['otp']:
        del otp_storage[email]  # Remove OTP after successful verification
        return jsonify({
            'success': True, 
            'message': 'Email verified successfully!'
        })
    else:
        stored_data['attempts'] += 1
        return jsonify({
            'success': False, 
            'message': f'Invalid OTP. {3 - stored_data["attempts"]} attempts remaining.'
        })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'CancerCare AI Email OTP'})

if __name__ == '__main__':
    print("🏥 CancerCare AI Email OTP System")
    print("📧 Starting server on http://localhost:5001")
    print("🎗️ Ready to send OTP emails!")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
