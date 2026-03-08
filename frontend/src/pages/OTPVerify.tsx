import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { verifyOTP, resendOTP } from "../services/otpApi";
import type { VerifyOTPRequest, ResendOTPRequest } from "../services/otpApi";
import type { FC } from "react";

const OTPVerify: FC = () => {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [contact, setContact] = useState("");
  const [method, setMethod] = useState<"email" | "phone">("email");
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes in seconds
  const navigate = useNavigate();
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    const storedContact = sessionStorage.getItem('otpContact');
    const storedMethod = sessionStorage.getItem('otpMethod') as "email" | "phone" | null;

    if (!storedContact || !storedMethod) {
      navigate('/otp-request');
      return;
    }

    setContact(storedContact);
    setMethod(storedMethod);

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return;

    const newOtp = [...otp];
    newOtp[index] = value.slice(-1);
    setOtp(newOtp);
    setError(null);

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData("text").slice(0, 6);
    if (/^\d+$/.test(pastedData)) {
      const newOtp = [...otp];
      for (let i = 0; i < 6; i++) {
        newOtp[i] = pastedData[i] || "";
      }
      setOtp(newOtp);
      const lastIndex = Math.min(pastedData.length - 1, 5);
      inputRefs.current[lastIndex]?.focus();
    }
  };

  const handleVerify = async () => {
    const otpString = otp.join("");
    if (otpString.length !== 6) {
      setError("Please enter the complete 6-digit code");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const request: VerifyOTPRequest = {
        contact,
        otp: otpString,
        method,
      };

      const response = await verifyOTP(request);

      if (response.success) {
        sessionStorage.removeItem('otpContact');
        sessionStorage.removeItem('otpMethod');
        sessionStorage.removeItem('otpSent');
        sessionStorage.setItem('otpVerified', 'true');
        navigate('/otp-success');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid code. Please try again.');
      setOtp(["", "", "", "", "", ""]);
      inputRefs.current[0]?.focus();
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    setResending(true);
    setError(null);

    try {
      const request: ResendOTPRequest = {
        contact,
        method,
      };
      const response = await resendOTP(request);

      if (response.success) {
        setTimeLeft(600);
        setOtp(["", "", "", "", "", ""]);
        inputRefs.current[0]?.focus();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to resend. Please try again.');
    } finally {
      setResending(false);
    }
  };

  return (
    <section className="max-w-md mx-auto space-y-12 py-12 px-4 animate-fade-in">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="inline-block relative">
          <div className="absolute inset-0 bg-green-500/20 blur-2xl rounded-full"></div>
          <div className="w-24 h-24 bg-white/50 backdrop-blur-xl rounded-3xl flex items-center justify-center shadow-xl border border-white/50 relative z-10 transform rotate-6 hover:rotate-0 transition-transform duration-500">
            <span className="text-5xl animate-bounce">🛡️</span>
          </div>
        </div>
        <div>
          <h1 className="text-5xl font-heading font-black text-gray-900 tracking-tight leading-none mb-3">Verify Identity</h1>
          <p className="text-gray-500 font-medium max-w-[280px] mx-auto text-sm leading-relaxed">
            We've transmitted a 6-digit code to <br />
            <span className="text-primary font-bold break-all">{contact}</span>
          </p>
        </div>
      </div>

      {/* Verification Card */}
      <div className="glass-panel rounded-[2.5rem] p-10 relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full -mr-16 -mt-16 blur-2xl group-hover:scale-150 transition-transform duration-700"></div>

        {/* Timer UI */}
        <div className="flex justify-center mb-8">
          <div className={`px-4 py-2 rounded-2xl flex items-center gap-2 transition-colors border ${timeLeft < 60 ? 'bg-red-50 border-red-100 text-red-600 animate-pulse' : 'bg-gray-50 border-gray-100 text-gray-500'
            }`}>
            <span className="text-lg">⏱️</span>
            <span className="font-mono font-black text-xl tracking-wider">{formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* Segmented Inputs */}
        <div className="flex justify-center gap-2.5 mb-10">
          {otp.map((digit, index) => (
            <input
              key={index}
              ref={(el) => { inputRefs.current[index] = el; }}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(index, e.target.value)}
              onKeyDown={(e) => handleKeyDown(index, e)}
              onPaste={handlePaste}
              className="otp-box w-12 h-16 sm:w-14 sm:h-18"
              disabled={loading || timeLeft === 0}
            />
          ))}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-100 p-4 rounded-2xl animate-shake flex items-center gap-3 mb-8">
            <span className="text-xl">⚠️</span>
            <p className="text-sm text-red-600 font-bold">{error}</p>
          </div>
        )}

        <div className="space-y-4 relative z-10">
          <button
            onClick={handleVerify}
            disabled={loading || otp.join("").length !== 6 || timeLeft === 0}
            className="w-full py-5 rounded-2xl bg-primary text-white font-black text-xl shadow-xl shadow-primary/20 hover:bg-primary-hover hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed btn-premium group"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                VERIFYING...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-3">
                SECURE LOGIN <span className="group-hover:translate-x-1 transition-transform">→</span>
              </span>
            )}
          </button>

          <button
            onClick={handleResend}
            disabled={resending || timeLeft > 0}
            className="w-full py-4 text-gray-400 font-bold text-sm hover:text-primary transition-colors flex items-center justify-center gap-2 disabled:opacity-30"
          >
            {resending ? 'RESENDING CODE...' : 'DIDN\'T GET THE CODE? RESEND'}
          </button>
        </div>
      </div>

      <button
        onClick={() => navigate('/otp-request')}
        className="text-gray-400 hover:text-primary font-bold text-sm flex items-center gap-2 mx-auto transition-colors"
      >
        ← Correct my details
      </button>
    </section>
  );
};

export default OTPVerify;
