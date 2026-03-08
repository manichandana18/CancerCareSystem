import { useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import type { FC } from "react";

const OTPSuccess: FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const verified = sessionStorage.getItem('otpVerified');
    if (!verified) {
      navigate('/otp-request');
    }
  }, [navigate]);

  return (
    <section className="max-w-md mx-auto space-y-12 py-16 px-4 animate-fade-in text-center">
      {/* Success Moment */}
      <div className="space-y-6">
        <div className="inline-block relative">
          <div className="absolute inset-0 bg-green-500/30 blur-3xl rounded-full scale-150 animate-pulse"></div>
          <div className="w-32 h-32 bg-white rounded-[2.5rem] shadow-2xl flex items-center justify-center relative z-10 animate-success border-4 border-green-50">
            <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-5xl shadow-inner font-black">
              ✓
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <h1 className="text-5xl font-heading font-black text-gray-900 tracking-tight">Identity Verified</h1>
          <p className="text-gray-500 font-medium">Your account is now secure and ready.</p>
        </div>
      </div>

      {/* Content Panel */}
      <div className="glass-panel rounded-[3rem] p-10 relative overflow-hidden group shadow-2xl shadow-green-500/5">
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-green-500/5 rounded-full -ml-16 -mb-16 blur-2xl"></div>

        <div className="relative z-10 space-y-8">
          <div className="p-6 bg-green-50/50 rounded-3xl border border-green-100 flex items-center gap-4 text-left">
            <span className="text-3xl">🛡️</span>
            <div>
              <p className="text-xs font-black text-green-800 uppercase tracking-widest leading-none mb-1">Security Status</p>
              <p className="text-sm font-bold text-green-700">Multi-factor Authentication Active</p>
            </div>
          </div>

          <div className="space-y-4">
            <Link
              to="/dashboard"
              className="w-full py-5 rounded-2xl bg-primary text-white font-black text-xl shadow-xl shadow-primary/20 hover:bg-primary-hover hover:-translate-y-1 transition-all active:scale-95 block btn-premium"
            >
              LAUNCH DASHBOARD
            </Link>

            <Link
              to="/"
              className="w-full py-4 text-gray-400 font-bold text-sm hover:text-gray-600 transition-colors block"
            >
              RETURN TO HOME
            </Link>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-2">
        {[...Array(3)].map((_, i) => (
          <div key={i} className={`w-2 h-2 rounded-full ${i === 2 ? 'bg-primary' : 'bg-gray-200'}`}></div>
        ))}
      </div>
    </section>
  );
};

export default OTPSuccess;
