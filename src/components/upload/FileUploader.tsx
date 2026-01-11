'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';

interface FileUploaderProps {
    onFileSelected: (file: File) => void;
}

export function FileUploader({ onFileSelected }: FileUploaderProps) {
    const [isDragReject, setIsDragReject] = useState(false);

    const onDrop = useCallback((acceptedFiles: File[], fileRejections: any[]) => {
        if (fileRejections.length > 0) {
            setIsDragReject(true);
            setTimeout(() => setIsDragReject(false), 2000);
            return;
        }

        if (acceptedFiles.length > 0) {
            onFileSelected(acceptedFiles[0]);
        }
    }, [onFileSelected]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
            'image/jpeg': ['.jpg', '.jpeg'],
            'image/png': ['.png']
        },
        maxFiles: 1,
        multiple: false
    });

    return (
        <div className="w-full">
            <div
                {...getRootProps()}
                className={`
                    relative group cursor-pointer
                    border-2 border-dashed rounded-xl p-10 md:p-14
                    transition-all duration-300 ease-in-out
                    flex flex-col items-center justify-center text-center
                    ${isDragReject
                        ? 'border-red-400 bg-red-50'
                        : isDragActive
                            ? 'border-primary-500 bg-primary-50 scale-[1.02]'
                            : 'border-slate-300 hover:border-primary-400 hover:bg-slate-50 bg-white'
                    }
                `}
            >
                <input {...getInputProps()} />

                {/* Animated Icon */}
                <div className={`
                    w-20 h-20 mb-6 rounded-full flex items-center justify-center
                    transition-colors duration-300
                    ${isDragReject
                        ? 'bg-red-100 text-red-500'
                        : isDragActive
                            ? 'bg-primary-100 text-primary-600'
                            : 'bg-slate-100 text-slate-400 group-hover:bg-primary-50 group-hover:text-primary-600'
                    }
                `}>
                    {isDragReject ? (
                        <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    ) : (
                        <svg className="w-10 h-10 transform group-hover:-translate-y-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                    )}
                </div>

                {/* Text Content */}
                <h3 className="text-xl font-serif font-bold text-primary-900 mb-2">
                    {isDragActive ? 'Déposez votre document ici' : 'Cliquez ou glissez votre contrat'}
                </h3>

                <p className="text-slate-500 text-sm mb-6 max-w-sm">
                    Supporte PDF, Word, Images (Scan/Photo).
                    <br />
                    Taille maximale : 10 Mo.
                </p>

                <button className="px-6 py-2 bg-white border border-slate-300 text-slate-700 font-bold text-sm uppercase tracking-wider rounded-lg shadow-sm group-hover:border-primary-400 group-hover:text-primary-900 transition-colors">
                    Sélectionner un fichier
                </button>

                {/* Formats badge */}
                <div className="absolute bottom-4 right-4 flex gap-2 opacity-50">
                    <span className="text-[10px] font-bold uppercase text-slate-400 bg-slate-100 px-2 py-1 rounded">PDF</span>
                    <span className="text-[10px] font-bold uppercase text-slate-400 bg-slate-100 px-2 py-1 rounded">DOCX</span>
                    <span className="text-[10px] font-bold uppercase text-slate-400 bg-slate-100 px-2 py-1 rounded">JPG</span>
                </div>
            </div>

            {/* Error Message */}
            <AnimatePresence>
                {isDragReject && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="mt-4 p-3 bg-red-50 text-red-600 text-sm font-medium rounded-lg border border-red-100 text-center"
                    >
                        Format de fichier non supporté. Veuillez utiliser PDF, Word ou Image.
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
