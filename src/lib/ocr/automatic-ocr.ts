/**
 * Automatic OCR Service for Scanned PDFs
 * 
 * Simplified approach using Tesseract.js directly
 * For production: Would use pdf2pic for better quality
 * For MVP: Direct OCR on PDF buffer
 */

import Tesseract from 'tesseract.js';
import { writeFile, unlink, readFile } from 'fs/promises';
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
 * Simplified version - converts first page only for MVP
 */
export async function performAutomaticOCR(pdfBuffer: Buffer): Promise<OCRResult> {
    console.log('[Auto OCR] Starting automatic OCR for scanned PDF...');
    console.log('[Auto OCR] PDF size:', pdfBuffer.length, 'bytes');

    const tempDir = os.tmpdir();
    const tempPdfPath = path.join(tempDir, `pdf-ocr-${Date.now()}.pdf`);

    try {
        // Save PDF temporarily
        await writeFile(tempPdfPath, pdfBuffer);
        console.log('[Auto OCR] PDF saved to:', tempPdfPath);

        // For MVP: Use Tesseract directly on PDF
        // Tesseract.js can handle PDF directly (experimental)
        console.log('[Auto OCR] Starting Tesseract OCR...');

        const result = await Tesseract.recognize(
            tempPdfPath,
            'fra', // French
            {
                logger: (m) => {
                    if (m.status === 'recognizing text') {
                        console.log(`[Tesseract] Progress: ${(m.progress * 100).toFixed(0)}%`);
                    } else {
                        console.log(`[Tesseract] ${m.status}`);
                    }
                }
            }
        );

        console.log('[Auto OCR] ✅ OCR complete:', {
            textLength: result.data.text.length,
            confidence: result.data.confidence
        });

        // Cleanup
        await unlink(tempPdfPath).catch(() => { });

        const cleanedText = cleanOCRText(result.data.text);

        return {
            text: cleanedText,
            confidence: result.data.confidence,
            method: 'ocr',
            pageCount: 1 // MVP: single page
        };

    } catch (error: any) {
        console.error('[Auto OCR] Error:', error);

        // Cleanup on error
        await unlink(tempPdfPath).catch(() => { });

        throw new Error(`OCR failed: ${error.message}`);
    }
}

/**
 * Clean OCR text output
 */
function cleanOCRText(text: string): string {
    let cleaned = text;

    // Remove common OCR artifacts
    cleaned = cleaned.replace(/[|]/g, 'l');
    cleaned = cleaned.replace(/[\\]/g, '/');

    // Normalize whitespace
    cleaned = cleaned.replace(/[ \t]+/g, ' ');
    cleaned = cleaned.replace(/\n\s*\n\s*\n+/g, '\n\n');

    // Remove page numbers
    cleaned = cleaned.replace(/^Page\s+\d+.*$/gm, '');
    cleaned = cleaned.replace(/^\d+\s*$/gm, '');

    return cleaned.trim();
}

export function isOCRAvailable(): boolean {
    return true;
}
