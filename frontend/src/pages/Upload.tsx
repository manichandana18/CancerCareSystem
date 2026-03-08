import { useState, useRef, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { saveAnalysis, type AnalysisResult } from "../services/historyApi";
import { useToast } from "../components/Toast";

const API_BASE = import.meta.env.VITE_API_URL || '';

const DETECTION_TYPES = [
  { value: 'auto', label: 'Auto Detect', icon: '🤖', desc: 'AI picks the best model', accent: '#0d9488', bg: 'linear-gradient(135deg, #f0fdfa, #ccfbf1)' },
  { value: 'bone', label: 'Bone', icon: '🦴', desc: 'X-ray / CT analysis', accent: '#f59e0b', bg: 'linear-gradient(135deg, #fffbeb, #fef3c7)' },
  { value: 'lung', label: 'Lung', icon: '🫁', desc: 'X-ray / CT analysis', accent: '#0ea5e9', bg: 'linear-gradient(135deg, #f0f9ff, #e0f2fe)' },
  { value: 'brain', label: 'Brain', icon: '🧠', desc: 'MRI / CT analysis', accent: '#8b5cf6', bg: 'linear-gradient(135deg, #faf5ff, #ede9fe)' },
  { value: 'blood', label: 'Blood', icon: '🩸', desc: 'Blood smear images', accent: '#ef4444', bg: 'linear-gradient(135deg, #fef2f2, #fecaca)' },
  { value: 'skin', label: 'Skin', icon: '🧴', desc: 'Dermoscopy images', accent: '#10b981', bg: 'linear-gradient(135deg, #ecfdf5, #d1fae5)' },
  { value: 'breast', label: 'Breast', icon: '🎀', desc: 'Mammogram / Ultrasound', accent: '#ec4899', bg: 'linear-gradient(135deg, #fdf2f8, #fce7f3)' },
] as const;

export default function Upload() {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [detectionType, setDetectionType] = useState<string>('auto');
  const [isDragging, setIsDragging] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  useEffect(() => {
    const type = searchParams.get('type');
    if (type && DETECTION_TYPES.some(t => t.value === type)) {
      setDetectionType(type);
    }
  }, [searchParams]);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleAnalyze = async () => {
    if (!image) {
      showToast("Please upload an image first", "warning");
      return;
    }

    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append('file', image);

      let endpoint = '/auto-predict';
      if (detectionType === 'bone') endpoint = '/predict';
      else if (detectionType === 'blood') endpoint = '/predict/blood';
      else if (detectionType === 'brain') endpoint = '/predict/brain';
      else if (detectionType === 'skin') endpoint = '/predict/skin';
      else if (detectionType === 'breast') endpoint = '/predict/breast';
      else if (detectionType === 'lung') endpoint = '/auto-predict';

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Analysis failed');

      const result: AnalysisResult = await response.json();
      result.id = Date.now().toString();
      result.timestamp = new Date().toISOString();

      if (!result.confidence && result.diagnosis_confidence) result.confidence = result.diagnosis_confidence;
      if (!result.confidence_pct && result.diagnosis_confidence_pct) result.confidence_pct = result.diagnosis_confidence_pct;

      await saveAnalysis(result);
      showToast('Analysis complete! Navigating to results...', 'success');
      navigate(`/results/${result.id}`, { state: { result } });

    } catch (error) {
      console.error('Analysis error:', error);
      showToast('Failed to analyze image. Please try again.', 'error');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const selectedType = DETECTION_TYPES.find(t => t.value === detectionType)!;

  return (
    <div className="relative min-h-screen mesh-bg">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">

        {/* ─── HEADER ─── */}
        <div className="glass-panel p-8 md:p-10 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-teal-400/10 rounded-full blur-[100px] -z-0 animate-float" />
          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 mb-4 px-4 py-1.5 rounded-full bg-teal-50 text-teal-600 font-black text-[10px] tracking-[0.2em] uppercase border border-teal-100">
              <span className="w-2 h-2 bg-teal-500 rounded-full animate-pulse" /> AI Diagnostic Engine
            </div>
            <h1 className="text-4xl md:text-5xl font-heading font-black text-gray-900 mb-3 leading-tight">
              Cancer <span className="text-teal-600">Detection</span>
            </h1>
            <p className="text-gray-500 font-medium text-lg max-w-2xl">
              Upload a medical scan — our AI analyzes it with <strong className="text-gray-700">6 specialized neural networks</strong> for maximum diagnostic accuracy.
            </p>
          </div>
        </div>

        {/* ─── DETECTION TYPE SELECTOR ─── */}
        <div className="glass-panel p-8">
          <h2 className="text-xl font-heading font-black text-gray-900 mb-2 flex items-center gap-3">
            <span className="w-10 h-10 bg-teal-50 rounded-xl flex items-center justify-center text-lg border border-teal-100">🎯</span>
            Detection Type
          </h2>
          <p className="text-sm text-gray-400 font-medium mb-6 ml-[52px]">Select the cancer type or let AI auto-detect from the image.</p>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {DETECTION_TYPES.map((type) => (
              <button
                key={type.value}
                onClick={() => setDetectionType(type.value)}
                className={`relative p-5 rounded-2xl transition-all duration-300 border-2 text-left group overflow-hidden
                  ${detectionType === type.value
                    ? 'scale-[1.02] shadow-lg -translate-y-1'
                    : 'hover:scale-[1.01] hover:-translate-y-0.5 hover:shadow-md'
                  }`}
                style={{
                  background: type.bg,
                  borderColor: detectionType === type.value ? type.accent : 'transparent',
                  boxShadow: detectionType === type.value ? `0 8px 30px ${type.accent}25` : undefined,
                }}
              >
                {/* Selected indicator */}
                {detectionType === type.value && (
                  <div className="absolute top-2 right-2 w-5 h-5 rounded-full flex items-center justify-center text-white text-[10px] font-black"
                    style={{ background: type.accent }}>✓</div>
                )}
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform duration-300">{type.icon}</div>
                <div className="font-black text-gray-900 text-sm">{type.label}</div>
                <div className="text-[10px] text-gray-400 font-bold mt-0.5">{type.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* ─── IMAGE UPLOAD AREA ─── */}
        <div className="glass-panel p-8">
          <h2 className="text-xl font-heading font-black text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-teal-50 rounded-xl flex items-center justify-center text-lg border border-teal-100">📤</span>
            Upload Medical Image
          </h2>

          <div
            onDrop={handleDrop}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onClick={() => fileRef.current?.click()}
            className={`relative rounded-3xl p-12 text-center cursor-pointer transition-all duration-400 border-2 border-dashed group
              ${isDragging
                ? 'border-teal-500 bg-teal-50/60 scale-[1.01]'
                : preview
                  ? 'border-teal-200 bg-teal-50/20'
                  : 'border-gray-200 hover:border-teal-300 hover:bg-teal-50/30'
              }`}
          >
            <input ref={fileRef} type="file" accept="image/*" onChange={handleImageChange} className="hidden" />

            {preview ? (
              <div className="space-y-4">
                <div className="relative inline-block rounded-2xl overflow-hidden shadow-2xl border-4 border-white/80">
                  <img src={preview} alt="Medical scan preview" className="max-h-80 object-contain" />
                  {/* Overlay with file info */}
                  <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/60 to-transparent p-4">
                    <p className="text-white text-sm font-black truncate">{image?.name}</p>
                    <p className="text-white/70 text-xs font-bold">{((image?.size || 0) / 1024 / 1024).toFixed(2)} MB • Click to change</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="w-20 h-20 mx-auto rounded-3xl bg-teal-50 border-2 border-teal-100 flex items-center justify-center text-4xl group-hover:scale-110 group-hover:-rotate-6 transition-all duration-500">
                  {isDragging ? '⬇️' : '📸'}
                </div>
                <div>
                  <p className="text-lg font-black text-gray-700 mb-1">
                    {isDragging ? 'Release to upload' : 'Drag & drop your medical scan here'}
                  </p>
                  <p className="text-gray-400 font-medium text-sm">or click to browse files</p>
                </div>
                <div className="inline-flex items-center gap-2 text-[10px] text-gray-400 font-bold uppercase tracking-[0.15em]">
                  <span className="text-teal-500">✓</span> JPG, PNG, BMP, TIFF • Max 50MB
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ─── ANALYZE BUTTON ─── */}
        <div className="text-center">
          <button
            onClick={handleAnalyze}
            disabled={!image || isAnalyzing}
            className={`px-14 py-5 rounded-2xl font-black text-lg transition-all duration-400 btn-premium relative overflow-hidden
              ${!image || isAnalyzing
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none'
                : 'text-white hover:-translate-y-1.5 active:scale-95 shadow-2xl'
              }`}
            style={image && !isAnalyzing ? {
              background: `linear-gradient(135deg, ${selectedType.accent}, ${selectedType.accent}dd)`,
              boxShadow: `0 20px 60px ${selectedType.accent}35`,
            } : undefined}
          >
            {isAnalyzing ? (
              <span className="flex items-center gap-3">
                <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Analyzing with {selectedType.label}...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                {selectedType.icon} Analyze with {selectedType.label}
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
            )}
          </button>
          {!image && (
            <p className="text-xs text-gray-400 font-medium mt-3">Upload an image to enable analysis</p>
          )}
        </div>

        {/* ─── AI MODELS INFO ─── */}
        <div className="glass-panel p-8" style={{ background: 'linear-gradient(135deg, rgba(240,253,250,0.6), rgba(240,249,255,0.4))' }}>
          <h3 className="text-lg font-heading font-black text-gray-900 mb-6 flex items-center gap-3">
            <span className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-500 rounded-xl flex items-center justify-center text-lg text-white shadow-md">🚀</span>
            AI Model Architecture
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: '🦴', name: 'Bone & Lung', tech: 'Radiomics Ensemble + ViT', detail: '100+ radiological features • 8-layer Vision Transformer' },
              { icon: '🧠', name: 'Brain & Skin', tech: 'Deep CNN + ML Classifier', detail: 'ResNet-50 architecture • Dermoscopy-tuned models' },
              { icon: '🩸', name: 'Blood & Breast', tech: 'Graph NN + Ensemble', detail: 'Cell-level graph analysis • Multi-model consensus' },
            ].map((m, i) => (
              <div key={i} className="flex items-start gap-4 p-4 rounded-2xl bg-white/50 border border-white/80 hover:bg-white/80 hover:-translate-y-1 transition-all duration-300 group">
                <div className="text-3xl flex-shrink-0 group-hover:scale-110 transition-transform">{m.icon}</div>
                <div>
                  <div className="font-black text-gray-900 text-sm">{m.name}</div>
                  <div className="text-[10px] text-teal-600 font-black uppercase tracking-[0.15em] mb-1">{m.tech}</div>
                  <div className="text-xs text-gray-500 font-medium leading-relaxed">{m.detail}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
