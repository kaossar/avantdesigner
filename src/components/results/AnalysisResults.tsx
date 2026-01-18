'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { ScoreCard } from '@/components/analysis/ScoreCard';
import { ContractSummary } from '@/components/analysis/ContractSummary';
import { RiskSummary } from '@/components/analysis/RiskSummary';
import { ClauseByClauseView } from '@/components/analysis/ClauseByClauseView';
import { AnalysisReport } from '@/lib/analysis/types';
import { ArrowLeft, Download, Share2, Loader2 } from 'lucide-react';

interface AnalysisResultsProps {
    report: AnalysisReport;
    onReset: () => void;
}

export function AnalysisResults({ report, onReset }: AnalysisResultsProps) {
    const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
    const [pdfError, setPdfError] = useState<string | null>(null);

    // Transform report data to match expert component interfaces
    const score = {
        global: report.score?.total || 0,
        conformity: report.score?.conformity || 85,
        balance: report.score?.balance || 80,
        clarity: report.score?.clarity || 75,
        details: {
            total_clauses: report.clauses?.length || 0,
            high_risks: report.risks?.filter(r => r.severity === 'high').length || 0,
            medium_risks: report.risks?.filter(r => r.severity === 'medium').length || 0,
            low_risks: report.clauses?.filter(c => c.risk_level === 'low').length || 0,
        }
    };

    const contractType = report.contractType || 'Contrat';
    const contractCategory = report.contractCategory || '';
    const detectedClauses = report.detected_clauses || [];
    const summary = report.summary || 'Analyse terminée avec succès.';
    const entities = report.entities || { montants: [], dates: [], durees: [] };
    const metadata = {
        total_clauses: report.clauses?.length || 0,
        analyzed_clauses: report.clauses?.length || 0,
        cleaning_stats: report.metadata?.cleaning_stats
    };

    const handleExportPdf = async () => {
        setIsGeneratingPDF(true);
        setPdfError(null);

        try {
            // Prepare analysis data for PDF export
            const analysisData = {
                contract_type: contractType,
                score: {
                    global: score.global,
                    conformite: score.conformity,
                    equilibre: score.balance,
                    clarte: score.clarity
                },
                clauses: report.clauses || [],
                risks: report.risks || [],
                entities: entities,
                metadata: {
                    ...metadata,
                    search_method: 'semantic' // From RAG
                }
            };

            // Call Next.js Proxy API
            const response = await fetch('/api/export-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(analysisData)
            });

            if (!response.ok) {
                throw new Error(`PDF generation failed: ${response.statusText}`);
            }

            // Get PDF blob
            const blob = await response.blob();

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `rapport_analyse_${contractType.replace(/\s+/g, '_')}_${Date.now()}.pdf`;
            document.body.appendChild(a);
            a.click();

            // Cleanup
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

        } catch (error) {
            console.error('PDF generation error:', error);
            setPdfError(error instanceof Error ? error.message : 'Erreur lors de la génération du PDF');
        } finally {
            setIsGeneratingPDF(false);
        }
    };

    const handleShare = () => {
        // TODO: Implement share functionality
        alert('Partage - Fonctionnalité à venir');
    };

    const scrollToSection = (id: string) => {
        const element = document.getElementById(id);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    return (
        <div className="w-full space-y-8 animate-fadeIn relative">
            {/* Header with Actions */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 print:hidden">
                <div>
                    <h1 className="text-3xl font-bold text-primary-900">
                        Analyse Expert IA
                    </h1>
                    <p className="text-slate-600 mt-1">
                        Résultats détaillés de l'analyse de votre contrat
                    </p>
                </div>
                <div className="flex gap-3 flex-wrap">
                    <Button variant="ghost" onClick={onReset}>
                        <ArrowLeft size={16} className="mr-2" />
                        Nouvelle analyse
                    </Button>
                    <Button variant="secondary" onClick={handleShare} className="hidden sm:flex">
                        <Share2 size={16} className="mr-2" />
                        Partager
                    </Button>
                    <Button variant="secondary" onClick={handleExportPdf} disabled={isGeneratingPDF}>
                        {isGeneratingPDF ? (
                            <>
                                <Loader2 size={16} className="mr-2 animate-spin" />
                                Génération...
                            </>
                        ) : (
                            <>
                                <Download size={16} className="mr-2" />
                                PDF
                            </>
                        )}
                    </Button>
                </div>
            </div>

            {/* Sticky Navigation */}
            <div className="sticky top-0 z-50 bg-white/80 backdrop-blur-md shadow-sm border-b border-slate-200 -mx-4 px-4 py-2 overflow-x-auto print:hidden">
                <div className="flex gap-2 min-w-max">
                    <button onClick={() => scrollToSection('score')} className="px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-primary-600 hover:bg-slate-100 rounded-lg transition-colors">
                        📊 Score
                    </button>
                    <button onClick={() => scrollToSection('summary')} className="px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-primary-600 hover:bg-slate-100 rounded-lg transition-colors">
                        📝 Résumé
                    </button>
                    <button onClick={() => scrollToSection('risks')} className="px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-primary-600 hover:bg-slate-100 rounded-lg transition-colors">
                        ⚠️ Risques ({score.details.high_risks + score.details.medium_risks})
                    </button>
                    <button onClick={() => scrollToSection('clauses')} className="px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-primary-600 hover:bg-slate-100 rounded-lg transition-colors">
                        🔍 Clauses ({score.details.total_clauses})
                    </button>
                    {report.recommendations && report.recommendations.length > 0 && (
                        <button onClick={() => scrollToSection('recommendations')} className="px-3 py-1.5 text-sm font-medium text-slate-700 hover:text-primary-600 hover:bg-slate-100 rounded-lg transition-colors">
                            💡 Conseils
                        </button>
                    )}
                </div>
            </div>

            {/* Score Card */}
            <div id="score" className="scroll-mt-24">
                <ScoreCard score={score} />
            </div>

            {/* Contract Summary */}
            <div id="summary" className="scroll-mt-24">
                <ContractSummary
                    contractType={contractType}
                    contractCategory={contractCategory}
                    detectedClauses={detectedClauses}
                    summary={summary}
                    entities={entities}
                    metadata={metadata}
                />
            </div>

            {/* Risk Summary */}
            {report.risks && report.risks.length > 0 && (
                <div id="risks" className="scroll-mt-24">
                    <RiskSummary risks={report.risks} />
                </div>
            )}

            {/* Clause by Clause Analysis */}
            {report.clauses && report.clauses.length > 0 && (
                <div id="clauses" className="scroll-mt-24">
                    <ClauseByClauseView clauses={report.clauses} />
                </div>
            )}

            {/* Recommendations */}
            {report.recommendations && report.recommendations.length > 0 && (
                <div id="recommendations" className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 scroll-mt-24">
                    <h2 className="text-2xl font-bold text-primary-900 mb-6">
                        Recommandations IA
                    </h2>
                    <div className="space-y-4">
                        {report.recommendations.map((rec, index) => (
                            <div
                                key={index}
                                className={`border-l-4 rounded-lg p-4 ${rec.priority === 'urgent' ? 'border-red-500 bg-red-50' :
                                    rec.priority === 'important' ? 'border-amber-500 bg-amber-50' :
                                        'border-blue-500 bg-blue-50'
                                    }`}
                            >
                                <p className="font-bold text-sm mb-1">
                                    {rec.priority === 'urgent' ? '🔴 Urgent' :
                                        rec.priority === 'important' ? '🟡 Important' :
                                            '🔵 Information'}
                                </p>
                                <p className="font-semibold text-slate-900">{rec.action}</p>
                                <p className="text-sm text-slate-700 mt-1">{rec.detail}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Legal Disclaimer */}
            <div className="p-6 bg-blue-50 border border-blue-100 rounded-xl text-center">
                <h4 className="text-blue-900 font-bold mb-2">⚖️ Avertissement juridique</h4>
                <p className="text-blue-700 text-sm mb-4">
                    Cette analyse automatique par IA ne remplace pas l'avis d'un professionnel du droit.
                    Pour toute question juridique, consultez un avocat.
                </p>
                <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-md">
                    Parler à un expert juridique
                </Button>
            </div>

            {/* Bottom Actions */}
            <div className="flex gap-4 justify-center pt-8 print:hidden">
                <Button size="lg" onClick={onReset}>
                    Analyser un autre contrat
                </Button>
                <Button size="lg" variant="outline" onClick={handleExportPdf}>
                    📄 Exporter en PDF
                </Button>
            </div>
        </div>
    );
}
