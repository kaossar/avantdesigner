'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';

import { DetectedRisk } from '@/lib/analysis/types';

interface RiskSummaryProps {
    risks: DetectedRisk[];
}

export function RiskSummary({ risks }: RiskSummaryProps) {
    const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');

    const filteredRisks = filter === 'all'
        ? risks
        : risks.filter(r => r.severity === filter);

    const getSeverityBadge = (severity: string) => {
        switch (severity) {
            case 'high':
                return { icon: '🔴', text: 'Urgent', class: 'bg-red-100 text-red-800 border-red-300' };
            case 'medium':
                return { icon: '🟡', text: 'Important', class: 'bg-amber-100 text-amber-800 border-amber-300' };
            default:
                return { icon: '🟢', text: 'Mineur', class: 'bg-green-100 text-green-800 border-green-300' };
        }
    };

    const highCount = risks.filter(r => r.severity === 'high').length;
    const mediumCount = risks.filter(r => r.severity === 'medium').length;
    const lowCount = risks.filter(r => r.severity === 'low').length;

    return (
        <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-primary-900">
                    Risques Détectés
                </h2>
                <span className="text-sm text-slate-600">
                    {risks.length} risque{risks.length > 1 ? 's' : ''}
                </span>
            </div>

            {/* Filtres */}
            <div className="flex gap-2 mb-6 flex-wrap">
                <button
                    onClick={() => setFilter('all')}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${filter === 'all'
                        ? 'bg-primary-600 text-white'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        }`}
                >
                    Tous ({risks.length})
                </button>
                <button
                    onClick={() => setFilter('high')}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${filter === 'high'
                        ? 'bg-red-600 text-white'
                        : 'bg-red-50 text-red-700 hover:bg-red-100'
                        }`}
                >
                    🔴 Élevés ({highCount})
                </button>
                <button
                    onClick={() => setFilter('medium')}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${filter === 'medium'
                        ? 'bg-amber-600 text-white'
                        : 'bg-amber-50 text-amber-700 hover:bg-amber-100'
                        }`}
                >
                    🟡 Moyens ({mediumCount})
                </button>
                <button
                    onClick={() => setFilter('low')}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${filter === 'low'
                        ? 'bg-green-600 text-white'
                        : 'bg-green-50 text-green-700 hover:bg-green-100'
                        }`}
                >
                    🟢 Faibles ({lowCount})
                </button>
            </div>

            {/* Liste des risques */}
            {filteredRisks.length === 0 ? (
                <div className="text-center py-12">
                    <p className="text-slate-500">Aucun risque dans cette catégorie</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {filteredRisks.map((risk, index) => {
                        const badge = getSeverityBadge(risk.severity);

                        return (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`border-2 rounded-xl p-4 ${badge.class}`}
                            >
                                <div className="flex items-start gap-4">
                                    <span className="text-2xl">{badge.icon}</span>
                                    <div className="flex-1">
                                        <div className="flex items-center justify-between mb-2">
                                            <h4 className="font-bold text-slate-900">
                                                Clause {risk.clause_number || '?'} - {risk.clause_type || 'Général'}
                                            </h4>
                                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${badge.class}`}>
                                                {badge.text}
                                            </span>
                                        </div>

                                        <p className="text-sm text-slate-700 mb-3 italic">
                                            "{risk.clause_preview || risk.description || '...'}"
                                        </p>

                                        <div className="bg-white/50 rounded-lg p-3 mb-3">
                                            <p className="text-sm font-semibold text-slate-800 mb-1">
                                                ⚠️ Problème détecté :
                                            </p>
                                            <p className="text-sm text-slate-700">{risk.issue || risk.title || 'Risque détecté'}</p>
                                        </div>

                                        <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                                            <p className="text-sm font-semibold text-blue-800 mb-1">
                                                💡 Recommandation :
                                            </p>
                                            <p className="text-sm text-blue-700">{risk.recommendation}</p>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}
