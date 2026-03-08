import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";

interface AnalysisResult {
  id: string;
  organ: string;
  diagnosis: string;
  diagnosis_confidence: number;
  diagnosis_confidence_pct: number;
  method: string;
  model_type: string;
  timestamp: string;
  cell_count?: number;
}

export default function Analytics() {
  const { t } = useLanguage();
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([]);
  const [analytics, setAnalytics] = useState({
    totalAnalyses: 0,
    avgConfidence: 0,
    organDistribution: {} as Record<string, number>,
    diagnosisDistribution: {} as Record<string, number>,
    modelPerformance: {} as Record<string, { count: number; avgConfidence: number }>,
    monthlyTrends: [] as Array<{ month: string; count: number; avgConfidence: number }>
  });
  const navigate = useNavigate();

  useEffect(() => {
    const history = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
    setAnalyses(history);
    if (history.length > 0) {
      calculateAnalytics(history);
    }
  }, []);

  const calculateAnalytics = (data: AnalysisResult[]) => {
    const totalAnalyses = data.length;
    const avgConfidence = data.reduce((sum, item) => sum + item.diagnosis_confidence_pct, 0) / totalAnalyses;

    const organDistribution: Record<string, number> = {};
    data.forEach(item => {
      organDistribution[item.organ] = (organDistribution[item.organ] || 0) + 1;
    });

    const diagnosisDistribution: Record<string, number> = {};
    data.forEach(item => {
      const diagnosis = item.diagnosis.toLowerCase().includes('normal') ||
        item.diagnosis.toLowerCase().includes('benign') ? 'Normal' : 'Cancer';
      diagnosisDistribution[diagnosis] = (diagnosisDistribution[diagnosis] || 0) + 1;
    });

    const modelPerformance: Record<string, { count: number; avgConfidence: number }> = {};
    data.forEach(item => {
      if (!modelPerformance[item.method]) {
        modelPerformance[item.method] = { count: 0, avgConfidence: 0 };
      }
      modelPerformance[item.method].count += 1;
      modelPerformance[item.method].avgConfidence += item.diagnosis_confidence_pct;
    });

    Object.keys(modelPerformance).forEach(model => {
      modelPerformance[model].avgConfidence /= modelPerformance[model].count;
    });

    const monthlyTrends: Array<{ month: string; count: number; avgConfidence: number }> = [];
    const now = new Date();
    for (let i = 5; i >= 0; i--) {
      const monthDate = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const monthStr = monthDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });

      const monthData = data.filter(item => {
        const itemDate = new Date(item.timestamp);
        return itemDate.getMonth() === monthDate.getMonth() &&
          itemDate.getFullYear() === monthDate.getFullYear();
      });

      monthlyTrends.push({
        month: monthStr,
        count: monthData.length,
        avgConfidence: monthData.length > 0
          ? monthData.reduce((sum, item) => sum + item.diagnosis_confidence_pct, 0) / monthData.length
          : 0
      });
    }

    setAnalytics({ totalAnalyses, avgConfidence, organDistribution, diagnosisDistribution, modelPerformance, monthlyTrends });
  };

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

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'text-green-600';
    if (confidence >= 70) return 'text-amber-500';
    return 'text-red-500';
  };

  const getConfidenceBarColor = (confidence: number) => {
    if (confidence >= 90) return 'from-green-400 to-emerald-500';
    if (confidence >= 70) return 'from-amber-400 to-orange-500';
    return 'from-red-400 to-rose-500';
  };

  const getOrganBarColor = (organ: string) => {
    switch (organ?.toLowerCase()) {
      case 'bone': return 'from-amber-400 to-orange-500';
      case 'lung': return 'from-sky-400 to-blue-500';
      case 'brain': return 'from-purple-400 to-violet-500';
      case 'blood': return 'from-red-400 to-rose-500';
      case 'skin': return 'from-emerald-400 to-green-500';
      case 'breast': return 'from-pink-400 to-rose-500';
      default: return 'from-teal-400 to-cyan-500';
    }
  };

  const benchmarks = [
    { architecture: t('analytics.benchmarks.vit'), accuracy: "91%" },
    { architecture: t('analytics.benchmarks.cnn'), accuracy: "85%" },
    { architecture: t('analytics.benchmarks.gnn'), accuracy: "88%" },
    { architecture: t('analytics.benchmarks.ensemble'), accuracy: "94%", isWinner: true },
  ].sort((a, b) => parseInt(a.accuracy) - parseInt(b.accuracy));

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="glass-panel p-8">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center text-2xl text-white shadow-lg shadow-teal-200/50">
            📊
          </div>
          <div>
            <h1 className="text-3xl font-heading font-black text-gray-900">
              {t('analytics.title')}
            </h1>
            <p className="text-gray-500 font-medium">
              {t('analytics.subtitle')}
            </p>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { icon: '📊', label: t('dashboard.stats.scans'), value: analytics.totalAnalyses, bg: 'from-blue-500/10 to-indigo-500/10', border: 'border-blue-200/50', color: 'text-blue-600' },
          { icon: '🎯', label: t('history.confidence'), value: `${analytics.avgConfidence.toFixed(1)}%`, bg: 'from-green-500/10 to-emerald-500/10', border: 'border-green-200/50', color: getConfidenceColor(analytics.avgConfidence) },
          { icon: '🔬', label: t('rec.critical'), value: analytics.diagnosisDistribution['Cancer'] || 0, bg: 'from-red-500/10 to-rose-500/10', border: 'border-red-200/50', color: 'text-red-600' },
          { icon: '✅', label: t('staging.no'), value: analytics.diagnosisDistribution['Normal'] || 0, bg: 'from-green-500/10 to-teal-500/10', border: 'border-green-200/50', color: 'text-green-600' },
        ].map((metric, i) => (
          <div key={i}
            className={`glass-panel p-6 border ${metric.border} hover:-translate-y-1 transition-all duration-300 group`}
          >
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${metric.bg} flex items-center justify-center text-xl mb-4 group-hover:scale-110 transition-transform`}>
              {metric.icon}
            </div>
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">{metric.label}</p>
            <p className={`text-3xl font-black ${metric.color}`}>{metric.value}</p>
          </div>
        ))}
      </div>

      {/* Benchmarks Section */}
      <div className="glass-panel p-10 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 border-indigo-100/50">
        <h2 className="text-2xl font-heading font-black text-gray-900 mb-8 flex items-center gap-3">
          <span className="w-10 h-10 rounded-xl bg-white shadow-sm flex items-center justify-center text-xl">🏆</span>
          {t('analytics.benchmarks.title')}
        </h2>

        <div className="overflow-hidden rounded-3xl border border-white bg-white/40 backdrop-blur-md shadow-xl">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-white/60">
                <th className="px-8 py-5 text-[10px] font-black text-indigo-400 uppercase tracking-widest border-r border-indigo-50/50 last:border-0">
                  {t('analytics.benchmarks.model')}
                </th>
                <th className="px-8 py-5 text-[10px] font-black text-indigo-400 uppercase tracking-widest">
                  {t('analytics.benchmarks.accuracy')}
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-indigo-50/50">
              {benchmarks.map((b, i) => (
                <tr
                  key={i}
                  className={`transition-all duration-300 hover:bg-white/80 ${b.isWinner ? 'bg-primary/5' : ''
                    }`}
                >
                  <td className={`px-8 py-6 font-bold text-gray-700 border-r border-indigo-50/50 last:border-0 ${b.isWinner ? 'text-primary' : ''}`}>
                    {b.architecture}
                  </td>
                  <td className={`px-8 py-6 font-black text-gray-900 ${b.isWinner ? 'text-primary' : ''}`}>
                    {b.accuracy}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="mt-8 text-gray-500 font-medium leading-relaxed italic text-sm max-w-2xl">
          {t('analytics.benchmarks.desc')}
        </p>
      </div>

      {/* Charts Row */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Organ Distribution */}
        <div className="glass-panel p-8">
          <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-2">
            <span className="text-teal-500">🧬</span> Organ Distribution
          </h2>
          <div className="space-y-4">
            {Object.entries(analytics.organDistribution).map(([organ, count]) => (
              <div key={organ} className="group">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-2xl group-hover:scale-125 transition-transform">{getOrganIcon(organ)}</span>
                  <span className="font-bold text-gray-700 flex-1 capitalize">{t(`upload.${organ.toLowerCase()}`)}</span>
                  <span className="text-sm font-black text-gray-400 bg-gray-100 px-3 py-1 rounded-full">{count}</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                  <div
                    className={`bg-gradient-to-r ${getOrganBarColor(organ)} h-full rounded-full transition-all duration-1000`}
                    style={{ width: `${(count / analytics.totalAnalyses) * 100}%` }}
                  />
                </div>
              </div>
            ))}
            {Object.keys(analytics.organDistribution).length === 0 && (
              <p className="text-gray-400 text-center py-8 font-medium">No data available yet</p>
            )}
          </div>
        </div>

        {/* Diagnosis Distribution */}
        <div className="glass-panel p-8">
          <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-2">
            <span className="text-teal-500">📋</span> Diagnosis Distribution
          </h2>
          <div className="space-y-6">
            {Object.entries(analytics.diagnosisDistribution).map(([diagnosis, count]) => {
              const pct = ((count / analytics.totalAnalyses) * 100).toFixed(1);
              const isCancer = diagnosis === 'Cancer';
              return (
                <div key={diagnosis} className="group">
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-lg shadow-sm ${isCancer ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}`}>
                      {isCancer ? '⚠️' : '✅'}
                    </div>
                    <span className="font-bold text-gray-700 flex-1">{isCancer ? t('rec.critical') : t('staging.no')}</span>
                    <div className="text-right">
                      <span className={`text-lg font-black ${isCancer ? 'text-red-600' : 'text-green-600'}`}>{count}</span>
                      <span className="text-xs text-gray-400 ml-1">({pct}%)</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-1000 ${isCancer ? 'bg-gradient-to-r from-red-400 to-rose-500' : 'bg-gradient-to-r from-green-400 to-emerald-500'}`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
            {Object.keys(analytics.diagnosisDistribution).length === 0 && (
              <p className="text-gray-400 text-center py-8 font-medium">No data available yet</p>
            )}
          </div>
        </div>
      </div>

      {/* Model Performance */}
      <div className="glass-panel p-8">
        <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-2">
          <span className="text-teal-500">🤖</span> Model Performance
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          {Object.entries(analytics.modelPerformance).map(([model, performance]) => (
            <div key={model} className="glass-panel p-6 border border-gray-200/50 hover:-translate-y-1 transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500/10 to-purple-500/10 flex items-center justify-center text-lg">🧠</div>
                <h3 className="font-black text-gray-800 text-sm uppercase tracking-wider">{model}</h3>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400 font-medium">{t('dashboard.stats.scans')}</span>
                  <span className="font-black text-gray-700">{performance.count}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400 font-medium">{t('history.confidence')}</span>
                  <span className={`font-black ${getConfidenceColor(performance.avgConfidence)}`}>
                    {performance.avgConfidence.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${getConfidenceBarColor(performance.avgConfidence)} transition-all duration-1000`}
                    style={{ width: `${performance.avgConfidence}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
          {Object.keys(analytics.modelPerformance).length === 0 && (
            <div className="col-span-full text-center py-8">
              <p className="text-gray-400 font-medium">No model data available yet</p>
            </div>
          )}
        </div>
      </div>

      {/* Monthly Trends */}
      <div className="glass-panel p-8">
        <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-2">
          <span className="text-teal-500">📈</span> Monthly Trends
        </h2>
        <div className="space-y-4">
          {analytics.monthlyTrends.map((trend) => {
            const maxCount = Math.max(...analytics.monthlyTrends.map(t => t.count), 1);
            return (
              <div key={trend.month} className="flex items-center gap-4 group">
                <div className="w-28 text-sm font-bold text-gray-500 shrink-0">{trend.month}</div>
                <div className="flex-1">
                  <div className="flex justify-between mb-1.5">
                    <span className="text-xs font-bold text-gray-400">
                      {trend.count} {trend.count === 1 ? t('staging.step.results').slice(0, -1) : t('staging.step.results')}
                    </span>
                    <span className={`text-xs font-black ${trend.avgConfidence > 0 ? getConfidenceColor(trend.avgConfidence) : 'text-gray-300'}`}>
                      {trend.avgConfidence > 0 ? `${trend.avgConfidence.toFixed(1)}%` : 'N/A'}
                    </span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-teal-400 to-emerald-500 h-full rounded-full transition-all duration-1000 group-hover:shadow-[0_0_12px_rgba(13,148,136,0.4)]"
                      style={{
                        width: trend.count > 0 ? `${Math.min((trend.count / maxCount) * 100, 100)}%` : '0%'
                      }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Export Options */}
      <div className="glass-panel p-8">
        <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-2">
          <span className="text-teal-500">💾</span> {t('analytics.export.title')}
        </h2>
        <div className="flex flex-wrap gap-4">
          <button
            onClick={() => {
              const dataStr = JSON.stringify(analytics, null, 2);
              const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
              const exportFileDefaultName = `cancer-analytics-${new Date().toISOString().split('T')[0]}.json`;
              const linkElement = document.createElement('a');
              linkElement.setAttribute('href', dataUri);
              linkElement.setAttribute('download', exportFileDefaultName);
              linkElement.click();
            }}
            disabled={analyses.length === 0}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] text-white font-black shadow-lg shadow-teal-200/30 hover:shadow-xl hover:-translate-y-0.5 transition-all disabled:opacity-40 disabled:hover:translate-y-0 disabled:hover:shadow-lg"
          >
            📊 {t('analytics.export.btn')}
          </button>

          <button
            onClick={() => navigate('/history')}
            className="px-6 py-3 rounded-xl bg-gray-100 text-gray-700 font-bold hover:bg-gray-200 transition-all"
          >
            📋 {t('dashboard.view_all')}
          </button>
        </div>
      </div>
    </div>
  );
}
