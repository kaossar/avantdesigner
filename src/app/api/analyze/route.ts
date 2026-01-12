import { NextRequest, NextResponse } from 'next/server';
import { extractTextFromDocument } from '@/lib/extraction/universal-extractor';
import { CreditManager } from '@/lib/credits/credit-manager';

export async function POST(req: NextRequest) {
    try {
        console.log('[API] Analyze Request Received');

        // 1. Verify Credits (Mock)
        const userId = 'mock-user-id';
        const hasCredits = await CreditManager.hasCredits(userId);

        if (!hasCredits) {
            return NextResponse.json(
                { error: 'Insufficient credits' },
                { status: 403 }
            );
        }

        // 2. Parse Form Data
        console.log('[API Debug] Parsing FormData...');
        let formData;
        try {
            formData = await req.formData();
        } catch (e) {
            console.error('[API Debug] FormData Parsing Failed:', e);
            return NextResponse.json({ error: 'Invalid Form Data' }, { status: 400 });
        }

        const file = formData.get('file') as File | null;

        if (!file) {
            console.log('[API Debug] No file found');
            return NextResponse.json(
                { error: 'No file provided' },
                { status: 400 }
            );
        }

        console.log(`[API] Processing file: ${file.name} (${file.type})`);

        // 3. Extract Text using Universal Extractor
        console.log('[API Debug] Extracting text with universal extractor...');
        const buffer = Buffer.from(await file.arrayBuffer());
        let text = '';

        try {
            // Handle text files directly
            if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
                text = buffer.toString('utf-8');
                console.log('[API Debug] Text file processed directly');
            }
            // Use universal extractor for all other formats (PDF, DOCX, etc.)
            // Note: OCR is only available for images via client-side Tesseract
            else {
                text = await extractTextFromDocument(buffer, file.name);
            }
        } catch (extractionError: any) {
            console.error('[API Debug] Extraction failed:', extractionError);

            // Special handling for scanned PDFs
            if (extractionError.message?.includes('PDF_SCANNED')) {
                const message = extractionError.message.split('|')[1] || 'PDF scanné détecté';
                return NextResponse.json(
                    {
                        error: 'PDF_SCANNED',
                        message: message,
                        text: '',
                        suggestions: [
                            'Utilisez l\'onglet "Scan Caméra" pour l\'OCR automatique',
                            'Ou copiez le texte manuellement dans "Coller Texte"',
                            'Ou convertissez le PDF en DOCX'
                        ]
                    },
                    { status: 400 }
                );
            }

            return NextResponse.json(
                {
                    error: extractionError.message || 'Failed to extract text from document.',
                    details: process.env.NODE_ENV === 'development' ? extractionError.stack : undefined
                },
                { status: 500 }
            );
        }

        console.log('[API Debug] Text extracted, length:', text.length);

        if (!text || text.trim().length === 0) {
            return NextResponse.json(
                { error: 'No text extracted.' },
                { status: 422 }
            );
        }

        // 4. Deduct Credit
        await CreditManager.deductCredit(userId);

        // 5. Analyze Logic
        const contractType = 'housing';

        console.log('[API Debug] Loading AnalysisEngine...');
        const { AnalysisEngine } = require('@/lib/analysis/engine');

        const enableAi = !!process.env.HUGGINGFACE_API_KEY;
        console.log('[API Debug] Enable AI:', enableAi);

        console.log('[API Debug] Starting Analysis...');
        const report = await AnalysisEngine.analyze(text, {
            contractType,
            enableAi
        });
        console.log('[API Debug] Analysis Complete');

        // 6. Return Result
        return NextResponse.json({
            success: true,
            data: report,
            text: text,
            creditsRemaining: 99,
            message: 'Analysis successful'
        });

    } catch (error: any) {
        console.error('[API] Internal Error Stack:', error);

        // Handle Validation Errors (e.g. "Le document ne semble pas être un contrat")
        const errorMessage = error instanceof Error ? error.message : 'Une erreur inconnue est survenue';

        // If it's a known validation error, return 400 with the message
        return NextResponse.json(
            { error: errorMessage },
            { status: 400 }
        );
    }
}
