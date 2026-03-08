export interface WellnessExercise {
    id: string;
    title: string;
    description: string;
    duration: number; // minutes
    difficulty: 'Gentle' | 'Moderate' | 'Advanced'; // Strict safety categories
    type: 'Yoga' | 'Meditation' | 'Pranayama';
    imageUrl: string;
    steps: string[];
}

export const wellnessExercises: WellnessExercise[] = [
    {
        id: 'pranayama-basic',
        title: 'Calming Box Breathing',
        description: 'A simple breathing technique to reduce stress and anxiety. Safe for all patients.',
        duration: 5,
        difficulty: 'Gentle',
        type: 'Pranayama',
        imageUrl: 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&q=80&w=800',
        steps: [
            "Sit comfortably with your back straight.",
            "Inhale slowly through your nose for 4 seconds.",
            "Hold your breath for 4 seconds.",
            "Exhale slowly through your mouth for 4 seconds.",
            "Repeat for the duration of the session."
        ]
    },
    {
        id: 'chair-yoga-1',
        title: 'Seated Spinal Twist',
        description: 'Gentle movement to improve circulation without standing. Ideal for limited mobility.',
        duration: 10,
        difficulty: 'Gentle',
        type: 'Yoga',
        imageUrl: 'https://images.unsplash.com/photo-1544367563-12123d8965cd?auto=format&fit=crop&q=80&w=800',
        steps: [
            "Sit tall in a sturdy chair, feet flat on the floor.",
            "Place your right hand on the back of the chair.",
            "Place your left hand on your right thigh.",
            "Gently twist your torso to the right on an exhale.",
            "Hold for 5 breaths, then switch sides."
        ]
    },
    {
        id: 'bed-yoga-2',
        title: 'Bedside Stretch & Relax',
        description: 'Simple stretches you can do lying down to release tension.',
        duration: 8,
        difficulty: 'Gentle',
        type: 'Yoga',
        imageUrl: 'https://images.unsplash.com/photo-1512438248247-f0f2a5a8b7f0?auto=format&fit=crop&q=80&w=800',
        steps: [
            "Lie on your back, legs extended.",
            "Bring one knee to your chest, holding it gently.",
            "Rotate your ankle slowly in both directions.",
            "Switch legs and repeat.",
            "Finish by stretching arms overhead."
        ]
    },
    {
        id: 'meditation-healing',
        title: 'Healing Light Visualization',
        description: 'Guided visualization to promote mental peace and hope.',
        duration: 15,
        difficulty: 'Gentle',
        type: 'Meditation',
        imageUrl: 'https://images.unsplash.com/photo-1528319725582-ddc096101511?auto=format&fit=crop&q=80&w=800',
        steps: [
            "Close your eyes and breathe naturally.",
            "Visualize a warm, golden light surrounding your body.",
            "Imagine the light healing and soothing every cell.",
            "Stay with this feeling of warmth and safety."
        ]
    }
];
