import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { useLanguage } from '../contexts/LanguageContext';
import type { Language } from '../contexts/LanguageContext';

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const { language, setLanguage, t } = useLanguage();

  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showLangMenu, setShowLangMenu] = useState(false);
  const [showThemeMenu, setShowThemeMenu] = useState(false);
  const [showDiagnosticsMenu, setShowDiagnosticsMenu] = useState(false);

  const isActive = (path: string) => {
    return location.pathname === path
      ? 'text-primary bg-primary/10 font-bold shadow-sm'
      : 'text-gray-600 hover:text-primary hover:bg-primary/5';
  };

  const handleLogout = async () => {
    await logout();
    setShowProfileMenu(false);
    navigate('/');
  };

  // Get user initials for avatar
  const getUserInitials = () => {
    if (!user?.name) return 'U';
    const names = user.name.split(' ');
    if (names.length >= 2) {
      return `${names[0][0]}${names[1][0]}`.toUpperCase();
    }
    return user.name.substring(0, 2).toUpperCase();
  };

  return (
    <nav className="glass-nav sticky top-0 z-50 transition-all duration-300 border-b border-gray-100/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center group">
              <span className="text-4xl mr-3 transform group-hover:scale-110 transition-transform duration-500 drop-shadow-lg">🎗️</span>
              <div>
                <h1 className="text-2xl font-black text-primary font-heading tracking-tight">CancerCare AI</h1>
                <p className="text-[9px] text-gray-400 font-black tracking-[0.3em] uppercase">Healing & Hope</p>
              </div>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-2">
            <Link to="/" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/')}`}>
              {t('nav.home')}
            </Link>

            {isAuthenticated && (
              <div className="relative">
                <button
                  onClick={() => { setShowDiagnosticsMenu(!showDiagnosticsMenu); setShowLangMenu(false); setShowThemeMenu(false); setShowProfileMenu(false); }}
                  className={`px-4 py-2 rounded-full text-sm transition-all duration-300 flex items-center gap-1 ${showDiagnosticsMenu || location.search.includes('type') ? 'text-primary bg-primary/10 font-bold' : 'text-gray-600 hover:text-primary hover:bg-primary/5'}`}
                >
                  🔬 Diagnostics
                  <svg className={`w-3 h-3 transition-transform duration-300 ${showDiagnosticsMenu ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                </button>
                {showDiagnosticsMenu && (
                  <div className="absolute left-0 mt-2 w-56 glass-panel bg-white/95 py-2 z-50 animate-fade-in shadow-xl border-t-2 border-primary">
                    <p className="px-4 py-1 text-[9px] font-black text-gray-400 uppercase tracking-widest">Select Model</p>
                    {[
                      { id: 'auto', label: '🤖 Auto Detect', color: 'text-teal-600' },
                      { id: 'skin', label: '🧴 Skin Cancer', color: 'text-emerald-600' },
                      { id: 'breast', label: '🎀 Breast Cancer', color: 'text-pink-600' },
                      { id: 'lung', label: '🫁 Lung Cancer', color: 'text-sky-600' },
                      { id: 'brain', label: '🧠 Brain Tumor', color: 'text-purple-600' },
                      { id: 'blood', label: '🩸 Blood Cancer', color: 'text-red-600' },
                      { id: 'bone', label: '🦴 Bone Cancer', color: 'text-amber-600' },
                    ].map((type) => (
                      <Link
                        key={type.id}
                        to={`/upload?type=${type.id}`}
                        onClick={() => setShowDiagnosticsMenu(false)}
                        className={`block px-4 py-2.5 text-sm hover:bg-primary/5 transition-all font-bold ${type.color} border-l-4 border-transparent hover:border-primary`}
                      >
                        {type.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            )}

            {isAuthenticated && (
              <Link to="/upload" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/upload')}`}>
                {t('nav.upload')}
              </Link>
            )}

            {isAuthenticated && (
              <Link to="/staging" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/staging')}`}>
                🔬 Staging
              </Link>
            )}

            {isAuthenticated && (
              <Link to="/medicines" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/medicines')}`}>
                💊 Medicines
              </Link>
            )}

            <Link to="/wigs" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/wigs')}`}>
              {t('nav.wigs')}
            </Link>
            <Link to="/donate" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/donate')}`}>
              {t('nav.donate')}
            </Link>
            <Link to="/wellness" className={`px-4 py-2 rounded-full text-sm transition-all duration-300 ${isActive('/wellness')}`}>
              {t('nav.wellness')}
            </Link>

            <div className="w-px h-6 bg-gray-200 mx-2"></div>

            {/* Language Selector */}
            <div className="relative">
              <button
                onClick={() => { setShowLangMenu(!showLangMenu); setShowThemeMenu(false); }}
                className="p-2 rounded-full hover:bg-gray-100 text-gray-600 transition-colors flex items-center gap-1"
                title="Select Language"
              >
                <span className="text-lg opacity-80 italic font-bold">{language.toUpperCase()}</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
              </button>
              {showLangMenu && (
                <div className="absolute right-0 mt-2 w-36 glass-panel bg-white/90 py-2 z-50 animate-fade-in">
                  {(['en', 'hi', 'es', 'te'] as Language[]).map((lang) => (
                    <button
                      key={lang}
                      onClick={() => { setLanguage(lang); setShowLangMenu(false); }}
                      className={`w-full text-left px-4 py-2.5 text-sm hover:bg-primary/5 transition-all ${language === lang ? 'text-primary font-black' : 'text-gray-600 font-medium'}`}
                    >
                      {lang === 'en' && '🇺🇸 English'}
                      {lang === 'hi' && '🇮🇳 Hindi'}
                      {lang === 'es' && '🇪🇸 Spanish'}
                      {lang === 'te' && '🇮🇳 Telugu'}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Theme Selector */}
            <div className="relative">
              <button
                onClick={() => { setShowThemeMenu(!showThemeMenu); setShowLangMenu(false); }}
                className="p-2 rounded-full hover:bg-gray-100 text-gray-600 transition-colors"
                title="Change Theme"
              >
                {theme === 'coral' && '💖'}
                {theme === 'teal' && '🌊'}
                {theme === 'dark' && '🌙'}
              </button>
              {showThemeMenu && (
                <div className="absolute right-0 mt-2 w-44 glass-panel bg-white/90 py-2 z-50 animate-fade-in">
                  <button onClick={() => { setTheme('coral'); setShowThemeMenu(false); }} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-primary/5 flex items-center gap-2 font-medium transition-all">
                    💖 Healing Coral {theme === 'coral' && <span className="ml-auto text-primary font-black">✓</span>}
                  </button>
                  <button onClick={() => { setTheme('teal'); setShowThemeMenu(false); }} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-primary/5 flex items-center gap-2 font-medium transition-all">
                    🌊 Calm Teal {theme === 'teal' && <span className="ml-auto text-primary font-black">✓</span>}
                  </button>
                  <button onClick={() => { setTheme('dark'); setShowThemeMenu(false); }} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-primary/5 flex items-center gap-2 font-medium transition-all">
                    🌙 Midnight Hope {theme === 'dark' && <span className="ml-auto text-primary font-black">✓</span>}
                  </button>
                </div>
              )}
            </div>

            <div className="w-px h-6 bg-gray-200 mx-2"></div>

            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setShowProfileMenu(!showProfileMenu)}
                  className="flex items-center space-x-3 px-3 py-2 rounded-2xl hover:bg-primary/5 transition-all duration-300 border border-transparent hover:border-primary/10"
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shadow-md transition-transform group-hover:scale-105 ${user?.gender === 'female' ? 'bg-gradient-to-br from-pink-400 to-rose-500 text-white' :
                    user?.gender === 'male' ? 'bg-gradient-to-br from-sky-400 to-indigo-500 text-white' :
                      'bg-gradient-to-br from-amber-400 to-orange-500 text-white'
                    }`} style={{ color: 'white' }}>
                    {getUserInitials()}
                  </div>
                  <div className="text-left hidden lg:block">
                    <p className="text-xs font-black text-gray-400 uppercase tracking-tighter leading-none mb-1">Authenticated</p>
                    <p className="text-sm font-bold text-gray-900 leading-none">{user?.name}</p>
                  </div>
                </button>

                {showProfileMenu && (
                  <div className="absolute right-0 mt-2 w-72 glass-panel bg-white/95 py-0 z-50 animate-fade-in overflow-hidden">
                    <div className="px-5 py-4 bg-gradient-to-r from-primary/10 to-primary/5 border-b border-white/50">
                      <p className="text-sm font-black text-gray-900">{user?.name}</p>
                      <p className="text-[10px] text-gray-500 mt-0.5 truncate font-medium">{user?.email}</p>
                    </div>
                    <Link
                      to="/dashboard"
                      onClick={() => setShowProfileMenu(false)}
                      className="block px-5 py-3.5 text-sm text-gray-700 hover:bg-primary/5 transition-all font-medium flex items-center gap-3"
                    >
                      <span className="text-base">📊</span> Dashboard
                    </Link>
                    <Link
                      to="/profile"
                      onClick={() => setShowProfileMenu(false)}
                      className="block px-5 py-3.5 text-sm text-gray-700 hover:bg-primary/5 transition-all font-bold flex items-center gap-3 border-t border-gray-50"
                    >
                      <span className="text-base">👤</span> My Profile
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-5 py-3.5 text-sm text-red-500 hover:bg-red-50/50 transition-all font-black border-t border-gray-100 flex items-center gap-3"
                    >
                      <span className="text-base">🚪</span> Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center space-x-3 lg:space-x-4 ml-4">
                <Link
                  to="/login"
                  className="px-6 py-2.5 rounded-2xl text-sm font-black text-gray-700 hover:text-primary transition-all duration-300 border-2 border-transparent hover:border-primary/10 hover:bg-primary/5"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="px-8 py-3 rounded-2xl text-sm bg-primary text-white font-black shadow-xl shadow-primary/25 hover:shadow-primary/40 hover:-translate-y-0.5 transition-all duration-300 transform active:scale-95"
                >
                  {t('nav.signup')}
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
