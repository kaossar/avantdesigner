import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();

        console.log('🔵 [Next.js Route] Forwarding OCR request to Python backend...');

        // Forward to Python Service with extended timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes

        const response = await fetch(`${AI_SERVICE_URL}/extract-text`, {
            method: 'POST',
            body: formData,
            signal: controller.signal,
            // @ts-ignore - Undici-specific options
            headersTimeout: 60000, // 60 seconds for headers
            bodyTimeout: 300000,   // 5 minutes for body
        });

        clearTimeout(timeoutId);

        console.log('🟢 [Next.js Route] Received OCR response from Python:', response.status, response.headers.get('content-type'));

        if (!response.ok) {
            const errorText = await response.text();
            return NextResponse.json(
                { error: 'OCR Failed', details: errorText },
                { status: response.status }
            );
        }

        // Return the stream directly to the client
        return new Response(response.body, {
            status: 200,
            headers: {
                'Content-Type': 'application/x-ndjson',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            },
        });

    } catch (error) {
        console.error('OCR Error:', error);
        return NextResponse.json(
            { error: 'Internal server error during OCR' },
            { status: 500 }
        );
    }
}

// Allow up to 5 minutes for OCR processing
export const maxDuration = 300;
