'use client';

import { motion } from 'framer-motion';

interface ScoreGaugeProps {
    score: number; // 0 to 100
}

export function ScoreGauge({ score }: ScoreGaugeProps) {
    // Determine color based on score
    let color = 'text-green-500';
    let label = 'Excellent';

    if (score < 50) {
        color = 'text-red-500';
        label = 'Critique';
    } else if (score < 70) {
        color = 'text-orange-500';
        label = 'Risqué';
    } else if (score < 90) {
        color = 'text-yellow-500';
        label = 'Passable';
    }

    // Canvas properties
    const strokeWidth = 12;
    const radius = 80;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    return (
        <div className="flex flex-col items-center justify-center p-6 relative">
            <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400 mb-4">
                Score de Confiance
            </h2>

            <div className="relative w-48 h-48 flex items-center justify-center">
                {/* Back Circle */}
                <svg className="absolute w-full h-full transform -rotate-90">
                    <circle
                        cx="50%"
                        cy="50%"
                        r={radius}
                        stroke="currentColor"
                        strokeWidth={strokeWidth}
                        fill="transparent"
                        className="text-slate-100"
                    />
                    {/* Progress Circle */}
                    <motion.circle
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: offset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        cx="50%"
                        cy="50%"
                        r={radius}
                        stroke="currentColor"
                        strokeWidth={strokeWidth}
                        fill="transparent"
                        strokeDasharray={circumference}
                        strokeLinecap="round"
                        className={color}
                    />
                </svg>

                {/* Text Content */}
                <div className="absolute flex flex-col items-center">
                    <motion.span
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5, duration: 0.5 }}
                        className={`text-5xl font-extrabold ${color}`}
                    >
                        {score}
                    </motion.span>
                    <span className="text-slate-400 text-sm mt-1">/ 100</span>
                </div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
                className={`mt-4 px-4 py-1.5 rounded-full text-sm font-bold bg-opacity-10 ${color.replace('text-', 'bg-')} ${color}`}
            >
                {label}
            </motion.div>
        </div>
    );
}
