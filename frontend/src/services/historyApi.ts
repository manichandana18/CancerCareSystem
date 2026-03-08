/**
 * History API Service
 * Handles communication with the backend analysis history endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('sessionToken');
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

export interface AnalysisResult {
    id: string | number;
    organ: string;
    diagnosis: string;
    confidence: number;
    confidence_pct: number;
    method: string;
    model_type?: string;
    timestamp: string;
    doctor_verified?: boolean;
    explainability?: any;
    cell_count?: number;
    debug?: any;
    diagnosis_confidence?: number;
    diagnosis_confidence_pct?: number;
}

export interface HistoryStats {
    total: number;
    bone: number;
    lung: number;
    blood: number;
    brain: number;
    skin: number;
    breast: number;
    cancer: number;
    normal: number;
}

/**
 * Save an analysis result to the backend database.
 * Falls back to localStorage if user is not authenticated.
 */
export async function saveAnalysis(result: AnalysisResult): Promise<boolean> {
    // Always save to localStorage as cache
    const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    history.unshift(result);
    localStorage.setItem('analysisHistory', JSON.stringify(history));

    // Try to save to backend
    const token = localStorage.getItem('sessionToken');
    if (!token) return true; // Not authenticated — localStorage is fine

    try {
        const response = await fetch(`${API_BASE_URL}/api/history/save`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
                organ: result.organ || 'unknown',
                diagnosis: result.diagnosis || 'unknown',
                confidence: result.confidence ?? result.diagnosis_confidence ?? 0,
                confidence_pct: result.confidence_pct ?? result.diagnosis_confidence_pct ?? 0,
                method: result.method || '',
                model_type: result.model_type || '',
                explainability: result.explainability || null,
                cell_count: result.cell_count || null,
                debug: result.debug || null,
            }),
        });
        return response.ok;
    } catch (error) {
        console.warn('Failed to save to backend, using localStorage fallback:', error);
        return true; // localStorage save was successful
    }
}

/**
 * Fetch analysis history from backend.
 * Falls back to localStorage if not authenticated or backend unavailable.
 */
export async function fetchHistory(limit = 50, offset = 0): Promise<{
    history: AnalysisResult[];
    total: number;
}> {
    const token = localStorage.getItem('sessionToken');
    if (!token) {
        // Fallback to localStorage
        const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
        return { history: history.slice(offset, offset + limit), total: history.length };
    }

    try {
        const response = await fetch(
            `${API_BASE_URL}/api/history/list?limit=${limit}&offset=${offset}`,
            { headers: getAuthHeaders() }
        );
        if (response.ok) {
            const data = await response.json();
            return { history: data.history, total: data.total };
        }
    } catch (error) {
        console.warn('Failed to fetch from backend, using localStorage fallback:', error);
    }

    // Fallback
    const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    return { history: history.slice(offset, offset + limit), total: history.length };
}

/**
 * Fetch dashboard stats from backend.
 * Falls back to computing from localStorage.
 */
export async function fetchStats(): Promise<HistoryStats> {
    const token = localStorage.getItem('sessionToken');
    if (token) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/history/stats`, {
                headers: getAuthHeaders(),
            });
            if (response.ok) {
                const data = await response.json();
                return data.stats;
            }
        } catch (error) {
            console.warn('Failed to fetch stats from backend:', error);
        }
    }

    // Fallback: compute from localStorage
    const history: AnalysisResult[] = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    return {
        total: history.length,
        bone: history.filter(h => h.organ === 'bone').length,
        lung: history.filter(h => h.organ === 'lung').length,
        blood: history.filter(h => h.organ === 'blood').length,
        brain: history.filter(h => h.organ === 'brain').length,
        skin: history.filter(h => h.organ === 'skin').length,
        breast: history.filter(h => h.organ === 'breast').length,
        cancer: history.filter(h =>
            h.diagnosis?.toLowerCase().includes('cancer') ||
            h.diagnosis?.toLowerCase().includes('malignant')
        ).length,
        normal: history.filter(h =>
            h.diagnosis?.toLowerCase().includes('normal') ||
            h.diagnosis?.toLowerCase().includes('benign')
        ).length,
    };
}

/**
 * Delete a specific analysis record.
 */
export async function deleteAnalysis(recordId: number): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history/${recordId}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return response.ok;
    } catch (error) {
        console.warn('Failed to delete record:', error);
        return false;
    }
}
