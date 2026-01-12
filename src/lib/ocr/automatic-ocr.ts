/**
 * Automatic OCR Service for Scanned PDFs
 * 
 * Simplified approach - uses Tesseract.js default configuration
 * Works in Next.js API routes
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
 * Simplified - uses Tesseract defaults
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

        // Create Tesseract worker - simplified config
        console.log('[Auto OCR] Creating Tesseract worker...');

        worker = await createWorker({
            logger: (m) => {
                console.log(`[Tesseract] ${m.status}: ${m.progress ? (m.progress * 100).toFixed(0) + '%' : ''}`);
            },
        });

        console.log('[Auto OCR] Loading French language...');
        await worker.loadLanguage('fra');
        await worker.initialize('fra');

        console.log('[Auto OCR] Worker ready, starting recognition...');

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
