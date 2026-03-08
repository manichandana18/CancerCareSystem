# OTP Authentication System - Complete Guide

## 📋 Overview

This document explains the complete OTP (One-Time Password) authentication system implemented in the CancerCare System. The system allows users to verify their email or phone number using a 6-digit code.

## 🎯 Features

- ✅ **Email OTP**: Send verification codes via email
- ✅ **Phone OTP**: Send verification codes via SMS (ready for integration)
- ✅ **Secure Storage**: OTPs are hashed and stored securely in the database
- ✅ **Expiration**: OTPs expire after 10 minutes
- ✅ **Rate Limiting**: Maximum 3 verification attempts per OTP
- ✅ **Resend Functionality**: Users can request a new OTP
- ✅ **Beautiful UI**: Modern, responsive frontend interface

## 🏗️ System Architecture

### Backend Components

1. **OTP Service** (`backend/app/services/otp_service.py`)
   - Generates 6-digit OTPs
   - Stores OTPs securely in database
   - Sends OTPs via email/SMS
   - Verifies OTPs

2. **OTP Routes** (`backend/app/routes/otp.py`)
   - `/api/otp/send` - Send OTP
   - `/api/otp/verify` - Verify OTP
   - `/api/otp/resend` - Resend OTP

3. **Database Integration** (`secure_database.py`)
   - Stores OTPs with encryption
   - Tracks expiration and attempts
   - Logs security events

### Frontend Components

1. **OTP Request Page** (`/otp-request`)
   - User enters email or phone
   - Selects verification method
   - Sends OTP request

2. **OTP Verify Page** (`/otp-verify`)
   - User enters 6-digit code
   - Real-time validation
   - Countdown timer
   - Resend functionality

3. **OTP Success Page** (`/otp-success`)
   - Confirmation screen
   - Navigation to dashboard

## 🚀 How It Works

### Step-by-Step Flow

1. **User Requests OTP**
   ```
   User → Frontend (/otp-request)
        → Enters email/phone
        → Selects method (email/phone)
        → Clicks "Send Verification Code"
   ```

2. **Backend Generates OTP**
   ```
   Frontend → POST /api/otp/send
           → Backend generates 6-digit OTP
           → OTP stored in database (hashed)
           → OTP sent via email/SMS
           → Returns success response
   ```

3. **User Receives OTP**
   ```
   Email: Check inbox for verification code
   SMS: Check phone messages for verification code
   ```

4. **User Verifies OTP**
   ```
   User → Frontend (/otp-verify)
        → Enters 6-digit code
        → Clicks "Verify Code"
        → Backend verifies OTP
        → Returns success/failure
   ```

5. **Verification Complete**
   ```
   Success → Navigate to /otp-success
          → User can proceed to dashboard
   ```

## 📡 API Endpoints

### 1. Send OTP

**Endpoint:** `POST /api/otp/send`

**Request Body:**
```json
{
  "contact": "user@example.com",
  "method": "email",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully to your email",
  "otp": "123456",  // Only for testing - remove in production
  "expires_in_minutes": 10
}
```

### 2. Verify OTP

**Endpoint:** `POST /api/otp/verify`

**Request Body:**
```json
{
  "contact": "user@example.com",
  "otp": "123456",
  "method": "email"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "expires_in_minutes": 0
}
```

### 3. Resend OTP

**Endpoint:** `POST /api/otp/resend`

**Request Body:**
```json
{
  "contact": "user@example.com",
  "method": "email",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP resent successfully to your email",
  "otp": "654321",  // Only for testing - remove in production
  "expires_in_minutes": 10
}
```

## ⚙️ Configuration

### Email Configuration

To enable email sending, set these environment variables:

```bash
# SMTP Configuration
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export FROM_EMAIL="noreply@cancercare.com"
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password as `SMTP_PASSWORD`

**Example `.env` file:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
FROM_EMAIL=noreply@cancercare.com
```

**Note:** If SMTP is not configured, OTPs will be printed to the console for testing purposes.

### SMS Configuration (Future)

To enable SMS sending, integrate with a service like Twilio:

```python
# In otp_service.py, update send_otp_sms method
from twilio.rest import Client

client = Client(account_sid, auth_token)
message = client.messages.create(
    body=f"Your CancerCare verification code is: {otp}",
    from_=twilio_phone,
    to=phone_number
)
```

## 🔒 Security Features

