import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useToast } from "../components/Toast";

interface Medicine {
    id: number;
    name: string;
    dosage: string;
    reminder_time: string;
    days: string[];
    photo_base64?: string;
    notes?: string;
    is_active: boolean;
    caretaker_name?: string;
    category?: string;
    medications?: { name: string; dosage: string }[];
}

interface Stats {
    total_platform_users: number;
    user_medicine_count: number;
    active_reminders: number;
}

const API = import.meta.env.VITE_API_URL || "";

export default function MedicineReminders() {
    const { user, sessionToken } = useAuth();
    const { showToast } = useToast();

    const [medicines, setMedicines] = useState<Medicine[]>([]);
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);

    // Form state
    const [newName, setNewName] = useState("");
    const [newDosage, setNewDosage] = useState("");
    const [newTime, setNewTime] = useState("");
    const [newNotes, setNewNotes] = useState("");
    const [newPhoto, setNewPhoto] = useState<string | null>(null);
    const [caretakerName, setCaretakerName] = useState("");
    const [category, setCategory] = useState("medicine");
    const [addedMedications, setAddedMedications] = useState<{ name: string; dosage: string }[]>([]);

    const [activeReminder, setActiveReminder] = useState<Medicine | null>(null);
    const [reminderQueue, setReminderQueue] = useState<Medicine[]>([]);
    const [lastNotifiedTime, setLastNotifiedTime] = useState<string>("");
    const [isTriggering, setIsTriggering] = useState(false);

    useEffect(() => {
        fetchMedicines();
        fetchStats();

        // Request notification permission
        if ("Notification" in window && Notification.permission === "default") {
            Notification.requestPermission();
        }

        // Checking for reminders every 30 seconds for better accuracy
        const interval = setInterval(checkReminders, 30000);
        checkReminders(); // Initial check

        return () => clearInterval(interval);
    }, [medicines]); // Dependency on medicines to ensure checkReminders uses latest data

    // Watcher to pull from queue when active is empty
    useEffect(() => {
        if (!activeReminder && reminderQueue.length > 0 && !isTriggering) {
            setIsTriggering(true);
            const nextMed = reminderQueue[0];
            setReminderQueue(prev => prev.slice(1));

            // Short delay to ensure state transitions smoothly
            setTimeout(() => {
                triggerReminder(nextMed);
                setIsTriggering(false);
            }, 100);
        }
    }, [activeReminder, reminderQueue, isTriggering]);

    const fetchMedicines = async () => {
        try {
            const res = await fetch(`${API}/api/medicines`, {
                headers: { Authorization: `Bearer ${sessionToken}` }
            });
            const data = await res.json();
            if (data.success) setMedicines(data.medicines);
        } catch (err) {
            console.error("Failed to fetch medicines", err);
        } finally {
            setLoading(false);
        }
    };

    const fetchStats = async () => {
        try {
            const res = await fetch(`${API}/api/medicines/stats`, {
                headers: { Authorization: `Bearer ${sessionToken}` }
            });
            const data = await res.json();
            if (data.success) setStats(data.stats);
        } catch (err) {
            console.error("Failed to fetch stats", err);
        }
    };

    const handlePhotoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setNewPhoto(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleAddMedicationToList = () => {
        if (!newName || !newDosage) {
            showToast("Please enter name and dosage", "warning");
            return;
        }
        setAddedMedications([...addedMedications, { name: newName, dosage: newDosage }]);
        setNewName("");
        setNewDosage("");
    };

    const removeMedicationFromList = (index: number) => {
        setAddedMedications(addedMedications.filter((_, i) => i !== index));
    };

    const handleAddMedicine = async (e: React.FormEvent) => {
        e.preventDefault();

        let finalMeds = [...addedMedications];
        if (newName && newDosage && finalMeds.length === 0) {
            finalMeds.push({ name: newName, dosage: newDosage });
        }

        if (finalMeds.length === 0 && category === "medicine") {
            showToast("Please add at least one medicine", "warning");
            return;
        }

        try {
            const res = await fetch(`${API}/api/medicines`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${sessionToken}`
                },
                body: JSON.stringify({
                    name: finalMeds.length > 0 ? finalMeds.map(m => m.name).join(", ") : newName || category,
                    dosage: finalMeds.length > 0 ? finalMeds.map(m => m.dosage).join(", ") : newDosage,
                    category: category,
                    medications: finalMeds,
                    reminder_time: newTime,
                    photo_base64: newPhoto,
                    notes: newNotes,
                    caretaker_name: caretakerName
                })
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, "success");
                setNewName("");
                setNewDosage("");
                setNewTime("");
                setNewNotes("");
                setNewPhoto(null);
                setAddedMedications([]);
                setCategory("medicine");
                fetchMedicines();
                fetchStats();
            }
        } catch (err) {
            showToast("Failed to add reminder", "error");
        }
    };

    const toggleMedicine = async (id: number, currentStatus: boolean) => {
        try {
            await fetch(`${API}/api/medicines/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${sessionToken}`
                },
                body: JSON.stringify({ is_active: !currentStatus })
            });
            fetchMedicines();
            fetchStats();
        } catch (err) {
            showToast("Failed to update status", "error");
        }
    };

    const deleteMedicine = async (id: number) => {
        if (!confirm("Are you sure?")) return;
        try {
            await fetch(`${API}/api/medicines/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${sessionToken}` }
            });
            fetchMedicines();
            fetchStats();
            showToast("Medicine deleted", "success");
        } catch (err) {
            showToast("Failed to delete", "error");
        }
    };

    const checkReminders = () => {
        const now = new Date();
        const currentTime = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

        // Don't re-trigger multiple times for the same minute
        if (currentTime === lastNotifiedTime) return;

        const dueNow = medicines.filter(med =>
            med.is_active && med.reminder_time === currentTime
        );

        if (dueNow.length > 0) {
            setLastNotifiedTime(currentTime);
            setReminderQueue(prev => [...prev, ...dueNow]);
        }
    };

    const triggerReminder = (med: Medicine) => {
        setActiveReminder(med);

        // 1. Browser Notification
        if (Notification.permission === "granted") {
            new Notification(`Medicine Time: ${med.name} 💊`, {
                body: `It's time for ${med.dosage}.`,
                icon: "/vite.svg"
            });
        }

        // 2. Alarm Buzzer
        playAlarm();

        // 3. AI Voice Call (Mimic)
        speakReminder(med);
    };

    const handleTestAlert = () => {
        // Test multiple inputs sequentially to verify sequence logic
        const testMeds: Medicine[] = [
            {
                id: Date.now(),
                name: "Multi-Pill Group",
                dosage: "Combined Demo",
                reminder_time: "NOW",
                days: [],
                is_active: true,
                caretaker_name: "Assistant",
                category: "medicine",
                medications: [
                    { name: "Pill A", dosage: "500mg" },
                    { name: "Pill B", dosage: "250mg" }
                ]
            },
            {
                id: Date.now() + 1,
                name: "Evening Stretching",
                dosage: "15 Minutes",
                reminder_time: "NOW",
                days: [],
                is_active: true,
                caretaker_name: "Assistant",
                category: "exercise"
            }
        ];

        setReminderQueue(prev => [...prev, ...testMeds]);
    };

    const [alarmOscillator, setAlarmOscillator] = useState<OscillatorNode | null>(null);
    const [audioCtxState, setAudioCtxState] = useState<AudioContext | null>(null);

    const playAlarm = () => {
        try {
            const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.type = 'sine';
            // Pulsing alarm frequency
            oscillator.frequency.setValueAtTime(440, audioCtx.currentTime);

            gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
            // Create a pulsing beep effect for 60 seconds
            for (let i = 0; i < 60; i += 1.5) {
                gainNode.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + i);
                gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + i + 0.5);
            }

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.start();

            setAlarmOscillator(oscillator);
            setAudioCtxState(audioCtx);
        } catch (err) {
            console.error("Audio failed", err);
        }
    };

    const stopAlarm = () => {
        if (alarmOscillator) {
            try {
                alarmOscillator.stop();
                alarmOscillator.disconnect();
            } catch (e) { }
            setAlarmOscillator(null);
        }
        if (audioCtxState) {
            try {
                audioCtxState.close();
            } catch (e) { }
            setAudioCtxState(null);
        }
    };

    const speakReminder = (med: Medicine) => {
        if ("speechSynthesis" in window) {
            const msg = new SpeechSynthesisUtterance();
            const voiceName = med.caretaker_name || "your caretaker";

            let text = `Hi ${user?.name || 'there'}, this is a reminder from ${voiceName}. `;

            if (med.category === "exercise") {
                text += `It is time for your exercise: ${med.name}. Stay active!`;
            } else if (med.category === "vitals") {
                text += `It is time to check your vitals: ${med.name}.`;
            } else if (med.category === "water") {
                text += `Time for a glass of water. Stay hydrated!`;
            } else {
                const medNames = med.medications && med.medications.length > 0
                    ? med.medications.map(m => m.name).join(" and ")
                    : med.name;
                text += `It is time to take your medicine: ${medNames}. ${med.dosage}. Don't forget!`;
            }

            msg.text = text;
            msg.rate = 0.9;
            msg.pitch = 1.1;
            window.speechSynthesis.speak(msg);
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-6 pb-20">
            {/* Header & Stats */}
            <div className="glass-panel p-8">
                <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-red-400 to-rose-500 flex items-center justify-center text-3xl shadow-lg shadow-rose-200/50 text-white">
                            💊
                        </div>
                        <div>
                            <h1 className="text-3xl font-heading font-black text-gray-900">Medicine Reminders</h1>
                            <p className="text-gray-500 font-medium">Never miss a dose with AI voice & photo reminders</p>
                        </div>
                    </div>

                    <div className="flex gap-4">
                        <div className="glass-panel px-6 py-4 bg-primary/5 border-primary/20 text-center">
                            <p className="text-2xl font-black text-primary">{stats?.total_platform_users || "..."}</p>
                            <p className="text-[10px] uppercase font-black text-gray-400 tracking-widest">Total Users on Platform</p>
                        </div>
                        <div className="glass-panel px-6 py-4 bg-emerald-500/5 border-emerald-200 text-center">
                            <p className="text-2xl font-black text-emerald-600">{stats?.active_reminders ?? "0"}</p>
                            <p className="text-[10px] uppercase font-black text-gray-400 tracking-widest">Active Reminders</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="grid lg:grid-cols-3 gap-6">

                {/* Left Column: List */}
                <div className="lg:col-span-2 space-y-4">
                    <div className="flex justify-between items-center mb-2">
                        <h2 className="text-xl font-heading font-black text-gray-800">Your Medications</h2>
                        <div className="flex gap-4">
                            <button
                                onClick={handleTestAlert}
                                className="px-6 py-2.5 bg-amber-500 text-white rounded-xl font-black text-sm shadow-lg shadow-amber-200 hover:-translate-y-0.5 transition-all"
                            >
                                🔔 Test Alert
                            </button>
                            <button
                                onClick={() => setShowAddForm(!showAddForm)}
                                className="px-6 py-2.5 bg-primary text-white rounded-xl font-black text-sm shadow-lg shadow-primary/30 hover:-translate-y-0.5 transition-all"
                            >
                                {showAddForm ? "✕ Close Form" : "＋ Add Medicine"}
                            </button>
                        </div>
                    </div>

                    {medicines.length === 0 && !loading && (
                        <div className="glass-panel p-12 text-center">
                            <div className="text-6xl mb-4 animate-float">😴</div>
                            <h3 className="text-xl font-black mb-2">No medications added</h3>
                            <p className="text-gray-500 mb-6">Start by adding your first medicine and setting a reminder time.</p>
                        </div>
                    )}

                    <div className="grid md:grid-cols-2 gap-4">
                        {medicines.map(med => (
                            <div key={med.id} className={`glass-panel p-5 transition-all group ${!med.is_active ? 'opacity-60 grayscale' : 'hover:border-primary/50 cursor-pointer'}`}>
                                <div className="flex gap-4">
                                    <div className="w-20 h-20 rounded-xl overflow-hidden bg-gray-100 border border-gray-200 shrink-0">
                                        {med.photo_base64 ? (
                                            <img src={med.photo_base64} alt={med.name} className="w-full h-full object-cover" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center text-3xl">💊</div>
                                        )}
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex justify-between">
                                            <div className="flex items-center gap-2">
                                                <span className="text-lg">
                                                    {med.category === "exercise" ? "🏃" :
                                                        med.category === "vitals" ? "🌡️" :
                                                            med.category === "water" ? "💧" : "💊"}
                                                </span>
                                                <h3 className="font-black text-gray-900 capitalize">{med.category}: {med.name}</h3>
                                            </div>
                                            <button onClick={() => deleteMedicine(med.id)} className="text-gray-300 hover:text-red-500 transition-colors">🗑️</button>
                                        </div>
                                        {med.medications && med.medications.length > 0 ? (
                                            <div className="mt-1 space-y-0.5">
                                                {med.medications.map((m, idx) => (
                                                    <p key={idx} className="text-[10px] font-bold text-gray-500">
                                                        • {m.name} ({m.dosage})
                                                    </p>
                                                ))}
                                            </div>
                                        ) : (
                                            <p className="text-sm font-bold text-gray-500 mb-2">{med.dosage}</p>
                                        )}
                                        <div className="flex items-center gap-2 text-primary font-black text-lg mt-2">
                                            <span className="text-xl">⏰</span> {med.reminder_time}
                                        </div>
                                    </div>
                                </div>
                                {med.notes && <p className="mt-3 text-xs text-gray-400 italic font-medium bg-gray-50 p-2 rounded-lg">"{med.notes}"</p>}

                                <div className="mt-4 pt-4 border-t border-gray-100 flex justify-between items-center">
                                    <span className="text-[10px] font-black uppercase text-gray-400 tracking-widest">
                                        Voice: {med.caretaker_name || "Standard"}
                                    </span>
                                    <button
                                        onClick={() => toggleMedicine(med.id, med.is_active)}
                                        className={`px-4 py-1.5 rounded-lg text-[10px] font-black transition-all ${med.is_active ? 'bg-emerald-100 text-emerald-600' : 'bg-gray-200 text-gray-500'}`}
                                    >
                                        {med.is_active ? "ACTIVE" : "PAUSED"}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right Column: Form */}
                <div className={`space-y-6 ${showAddForm ? 'block' : 'hidden lg:block'}`}>
                    <div className="glass-panel p-6 sticky top-24">
                        <h2 className="text-xl font-heading font-black text-gray-800 mb-6">Add New Reminder</h2>
                        <form onSubmit={handleAddMedicine} className="space-y-4">
                            <div>
                                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Category</label>
                                <div className="grid grid-cols-5 gap-2">
                                    {[
                                        { id: 'medicine', icon: '💊', label: 'Meds' },
                                        { id: 'exercise', icon: '🏃', label: 'Gym' },
                                        { id: 'vitals', icon: '🌡️', label: 'Vitals' },
                                        { id: 'water', icon: '💧', label: 'Water' },
                                        { id: 'other', icon: '🏷️', label: 'Other' }
                                    ].map(cat => (
                                        <button
                                            key={cat.id}
                                            type="button"
                                            onClick={() => setCategory(cat.id)}
                                            className={`p-2 rounded-xl border-2 transition-all text-center ${category === cat.id ? 'border-primary bg-primary/5' : 'border-gray-100 hover:border-gray-200'}`}
                                        >
                                            <div className="text-xl">{cat.icon}</div>
                                            <div className="text-[8px] font-black uppercase mt-1">{cat.label}</div>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {category === 'medicine' ? (
                                <div className="space-y-4 pt-2 border-t border-gray-100">
                                    <div className="flex gap-2">
                                        <div className="flex-1">
                                            <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Add Tablet Name</label>
                                            <input
                                                value={newName}
                                                onChange={e => setNewName(e.target.value)}
                                                className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold text-sm"
                                                placeholder="e.g. Paracetamol"
                                            />
                                        </div>
                                        <div className="w-1/3">
                                            <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Dosage</label>
                                            <input
                                                value={newDosage}
                                                onChange={e => setNewDosage(e.target.value)}
                                                className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold text-sm"
                                                placeholder="650mg"
                                            />
                                        </div>
                                        <button
                                            type="button"
                                            onClick={handleAddMedicationToList}
                                            className="mt-6 p-3 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all font-black"
                                        >+</button>
                                    </div>

                                    {addedMedications.length > 0 && (
                                        <div className="bg-gray-50 p-3 rounded-xl space-y-2">
                                            {addedMedications.map((m, idx) => (
                                                <div key={idx} className="flex justify-between items-center bg-white p-2 rounded-lg border border-gray-100 shadow-sm">
                                                    <span className="text-xs font-bold text-gray-700">{m.name} - {m.dosage}</span>
                                                    <button type="button" onClick={() => removeMedicationFromList(idx)} className="text-red-400 hover:text-red-600 text-xs">✕</button>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <div>
                                    <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">{category.charAt(0).toUpperCase() + category.slice(1)} Details</label>
                                    <input
                                        required
                                        value={newName}
                                        onChange={e => setNewName(e.target.value)}
                                        className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold"
                                        placeholder={`e.g. ${category === 'exercise' ? 'Walk for 20 mins' : category === 'vitals' ? 'Blood Pressure Check' : 'Drink 500ml'}`}
                                    />
                                </div>
                            )}

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Time</label>
                                    <input
                                        required
                                        type="time"
                                        value={newTime}
                                        onChange={e => setNewTime(e.target.value)}
                                        className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold"
                                    />
                                </div>
                                <div>
                                    <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Whose Voice?</label>
                                    <input
                                        value={caretakerName}
                                        onChange={e => setCaretakerName(e.target.value)}
                                        className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold"
                                        placeholder="e.g. Daughter"
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Medicine Photo</label>
                                <div className="relative group overflow-hidden rounded-xl border-2 border-dashed border-gray-200 hover:border-primary/50 transition-all p-2">
                                    {newPhoto ? (
                                        <div className="relative aspect-video">
                                            <img src={newPhoto} className="w-full h-full object-cover rounded-lg" />
                                            <button
                                                type="button"
                                                onClick={() => setNewPhoto(null)}
                                                className="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full shadow-lg"
                                            >✕</button>
                                        </div>
                                    ) : (
                                        <div className="py-8 text-center cursor-pointer">
                                            <p className="text-3xl mb-2">📸</p>
                                            <p className="text-[10px] font-black text-gray-400 uppercase">Upload or Take Photo</p>
                                            <input type="file" accept="image/*" onChange={handlePhotoUpload} className="absolute inset-0 opacity-0 cursor-pointer" />
                                        </div>
                                    )}
                                </div>
                            </div>

                            <div>
                                <label className="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1.5">Notes (Optional)</label>
                                <textarea
                                    value={newNotes}
                                    onChange={e => setNewNotes(e.target.value)}
                                    className="w-full p-3 rounded-xl border border-gray-200 focus:border-primary outline-none transition-all font-bold h-20 resize-none text-sm"
                                    placeholder="e.g. Take after meal"
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full py-4 bg-gradient-to-r from-primary to-primary-hover text-white rounded-2xl font-black shadow-xl shadow-primary/30 hover:-translate-y-1 transition-all"
                            >
                                Set Reminder
                            </button>
                        </form>
                    </div>
                </div>
            </div >

            {/* Trigger Modal (Active Reminder) */}
            {
                activeReminder && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm animate-fade-in">
                        <div className="glass-panel max-w-md w-full p-8 text-center bg-white shadow-[0_0_100px_rgba(13,148,136,0.3)] animate-scale-up border-4 border-primary">
                            <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center text-5xl mx-auto mb-6 animate-pulse">
                                {activeReminder.category === "exercise" ? "🏃" :
                                    activeReminder.category === "vitals" ? "🌡️" :
                                        activeReminder.category === "water" ? "💧" : "🔔"}
                            </div>
                            <h2 className="text-3xl font-heading font-black text-gray-900 mb-2">
                                {activeReminder.category === "exercise" ? "Time to Move!" :
                                    activeReminder.category === "vitals" ? "Check your Vitals" :
                                        activeReminder.category === "water" ? "Hydration Time!" : "Medicine Time!"}
                            </h2>

                            <div className="my-6 p-6 bg-gray-50 rounded-2xl border border-gray-100 flex items-center gap-6">
                                {activeReminder.photo_base64 && (
                                    <img src={activeReminder.photo_base64} className="w-20 h-20 rounded-xl object-cover shadow-md" />
                                )}
                                <div className="text-left">
                                    {activeReminder.medications && activeReminder.medications.length > 0 ? (
                                        <div className="space-y-1">
                                            <p className="text-sm font-black text-gray-400 uppercase tracking-widest leading-none mb-2">Grouped Reminders:</p>
                                            {activeReminder.medications.map((m, idx) => (
                                                <p key={idx} className="text-xl font-black text-primary leading-tight">• {m.name} ({m.dosage})</p>
                                            ))}
                                        </div>
                                    ) : (
                                        <>
                                            <p className="text-2xl font-black text-primary">{activeReminder.name}</p>
                                            <p className="font-bold text-gray-500">{activeReminder.dosage}</p>
                                        </>
                                    )}
                                </div>
                            </div>

                            <p className="text-sm font-bold text-gray-400 mb-8 italic">
                                "Hi {user?.name}, this is {activeReminder.caretaker_name || 'your caretaker'} reminding you {activeReminder.category === 'medicine' ? 'to take your medicine' : 'about this session'}."
                            </p>

                            <button
                                onClick={() => {
                                    setActiveReminder(null);
                                    window.speechSynthesis.cancel();
                                    stopAlarm();
                                }}
                                className="w-full py-4 bg-primary text-white rounded-2xl font-black text-xl shadow-2xl shadow-primary/40 hover:scale-105 active:scale-95 transition-all"
                            >
                                {activeReminder.category === 'medicine' ? "✅ I've taken it" : "Done ✅"}
                            </button>
                        </div>
                    </div>
                )
            }
        </div >
    );
}
