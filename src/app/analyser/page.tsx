'use client';

import { UploadSection } from '@/components/upload/UploadSection';
import { SecurityBadge } from '@/components/upload/SecurityBadge';
import { motion } from 'framer-motion';

export default function AnalyserPage() {
    return (
        <div className="min-h-screen bg-slate-50 flex flex-col">

            <main className="flex-1 py-16 md:py-24">
                <div className="container">
                    {/* Page Header */}
                    <div className="text-center max-w-3xl mx-auto mb-16">
                        <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 rounded-full text-primary-900 text-xs font-bold uppercase tracking-widest mb-6">
                            <span className="w-2 h-2 rounded-full bg-primary-600 animate-pulse"></span>
                            Zone Sécurisée
                        </div>
                        <h1 className="text-4xl md:text-5xl font-serif font-black text-primary-900 mb-6">
                            Analysez votre contrat
                        </h1>
                        <p className="text-lg text-slate-600 leading-relaxed">
                            Notre intelligence artificielle va lire, vérifier et sécuriser votre document en quelques secondes.
                        </p>
                    </div>

                    {/* Main Content */}
                    <div className="flex flex-col lg:flex-row gap-8 items-start justify-center">
                        <div className="w-full lg:w-2/3">
                            <UploadSection />
                        </div>

                        {/* Sidebar */}
                        <div className="w-full lg:w-1/3 space-y-6">
                            <SecurityBadge />

                            <div className="bg-white border border-slate-200 rounded-xl p-6">
                                <h3 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-4">Étapes d'analyse</h3>
                                <div className="space-y-6">
                                    <div className="flex gap-4">
                                        <div className="flex flex-col items-center">
                                            <div className="w-6 h-6 rounded-full bg-primary-900 text-white flex items-center justify-center text-xs font-bold">1</div>
                                            <div className="w-px h-full bg-slate-200 my-1"></div>
                                        </div>
                                        <div className="pb-4">
                                            <h4 className="font-bold text-primary-900 text-sm">Extraction & OCR</h4>
                                            <p className="text-xs text-slate-500 mt-1">Lecture numérisée du contenu.</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="flex flex-col items-center">
                                            <div className="w-6 h-6 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center text-xs font-bold">2</div>
                                            <div className="w-px h-full bg-slate-200 my-1"></div>
                                        </div>
                                        <div className="pb-4">
                                            <h4 className="font-bold text-slate-400 text-sm">Détection des risques</h4>
                                            <p className="text-xs text-slate-400 mt-1">Analyse juridique par IA.</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="flex flex-col items-center">
                                            <div className="w-6 h-6 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center text-xs font-bold">3</div>
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-slate-400 text-sm">Rapport & Conseils</h4>
                                            <p className="text-xs text-slate-400 mt-1">Scores et reformulations.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
