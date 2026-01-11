'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

export function Header() {
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header
            className={cn(
                "fixed top-0 left-0 right-0 z-50 w-full transition-all duration-300 border-b",
                isScrolled
                    ? "bg-white/90 backdrop-blur-md border-neutral-200 shadow-sm"
                    : "bg-transparent border-transparent"
            )}
        >
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2 group">
                        <div className={cn(
                            "flex items-center justify-center w-10 h-10 rounded-lg transition-all duration-300",
                            isScrolled ? "bg-primary-900" : "bg-white/20 backdrop-blur-sm group-hover:bg-white/30"
                        )}>
                            <svg
                                className={cn(
                                    "w-6 h-6 transition-colors duration-300",
                                    isScrolled ? "text-white" : "text-white"
                                )}
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
                        <span className={cn(
                            "text-xl font-bold font-display transition-colors duration-300",
                            isScrolled ? "text-slate-900" : "text-white"
                        )}>
                            AvantDeSigner
                        </span>
                    </Link>

                    {/* Navigation */}
                    <nav className="hidden md:flex items-center gap-12">
                        {['Comment ça marche', 'Tarifs', 'FAQ'].map((item) => (
                            <Link
                                key={item}
                                href={`/#${item.toLowerCase().replace(/ /g, '-').replace('ç', 'c')}`}
                                className={cn(
                                    "text-sm font-medium transition-colors tracking-wide hover:text-primary-500",
                                    isScrolled ? "text-slate-600" : "text-white/90 hover:text-white"
                                )}
                            >
                                {item}
                            </Link>
                        ))}
                    </nav>

                    {/* CTA */}
                    <div className="flex items-center gap-6">
                        <Link
                            href="/login"
                            className={cn(
                                "text-sm font-bold transition-colors hover:text-primary-500",
                                isScrolled ? "text-slate-700" : "text-white hover:text-white"
                            )}
                        >
                            Connexion
                        </Link>
                        <Link href="/analyser">
                            <Button
                                size="md"
                                // Hardcoded dark background to absolutely guarantee visibility against white header
                                className="bg-[#0f172a] hover:bg-[#1e293b] text-white border-none font-bold shadow-lg shadow-primary-900/20"
                            >
                                Vérifier un contrat
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </header>
    );
}
