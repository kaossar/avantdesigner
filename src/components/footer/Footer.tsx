'use client';

import Link from 'next/link';

export function Footer() {
    return (
        <footer className="bg-primary-900 text-white py-32 border-t border-white/5">
            <div className="container mx-auto px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
                    {/* Brand */}
                    <div className="col-span-1 md:col-span-1">
                        <Link href="/" className="flex items-center gap-2 mb-6">
                            <div className="w-8 h-8 bg-white rounded flex items-center justify-center">
                                <span className="text-primary-900 font-black text-lg">A</span>
                            </div>
                            <span className="text-xl font-serif font-black tracking-tight">AvantDeSigner</span>
                        </Link>
                        <p className="text-slate-400 text-sm leading-relaxed mb-6 font-medium">
                            Intelligence Artificielle au service de la sécurité juridique. Analysez, sécurisez, et négociez en toute confiance.
                        </p>
                    </div>

                    {/* Links */}
                    <div>
                        <h4 className="font-bold text-xs uppercase tracking-[0.2em] text-white/40 mb-6">Service</h4>
                        <ul className="space-y-4">
                            <li><Link href="/analyser" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Analyse Express</Link></li>
                            <li><Link href="/#tarifs" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Nos Tarifs</Link></li>
                            <li><Link href="/login" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Connexion Client</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-bold text-xs uppercase tracking-[0.2em] text-white/40 mb-6">Informations</h4>
                        <ul className="space-y-4">
                            <li><Link href="/mentions-legales" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Mentions Légales</Link></li>
                            <li><Link href="/cgu" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">CGU / CGV</Link></li>
                            <li><Link href="/politique-confidentialite" className="text-slate-300 hover:text-white transition-colors text-sm font-semibold">Confidentialité</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-bold text-xs uppercase tracking-[0.2em] text-white/40 mb-6">Confiance</h4>
                        <div className="flex flex-wrap gap-4 grayscale brightness-200 opacity-50">
                            <div className="w-10 h-6 bg-white/20 rounded"></div>
                            <div className="w-10 h-6 bg-white/20 rounded"></div>
                            <div className="w-10 h-6 bg-white/20 rounded"></div>
                        </div>
                        <p className="text-[10px] text-slate-500 mt-6 font-bold leading-relaxed">
                            Paiement sécurisé via Stripe. <br />
                            Serveurs hébergés en Europe.
                        </p>
                        <p className="text-[10px] text-slate-400 mt-4 leading-relaxed font-medium border-t border-white/10 pt-4">
                            * AvantDeSigner est un outil d'analyse automatisé. Il ne remplace pas le conseil d'un avocat. Nos reformulations sont des suggestions à des fins de négociation.
                        </p>
                    </div>
                </div>

                <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                        © 2024 AvantDeSigner. Tous droits réservés.
                    </p>
                    <div className="flex gap-6">
                        <span className="text-slate-500 text-[10px] font-bold uppercase tracking-widest cursor-pointer hover:text-white transition-colors">Twitter</span>
                        <span className="text-slate-500 text-[10px] font-bold uppercase tracking-widest cursor-pointer hover:text-white transition-colors">LinkedIn</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}
