import { Link } from 'react-router-dom';

interface ExerciseCardProps {
    id: string;
    title: string;
    duration: number; // in minutes
    difficulty: 'Gentle' | 'Moderate' | 'Advanced';
    type: 'Yoga' | 'Meditation' | 'Pranayama';
    imageUrl: string;
}

export default function ExerciseCard({ id, title, duration, difficulty, type, imageUrl }: ExerciseCardProps) {
    return (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 transform hover:-translate-y-1">
            <div className="h-48 overflow-hidden relative">
                <img
                    src={imageUrl}
                    alt={title}
                    className="w-full h-full object-cover"
                />
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold shadow-sm">
                    {difficulty}
                </div>
            </div>
            <div className="p-6">
                <div className="text-xs font-semibold text-blue-600 uppercase tracking-wide mb-2">
                    {type} • {duration} Min
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
                <Link
                    to={`/wellness/session/${id}`}
                    className="block w-full text-center bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                    Start Session ▶
                </Link>
            </div>
        </div>
    );
}
