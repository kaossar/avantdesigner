'use client';

interface ContractSummaryProps {
    contractType: string;
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

export function ContractSummary({ contractType, summary, entities, metadata }: ContractSummaryProps) {
    return (
        <div className="bg-gradient-to-br from-primary-50 to-blue-50 rounded-2xl shadow-xl border border-primary-200 p-8">
            <h2 className="text-2xl font-bold text-primary-900 mb-6">
                Résumé Exécutif
            </h2>

            <div className="space-y-6">
                {/* Type de contrat */}
                <div className="bg-white rounded-xl p-4 shadow-sm">
                    <p className="text-sm text-slate-600 mb-1">Type de contrat détecté</p>
                    <p className="text-xl font-bold text-primary-900">{contractType}</p>
                </div>

                {/* Résumé IA */}
                <div className="bg-white rounded-xl p-4 shadow-sm">
                    <p className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                        🤖 Analyse IA
                    </p>
                    <p className="text-sm text-slate-800 leading-relaxed">{summary}</p>
                </div>

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
