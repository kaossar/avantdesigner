/**
 * Professional PDF Handler with Automatic OCR Fallback
 * 
 * Workflow:
 * 1. Try native text extraction
 * 2. If scanned (text < 50 chars) → Automatic OCR
 * 3. Never block the user
 */

interface PDFProcessingResult {
    text: string;
    method: 'native' | 'ocr';
    isScanned: boolean;
    pageCount: number;
}

const TEXT_THRESHOLD = 50;

export async function processPdfDocument(buffer: Buffer): Promise<PDFProcessingResult> {
    console.log('[PDF Handler] Starting professional PDF processing...');

    // Step 1: Try native text extraction
    const nativeResult = await tryNativeExtraction(buffer);

    console.log('[PDF Handler] Detection result:', {
        textLength: nativeResult.text.length,
        isScanned: nativeResult.isScanned,
        pageCount: nativeResult.pageCount
    });

    // Step 2: Decision - Native or OCR
    if (!nativeResult.isScanned && nativeResult.text.trim().length >= TEXT_THRESHOLD) {
        // PDF has native text - use it
        console.log('[PDF Handler] ✅ Using native text extraction');
        return {
            text: nativeResult.text.trim(),
            method: 'native',
            isScanned: false,
            pageCount: nativeResult.pageCount
        };
    }

    // Step 3: PDF is scanned - Guide to client-side OCR
    console.log('[PDF Handler] ⚠️ Scanned PDF detected - OCR required');

    // For now, throw a helpful error that guides to OCR
    // Client-side will handle this and show OCR options
    throw new Error(
        'PDF_SCANNED|' +
        'Ce PDF est scanné (image). ' +
        'Veuillez utiliser l\'onglet "Scan Caméra" pour l\'OCR automatique, ' +
        'ou copier le texte manuellement dans "Coller Texte".'
    );
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
        console.error('[PDF Handler] Native extraction failed:', error);
        return {
            text: '',
            isScanned: true,
            pageCount: 0
        };
    }
}

// Legacy export for compatibility
export async function extractTextFromPdf(buffer: Buffer): Promise<string> {
    const result = await processPdfDocument(buffer);
    return result.text;
}
