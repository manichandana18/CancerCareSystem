import { useState, useEffect, createContext, useContext, useCallback } from 'react';
import type { ReactNode } from 'react';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
    id: number;
    message: string;
    type: ToastType;
}

interface ToastContextType {
    showToast: (message: string, type?: ToastType) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

let toastId = 0;

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<Toast[]>([]);

    const showToast = useCallback((message: string, type: ToastType = 'info') => {
        const id = ++toastId;
        setToasts(prev => [...prev, { id, message, type }]);
    }, []);

    const removeToast = useCallback((id: number) => {
        setToasts(prev => prev.filter(t => t.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            {/* Toast container */}
            <div style={{
                position: 'fixed',
                top: '1.25rem',
                right: '1.25rem',
                zIndex: 9999,
                display: 'flex',
                flexDirection: 'column',
                gap: '0.5rem',
                maxWidth: '400px',
            }}>
                {toasts.map(toast => (
                    <ToastItem key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
                ))}
            </div>
        </ToastContext.Provider>
    );
}

export function useToast() {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error('useToast must be used within a ToastProvider');
    }
    return context;
}

// --- Toast Item Component ---
const TOAST_STYLES: Record<ToastType, { bg: string; border: string; icon: string }> = {
    success: { bg: 'rgba(16, 185, 129, 0.12)', border: '#10b981', icon: '✅' },
    error: { bg: 'rgba(239, 68, 68, 0.12)', border: '#ef4444', icon: '❌' },
    warning: { bg: 'rgba(245, 158, 11, 0.12)', border: '#f59e0b', icon: '⚠️' },
    info: { bg: 'rgba(59, 130, 246, 0.12)', border: '#3b82f6', icon: 'ℹ️' },
};

function ToastItem({ toast, onClose }: { toast: Toast; onClose: () => void }) {
    const [isExiting, setIsExiting] = useState(false);
    const style = TOAST_STYLES[toast.type];

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsExiting(true);
            setTimeout(onClose, 300); // Wait for exit animation
        }, 4000);
        return () => clearTimeout(timer);
    }, [onClose]);

    return (
        <div
            role="alert"
            style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.875rem 1rem',
                borderRadius: '0.75rem',
                backgroundColor: style.bg,
                borderLeft: `4px solid ${style.border}`,
                backdropFilter: 'blur(12px)',
                boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
                animation: isExiting
                    ? 'toast-exit 0.3s ease-in forwards'
                    : 'toast-enter 0.3s ease-out',
                cursor: 'pointer',
            }}
            onClick={onClose}
        >
            <span style={{ fontSize: '1.25rem', flexShrink: 0 }}>{style.icon}</span>
            <p style={{
                margin: 0,
                fontSize: '0.875rem',
                fontWeight: 500,
                color: 'var(--text-primary, #1f2937)',
                lineHeight: 1.4,
            }}>
                {toast.message}
            </p>
            <button
                onClick={(e) => { e.stopPropagation(); onClose(); }}
                style={{
                    marginLeft: 'auto',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '1rem',
                    opacity: 0.5,
                    color: 'var(--text-primary, #1f2937)',
                    padding: '0.25rem',
                    lineHeight: 1,
                }}
                aria-label="Close notification"
            >
                ✕
            </button>
            <style>{`
        @keyframes toast-enter {
          from { opacity: 0; transform: translateX(100%); }
          to { opacity: 1; transform: translateX(0); }
        }
        @keyframes toast-exit {
          from { opacity: 1; transform: translateX(0); }
          to { opacity: 0; transform: translateX(100%); }
        }
      `}</style>
        </div>
    );
}
