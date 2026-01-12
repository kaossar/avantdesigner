/**
 * Automatic OCR Service for Scanned PDFs
 * 
 * Professional workflow:
 * 1. Convert PDF pages to images (pdf2pic)
 * 2. Preprocess images (optional: binarization, deskew)
 * 3. Perform OCR with Tesseract.js
 * 4. Clean and normalize text
 * 
 * Completely transparent to user
 */

import { fromBuffer } from 'pdf2pic';
import Tesseract from 'tesseract.js';
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
 * Main entry point - completely transparent
 */
export async function performAutomaticOCR(pdfBuffer: Buffer): Promise<OCRResult> {
    console.log('[Auto OCR] Starting automatic OCR for scanned PDF...');

    const tempDir = os.tmpdir();
    const tempPdfPath = path.join(tempDir, `pdf-${Date.now()}.pdf`);

    try {
        // Step 1: Save PDF to temp file (required by pdf2pic)
        await writeFile(tempPdfPath, pdfBuffer);
        console.log('[Auto OCR] PDF saved to temp:', tempPdfPath);

        // Step 2: Convert PDF to images
        const images = await convertPdfToImages(tempPdfPath);
        console.log(`[Auto OCR] Converted ${images.length} pages to images`);

        // Step 3: Perform OCR on each page
        const pageTexts: string[] = [];
        let totalConfidence = 0;

        for (let i = 0; i < images.length; i++) {
            console.log(`[Auto OCR] Processing page ${i + 1}/${images.length}...`);

            const result = await performOCROnImage(images[i]);
            pageTexts.push(result.text);
            totalConfidence += result.confidence;

            // Cleanup image file
            await unlink(images[i]).catch(() => { });
        }

        // Step 4: Combine and clean text
        const combinedText = pageTexts.join('\n\n');
        const cleanedText = cleanOCRText(combinedText);

        const avgConfidence = images.length > 0 ? totalConfidence / images.length : 0;

        console.log('[Auto OCR] ✅ OCR complete:', {
            pages: images.length,
            textLength: cleanedText.length,
            avgConfidence: avgConfidence.toFixed(2)
        });

        // Cleanup temp PDF
        await unlink(tempPdfPath).catch(() => { });

        return {
            text: cleanedText,
            confidence: avgConfidence,
            method: 'ocr',
            pageCount: images.length
        };

    } catch (error: any) {
        console.error('[Auto OCR] Error:', error);

        // Cleanup on error
        await unlink(tempPdfPath).catch(() => { });

        throw new Error(`OCR failed: ${error.message}`);
    }
}

/**
 * Convert PDF to images using pdf2pic
 */
async function convertPdfToImages(pdfPath: string): Promise<string[]> {
    const options = {
        density: 300,           // DPI (higher = better quality, slower)
        saveFilename: `page-${Date.now()}`,
        savePath: os.tmpdir(),
        format: 'png',
        width: 2480,           // A4 at 300 DPI
        height: 3508
    };

    const convert = fromBuffer(await import('fs').then(fs => fs.promises.readFile(pdfPath)), options);

    // Convert all pages
    const results = await convert.bulk(-1, { responseType: 'image' });

    return results.map(r => r.path);
}

/**
 * Perform OCR on a single image
 */
async function performOCROnImage(imagePath: string): Promise<{ text: string; confidence: number }> {
    const result = await Tesseract.recognize(
        imagePath,
        'fra', // French language
        {
            logger: (m) => {
                if (m.status === 'recognizing text') {
                    console.log(`[Tesseract] Progress: ${(m.progress * 100).toFixed(0)}%`);
                }
            }
        }
    );

    return {
        text: result.data.text,
        confidence: result.data.confidence
    };
}

/**
 * Clean OCR text output
 * - Remove artifacts
 * - Fix common OCR errors
 * - Normalize whitespace
 */
function cleanOCRText(text: string): string {
    let cleaned = text;

    // Remove common OCR artifacts
    cleaned = cleaned.replace(/[|]/g, 'l'); // Pipe to lowercase L
    cleaned = cleaned.replace(/[\\]/g, '/'); // Backslash to forward slash

    // Fix common French OCR errors
    cleaned = cleaned.replace(/\bà\b/g, 'à');
    cleaned = cleaned.replace(/\bé\b/g, 'é');

    // Normalize whitespace
    cleaned = cleaned.replace(/[ \t]+/g, ' '); // Multiple spaces to single
    cleaned = cleaned.replace(/\n\s*\n\s*\n+/g, '\n\n'); // Multiple newlines to double

    // Remove page numbers and headers/footers artifacts
    cleaned = cleaned.replace(/^Page\s+\d+.*$/gm, '');
    cleaned = cleaned.replace(/^\d+\s*$/gm, '');

    // Trim
    cleaned = cleaned.trim();

    return cleaned;
}

/**
 * Check if OCR is available and configured
 */
export function isOCRAvailable(): boolean {
    // OCR is always available with tesseract.js
    // But we can add checks for optimal configuration
    return true;
}
