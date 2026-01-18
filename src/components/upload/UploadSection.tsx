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
    const [isAnalyzing, setIsAnalyzing] = useState(false); // NEW: separate state for AI analysis
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
            setExtractedText("Connexion au serveur...");

            const formData = new FormData();
            formData.append('file', fileObj);

            // Use OCR-only endpoint
            const response = await fetch('/api/ai-extract-text', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Erreur serveur: ${response.status}`);
            }

            if (!response.body) throw new Error("Réponse vide du serveur");

            // Streaming Reader Logic
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let fullTextLog = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                // Improved Split (handles \r\n from Windows backend)
                const lines = buffer.split(/\r?\n/);
                buffer = lines.pop() || ''; // Keep incomplete line in buffer

                for (let line of lines) {
                    line = line.trim();
                    if (!line) continue;

                    // Robust helper to handle concatenated JSONs (e.g. obj1}{obj2) if backend flush misses \n
                    const fixConcatenated = (str: string) => {
                        if (str.includes('}{')) {
                            return str.replace(/}{/g, '}\n{').split('\n');
                        }
                        return [str];
                    };

                    const parts = fixConcatenated(line);

                    for (const part of parts) {
                        try {
                            const msg = JSON.parse(part);

                            switch (msg.type) {
                                case 'init':
                                    setExtractedText(msg.message);
                                    break;
                                case 'page_start':
                                    setExtractedText(current => `${current}\n⏳ ${msg.message}`);
                                    break;
                                case 'page_done':
                                    setExtractedText(current => `${current} ✅ (Terminé)\n`);
                                    break;
                                case 'ocr_warning':
                                case 'page_warning':
                                    setExtractedText(current => `${current} ⚠️ ${msg.message}\n`);
                                    break;
                                case 'ocr_complete':
                                    fullTextLog = msg.full_text; // Keep text separately
                                    setExtractedText(fullTextLog); // Show complete OCR text
                                    break;
                                case 'info':
                                case 'stage':
                                    setExtractedText(current => `${current}\nℹ️ ${msg.message}`);
                                    break;
                                case 'complete':
                                    // OCR complete - text is ready for analysis
                                    setExtractedText(fullTextLog || "Texte extrait.");
                                    break;
                                case 'error':
                                    throw new Error(msg.error);
                            }
                        } catch (err) {
                            console.error("❌ Error parsing stream part:", part, err);
                            console.error("   Original line was:", line);
                            // Don't throw - continue processing other messages
                        }
                    }
                }
            }

            // OCR complete - don't auto-proceed to analysis
            // User must click "Lancer l'analyse" button

        } catch (error) {
            console.error('Processing error:', error);
            let msg = "Erreur lors de l'extraction du texte.";
            if (error instanceof Error) {
                if (error.message.includes('fetch')) {
                    msg = "Le serveur ne répond pas. Vérifiez la connexion.";
                } else {
                    msg = `Erreur: ${error.message}`;
                }
            }
            setExtractedText(msg);
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

    const handleAnalyzeClick = async () => {
        if (analysisReport) {
            // Already analyzed - just show results
            setStep('results');
            return;
        }

        if (!extractedText || !extractedText.trim()) {
            alert("Aucun texte à analyser. Veuillez d'abord extraire le texte d'un document.");
            return;
        }

        try {
            setIsAnalyzing(true);
            setExtractedText(current => `${current}\n\n🧠 Lancement de l'analyse IA...`);

            // Send extracted text to AI analysis endpoint
            const response = await fetch('/api/ai-analyze-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: extractedText,
                    contract_type: 'auto',
                }),
            });

            if (!response.ok) {
                throw new Error(`Erreur serveur: ${response.status}`);
            }

            const result = await response.json();

            // Set analysis results
            setAnalysisReport(result);
            setExtractedText(current => `${current}\n✅ Analyse terminée avec succès !`);

            // Auto-proceed to results
            setTimeout(() => setStep('results'), 800);

        } catch (error) {
            console.error('Analysis error:', error);
            let msg = "\n\n❌ Erreur lors de l'analyse IA.";
            if (error instanceof Error) {
                msg += ` ${error.message}`;
            }
            setExtractedText(current => `${current}${msg}`);
        } finally {
            setIsAnalyzing(false);
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
                            isAnalyzing={isAnalyzing}
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
