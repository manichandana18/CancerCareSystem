import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";
import { useToast } from "../components/Toast";

const API = import.meta.env.VITE_API_URL || '';

interface Wig {
    id: number;
    name: string;
    type: string;
    color: string;
    length: string;
    price: number;
    free: boolean;
    condition: string;
    description: string;
    image: string;
    available: boolean;
}

const CURRENCIES = [
    { code: "INR", symbol: "₹" },
    { code: "USD", symbol: "$" },
    { code: "EUR", symbol: "€" },
    { code: "GBP", symbol: "£" },
];

// Fallback seed data so cards always show even if API is down
const FALLBACK_WIGS: Wig[] = [
    {
        id: 1, name: "Natural Wave Bob", type: "Human Hair", color: "Dark Brown",
        length: "Short", price: 0, free: true, condition: "New",
        description: "Beautiful natural wave bob wig, donated for patients undergoing chemotherapy.",
        image: "💇‍♀️", available: true,
    },
    {
        id: 2, name: "Long Straight Classic", type: "Synthetic", color: "Black",
        length: "Long", price: 0, free: true, condition: "New",
        description: "Comfortable long straight wig, lightweight and breathable for everyday wear.",
        image: "💇", available: true,
    },
    {
        id: 3, name: "Curly Confidence", type: "Human Hair", color: "Auburn",
        length: "Medium", price: 25, free: false, condition: "New",
        description: "Gorgeous curly wig that adds volume and confidence. Subsidized pricing for patients.",
        image: "👩‍🦱", available: true,
    },
    {
        id: 4, name: "Pixie Power", type: "Synthetic", color: "Blonde",
        length: "Short", price: 0, free: true, condition: "Gently Used",
        description: "Chic pixie cut wig, professionally cleaned and ready to wear.",
        image: "✨", available: true,
    },
    {
        id: 5, name: "Silver Grace", type: "Synthetic", color: "Silver/Grey",
        length: "Medium", price: 15, free: false, condition: "New",
        description: "Elegant silver wig for a sophisticated, natural look.",
        image: "🤍", available: true,
    },
    {
        id: 6, name: "Headscarf Collection", type: "Headwear", color: "Assorted",
        length: "N/A", price: 0, free: true, condition: "New",
        description: "Set of 5 beautiful headscarves in assorted colors and patterns.",
        image: "🧕", available: true,
    },
];

// Visual themes for each wig type
const WIG_THEMES: Record<string, { gradient: string; accent: string; glow: string }> = {
    "Human Hair": {
        gradient: "from-rose-400 via-pink-300 to-fuchsia-400",
        accent: "rgba(244, 114, 182, 0.4)",
        glow: "shadow-[0_20px_60px_rgba(244,114,182,0.2)]",
    },
    "Synthetic": {
        gradient: "from-violet-400 via-purple-300 to-indigo-400",
        accent: "rgba(139, 92, 246, 0.4)",
        glow: "shadow-[0_20px_60px_rgba(139,92,246,0.2)]",
    },
    "Headwear": {
        gradient: "from-amber-400 via-orange-300 to-yellow-400",
        accent: "rgba(251, 191, 36, 0.4)",
        glow: "shadow-[0_20px_60px_rgba(251,191,36,0.2)]",
    },
};

const getTheme = (type: string) => WIG_THEMES[type] || WIG_THEMES["Synthetic"];

