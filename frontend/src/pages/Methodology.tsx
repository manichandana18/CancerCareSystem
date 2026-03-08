import { useLanguage } from "../contexts/LanguageContext";

export default function Methodology() {
    const { t } = useLanguage();

    const stages = [
        {
            id: "dp",
            title: t('methodology.data_prep'),
            icon: (
                <svg className="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
            ),
            items: [
                t('methodology.dp.clean'),
                t('methodology.dp.missing'),
                t('methodology.dp.scale')
            ]
        },
        {
            id: "mt",
            title: t('methodology.model_training'),
            icon: (
                <svg className="w-12 h-12 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    <circle cx="12" cy="9" r="2" />
                </svg>
            ),
            items: [
                t('methodology.mt.lr'),
                t('methodology.mt.dt'),
                t('methodology.mt.rf'),
                t('methodology.mt.svm')
            ]
        },
        {
            id: "et",
            title: t('methodology.ensemble'),
            icon: (
                <svg className="w-12 h-12 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
            ),
            items: [
                t('methodology.en.voting'),
                t('methodology.en.bagging'),
                t('methodology.en.boosting')
            ]
        }
    ];

    return (
        <div className="max-w-7xl mx-auto py-12 px-6 space-y-16">
            {/* Header */}
            <div className="text-center space-y-6">
                <h1 className="text-5xl font-heading font-black text-gray-900 tracking-tight">
                    {t('methodology.title')}
                </h1>
                <p className="text-xl text-gray-500 font-medium max-w-3xl mx-auto leading-relaxed">
                    {t('methodology.subtitle')}
                </p>
            </div>

            {/* Main Flow */}
            <div className="grid lg:grid-cols-3 gap-8 relative">
                {/* Connection Arrows (Desktop) */}
                <div className="hidden lg:block absolute top-1/2 left-1/3 -translate-y-1/2 z-0">
                    <svg className="w-24 h-8 text-indigo-200 animate-pulse" fill="none" viewBox="0 0 100 30">
                        <path stroke="currentColor" strokeWidth="4" strokeLinecap="round" d="M10 15h80m-15-10l15 10-15 10" />
                    </svg>
                </div>
                <div className="hidden lg:block absolute top-1/2 left-2/3 -translate-y-1/2 z-0">
                    <svg className="w-24 h-8 text-teal-200 animate-pulse" fill="none" viewBox="0 0 100 30">
                        <path stroke="currentColor" strokeWidth="4" strokeLinecap="round" d="M10 15h80m-15-10l15 10-15 10" />
                    </svg>
                </div>

                {stages.map((stage, i) => (
                    <div key={stage.id} className="relative z-10 group">
                        <div className={`glass-panel p-10 h-full border border-white/40 shadow-xl group-hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 relative overflow-hidden`}>
                            {/* Subtle background gradient */}
                            <div className={`absolute -right-12 -top-12 w-48 h-48 rounded-full blur-3xl opacity-10 bg-gradient-to-br ${i === 0 ? 'from-blue-500' : i === 1 ? 'from-indigo-500' : 'from-teal-500'
                                }`} />

                            <div className="space-y-8">
                                <div className="w-20 h-20 rounded-2xl bg-gray-50 flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform duration-500">
                                    {stage.icon}
                                </div>

                                <h2 className="text-2xl font-black text-gray-900 uppercase tracking-wide">
                                    {stage.title}
                                </h2>

                                <ul className="space-y-4">
                                    {stage.items.map((item, idx) => (
                                        <li key={idx} className="flex items-center gap-3 text-gray-600 font-bold group/item">
                                            <div className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-blue-400' : i === 1 ? 'bg-indigo-400' : 'bg-teal-400'
                                                } group-hover/item:scale-150 transition-transform`} />
                                            <span className="group-hover/item:text-gray-900 transition-colors uppercase text-xs tracking-widest">
                                                {item}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer Info */}
            <div className="glass-panel p-10 bg-gradient-to-r from-gray-900 to-indigo-950 text-white border-none shadow-2xl relative overflow-hidden">
                <div className="absolute right-0 top-0 w-1/2 h-full bg-gradient-to-l from-white/5 to-transparent skew-x-12 translate-x-1/4" />
                <div className="relative z-10 space-y-4 max-w-2xl">
                    <h3 className="text-2xl font-black italic">
                        {t('common.stay_strong')}
                    </h3>
                    <p className="text-gray-300 font-medium leading-relaxed">
                        {t('methodology.subtitle')}
                    </p>
                </div>
            </div>
        </div>
    );
}
