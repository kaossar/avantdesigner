import { NextRequest, NextResponse } from 'next/server';

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
    try {
        const { text } = await request.json();

        if (!text || text.trim().length < 50) {
            return NextResponse.json(
                { error: 'Le texte est trop court pour être analysé' },
                { status: 400 }
            );
        }

        console.log('[AI] Envoi au service Python IA...');
        console.log(`[AI] Texte: ${text.length} caractères`);

        // Call Python AI service
        const response = await fetch(`${AI_SERVICE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                text,
                contract_type: 'auto'
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('[AI] Service error:', response.status, errorText);
            throw new Error(`AI service error: ${response.status}`);
        }

        const analysis = await response.json();

        console.log('[AI] Analyse terminée:', {
            type: analysis.contract_type,
            clauses: analysis.clauses?.length || 0,
            risks: analysis.risks?.length || 0,
            score: analysis.score?.global || 0
        });

        // Transform to match existing frontend format
        return NextResponse.json({
            text: text,
            data: {
                contractType: analysis.contract_type,
                summary: analysis.summary,
                score: analysis.score?.global || 0,
                risks: analysis.risks || [],
                clauses: analysis.clauses || [],
                recommendations: analysis.recommendations || [],
                metadata: analysis.metadata || {}
            }
        });

    } catch (error: any) {
        console.error('[AI] Erreur:', error);

        // Fallback to existing analysis if AI service is down
        return NextResponse.json(
            {
                error: 'Service IA temporairement indisponible',
                details: error.message,
                fallback: true
            },
            { status: 503 }
        );
    }
}
