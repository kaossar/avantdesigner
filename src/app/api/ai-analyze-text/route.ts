import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();

        console.log('🔵 [Next.js Route] Forwarding analysis request to Python backend...');

        const response = await fetch(`${AI_SERVICE_URL}/analyze-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        console.log('🟢 [Next.js Route] Received analysis response from Python:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            return NextResponse.json(
                { error: 'Analysis Failed', details: errorText },
                { status: response.status }
            );
        }

        const result = await response.json();
        return NextResponse.json(result);

    } catch (error) {
        console.error('Analysis Error:', error);
        return NextResponse.json(
            { error: 'Internal server error during analysis' },
            { status: 500 }
        );
    }
}

// Allow up to 5 minutes for AI analysis
export const maxDuration = 300;
