'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const faqs = [
    {
        question: 'Qu\'est-ce qu\'une reformulation et pourquoi est-ce utile ?',
        answer:
            'Une reformulation est une version améliorée et protectrice d\'une clause à risque. Au lieu de simplement vous dire "cette clause est dangereuse", nous vous proposons une version équilibrée, prête à négocier avec l\'autre partie. C\'est la différence entre comprendre un problème et avoir la solution en main.',
    },
    {
        question: 'Combien coûte l\'analyse d\'un contrat ?',
        answer:
            'L\'analyse complète d\'un contrat coûte 1,90€. Ce prix inclut la détection de toutes les clauses à risque, les reformulations protectrices, l\'assistance contextuelle et l\'export PDF. Vous pouvez aussi acheter des packs pour économiser : 10 contrats pour 15€, 25 pour 35€, ou 50 pour 60€.',
    },
    {
        question: 'AvantDeSigner remplace-t-il un avocat ?',
        answer:
            'Non. AvantDeSigner est un outil d\'aide à la compréhension et à la vigilance contractuelle. Il ne constitue pas un avis juridique et ne remplace pas un professionnel du droit. Pour des questions juridiques complexes, consultez un avocat.',
    },
    {
        question: 'Quels types de contrats puis-je analyser ?',
        answer:
            'Vous pouvez analyser tous types de contrats : location, travail, freelance, abonnements, prestations de services, vente, etc. Notre système s\'adapte automatiquement au type de document.',
    },
    {
        question: 'Mes données sont-elles sécurisées ?',
        answer:
            'Absolument. Vos contrats sont chiffrés et supprimés automatiquement après 24h. Nous ne réutilisons jamais vos données et sommes conformes au RGPD.',
    },
    {
        question: 'Quels formats de fichiers acceptez-vous ?',
        answer:
            'Nous acceptons tous les formats : PDF, Word (DOC/DOCX), images (JPG, PNG, HEIC), scans papier, et même le copier-coller. Notre OCR extrait automatiquement le texte des images.',
    },
    {
        question: 'Les packs de contrats ont-ils une date d\'expiration ?',
        answer:
            'Oui, les packs de contrats sont valables 12 mois à partir de la date d\'achat. Vous recevrez des alertes avant l\'expiration de vos crédits. Les crédits non utilisés après 12 mois ne sont pas remboursables.',
    },
    {
        question: 'Combien de temps prend l\'analyse ?',
        answer:
            'L\'analyse complète prend généralement entre 30 secondes et 2 minutes selon la longueur du contrat. Vous recevez immédiatement un score global et pouvez consulter les détails clause par clause.',
    },
];

export function FAQ() {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <section id="faq" className="py-32 bg-slate-50">
            <div className="container mx-auto px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl sm:text-5xl font-bold font-display text-neutral-900 mb-4">
                        Questions fréquentes
                    </h2>
                    <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                        Tout ce que vous devez savoir sur AvantDeSigner
                    </p>
                </div>

                <div className="max-w-3xl mx-auto space-y-4">
                    {faqs.map((faq, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.3, delay: index * 0.05 }}
                            className="bg-white rounded-xl border border-neutral-200 overflow-hidden"
                        >
                            <button
                                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                                className="w-full px-6 py-5 text-left flex items-center justify-between hover:bg-neutral-50 transition-colors"
                            >
                                <span className="font-semibold text-neutral-900 pr-8">{faq.question}</span>
                                <svg
                                    className={`w-5 h-5 text-neutral-500 transition-transform flex-shrink-0 ${openIndex === index ? 'rotate-180' : ''
                                        }`}
                                    fill="none"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            <AnimatePresence>
                                {openIndex === index && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <div className="px-6 pb-5 text-neutral-600">{faq.answer}</div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