1. **OTP Hashing**: OTPs are hashed using SHA-256 before storage
2. **Expiration**: OTPs expire after 10 minutes
3. **Attempt Limiting**: Maximum 3 verification attempts per OTP
4. **One-Time Use**: OTPs are marked as used after successful verification
5. **Encryption**: Contact information is encrypted in the database
6. **Security Logging**: All OTP operations are logged

## 📱 Frontend Usage

### Navigate to OTP Request
```typescript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/otp-request');
```

### Programmatic OTP Send
```typescript
import { sendOTP } from '../services/otpApi';

const response = await sendOTP({
  contact: 'user@example.com',
  method: 'email'
});
```

### Programmatic OTP Verify
```typescript
import { verifyOTP } from '../services/otpApi';

const response = await verifyOTP({
  contact: 'user@example.com',
  otp: '123456',
  method: 'email'
});
```

## 🧪 Testing

### Test Email OTP (Without SMTP)

1. Start the backend server
2. Navigate to `/otp-request` in frontend
3. Enter your email
4. Select "Email" method
5. Click "Send Verification Code"
6. Check backend console for OTP:
   ```
   📧 [EMAIL OTP] To: user@example.com
   🔐 Your CancerCare verification code is: 123456
   ⏰ This code expires in 10 minutes
   ```
7. Enter the OTP in the verification page

### Test Phone OTP

1. Navigate to `/otp-request`
2. Enter phone number (e.g., +1234567890)
3. Select "Phone" method
4. Check backend console for OTP

## 🐛 Troubleshooting

### OTP Not Received

1. **Check SMTP Configuration**
   - Verify environment variables are set
   - Check SMTP credentials
   - Test SMTP connection

2. **Check Console Logs**
   - OTP is printed to console if SMTP fails
   - Check backend terminal for OTP

3. **Check Spam Folder**
   - Email might be in spam/junk folder

### OTP Expired

- OTPs expire after 10 minutes
- Request a new OTP using "Resend Code" button

### Invalid OTP

- Check for typos
- Ensure you're using the latest OTP
- Maximum 3 attempts per OTP

### Database Errors

- Ensure database file exists
- Check database permissions
- Verify secure_database.py is accessible

## 📝 Code Examples

### Backend: Custom OTP Generation

```python
from app.services.otp_service import OTPService

otp_service = OTPService()

# Generate and send OTP
otp = otp_service.create_and_send_otp(
    contact="user@example.com",
    method="email",
    user_id="user-123"
)

# Verify OTP
is_valid = otp_service.verify_otp(
    contact="user@example.com",
    otp="123456",
    method="email"
)
```

### Frontend: Custom OTP Flow

```typescript
import { sendOTP, verifyOTP } from '../services/otpApi';

// Send OTP
const sendResponse = await sendOTP({
  contact: 'user@example.com',
  method: 'email'
});

// Verify OTP
const verifyResponse = await verifyOTP({
  contact: 'user@example.com',
  otp: '123456',
  method: 'email'
});
```

## 🎨 UI Features

- **Modern Design**: Clean, professional interface
- **Responsive**: Works on mobile, tablet, and desktop
- **Real-time Validation**: Instant feedback on input
- **Countdown Timer**: Shows remaining time for OTP
- **Auto-focus**: Automatically moves to next input field
- **Paste Support**: Can paste 6-digit code directly
- **Error Handling**: Clear error messages
- **Loading States**: Visual feedback during operations

## 🔄 Integration with Registration/Login

The OTP system can be integrated with registration:

```python
# After user registration
from app.services.otp_service import OTPService

otp_service = OTPService()
otp_service.create_and_send_otp(
    contact=user_email,
    method="email",
    user_id=user_id
)
```

## 📊 Database Schema

The OTP system uses the `otp_verification` table:

```sql
CREATE TABLE otp_verification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_encrypted TEXT NOT NULL,
    otp_hash TEXT NOT NULL,
    method TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🚀 Production Checklist

- [ ] Configure SMTP credentials
- [ ] Remove OTP from API responses (for testing)
- [ ] Set up SMS service (Twilio, AWS SNS, etc.)
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerts
- [ ] Configure email templates
- [ ] Test email delivery
- [ ] Set up error logging
- [ ] Configure CORS properly
- [ ] Enable HTTPS

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SMTP Configuration Guide](https://docs.python.org/3/library/smtplib.html)
- [Twilio SMS API](https://www.twilio.com/docs/sms)

---

**Status**: ✅ Complete and Ready to Use
**Last Updated**: 2025
