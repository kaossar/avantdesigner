import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();

        // Call Python AI service
        const response = await fetch(`${AI_SERVICE_URL}/export-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
            // Timeout after 30 seconds
            signal: AbortSignal.timeout(30000),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('PDF service error:', errorText);
            return NextResponse.json(
                { error: 'PDF generation failed', details: errorText },
                { status: response.status }
            );
        }

        // Get PDF blob
        const blob = await response.blob();

        // Return PDF with correct headers
        return new NextResponse(blob, {
            status: 200,
            headers: {
                'Content-Type': 'application/pdf',
                'Content-Disposition': response.headers.get('Content-Disposition') || 'attachment; filename=report.pdf',
            },
        });

    } catch (error) {
        console.error('PDF export error:', error);

        if (error instanceof Error) {
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
