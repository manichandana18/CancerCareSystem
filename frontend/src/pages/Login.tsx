import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();
    const { t } = useLanguage();

    const [showPassword, setShowPassword] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await login(formData.email, formData.password);
            navigate('/dashboard');
        } catch (err: any) {
            const message = err.message.includes('locked') ? t('auth.locked') : t('auth.invalid');
            setError(message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <div className="min-h-screen flex">
            {/* Left Side - Visual/Branding with Background Image */}
            <div className="hidden lg:flex lg:w-1/2 relative items-center justify-center p-20 overflow-hidden">
                {/* Background image */}
                <div className="absolute inset-0"
                    style={{
                        backgroundImage: 'url(https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200&q=80&auto=format&fit=crop)',
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }} />
                {/* Overlay */}
                <div className="absolute inset-0"
                    style={{ background: 'linear-gradient(135deg, rgba(2,32,40,0.85) 0%, rgba(6,78,78,0.75) 50%, rgba(13,148,136,0.6) 100%)' }} />
                {/* Floating orbs */}
                <div className="absolute top-20 right-[15%] w-72 h-72 bg-teal-400 opacity-15 rounded-full blur-[120px] animate-float" />
                <div className="absolute bottom-10 left-[10%] w-96 h-96 bg-emerald-500 opacity-10 rounded-full blur-[100px] animate-float" style={{ animationDelay: '3s' }} />

                <div className="relative z-10 text-white text-center max-w-lg animate-fade-in">
                    <div className="text-9xl mb-12 drop-shadow-2xl hover:scale-110 transition-transform duration-500 cursor-default">🎗️</div>
                    <h2 className="text-6xl font-heading font-black mb-6 leading-tight tracking-tight drop-shadow-md">
                        {t('login.title')}
                    </h2>
                    <p className="text-xl text-white/80 leading-relaxed font-medium">
                        Continuing your journey with compassionate care and world-class AI diagnostics.
                    </p>
                    {/* Trust badges */}
                    <div className="flex justify-center gap-6 mt-10 text-white/50 text-[10px] font-bold tracking-[0.15em] uppercase">
                        <span>✓ HIPAA</span>
                        <span>✓ AES-256</span>
                        <span>✓ Zero-Knowledge</span>
                    </div>
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white">
                <div className="w-full max-w-md animate-fade-in">
                    <div className="text-center mb-12">
                        <div className="lg:hidden text-5xl mb-6">🎗️</div>
                        <h1 className="text-4xl font-heading font-bold text-gray-900 mb-2">{t('login.title')}</h1>
                        <p className="text-gray-500 font-medium">Welcome back to your health companion</p>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-2xl animate-shake flex items-start gap-3">
                            <span className="text-xl">⚠️</span>
                            <p className="text-red-600 text-sm font-semibold pt-0.5">
                                {error}
                            </p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-bold text-gray-700 ml-1">{t('login.email')}</label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary transition-all">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                    </svg>
                                </div>
                                <input
                                    name="email"
                                    type="email"
                                    required
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="w-full pl-12 pr-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                    placeholder="you@example.com"
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between items-center ml-1">
                                <label className="text-sm font-bold text-gray-700">{t('login.password')}</label>
                                <Link to="#" className="text-xs font-bold text-primary hover:opacity-80 transition-all underline outline-none">
                                    Forgot password?
                                </Link>
                            </div>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary transition-all">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                                    </svg>
                                </div>
                                <input
                                    name="password"
                                    type={showPassword ? "text" : "password"}
                                    required
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="w-full pl-12 pr-12 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                    placeholder="••••••••"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-primary transition-colors focus:outline-none"
                                >
                                    {showPassword ? (
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                                        </svg>
                                    ) : (
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                        </svg>
                                    )}
                                </button>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-primary hover:bg-primary-hover text-white py-5 rounded-2xl font-black text-xl shadow-xl shadow-primary/20 transition-all transform hover:-translate-y-1 active:scale-95 disabled:opacity-50 mt-4 flex justify-center items-center btn-premium"
                        >
                            {isLoading ? (
                                <>
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    {t('login.processing')}
                                </>
                            ) : (
                                t('login.submit')
                            )}
                        </button>
                    </form>

                    <div className="mt-8 text-center border-t border-gray-100 pt-8">
                        <p className="text-gray-600">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-primary-600 hover:text-primary-700 font-bold underline-offset-4 hover:underline">
                                Sign up now
                            </Link>
                        </p>
                    </div>

                    <div className="mt-8 text-center">
                        <Link to="/" className="text-sm text-gray-400 hover:text-gray-600 transition-colors flex items-center justify-center gap-2">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                            </svg>
                            Back to Home
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
