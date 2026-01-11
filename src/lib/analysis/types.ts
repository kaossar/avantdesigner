export type Severity = 'low' | 'medium' | 'high' | 'critical';

export interface ExtractedClause {
    text: string;
    startIndex: number;
    endIndex: number;
}

export interface DetectedRisk {
    id: string;
    severity: Severity;
    title: string;
    description: string;
    recommendation: string;
    clause: ExtractedClause;
    source: 'rule' | 'ai'; // To distinguish between deterministic rules and AI suggestions
}

export interface AnalysisScore {
    total: number; // 0-100
    details: {
        legal: number;
        financial: number;
        clarity: number;
    };
    grade: 'A' | 'B' | 'C' | 'D' | 'F';
}

export interface AnalysisReport {
    documentId?: string;
    contractType: string; // 'housing', 'work', etc.
    score: AnalysisScore;
    risks: DetectedRisk[];
    summary: string;
    processedAt: Date;
    processingTimeMs: number;
}

// Engine Configuration
export interface AnalysisConfig {
    enableAi: boolean;
    contractType: string;
}
