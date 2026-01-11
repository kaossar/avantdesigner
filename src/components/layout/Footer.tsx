import Link from 'next/link';

export function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="border-t border-neutral-200 bg-neutral-50">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                    {/* Brand */}
                    <div className="col-span-1 md:col-span-2">
                        <div className="flex items-center space-x-2 mb-4">
                            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-primary">
                                <svg
                                    className="w-6 h-6 text-white"
                                    fill="none"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth="2"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <span className="text-xl font-bold font-display text-gradient">
                                AvantDeSigner
                            </span>
                        </div>
                        <p className="text-sm text-neutral-600 max-w-md">
                            Vérifiez votre contrat avant de signer. Identifiez les clauses à risque et
                            protégez-vous des arnaques contractuelles.
                        </p>
                    </div>

                    {/* Navigation */}
                    <div>
                        <h3 className="font-semibold text-neutral-900 mb-4">Navigation</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link
                                    href="/"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    Accueil
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/analyser"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    Analyser un contrat
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/dashboard"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    Mon compte
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Legal */}
                    <div>
                        <h3 className="font-semibold text-neutral-900 mb-4">Légal</h3>
                        <ul className="space-y-2">
                            <li>
                                <Link
                                    href="/mentions-legales"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    Mentions légales
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/confidentialite"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    Confidentialité
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="/cgu"
                                    className="text-sm text-neutral-600 hover:text-primary-600 transition-colors"
                                >
                                    CGU
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Bottom */}
                <div className="mt-12 pt-8 border-t border-neutral-200">
                    <p className="text-sm text-neutral-600 text-center">
                        © {currentYear} AvantDeSigner. Tous droits réservés.
                    </p>
                    <p className="text-xs text-neutral-500 text-center mt-2">
                        AvantDeSigner est un outil d'aide à la compréhension et à la vigilance
                        contractuelle. Il ne constitue pas un avis juridique et ne remplace pas un
                        professionnel du droit.
                    </p>
                </div>
            </div>
        </footer>
    );
}
