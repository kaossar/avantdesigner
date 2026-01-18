'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

export function Header() {
    const [isScrolled, setIsScrolled] = useState(false);
    const pathname = usePathname();
    const isHome = pathname === '/';

    // Show solid header if scrolled OR if not on home page
    const shouldShowSolid = isScrolled || !isHome;

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
                shouldShowSolid
                    ? "bg-white/90 backdrop-blur-md border-neutral-200 shadow-sm"
                    : "bg-transparent border-transparent"
            )}
        >
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2 group">
                        <div className={cn(
                            "flex items-center justify-center w-10 h-10 rounded-lg transition-all duration-300 relative",
                            shouldShowSolid ? "bg-transparent" : "bg-white/20 backdrop-blur-sm group-hover:bg-white/30"
                        )}>
                            <Image
                                src="/logos/logo.png"
                                alt="Logo"
                                fill
                                className="object-contain p-1"
                                priority
                            />
                        </div>
                        <span className={cn(
                            "text-xl font-bold font-display transition-colors duration-300",
                            shouldShowSolid ? "text-slate-900" : "text-white"
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
                                    shouldShowSolid ? "text-slate-600" : "text-white/90 hover:text-white"
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
                                "hidden sm:block", // Hide on mobile if space is tight
                                shouldShowSolid ? "text-slate-700" : "text-white hover:text-white"
                            )}
                        >
                            Connexion
                        </Link>
                        <Link href="/analyser">
                            <Button
                                size="md"
                                // Keep button consistently visible/styled
                                className="bg-[#0f172a] hover:bg-[#1e293b] text-white border-none font-bold shadow-lg shadow-primary-900/20"
                            >
                                Vérifier un contrat
                            </Button>
                        </Link>
                    </div>
                </div>
            </div >
        </header >
    );
}
