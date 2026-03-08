import { useState, useEffect } from "react";
import { useLanguage } from "../contexts/LanguageContext";

const API = import.meta.env.VITE_API_URL || '';

interface Exercise {
    id: number;
    title: string;
    type: string;
    duration: number;
    difficulty: string;
    description: string;
    imageUrl: string;
    steps: string[];
    benefits: string[];
}

// Fallback data so cards always render even if API is unavailable
const FALLBACK_EXERCISES: Exercise[] = [
    {
        id: 1, title: "Deep Breathing", type: "breathing", duration: 120,
        difficulty: "Beginner", description: "A calming deep breathing exercise to reduce stress and anxiety during treatment.",
        imageUrl: "", steps: ["Sit comfortably and close your eyes", "Breathe in through your nose for 4 seconds", "Hold your breath for 4 seconds", "Exhale slowly through your mouth for 4 seconds", "Repeat for the full duration"],
        benefits: ["Reduces anxiety", "Lowers blood pressure", "Improves focus"],
    },
    {
        id: 2, title: "Gentle Yoga Flow", type: "yoga", duration: 600,
        difficulty: "Beginner", description: "A gentle yoga sequence designed for cancer patients to improve flexibility and well-being.",
        imageUrl: "", steps: ["Start in Mountain Pose", "Move to Cat-Cow stretch", "Warrior I pose (both sides)", "Tree Pose for balance", "Seated forward fold", "End in Savasana for relaxation"],
        benefits: ["Improves flexibility", "Reduces fatigue", "Enhances mood"],
    },
    {
        id: 3, title: "Body Scan Meditation", type: "meditation", duration: 600,
        difficulty: "Beginner", description: "Guided body scan meditation to promote relaxation and body awareness.",
        imageUrl: "", steps: ["Lie down comfortably", "Focus attention on your toes", "Gradually move awareness up through your body", "Notice any areas of tension or discomfort", "Send healing breath to those areas", "Complete the scan at the crown of your head"],
        benefits: ["Pain management", "Better sleep", "Body awareness"],
    },
    {
        id: 4, title: "Progressive Muscle Relaxation", type: "relaxation", duration: 480,
        difficulty: "Beginner", description: "Systematic muscle relaxation technique to release physical tension.",
        imageUrl: "", steps: ["Start with your toes - tense for 5 seconds", "Release and notice the relaxation", "Move to calves, then thighs", "Tense fists, arms, shoulders", "Scrunch face muscles then release", "Feel the wave of relaxation"],
        benefits: ["Muscle tension relief", "Stress reduction", "Sleep improvement"],
    },
    {
        id: 5, title: "Gratitude Journaling", type: "mindfulness", duration: 600,
        difficulty: "Beginner", description: "A guided mindfulness exercise focusing on gratitude and positive reflection.",
        imageUrl: "", steps: ["Find a quiet space with a journal", "Write 3 things you are grateful for today", "Describe why each matters to you", "Reflect on a challenge you overcame recently", "Write a kind message to yourself", "Read your entries aloud"],
        benefits: ["Emotional resilience", "Positive outlook", "Mental clarity"],
    },
    {
        id: 6, title: "Chair Yoga for Recovery", type: "yoga", duration: 720,
        difficulty: "Beginner", description: "Accessible yoga practice using a chair, perfect for patients with limited mobility.",
        imageUrl: "", steps: ["Sit tall in a sturdy chair", "Gentle neck rolls (both directions)", "Seated cat-cow stretch", "Seated twist (both sides)", "Ankle and wrist circles", "Finish with seated meditation"],
        benefits: ["Improved mobility", "Accessible for all", "Reduces stiffness"],
    },
    {
        id: 7, title: "Hold & Breathe Cycle", type: "breathing", duration: 300,
        difficulty: "Beginner", description: "A structured breathing exercise with timed inhale-hold-exhale cycles.",
        imageUrl: "", steps: ["Breathe In (4s)", "Hold Breath (4s)", "Breathe Out (4s)", "Repeat cycle"],
        benefits: ["Improved lung capacity", "Mental clarity", "Nervous system calming"],
    },
    {
        id: 8, title: "Bedside Stretch & Relax", type: "yoga", duration: 480,
        difficulty: "Beginner", description: "Gentle stretches you can do from your bed or bedside.",
        imageUrl: "", steps: ["Lie on your back, stretch arms overhead", "Bring knees to chest gently", "Gentle spinal twist to each side", "Stretch one leg to the ceiling", "Switch legs and repeat", "Finish by stretching arms overhead"],
        benefits: ["Improves circulation", "Releases muscle tension", "Accessible from bed"],
    },
];


