'use client';

import { Card, CardContent } from '@/components/ui/Card';
import { motion } from 'framer-motion';
import Image from 'next/image';

const contractTypes = [
    {
        name: 'Particuliers & Logement',
        image: '/images/categories/housing.webp',
        description: 'Baux d’habitation, locations saisonnières, colocation. Vérifiez vos droits, dépôts de garantie et charges.',
    },
    {
        name: 'Travail & Emploi',
        image: '/images/categories/work.webp',
        description: 'CDI, CDD, alternance. Vérifiez périodes d’essai, clauses de non-concurrence et avantages liés à l’emploi.',
    },
    {
        name: 'Étudiants & Jeunes professionnels',
        image: '/images/categories/student.webp',
        description: 'Stages, apprentissage, conventions universitaires. Protégez vos droits dès le début de votre parcours professionnel.',
    },
    {
        name: 'Freelance & Prestataires',
        image: '/images/categories/freelance.webp',
        description: 'Contrats de prestation de services et missions freelance. Sécurisez délais, paiements et propriété intellectuelle.',
    },
    {
        name: 'Entreprises & Pro – B2B',
        image: '/images/categories/b2b.webp',
        description: 'Contrats de sous-traitance pour PME, sécurité, nettoyage. Clarifiez prestations, responsabilités et obligations légales.',
    },
    {
        name: 'Abonnements & Services',
        image: '/images/categories/subscriptions.webp',
        description: 'Téléphonie, internet, streaming, salles de sport. Évitez reconductions tacites et clauses abusives.',
    },
    {
        name: 'Vente & Achats',
        image: '/images/categories/sales.webp',
        description: 'Contrats d’achat de biens ou services. Vérifiez conditions de garantie, livraison et retour.',
    },
    {
        name: 'Assurance',
        image: '/images/categories/insurance_clean.webp',
        description: 'Auto, habitation, santé. Comprenez exclusions et limitations.',
    },
];

export function ContractTypes() {
    return (
        <section className="py-32 bg-slate-50">
            <div className="container mx-auto px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl sm:text-5xl font-bold font-display text-neutral-900 mb-4">
                        Tous types de contrats
                    </h2>
                    <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                        AvantDeSigner analyse tout type de contrat pour que vous soyez toujours protégé.
                    </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
                    {contractTypes.map((type, index) => (
                        <motion.div
                            key={type.name}
                            initial={{ opacity: 0, scale: 0.9 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.3, delay: index * 0.05 }}
                        >
                            <Card hover className="h-full border-slate-200 shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden flex flex-col">
                                <div className="relative w-full h-48 bg-slate-100">
                                    <Image
                                        src={type.image}
                                        alt={type.name}
                                        fill
                                        className="object-cover"
                                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                                    />
                                </div>
                                <CardContent className="p-6 text-center flex flex-col items-center flex-grow">
                                    <h3 className="font-bold text-lg text-neutral-900 mb-2">{type.name}</h3>
                                    <p className="text-sm text-neutral-600 leading-relaxed max-w-[250px] mx-auto">
                                        {type.description}
                                    </p>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
