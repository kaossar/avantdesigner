'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export function Header() {
    return (
        <header className="sticky top-0 z-40 w-full border-b border-neutral-200 bg-white/80 backdrop-blur-md">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2">
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
                    </Link>

                    {/* Navigation */}
                    <nav className="hidden md:flex items-center space-x-8">
                        <Link
                            href="/#comment-ca-marche"
                            className="text-sm font-medium text-neutral-700 hover:text-primary-600 transition-colors"
                        >
                            Comment ça marche
                        </Link>
                        <Link
                            href="/#tarifs"
                            className="text-sm font-medium text-neutral-700 hover:text-primary-600 transition-colors"
                        >
                            Tarifs
                        </Link>
                        <Link
                            href="/#faq"
                            className="text-sm font-medium text-neutral-700 hover:text-primary-600 transition-colors"
                        >
                            FAQ
                        </Link>
                    </nav>

                    {/* CTA */}
                    <div className="flex items-center space-x-4">
                        <Link href="/analyser">
                            <Button variant="primary" size="md">
                                Vérifier un contrat
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </header>
    );
}
