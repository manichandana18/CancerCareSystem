import { useState, useEffect } from "react";
import { useLanguage } from "../contexts/LanguageContext";
import { useToast } from "../components/Toast";

const API = import.meta.env.VITE_API_URL || '';

const CURRENCIES = [
    { code: "INR", symbol: "₹", key: "curr.inr" },
    { code: "USD", symbol: "$", key: "curr.usd" },
    { code: "EUR", symbol: "€", key: "curr.eur" },
    { code: "GBP", symbol: "£", key: "curr.gbp" },
    { code: "AUD", symbol: "A$", key: "curr.aud" },
    { code: "CAD", symbol: "C$", key: "curr.cad" },
    { code: "JPY", symbol: "¥", key: "curr.jpy" },
];

const PAYMENT_MODES = [
    { id: "upi", labelKey: "pay.upi.label", icon: "📱", descKey: "pay.upi.desc" },
    { id: "card", labelKey: "pay.card.label", icon: "💳", descKey: "pay.card.desc" },
    { id: "netbanking", labelKey: "pay.netbanking.label", icon: "🏦", descKey: "pay.netbanking.desc" },
    { id: "wallet", labelKey: "pay.wallet.label", icon: "👛", descKey: "pay.wallet.desc" },
    { id: "crypto", labelKey: "pay.crypto.label", icon: "🪙", descKey: "pay.crypto.desc" },
];

const PRESET_AMOUNTS: Record<string, number[]> = {
    INR: [100, 500, 1000, 5000],
    USD: [5, 10, 25, 100],
    EUR: [5, 10, 25, 100],
    GBP: [5, 10, 25, 100],
    AUD: [5, 10, 25, 100],
    CAD: [5, 10, 25, 100],
    JPY: [500, 1000, 2500, 10000],
};

interface DonationStats {
    total_monetary_donations: number;
    total_amount_raised: number;
    total_wigs_donated: number;
    patients_helped: number;
}

