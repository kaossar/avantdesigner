export type Severity = 'low' | 'medium' | 'high' | 'critical';
export type RiskLevel = 'low' | 'medium' | 'high';

export interface ExtractedClause {
    text: string;
    startIndex: number;
    endIndex: number;
}

export interface DetectedRisk {
    clause_number?: number;
    clause_type?: string;
    clause_preview?: string;
    issue?: string;
    severity: Severity;
    recommendation: string;
    // Legacy/Optional fields
    id?: string;
    title?: string;
    description?: string;
    clause?: ExtractedClause;
    source?: 'rule' | 'ai';
}

export interface Recommendation {
    priority: 'urgent' | 'important' | 'info';
    action: string;
    detail: string;
}

// ... (other interfaces)

export interface AnalysisReport {
    documentId?: string;
    contractType: string;
    score: AnalysisScore;
    risks: DetectedRisk[];
    recommendations?: Recommendation[]; // Added missing field
    summary: string;
    clauses?: AnalyzedClause[];
    entities?: ExtractedEntities;
    metadata?: AnalysisMetadata;
    processedAt?: Date;
    processingTimeMs?: number;
}
export interface LegalReference {
    source: string;        // "Loi 89-462" or "Code Civil"
    article: string;       // "Article 22"
    title: string;         // Article title
    summary: string;       // Article summary
    relevance?: string;    // Relevance percentage (from semantic search)
}

// Analyzed Clause (from Python backend)
export interface AnalyzedClause {
    clause_number: number;
    clause_text: string;
    clause_type: string;
    resume: string;
    implications: string;
    risques: string;
    conformite: string;
    recommandation: string;
    risk_level: RiskLevel;
    legal_references?: LegalReference[];
    legal_context?: string;
    search_method?: 'semantic' | 'keyword';
}

// Extracted Entities
export interface ExtractedEntities {
    parties?: string[];
    montants?: string[];
    dates?: string[];
    durees?: string[];
}

// Analysis Metadata
export interface AnalysisMetadata {
    total_clauses?: number;
    analyzed_clauses?: number;
    high_risk_count?: number;
    medium_risk_count?: number;
    low_risk_count?: number;
    search_method?: string;
    cleaning_stats?: any;
}

export interface AnalysisScore {
    total: number; // 0-100
    conformity?: number;
    balance?: number;
    clarity?: number;
    details?: {
        legal?: number;
        financial?: number;
        clarity?: number;
        total_clauses?: number;
        high_risks?: number;
        medium_risks?: number;
        low_risks?: number;
    };
    grade?: 'A' | 'B' | 'C' | 'D' | 'F';
}

export interface AnalysisReport {
    documentId?: string;
    contractType: string;
    score: AnalysisScore;
    risks: DetectedRisk[];
    recommendations?: Recommendation[];
    summary: string;
    clauses?: AnalyzedClause[];
    entities?: ExtractedEntities;
    metadata?: AnalysisMetadata;
    processedAt?: Date;
    processingTimeMs?: number;
}

// Engine Configuration
export interface AnalysisConfig {
    enableAi: boolean;
    contractType: string;
}
