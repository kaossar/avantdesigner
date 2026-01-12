/**
 * Automatic OCR Service for Scanned PDFs
 * 
 * Server-side OCR using Tesseract.js with explicit worker configuration
 */

import { createWorker } from 'tesseract.js';
import { writeFile, unlink } from 'fs/promises';
import path from 'path';
import os from 'os';

interface OCRResult {
    text: string;
    confidence: number;
    method: 'ocr';
    pageCount: number;
}

/**
 * Perform automatic OCR on a scanned PDF
 * Configured worker path for Next.js
 */
export async function performAutomaticOCR(pdfBuffer: Buffer): Promise<OCRResult> {
    console.log('[Auto OCR] Starting automatic OCR for scanned PDF...');
    console.log('[Auto OCR] PDF size:', pdfBuffer.length, 'bytes');

    const tempDir = os.tmpdir();
    const tempPdfPath = path.join(tempDir, `pdf-ocr-${Date.now()}.pdf`);

    let worker;

    try {
        // Save PDF temporarily
        await writeFile(tempPdfPath, pdfBuffer);
        console.log('[Auto OCR] PDF saved to:', tempPdfPath);

        // Create Tesseract worker with explicit paths for Next.js
        console.log('[Auto OCR] Creating Tesseract worker with custom config...');

        // Get the correct node_modules path
        const nodeModulesPath = path.join(process.cwd(), 'node_modules');
        const workerPath = path.join(nodeModulesPath, 'tesseract.js', 'src', 'worker-script', 'node', 'index.js');
        const langPath = path.join(nodeModulesPath, 'tesseract.js-languages', 'fra.traineddata.gz');

        console.log('[Auto OCR] Worker path:', workerPath);
        console.log('[Auto OCR] Lang path:', langPath);

        worker = await createWorker('fra', 1, {
            workerPath: workerPath,
            langPath: langPath,
            logger: (m) => {
                if (m.status === 'recognizing text') {
                    console.log(`[Tesseract] Progress: ${(m.progress * 100).toFixed(0)}%`);
                } else if (m.status) {
                    console.log(`[Tesseract] ${m.status}`);
                }
            },
        });

        console.log('[Auto OCR] Worker created, starting recognition...');

        // Recognize text from PDF
        const { data } = await worker.recognize(tempPdfPath);

        console.log('[Auto OCR] ✅ OCR complete:', {
            textLength: data.text.length,
            confidence: data.confidence
        });

        // Cleanup
        await worker.terminate();
        await unlink(tempPdfPath).catch(() => { });

        const cleanedText = cleanOCRText(data.text);

        if (cleanedText.length < 50) {
            throw new Error('OCR produced very little text. PDF may be empty or unreadable.');
        }

        return {
            text: cleanedText,
            confidence: data.confidence,
            method: 'ocr',
            pageCount: 1
        };

    } catch (error: any) {
        console.error('[Auto OCR] Error:', error);

        // Cleanup on error
        if (worker) {
            await worker.terminate().catch(() => { });
        }
        await unlink(tempPdfPath).catch(() => { });

        throw new Error(`OCR failed: ${error.message}`);
    }
}

function cleanOCRText(text: string): string {
    let cleaned = text;
    cleaned = cleaned.replace(/[|]/g, 'l');
    cleaned = cleaned.replace(/[\\]/g, '/');
    cleaned = cleaned.replace(/[ \t]+/g, ' ');
    cleaned = cleaned.replace(/\n\s*\n\s*\n+/g, '\n\n');
    cleaned = cleaned.replace(/^Page\s+\d+.*$/gm, '');
    cleaned = cleaned.replace(/^\d+\s*$/gm, '');
    return cleaned.trim();
}

export function isOCRAvailable(): boolean {
    return true;
}
