'use client';

import { motion } from 'framer-motion';

interface Score {
    global: number;
    conformity: number;
    balance: number;
    clarity: number;
    details: {
        total_clauses: number;
        high_risks: number;
        medium_risks: number;
        low_risks: number;
    };
}

interface ScoreCardProps {
    score: Score;
}

export function ScoreCard({ score }: ScoreCardProps) {
    const getScoreColor = (value: number) => {
        if (value >= 80) return 'text-green-600';
        if (value >= 60) return 'text-amber-600';
        return 'text-red-600';
    };

    const getScoreBg = (value: number) => {
        if (value >= 80) return 'bg-green-500';
        if (value >= 60) return 'bg-amber-500';
        return 'bg-red-500';
    };

    const getScoreLabel = (value: number) => {
        if (value >= 80) return 'Excellent';
        if (value >= 60) return 'Acceptable';
        return 'À risque';
    };

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">
            <h2 className="text-2xl font-bold text-primary-900 mb-6">
                Score d'Analyse IA
            </h2>

            <div className="grid md:grid-cols-2 gap-8">
                {/* Score Global */}
                <div className="flex flex-col items-center justify-center">
                    <div className="relative w-48 h-48">
                        {/* Cercle de fond */}
                        <svg className="w-full h-full transform -rotate-90">
                            <circle
                                cx="96"
                                cy="96"
                                r="80"
                                stroke="#e2e8f0"
                                strokeWidth="12"
                                fill="none"
                            />
                            {/* Cercle de progression */}
                            <motion.circle
                                cx="96"
                                cy="96"
                                r="80"
                                stroke="currentColor"
                                strokeWidth="12"
                                fill="none"
                                strokeLinecap="round"
                                className={getScoreColor(score.global)}
                                initial={{ strokeDasharray: "0 502" }}
                                animate={{ strokeDasharray: `${(score.global / 100) * 502} 502` }}
                                transition={{ duration: 1.5, ease: "easeOut" }}
                            />
                        </svg>

                        {/* Score au centre */}
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            <motion.span
                                className={`text-5xl font-bold ${getScoreColor(score.global)}`}
                                initial={{ opacity: 0, scale: 0.5 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.5, duration: 0.5 }}
                            >
                                {score.global}
                            </motion.span>
                            <span className="text-sm text-slate-600 mt-1">/ 100</span>
                            <span className={`text-xs font-bold mt-2 px-3 py-1 rounded-full ${score.global >= 80 ? 'bg-green-100 text-green-700' :
                                    score.global >= 60 ? 'bg-amber-100 text-amber-700' :
                                        'bg-red-100 text-red-700'
                                }`}>
                                {getScoreLabel(score.global)}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Scores détaillés */}
                <div className="space-y-4">
                    {/* Conformité */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-slate-700">
                                ⚖️ Conformité légale
                            </span>
                            <span className={`text-sm font-bold ${getScoreColor(score.conformity)}`}>
                                {score.conformity}%
                            </span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2">
                            <motion.div
                                className={`h-2 rounded-full ${getScoreBg(score.conformity)}`}
                                initial={{ width: 0 }}
                                animate={{ width: `${score.conformity}%` }}
                                transition={{ duration: 1, delay: 0.2 }}
                            />
                        </div>
                    </div>

                    {/* Équilibre */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-slate-700">
                                ⚖️ Équilibre contractuel
                            </span>
                            <span className={`text-sm font-bold ${getScoreColor(score.balance)}`}>
                                {score.balance}%
                            </span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2">
                            <motion.div
                                className={`h-2 rounded-full ${getScoreBg(score.balance)}`}
                                initial={{ width: 0 }}
                                animate={{ width: `${score.balance}%` }}
                                transition={{ duration: 1, delay: 0.4 }}
                            />
                        </div>
                    </div>

                    {/* Clarté */}
                    <div>
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-semibold text-slate-700">
                                📖 Clarté et lisibilité
                            </span>
                            <span className={`text-sm font-bold ${getScoreColor(score.clarity)}`}>
                                {score.clarity}%
                            </span>
                        </div>
                        <div className="w-full bg-slate-200 rounded-full h-2">
                            <motion.div
                                className={`h-2 rounded-full ${getScoreBg(score.clarity)}`}
                                initial={{ width: 0 }}
                                animate={{ width: `${score.clarity}%` }}
                                transition={{ duration: 1, delay: 0.6 }}
                            />
                        </div>
                    </div>

                    {/* Statistiques */}
                    <div className="mt-6 pt-6 border-t border-slate-200">
                        <h4 className="text-sm font-bold text-slate-700 mb-3">Détails de l'analyse</h4>
                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-slate-50 rounded-lg p-3">
                                <p className="text-xs text-slate-600">Total clauses</p>
                                <p className="text-lg font-bold text-slate-900">{score.details.total_clauses}</p>
                            </div>
                            <div className="bg-red-50 rounded-lg p-3">
                                <p className="text-xs text-red-600">Risques élevés</p>
                                <p className="text-lg font-bold text-red-700">{score.details.high_risks}</p>
                            </div>
                            <div className="bg-amber-50 rounded-lg p-3">
                                <p className="text-xs text-amber-600">Risques moyens</p>
                                <p className="text-lg font-bold text-amber-700">{score.details.medium_risks}</p>
                            </div>
                            <div className="bg-green-50 rounded-lg p-3">
                                <p className="text-xs text-green-600">Conformes</p>
                                <p className="text-lg font-bold text-green-700">{score.details.low_risks}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
