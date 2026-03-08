import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { fetchHistory, type AnalysisResult } from "../services/historyApi";

export default function History() {
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([]);
  const [filteredAnalyses, setFilteredAnalyses] = useState<AnalysisResult[]>([]);
  const [filter, setFilter] = useState<'all' | 'bone' | 'lung' | 'blood' | 'brain' | 'skin' | 'breast'>('all');
  const [sortBy, setSortBy] = useState<'date' | 'confidence' | 'organ'>('date');
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadHistory = async () => {
      setIsLoading(true);
      try {
        const { history } = await fetchHistory(200, 0);
        setAnalyses(history);
        setFilteredAnalyses(history);
      } catch (error) {
        console.error('Failed to load history:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadHistory();
  }, []);

  useEffect(() => {
    let filtered = analyses;
    if (filter !== 'all') {
      filtered = filtered.filter(item => item.organ === filter);
    }
    filtered = [...filtered].sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
        case 'confidence':
          return (b.confidence_pct ?? 0) - (a.confidence_pct ?? 0);
        case 'organ':
          return (a.organ || '').localeCompare(b.organ || '');
        default:
          return 0;
      }
    });
    setFilteredAnalyses(filtered);
  }, [analyses, filter, sortBy]);

  const getOrganIcon = (organ: string) => {
    switch (organ?.toLowerCase()) {
      case 'bone': return '🦴';
      case 'lung': return '🫁';
      case 'brain': return '🧠';
      case 'blood': return '🩸';
      case 'skin': return '🧴';
      case 'breast': return '🎀';
      default: return '🔬';
    }
  };

  const getDiagnosisColor = (diagnosis: string) => {
    if (diagnosis.toLowerCase().includes('normal') || diagnosis.toLowerCase().includes('benign')) {
      return 'text-green-600';
    }
    return 'text-red-600';
  };

  const getDiagnosisBadge = (diagnosis: string) => {
    const isNormal = diagnosis.toLowerCase().includes('normal') || diagnosis.toLowerCase().includes('benign');
    return isNormal
      ? 'bg-green-50 text-green-700 border-green-200'
      : 'bg-red-50 text-red-700 border-red-200';
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'text-green-600';
    if (confidence >= 70) return 'text-amber-500';
    return 'text-red-500';
  };

  const getConfidenceBarColor = (confidence: number) => {
    if (confidence >= 90) return 'bg-gradient-to-r from-green-400 to-emerald-500';
    if (confidence >= 70) return 'bg-gradient-to-r from-amber-400 to-orange-500';
    return 'bg-gradient-to-r from-red-400 to-rose-500';
  };

  const clearHistory = () => {
    if (confirm('Are you sure you want to clear all analysis history?')) {
      localStorage.removeItem('analysisHistory');
      setAnalyses([]);
      setFilteredAnalyses([]);
    }
  };

  const exportHistory = () => {
    const dataStr = JSON.stringify(analyses, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = `cancer-analysis-history-${new Date().toISOString().split('T')[0]}.json`;
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="glass-panel p-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-2xl text-white shadow-lg shadow-indigo-200/50">
              📋
            </div>
            <div>
              <h1 className="text-3xl font-heading font-black text-gray-900">
                Analysis History
              </h1>
              <p className="text-gray-500 font-medium">
                {filteredAnalyses.length} {filteredAnalyses.length === 1 ? 'analysis' : 'analyses'} found
              </p>
            </div>
          </div>
          <div className="flex gap-3">
            <button
              onClick={exportHistory}
              disabled={analyses.length === 0}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-bold shadow-lg shadow-teal-200/30 hover:shadow-xl hover:-translate-y-0.5 transition-all disabled:opacity-40 disabled:hover:translate-y-0 text-sm"
            >
              💾 Export
            </button>
            <button
              onClick={clearHistory}
              disabled={analyses.length === 0}
              className="px-5 py-2.5 rounded-xl bg-red-50 text-red-600 font-bold hover:bg-red-100 transition-all disabled:opacity-40 border border-red-200/50 text-sm"
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-panel p-6">
        <div className="grid md:grid-cols-3 gap-4 items-end">
          <div>
            <label className="block text-xs font-bold mb-2 uppercase tracking-widest text-gray-400">
              Filter by Organ
            </label>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="w-full p-3 rounded-xl border border-gray-200 bg-white/50 font-medium focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/10 outline-none transition-all"
            >
              <option value="all">All Organs</option>
              <option value="bone">🦴 Bone</option>
              <option value="lung">🫁 Lung</option>
              <option value="brain">🧠 Brain</option>
              <option value="blood">🩸 Blood</option>
              <option value="skin">🧴 Skin</option>
              <option value="breast">🎀 Breast</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold mb-2 uppercase tracking-widest text-gray-400">
              Sort By
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full p-3 rounded-xl border border-gray-200 bg-white/50 font-medium focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/10 outline-none transition-all"
            >
              <option value="date">Date (Newest First)</option>
              <option value="confidence">Confidence (High to Low)</option>
              <option value="organ">Organ (A-Z)</option>
            </select>
          </div>

          <div className="glass-panel p-4 bg-gray-50/50">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">Stats</span>
              <div className="flex gap-4">
                <span className="text-sm font-bold text-gray-600">Total: <span className="text-gray-900">{analyses.length}</span></span>
                <span className="text-sm font-bold text-gray-600">Showing: <span className="text-[var(--color-primary)]">{filteredAnalyses.length}</span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="glass-panel p-12 text-center">
          <div className="w-12 h-12 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 font-bold">Loading analysis history...</p>
        </div>
      )}

      {/* Analyses List — Card-style on mobile, table-style on desktop */}
      {!isLoading && filteredAnalyses.length > 0 && (
        <div className="glass-panel overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b border-gray-200/60">
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Organ</th>
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Diagnosis</th>
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Confidence</th>
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Model</th>
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Date</th>
                  <th className="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100/60">
                {filteredAnalyses.map((analysis) => (
                  <tr key={analysis.id} className="hover:bg-white/60 transition-colors group">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="text-xl group-hover:scale-125 transition-transform">{getOrganIcon(analysis.organ)}</span>
                        <span className="font-bold text-gray-700 capitalize">{analysis.organ}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-block px-3 py-1 rounded-lg text-xs font-black border ${getDiagnosisBadge(analysis.diagnosis)}`}>
                        {analysis.diagnosis}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div className="w-20 bg-gray-100 rounded-full h-2 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${getConfidenceBarColor(analysis.confidence_pct ?? 0)}`}
                            style={{ width: `${analysis.confidence_pct ?? 0}%` }}
                          />
                        </div>
                        <span className={`text-sm font-black ${getConfidenceColor(analysis.confidence_pct ?? 0)}`}>
                          {analysis.confidence_pct ?? 0}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm">
                        <div className="font-bold text-gray-700">{analysis.method}</div>
                        <div className="text-gray-400 text-xs">{analysis.model_type}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-600">
                        {new Date(analysis.timestamp).toLocaleDateString()}
                      </div>
                      <div className="text-xs text-gray-400">
                        {new Date(analysis.timestamp).toLocaleTimeString()}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => navigate(`/results/${analysis.id}`)}
                        className="px-4 py-2 rounded-lg bg-[var(--color-primary)]/10 text-[var(--color-primary)] font-bold text-sm hover:bg-[var(--color-primary)] hover:text-white transition-all"
                      >
                        View →
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && filteredAnalyses.length === 0 && (
        <div className="glass-panel p-12 text-center">
          <div className="text-6xl mb-6 animate-float">📋</div>
          <h3 className="text-2xl font-heading font-black text-gray-900 mb-2">
            {analyses.length === 0 ? 'No Analysis History' : 'No Analyses Found'}
          </h3>
          <p className="text-gray-500 font-medium mb-8 max-w-md mx-auto">
            {analyses.length === 0
              ? 'Start by uploading your first medical image for analysis. Your results will appear here.'
              : 'Try adjusting your filters to see more analyses.'
            }
          </p>
          {analyses.length === 0 && (
            <button
              onClick={() => navigate('/upload')}
              className="px-8 py-4 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white rounded-2xl font-black text-lg shadow-xl shadow-teal-200/30 hover:shadow-2xl hover:-translate-y-1 transition-all"
            >
              🔬 Upload First Image
            </button>
          )}
        </div>
      )}
    </div>
  );
}
