import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();

        console.log('🔵 [Next.js Route] Forwarding request to Python backend...');

        // Forward to Python Service with extended timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes

        const response = await fetch(`${AI_SERVICE_URL}/analyze-file`, {
            method: 'POST',
            body: formData,
            signal: controller.signal,
            // @ts-ignore - Undici-specific options
            headersTimeout: 60000, // 60 seconds for headers
            bodyTimeout: 300000,   // 5 minutes for body
        });

        clearTimeout(timeoutId);

        console.log('🟢 [Next.js Route] Received response from Python:', response.status, response.headers.get('content-type'));

        if (!response.ok) {
            const errorText = await response.text();
            return NextResponse.json(
                { error: 'Server Analysis Failed', details: errorText },
                { status: response.status }
            );
        }

        // Return the stream directly to the client
        // This enables real-time progress updates (NDJSON)
        return new Response(response.body, {
            status: 200,
            headers: {
                'Content-Type': 'application/x-ndjson',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            },
        });

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


