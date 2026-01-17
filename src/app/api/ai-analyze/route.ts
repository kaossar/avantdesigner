import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { text, contract_type = 'auto' } = body;

        if (!text) {
            return NextResponse.json(
                { error: 'Text is required' },
                { status: 400 }
            );
        }

        // Call Python AI service
        const response = await fetch(`${AI_SERVICE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                contract_type
            }),
            // Timeout after 60 seconds
            signal: AbortSignal.timeout(60000),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('AI service error:', errorText);
            return NextResponse.json(
                { error: 'Analysis failed', details: errorText },
                { status: response.status }
            );
        }

        const result = await response.json();

        return NextResponse.json(result);

    } catch (error) {
        console.error('AI analysis error:', error);

        if (error instanceof Error) {
            if (error.name === 'AbortError') {
                return NextResponse.json(
                    { error: 'Analysis timeout - request took too long' },
                    { status: 504 }
                );
            }

            return NextResponse.json(
                { error: 'Internal server error', details: error.message },
                { status: 500 }
            );
        }

        return NextResponse.json(
            { error: 'Unknown error occurred' },
            { status: 500 }
        );
    }
}

export async function GET() {
    return NextResponse.json({
        status: 'ok',
        service: 'ai-analyze-proxy',
        backend: AI_SERVICE_URL
    });
}
