'use client';

import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';

interface CameraScannerProps {
    onCapture: (imageSrc: string) => void;
    onCancel: () => void;
}

export function CameraScanner({ onCapture, onCancel }: CameraScannerProps) {
    const webcamRef = useRef<Webcam>(null);
    const [capturedImage, setCapturedImage] = useState<string | null>(null);

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current?.getScreenshot();
        if (imageSrc) {
            setCapturedImage(imageSrc);
        }
    }, [webcamRef]);

    const retake = () => {
        setCapturedImage(null);
    };

    const confirm = () => {
        if (capturedImage) {
            onCapture(capturedImage);
        }
    };

    return (
        <div className="flex flex-col items-center w-full max-w-2xl mx-auto">
            <div className="relative w-full aspect-video bg-black rounded-xl overflow-hidden shadow-2xl border-4 border-slate-200">
                {!capturedImage ? (
                    <>
                        <Webcam
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            videoConstraints={{ facingMode: "environment" }}
                            className="w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 border-2 border-white/30 m-8 rounded-lg pointer-events-none flex items-center justify-center">
                            <div className="text-white/50 text-sm font-bold uppercase tracking-widest bg-black/50 px-3 py-1 rounded">
                                Cadrez le document
                            </div>
                        </div>
                    </>
                ) : (
                    <img src={capturedImage} alt="Captured" className="w-full h-full object-cover" />
                )}
            </div>

            <div className="flex gap-4 mt-8">
                {!capturedImage ? (
                    <>
                        <Button variant="ghost" onClick={onCancel}>Annuler</Button>
                        <Button
                            onClick={capture}
                            className="bg-red-600 hover:bg-red-700 text-white rounded-full w-16 h-16 flex items-center justify-center p-0 shadow-xl border-4 border-white ring-2 ring-red-100"
                        >
                            <div className="w-4 h-4 bg-white rounded-full"></div>
                        </Button>
                        <div className="w-20"></div> {/* Spacer for alignment */}
                    </>
                ) : (
                    <>
                        <Button variant="outline" onClick={retake}>Reprendre</Button>
                        <Button onClick={confirm}>Valider la photo</Button>
                    </>
                )}
            </div>
        </div>
    );
}
