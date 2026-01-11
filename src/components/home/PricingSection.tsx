'use client';

import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';
import Link from 'next/link';

const plans = [
    {
        name: 'À l\'acte',
        price: '1,90€',
        priceDetail: 'par contrat',
        description: 'Payez uniquement ce que vous utilisez',
        features: [
            'Analyse complète du contrat',
            'Détection des clauses à risque',
            'Reformulations protectrices',
            'Assistance contextuelle',
            'Export PDF',
        ],
        cta: 'Analyser un contrat',
        href: '/analyser',
        popular: false,
        badge: null,
    },
    {
        name: 'Pack 10',
        price: '15€',
        priceDetail: '1,50€/contrat',
        savings: 'Économie de 4€',
        description: 'Pour une utilisation régulière',
        features: [
            'Tout À l\'acte +',
            '10 contrats inclus',
            'Valable 12 mois',
            'Alertes avant expiration',
            'Historique complet',
        ],
        cta: 'Acheter le pack',
        href: '/analyser',
        popular: true,
        badge: 'Populaire',
    },
    {
        name: 'Pack 25',
        price: '35€',
        priceDetail: '1,40€/contrat',
        savings: 'Économie de 12,50€',
        description: 'Pour les professionnels',
        features: [
            'Tout Pack 10 +',
            '25 contrats inclus',
            'Valable 12 mois',
            'Support prioritaire',
            'Rapports détaillés',
        ],
        cta: 'Acheter le pack',
        href: '/analyser',
        popular: false,
        badge: null,
    },
    {
        name: 'Pack 50',
        price: '60€',
        priceDetail: '1,20€/contrat',
        savings: 'Économie de 35€',
        description: 'Pour un usage intensif',
        features: [
            'Tout Pack 25 +',
            '50 contrats inclus',
            'Valable 12 mois',
            'Assistance dédiée',
            'API access (bientôt)',
        ],
        cta: 'Acheter le pack',
        href: '/analyser',
        popular: false,
        badge: 'Meilleure Valeur',
    },
];

export function PricingSection() {
    return (
        <section id="tarifs" className="py-32 bg-white">
            <div className="container mx-auto px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl sm:text-5xl font-bold font-display text-neutral-900 mb-4">
                        Tarifs simples et transparents
                    </h2>
                    <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
                        Payez uniquement pour les contrats que vous analysez. Aucun abonnement, aucun
                        engagement.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
                    {plans.map((plan, index) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="relative"
                        >
                            {plan.badge && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 z-10">
                                    <span className="bg-gradient-to-r from-primary-600 to-primary-900 text-white px-4 py-1 rounded-full text-sm font-semibold shadow-lg">
                                        {plan.badge}
                                    </span>
                                </div>
                            )}
                            <Card
                                hover
                                className={`h-full ${plan.popular ? 'border-2 border-primary-500 shadow-xl' : ''}`}
                            >
                                <CardContent className="p-6">
                                    <div className="text-center mb-6">
                                        <h3 className="text-xl font-semibold text-neutral-900 mb-2">{plan.name}</h3>
                                        <div className="mb-2">
                                            <span className="text-4xl font-bold text-neutral-900">{plan.price}</span>
                                            {plan.priceDetail && (
                                                <div className="text-sm text-neutral-600 mt-1">{plan.priceDetail}</div>
                                            )}
                                        </div>
                                        {plan.savings && (
                                            <div className="inline-block bg-success-100 text-success-700 px-3 py-1 rounded-full text-xs font-semibold mb-2">
                                                {plan.savings}
                                            </div>
                                        )}
                                        <p className="text-sm text-neutral-600">{plan.description}</p>
                                    </div>

                                    <ul className="space-y-3 mb-6">
                                        {plan.features.map((feature, i) => (
                                            <li key={i} className="flex items-start gap-2 text-sm">
                                                <svg
                                                    className="w-5 h-5 text-success-600 flex-shrink-0 mt-0.5"
                                                    fill="currentColor"
                                                    viewBox="0 0 20 20"
                                                >
                                                    <path
                                                        fillRule="evenodd"
                                                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                        clipRule="evenodd"
                                                    />
                                                </svg>
                                                <span className="text-neutral-700">{feature}</span>
                                            </li>
                                        ))}
                                    </ul>

                                    <Link href={plan.href} className="block">
                                        <Button
                                            variant={plan.popular ? 'primary' : 'outline'}
                                            fullWidth
                                            className="w-full"
                                        >
                                            {plan.cta}
                                        </Button>
                                    </Link>
                                </CardContent>
                            </Card>
                        </motion.div>
                    ))}
                </div>

                <div className="mt-12 space-y-4 text-center max-w-3xl mx-auto">
                    <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                        <p className="text-sm text-primary-900">
                            <strong>⏱️ Validité des packs :</strong> Les packs de contrats sont valables 12
                            mois à partir de la date d'achat. Les crédits non utilisés expirent après cette
                            période.
                        </p>
                    </div>
                    <p className="text-sm text-neutral-600">
                        💡 <strong>Astuce :</strong> Commencez avec un contrat à l'acte pour tester le
                        service, puis passez à un pack si vous avez plusieurs contrats à analyser.
                    </p>
                    <p className="text-xs text-neutral-500">
                        Prix TTC. Paiement sécurisé par Stripe. Aucun abonnement récurrent, aucun
                        prélèvement automatique.
                    </p>
                </div>
            </div>
        </section>
    );
}
