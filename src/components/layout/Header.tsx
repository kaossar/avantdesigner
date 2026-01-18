'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

export function Header() {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const pathname = usePathname();
    const isHome = pathname === '/';

    // Show solid header if scrolled OR if not on home page OR if mobile menu is open
    const shouldShowSolid = isScrolled || !isHome || isMobileMenuOpen;

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close mobile menu when route changes
    useEffect(() => {
        setIsMobileMenuOpen(false);
    }, [pathname]);

    const navItems = ['Comment ça marche', 'Tarifs', 'FAQ'];

    return (
        <header
            className={cn(
                "fixed top-0 left-0 right-0 z-50 w-full transition-all duration-300 border-b",
                shouldShowSolid
                    ? "bg-white/95 backdrop-blur-md border-neutral-200 shadow-sm"
                    : "bg-transparent border-transparent"
            )}
        >
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link
                        href="/"
                        className="flex items-center space-x-2 group relative z-50"
                        aria-label="Retour à l'accueil"
                    >
                        <div className={cn(
                            "flex items-center justify-center w-10 h-10 rounded-lg transition-all duration-300 relative",
                            shouldShowSolid ? "bg-transparent" : "bg-white/20 backdrop-blur-sm group-hover:bg-white/30"
                        )}>
                            <Image
                                src={shouldShowSolid ? "/logos/logo.png" : "/logos/logo-white.png"}
                                alt="AvantDeSigner Logo"
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

                    {/* Desktop Navigation */}
                    <nav className="hidden md:flex items-center gap-12">
                        {navItems.map((item) => (
                            <Link
                                key={item}
                                href={`/#${item.toLowerCase().replace(/ /g, '-').replace('ç', 'c')}`}
                                className={cn(
                                    "text-sm font-medium transition-colors tracking-wide hover:text-primary-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-sm",
                                    shouldShowSolid ? "text-slate-600" : "text-white/90 hover:text-white"
                                )}
                            >
                                {item}
                            </Link>
                        ))}
                    </nav>

                    {/* Desktop CTA */}
                    <div className="hidden md:flex items-center gap-6">
                        <Link
                            href="/login"
                            className={cn(
                                "text-sm font-bold transition-colors hover:text-primary-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-sm",
                                shouldShowSolid ? "text-slate-700" : "text-white hover:text-white"
                            )}
                        >
                            Connexion
                        </Link>
                        <Link href="/analyser" tabIndex={-1}>
                            <Button
                                size="md"
                                className="bg-[#0f172a] hover:bg-[#1e293b] text-white border-none font-bold shadow-lg shadow-primary-900/20"
                            >
                                Vérifier un contrat
                            </Button>
                        </Link>
                    </div>

                    {/* Mobile Menu Trigger */}
                    <button
                        className="md:hidden relative z-50 p-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-md"
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        aria-label={isMobileMenuOpen ? "Fermer le menu" : "Ouvrir le menu"}
                        aria-expanded={isMobileMenuOpen}
                    >
                        {isMobileMenuOpen ? (
                            <X className={cn("w-6 h-6", shouldShowSolid ? "text-slate-900" : "text-white")} />
                        ) : (
                            <Menu className={cn("w-6 h-6", shouldShowSolid ? "text-slate-900" : "text-white")} />
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile Menu Overlay */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.2 }}
                        className="fixed inset-0 top-16 z-40 bg-white border-t border-neutral-100 md:hidden flex flex-col p-6 overflow-y-auto"
                    >
                        <nav className="flex flex-col gap-6">
                            {navItems.map((item) => (
                                <Link
                                    key={item}
                                    href={`/#${item.toLowerCase().replace(/ /g, '-').replace('ç', 'c')}`}
                                    className="text-lg font-medium text-slate-900 hover:text-primary-600 py-2 border-b border-neutral-50"
                                    onClick={() => setIsMobileMenuOpen(false)}
                                >
                                    {item}
                                </Link>
                            ))}
                            <hr className="border-neutral-100 my-2" />
                            <Link
                                href="/login"
                                className="text-lg font-bold text-slate-900 hover:text-primary-600 py-2"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                Connexion
                            </Link>
                            <Link href="/analyser" onClick={() => setIsMobileMenuOpen(false)} className="mt-2">
                                <Button size="lg" className="w-full bg-[#0f172a] text-white">
                                    Vérifier un contrat
                                </Button>
                            </Link>
                        </nav>
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
}
