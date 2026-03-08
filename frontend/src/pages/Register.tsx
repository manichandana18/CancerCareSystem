import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';

export default function Register() {
    const navigate = useNavigate();
    const { register, verifyOtp, login, registrationOtp } = useAuth();
    const { t } = useLanguage();

    const [showPassword, setShowPassword] = useState(false);
    const [passwordStrength, setPasswordStrength] = useState(0); // 0-3
    const [otpArray, setOtpArray] = useState(['', '', '', '', '', '']);
    const [isSuccess, setIsSuccess] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        age: '',
        gender: '',
    });
    const [otp, setOtp] = useState('');
    const [step, setStep] = useState(1); // 1: Register, 2: OTP
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [serverOtp, setServerOtp] = useState('');

    useEffect(() => {
        if (registrationOtp) {
            setOtp(registrationOtp);
            setOtpArray(registrationOtp.split(''));
        }
    }, [registrationOtp]);

    const checkPasswordStrength = (pass: string) => {
        let strength = 0;
        if (pass.length >= 8) strength++;
        if (/[A-Z]/.test(pass) && /[0-9]/.test(pass)) strength++;
        if (/[^A-Za-z0-9]/.test(pass)) strength++;
        setPasswordStrength(strength);
    };

    const handleRegisterSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (formData.password.length < 8) {
            setError('Password must be at least 8 characters long');
            return;
        }

        setIsLoading(true);

        try {
            const data = await register(
                formData.name,
                formData.email,
                formData.phone,
                formData.password,
                parseInt(formData.age),
                formData.gender
            );
            if (data.otp) {
                setServerOtp(data.otp);
            }
            setStep(2);
        } catch (err: any) {
            setError(t('auth.invalid'));
        } finally {
            setIsLoading(false);
        }
    };

    const handleOtpChange = (value: string, index: number) => {
        if (value.length > 1) value = value.slice(-1);
        if (!/^\d*$/.test(value)) return;

        const newOtpArray = [...otpArray];
        newOtpArray[index] = value;
        setOtpArray(newOtpArray);
        setOtp(newOtpArray.join(''));

        // Auto focus next
        if (value && index < 5) {
            const nextInput = document.getElementById(`otp-${index + 1}`);
            nextInput?.focus();
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
        if (e.key === 'Backspace' && !otpArray[index] && index > 0) {
            const prevInput = document.getElementById(`otp-${index - 1}`);
            prevInput?.focus();
        }
    };

    const handleOtpSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            await verifyOtp(formData.email, otp);
            setIsSuccess(true);
            setTimeout(async () => {
                await login(formData.email, formData.password);
                navigate('/dashboard');
            }, 1500);
        } catch (err: any) {
            setError(err.message || 'Verification failed. Please check your OTP.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
        if (e.target.name === 'password') {
            const val = (e.target as HTMLInputElement).value;
            checkPasswordStrength(val);
        }
    };

    return (
        <div className="min-h-screen flex">
            {/* Left Side - Form Container */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8 bg-white relative">
                {isSuccess && (
                    <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-white/95 backdrop-blur-sm animate-success">
                        <div className="w-24 h-24 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-5xl mb-6 shadow-lg">
                            ✓
                        </div>
                        <h2 className="text-3xl font-heading font-black text-gray-900 mb-2">Welcome Aboard!</h2>
                        <p className="text-gray-500 font-bold">Registration Successful</p>
                    </div>
                )}

                <div className="w-full max-w-md animate-fade-in">
                    {step === 1 ? (
                        <>
                            <div className="text-center mb-10">
                                <div className="lg:hidden text-5xl mb-6">🎗️</div>
                                <h1 className="text-4xl font-heading font-bold text-gray-900 mb-2">{t('reg.title')}</h1>
                                <p className="text-gray-500 font-medium">Join thousands in the journey to better health</p>
                            </div>

                            {error && (
                                <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-2xl animate-shake flex items-start gap-3">
                                    <span className="text-xl">⚠️</span>
                                    <p className="text-red-600 text-sm font-semibold pt-0.5">{error}</p>
                                </div>
                            )}

                            <form onSubmit={handleRegisterSubmit} className="space-y-4">
                                <div className="space-y-1">
                                    <label className="text-sm font-bold text-gray-700 ml-1">{t('reg.name')}</label>
                                    <input
                                        name="name"
                                        type="text"
                                        required
                                        value={formData.name}
                                        onChange={handleChange}
                                        className="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                        placeholder="Full Name"
                                    />
                                </div>

                                <div className="space-y-1">
                                    <label className="text-sm font-bold text-gray-700 ml-1">{t('login.email')}</label>
                                    <input
                                        name="email"
                                        type="email"
                                        required
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                        placeholder="Email"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-1">
                                        <label className="text-sm font-bold text-gray-700 ml-1">Age</label>
                                        <input
                                            name="age"
                                            type="number"
                                            required
                                            min="1"
                                            max="120"
                                            value={formData.age}
                                            onChange={handleChange}
                                            className="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                            placeholder="Age"
                                        />
                                    </div>
                                    <div className="space-y-1">
                                        <label className="text-sm font-bold text-gray-700 ml-1">Gender Identity</label>
                                        <div className="grid grid-cols-2 gap-3">
                                            {['male', 'female'].map((g) => (
                                                <button
                                                    key={g}
                                                    type="button"
                                                    onClick={() => setFormData(prev => ({ ...prev, gender: g }))}
                                                    className={`py-3.5 px-4 rounded-xl border-2 font-bold transition-all duration-300 flex items-center justify-center gap-2 ${formData.gender === g
                                                        ? 'border-primary bg-primary/5 text-primary shadow-lg shadow-primary/5'
                                                        : 'border-gray-50 bg-gray-50/50 hover:border-gray-100 text-gray-400'
                                                        }`}
                                                >
                                                    <span>{g === 'male' ? '🧔' : '👩'}</span>
                                                    <span className="capitalize">{g}</span>
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-1 relative group">
                                    <label className="text-sm font-bold text-gray-700 ml-1">{t('login.password')}</label>
                                    <div className="relative">
                                        <input
                                            name="password"
                                            type={showPassword ? "text" : "password"}
                                            required
                                            value={formData.password}
                                            onChange={handleChange}
                                            className="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium pr-12"
                                            placeholder="Create Password"
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setShowPassword(!showPassword)}
                                            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary transition-colors focus:outline-none"
                                        >
                                            {showPassword ? "🙈" : "👁️"}
                                        </button>
                                    </div>

                                    {/* Password Strength Meter */}
                                    <div className="px-1 mt-2">
                                        <div className="strength-bar">
                                            <div className={`strength-bar-fill ${passwordStrength === 1 ? 'strength-weak' :
                                                passwordStrength === 2 ? 'strength-medium' :
                                                    passwordStrength === 3 ? 'strength-strong' : ''
                                                }`}></div>
                                        </div>
                                        <div className="flex justify-between mt-1 px-1">
                                            <p className="text-[10px] font-bold text-gray-400 tracking-wider">STRENGTH</p>
                                            <p className={`text-[10px] font-black tracking-widest ${passwordStrength === 1 ? 'text-red-500' :
                                                passwordStrength === 2 ? 'text-amber-500' :
                                                    passwordStrength === 3 ? 'text-green-500' : 'text-gray-300'
                                                }`}>
                                                {passwordStrength === 1 ? 'WEAK' : passwordStrength === 2 ? 'FAIR' : passwordStrength === 3 ? 'STRONG' : 'NONE'}
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-1">
                                    <label className="text-sm font-bold text-gray-700 ml-1">Confirm Password</label>
                                    <input
                                        name="confirmPassword"
                                        type="password"
                                        required
                                        value={formData.confirmPassword}
                                        onChange={handleChange}
                                        className="w-full px-5 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:bg-white focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none transition-all shadow-sm font-medium"
                                        placeholder="Confirm Password"
                                    />
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
                                            {t('reg.processing')}
                                        </>
                                    ) : (
                                        t('reg.submit')
                                    )}
                                </button>
                            </form>
                        </>
                    ) : (
                        <div className="animate-fade-in">
                            <div className="text-center mb-10">
                                <div className="w-20 h-20 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-6 text-4xl shadow-inner animate-bounce">
                                    📩
                                </div>
                                <h1 className="text-4xl font-heading font-bold text-gray-900 mb-2">{t('reg.verify_title')}</h1>
                                <p className="text-gray-500 font-medium">We've sent a 6-digit code to</p>
                                <p className="font-black text-primary break-all text-lg">{formData.email}</p>

                                {(serverOtp || registrationOtp) && (
                                    <div className="mt-8 relative group">
                                        <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 to-coral-500/20 rounded-[2.5rem] blur opacity-75 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                                        <div className="relative p-6 bg-white/80 backdrop-blur-xl border border-white/50 rounded-[2.5rem] shadow-xl text-primary animate-float">
                                            <p className="text-[10px] uppercase font-black tracking-[0.3em] mb-1 opacity-60">Secure OTP Transmitted</p>
                                            <p className="text-5xl font-black tracking-[0.3em] text-gray-900">{serverOtp || registrationOtp}</p>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <form onSubmit={handleOtpSubmit} className="space-y-10">
                                <div className="flex justify-center gap-3">
                                    {otpArray.map((digit, idx) => (
                                        <input
                                            key={idx}
                                            id={`otp-${idx}`}
                                            type="text"
                                            maxLength={1}
                                            value={digit}
                                            onChange={(e) => handleOtpChange(e.target.value, idx)}
                                            onKeyDown={(e) => handleKeyDown(e, idx)}
                                            className="otp-box"
                                            autoFocus={idx === 0}
                                        />
                                    ))}
                                </div>

                                <div className="space-y-4">
                                    <button
                                        type="submit"
                                        disabled={isLoading || otp.length < 6}
                                        className="w-full bg-primary hover:bg-primary-hover text-white py-5 rounded-[2rem] font-black text-xl shadow-xl shadow-primary/30 transition-all transform hover:-translate-y-1 active:scale-95 disabled:opacity-30 flex justify-center items-center"
                                    >
                                        {isLoading ? 'Verifying...' : 'Verify & Launch Dashboard'}
                                    </button>

                                    <button
                                        type="button"
                                        onClick={() => setStep(1)}
                                        className="w-full text-gray-400 font-bold hover:text-primary transition-colors flex items-center justify-center gap-2 text-sm"
                                    >
                                        ← Correct email address
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    <div className="mt-12 text-center border-t border-gray-100 pt-8">
                        <p className="text-gray-500 font-medium">
                            Already have an account?{' '}
                            <Link to="/login" className="text-primary font-black hover:opacity-80 transition-all">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </div>
            </div>

            {/* Right Side - Branding/Visual with Background Image */}
            <div className="hidden lg:flex lg:w-1/2 relative items-center justify-center p-20 overflow-hidden">
                {/* Background image */}
                <div className="absolute inset-0"
                    style={{
                        backgroundImage: 'url(https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1200&q=80&auto=format&fit=crop)',
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }} />
                {/* Overlay */}
                <div className="absolute inset-0"
                    style={{ background: 'linear-gradient(135deg, rgba(2,32,40,0.88) 0%, rgba(6,78,78,0.78) 50%, rgba(13,148,136,0.55) 100%)' }} />
                {/* Floating orbs */}
                <div className="absolute top-20 right-[15%] w-72 h-72 bg-teal-400 opacity-15 rounded-full blur-[120px] animate-float" />
                <div className="absolute bottom-10 left-[10%] w-96 h-96 bg-emerald-500 opacity-10 rounded-full blur-[100px] animate-float" style={{ animationDelay: '3s' }} />

                <div className="relative z-10 text-white text-center max-w-lg animate-fade-in">
                    <div className="text-9xl mb-12 animate-float drop-shadow-2xl">💝</div>
                    <h2 className="text-5xl font-heading font-black mb-6 leading-tight tracking-tight drop-shadow-md">
                        "Empowering Every <br /><span className="italic">Step to Healing.</span>"
                    </h2>
                    <p className="text-xl text-white/80 leading-relaxed font-medium">
                        Join thousands of patients and caregivers finding hope, support, and advanced AI diagnostics on their path to healing.
                    </p>
                    {/* Trust badges */}
                    <div className="flex justify-center gap-6 mt-10 text-white/50 text-[10px] font-bold tracking-[0.15em] uppercase">
                        <span>✓ Free Account</span>
                        <span>✓ Instant Access</span>
                        <span>✓ HIPAA Secure</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
