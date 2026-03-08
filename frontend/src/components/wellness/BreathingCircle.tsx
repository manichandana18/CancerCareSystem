import { useEffect, useState } from 'react';

export default function BreathingCircle() {
    const [phase, setPhase] = useState<'Inhale' | 'Hold' | 'Exhale'>('Inhale');
    const [instruction, setInstruction] = useState('Breathe In');

    useEffect(() => {
        const cycle = async () => {
            // Inhale: 4s
            setPhase('Inhale');
            setInstruction('Breathe In... 🌸');
            await new Promise(r => setTimeout(r, 4000));

            // Hold: 4s (Box Breathing style, adapted)
            setPhase('Hold');
            setInstruction('Hold... ✋');
            await new Promise(r => setTimeout(r, 4000));

            // Exhale: 4s
            setPhase('Exhale');
            setInstruction('Breathe Out... 🌬️');
            await new Promise(r => setTimeout(r, 4000));
        };

        cycle(); // Start immediately
        const interval = setInterval(cycle, 12000); // 4+4+4 = 12s cycle

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex flex-col items-center justify-center py-12">
            <div className="relative flex items-center justify-center w-64 h-64">
                {/* Outer pulsating rings */}
                <div
                    className={`absolute rounded-full border-4 border-blue-200 transition-all duration-[4000ms] ease-in-out
            ${phase === 'Inhale' ? 'w-64 h-64 opacity-50' : phase === 'Exhale' ? 'w-32 h-32 opacity-20' : 'w-64 h-64 opacity-50'}
          `}
                />
                <div
                    className={`absolute rounded-full bg-blue-100 transition-all duration-[4000ms] ease-in-out
            ${phase === 'Inhale' ? 'w-56 h-56' : phase === 'Exhale' ? 'w-24 h-24' : 'w-56 h-56'}
          `}
                />

                {/* Core circle with text */}
                <div className="z-10 text-center">
                    <h3 className="text-2xl font-bold text-blue-800 transition-opacity duration-500">
                        {instruction}
                    </h3>
                </div>
            </div>
            <p className="mt-8 text-gray-500 text-sm">Follow the circle's rhythm to calm your mind.</p>
        </div>
    );
}
