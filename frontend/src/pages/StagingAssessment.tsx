import { useState } from "react";
import { useToast } from "../components/Toast";
import { useLanguage } from "../contexts/LanguageContext";

const API = import.meta.env.VITE_API_URL || '';

export default function StagingAssessment() {
    const { t } = useLanguage();
    const [step, setStep] = useState(1);
    const { showToast } = useToast();
    const [cancerType, setCancerType] = useState("");
    const [formData, setFormData] = useState({
        tumor_size: "",
        lymph_nodes: "",
        metastasis: "",
        pain_level: 0,
        weight_loss: false,
        fatigue_level: "",
        duration_months: 0,
        breathing_difficulty: false,
        coughing_blood: false,
        skin_changes: "",
        lump_detected: false,
        bone_pain: false,
        night_sweats: false,
        swollen_lymph: false,
        headaches: false,
        vision_changes: false,
        seizures: false,
        family_history: false,
        previous_treatment: "none",
    });
    const [assessment, setAssessment] = useState<any | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const CANCER_TYPES = [
        { id: "bone", label: t('upload.bone'), icon: "🦴" },
        { id: "lung", label: t('upload.lung'), icon: "🫁" },
        { id: "blood", label: t('upload.blood'), icon: "🩸" },
        { id: "brain", label: t('upload.brain'), icon: "🧠" },
        { id: "skin", label: t('upload.skin'), icon: "🧴" },
        { id: "breast", label: t('upload.breast'), icon: "🎀" },
    ];

    const handleSubmit = async () => {
        setIsLoading(true);
        try {
            const token = localStorage.getItem("sessionToken");
            const headers: Record<string, string> = { "Content-Type": "application/json" };
            if (token) headers["Authorization"] = `Bearer ${token}`;

            const res = await fetch(`${API}/api/staging/assess`, {
                method: "POST",
                headers,
                body: JSON.stringify({ cancer_type: cancerType, ...formData }),
            });
            const data = await res.json();
            if (data.success) {
                setAssessment(data.assessment);
                setStep(4);
            }
        } catch (err) {
            console.error(err);
            showToast(t('common.error'), 'error');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div className="glass-panel p-8 text-center">
                <h1 className="text-3xl font-heading font-black mb-2" style={{ color: "var(--color-primary)" }}>
                    🔬 {t('staging.title')}
                </h1>
                <p className="text-gray-500 font-medium">
                    {t('staging.subtitle')}
                </p>
            </div>

            {/* Step indicators */}
            <div className="flex justify-center space-x-4 mb-6">
                {[
                    { label: t('staging.step.type') },
                    { label: t('staging.step.symptoms') },
                    { label: t('staging.step.details') },
                    { label: t('staging.step.results') }
                ].map((stepObj, i) => (
                    <div key={i} className="flex items-center space-x-2">
                        <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-black transition-all ${step > i + 1
                                ? "bg-green-500 text-white"
                                : step === i + 1
                                    ? "bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white shadow-lg"
                                    : "bg-gray-200 text-gray-400"
                                }`}
                        >
                            {step > i + 1 ? "✓" : i + 1}
                        </div>
                        <span className={`text-xs font-bold ${step === i + 1 ? "text-gray-900" : "text-gray-400"}`}>
                            {stepObj.label}
                        </span>
                    </div>
                ))}
            </div>

            {/* Step 1: Select Cancer Type */}
            {step === 1 && (
                <div className="glass-panel p-8">
                    <h2 className="text-xl font-black mb-6">{t('staging.select_cancer')}</h2>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        {CANCER_TYPES.map((ct) => (
                            <button
                                key={ct.id}
                                onClick={() => { setCancerType(ct.id); setStep(2); }}
                                className={`glass-panel p-6 text-center border-2 transition-all hover:-translate-y-1 cursor-pointer ${cancerType === ct.id ? "border-[var(--color-primary)] bg-[var(--color-primary)]/10" : "border-white/30"
                                    }`}
                            >
                                <div className="text-4xl mb-2">{ct.icon}</div>
                                <div className="font-black text-sm">{ct.label}</div>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Step 2: Core symptoms (TNM) */}
            {step === 2 && (
                <div className="glass-panel p-8 space-y-6">
                    <h2 className="text-xl font-black mb-2">{t('staging.core_symptoms')} — {cancerType.toUpperCase()}</h2>
                    <p className="text-sm text-gray-500 mb-4">{t('staging.tnm_desc')}</p>

                    <div className="grid md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.tumor_size')}</label>
                            <select value={formData.tumor_size} onChange={(e) => setFormData({ ...formData, tumor_size: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="">{t('opt.unknown')}</option>
                                <option value="small">{t('opt.small')}</option>
                                <option value="medium">{t('opt.medium')}</option>
                                <option value="large">{t('opt.large')}</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.lymph_node_involvement')}</label>
                            <select value={formData.lymph_nodes} onChange={(e) => setFormData({ ...formData, lymph_nodes: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="">{t('opt.none')} / {t('opt.unknown')}</option>
                                <option value="none">{t('opt.lymph.none')}</option>
                                <option value="nearby">{t('opt.lymph.nearby')}</option>
                                <option value="distant">{t('opt.lymph.distant')}</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.metastasis_spread')}</label>
                            <select value={formData.metastasis} onChange={(e) => setFormData({ ...formData, metastasis: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="">{t('opt.unknown')}</option>
                                <option value="no">{t('opt.meta.no')}</option>
                                <option value="suspected">{t('opt.meta.suspected')}</option>
                                <option value="confirmed">{t('opt.meta.confirmed')}</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.pain_level_label')}: {formData.pain_level}</label>
                            <input type="range" min="0" max="10" value={formData.pain_level}
                                onChange={(e) => setFormData({ ...formData, pain_level: parseInt(e.target.value) })}
                                className="w-full accent-[var(--color-primary)]" />
                            <div className="flex justify-between text-xs text-gray-400"><span>{t('staging.no')}</span><span>{t('staging.large')}</span></div>
                        </div>
                    </div>

                    <div className="flex justify-between">
                        <button onClick={() => setStep(1)} className="px-6 py-3 rounded-xl bg-gray-200 font-bold hover:bg-gray-300 transition-all">← {t('staging.previous')}</button>
                        <button onClick={() => setStep(3)} className="px-6 py-3 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-lg hover:shadow-xl transition-all">{t('staging.next')} →</button>
                    </div>
                </div>
            )}

            {/* Step 3: Additional details */}
            {step === 3 && (
                <div className="glass-panel p-8 space-y-6">
                    <h2 className="text-xl font-black mb-2">{t('staging.additional_details')}</h2>

                    <div className="grid md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.fatigue_level')}</label>
                            <select value={formData.fatigue_level} onChange={(e) => setFormData({ ...formData, fatigue_level: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="">{t('opt.none')}</option>
                                <option value="mild">{t('staging.small')}</option>
                                <option value="moderate">{t('staging.medium')}</option>
                                <option value="severe">{t('staging.large')}</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.duration_label')}</label>
                            <input type="number" min="0" max="120" value={formData.duration_months}
                                onChange={(e) => setFormData({ ...formData, duration_months: parseInt(e.target.value) || 0 })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50" />
                        </div>

                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.prev_treatment')}</label>
                            <select value={formData.previous_treatment} onChange={(e) => setFormData({ ...formData, previous_treatment: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="none">{t('opt.treatment.none')}</option>
                                <option value="surgery">{t('opt.treatment.surgery')}</option>
                                <option value="chemo">{t('opt.treatment.chemo')}</option>
                                <option value="radiation">{t('opt.treatment.radiation')}</option>
                                <option value="combination">{t('opt.treatment.combination')}</option>
                            </select>
                        </div>
                    </div>

                    {/* Checkboxes */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {[
                            { key: "weight_loss", label: t('check.weight_loss') },
                            { key: "family_history", label: t('check.family_history') },
                            ...(cancerType === "lung" ? [
                                { key: "breathing_difficulty", label: t('check.breathing_diff') },
                                { key: "coughing_blood", label: t('check.coughing_blood') },
                            ] : []),
                            ...(cancerType === "breast" ? [{ key: "lump_detected", label: t('check.lump_detected') }] : []),
                            ...(cancerType === "bone" ? [{ key: "bone_pain", label: t('check.bone_pain') }] : []),
                            ...(cancerType === "blood" ? [
                                { key: "night_sweats", label: t('check.night_sweats') },
                                { key: "swollen_lymph", label: t('check.swollen_lymph') },
                            ] : []),
                            ...(cancerType === "brain" ? [
                                { key: "headaches", label: t('check.headaches') },
                                { key: "vision_changes", label: t('check.vision_changes') },
                                { key: "seizures", label: t('check.seizures') },
                            ] : []),
                        ].map((item: any) => (
                            <label key={item.key} className="flex items-center space-x-2 glass-panel p-3 cursor-pointer hover:bg-white/60 transition-all rounded-xl">
                                <input type="checkbox" checked={(formData as any)[item.key]}
                                    onChange={(e) => setFormData({ ...formData, [item.key]: e.target.checked })}
                                    className="w-4 h-4 accent-[var(--color-primary)]" />
                                <span className="text-sm font-medium">{item.label}</span>
                            </label>
                        ))}
                    </div>

                    {cancerType === "skin" && (
                        <div>
                            <label className="block text-sm font-bold mb-2">{t('staging.skin_changes_label')}</label>
                            <select value={formData.skin_changes} onChange={(e) => setFormData({ ...formData, skin_changes: e.target.value })}
                                className="w-full p-3 rounded-xl border border-gray-200 bg-white/50">
                                <option value="">{t('opt.none')}</option>
                                <option value="color_change">{t('opt.skin.color')}</option>
                                <option value="irregular_border">{t('opt.skin.border')}</option>
                                <option value="growing">{t('opt.skin.growing')}</option>
                                <option value="bleeding">{t('opt.skin.bleeding')}</option>
                            </select>
                        </div>
                    )}

                    <div className="flex justify-between">
                        <button onClick={() => setStep(2)} className="px-6 py-3 rounded-xl bg-gray-200 font-bold hover:bg-gray-300 transition-all">← {t('staging.previous')}</button>
                        <button onClick={handleSubmit} disabled={isLoading}
                            className="px-8 py-3 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-lg hover:shadow-xl transition-all disabled:opacity-50">
                            {isLoading ? t('staging.assessing') : `🔬 ${t('staging.get_assessment')}`}
                        </button>
                    </div>
                </div>
            )}

            {/* Step 4: Results */}
            {step === 4 && assessment && (
                <div className="space-y-6">
                    {/* Disclaimer */}
                    <div className="glass-panel p-4 bg-amber-50 border-amber-200">
                        <div className="text-sm text-amber-800 font-medium">
                            ⚠️ {t('staging.disclaimer')}
                        </div>
                    </div>

                    {/* Stage result */}
                    <div className="glass-panel p-8 text-center">
                        <div className="text-6xl mb-4" style={{ color: assessment.stage_info.color }}>
                            {assessment.estimated_stage === "Stage 0" ? "🟢" :
                                assessment.estimated_stage === "Stage I" ? "🟡" :
                                    assessment.estimated_stage === "Stage II" ? "🟠" :
                                        assessment.estimated_stage === "Stage III" ? "🔴" : "⛔"}
                        </div>
                        <h2 className="text-4xl font-black mb-2" style={{ color: assessment.stage_info.color }}>
                            {t('staging.estimated_stage')}: {assessment.estimated_stage}
                        </h2>
                        <span className="inline-block px-4 py-1 rounded-full text-sm font-bold text-white mb-4"
                            style={{ backgroundColor: assessment.stage_info.color }}>
                            {assessment.stage_info.severity}
                        </span>
                        <p className="text-gray-600 max-w-lg mx-auto">{assessment.stage_info.description}</p>
                        <p className="text-sm text-gray-500 mt-2 italic">{assessment.stage_info.survival_note}</p>
                    </div>

                    {/* Recommendations */}
                    <div className="glass-panel p-8">
                        <h3 className="text-2xl font-black mb-6">📋 {t('rec.personalized')}</h3>
                        <div className="space-y-4">
                            {assessment.recommendations.map((rec: any, i: number) => (
                                <div key={i} className={`glass-panel p-5 border-l-4 ${rec.priority === "Critical" ? "border-red-500 bg-red-50/50" :
                                    rec.priority === "High" ? "border-orange-500 bg-orange-50/50" :
                                        "border-blue-500 bg-blue-50/50"
                                    }`}>
                                    <div className="flex items-center justify-between mb-1">
                                        <span className="font-black text-sm">{rec.category}</span>
                                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${rec.priority === "Critical" ? "bg-red-200 text-red-800" :
                                            rec.priority === "High" ? "bg-orange-200 text-orange-800" :
                                                "bg-blue-200 text-blue-800"
                                            }`}>{rec.priority === "Critical" ? t('rec.critical') : rec.priority === "High" ? t('rec.high') : t('rec.medium')}</span>
                                    </div>
                                    <h4 className="font-bold text-gray-900">{rec.title}</h4>
                                    <p className="text-sm text-gray-600 mt-1">{rec.description}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="flex justify-center">
                        <button onClick={() => { setStep(1); setAssessment(null); }}
                            className="px-8 py-3 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-lg hover:shadow-xl transition-all">
                            🔄 {t('staging.new_assessment')}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