interface WellnessStats {
    total_sessions: number;
    total_minutes: number;
}

const BreathingAnimator = ({ timer }: { timer: number }) => {
    const { t } = useLanguage();
    // 12s cycle: Inhale(4) -> Hold(4) -> Exhale(4)
    const cycleTime = timer % 12;
    let phase = "";
    let animationClass = "";
    let glowColor = "rgba(13, 148, 136, 0.5)"; // Primary Teal

    if (cycleTime < 4) {
        phase = t('wellness.ritual.breathe_in');
        animationClass = "scale-150"; // Expand
        glowColor = "rgba(13, 148, 136, 0.6)";
    } else if (cycleTime < 8) {
        phase = t('wellness.ritual.hold');
        animationClass = "scale-150 opacity-80"; // Hold at expanded
        glowColor = "rgba(244, 63, 94, 0.5)"; // Accent Coral
    } else {
        phase = t('wellness.ritual.breathe_out');
        animationClass = "scale-100"; // Contract
        glowColor = "rgba(13, 148, 136, 0.4)";
    }

    return (
        <div className="flex flex-col items-center justify-center space-y-16 py-16 overflow-hidden">
            <div className="relative flex items-center justify-center">
                {/* Background Dynamic Ambient Glow */}
                <div
                    className="absolute w-80 h-80 rounded-full blur-[100px] transition-all duration-[4000ms] mix-blend-screen"
                    style={{ backgroundColor: glowColor, opacity: 0.3 }}
                />

                {/* 3D-like Breathing Sphere */}
                <div className={`relative transition-all duration-[4000ms] ease-in-out ${animationClass}`}>
                    {/* Glassmorphic Layer */}
                    <div className="absolute inset-0 rounded-full bg-white/20 backdrop-blur-sm border border-white/30 z-20" />

                    {/* Core Gradient Sphere */}
                    <div className={`w-40 h-40 rounded-full bg-gradient-to-br from-[var(--color-primary)] via-[var(--color-accent)] to-[var(--color-primary)] shadow-[0_0_80px_rgba(13,148,136,0.5)] flex items-center justify-center z-10 animate-gradient`}>
                        <div className="text-white font-heading font-black text-2xl text-center px-4 leading-tight drop-shadow-lg z-30">
                            {phase}
                        </div>
                    </div>

                    {/* Inner Pulse Ring */}
                    <div className="absolute -inset-4 border-2 border-[var(--color-primary)]/20 rounded-full animate-ping opacity-20" />
                </div>

                {/* Timed Instruction Overlay */}
                <div className="absolute -bottom-24 left-1/2 -translate-x-1/2 w-max bg-white/10 backdrop-blur-md px-6 py-2 rounded-full border border-white/20 shadow-xl">
                    <span className="text-sm font-black tracking-widest uppercase text-gray-400">
                        {cycleTime < 4 ? t('wellness.ritual.expand') : cycleTime < 8 ? t('wellness.ritual.keep_still') : t('wellness.ritual.release')}
                    </span>
                </div>
            </div>

            {/* Visual Indicators */}
            <div className="flex space-x-6 items-center">
                {[t('wellness.ritual.inhale'), t('wellness.ritual.hold_short'), t('wellness.ritual.exhale')].map((label, i) => {
                    const isActive = Math.floor(cycleTime / 4) === i;
                    return (
                        <div key={i} className="flex flex-col items-center space-y-3">
                            <div className={`h-1.5 rounded-full transition-all duration-700 ${isActive ? "bg-[var(--color-primary)] w-16 shadow-[0_0_15px_var(--color-primary)]" : "bg-gray-200 w-10"}`} />
                            <span className={`text-[11px] tracking-tighter font-black transition-colors ${isActive ? "text-[var(--color-primary)]" : "text-gray-300"}`}>
                                {label}
                            </span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default function Wellness() {
    const { t } = useLanguage();
    const [exercises, setExercises] = useState<Exercise[]>(FALLBACK_EXERCISES);
    const [typeFilter, setTypeFilter] = useState("");
    const [stats, setStats] = useState<WellnessStats | null>(null);
    const [activeSession, setActiveSession] = useState<Exercise | null>(null);
    const [timer, setTimer] = useState(0);
    const [isRunning, setIsRunning] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);
    const [sessionComplete, setSessionComplete] = useState(false);

    useEffect(() => {
        loadExercises();
        loadStats();
    }, []);

    useEffect(() => {
        let interval: ReturnType<typeof setInterval>;
        if (isRunning && activeSession && timer < activeSession.duration) {
            interval = setInterval(() => {
                setTimer((t) => {
                    const nextTime = t + 1;
                    if (nextTime >= (activeSession?.duration ?? 0)) {
                        setIsRunning(false);
                        setSessionComplete(true);
                        saveSession(activeSession.id, activeSession.duration);
                        return activeSession?.duration ?? 0;
                    }
                    if (activeSession.type === 'breathing') {
                        const cycleLength = 12;
                        const stepIndex = Math.floor((nextTime % cycleLength) / 4);
                        setCurrentStep(stepIndex + 1);
                    }
                    return nextTime;
                });
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isRunning, activeSession]);

    const loadExercises = async () => {
        try {
            const res = await fetch(`${API}/api/wellness/exercises`);
            const data = await res.json();
            if (data.success && data.exercises?.length > 0) setExercises(data.exercises);
        } catch {
            // fallback data is already set
        }
    };

    const loadStats = async () => {
        const token = localStorage.getItem("sessionToken");
        if (!token) return;
        try {
            const res = await fetch(`${API}/api/wellness/sessions/stats`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await res.json();
            if (data.success) setStats(data.stats);
        } catch { /* not logged in */ }
    };

    const saveSession = async (exerciseId: number, duration: number) => {
        const token = localStorage.getItem("sessionToken");
        if (!token) return;
        try {
            await fetch(`${API}/api/wellness/sessions/complete`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ exercise_id: exerciseId, duration_completed: duration }),
            });
            loadStats();
        } catch { /* silent */ }
    };

    const formatTime = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

    const getExerciseKey = (title: string) => {
        const mapping: { [key: string]: string } = {
            "Deep Breathing": "deep_breathing",
            "Gentle Yoga Flow": "gentle_yoga",
            "Body Scan Meditation": "body_scan",
            "Progressive Muscle Relaxation": "muscle_relax",
            "Gratitude Journaling": "gratitude",
            "Chair Yoga for Recovery": "chair_yoga",
            "Hold & Breathe Cycle": "hold_breathe",
            "Bedside Stretch & Relax": "bedside_stretch"
        };
        return mapping[title] || title.toLowerCase().replace(/ /g, "_");
    };

    const filtered = typeFilter ? exercises.filter(e => e.type === typeFilter) : exercises;

    if (activeSession) {
        const progress = activeSession.duration > 0 ? (timer / activeSession.duration) * 100 : 0;
        const exKey = getExerciseKey(activeSession.title);

        return (
            <div className="max-w-4xl mx-auto space-y-8 animate-fade-in px-4 md:px-0">
                <div className="relative h-72 rounded-[var(--radius-zen)] overflow-hidden shadow-3xl border border-white/50">
                    <div className={`absolute inset-0 bg-gradient-to-br ${activeSession.type === 'breathing' ? 'from-teal-500 via-emerald-300 to-cyan-400' :
                        activeSession.type === 'yoga' ? 'from-rose-400 via-orange-300 to-amber-300' :
                            activeSession.type === 'meditation' ? 'from-indigo-500 via-purple-400 to-pink-400' :
                                'from-blue-500 via-sky-400 to-teal-300'
                        } animate-gradient opacity-80`} />
                    <div className="absolute inset-0 backdrop-blur-2xl" />

                    <div className="absolute inset-0">
                        <div className="w-64 h-64 rounded-full bg-white/20 blur-3xl absolute -top-10 -left-10 animate-float" />
                        <div className="w-80 h-80 rounded-full bg-white/10 blur-3xl absolute -bottom-20 -right-20 animate-float [animation-delay:2s]" />
                    </div>

                    <div className="absolute inset-0 p-10 flex flex-col justify-end bg-gradient-to-t from-black/60 via-black/20 to-transparent z-10">
                        <div className="flex items-center gap-4 mb-3">
                            <span className="text-4xl filter saturate-[0.8] brightness-125">
                                {activeSession.type === 'breathing' ? '🌬️' :
                                    activeSession.type === 'yoga' ? '🧘' :
                                        activeSession.type === 'meditation' ? '✨' :
                                            activeSession.type === 'relaxation' ? '🌙' : '🌱'}
                            </span>
                            <span className="px-4 py-1.5 rounded-full bg-white/20 backdrop-blur-md text-[10px] font-black text-white uppercase tracking-[0.3em] border border-white/30">
                                {t(`wellness.cat.${activeSession.type}`)} {t('wellness.mastery')}
                            </span>
                        </div>
                        <h2 className="text-4xl md:text-5xl font-heading font-black text-white mb-2 leading-tight drop-shadow-2xl">
                            {t(`ex.${exKey}.title`)}
                        </h2>
                        <p className="text-white/80 text-lg max-w-2xl font-medium leading-relaxed line-clamp-2 md:line-clamp-none">
                            {t(`ex.${exKey}.desc`)}
                        </p>
                    </div>
                </div>

                <div className="grid lg:grid-cols-2 gap-8">
                    <div className="glass-panel p-8 flex flex-col items-center justify-center min-h-[500px]">
                        {activeSession.type === 'breathing' && isRunning && !sessionComplete ? (
                            <BreathingAnimator timer={timer} />
                        ) : (
                            <div className="w-full text-center space-y-8">
                                <div className="text-7xl font-black font-mono tracking-tighter" style={{ color: "var(--color-primary)" }}>
                                    {formatTime(timer)}
                                </div>
                                <div className="text-xl font-bold text-gray-400">
                                    {t('wellness.session.complete_of')} {formatTime(activeSession.duration)} {t('wellness.session.complete')}
                                </div>
                                <div className="w-full h-4 bg-gray-100 rounded-full overflow-hidden shadow-inner">
                                    <div className="h-full rounded-full transition-all duration-1000 bg-gradient-to-r from-[var(--color-primary)] via-[var(--color-accent)] to-[var(--color-primary)] animate-gradient"
                                        style={{ width: `${progress}%` }} />
                                </div>
                            </div>
                        )}

                        {sessionComplete ? (
                            <div className="mt-8 space-y-6 text-center">
                                <div className="text-6xl animate-bounce">🌟</div>
                                <p className="text-2xl font-black text-green-600">{t('wellness.complete.title')}</p>
                                <button onClick={() => { setActiveSession(null); setTimer(0); setSessionComplete(false); setCurrentStep(0); }}
                                    className="px-10 py-4 rounded-2xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black text-lg shadow-xl hover:scale-105 transition-transform">
                                    {t('wellness.complete.btn')}
                                </button>
                            </div>
                        ) : (
                            <div className="mt-12 flex flex-col md:flex-row justify-center gap-4 w-full md:w-auto">
                                <button onClick={() => setIsRunning(!isRunning)}
                                    className={`px-12 py-4 rounded-2xl font-black text-white shadow-2xl transform transition-all active:scale-95 text-lg ${isRunning ? "bg-orange-500 shadow-orange-200" : "bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] shadow-teal-100"
                                        }`}>
                                    {isRunning ? `⏸ ${t('wellness.ritual.pause')}` : `▶️ ${t('wellness.ritual.start')}`}
                                </button>
                                <button onClick={() => { setActiveSession(null); setTimer(0); setIsRunning(false); setCurrentStep(0); }}
                                    className="px-8 py-4 rounded-2xl bg-gray-100 text-gray-500 font-bold hover:bg-gray-200 transition-colors">
                                    {t('wellness.ritual.end')}
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="space-y-6">
                        <div className="glass-panel p-8 h-full">
                            <h3 className="text-xl font-black mb-6 flex items-center gap-2">
                                <span className="w-8 h-8 rounded-lg bg-[var(--color-primary)]/10 flex items-center justify-center text-[var(--color-primary)]">📜</span>
                                {t('wellness.guidance')}
                            </h3>
                            <div className="space-y-4">
                                {activeSession.steps.map((step, i) => (
                                    <div key={i}
                                        className={`group p-4 rounded-2xl border transition-all duration-500 flex gap-4 ${i === currentStep ? "bg-white shadow-xl border-[var(--color-primary)] scale-105 z-10" : "border-transparent opacity-80 grayscale hover:grayscale-0 hover:opacity-100"
                                            }`}>
                                        <div className={`w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center font-black ${i === currentStep ? "bg-[var(--color-primary)] text-white shadow-lg" : "bg-gray-200 text-gray-600"}`}>
                                            {i + 1}
                                        </div>
                                        <div className="flex-1">
                                            <p className={`font-bold leading-tight ${i === currentStep ? "text-gray-900" : "text-gray-500"}`}>{step}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="rounded-[var(--radius-zen)] p-8 bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] shadow-2xl relative overflow-hidden group">
                            <div className="absolute inset-0 bg-white/10 group-hover:bg-transparent transition-colors duration-500" />
                            <h3 className="text-xl font-black text-white mb-4 relative z-10 drop-shadow-md">{t('wellness.benefits')}</h3>
                            <div className="flex flex-wrap gap-2 relative z-10">
                                {activeSession.benefits.map((b, i) => (
                                    <span key={i} className="px-4 py-2 rounded-xl bg-white/20 text-white font-bold text-sm backdrop-blur-md border border-white/30">
                                        ✨ {b}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto space-y-12 animate-fade-in px-4">
            {/* ── Hero Header ── */}
            <div className="relative text-center py-16 overflow-hidden">
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute top-0 left-1/4 w-72 h-72 rounded-full bg-teal-200/30 blur-[100px] animate-float" />
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 rounded-full bg-rose-200/30 blur-[100px] animate-float [animation-delay:3s]" />
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-purple-200/20 blur-[80px] animate-float [animation-delay:1.5s]" />
                </div>
                <div className="relative z-10 space-y-6">
                    <div className="inline-flex items-center gap-3 px-6 py-2 rounded-full bg-white/60 backdrop-blur-md border border-white/40 shadow-lg">
                        <span className="text-2xl animate-float">🧘</span>
                        <span className="text-xs font-black uppercase tracking-[0.3em] text-gray-500">Mind · Body · Spirit</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-heading font-black tracking-tight">
                        <span style={{ color: "var(--color-primary)" }}>{t('wellness.title')}</span>
                    </h1>
                    <p className="text-lg md:text-xl text-gray-500 font-medium max-w-2xl mx-auto leading-relaxed">
                        {t('wellness.subtitle')}
                    </p>
                </div>
            </div>

            {/* ── Quick Stats ── */}
            {stats && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto">
                    <div className="glass-panel p-8 flex items-center justify-between group hover:border-[var(--color-primary)]/30 transition-all duration-500 hover:-translate-y-1">
                        <div>
                            <div className="text-sm font-black text-gray-400 uppercase tracking-widest mb-1">{t('wellness.stats.consistency')}</div>
                            <div className="text-4xl font-black" style={{ color: "var(--color-primary)" }}>{stats.total_sessions}</div>
                        </div>
                        <div className="w-16 h-16 rounded-3xl bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 shadow-lg">
                            <span className="text-3xl">🌿</span>
                        </div>
                    </div>
                    <div className="glass-panel p-8 flex items-center justify-between group hover:border-[var(--color-accent)]/30 transition-all duration-500 hover:-translate-y-1">
                        <div>
                            <div className="text-sm font-black text-gray-400 uppercase tracking-widest mb-1">{t('wellness.stats.total_healing')}</div>
                            <div className="text-4xl font-black text-[var(--color-accent)]">{stats.total_minutes} <span className="text-xl lowercase">{t('wellness.min')}</span></div>
                        </div>
                        <div className="w-16 h-16 rounded-3xl bg-gradient-to-br from-rose-400 to-pink-500 flex items-center justify-center group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 shadow-lg">
                            <span className="text-3xl">✨</span>
                        </div>
                    </div>
                </div>
            )}

            {/* ── Always-visible Stats (even without login) ── */}
            {!stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                    {[
                        { icon: "🌬️", label: "Breathing", value: exercises.filter(e => e.type === "breathing").length, color: "from-teal-400 to-cyan-500" },
                        { icon: "🧘", label: "Yoga", value: exercises.filter(e => e.type === "yoga").length, color: "from-rose-400 to-orange-500" },
                        { icon: "✨", label: "Meditation", value: exercises.filter(e => e.type === "meditation").length, color: "from-indigo-400 to-purple-500" },
                        { icon: "🌱", label: "Mindfulness", value: exercises.filter(e => e.type === "mindfulness" || e.type === "relaxation").length, color: "from-emerald-400 to-teal-500" },
                    ].map((stat, i) => (
                        <div key={i} className="glass-panel p-5 group hover:border-[var(--color-primary)]/20 transition-all duration-500 hover:-translate-y-1"
                            style={{ animation: `scale-in 0.5s cubic-bezier(0.16, 1, 0.3, 1) ${i * 100}ms both` }}>
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
            )}

            {/* ── Filter Pills ── */}
            <div className="flex flex-wrap justify-center gap-3">
                {["", "breathing", "yoga", "meditation", "relaxation", "mindfulness"].map((tStr) => (
                    <button key={tStr} onClick={() => setTypeFilter(tStr)}
                        className={`px-8 py-3 rounded-2xl text-sm font-black transition-all duration-300 shadow-sm hover:shadow-md relative overflow-hidden ${typeFilter === tStr
                            ? "bg-[var(--color-primary)] text-white scale-105 shadow-[0_10px_20px_rgba(13,148,136,0.2)]"
                            : "bg-white text-gray-500 hover:text-[var(--color-primary)]"
                            }`}>
                        {typeFilter === tStr && (
                            <span className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 animate-shimmer" />
                        )}
                        <span className="relative z-10">{tStr ? t(`wellness.cat.${tStr}`) : t('wellness.all_disciplines')}</span>
                    </button>
                ))}
            </div>

            {/* ── Exercise Cards ── */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-10">
                {filtered.map((ex, index) => {
                    const exKey = getExerciseKey(ex.title);
                    return (
                        <div key={ex.id} className="group relative glass-panel overflow-hidden transition-all duration-700 hover:-translate-y-4 hover:shadow-3xl flex flex-col h-full border-transparent hover:border-[var(--color-primary)]/20"
                            style={{
                                animationDelay: `${index * 120}ms`,
                                animation: 'scale-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) both',
                            }}>
                            <div className="relative h-64 overflow-hidden bg-white">
                                <div className="absolute inset-0 opacity-40 group-hover:opacity-60 transition-opacity duration-1000">
                                    <div className={`absolute inset-0 bg-gradient-to-tr ${ex.type === 'breathing' ? 'from-teal-400 via-emerald-200 to-cyan-300' :
                                        ex.type === 'yoga' ? 'from-rose-300 via-orange-200 to-amber-200' :
                                            ex.type === 'meditation' ? 'from-indigo-400 via-purple-300 to-pink-300' :
                                                'from-blue-400 via-sky-300 to-teal-200'
                                        } animate-gradient`} />
                                    <div className="absolute inset-0 backdrop-blur-3xl" />
                                </div>

                                <div className="absolute inset-0 flex items-center justify-center overflow-hidden pointer-events-none">
                                    <div className="w-32 h-32 rounded-full bg-white/30 backdrop-blur-md border border-white/40 absolute -top-8 -left-8 animate-float group-hover:scale-125 transition-transform duration-700" />
                                    <div className="w-48 h-48 rounded-full bg-white/20 backdrop-blur-lg border border-white/30 absolute -bottom-12 -right-12 animate-float [animation-delay:1s] group-hover:scale-110 transition-transform duration-700" />
                                    <div className="w-16 h-16 rounded-3xl bg-white/40 backdrop-blur-xl border border-white/50 rotate-12 absolute top-12 right-12 animate-float [animation-delay:2s]" />
                                </div>

                                <div className="absolute top-4 right-4 z-20">
                                    <div className="bg-white/90 backdrop-blur-md px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-[0.2em] text-gray-700 shadow-xl border border-white/50">
                                        {t(`wellness.cat.${ex.type}`)}
                                    </div>
                                </div>

                                <div className="absolute inset-0 flex items-center justify-center z-10 transition-transform duration-700 group-hover:scale-110">
                                    <span className="text-7xl drop-shadow-2xl filter saturate-[0.8] brightness-110">
                                        {ex.type === 'breathing' ? '🌬️' :
                                            ex.type === 'yoga' ? '🧘' :
                                                ex.type === 'meditation' ? '✨' :
                                                    ex.type === 'relaxation' ? '🌙' : '🌱'}
                                    </span>
                                </div>

                                <div className="absolute inset-0 bg-gradient-to-t from-white via-white/20 to-transparent z-20" />
                            </div>

                            <div className="p-8 flex-1 flex flex-col pt-0 relative z-30">
                                <div className="bg-white/80 backdrop-blur-md rounded-2xl p-7 -mt-10 shadow-2xl border border-white/50 flex-1 flex flex-col group-hover:bg-white transition-colors duration-500">
                                    <h3 className="text-2xl font-heading font-black text-gray-900 group-hover:text-[var(--color-primary)] transition-colors mb-3">
                                        {t(`ex.${exKey}.title`)}
                                    </h3>
                                    <div className="flex items-center gap-3 mb-5">
                                        <span className="text-[10px] font-black px-3 py-1 bg-gray-50 text-gray-500 rounded-lg border border-gray-100 uppercase tracking-wider">{t(`wellness.difficulty.${ex.difficulty.toLowerCase()}`)}</span>
                                        <span className="text-[10px] font-black px-3 py-1 bg-teal-50 text-[var(--color-primary)] rounded-lg border border-teal-100 uppercase tracking-wider">{Math.floor(ex.duration / 60)} {t('wellness.min')}</span>
                                    </div>
                                    <p className="text-gray-500 leading-relaxed line-clamp-3 font-medium text-sm mb-6">
                                        {t(`ex.${exKey}.desc`)}
                                    </p>
                                </div>

                                <div className="mt-auto pt-6 border-t border-gray-50 flex items-center justify-between">
                                    <button onClick={() => { setActiveSession(ex); setTimer(0); setIsRunning(false); setSessionComplete(false); }}
                                        className="w-full py-5 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-hover)] text-white font-black text-sm tracking-wider shadow-lg hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] transition-all relative overflow-hidden group/btn">
                                        <span className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 -translate-x-full group-hover/btn:translate-x-full transition-transform duration-700" />
                                        <span className="relative z-10 flex items-center justify-center gap-2">
                                            {t('wellness.start_ritual')}
                                            <span className="text-lg group-hover/btn:translate-x-1 transition-transform">→</span>
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
