'use client';

import { motion } from 'framer-motion';

interface Clause {
    clause_number: number;
    clause_text: string;
    clause_type: string;
    resume: string;
    implications: string;
    risques: string;
    conformite: string;
    recommandation: string;
    risk_level: 'low' | 'medium' | 'high';
    legal_references?: Array<{
        source: string;
        article: string;
        title: string;
        summary: string;
        relevance?: string;
    }>;
    legal_context?: string;
    search_method?: string;
}

interface ClauseByClauseViewProps {
    clauses: Clause[];
}

export function ClauseByClauseView({ clauses }: ClauseByClauseViewProps) {
    const getRiskColor = (level: string) => {
        switch (level) {
            case 'high': return 'bg-red-50 border-red-300';
            case 'medium': return 'bg-amber-50 border-amber-300';
            default: return 'bg-green-50 border-green-300';
        }
    };

    const getRiskIcon = (level: string) => {
        switch (level) {
            case 'high': return '🔴';
            case 'medium': return '🟡';
            default: return '🟢';
        }
    };

    const getRiskBadge = (level: string) => {
        switch (level) {
            case 'high': return { text: 'Risque élevé', class: 'bg-red-200 text-red-800' };
            case 'medium': return { text: 'Attention', class: 'bg-amber-200 text-amber-800' };
            default: return { text: 'Conforme', class: 'bg-green-200 text-green-800' };
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'financial': return '💰';
            case 'termination': return '🚪';
            case 'duration': return '⏱️';
            case 'guarantee': return '🛡️';
            case 'obligation': return '📋';
            default: return '📄';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-primary-900">
                    Analyse Clause par Clause
                </h2>
                <p className="text-sm text-slate-600">
                    {clauses.length} clause{clauses.length > 1 ? 's' : ''} analysée{clauses.length > 1 ? 's' : ''}
                </p>
            </div>

            {clauses.map((clause, index) => {
                const badge = getRiskBadge(clause.risk_level);

                return (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className={`border-2 rounded-xl p-6 ${getRiskColor(clause.risk_level)} transition-all hover:shadow-lg`}
                    >
                        {/* En-tête */}
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center gap-3">
                                <span className="text-2xl">{getRiskIcon(clause.risk_level)}</span>
                                <div>
                                    <h3 className="text-lg font-bold text-slate-900">
                                        Clause {clause.clause_number}
                                    </h3>
                                    <div className="flex items-center gap-2 mt-1">
                                        <span className="text-sm text-slate-600">
                                            {getTypeIcon(clause.clause_type)} {clause.clause_type}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${badge.class}`}>
                                {badge.text}
                            </span>
                        </div>

                        {/* Texte original */}
                        <div className="bg-white/70 rounded-lg p-4 mb-4 border border-slate-200">
                            <p className="text-sm text-slate-700 italic leading-relaxed">
                                "{clause.clause_text}"
                            </p>
                        </div>

                        {/* Analyse IA */}
                        <div className="space-y-3">
                            {/* Résumé */}
                            <div className="bg-white/50 rounded-lg p-3">
                                <h4 className="font-bold text-sm text-slate-700 mb-1 flex items-center gap-2">
                                    💡 En clair
                                </h4>
                                <p className="text-sm text-slate-800">{clause.resume}</p>
                            </div>

                            {/* Implications */}
                            <div className="bg-white/50 rounded-lg p-3">
                                <h4 className="font-bold text-sm text-slate-700 mb-1 flex items-center gap-2">
                                    📋 Implications
                                </h4>
                                <p className="text-sm text-slate-800">{clause.implications}</p>
                            </div>

                            {/* Risques */}
                            {clause.risques && (
                                <div className={`rounded-lg p-3 ${clause.risk_level === 'high' ? 'bg-red-100/50' :
                                    clause.risk_level === 'medium' ? 'bg-amber-100/50' :
                                        'bg-green-100/50'
                                    }`}>
                                    <h4 className="font-bold text-sm mb-1 flex items-center gap-2">
                                        ⚠️ Risques
                                    </h4>
                                    <p className="text-sm">{clause.risques}</p>
                                </div>
                            )}

                            {/* Conformité */}
                            <div className="bg-white/50 rounded-lg p-3">
                                <h4 className="font-bold text-sm text-slate-700 mb-1 flex items-center gap-2">
                                    ⚖️ Conformité légale
                                </h4>
                                <p className="text-sm text-slate-800">{clause.conformite}</p>
                            </div>

                            {/* Recommandation */}
                            {clause.recommandation && (
                                <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
                                    <h4 className="font-bold text-sm text-blue-700 mb-1 flex items-center gap-2">
                                        ✨ Recommandation IA
                                    </h4>
                                    <p className="text-sm text-blue-800">{clause.recommandation}</p>
                                </div>
                            )}

                            {/* Références Légales RAG */}
                            {clause.legal_references && clause.legal_references.length > 0 && (
                                <div className="bg-purple-50 rounded-lg p-3 border border-purple-200">
                                    <div className="flex items-center justify-between mb-2">
                                        <h4 className="font-bold text-sm text-purple-700 flex items-center gap-2">
                                            📚 Références Légales
                                        </h4>
                                        {clause.search_method && (
                                            <span className="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-purple-600">
                                                {clause.search_method === 'semantic' ? '🧠 Recherche sémantique' : '🔍 Recherche keywords'}
                                            </span>
                                        )}
                                    </div>
                                    <div className="space-y-2">
                                        {clause.legal_references.map((ref, idx) => (
                                            <div key={idx} className="bg-white/70 rounded p-2 border border-purple-100">
                                                <div className="flex items-start justify-between gap-2">
                                                    <div className="flex-1">
                                                        <p className="text-xs font-bold text-purple-900">
                                                            {ref.source} {ref.article}
                                                        </p>
                                                        <p className="text-xs text-purple-700 mt-0.5">
                                                            {ref.title}
                                                        </p>
                                                        <p className="text-xs text-slate-600 mt-1 italic">
                                                            {ref.summary}
                                                        </p>
                                                    </div>
                                                    {ref.relevance && (
                                                        <span className="text-xs font-bold text-purple-600 whitespace-nowrap">
                                                            {ref.relevance}
                                                        </span>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </motion.div>
                );
            })}
        </div>
    );
}
