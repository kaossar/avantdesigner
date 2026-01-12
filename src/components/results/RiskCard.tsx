'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, ChevronUp, AlertTriangle, AlertCircle, Info } from 'lucide-react';
import { DetectedRisk } from '@/lib/analysis/types';
import { cn } from '@/lib/utils';

interface RiskCardProps {
    risk: DetectedRisk;
}

export function RiskCard({ risk }: RiskCardProps) {
    const [isExpanded, setIsExpanded] = useState(false);

    const severityConfig = {
        critical: {
            color: 'text-red-700',
            bg: 'bg-red-50',
            border: 'border-l-red-600',
            icon: AlertTriangle,
            badge: 'bg-red-100 text-red-800'
        },
        high: {
            color: 'text-orange-700',
            bg: 'bg-orange-50',
            border: 'border-l-orange-500',
            icon: AlertCircle,
            badge: 'bg-orange-100 text-orange-800'
        },
        medium: {
            color: 'text-yellow-700',
            bg: 'bg-yellow-50',
            border: 'border-l-yellow-500',
            icon: Info,
            badge: 'bg-yellow-100 text-yellow-800'
        },
        low: {
            color: 'text-blue-700',
            bg: 'bg-blue-50',
            border: 'border-l-blue-500',
            icon: Info,
            badge: 'bg-blue-100 text-blue-800'
        }
    };

    const config = severityConfig[risk.severity] || severityConfig.medium;
    const Icon = config.icon;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
                "mb-4 rounded-lg border border-slate-200 shadow-sm overflow-hidden",
                "border-l-4",
                config.border,
                "bg-white"
            )}
        >
            <div
                className="p-4 cursor-pointer flex items-start justify-between hover:bg-slate-50 transition-colors"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex items-start gap-3">
                    <div className={cn("p-2 rounded-full", config.bg)}>
                        <Icon className={cn("w-5 h-5", config.color)} />
                    </div>
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <span className={cn("text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider", config.badge)}>
                                {risk.severity}
                            </span>
                            {risk.source === 'ai' && (
                                <span className="text-xs font-medium text-purple-600 bg-purple-50 px-2 py-0.5 rounded border border-purple-100 flex items-center gap-1">
                                    ✨ IA Mistral
                                </span>
                            )}
                        </div>
                        <h3 className="font-semibold text-slate-900 text-lg leading-tight">
                            {risk.title}
                        </h3>
                    </div>
                </div>

                <button className="text-slate-400 hover:text-slate-600 transition-colors mt-1">
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>
            </div>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="border-t border-slate-100 bg-slate-50/50"
                    >
                        <div className="p-4 pl-14 space-y-4">
                            <div>
                                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Analyse</h4>
                                <p className="text-slate-700 text-sm leading-relaxed">
                                    {risk.description}
                                </p>
                            </div>

                            {risk.clause.text && risk.clause.text.length > 5 && (
                                <div className="bg-white p-3 rounded border border-slate-200 text-xs font-mono text-slate-600 italic relative">
                                    <span className="absolute top-2 left-2 text-slate-300 text-2xl leading-none">"</span>
                                    <div className="pl-4 pt-1">
                                        {risk.clause.text}
                                    </div>
                                </div>
                            )}

                            {risk.recommendation && (
                                <div className="bg-green-50 border border-green-100 rounded-md p-3">
                                    <h4 className="text-xs font-bold text-green-700 uppercase tracking-wide mb-1 flex items-center gap-2">
                                        💡 Conseil de l'expert
                                    </h4>
                                    <p className="text-green-800 text-sm font-medium">
                                        {risk.recommendation}
                                    </p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
}
