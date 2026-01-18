import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileUploader } from './FileUploader';
import { CameraScanner } from './CameraScanner';
import { DocumentPreview } from './DocumentPreview';
import { AnalysisResults } from '@/components/results/AnalysisResults';
import { Button } from '@/components/ui/Button';
// OCR will be handled by Python AI service
import { AnalysisReport } from '@/lib/analysis/types';

export function UploadSection() {
    const [activeTab, setActiveTab] = useState<'upload' | 'text' | 'camera'>('upload');
    const [step, setStep] = useState<'input' | 'preview' | 'results'>('input');
    const [isProcessing, setIsProcessing] = useState(false);
    const [processingStatus, setProcessingStatus] = useState<string>('');
    const [processingProgress, setProcessingProgress] = useState<number>(0);

    // Data State
    const [file, setFile] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [extractedText, setExtractedText] = useState<string | null>(null);
    const [analysisReport, setAnalysisReport] = useState<AnalysisReport | null>(null);

    const processFile = async (fileObj: File, autoProceed: boolean = false) => {
        setIsProcessing(true);
        setStep('preview');
        setFile(fileObj);

        // Preview Image immediately
        if (fileObj.type.startsWith('image/')) {
            setImagePreview(URL.createObjectURL(fileObj));
        }

        try {
            setExtractedText("Analyse et extraction en cours...");

            const formData = new FormData();
            formData.append('file', fileObj);
            formData.append('contract_type', 'auto');

            // Use the robust file analysis endpoint
            // It handles Native PDF, Scanned PDF (OCR), and Images
            const response = await fetch('/api/ai-upload-analyze', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                // Determine if it's a server error or just OCR failure
                // Prefer 'details' (real backend error) over 'error' (generic proxy message)
                const errorMsg = data.details || data.error || 'Erreur lors de l\'analyse';
                // Try to parse if it looks like JSON (FastAPI detail)
                try {
                    const parsed = JSON.parse(errorMsg);
                    if (parsed.detail) throw new Error(parsed.detail);
                } catch { }
                throw new Error(errorMsg);
            }

            // Update state with result
            const textResult = data.text || "Texte extrait.";
            setExtractedText(textResult);

            if (data.data || data) {
                // Store the report
                setAnalysisReport(data.data || data);

                // Auto-proceed if requested (or we can just wait for user to click 'Audit')
                if (autoProceed) {
                    setTimeout(() => setStep('results'), 500);
                }
            }

        } catch (error) {
            console.error('Processing error:', error);
            let msg = "Erreur lors de l'analyse du fichier.";
            if (error instanceof Error) {
                if (error.message.includes('Failed to fetch')) {
                    msg = "Le serveur ne répond pas (Délai dépassé ou Démarrage en cours). Veuillez réessayez dans 30 secondes.";
                } else {
                    msg = `Erreur: ${error.message}`;
                }
            }
            setExtractedText(msg);
            // Don't show alert if we display the error in the text area
        } finally {
            setIsProcessing(false);
        }
    };

    const processCameraCapture = async (base64Image: string) => {
        setIsProcessing(true);
        setStep('preview');
        setImagePreview(base64Image);

        // Convert base64 to File for backend processing
        const blob = await fetch(base64Image).then(r => r.blob());
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });

        // Use backend API for OCR (Python AI service)
        await processFile(file, false);

        setIsProcessing(false);
    };

    const handleTextSubmit = async (text: string) => {
        setExtractedText(text);
        // Simulate file upload for the API
        const blob = new Blob([text], { type: 'text/plain' });
        const textFile = new File([blob], "contract-text.txt", { type: 'text/plain' });

        // Auto-proceed to results for pasted text
        await processFile(textFile, true);
    };

    const handleAnalyzeClick = () => {
        if (analysisReport) {
            setStep('results');
        } else if (file) {
            // Already handled by processFile called in onFileSelected, 
            // but if user went back or something, we might need logic.
            // Currently processFile does everything. 
            // This button in DocumentPreview is for "Lancer l'audit".
            // If file exists, we probably already have the report OR we need to fetch it?
            // Actually, processFile calls API.
            // If API succeeded, 'analysisReport' is set. 
            // So if we are here and 'analysisReport' is null, that means processFile failed or didn't run?
            // OR processFile only did extraction? (In current logic it does full analysis).

            // Re-run processFile to be safe or just show processing
            alert("Réanalyse en cours...");
            processFile(file, true);
        } else if (extractedText) {
            // Case: Camera Scan or Manual Text (if logic separated)
            // We have text but no file object. We must submit this text as a file.
            handleTextSubmit(extractedText);
        }
    };

    const reset = () => {
        setStep('input');
        setFile(null);
        setImagePreview(null);
        setExtractedText(null);
        setAnalysisReport(null);
    };

    return (
        <div className="max-w-4xl mx-auto w-full">
            {/* Tabs Navigation (Only visible in input mode) */}
            {step === 'input' && (
                <div className="flex justify-center mb-10">
                    <div className="bg-slate-100 p-1 rounded-xl inline-flex">
                        {[
                            { id: 'upload', label: 'Upload Fichier', icon: '📄' },
                            { id: 'text', label: 'Coller Texte', icon: '📝' },
                            { id: 'camera', label: 'Scan Caméra', icon: '📷' }
                        ].map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id as any)}
                                className={`
                                    flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-bold uppercase tracking-wider transition-all
                                    ${activeTab === tab.id
                                        ? 'bg-white text-primary-900 shadow-md transform scale-105'
                                        : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50'
                                    }
                                `}
                            >
                                <span>{tab.icon}</span>
                                <span className="hidden sm:inline">{tab.label}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Content Area */}
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 min-h-[400px] flex flex-col items-center justify-center relative overflow-hidden">
                {/* Decorative background blur */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary-50 rounded-full filter blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

                <div className="relative z-10 w-full">
                    {step === 'results' && analysisReport ? (
                        <AnalysisResults
                            report={analysisReport}
                            onReset={reset}
                        />
                    ) : step === 'preview' ? (
                        <DocumentPreview
                            fileObject={file}
                            imageSrc={imagePreview}
                            extractedText={extractedText}
                            isScanning={isProcessing}
                            onAnalyze={handleAnalyzeClick}
                            onReset={reset}
                        />
                    ) : (
                        <>
                            {activeTab === 'upload' && (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <FileUploader onFileSelected={processFile} />
                                </motion.div>
                            )}

                            {activeTab === 'text' && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="w-full"
                                >
                                    <textarea
                                        className="w-full h-80 p-6 rounded-xl border border-slate-300 focus:border-primary-500 focus:ring-4 focus:ring-primary-100 outline-none resize-none font-mono text-sm leading-relaxed text-slate-700"
                                        placeholder="Collez le texte de votre contrat ici..."
                                        onChange={(e) => setExtractedText(e.target.value)}
                                    />
                                    <div className="mt-6 text-right">
                                        <Button size="lg" onClick={() => extractedText && handleTextSubmit(extractedText)}>
                                            Analyser le texte
                                        </Button>
                                    </div>
                                </motion.div>
                            )}

                            {activeTab === 'camera' && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="w-full"
                                >
                                    <CameraScanner
                                        onCapture={processCameraCapture}
                                        onCancel={() => setActiveTab('upload')}
                                    />
                                </motion.div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
