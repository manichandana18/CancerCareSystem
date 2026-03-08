import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { wellnessExercises } from '../data/wellnessExercises';
import Confetti from 'react-confetti';

export default function YogaSession() {
    const { id } = useParams<{ id: string }>();
    const exercise = wellnessExercises.find(e => e.id === id);

    const [timeLeft, setTimeLeft] = useState(exercise ? exercise.duration * 60 : 0);
    const [isActive, setIsActive] = useState(false);
    const [isCompleted, setIsCompleted] = useState(false);

    useEffect(() => {
        let interval: ReturnType<typeof setInterval>;

        if (isActive && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft((prev) => prev - 1);
            }, 1000);
        } else if (timeLeft === 0 && isActive) {
            setIsActive(false);
            setIsCompleted(true);
        }

        return () => clearInterval(interval);
    }, [isActive, timeLeft]);

    if (!exercise) {
        return <div className="text-center py-20">Session not found. <Link to="/wellness" className="text-teal-600 font-bold underline">Go Back</Link></div>;
    }

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const toggleTimer = () => setIsActive(!isActive);

    return (
        <div className="max-w-6xl mx-auto px-4 py-12 animate-fade-in min-h-screen">
            {isCompleted && <Confetti recycle={false} numberOfPieces={500} colors={['#0f766e', '#f43f5e', '#fbbf24']} />}

            <Link to="/wellness" className="glass-panel px-4 py-2 rounded-full text-gray-500 hover:text-[var(--color-primary)] mb-8 inline-flex items-center transition-all hover:pl-6 shadow-sm">
                <span className="mr-2">←</span> Back to Wellness
            </Link>

            <div className="grid lg:grid-cols-2 gap-16 items-start">
                {/* Visuals */}
                <div className="rounded-[2.5rem] overflow-hidden shadow-2xl shadow-teal-200/50 sticky top-24 transform hover:rotate-1 transition-transform duration-500">
                    <img src={exercise.imageUrl} alt={exercise.title} className="w-full h-full object-cover min-h-[500px]" />
                    <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-[var(--color-primary)] to-transparent p-8 pt-20">
                        <span className="inline-block bg-white/20 backdrop-blur-md text-white text-xs font-bold px-4 py-1.5 rounded-full mb-2 uppercase tracking-widest border border-white/30">
                            {exercise.difficulty} • {exercise.type}
                        </span>
                        <h1 className="text-4xl font-heading font-bold text-white mb-2 shadow-sm">{exercise.title}</h1>
                    </div>
                </div>

                {/* Controls & Instructions */}
                <div className="space-y-10">
                    <div>
                        <p className="text-xl text-gray-600 leading-relaxed font-light">{exercise.description}</p>
                    </div>

                    <div className="glass-panel rounded-[2.5rem] p-10 shadow-xl border border-white/60 relative overflow-hidden group">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-teal-100 rounded-full blur-3xl opacity-50 -z-10 group-hover:bg-teal-200 transition-colors duration-700"></div>

                        {/* Timer Progress Bar */}
                        <div className="w-full bg-gray-100 h-3 rounded-full mb-10 overflow-hidden relative">
                            <div className={`absolute top-0 left-0 h-full bg-gradient-to-r from-[var(--color-primary)] to-teal-400 transition-all duration-1000 ease-linear shadow-[0_0_10px_rgba(15,118,110,0.5)]`} style={{ width: `${(timeLeft / (exercise.duration * 60)) * 100}%` }}></div>
                        </div>

                        <div className="text-center mb-10">
                            <div className={`text-8xl font-heading font-bold text-gray-800 mb-2 transition-all duration-300 tabular-nums tracking-tighter ${isActive ? 'scale-105 text-[var(--color-primary)]' : ''}`}>
                                {formatTime(timeLeft)}
                            </div>
                            <p className="text-gray-400 text-sm font-bold tracking-[0.2em] uppercase">Time Remaining</p>
                        </div>

                        <button
                            onClick={toggleTimer}
                            disabled={isCompleted}
                            className={`w-full py-6 rounded-2xl text-xl font-bold text-white transition-all transform active:scale-95 shadow-xl flex items-center justify-center relative overflow-hidden
                                ${isCompleted
                                    ? 'bg-green-500 cursor-default'
                                    : isActive
                                        ? 'bg-amber-400 hover:bg-amber-500 text-amber-900 shadow-amber-200/50'
                                        : 'bg-[var(--color-primary)] hover:bg-teal-800 hover:-translate-y-1 shadow-teal-700/30'
                                }
                            `}
                        >
                            {isCompleted ? (
                                <span className="flex items-center animate-bounce">🎉 Session Complete!</span>
                            ) : isActive ? (
                                <span className="flex items-center">⏸ Pause Session</span>
                            ) : (
                                <span className="flex items-center">▶ Start Session</span>
                            )}
                        </button>
                    </div>

                    <div>
                        <h3 className="text-2xl font-heading font-bold text-gray-900 mb-6 flex items-center"><span className="text-3xl mr-3">🦶</span> Steps to Follow</h3>
                        <ol className="space-y-6">
                            {exercise.steps.map((step, idx) => (
                                <li key={idx} className="flex items-start group">
                                    <span className="bg-teal-50 text-[var(--color-primary)] w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg mr-5 flex-shrink-0 group-hover:bg-[var(--color-primary)] group-hover:text-white transition-colors duration-300 shadow-sm border border-teal-100">
                                        {idx + 1}
                                    </span>
                                    <p className="text-gray-700 mt-2 text-lg leading-relaxed">{step}</p>
                                </li>
                            ))}
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    );
}
