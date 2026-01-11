import { NextRequest, NextResponse } from 'next/server';
import { extractTextFromPdf } from '@/lib/extraction/pdf-extractor';
import { extractTextFromDocx } from '@/lib/extraction/docx-extractor';
import { CreditManager } from '@/lib/credits/credit-manager';

export async function POST(req: NextRequest) {
    try {
        console.log('[API] Analyze Request Received');

        // 1. Verify Credits (Mock)
        // In a real app, we would get the userId from the session
        const userId = 'mock-user-id';
        const hasCredits = await CreditManager.hasCredits(userId);

        if (!hasCredits) {
            return NextResponse.json(
                { error: 'Insufficient credits' },
                { status: 403 }
            );
        }

        // 2. Parse Form Data
        const formData = await req.formData();
        const file = formData.get('file') as File | null;

        if (!file) {
            return NextResponse.json(
                { error: 'No file provided' },
                { status: 400 }
            );
        }

        console.log(`[API] Processing file: ${file.name} (${file.type})`);

        // 3. Extract Text based on mime type
        const buffer = Buffer.from(await file.arrayBuffer());
        let text = '';

        try {
            if (file.type === 'application/pdf') {
                text = await extractTextFromPdf(buffer);
            } else if (
                file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
                file.name.endsWith('.docx')
            ) {
                text = await extractTextFromDocx(buffer);
            } else {
                return NextResponse.json(
                    { error: 'Unsupported file type. Please upload PDF or DOCX.' },
                    { status: 400 }
                );
            }
        } catch (extractionError) {
            console.error('[API] Extraction failed:', extractionError);
            return NextResponse.json(
                { error: 'Failed to extract text from document.' },
                { status: 500 }
            );
        }

        if (!text || text.trim().length === 0) {
            return NextResponse.json(
                { error: 'No text extracted. The document might be an image-only PDF.' },
                { status: 422 }
            );
        }

        // 4. Deduct Credit
        await CreditManager.deductCredit(userId);

        // 5. Return Result
        return NextResponse.json({
            success: true,
            text: text,
            creditsRemaining: 99, // Mock
            message: 'Analysis successful'
        });

    } catch (error) {
        console.error('[API] Internal Error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
