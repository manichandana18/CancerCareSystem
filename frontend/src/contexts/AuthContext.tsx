import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface User {
    user_id: string;
    email: string;
    name: string;
    phone?: string;
    created_at: string;
    last_login?: string;
    security_level: string;
    is_active: boolean;
    age?: number;
    gender?: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    sessionToken: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (name: string, email: string, phone: string, password: string, age: number, gender: string) => Promise<any>;
    verifyOtp: (email: string, otp: string) => Promise<void>;
    logout: () => Promise<void>;
    verifySession: () => Promise<void>;
    registrationOtp: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [sessionToken, setSessionToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [registrationOtp, setRegistrationOtp] = useState<string | null>(null);

    const isAuthenticated = !!user && !!sessionToken;

    // Verify session on mount
    useEffect(() => {
        const storedToken = localStorage.getItem('sessionToken');
        if (storedToken) {
            setSessionToken(storedToken);
            verifyStoredSession(storedToken);
        } else {
            setIsLoading(false);
        }
    }, []);

    const verifyStoredSession = async (token: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success && data.user_info) {
                    setUser(data.user_info);
                    setSessionToken(token);
                } else {
                    // Invalid session, clear storage
                    localStorage.removeItem('sessionToken');
                    setSessionToken(null);
                    setUser(null);
                }
            } else {
                // Session expired or invalid
                localStorage.removeItem('sessionToken');
                setSessionToken(null);
                setUser(null);
            }
        } catch (error) {
            console.error('Session verification error:', error);
            localStorage.removeItem('sessionToken');
            setSessionToken(null);
            setUser(null);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (email: string, password: string) => {
        setIsLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Login failed');
            }

            if (data.success && data.session_token && data.user_info) {
                setUser(data.user_info);
                setSessionToken(data.session_token);
                localStorage.setItem('sessionToken', data.session_token);
            } else {
                throw new Error('Invalid response from server');
            }
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const register = async (name: string, email: string, phone: string, password: string, age: number, gender: string) => {
        setIsLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, phone, password, age, gender }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Registration failed');
            }

            if (data.otp) {
                setRegistrationOtp(data.otp);
            }

            return data;
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const verifyOtp = async (email: string, otp: string) => {
        setIsLoading(true);
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/verify-otp`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, otp }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'OTP verification failed');
            }

            return data;
        } catch (error) {
            console.error('OTP verification error:', error);
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        setIsLoading(true);
        try {
            if (sessionToken) {
                await fetch(`${API_BASE_URL}/api/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ session_token: sessionToken }),
                });
            }
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            setUser(null);
            setSessionToken(null);
            localStorage.removeItem('sessionToken');
            setIsLoading(false);
        }
    };

    const verifySession = async () => {
        if (!sessionToken) return;
        await verifyStoredSession(sessionToken);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated,
                isLoading,
                sessionToken,
                login,
                register,
                verifyOtp,
                logout,
                verifySession,
                registrationOtp,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
