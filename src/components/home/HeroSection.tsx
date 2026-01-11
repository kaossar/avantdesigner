'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';

export function HeroSection() {
    return (
        <section className="relative min-h-screen flex flex-col justify-center items-center overflow-hidden pt-20">
            {/* Professional WebP Background */}
            <div
                className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat"
                style={{
                    backgroundImage: 'url(/hero-bg.webp)',
                }}
            >
                {/* Dark overlay for excellent text contrast */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary-900/95 via-primary-900/90 to-slate-900/95" />
            </div>

            <div className="container relative z-10 mx-auto px-4 sm:px-6 lg:px-8 flex-grow flex flex-col justify-center">
                <div className="mx-auto max-w-4xl text-center">
                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="inline-flex items-center gap-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 px-4 py-2 text-sm font-medium text-white mb-6"
                    >
                        <svg className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        Protection contractuelle accessible à tous
                    </motion.div>

                    {/* Title */}
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-5xl sm:text-7xl lg:text-8xl font-black font-serif text-white mb-6 tracking-tight"
                    >
                        AvantDeSigner
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="text-2xl sm:text-4xl font-light text-slate-200 mb-10 max-w-3xl mx-auto leading-relaxed"
                    >
                        Vérifiez votre contrat en <span className="text-white font-bold border-b-2 border-emerald-400">2 minutes</span>.
                    </motion.p>

                    {/* CTA Buttons */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16"
                    >
                        <Link href="/analyser" className="w-full sm:w-auto">
                            <Button
                                variant="secondary"
                                size="xl"
                                className="w-full sm:w-auto shadow-2xl hover:scale-105 transition-transform"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Analyser mon contrat
                            </Button>
                        </Link>
                        <Link href="/#comment-ca-marche" className="w-full sm:w-auto">
                            <Button
                                variant="outline"
                                size="xl"
                                className="w-full sm:w-auto border-white/40 text-white bg-transparent hover:bg-white/10 hover:border-white"
                            >
                                Comment ça marche ?
                            </Button>
                        </Link>
                    </motion.div>

                    {/* Trust Bar */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5, delay: 0.5 }}
                        className="bg-white/5 backdrop-blur-sm border-y border-white/10 py-6 w-full max-w-5xl mx-auto rounded-xl"
                    >
                        <div className="flex flex-wrap justify-around items-center gap-6 px-4">
                            {[
                                { text: "Analyse par IA", icon: "⚡" },
                                { text: "100% Confidentiel", icon: "🔒" },
                                { text: "Aide à la Décision", icon: "🛡️" }
                            ].map((item, i) => (
                                <div key={i} className="flex items-center gap-3 text-slate-200">
                                    <span className="text-2xl">{item.icon}</span>
                                    <span className="text-sm sm:text-base font-bold uppercase tracking-wider">{item.text}</span>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </div>


        </section>
    );
}
