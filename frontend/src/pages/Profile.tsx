import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { useLanguage } from '../contexts/LanguageContext';

const API = import.meta.env.VITE_API_URL || '';

export default function Profile() {
    const { user, sessionToken } = useAuth();
    const { theme } = useTheme();
    const { t } = useLanguage();

    const [isEditing, setIsEditing] = useState(false);
    const [showPasswordModal, setShowPasswordModal] = useState(false);

    // Edit form state
    const [editName, setEditName] = useState(user?.name || '');
    const [editPhone, setEditPhone] = useState(user?.phone || '');
    const [editAge, setEditAge] = useState(user?.age || '');
    const [editGender, setEditGender] = useState(user?.gender || '');
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState('');

    // Password form state
    const [currentPw, setCurrentPw] = useState('');
    const [newPw, setNewPw] = useState('');
    const [confirmPw, setConfirmPw] = useState('');
    const [pwMessage, setPwMessage] = useState('');
    const [pwSaving, setPwSaving] = useState(false);

    if (!user) return <div className="p-20 text-center">{t('common.loading')}</div>;

    const genderGradient = user?.gender === 'female'
        ? 'from-pink-400 via-rose-400 to-fuchsia-500'
        : user?.gender === 'male'
            ? 'from-sky-400 via-blue-500 to-indigo-500'
            : 'from-amber-400 via-orange-400 to-rose-400';

    const genderShadow = user?.gender === 'female'
        ? 'shadow-pink-300/50'
        : user?.gender === 'male'
            ? 'shadow-blue-300/50'
            : 'shadow-amber-300/50';

    const handleSaveProfile = async () => {
        setSaving(true);
        setMessage('');
        try {
            const res = await fetch(`${API}/api/profile/update`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionToken}`,
                },
                body: JSON.stringify({
                    name: editName || undefined,
                    phone: editPhone || undefined,
                    age: editAge ? Number(editAge) : undefined,
                    gender: editGender || undefined,
                }),
            });
            const data = await res.json();
            if (data.success) {
                setMessage(`✅ ${t('profile.update_success')}`);
                setIsEditing(false);
                // Reload page to refresh user context
                setTimeout(() => window.location.reload(), 1000);
            } else {
                setMessage(`❌ ${data.detail || data.error || t('profile.update_failed')}`);
            }
        } catch {
            setMessage(`❌ ${t('common.error')}`);
        } finally {
            setSaving(false);
        }
    };

    const handleChangePassword = async () => {
        setPwMessage('');
        if (newPw.length < 6) {
            setPwMessage(`❌ ${t('profile.pw_min_length')}`);
            return;
        }
        if (newPw !== confirmPw) {
            setPwMessage(`❌ ${t('profile.pw_mismatch')}`);
            return;
        }
        setPwSaving(true);
        try {
            const res = await fetch(`${API}/api/profile/change-password`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${sessionToken}`,
                },
                body: JSON.stringify({
                    current_password: currentPw,
                    new_password: newPw,
                }),
            });
            const data = await res.json();
            if (data.success) {
                setPwMessage(`✅ ${t('profile.pw_success')}`);
                setCurrentPw('');
                setNewPw('');
                setConfirmPw('');
                setTimeout(() => setShowPasswordModal(false), 1500);
            } else {
                setPwMessage(`❌ ${data.detail || t('common.error')}`);
            }
        } catch {
            setPwMessage(`❌ ${t('common.error')}`);
        } finally {
            setPwSaving(false);
        }
    };

    return (
        <div className={`min-h-screen mesh-bg pt-24 pb-16 px-4 sm:px-6 lg:px-8 theme-${theme}`}>
            <div className="max-w-5xl mx-auto animate-fade-in">

                {/* Cover Header with Avatar */}
                <div className="relative mb-24">
                    <div className={`h-56 md:h-64 rounded-[3rem] overflow-hidden relative bg-gradient-to-br ${genderGradient}`}>
                        <div className="absolute top-0 right-0 w-96 h-96 bg-white/20 rounded-full blur-[100px] translate-x-1/3 -translate-y-1/3 animate-float"></div>
                        <div className="absolute bottom-0 left-0 w-72 h-72 bg-black/10 rounded-full blur-[80px] -translate-x-1/4 translate-y-1/4 animate-float" style={{ animationDelay: '3s' }}></div>
                        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent"></div>
                        <div className="absolute inset-0 opacity-[0.03]"
                            style={{ backgroundImage: 'radial-gradient(circle, white 1px, transparent 1px)', backgroundSize: '30px 30px' }}
                        ></div>
                    </div>

                    <div className="absolute -bottom-16 left-8 md:left-16 group">
                        <div className={`w-36 h-36 rounded-[2rem] border-[5px] border-white shadow-2xl ${genderShadow} flex items-center justify-center text-6xl font-black text-white transition-all duration-700 transform group-hover:scale-110 group-hover:-rotate-3 animate-float bg-gradient-to-br ${genderGradient}`}>
                            {user?.name?.substring(0, 1).toUpperCase() || 'U'}
                        </div>
                        <div className="absolute -bottom-1 -right-1 w-8 h-8 bg-green-400 rounded-full border-4 border-white shadow-lg flex items-center justify-center">
                            <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                        </div>
                    </div>
                </div>

                {/* User Identity Bar */}
                <div className="glass-panel p-8 md:p-10 mb-8">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                        <div>
                            <div className="flex items-center gap-4 mb-2 flex-wrap">
                                <h1 className="text-4xl md:text-5xl font-heading font-black text-gray-900 leading-tight">{user.name}</h1>
                                <span className="px-4 py-1.5 bg-green-50 text-green-600 text-[10px] font-black uppercase tracking-[0.2em] rounded-full border border-green-200 flex items-center gap-2 shadow-sm">
                                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                                    {t('profile.verified')}
                                </span>
                            </div>
                            <p className="text-gray-500 font-bold flex items-center gap-2 text-lg">
                                <span className="text-xl">🛡️</span>
                                <span className="text-primary font-black">{user.security_level?.toUpperCase()}</span> {t('profile.access_level')}
                            </p>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={() => { setIsEditing(!isEditing); setMessage(''); }}
                                className={`px-8 py-3 rounded-2xl font-black shadow-xl hover:-translate-y-1 transition-all duration-300 text-sm border-2 ${isEditing
                                    ? 'border-red-400 text-red-500 bg-red-50 hover:bg-red-100'
                                    : 'border-primary text-primary bg-primary/10 hover:bg-primary/20 shadow-primary/10'
                                    }`}
                            >
                                {isEditing ? `✕ ${t('profile.cancel')}` : `✏️ ${t('profile.edit_profile')}`}
                            </button>
                            <button
                                onClick={() => { setShowPasswordModal(true); setPwMessage(''); }}
                                className="px-8 py-3 bg-white text-gray-700 border-2 border-gray-200 rounded-2xl font-black hover:border-primary/30 hover:text-primary hover:bg-primary/5 transition-all duration-300 text-sm shadow-sm"
                            >
                                🔐 {t('profile.security')}
                            </button>
                        </div>
                    </div>

                    {/* Success/Error Message */}
                    {message && (
                        <div className={`mt-4 p-3 rounded-xl text-sm font-bold ${message.startsWith('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                            {message}
                        </div>
                    )}
                </div>

                {/* Edit Form (collapsible) */}
                {isEditing && (
                    <div className="glass-panel p-8 mb-8 animate-fade-in border-2 border-primary/20">
                        <h3 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-3">
                            <span className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary text-lg">✏️</span>
                            {t('profile.edit_profile')}
                        </h3>
                        <div className="grid md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.full_name')}</label>
                                <input type="text" value={editName} onChange={(e) => setEditName(e.target.value)}
                                    className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                            </div>
                            <div>
                                <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.phone_number')}</label>
                                <input type="tel" value={editPhone} onChange={(e) => setEditPhone(e.target.value)}
                                    placeholder="+91 9876543210"
                                    className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                            </div>
                            <div>
                                <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.age')}</label>
                                <input type="number" value={editAge} onChange={(e) => setEditAge(e.target.value)}
                                    min="1" max="120"
                                    className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                            </div>
                            <div>
                                <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.gender')}</label>
                                <select value={editGender} onChange={(e) => setEditGender(e.target.value)}
                                    className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all">
                                    <option value="">{t('profile.select')}</option>
                                    <option value="male">{t('reg.male')}</option>
                                    <option value="female">{t('reg.female')}</option>
                                    <option value="other">{t('reg.other')}</option>
                                    <option value="prefer_not_to_say">{t('profile.gender.prefer_not_to_say')}</option>
                                </select>
                            </div>
                        </div>
                        <div className="mt-6 flex justify-end">
                            <button onClick={handleSaveProfile} disabled={saving}
                                className="px-10 py-4 rounded-2xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-xl hover:shadow-2xl transition-all disabled:opacity-50 text-sm">
                                {saving ? `⏳ ${t('profile.saving')}` : `💾 ${t('profile.save_changes')}`}
                            </button>
                        </div>
                    </div>
                )}

                {/* Info Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                    {/* Confidential Information */}
                    <div className="glass-panel p-8">
                        <h3 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-3">
                            <span className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary text-lg">🔒</span>
                            {t('profile.confidential_info')}
                        </h3>
                        <div className="space-y-4">
                            {[
                                { icon: '📧', label: t('profile.verified_email'), value: user.email, color: 'bg-blue-50 text-blue-500' },
                                { icon: '📱', label: t('profile.secure_phone'), value: user.phone || t('profile.not_provided'), color: 'bg-purple-50 text-purple-500' },
                                { icon: '🎂', label: t('profile.age'), value: user.age ? `${user.age} ${t('profile.years')}` : 'N/A', color: 'bg-amber-50 text-amber-500' },
                                { icon: '⚧', label: t('profile.gender'), value: user.gender ? (user.gender === 'prefer_not_to_say' ? t('profile.gender.prefer_not_to_say') : t(`reg.${user.gender}`)) : 'N/A', color: 'bg-teal-50 text-teal-500' },
                            ].map((item, i) => (
                                <div key={i} className="flex items-center p-4 bg-white/60 rounded-2xl border border-white/80 hover:bg-white/90 transition-all group">
                                    <div className={`w-12 h-12 ${item.color} rounded-xl flex items-center justify-center text-xl shadow-sm mr-4 group-hover:scale-110 transition-transform`}>
                                        {item.icon}
                                    </div>
                                    <div>
                                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-[0.2em]">{item.label}</p>
                                        <p className="text-gray-900 font-bold text-sm">{item.value}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Account Activity */}
                    <div className="glass-panel p-8">
                        <h3 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-3">
                            <span className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary text-lg">📊</span>
                            {t('profile.account_activity')}
                        </h3>
                        <div className="space-y-4">
                            {[
                                { icon: '📅', label: t('profile.member_since'), value: new Date(user.created_at).toLocaleDateString(), color: 'bg-teal-50 text-teal-500' },
                                { icon: '🕒', label: t('profile.session_status'), value: user.last_login ? t('profile.active_session') : t('profile.just_created'), color: 'bg-green-50 text-green-500' },
                                { icon: '🔐', label: t('profile.security_level'), value: user.security_level?.toUpperCase(), color: 'bg-rose-50 text-rose-500' },
                            ].map((item, i) => (
                                <div key={i} className="flex items-center p-4 bg-white/60 rounded-2xl border border-white/80 hover:bg-white/90 transition-all group">
                                    <div className={`w-12 h-12 ${item.color} rounded-xl flex items-center justify-center text-xl shadow-sm mr-4 group-hover:scale-110 transition-transform`}>
                                        {item.icon}
                                    </div>
                                    <div>
                                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-[0.2em]">{item.label}</p>
                                        <p className="text-gray-900 font-bold text-sm">{item.value}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <p className="text-[10px] text-gray-400 font-bold italic text-right mt-4 tracking-wider">
                            {t('common.last_updated')}: {new Date().toLocaleDateString()}
                        </p>
                    </div>
                </div>

                {/* Quick Stats Ribbon */}
                <div className="glass-panel p-6 mb-8 bg-primary/5">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {[
                            { label: t('profile.scans_done'), val: '0', icon: '🔬' },
                            { label: t('profile.reports'), val: '0', icon: '📋' },
                            { label: t('profile.wellness_score'), val: '—', icon: '💚' },
                            { label: t('profile.trust_level'), val: user.security_level === 'standard' ? '★★★' : '★★★★★', icon: '⭐' },
                        ].map((s, i) => (
                            <div key={i} className="text-center group cursor-default">
                                <div className="text-3xl mb-2 group-hover:scale-125 transition-transform duration-500">{s.icon}</div>
                                <div className="text-2xl font-heading font-black text-gray-900">{s.val}</div>
                                <div className="text-[9px] text-gray-400 font-black uppercase tracking-[0.2em]">{s.label}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* HIPAA Notice */}
                <div className="glass-panel p-6 border-l-4 border-amber-400 bg-amber-50/30">
                    <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 shadow-sm">
                            🔒
                        </div>
                        <div>
                            <h4 className="text-amber-900 font-black text-sm mb-1">{t('profile.hipaa_title')}</h4>
                            <p className="text-amber-800/80 text-xs leading-relaxed font-medium">
                                {t('profile.hipaa_text')}
                            </p>
                        </div>
                    </div>
                </div>

            </div>

            {/* Password Change Modal */}
            {showPasswordModal && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="glass-panel p-8 max-w-md w-full space-y-5 bg-white/95 animate-fade-in">
                        <h3 className="text-xl font-heading font-black text-gray-900 flex items-center gap-3">
                            <span className="text-2xl">🔐</span> {t('profile.change_password')}
                        </h3>

                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.current_password')}</label>
                            <input type="password" value={currentPw} onChange={(e) => setCurrentPw(e.target.value)}
                                className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                        </div>
                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.new_password')}</label>
                            <input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)}
                                placeholder={t('profile.pw_min_length')}
                                className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                        </div>
                        <div>
                            <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{t('profile.confirm_password')}</label>
                            <input type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)}
                                className="w-full p-4 rounded-2xl border-2 border-gray-200 bg-white/60 font-bold focus:border-primary focus:outline-none transition-all" />
                        </div>

                        {pwMessage && (
                            <div className={`p-3 rounded-xl text-sm font-bold ${pwMessage.startsWith('✅') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                                {pwMessage}
                            </div>
                        )}

                        <div className="flex space-x-3">
                            <button onClick={() => setShowPasswordModal(false)}
                                className="flex-1 py-4 rounded-2xl bg-gray-200 font-black hover:bg-gray-300 transition-all text-sm">
                                {t('profile.cancel')}
                            </button>
                            <button onClick={handleChangePassword} disabled={pwSaving || !currentPw || !newPw}
                                className="flex-1 py-4 rounded-2xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-xl disabled:opacity-50 transition-all text-sm">
                                {pwSaving ? `⏳ ${t('profile.changing')}` : `🔐 ${t('profile.change_password')}`}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
