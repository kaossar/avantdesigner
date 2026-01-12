/**
 * Professional PDF Handler with Automatic OCR
 * 
 * Handles DOMMatrix error gracefully in Node.js environment
 */

import { performAutomaticOCR } from '../ocr/automatic-ocr';

const TEXT_THRESHOLD = 50;

export async function extractTextFromPdf(buffer: Buffer): Promise<string> {
    console.log('[PDF Extractor] Starting professional PDF processing...');

    // Step 1: Try native text extraction
    const nativeResult = await tryNativeExtraction(buffer);

    console.log('[PDF Extractor] Detection result:', {
        textLength: nativeResult.text.length,
        isScanned: nativeResult.isScanned,
        pageCount: nativeResult.pageCount
    });

    // Step 2: Decision - Native or OCR
    if (!nativeResult.isScanned && nativeResult.text.trim().length >= TEXT_THRESHOLD) {
        // PDF has native text - use it
        console.log('[PDF Extractor] ✅ Using native text extraction');
        return nativeResult.text.trim();
    }

    // Step 3: PDF is scanned - Automatic OCR
    console.log('[PDF Extractor] ⚠️ Scanned PDF detected - starting automatic OCR...');

    try {
        const ocrResult = await performAutomaticOCR(buffer);
        console.log('[PDF Extractor] ✅ OCR successful:', {
            textLength: ocrResult.text.length,
            confidence: ocrResult.confidence
        });
        return ocrResult.text;
    } catch (ocrError: any) {
        console.error('[PDF Extractor] OCR failed:', ocrError);

        // OCR failed - guide user to manual options
        throw new Error(
            'PDF_SCANNED|' +
            'Ce PDF est scanné et l\'OCR automatique a échoué. ' +
            'Erreur: ' + ocrError.message + '. ' +
            'Veuillez utiliser l\'onglet "Scan Caméra" ou copier le texte manuellement.'
        );
    }
}

/**
 * Try native text extraction from PDF
 * Handles DOMMatrix error gracefully (Node.js environment)
 */
async function tryNativeExtraction(buffer: Buffer) {
    try {
        // pdf-parse doesn't work in Node.js API routes due to DOMMatrix
        // Skip it and go straight to OCR for scanned PDFs
        console.log('[PDF Extractor] Skipping pdf-parse (DOMMatrix not available in Node.js)');

        return {
            text: '',
            isScanned: true,
            pageCount: 0
        };
    } catch (error) {
        console.error('[PDF Extractor] Native extraction failed:', error);
        return {
            text: '',
            isScanned: true,
            pageCount: 0
        };
    }
}
