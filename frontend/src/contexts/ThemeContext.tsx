import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode, FC } from 'react';
import { useAuth } from './AuthContext';

type Theme = 'coral' | 'teal' | 'dark';

interface ThemeContextType {
    theme: Theme;
    setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: FC<{ children: ReactNode }> = ({ children }) => {
    const { user } = useAuth();
    const [theme, setThemeState] = useState<Theme>(() => {
        const saved = localStorage.getItem('app-theme');
        return (saved as Theme) || 'teal';
    });

    useEffect(() => {
        const root = window.document.documentElement;
        root.classList.remove('theme-coral', 'theme-teal', 'theme-dark');
        root.classList.add(`theme-${theme}`);
        localStorage.setItem('app-theme', theme);

        // Apply Font Scaling based on age
        const age = user?.age;
        let fontScale = 1.0;

        if (age) {
            if (age < 12) {
                fontScale = 1.25; // Large for small kids
            } else if (age < 25) {
                fontScale = 1.15; // Slightly larger for youngsters
            }
        }

        root.style.setProperty('--font-scale', fontScale.toString());
        root.style.fontSize = `${16 * fontScale}px`;
    }, [theme, user]);

    const setTheme = (newTheme: Theme) => {
        setThemeState(newTheme);
    };

    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};
