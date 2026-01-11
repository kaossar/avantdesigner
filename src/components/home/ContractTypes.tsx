'use client';

import { Card, CardContent } from '@/components/ui/Card';
import { motion } from 'framer-motion';

const contractTypes = [
    {
        name: 'Location',
        icon: '🏠',
        description: 'Bail d\'habitation, commercial',
    },
    {
        name: 'Travail',
        icon: '💼',
        description: 'CDI, CDD, stage',
    },
    {
        name: 'Freelance',
        icon: '💻',
        description: 'Prestation de services',
    },
    {
        name: 'Abonnement',
        icon: '📱',
        description: 'Téléphonie, internet, salle de sport',
    },
    {
        name: 'Vente',
        icon: '🛒',
        description: 'Achat de biens, services',
    },
    {
        name: 'Assurance',
        icon: '🛡️',
        description: 'Auto, habitation, santé',
    },
];

export function ContractTypes() {
    return (
        <section className="py-20 bg-white">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl sm:text-5xl font-bold font-display text-neutral-900 mb-4">
                        Tous types de contrats
                    </h2>
                    <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                        AvantDeSigner analyse n\'importe quel contrat, quelle que soit sa nature
                    </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 max-w-6xl mx-auto">
                    {contractTypes.map((type, index) => (
                        <motion.div
                            key={type.name}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.3, delay: index * 0.05 }}
                        >
                            <Card hover className="h-full">
                                <CardContent className="p-6 text-center">
                                    <div className="text-4xl mb-3">{type.icon}</div>
                                    <h3 className="font-semibold text-neutral-900 mb-1">{type.name}</h3>
                                    <p className="text-xs text-neutral-600">{type.description}</p>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
