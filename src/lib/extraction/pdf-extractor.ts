export async function extractTextFromPdf(buffer: Buffer): Promise<string> {
    console.log('[PDF Extractor] Starting pdf-parse extraction...');

    try {
        // pdf-parse v1.1.1 usage: just call the module as a function
        const pdfParse = require('pdf-parse');

        // Call it directly - it's the default export
        const data = await pdfParse(buffer);

        console.log('[PDF Extractor] Extraction complete:', {
            pages: data.numpages,
            textLength: data.text?.length
        });

        if (data.text && data.text.trim().length > 50) {
            return data.text.trim();
        }

        throw new Error('PDF semble vide ou scanné. Utilisez l\'onglet "Scan Caméra" pour l\'OCR.');

    } catch (error: any) {
        console.error('[PDF Extractor] Error:', error);

        // If it's our own error, rethrow it
        if (error.message?.includes('PDF semble vide')) {
            throw error;
        }

        // Otherwise, it's a pdf-parse error
        throw new Error(
            `Impossible de lire ce PDF (${error.message}). ` +
            'Solutions: 1) Convertir en DOCX avec Word, 2) Copier le texte, 3) Utiliser Scan Caméra'
        );
    }
}
