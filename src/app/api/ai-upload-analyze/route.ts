import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();

        // Forward to Python Service
        const response = await fetch(`${AI_SERVICE_URL}/analyze-file`, {
            method: 'POST',
            body: formData,
            // Header is auto-managed for FormData in fetch
        });

        if (!response.ok) {
            const errorText = await response.text();
            return NextResponse.json(
                { error: 'Server Analysis Failed', details: errorText },
                { status: response.status }
            );
        }

        const result = await response.json();
        return NextResponse.json(result);

    } catch (error) {
        console.error('Upload Error:', error);
        return NextResponse.json(
            { error: 'Internal server error during upload' },
            { status: 500 }
        );
    }
}

// Allow up to 5 minutes for analysis (OCR Model Download + Processing)
export const maxDuration = 300;

export const config = {
    api: {
        bodyParser: false,
    },
};