export default function WigMarketplace() {
    const [wigs, setWigs] = useState<Wig[]>(FALLBACK_WIGS);
    const [filteredWigs, setFilteredWigs] = useState<Wig[]>(FALLBACK_WIGS);
    const [search, setSearch] = useState("");
    const [typeFilter, setTypeFilter] = useState("");
    const [freeOnly, setFreeOnly] = useState(false);
    const [currency, setCurrency] = useState("INR");
    const [selectedWig, setSelectedWig] = useState<Wig | null>(null);
    const [showRequestForm, setShowRequestForm] = useState(false);
    const [patientName, setPatientName] = useState("");
    const [reason, setReason] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [requestSuccess, setRequestSuccess] = useState(false);
    const [hoveredId, setHoveredId] = useState<number | null>(null);
    const navigate = useNavigate();
    const { t } = useLanguage();
    const { showToast } = useToast();

    useEffect(() => {
        loadWigs();
    }, []);

    useEffect(() => {
        let result = wigs;
        if (search) {
            result = result.filter(w =>
                w.name.toLowerCase().includes(search.toLowerCase()) ||
                w.color.toLowerCase().includes(search.toLowerCase())
            );
        }
        if (typeFilter) {
            result = result.filter(w => w.type.toLowerCase().includes(typeFilter.toLowerCase()));
        }
        if (freeOnly) {
            result = result.filter(w => w.free);
        }
        setFilteredWigs(result);
    }, [wigs, search, typeFilter, freeOnly]);

    const loadWigs = async () => {
        try {
            const res = await fetch(`${API}/api/wigs/listings`);
            const data = await res.json();
            if (data.success && data.wigs?.length > 0) setWigs(data.wigs);
        } catch {
            // fallback data is already set
        }
    };

    const currencySymbol = CURRENCIES.find(c => c.code === currency)?.symbol || "₹";

    const convertPrice = (usdPrice: number) => {
        const rates: Record<string, number> = { INR: 83, USD: 1, EUR: 0.92, GBP: 0.79 };
        return Math.round(usdPrice * (rates[currency] || 1));
    };

    const getWigKey = (title: string) => {
        const mapping: { [key: string]: string } = {
            "Natural Wave Bob": "natural_bob",
            "Long Straight Classic": "long_straight",
            "Curly Confidence": "curly_confidence",
            "Pixie Power": "pixie_power",
            "Silver Grace": "silver_grace",
            "Headscarf Collection": "headscarf"
        };
        return mapping[title] || title.toLowerCase().replace(/ /g, "_");
    };

    const handleRequest = async () => {
        if (!selectedWig || !patientName) return;
        setIsSubmitting(true);
        try {
            const token = localStorage.getItem("sessionToken");
            const headers: Record<string, string> = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = `Bearer ${token}`;

            const res = await fetch(`${API}/api/wigs/request`, {
                method: "POST",
                headers,
                body: JSON.stringify({
                    wig_id: selectedWig.id,
                    patient_name: patientName,
                    reason,
                }),
            });
            const data = await res.json();
            if (data.success) {
                setRequestSuccess(true);
                setShowRequestForm(false);
            } else {
                showToast(data.detail || 'Failed to submit request', 'error');
            }
        } catch {
            showToast('Failed to submit request. Please log in first.', 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    // ── Success Screen ──
    if (requestSuccess) {
        return (
            <div className="max-w-2xl mx-auto text-center animate-fade-in px-4">
                <div className="glass-panel p-16 relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-primary)]/5 via-transparent to-[var(--color-accent)]/5" />
                    <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full bg-[var(--color-primary)]/10 blur-3xl animate-float" />
                    <div className="absolute -bottom-20 -left-20 w-60 h-60 rounded-full bg-[var(--color-accent)]/10 blur-3xl animate-float [animation-delay:2s]" />
                    <div className="relative z-10">
                        <div className="text-8xl mb-8 animate-bounce">🎉</div>
                        <h2 className="text-4xl font-heading font-black mb-4" style={{ color: "var(--color-primary)" }}>
                            {t('wigs.request_submitted')}
                        </h2>
                        <p className="text-gray-500 text-lg mb-10 max-w-md mx-auto font-medium">{t('wigs.request_success_msg')}</p>
                        <button onClick={() => { setRequestSuccess(false); setSelectedWig(null); }}
                            className="px-10 py-4 rounded-2xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black text-lg shadow-xl hover:shadow-2xl hover:scale-105 transition-all">
                            {t('wigs.browse_more')}
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto space-y-12 animate-fade-in px-4">
            {/* ── Hero Header ── */}
            <div className="relative text-center py-16 overflow-hidden">
                {/* Animated background blobs */}
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-72 h-72 rounded-full bg-pink-200/30 blur-[100px] animate-float" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-violet-200/30 blur-[100px] animate-float [animation-delay:3s]" />
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-amber-200/20 blur-[80px] animate-float [animation-delay:1.5s]" />
                </div>
                <div className="relative z-10 space-y-6">
                    <div className="inline-flex items-center gap-3 px-6 py-2 rounded-full bg-white/60 backdrop-blur-md border border-white/40 shadow-lg">
                        <span className="text-2xl animate-float">💇</span>
                        <span className="text-xs font-black uppercase tracking-[0.3em] text-gray-500">Wig & Headwear Marketplace</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-heading font-black tracking-tight">
                        <span style={{ color: "var(--color-primary)" }}>{t('wigs.title')}</span>
                    </h1>
                    <p className="text-lg md:text-xl text-gray-500 font-medium max-w-2xl mx-auto leading-relaxed">
                        {t('wigs.subtitle')}
                    </p>
                </div>
            </div>

            {/* ── Quick Stats Bar ── */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                    { icon: "💇‍♀️", label: "Total Wigs", value: wigs.length, color: "from-rose-500 to-pink-500" },
                    { icon: "🎁", label: "Free Items", value: wigs.filter(w => w.free).length, color: "from-emerald-500 to-teal-500" },
                    { icon: "✨", label: "Human Hair", value: wigs.filter(w => w.type === "Human Hair").length, color: "from-violet-500 to-purple-500" },
                    { icon: "🧕", label: "Headwear", value: wigs.filter(w => w.type === "Headwear").length, color: "from-amber-500 to-orange-500" },
                ].map((stat, i) => (
                    <div key={i} className="glass-panel p-5 group hover:border-[var(--color-primary)]/20 transition-all duration-500 hover:-translate-y-1"
                        style={{ animationDelay: `${i * 100}ms` }}>
                        <div className="flex items-center justify-between">
                            <div>
                                <div className="text-xs font-black text-gray-400 uppercase tracking-wider mb-1">{stat.label}</div>
                                <div className="text-3xl font-black" style={{ color: "var(--color-primary)" }}>{stat.value}</div>
                            </div>
                            <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${stat.color} flex items-center justify-center text-2xl shadow-lg group-hover:scale-110 group-hover:rotate-6 transition-all duration-500`}>
                                {stat.icon}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* ── Filters & Currency ── */}
            <div className="glass-panel p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-[var(--color-primary)]/5 blur-3xl" />
                <div className="relative z-10">
                    <h3 className="text-sm font-black uppercase tracking-[0.2em] text-gray-400 mb-5 flex items-center gap-2">
                        <span className="w-8 h-8 rounded-lg bg-[var(--color-primary)]/10 flex items-center justify-center">🔍</span>
                        Find Your Perfect Match
                    </h3>
                    <div className="grid md:grid-cols-4 gap-4 items-end">
                        <div>
                            <label className="block text-xs font-bold mb-2 uppercase tracking-wider text-gray-400">{t('wigs.search_label')}</label>
                            <input type="text" value={search} onChange={(e) => setSearch(e.target.value)}
                                placeholder={t('wigs.search')}
                                className="w-full p-3.5 rounded-xl border-2 border-gray-100 bg-white/70 backdrop-blur-sm focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-all font-medium" />
                        </div>
                        <div>
                            <label className="block text-xs font-bold mb-2 uppercase tracking-wider text-gray-400">{t('wigs.type_label')}</label>
                            <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}
                                className="w-full p-3.5 rounded-xl border-2 border-gray-100 bg-white/70 backdrop-blur-sm focus:border-[var(--color-primary)] transition-all font-medium">
                                <option value="">{t('wigs.all_types')}</option>
                                <option value="Human Hair">{t('wigs.human_hair')}</option>
                                <option value="Synthetic">{t('wigs.synthetic')}</option>
                                <option value="Headwear">{t('wigs.headwear')}</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-xs font-bold mb-2 uppercase tracking-wider text-gray-400">{t('wigs.currency_label')}</label>
                            <select value={currency} onChange={(e) => setCurrency(e.target.value)}
                                className="w-full p-3.5 rounded-xl border-2 border-gray-100 bg-white/70 backdrop-blur-sm focus:border-[var(--color-primary)] transition-all font-medium">
                                {CURRENCIES.map(c => (
                                    <option key={c.code} value={c.code}>{c.symbol} {c.code}</option>
                                ))}
                            </select>
                        </div>
                        <label className="flex items-center space-x-3 cursor-pointer p-3.5 rounded-xl bg-white/50 border-2 border-gray-100 hover:border-green-300 transition-all group">
                            <input type="checkbox" checked={freeOnly} onChange={(e) => setFreeOnly(e.target.checked)}
                                className="w-5 h-5 accent-[var(--color-primary)] rounded" />
                            <span className="text-sm font-black group-hover:text-green-600 transition-colors">{t('wigs.free_only')} 🎁</span>
                        </label>
                    </div>
                </div>
            </div>

            {/* ── Wig Cards Grid ── */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
                {filteredWigs.map((wig, index) => {
                    const wigKey = getWigKey(wig.name);
                    const theme = getTheme(wig.type);
                    const colorKey = wig.color.toLowerCase().replace('/', '_').replace(/ /g, '_');
                    const conditionKey = wig.condition.toLowerCase().replace(/ /g, '_');
                    const lengthKey = wig.length.toLowerCase();
                    const isHovered = hoveredId === wig.id;

                    return (
                        <div key={wig.id}
                            className={`group relative glass-panel overflow-hidden transition-all duration-700 hover:-translate-y-4 flex flex-col h-full border-transparent hover:border-[var(--color-primary)]/20 ${theme.glow}`}
                            style={{
                                animationDelay: `${index * 120}ms`,
                                animation: 'scale-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) both',
                            }}
                            onMouseEnter={() => setHoveredId(wig.id)}
                            onMouseLeave={() => setHoveredId(null)}
                        >
                            {/* Card Visual Header */}
                            <div className="relative h-56 overflow-hidden">
                                {/* Animated gradient background */}
                                <div className="absolute inset-0 opacity-50 group-hover:opacity-70 transition-opacity duration-1000">
                                    <div className={`absolute inset-0 bg-gradient-to-tr ${theme.gradient} animate-gradient`} />
                                    <div className="absolute inset-0 backdrop-blur-3xl" />
                                </div>

                                {/* Floating orbs */}
                                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                                    <div className={`w-28 h-28 rounded-full bg-white/30 backdrop-blur-md border border-white/40 absolute -top-6 -left-6 animate-float transition-transform duration-700 ${isHovered ? 'scale-125' : ''}`} />
                                    <div className={`w-40 h-40 rounded-full bg-white/20 backdrop-blur-lg border border-white/30 absolute -bottom-10 -right-10 animate-float [animation-delay:1s] transition-transform duration-700 ${isHovered ? 'scale-110' : ''}`} />
                                    <div className="w-14 h-14 rounded-2xl bg-white/40 backdrop-blur-xl border border-white/50 rotate-12 absolute top-10 right-10 animate-float [animation-delay:2s]" />
                                </div>

                                {/* Type badge */}
                                <div className="absolute top-4 right-4 z-20">
                                    <div className="bg-white/90 backdrop-blur-md px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.2em] text-gray-700 shadow-xl border border-white/50">
                                        {wig.type === 'Human Hair' ? t('wigs.human_hair') :
                                            wig.type === 'Synthetic' ? t('wigs.synthetic') :
                                                wig.type === 'Headwear' ? t('wigs.headwear') : wig.type}
                                    </div>
                                </div>

                                {/* Free badge */}
                                {wig.free && (
                                    <div className="absolute top-4 left-4 z-20">
                                        <div className="bg-green-500 text-white px-3 py-1.5 rounded-full text-[10px] font-black uppercase tracking-wider shadow-lg animate-pulse-soft">
                                            🎁 FREE
                                        </div>
                                    </div>
                                )}

                                {/* Centre emoji icon */}
                                <div className="absolute inset-0 flex items-center justify-center z-10 transition-transform duration-700 group-hover:scale-125 group-hover:-rotate-6">
                                    <span className="text-7xl drop-shadow-2xl filter saturate-[0.8] brightness-110">
                                        {wig.image}
                                    </span>
                                </div>

                                {/* Bottom fade */}
                                <div className="absolute inset-0 bg-gradient-to-t from-white via-white/20 to-transparent z-20" />
                            </div>

                            {/* Card Content */}
                            <div className="p-8 flex-1 flex flex-col pt-0 relative z-30">
                                <div className="bg-white/80 backdrop-blur-md rounded-2xl p-7 -mt-10 shadow-2xl border border-white/50 flex-1 flex flex-col group-hover:bg-white transition-colors duration-500">
                                    <h3 className="text-2xl font-heading font-black text-gray-900 group-hover:text-[var(--color-primary)] transition-colors mb-3">
                                        {t(`wig.${wigKey}.name`)}
                                    </h3>

                                    {/* Tags */}
                                    <div className="flex flex-wrap gap-2 mb-4">
                                        <span className="text-[10px] font-black px-3 py-1 bg-gray-50 text-gray-500 rounded-lg border border-gray-100 uppercase tracking-wider">
                                            {t(`color.${colorKey}`)}
                                        </span>
                                        <span className="text-[10px] font-black px-3 py-1 bg-teal-50/80 text-[var(--color-primary)] rounded-lg border border-teal-100 uppercase tracking-wider">
                                            {lengthKey === 'short' ? t('wigs.short') :
                                                lengthKey === 'medium' ? t('wigs.medium') :
                                                    lengthKey === 'long' ? t('wigs.long') : t(`length.${lengthKey}`)}
                                        </span>
                                        <span className="text-[10px] font-black px-3 py-1 bg-green-50 text-green-700 rounded-lg border border-green-100 uppercase tracking-wider">
                                            {t(`condition.${conditionKey}`)}
                                        </span>
                                    </div>

                                    <p className="text-gray-500 leading-relaxed line-clamp-2 font-medium text-sm mb-6 flex-1">
                                        {t(`wig.${wigKey}.desc`)}
                                    </p>

                                    {/* Price */}
                                    <div className="mb-5">
                                        {wig.free ? (
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl font-black text-green-600">FREE</span>
                                                <span className="text-xl">🎁</span>
                                            </div>
                                        ) : (
                                            <div className="flex items-baseline gap-1">
                                                <span className="text-3xl font-black" style={{ color: "var(--color-primary)" }}>
                                                    {currencySymbol}{convertPrice(wig.price).toLocaleString()}
                                                </span>
                                                <span className="text-xs text-gray-400 font-bold">subsidized</span>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* CTA Button */}
                                <div className="mt-auto pt-6">
                                    <button onClick={() => { setSelectedWig(wig); setShowRequestForm(true); }}
                                        className="w-full py-5 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-hover)] text-white font-black text-sm tracking-wider shadow-lg hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] transition-all relative overflow-hidden group/btn">
                                        <span className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 -translate-x-full group-hover/btn:translate-x-full transition-transform duration-700" />
                                        <span className="relative z-10 flex items-center justify-center gap-2">
                                            {t('wigs.request')}
                                            <span className="text-lg group-hover/btn:translate-x-1 transition-transform">→</span>
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {filteredWigs.length === 0 && (
                <div className="glass-panel p-16 text-center animate-fade-in">
                    <div className="text-6xl mb-6 animate-float">🔍</div>
                    <p className="text-xl text-gray-500 font-black mb-2">No wigs found</p>
                    <p className="text-gray-400 font-medium">{t('wigs.no_results')}</p>
                </div>
            )}

            {/* ── Request Modal ── */}
            {showRequestForm && selectedWig && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-fade-in">
                    <div className="glass-panel p-10 max-w-md w-full space-y-6 relative overflow-hidden"
                        style={{ animation: 'scale-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) both' }}>
                        <div className="absolute -top-20 -right-20 w-40 h-40 rounded-full bg-[var(--color-primary)]/10 blur-3xl" />
                        <div className="absolute -bottom-20 -left-20 w-40 h-40 rounded-full bg-[var(--color-accent)]/10 blur-3xl" />
                        <div className="relative z-10 space-y-5">
                            <div className="text-center">
                                <span className="text-5xl block mb-3">{selectedWig.image}</span>
                                <h3 className="text-2xl font-heading font-black" style={{ color: "var(--color-primary)" }}>
                                    {t('wigs.request_form')}
                                </h3>
                                <p className="text-sm text-gray-400 font-medium mt-1">{t(`wig.${getWigKey(selectedWig.name)}.name`)}</p>
                            </div>
                            <div>
                                <label className="block text-sm font-black mb-2 text-gray-600">{t('wigs.patient_name')} *</label>
                                <input type="text" value={patientName} onChange={(e) => setPatientName(e.target.value)}
                                    placeholder={t('wigs.patient_name_placeholder')}
                                    className="w-full p-4 rounded-xl border-2 border-gray-100 bg-white/70 backdrop-blur-sm focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20 transition-all font-medium" />
                            </div>
                            <div>
                                <label className="block text-sm font-black mb-2 text-gray-600">{t('wigs.reason')}</label>
                                <textarea value={reason} onChange={(e) => setReason(e.target.value)}
                                    placeholder={t('wigs.reason_placeholder')}
                                    className="w-full p-4 rounded-xl border-2 border-gray-100 bg-white/70 backdrop-blur-sm focus:border-[var(--color-primary)] transition-all font-medium h-24 resize-none" />
                            </div>
                            <div className="flex gap-3 pt-2">
                                <button onClick={() => setShowRequestForm(false)}
                                    className="flex-1 py-4 rounded-xl bg-gray-100 font-black text-gray-500 hover:bg-gray-200 transition-all">
                                    {t('wigs.cancel')}
                                </button>
                                <button onClick={handleRequest} disabled={isSubmitting || !patientName}
                                    className="flex-1 py-4 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-xl disabled:opacity-50 hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] transition-all">
                                    {isSubmitting ? t('wigs.submitting') : t('wigs.submit_request')}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* ── Donate CTA Banner ── */}
            <div className="relative overflow-hidden rounded-[var(--radius-zen)] p-10 bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] shadow-3xl group">
                <div className="absolute inset-0 bg-white/10 group-hover:bg-transparent transition-colors duration-700" />
                <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full bg-white/10 blur-3xl animate-float" />
                <div className="absolute -bottom-20 -left-20 w-60 h-60 rounded-full bg-white/10 blur-3xl animate-float [animation-delay:2s]" />
                <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="flex items-center gap-6">
                        <div className="text-5xl animate-float">💝</div>
                        <div>
                            <h3 className="text-2xl font-heading font-black text-white mb-1">Have a wig to donate?</h3>
                            <p className="text-white/80 font-medium">{t('wigs.donate_cta')}</p>
                        </div>
                    </div>
                    <button onClick={() => navigate("/donate")}
                        className="px-10 py-4 rounded-2xl bg-white text-[var(--color-primary)] font-black text-lg shadow-xl hover:shadow-2xl hover:scale-105 transition-all whitespace-nowrap">
                        {t('wigs.donate_btn')} →
                    </button>
                </div>
            </div>
        </div>
    );
}
