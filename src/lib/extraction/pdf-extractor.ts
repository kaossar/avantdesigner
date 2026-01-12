/**
 * Professional PDF Handler with Automatic OCR
 * 
 * Workflow (Transparent to User):
 * 1. Try native text extraction
 * 2. If scanned (text < 50 chars) → Automatic OCR
 * 3. Return text seamlessly
 * 
 * NO ERRORS shown to user - everything is automatic
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

    // Step 3: PDF is scanned - Automatic OCR (ALWAYS RUNS)
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
 */
async function tryNativeExtraction(buffer: Buffer) {
    try {
        const pdfParse = await import('pdf-parse').then(m => m.default || m);
        const data = await pdfParse(buffer);

        const text = data.text || '';
        const isScanned = text.trim().length < TEXT_THRESHOLD;

        return {
            text,
            isScanned,
            pageCount: data.numpages || 0
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
