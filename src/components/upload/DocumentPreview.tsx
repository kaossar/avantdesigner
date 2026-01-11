import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';

interface DocumentPreviewProps {
    fileObject?: File | null;
    imageSrc?: string | null;
    extractedText: string | null;
    isScanning: boolean;
    onAnalyze: () => void;
    onReset: () => void;
}

export function DocumentPreview({
    fileObject,
    imageSrc,
    extractedText,
    isScanning,
    onAnalyze,
    onReset
}: DocumentPreviewProps) {
    if (isScanning) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <div className="relative w-24 h-24 mb-8">
                    <div className="absolute inset-0 border-4 border-slate-100 rounded-full"></div>
                    <div className="absolute inset-0 border-4 border-primary-600 rounded-full border-t-transparent animate-spin"></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <svg className="w-8 h-8 text-primary-600 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    </div>
                </div>
                <h3 className="text-xl font-serif font-bold text-primary-900 mb-2 animate-pulse">Lecture en cours...</h3>
                <p className="text-slate-500">Notre IA déchiffre votre document.</p>
            </div>
        );
    }

    return (
        <div className="w-full">
            <div className="flex flex-col md:flex-row gap-8 bg-slate-50 rounded-xl p-6 border border-slate-200">
                {/* Visual Preview */}
                <div className="w-full md:w-1/3 flex flex-col gap-4">
                    <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm aspect-[3/4] flex items-center justify-center overflow-hidden">
                        {imageSrc ? (
                            <img src={imageSrc} alt="Preview" className="w-full h-full object-contain" />
                        ) : (
                            <div className="text-center">
                                <div className="w-16 h-16 bg-primary-50 rounded-lg mx-auto mb-4 flex items-center justify-center text-primary-600">
                                    <span className="font-bold text-xl uppercase">{fileObject?.name.split('.').pop()}</span>
                                </div>
                                <p className="text-sm font-bold text-slate-700 truncate max-w-[150px]">{fileObject?.name}</p>
                                <p className="text-xs text-slate-400 mt-1">{(fileObject?.size ? fileObject.size / 1024 : 0).toFixed(0)} KB</p>
                            </div>
                        )}
                    </div>
                    <Button variant="outline" fullWidth size="sm" onClick={onReset} className="text-slate-500">
                        Changer de fichier
                    </Button>
                </div>

                {/* Text / Actions */}
                <div className="w-full md:w-2/3 flex flex-col">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-primary-900">Contenu détecté</h3>
                        <div className="bg-emerald-100 text-emerald-800 text-[10px] uppercase font-bold px-2 py-1 rounded">
                            Scan réussi
                        </div>
                    </div>

                    <div className="flex-1 bg-white border border-slate-200 rounded-lg p-4 mb-6 shadow-inner max-h-[300px] overflow-y-auto">
                        <p className="text-sm text-slate-600 font-mono whitespace-pre-wrap leading-relaxed">
                            {extractedText
                                ? extractedText.slice(0, 500) + (extractedText.length > 500 ? '...' : '')
                                : "Aucun texte détecté. Le document semble être une image sans texte lisible."
                            }
                        </p>
                    </div>

                    <div className="bg-primary-50 border border-primary-100 rounded-lg p-4 mb-6 flex gap-4 items-start">
                        <svg className="w-5 h-5 text-primary-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm text-primary-900">
                            Vérifiez que le texte ci-dessus correspond bien à votre contrat. Si tout est correct, lancez l'analyse juridique.
                        </p>
                    </div>

                    <Button onClick={onAnalyze} size="lg" fullWidth className="shadow-lg shadow-primary-900/20">
                        Lancer l'audit juridique (IA)
                    </Button>
                </div>
            </div>
        </div>
    );
}
