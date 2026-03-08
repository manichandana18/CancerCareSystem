const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SendOTPRequest {
  contact: string; // Email or phone number
  method: 'email' | 'phone';
  user_id?: string;
}

export interface VerifyOTPRequest {
  contact: string;
  otp: string;
  method: 'email' | 'phone';
}

export interface ResendOTPRequest {
  contact: string;
  method: 'email' | 'phone';
  user_id?: string;
}

export interface OTPResponse {
  success: boolean;
  message: string;
  otp?: string; // Only for testing
  expires_in_minutes: number;
}

export async function sendOTP(data: SendOTPRequest): Promise<OTPResponse> {
  const response = await fetch(`${API_BASE_URL}/api/otp/send`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to send OTP' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function verifyOTP(data: VerifyOTPRequest): Promise<OTPResponse> {
  const response = await fetch(`${API_BASE_URL}/api/otp/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to verify OTP' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

export async function resendOTP(data: ResendOTPRequest): Promise<OTPResponse> {
  const response = await fetch(`${API_BASE_URL}/api/otp/resend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to resend OTP' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  return await response.json();
}