export default function Donation() {
    const { t } = useLanguage();
    const { showToast } = useToast();
    const [tab, setTab] = useState<"money" | "wig">("money");
    const [amount, setAmount] = useState(0);
    const [currency, setCurrency] = useState("INR");
    const [paymentMode, setPaymentMode] = useState("");
    const [donorName, setDonorName] = useState("");
    const [message, setMessage] = useState("");
    const [anonymous, setAnonymous] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [success, setSuccess] = useState(false);
    const [stats, setStats] = useState<DonationStats | null>(null);

    // Wig donation fields
    const [wigType, setWigType] = useState("synthetic");
    const [wigColor, setWigColor] = useState("");
    const [wigLength, setWigLength] = useState("medium");
    const [wigCondition, setWigCondition] = useState("new");

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const res = await fetch(`${API}/api/donations/stats`);
            const data = await res.json();
            if (data.success) setStats(data.stats);
        } catch (e) { console.error(e); }
    };

    const currencySymbol = CURRENCIES.find(c => c.code === currency)?.symbol || "";

    const handleMoneyDonate = async () => {
        if (amount <= 0) { showToast('Please enter a valid amount', 'warning'); return; }
        if (!paymentMode) { showToast('Please select a payment method', 'warning'); return; }

        setIsSubmitting(true);
        try {
            const token = localStorage.getItem("sessionToken");
            const headers: Record<string, string> = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = `Bearer ${token}`;

            const res = await fetch(`${API}/api/donations/monetary`, {
                method: "POST",
                headers,
                body: JSON.stringify({ amount, currency, donor_name: donorName, message, anonymous, type: "monetary" }),
            });
            const data = await res.json();
            if (data.success) { setSuccess(true); fetchStats(); }
        } catch (e) {
            showToast('Failed to process donation.', 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleWigDonate = async () => {
        if (!wigColor) { showToast('Please enter the wig color', 'warning'); return; }

        setIsSubmitting(true);
        try {
            const token = localStorage.getItem("sessionToken");
            const headers: Record<string, string> = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = `Bearer ${token}`;

            const res = await fetch(`${API}/api/donations/wig`, {
                method: "POST",
                headers,
                body: JSON.stringify({ wig_type: wigType, color: wigColor, length: wigLength, condition: wigCondition, donor_name: donorName, message }),
            });
            const data = await res.json();
            if (data.success) { setSuccess(true); fetchStats(); }
        } catch (e) {
            showToast('Failed to process wig donation.', 'error');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (success) {
        return (
            <div className="max-w-2xl mx-auto text-center glass-panel p-12">
                <div className="text-7xl mb-6 animate-float">💕</div>
                <h2 className="text-3xl font-heading font-black mb-4" style={{ color: "var(--color-primary)" }}>
                    {t('donate.success')}
                </h2>
                <p className="text-gray-600 mb-8">{t('donate.subtitle')}</p>
                <button onClick={() => { setSuccess(false); setAmount(0); setPaymentMode(""); }}
                    className="px-8 py-3 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-lg">
                    {t('donate.submit')}
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div className="glass-panel p-8 text-center">
                <h1 className="text-3xl font-heading font-black mb-2" style={{ color: "var(--color-primary)" }}>
                    💝 {t('donate.title')}
                </h1>
                <p className="text-gray-500 font-medium">{t('donate.subtitle')}</p>
            </div>

            {/* Impact Stats */}
            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                        { label: t('donate.total_donors'), value: stats.total_monetary_donations, icon: "🎁" },
                        { label: t('donate.total_donated'), value: `$${stats.total_amount_raised.toLocaleString()}`, icon: "💰" },
                        { label: t('donate.wigs_donated'), value: stats.total_wigs_donated, icon: "💇" },
                        { label: t('donate.patients_helped'), value: stats.patients_helped, icon: "❤️" },
                    ].map((s, i) => (
                        <div key={i} className="glass-panel p-4 text-center">
                            <div className="text-2xl mb-1">{s.icon}</div>
                            <div className="text-xl font-black" style={{ color: "var(--color-primary)" }}>{s.value}</div>
                            <div className="text-xs text-gray-500 font-bold uppercase">{s.label}</div>
                        </div>
                    ))}
                </div>
            )}

            {/* Tabs */}
            <div className="flex rounded-xl overflow-hidden bg-white/50">
                <button onClick={() => setTab("money")}
                    className={`flex-1 py-3 font-black text-sm transition-all ${tab === "money" ? "bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white" : "text-gray-500"}`}>
                    💰 {t('donate.monetary')}
                </button>
                <button onClick={() => setTab("wig")}
                    className={`flex-1 py-3 font-black text-sm transition-all ${tab === "wig" ? "bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white" : "text-gray-500"}`}>
                    💇 {t('donate.wig_donation')}
                </button>
            </div>

            {tab === "money" && (
                <div className="glass-panel p-8 space-y-6">
                    {/* Currency */}
                    <div>
                        <label className="block text-sm font-bold mb-2">💱 {t('donate.currency')}</label>
                        <div className="grid grid-cols-4 md:grid-cols-7 gap-2">
                            {CURRENCIES.map((c) => (
                                <button key={c.code} onClick={() => setCurrency(c.code)}
                                    title={t(c.key)}
                                    className={`py-2 px-3 rounded-xl text-sm font-bold transition-all border-2 ${currency === c.code
                                        ? "border-[var(--color-primary)] bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
                                        : "border-gray-200 text-gray-500 hover:border-gray-300"
                                        }`}>
                                    {c.symbol} {c.code}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Amount */}
                    <div>
                        <label className="block text-sm font-bold mb-2">{t('donate.amount')}</label>
                        <div className="grid grid-cols-4 gap-3 mb-3">
                            {(PRESET_AMOUNTS[currency] || PRESET_AMOUNTS.USD).map((preset) => (
                                <button key={preset} onClick={() => setAmount(preset)}
                                    className={`py-3 rounded-xl font-bold transition-all border-2 ${amount === preset
                                        ? "border-[var(--color-primary)] bg-[var(--color-primary)] text-white"
                                        : "border-gray-200 hover:border-gray-300"
                                        }`}>
                                    {currencySymbol}{preset.toLocaleString()}
                                </button>
                            ))}
                        </div>
                        <div className="flex items-center space-x-2">
                            <span className="text-lg font-bold text-gray-500">{currencySymbol}</span>
                            <input type="number" value={amount || ""} onChange={(e) => setAmount(Number(e.target.value))}
                                placeholder={t('donate.amount')}
                                className="flex-1 p-3 rounded-xl border border-gray-200 bg-white/50 text-lg font-bold" />
                        </div>
                    </div>

                    {/* Payment Mode */}
                    <div>
                        <label className="block text-sm font-bold mb-2">💳 {t('donate.payment_method')}</label>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {PAYMENT_MODES.map((pm) => (
                                <button key={pm.id} onClick={() => setPaymentMode(pm.id)}
                                    className={`flex items-center space-x-3 p-4 rounded-xl transition-all border-2 text-left ${paymentMode === pm.id
                                        ? "border-[var(--color-primary)] bg-[var(--color-primary)]/10"
                                        : "border-gray-200 hover:border-gray-300"
                                        }`}>
                                    <span className="text-2xl">{pm.icon}</span>
                                    <div>
                                        <div className="font-bold text-sm">{t(pm.labelKey)}</div>
                                        <div className="text-xs text-gray-500">{t(pm.descKey)}</div>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Donor info */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.donor_name')}</label>
                            <input type="text" value={donorName} onChange={(e) => setDonorName(e.target.value)}
                                placeholder={t('donate.donor_name')} disabled={anonymous}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50 disabled:opacity-50" />
                        </div>
                        <div>
                            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)}
                                placeholder={t('common.stay_strong')}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50" />
                        </div>
                    </div>

                    <label className="flex items-center space-x-2 cursor-pointer">
                        <input type="checkbox" checked={anonymous} onChange={(e) => setAnonymous(e.target.checked)}
                            className="w-4 h-4 accent-[var(--color-primary)]" />
                        <span className="text-sm font-medium">{t('donate.anonymous')}</span>
                    </label>

                    <button onClick={handleMoneyDonate} disabled={isSubmitting}
                        className="w-full py-4 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50">
                        {isSubmitting ? t('donate.processing') : `${t('donate.submit')} ${currencySymbol}${amount > 0 ? amount.toLocaleString() : ""}`}
                    </button>
                </div>
            )}

            {tab === "wig" && (
                <div className="glass-panel p-8 space-y-6">
                    <div className="grid md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.wig_type')}</label>
                            <select value={wigType} onChange={(e) => setWigType(e.target.value)}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="synthetic">{t('wigs.synthetic')}</option>
                                <option value="human_hair">{t('wigs.human_hair')}</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.wig_color')}</label>
                            <input type="text" value={wigColor} onChange={(e) => setWigColor(e.target.value)}
                                placeholder={t('wigs.color_placeholder')}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50" />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('wigs.length_label')}</label>
                            <select value={wigLength} onChange={(e) => setWigLength(e.target.value)}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="short">{t('wigs.short')}</option>
                                <option value="medium">{t('wigs.medium')}</option>
                                <option value="long">{t('wigs.long')}</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.wig_condition')}</label>
                            <select value={wigCondition} onChange={(e) => setWigCondition(e.target.value)}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="new">{t('donate.new')}</option>
                                <option value="gently_used">{t('donate.gently_used')}</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.donor_name')}</label>
                            <input type="text" value={donorName} onChange={(e) => setDonorName(e.target.value)}
                                placeholder={t('donate.donor_name')}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50" />
                        </div>
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('donate.message')}</label>
                            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)}
                                placeholder={t('common.hope_helps')}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50" />
                        </div>
                    </div>

                    <button onClick={handleWigDonate} disabled={isSubmitting}
                        className="w-full py-4 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black text-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50">
                        {isSubmitting ? t('donate.processing') : `🎁 ${t('donate.wig_donation')}`}
                    </button>
                </div>
            )}

            <div className="glass-panel p-6 text-center">
                <div className="text-sm text-gray-500">
                    🔒 {t('profile.hipaa_text')}
                </div>
            </div>
        </div>
    );
}
