import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileUploader } from './FileUploader';
import { CameraScanner } from './CameraScanner';
import { DocumentPreview } from './DocumentPreview';
import { Button } from '@/components/ui/Button';
import { OcrService } from '@/lib/ocr/tesseract';

export function UploadSection() {
    const [activeTab, setActiveTab] = useState<'upload' | 'text' | 'camera'>('upload');
    const [step, setStep] = useState<'input' | 'preview'>('input');
    const [isProcessing, setIsProcessing] = useState(false);

    // Data State
    const [file, setFile] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [extractedText, setExtractedText] = useState<string | null>(null);

    const processFile = async (fileObj: File) => {
        setIsProcessing(true);
        setStep('preview');
        setFile(fileObj);

        // Create preview URL
        if (fileObj.type.startsWith('image/')) {
            setImagePreview(URL.createObjectURL(fileObj));
            // OCR
            try {
                const result = await OcrService.scanImage(fileObj);
                setExtractedText(result.text);
            } catch (e) {
                console.error("OCR Failed", e);
                setExtractedText("Erreur de lecture OCR.");
            }
        } else {
            // PDF/DOCX handling would go here (mock for now)
            setExtractedText("Contenu du fichier " + fileObj.name + " extrait avec succès (Simulation).");
        }

        setIsProcessing(false);
    };

    const processCameraCapture = async (base64Image: string) => {
        setIsProcessing(true);
        setStep('preview');
        setImagePreview(base64Image);

        try {
            const result = await OcrService.scanBase64(base64Image);
            setExtractedText(result.text);
        } catch (e) {
            console.error("OCR Failed", e);
            setExtractedText("Erreur de lecture OCR.");
        }

        setIsProcessing(false);
    };

    const handleTextSubmit = (text: string) => {
        setExtractedText(text);
        setStep('preview');
    };

    const reset = () => {
        setStep('input');
        setFile(null);
        setImagePreview(null);
        setExtractedText(null);
    };

    return (
        <div className="max-w-4xl mx-auto w-full">
            {/* Tabs Navigation */}
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

            {/* Content Area */}
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 min-h-[400px] flex flex-col items-center justify-center relative overflow-hidden">
                {/* Decorative background blur */}
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary-50 rounded-full filter blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

                <div className="relative z-10 w-full">
                    {step === 'preview' ? (
                        <DocumentPreview
                            fileObject={file}
                            imageSrc={imagePreview}
                            extractedText={extractedText}
                            isScanning={isProcessing}
                            onAnalyze={() => alert('Lancement de l\'analyse juridique phase suivante!')}
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
