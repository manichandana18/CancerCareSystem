import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { fetchStats, fetchHistory, type AnalysisResult, type HistoryStats } from "../services/historyApi";

export default function Dashboard() {
  const [recentAnalyses, setRecentAnalyses] = useState<AnalysisResult[]>([]);
  const [stats, setStats] = useState<HistoryStats>({
    total: 0,
    bone: 0,
    lung: 0,
    blood: 0,
    brain: 0,
    skin: 0,
    breast: 0,
    cancer: 0,
    normal: 0
  });
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch stats and recent history from backend (with localStorage fallback)
    const loadData = async () => {
      try {
        const [statsData, historyData] = await Promise.all([
          fetchStats(),
          fetchHistory(5, 0),
        ]);
        setStats(statsData);
        setRecentAnalyses(historyData.history);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      }
    };
    loadData();
  }, []);

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

  return (
    <div className="relative min-h-screen p-8 mesh-bg">
      <div className="max-w-7xl mx-auto space-y-8 animate-fade-in">
        {/* Header */}
        <div className="glass-panel p-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl -z-10 animate-float"></div>
          <h1 className="text-5xl font-heading font-black text-gray-900 mb-2 leading-tight">
            Care <span className="text-primary">Dashboard</span>
          </h1>
          <p className="text-gray-500 font-medium">
            Advanced AI-powered cancer detection system • <span className="text-primary-hover font-bold">Secure Patient Records</span>
          </p>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 xl:grid-cols-8 gap-6">
          <div className="glass-panel p-6 text-center border-t-4 border-primary bg-white/60">
            <div className="text-4xl font-black text-primary mb-1">{stats.total}</div>
            <div className="text-[10px] uppercase tracking-[0.2em] font-black text-gray-400">Total Scans</div>
          </div>

          {[
            { label: "Bone", val: stats.bone, icon: "🦴" },
            { label: "Lung", val: stats.lung, icon: "🫁" },
            { label: "Brain", val: stats.brain, icon: "🧠" },
            { label: "Blood", val: stats.blood, icon: "🩸" },
            { label: "Skin", val: stats.skin, icon: "🧴" },
            { label: "Breast", val: stats.breast, icon: "🎀" },
          ].map((stat, i) => (
            <div key={i} className="glass-panel p-6 text-center group hover:bg-white/80 transition-all duration-300">
              <div className="text-3xl mb-2 group-hover:scale-125 transition-transform duration-500">{stat.icon}</div>
              <div className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{stat.label}</div>
            </div>
          ))}

          <div className="glass-panel p-6 text-center border-t-4 border-red-500 bg-red-50/10">
            <div className="text-4xl font-black text-red-600 mb-1">{stats.cancer}</div>
            <div className="text-[10px] uppercase tracking-[0.2em] font-black text-gray-400">Suspicious</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="glass-panel p-8">
          <h2 className="text-2xl font-heading font-black text-gray-900 mb-6">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <button
              onClick={() => navigate('/upload')}
              className="p-6 bg-primary/5 rounded-3xl hover:bg-primary/10 transition-all group border border-primary/10"
            >
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">📸</div>
              <div className="font-black text-lg text-gray-900">New Analysis</div>
              <div className="text-sm text-gray-500 font-medium">Upload medical image</div>
            </button>

            <button
              onClick={() => navigate('/history')}
              className="p-6 bg-teal-50/50 rounded-3xl hover:bg-teal-50 transition-all group border border-teal-100"
            >
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">📋</div>
              <div className="font-black text-lg text-gray-900">View History</div>
              <div className="text-sm text-gray-500 font-medium">All past analyses</div>
            </button>

            <button
              onClick={() => navigate('/analytics')}
              className="p-6 bg-purple-50/50 rounded-3xl hover:bg-purple-50 transition-all group border border-purple-100"
            >
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">📊</div>
              <div className="font-black text-lg text-gray-900">Analytics</div>
              <div className="text-sm text-gray-500 font-medium">Performance insights</div>
            </button>

            <button
              onClick={() => navigate('/methodology')}
              className="p-6 bg-blue-100/50 rounded-3xl hover:bg-blue-100 transition-all group border border-blue-200"
            >
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">🔬</div>
              <div className="font-black text-lg text-gray-900">Methodology</div>
              <div className="text-sm text-gray-500 font-medium">Technical approach</div>
            </button>
          </div>
        </div>

        {/* Recent Analyses Content remains similar but wrapped in glass-panel */}
        {/* ... omitting unchanged logic for brevity, just updating container ... */}
        <div className="glass-panel p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-heading font-black">Recent Analyses</h2>
            <button
              onClick={() => navigate('/history')}
              className="text-primary hover:text-primary-hover text-sm font-black tracking-widest uppercase"
            >
              View All →
            </button>
          </div>
          {/* ... existing recentAnalyses mapping ... */}
          {recentAnalyses.length > 0 ? (
            <div className="space-y-4">
              {recentAnalyses.map((analysis) => (
                <div
                  key={analysis.id}
                  className="glass-panel p-4 bg-white/40 hover:bg-white/80 transition-all border-white/50"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex items-start space-x-4">
                      <span className="text-3xl bg-white w-12 h-12 rounded-xl flex items-center justify-center shadow-sm">{getOrganIcon(analysis.organ)}</span>
                      <div>
                        <div className="font-black text-gray-900">{analysis.organ} Analysis</div>
                        <div className={`text-sm font-bold ${getDiagnosisColor(analysis.diagnosis)}`}>
                          {analysis.diagnosis} ({analysis.confidence_pct ?? analysis.diagnosis_confidence_pct}%)
                        </div>
                        <div className="text-[10px] text-gray-400 font-black uppercase tracking-widest mt-1">
                          {analysis.method} • {new Date(analysis.timestamp).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => navigate(`/results/${analysis.id}`)}
                      className="px-4 py-2 bg-primary text-white text-xs font-black rounded-xl hover:bg-primary-hover transition-all btn-premium shadow-lg shadow-primary/20"
                    >
                      DETAILS
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📊</div>
              <p className="text-gray-500 font-bold mb-6">No analyses found in this session</p>
              <button
                onClick={() => navigate('/upload')}
                className="px-8 py-3 bg-primary text-white rounded-xl font-black btn-premium"
              >
                Start First Analysis
              </button>
            </div>
          )}
        </div>

        {/* AI Models Status */}
        <div className="glass-panel p-8">
          <h2 className="text-2xl font-heading font-black mb-6">🤖 Model Insight</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {[
              { id: 'bone', label: 'Bone', icon: '🦴', method: 'Radiomics' },
              { id: 'lung', label: 'Lung', icon: '🫁', method: 'ViT' },
              { id: 'brain', label: 'Brain', icon: '🧠', method: 'CNN' },
              { id: 'blood', label: 'Blood', icon: '🩸', method: 'GNN' },
              { id: 'skin', label: 'Skin', icon: '🧴', method: 'ML' },
              { id: 'breast', label: 'Breast', icon: '🎀', method: 'Ensemble' }
            ].map((m) => (
              <div key={m.id} className="glass-panel p-6 bg-white/20 border-white/30 text-center hover:-translate-y-2 transition-transform cursor-default">
                <div className="text-4xl mb-3 animate-float">{m.icon}</div>
                <div className="font-black text-gray-900 text-sm">{m.label}</div>
                <div className="text-[8px] font-black text-primary-hover uppercase tracking-widest mb-3">{m.method}</div>
                <div className="flex items-center justify-center text-[8px] text-green-600 font-black tracking-widest">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5 animate-pulse"></span>
                  ACTIVE
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
