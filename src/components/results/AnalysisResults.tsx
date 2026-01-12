import { useRef, useState } from 'react';
import { AnalysisReport } from '@/lib/analysis/types';
import { ScoreGauge } from './ScoreGauge';
import { RiskCard } from './RiskCard';
import { Button } from '@/components/ui/Button';
import { ArrowLeft, Share2, Download, Loader2 } from 'lucide-react';
import { generatePdf } from '@/lib/pdf/generator';

interface AnalysisResultsProps {
    report: AnalysisReport;
    onReset: () => void;
}

export function AnalysisResults({ report, onReset }: AnalysisResultsProps) {
    const riskCount = report.risks.length;
    const [isExporting, setIsExporting] = useState(false);

    // Sort risks: Critical first, then High, etc.
    const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
    const sortedRisks = [...report.risks].sort((a, b) =>
        (severityOrder[a.severity] ?? 4) - (severityOrder[b.severity] ?? 4)
    );

    const handleDownloadPdf = async () => {
        setIsExporting(true);
        try {
            await generatePdf('analysis-report-content', `Rapport-AvantDeSigner-${report.contractType}.pdf`);
        } catch (error) {
            console.error("Export failed", error);
            alert("Erreur lors de la génération du PDF.");
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <div id="analysis-report-content" className="w-full max-w-4xl mx-auto space-y-8 animate-fadeIn p-4 md:p-8 bg-white md:bg-transparent">

            {/* Top Bar with consistent Buttons */}
            <div className="flex items-center justify-between mb-6 print:hidden">
                <Button
                    variant="ghost"
                    onClick={onReset}
                    className="text-slate-500 hover:text-slate-900"
                >
                    <ArrowLeft size={16} className="mr-2" />
                    Nouvelle analyse
                </Button>
                <div className="flex gap-2">
                    <Button variant="secondary" size="sm" className="hidden sm:flex">
                        <Share2 size={16} className="mr-2" /> Partager
                    </Button>
                    <Button
                        variant="secondary"
                        size="sm"
                        onClick={handleDownloadPdf}
                        disabled={isExporting}
                    >
                        {isExporting ? <Loader2 size={16} className="mr-2 animate-spin" /> : <Download size={16} className="mr-2" />}
                        {isExporting ? 'Génération...' : 'PDF'}
                    </Button>
                </div>
            </div>

            {/* Score & Summary Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">

                {/* Left: Gauge */}
                <div className="col-span-1 border-r border-slate-100 flex justify-center">
                    <ScoreGauge score={report.score.total} />
                </div>

                {/* Right: Summary Text - Simplified */}
                <div className="col-span-2 space-y-4">
                    <div>
                        <h2 className="text-2xl font-bold text-slate-900 mb-2">
                            Résultats de l'analyse
                        </h2>
                        {/* Removed redundant text about detected risks, as it's shown below */}
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-slate-500">Confiance IA :</span>
                            <div className="h-2 flex-1 bg-slate-100 rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-blue-600 rounded-full"
                                    style={{ width: `${report.score.total}%` }}
                                />
                            </div>
                            <span className="font-bold text-slate-900">{report.score.total}/100</span>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mt-4">
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <div className="text-slate-500 text-xs font-semibold uppercase">Contrat</div>
                            <div className="text-slate-900 font-medium capitalize mt-1">
                                {report.contractType === 'housing' ? 'Bail d\'habitation' : report.contractType}
                            </div>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <div className="text-slate-500 text-xs font-semibold uppercase">Risques</div>
                            <div className="text-slate-900 font-medium mt-1">
                                {riskCount > 0 ? `${riskCount} détecté${riskCount > 1 ? 's' : ''}` : 'Aucun'}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Risk List */}
            <div className="space-y-4">
                <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    Détails des points de vigilance
                </h3>

                {sortedRisks.length > 0 ? (
                    <div className="space-y-4">
                        {sortedRisks.map((risk) => (
                            <RiskCard key={risk.id} risk={risk} />
                        ))}
                    </div>
                ) : (
                    <div className="p-12 text-center bg-green-50 rounded-xl border border-green-100">
                        <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4 text-green-600 text-2xl">
                            🎉
                        </div>
                        <h3 className="text-lg font-bold text-green-900 mb-2">Tout semble correct</h3>
                        <p className="text-green-700">
                            Aucun risque majeur n'a été détecté par nos algorithmes.
                        </p>
                    </div>
                )}
            </div>

            <div className="p-6 bg-blue-50 border border-blue-100 rounded-xl text-center">
                <h4 className="text-blue-900 font-bold mb-2">Question juridique ?</h4>
                <p className="text-blue-700 text-sm mb-4">
                    Cette analyse automatique ne remplace pas l'avis d'un professionnel.
                </p>
                <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-md">
                    Parler à un expert
                </Button>
            </div>
        </div>
    );
}
