'use client';

import { motion } from 'framer-motion';

export function SecurityBadge() {
    return (
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-6 flex flex-col md:flex-row items-center gap-6 text-center md:text-left">
            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-sm border border-slate-100 flex-shrink-0">
                <svg className="w-8 h-8 text-primary-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7f4 4 0 00-8 0v4h8z" />
                </svg>
            </div>
            <div className="flex-1">
                <h3 className="text-lg font-serif font-black text-primary-900 mb-2">Sécurité Bancaire & Confidentialité</h3>
                <p className="text-slate-600 text-sm leading-relaxed">
                    Vos documents sont chiffrés de bout en bout (AES-256). Aucune donnée n'est stockée plus de 24h.
                    Nous ne revendons aucune information.
                </p>
            </div>
            <div className="flex flex-col gap-2 opacity-60">
                <div className="flex items-center gap-2 text-[10px] uppercase font-bold text-slate-400">
                    <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                    Serveurs France
                </div>
                <div className="flex items-center gap-2 text-[10px] uppercase font-bold text-slate-400">
                    <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                    RGPD Compliant
                </div>
            </div>
        </div>
    );
}
