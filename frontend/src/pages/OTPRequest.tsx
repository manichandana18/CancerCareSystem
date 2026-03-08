import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { sendOTP } from "../services/otpApi";
import type { SendOTPRequest } from "../services/otpApi";

export default function OTPRequest() {
  const [contact, setContact] = useState("");
  const [method, setMethod] = useState<"email" | "phone">("email");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const validateEmail = (email: string) => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  };

  const validatePhone = (phone: string) => {
    const phonePattern = /^\+?[1-9]\d{9,14}$/;
    const cleaned = phone.replace(/[\s\-\(\)]/g, '');
    return phonePattern.test(cleaned);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validate contact based on method
    if (method === "email" && !validateEmail(contact)) {
      setError("Please enter a valid email address");
      return;
    }

    if (method === "phone" && !validatePhone(contact)) {
      setError("Please enter a valid phone number (10-15 digits)");
      return;
    }

    setLoading(true);

    try {
      const request: SendOTPRequest = {
        contact,
        method,
      };

      const response = await sendOTP(request);

      if (response.success) {
        // Store contact and method for verification page
        sessionStorage.setItem('otpContact', contact);
        sessionStorage.setItem('otpMethod', method);
        sessionStorage.setItem('otpSent', 'true');

        // Navigate to verification page
        navigate('/otp-verify');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send OTP. Please try again.');
      console.error('OTP send error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="max-w-md mx-auto space-y-12 py-12 px-4 animate-fade-in">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="inline-block relative">
          <div className="absolute inset-0 bg-primary/20 blur-2xl rounded-full"></div>
          <div className="w-24 h-24 bg-white/50 backdrop-blur-xl rounded-3xl flex items-center justify-center shadow-xl border border-white/50 relative z-10 transform -rotate-6 group-hover:rotate-0 transition-transform duration-500">
            <span className="text-5xl animate-float">📩</span>
          </div>
        </div>
        <div>
          <h1 className="text-5xl font-heading font-black text-gray-900 tracking-tight leading-none mb-3">Request OTP</h1>
          <p className="text-gray-500 font-medium max-w-[280px] mx-auto text-sm leading-relaxed">
            Verify your identity with a secure one-time passcode.
          </p>
        </div>
      </div>

      {/* Form Card */}
      <div className="glass-panel rounded-[2.5rem] p-10 relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:scale-150 transition-transform duration-700"></div>

        <form onSubmit={handleSubmit} className="space-y-8 relative z-10">
          {/* Method Selection */}
          <div className="space-y-4">
            <label className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-1">
              Select Method
            </label>
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setMethod("email")}
                className={`p-5 rounded-2xl border-2 transition-all duration-300 transform active:scale-95 ${method === "email"
                  ? "border-primary bg-primary/5 text-primary shadow-lg shadow-primary/5"
                  : "border-gray-50 bg-gray-50/50 hover:border-gray-200 text-gray-400"
                  }`}
              >
                <div className="text-2xl mb-2">{method === "email" ? "✉️" : "📧"}</div>
                <div className="font-bold text-sm">Email</div>
              </button>
              <button
                type="button"
                onClick={() => setMethod("phone")}
                className={`p-5 rounded-2xl border-2 transition-all duration-300 transform active:scale-95 ${method === "phone"
                  ? "border-primary bg-primary/5 text-primary shadow-lg shadow-primary/5"
                  : "border-gray-50 bg-gray-50/50 hover:border-gray-200 text-gray-400"
                  }`}
              >
                <div className="text-2xl mb-2">{method === "phone" ? "📱" : "🤳"}</div>
                <div className="font-bold text-sm">Phone</div>
              </button>
            </div>
          </div>

          {/* Contact Input */}
          <div className="space-y-3">
            <label htmlFor="contact" className="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] ml-1">
              {method === "email" ? "Email Address" : "Phone Number"}
            </label>
            <div className="relative group">
              <input
                id="contact"
                type={method === "email" ? "email" : "tel"}
                value={contact}
                onChange={(e) => setContact(e.target.value)}
                placeholder={method === "email" ? "name@example.com" : "+1 234 567 890"}
                required
                className="w-full px-6 py-5 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-bold text-gray-900 group-hover:border-gray-200"
              />
              <div className="absolute right-5 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-primary transition-colors">
                {method === "email" ? "📧" : "📱"}
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-100 p-4 rounded-2xl animate-shake flex items-center gap-3">
              <span className="text-xl">⚠️</span>
              <p className="text-sm text-red-600 font-bold">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || !contact}
            className="w-full py-5 rounded-2xl bg-primary text-white font-black text-xl shadow-xl shadow-primary/20 hover:bg-primary-hover hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed btn-premium group"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                TRANSMITTING...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-3">
                SEND PASSCODE <span className="group-hover:translate-x-1 transition-transform">→</span>
              </span>
            )}
          </button>
        </form>
      </div>

      {/* Footer Info */}
      <div className="text-center space-y-2">
        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Secure Access Protocol</p>
        <p className="text-[10px] text-gray-400 max-w-[200px] mx-auto leading-relaxed">
          One-time passcodes expire in 10 minutes for your protection.
        </p>
      </div>
    </section>
  );
}
