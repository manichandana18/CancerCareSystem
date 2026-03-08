import { Link } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";
import { useState, useEffect, useRef, useCallback } from "react";

/* ── Unsplash images (free, high-quality) ── */
const IMAGES = {
  hero: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1920&q=80&auto=format&fit=crop",
  // Caring doctor with patient — recovery & hope
  impact: "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=1920&q=80&auto=format&fit=crop",
  // Doctor with patient — supportive care
  cta: "https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=1920&q=80&auto=format&fit=crop",
  // Recovery & wellness — people outdoors
  testimonial: "https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?w=1920&q=80&auto=format&fit=crop",
  // Community support / togetherness
};

/* ── Animated counter hook ── */
function useCounter(end: number, duration = 2000, trigger = false) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!trigger) return;
    let start = 0;
    const step = end / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);
    return () => clearInterval(timer);
  }, [end, duration, trigger]);
  return count;
}

/* ── Intersection Observer hook for scroll-triggered animations ── */
function useInView(threshold = 0.2) {
  const ref = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setIsInView(true); },
      { threshold }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold]);
  return { ref, isInView };
}

export default function Home() {
  const { t } = useLanguage();
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  /* Parallax mouse tracking for hero */
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
    setMousePos({
      x: ((e.clientX - rect.left) / rect.width - 0.5) * 30,
      y: ((e.clientY - rect.top) / rect.height - 0.5) * 15,
    });
  }, []);

  /* Scroll-triggered sections */
  const hero = useInView(0.1);
  const cancerTypes = useInView(0.15);
  const howItWorks = useInView(0.15);
  const features = useInView(0.15);
  const impact = useInView(0.2);
  const testimonials = useInView(0.15);
  const cta = useInView(0.15);

  /* Animated counters (only start when impact section is in view) */
  const accuracy = useCounter(985, 2000, impact.isInView);
  const scans = useCounter(10000, 2500, impact.isInView);
  const patients = useCounter(5000, 2200, impact.isInView);
  const clinics = useCounter(120, 1500, impact.isInView);

  const reveal = (inView: boolean) =>
    `transition-all duration-1000 ease-out ${inView ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`;

  return (
    <div className="relative overflow-hidden" style={{ background: '#fafbfd' }}>

      {/* ═══════════════════════════════════════════════════════
         HERO — Full-bleed background image with parallax
         ═══════════════════════════════════════════════════════ */}
      <section
        ref={hero.ref}
        onMouseMove={handleMouseMove}
        className="relative min-h-[92vh] flex items-center justify-center overflow-hidden"
      >
        {/* Background image with parallax offset */}
        <div
          className="absolute inset-0 z-0 transition-transform duration-300 ease-out"
          style={{
            backgroundImage: `url(${IMAGES.hero})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            transform: `scale(1.1) translate(${mousePos.x * 0.3}px, ${mousePos.y * 0.3}px)`,
          }}
        />
        {/* Dark overlay for text contrast */}
        <div className="absolute inset-0 z-[1]"
          style={{ background: 'linear-gradient(135deg, rgba(2,32,40,0.82) 0%, rgba(6,78,78,0.72) 50%, rgba(13,148,136,0.55) 100%)' }}
        />
        {/* Floating accent orbs */}
        <div className="absolute top-20 right-[15%] w-72 h-72 bg-teal-400 opacity-15 rounded-full blur-[120px] animate-float z-[1]" />
        <div className="absolute bottom-10 left-[10%] w-96 h-96 bg-emerald-500 opacity-10 rounded-full blur-[100px] animate-float z-[1]" style={{ animationDelay: '3s' }} />

        {/* Hero content */}
        <div className={`relative z-10 text-center max-w-5xl mx-auto px-6 ${reveal(hero.isInView)}`}>
          <div className="inline-flex items-center gap-2 mb-8 px-5 py-2.5 rounded-full border border-white/20 text-white/90 font-black text-xs tracking-[0.2em] uppercase"
            style={{ background: 'rgba(255,255,255,0.08)', backdropFilter: 'blur(12px)' }}>
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            AI-Powered Cancer Diagnostics
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-[5.5rem] font-heading font-black mb-8 leading-[1.05] tracking-tight" style={{ color: 'white' }}>
            Early Detection<br />
            <span className="relative inline-block">
              <span className="text-transparent bg-clip-text animate-gradient"
                style={{ backgroundImage: 'linear-gradient(90deg, #5eead4, #2dd4bf, #99f6e4, #2dd4bf)', backgroundSize: '300% auto' }}>
                Saves Lives
              </span>
              <svg className="absolute -bottom-2 left-0 w-full" viewBox="0 0 300 12" fill="none">
                <path d="M2 8C50 2 100 2 150 6C200 10 250 4 298 8" stroke="rgba(94,234,212,0.5)" strokeWidth="3" strokeLinecap="round" />
              </svg>
            </span>
          </h1>

          <p className="text-xl md:text-2xl mb-12 leading-relaxed max-w-3xl mx-auto font-medium" style={{ color: 'rgba(255,255,255,0.85)' }}>
            State-of-the-art AI for <strong style={{ color: 'white' }}>Bone, Lung, Brain, Blood, Skin</strong> and <strong style={{ color: 'white' }}>Breast</strong> cancer — with <span className="text-emerald-300 font-bold">98.5% accuracy</span>.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-5 mb-10">
            <Link to="/upload">
              <button className="group px-12 py-5 rounded-2xl font-black text-lg transition-all transform hover:-translate-y-1.5 active:scale-95 w-full sm:w-auto btn-premium shadow-2xl"
                style={{ background: 'linear-gradient(135deg, #0d9488, #0f766e)', color: 'white', boxShadow: '0 20px 60px rgba(13,148,136,0.4)' }}>
                <span className="flex items-center justify-center gap-2">
                  🔬 Start Analysis
                  <svg className="w-5 h-5 group-hover:translate-x-1.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </button>
            </Link>
            <Link to="/wellness">
              <button className="px-12 py-5 border-2 border-white/25 rounded-2xl font-black text-lg hover:bg-white/10 hover:border-white/40 transition-all w-full sm:w-auto btn-premium"
                style={{ color: 'white', backdropFilter: 'blur(8px)' }}>
                🌿 {t('nav.wellness')}
              </button>
            </Link>
          </div>

          {/* Trust badges */}
          <div className="flex flex-wrap justify-center items-center gap-6 mt-4" style={{ color: 'rgba(255,255,255,0.6)' }}>
            {['HIPAA Compliant', 'End-to-End Encrypted', '6 Cancer Types', 'Sub-Second Results'].map((badge, i) => (
              <div key={i} className="flex items-center gap-2 text-sm font-bold">
                <span className="text-emerald-400">✓</span> {badge}
                {i < 3 && <span className="ml-6 w-px h-4 bg-white/20 hidden sm:block" />}
              </div>
            ))}
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2">
          <span className="text-white/40 text-[10px] font-bold tracking-[0.3em] uppercase">Scroll</span>
          <div className="w-6 h-10 rounded-full border-2 border-white/30 flex justify-center pt-2">
            <div className="w-1.5 h-3 bg-white/50 rounded-full" style={{ animation: 'scrollBounce 2s infinite' }} />
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         CANCER TYPES — Cards with hover glow
         ═══════════════════════════════════════════════════════ */}
      <section ref={cancerTypes.ref} className={`py-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto ${reveal(cancerTypes.isInView)}`}>
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-heading font-black text-gray-900 mb-4">
            What We <span className="text-teal-600">Detect</span>
          </h2>
          <p className="text-gray-500 font-medium text-lg max-w-2xl mx-auto">Six specialized AI models, each trained on thousands of clinical images.</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {[
            { icon: "🦴", name: "Bone", method: "Radiomics Ensemble", accent: "#f59e0b", bg: "linear-gradient(135deg, #fffbeb, #fef3c7)" },
            { icon: "🫁", name: "Lung", method: "Vision Transformer", accent: "#0ea5e9", bg: "linear-gradient(135deg, #f0f9ff, #e0f2fe)" },
            { icon: "🧠", name: "Brain", method: "Deep CNN", accent: "#8b5cf6", bg: "linear-gradient(135deg, #faf5ff, #ede9fe)" },
            { icon: "🩸", name: "Blood", method: "Graph Neural Net", accent: "#ef4444", bg: "linear-gradient(135deg, #fef2f2, #fecaca)" },
            { icon: "🧴", name: "Skin", method: "ML Classifier", accent: "#10b981", bg: "linear-gradient(135deg, #ecfdf5, #d1fae5)" },
            { icon: "🎀", name: "Breast", method: "Ensemble", accent: "#ec4899", bg: "linear-gradient(135deg, #fdf2f8, #fce7f3)" },
          ].map((type, i) => (
            <div key={i}
              className="relative group cursor-default p-7 rounded-3xl text-center transition-all duration-500 hover:scale-105 hover:-translate-y-2 border-2 overflow-hidden"
              style={{
                background: type.bg,
                borderColor: 'transparent',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.borderColor = type.accent)}
              onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'transparent')}
            >
              {/* Glow on hover */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl pointer-events-none"
                style={{ boxShadow: `inset 0 0 40px ${type.accent}15, 0 15px 40px ${type.accent}20` }} />

              <div className="text-5xl mb-4 group-hover:scale-125 transition-all duration-500 group-hover:drop-shadow-lg relative z-10">
                {type.icon}
              </div>
              <div className="font-black text-gray-900 text-base relative z-10">{type.name}</div>
              <div className="text-[8px] font-black text-gray-400 uppercase tracking-[0.15em] mt-1.5 relative z-10">{type.method}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         HOW IT WORKS — Numbered steps with connecting line
         ═══════════════════════════════════════════════════════ */}
      <section ref={howItWorks.ref}
        className="py-28 relative"
        style={{ background: 'linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%)' }}>
        <div className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 ${reveal(howItWorks.isInView)}`}>
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-heading font-black text-gray-900 mb-4">
              How It <span className="text-teal-600">Works</span>
            </h2>
            <p className="text-gray-500 font-medium text-lg">Three simple steps to a life-saving insight.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-10 relative">
            {/* Connecting line */}
            <div className="hidden md:block absolute top-20 left-[20%] right-[20%] h-0.5"
              style={{ background: 'linear-gradient(90deg, transparent, #99f6e4, #2dd4bf, #99f6e4, transparent)' }} />

            {[
              { step: "01", icon: "📤", title: "Upload Scan", desc: "Upload X-ray, MRI, CT scan, or blood sample image directly from your device." },
              { step: "02", icon: "🤖", title: "AI Analyzes", desc: "Our 6 specialized neural networks process the image with medical-grade precision in under 1 second." },
              { step: "03", icon: "📊", title: "Get Results", desc: "Receive detailed diagnosis, confidence score, staging assessment, and next-step recommendations." },
            ].map((s, i) => (
              <div key={i} className="relative text-center group"
                style={{ transitionDelay: `${i * 150}ms` }}>
                {/* Step number badge */}
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-20 px-3 py-1 rounded-full text-[10px] font-black tracking-[0.3em] uppercase"
                  style={{ background: 'linear-gradient(135deg, #0d9488, #0f766e)', color: 'white' }}>
                  Step {s.step}
                </div>

                <div className="w-36 h-36 mx-auto mb-8 rounded-[2.5rem] flex items-center justify-center text-6xl shadow-xl group-hover:shadow-teal-200/60 transition-all duration-700 group-hover:scale-110 group-hover:-rotate-3 relative overflow-hidden"
                  style={{ background: 'linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,253,250,0.9))', border: '2px solid #ccfbf1' }}>
                  {/* Shimmer effect on hover */}
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 animate-shimmer" />
                  <span className="relative z-10">{s.icon}</span>
                </div>
                <h3 className="text-xl font-heading font-black text-gray-900 mb-3 group-hover:text-teal-700 transition-colors">{s.title}</h3>
                <p className="text-gray-500 font-medium text-sm leading-relaxed max-w-xs mx-auto">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         FEATURE CARDS — With 3D tilt + glow
         ═══════════════════════════════════════════════════════ */}
      <section ref={features.ref} className={`py-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto ${reveal(features.isInView)}`}>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { icon: "🧠", title: "Multi-Model AI", desc: "Specialized architectures — CNN, ResNet, ViT, GNN — each optimized for specific cancer types and imaging modalities.", gradient: "from-teal-500 to-emerald-500" },
            { icon: "🛡️", title: "Privacy First", desc: "Your medical data is encrypted end-to-end with AES-256. We never store raw images — only encrypted diagnostic metadata.", gradient: "from-blue-500 to-indigo-500" },
            { icon: "💚", title: "Holistic Support", desc: "Beyond diagnosis: Access wigs marketplace, donation portal, mental wellness exercises, and guided yoga sessions.", gradient: "from-purple-500 to-violet-500" },
          ].map((feature, idx) => (
            <div key={idx} className="card-perspective">
              <div className="flash-card p-8 rounded-[2rem] group cursor-default relative overflow-hidden h-full">
                {/* Glow background */}
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-[0.04] transition-opacity duration-500 rounded-[2rem]`} />
                <div className="relative z-10">
                  <div className={`icon-container w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center text-3xl mb-6 shadow-lg`}
                    style={{ color: 'white' }}>
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-heading font-black text-gray-900 mb-3 group-hover:text-teal-700 transition-colors">{feature.title}</h3>
                  <p className="text-gray-500 leading-relaxed font-medium">{feature.desc}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         IMPACT STATS — Full-bleed image background + animated counters
         ═══════════════════════════════════════════════════════ */}
      <section ref={impact.ref} className="relative py-32 overflow-hidden">
        {/* Background image */}
        <div className="absolute inset-0"
          style={{ backgroundImage: `url(${IMAGES.impact})`, backgroundSize: 'cover', backgroundPosition: 'center', backgroundAttachment: 'fixed' }} />
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(135deg, rgba(13,148,136,0.92) 0%, rgba(15,118,110,0.88) 50%, rgba(17,94,89,0.95) 100%)' }} />

        {/* Floating orbs */}
        <div className="absolute top-0 right-0 w-80 h-80 bg-white opacity-10 rounded-full blur-[120px] translate-x-1/2 -translate-y-1/2 animate-float" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-black opacity-5 rounded-full blur-[100px] -translate-x-1/2 translate-y-1/2 animate-float" style={{ animationDelay: '4s' }} />

        <div className={`relative z-10 max-w-6xl mx-auto px-6 text-center ${reveal(impact.isInView)}`}>
          <h2 className="text-3xl md:text-5xl font-heading font-black mb-4 drop-shadow-lg" style={{ color: 'white' }}>
            Making a Real <span className="underline decoration-white/30 decoration-4 underline-offset-8">Impact</span>
          </h2>
          <p className="mb-16 text-lg font-medium max-w-2xl mx-auto" style={{ color: 'rgba(255,255,255,0.7)' }}>
            Trusted by hospitals, clinics, and patients worldwide for early cancer detection.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12">
            {[
              { label: "Accuracy Rate", val: `${(accuracy / 10).toFixed(1)}%`, icon: "🎯" },
              { label: "Scans Analyzed", val: scans >= 10000 ? "10K+" : scans.toLocaleString(), icon: "🔬" },
              { label: "Patients Helped", val: patients >= 5000 ? "5,000+" : patients.toLocaleString(), icon: "❤️" },
              { label: "Partner Clinics", val: clinics >= 120 ? "120+" : clinics.toString(), icon: "🏥" },
            ].map((stat, i) => (
              <div key={i} className="group cursor-default hover:scale-110 transition-transform duration-500 p-4 rounded-3xl"
                style={{ background: 'rgba(255,255,255,0.06)', backdropFilter: 'blur(8px)' }}>
                <div className="text-3xl mb-4 group-hover:scale-125 transition-transform">{stat.icon}</div>
                <div className="text-4xl md:text-5xl font-heading font-black mb-2 drop-shadow-lg tabular-nums" style={{ color: 'white' }}>{stat.val}</div>
                <div className="font-black uppercase tracking-[0.2em] text-[9px]" style={{ color: 'rgba(255,255,255,0.7)' }}>{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         TESTIMONIALS — Background image + glass cards
         ═══════════════════════════════════════════════════════ */}
      <section ref={testimonials.ref} className="relative py-28 overflow-hidden">
        {/* Subtle background image */}
        <div className="absolute inset-0 opacity-[0.04]"
          style={{ backgroundImage: `url(${IMAGES.testimonial})`, backgroundSize: 'cover', backgroundPosition: 'center' }} />

        <div className={`relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ${reveal(testimonials.isInView)}`}>
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-black text-gray-900 mb-4">
              Stories of <span className="text-teal-600">Hope</span>
            </h2>
            <p className="text-gray-500 font-medium text-lg">Real people, real impact.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Dr. Priya Sharma", role: "Senior Oncologist, AIIMS", quote: "The AI prediction matched our biopsy results with remarkable accuracy. It's a true second opinion tool that speeds up our workflow significantly.", avatar: "PS", color: "#0d9488" },
              { name: "Ravi Kumar", role: "Stage II Survivor, 42", quote: "Early detection through this platform gave me the head start I needed. I'm now in remission and spending time with my family.", avatar: "RK", color: "#2563eb" },
              { name: "Sarah Mitchell", role: "Caregiver & Advocate", quote: "The wellness resources and community support helped me cope while caring for my mother. The yoga sessions were a lifeline.", avatar: "SM", color: "#7c3aed" },
            ].map((person, i) => (
              <div key={i}
                className="glass-panel p-8 relative group hover:-translate-y-3 hover:shadow-2xl transition-all duration-500"
                style={{ transitionDelay: `${i * 100}ms` }}>
                {/* Quote mark */}
                <div className="absolute top-4 right-6 text-6xl font-heading opacity-10 group-hover:opacity-20 transition-opacity" style={{ color: person.color }}>"</div>

                {/* Star rating */}
                <div className="flex gap-1 mb-4 text-amber-400 text-sm">★★★★★</div>

                <p className="text-gray-600 font-medium mb-6 leading-relaxed italic relative z-10">"{person.quote}"</p>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full flex items-center justify-center text-xs font-black shadow-md"
                    style={{ background: `linear-gradient(135deg, ${person.color}, ${person.color}cc)`, color: 'white' }}>
                    {person.avatar}
                  </div>
                  <div>
                    <p className="font-black text-gray-900 text-sm">{person.name}</p>
                    <p className="text-[10px] text-gray-400 font-bold tracking-wider uppercase">{person.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════════
         FINAL CTA — Full-bleed background image
         ═══════════════════════════════════════════════════════ */}
      <section ref={cta.ref} className="relative py-32 overflow-hidden">
        {/* Background image */}
        <div className="absolute inset-0"
          style={{ backgroundImage: `url(${IMAGES.cta})`, backgroundSize: 'cover', backgroundPosition: 'center' }} />
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(135deg, rgba(15,23,42,0.88) 0%, rgba(30,41,59,0.82) 50%, rgba(13,148,136,0.75) 100%)' }} />

        <div className={`relative z-10 text-center max-w-4xl mx-auto px-6 ${reveal(cta.isInView)}`}>
          <h2 className="text-4xl md:text-5xl font-heading font-black mb-5" style={{ color: 'white' }}>
            Ready to Take <span className="text-emerald-300">Control</span>?
          </h2>
          <p className="text-lg font-medium max-w-xl mx-auto mb-12" style={{ color: 'rgba(255,255,255,0.75)' }}>
            Join thousands who trust CancerCare AI for early detection, peace of mind, and holistic support.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-5">
            <Link to="/register">
              <button className="px-14 py-5 rounded-2xl font-black text-lg shadow-2xl transition-all transform hover:-translate-y-1.5 active:scale-95 btn-premium"
                style={{ background: 'linear-gradient(135deg, #0d9488, #0f766e)', color: 'white', boxShadow: '0 20px 60px rgba(13,148,136,0.4)' }}>
                Create Free Account →
              </button>
            </Link>
            <Link to="/upload">
              <button className="px-14 py-5 border-2 border-white/25 rounded-2xl font-black text-lg hover:bg-white/10 hover:border-white/40 transition-all btn-premium"
                style={{ color: 'white', backdropFilter: 'blur(8px)' }}>
                Try Demo Analysis
              </button>
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
