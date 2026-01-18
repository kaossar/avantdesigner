import { DetectedClause } from '@/lib/analysis/types';

interface ContractSummaryProps {
    contractType: string;
    contractCategory?: string;
    detectedClauses?: DetectedClause[];
    summary: string;
    entities: {
        montants?: string[];
        dates?: string[];
        durees?: string[];
    };
    metadata: {
        total_clauses: number;
        analyzed_clauses: number;
        cleaning_stats?: {
            reduction_percent: number;
        };
    };
}

export function ContractSummary({ contractType, contractCategory, detectedClauses, summary, entities, metadata }: ContractSummaryProps) {
    return (
        <div className="bg-gradient-to-br from-primary-50 to-blue-50 rounded-2xl shadow-xl border border-primary-200 p-8">
            <h2 className="text-2xl font-bold text-primary-900 mb-6 flex items-center gap-3">
                Résumé Exécutif
                {contractCategory && (
                    <span className="text-sm font-normal text-primary-700 bg-primary-100 px-3 py-1 rounded-full border border-primary-200">
                        {contractCategory}
                    </span>
                )}
            </h2>

            <div className="space-y-6">
                {/* Type de contrat */}
                <div className="bg-white rounded-xl p-4 shadow-sm flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
                    <div>
                        <p className="text-sm text-slate-600 mb-1">Type de contrat détecté</p>
                        <p className="text-xl font-bold text-primary-900">{contractType}</p>
                    </div>
                    {detectedClauses && detectedClauses.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                            {detectedClauses.map((clause, idx) => (
                                <div key={idx} className={`px-3 py-1 rounded-lg text-xs font-bold border flex items-center gap-2 ${clause.risk_level === 'HIGH' ? 'bg-red-50 text-red-700 border-red-200' :
                                        clause.risk_level === 'MEDIUM' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                                            'bg-blue-50 text-blue-700 border-blue-200'
                                    }`}>
                                    <span>{clause.name}</span>
                                    {clause.risk_level === 'HIGH' && <span>🔴</span>}
                                    {clause.risk_level === 'MEDIUM' && <span>⚡</span>}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Résumé IA */}
                <div className="bg-white rounded-xl p-4 shadow-sm">
                    <p className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                        🤖 Analyse IA
                    </p>
                    <p className="text-sm text-slate-800 leading-relaxed">{summary}</p>
                </div>

                {/* Clauses Transversales Détails */}
                {detectedClauses && detectedClauses.length > 0 && (
                    <div className="bg-white rounded-xl p-4 shadow-sm border-l-4 border-l-indigo-500">
                        <p className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
                            🔍 Clauses Transversales Détectées
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {detectedClauses.map((clause, idx) => (
                                <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                                    <div className="flex items-center justify-between mb-1">
                                        <p className="font-semibold text-sm text-slate-900">{clause.name}</p>
                                        <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${clause.risk_level === 'HIGH' ? 'bg-red-100 text-red-700' :
                                                clause.risk_level === 'MEDIUM' ? 'bg-amber-100 text-amber-700' :
                                                    'bg-blue-100 text-blue-700'
                                            }`}>
                                            {clause.risk_level === 'HIGH' ? 'Risque Élevé' :
                                                clause.risk_level === 'MEDIUM' ? 'Vigilance' : 'Info'}
                                        </span>
                                    </div>
                                    <p className="text-xs text-slate-600 italic">
                                        {clause.description}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Entités extraites */}
                {(entities.montants?.length || entities.dates?.length || entities.durees?.length) && (
                    <div className="bg-white rounded-xl p-4 shadow-sm">
                        <p className="text-sm font-semibold text-slate-700 mb-3">
                            📊 Informations clés extraites
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                            {entities.montants && entities.montants.length > 0 && (
                                <div className="bg-green-50 rounded-lg p-3">
                                    <p className="text-xs text-green-600 font-semibold mb-1">💰 Montants</p>
                                    <div className="flex flex-wrap gap-1">
                                        {entities.montants.slice(0, 3).map((montant, i) => (
                                            <span key={i} className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                                                {montant}€
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {entities.dates && entities.dates.length > 0 && (
                                <div className="bg-blue-50 rounded-lg p-3">
                                    <p className="text-xs text-blue-600 font-semibold mb-1">📅 Dates</p>
                                    <div className="flex flex-wrap gap-1">
                                        {entities.dates.slice(0, 3).map((date, i) => (
                                            <span key={i} className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                                {date}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {entities.durees && entities.durees.length > 0 && (
                                <div className="bg-purple-50 rounded-lg p-3">
                                    <p className="text-xs text-purple-600 font-semibold mb-1">⏱️ Durées</p>
                                    <div className="flex flex-wrap gap-1">
                                        {entities.durees.slice(0, 3).map((duree, i) => (
                                            <span key={i} className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                                                {duree}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Métadonnées */}
                <div className="bg-white rounded-xl p-4 shadow-sm">
                    <p className="text-sm font-semibold text-slate-700 mb-3">
                        📈 Statistiques d'analyse
                    </p>
                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <p className="text-xs text-slate-600">Clauses totales</p>
                            <p className="text-lg font-bold text-slate-900">{metadata.total_clauses}</p>
                        </div>
                        <div>
                            <p className="text-xs text-slate-600">Clauses analysées</p>
                            <p className="text-lg font-bold text-slate-900">{metadata.analyzed_clauses}</p>
                        </div>
                        {metadata.cleaning_stats && (
                            <div className="col-span-2">
                                <p className="text-xs text-slate-600">Nettoyage du texte</p>
                                <p className="text-sm text-slate-800">
                                    {metadata.cleaning_stats.reduction_percent.toFixed(1)}% de réduction
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
