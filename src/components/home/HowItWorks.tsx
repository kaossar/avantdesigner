'use client';

import { Card, CardContent } from '@/components/ui/Card';
import { motion } from 'framer-motion';

const steps = [
    {
        number: '1',
        title: 'Téléversez votre contrat',
        description:
            'PDF, Word, image ou scan papier : tous les formats sont acceptés. Notre OCR extrait automatiquement le texte.',
        icon: (
            <svg
                className="w-8 h-8"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
        ),
    },
    {
        number: '2',
        title: 'Analyse automatique',
        description:
            'Notre IA identifie les clauses à risque, les déséquilibres contractuels et les pièges cachés en quelques secondes.',
        icon: (
            <svg
                className="w-8 h-8"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
        ),
    },
    {
        number: '3',
        title: 'Reformulations & Assistance',
        description:
            'Obtenez des reformulations concrètes pour chaque clause à risque, prêtes à négocier, avec des conseils pratiques pour agir.',
        icon: (
            <svg
                className="w-8 h-8"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
            >
                <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
        ),
    },
];

export function HowItWorks() {
    return (
        <section id="comment-ca-marche" className="py-20 bg-white">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl sm:text-5xl font-bold font-display text-neutral-900 mb-4">
                        Comment ça marche ?
                    </h2>
                    <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                        Vérifiez votre contrat en 3 étapes simples. Rapide, accessible et sécurisé.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {steps.map((step, index) => (
                        <motion.div
                            key={step.number}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                        >
                            <Card hover className="h-full">
                                <CardContent className="p-8">
                                    <div className="flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 text-primary-600 mb-6 mx-auto">
                                        {step.icon}
                                    </div>
                                    <div className="text-center">
                                        <div className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-gradient-primary text-white font-bold text-sm mb-4">
                                            {step.number}
                                        </div>
                                        <h3 className="text-xl font-semibold text-neutral-900 mb-3">
                                            {step.title}
                                        </h3>
                                        <p className="text-neutral-600">{step.description}</p>
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
