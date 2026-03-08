import Navbar from "../Navbar";
import { Link } from "react-router-dom";
import type { FC, ReactNode } from "react";

const Layout: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      <Navbar />
      <main className="py-8 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
      {/* Premium Footer */}
      <footer className="relative mt-16 overflow-hidden"
        style={{ background: 'linear-gradient(135deg, #0f172a, #1e293b, #0f172a)' }}>
        {/* Gradient divider */}
        <div className="h-1" style={{ background: 'linear-gradient(90deg, transparent, #0d9488, #2dd4bf, #0d9488, transparent)' }} />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-10">
            {/* Brand */}
            <div>
              <h3 className="text-white font-heading font-black text-xl mb-3 flex items-center gap-2">
                🎗️ CancerCare <span className="text-teal-400">AI</span>
              </h3>
              <p className="text-gray-400 text-sm font-medium leading-relaxed">
                AI-powered early cancer detection with 98.5% accuracy across 6 cancer types.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-white font-black text-xs uppercase tracking-[0.2em] mb-4">Platform</h4>
              <div className="space-y-2">
                {[
                  { to: '/upload', label: 'Start Analysis' },
                  { to: '/dashboard', label: 'Dashboard' },
                  { to: '/history', label: 'History' },
                  { to: '/analytics', label: 'Analytics' },
                  { to: '/methodology', label: 'Methodology' },
                ].map(link => (
                  <Link key={link.to} to={link.to} className="block text-gray-400 text-sm font-medium hover:text-teal-400 transition-colors">
                    {link.label}
                  </Link>
                ))}
              </div>
            </div>

            {/* Community */}
            <div>
              <h4 className="text-white font-black text-xs uppercase tracking-[0.2em] mb-4">Community</h4>
              <div className="space-y-2">
                {[
                  { to: '/wellness', label: 'Wellness' },
                  { to: '/donate', label: 'Donate' },
                  { to: '/wigs', label: 'Wig Marketplace' },
                ].map(link => (
                  <Link key={link.to} to={link.to} className="block text-gray-400 text-sm font-medium hover:text-teal-400 transition-colors">
                    {link.label}
                  </Link>
                ))}
              </div>
            </div>

            {/* Trust */}
            <div>
              <h4 className="text-white font-black text-xs uppercase tracking-[0.2em] mb-4">Security</h4>
              <div className="space-y-2 text-gray-400 text-sm font-medium">
                <div className="flex items-center gap-2"><span className="text-emerald-400">✓</span> HIPAA Compliant</div>
                <div className="flex items-center gap-2"><span className="text-emerald-400">✓</span> AES-256 Encryption</div>
                <div className="flex items-center gap-2"><span className="text-emerald-400">✓</span> Zero-Knowledge Architecture</div>
                <div className="flex items-center gap-2"><span className="text-emerald-400">✓</span> End-to-End Encrypted</div>
              </div>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="border-t border-white/10 pt-6 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-gray-500 text-xs font-medium">
              © {new Date().getFullYear()} CancerCare AI System. For educational purposes only. Not a substitute for professional medical diagnosis.
            </p>
            <div className="flex items-center gap-4 text-gray-500 text-xs font-bold">
              <span>v7.0</span>
              <span className="w-1 h-1 bg-gray-600 rounded-full" />
              <span>Made with 💚</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;

