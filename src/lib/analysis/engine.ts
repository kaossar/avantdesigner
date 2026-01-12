import { AnalysisReport, AnalysisConfig, DetectedRisk } from './types';
import { calculateScore } from './scoring';
import { analyzeHousingRules } from './rules/housing';

import { AiService } from './ai-service';

export class AnalysisEngine {
    static async analyze(text: string, config: AnalysisConfig): Promise<AnalysisReport> {
        const startTime = Date.now();

        // 0. Relevance Check (Is this a contract?)
        const relevanceCheck = this.validateContractRelevance(text);
        if (!relevanceCheck.isValid) {
            console.warn("[AnalysisEngine] Document Rejected:", relevanceCheck.reason);
            // We can either throw or return a low-score report.
            // Throwing enables the UI to show a specific error message easily.
            throw new Error("Le document ne semble pas être un contrat valide. " + relevanceCheck.reason);
        }

        const allRisks: DetectedRisk[] = [];

        // 1. Deterministic Rule Analysis (The "Clinical" Layer)
        // Select rule set based on contract type
        if (config.contractType === 'housing' || config.contractType === 'baux') {
            const housingRisks = analyzeHousingRules(text);
            allRisks.push(...housingRisks);
        } else {
            // Default / Fallback rules (Mental check: "Tacite reconduction" is common)
            // For now, if type is unknown, we might run generic rules.
            // allRisks.push(...analyzeGenericRules(text));
        }

        // 2. AI Analysis (The "Open Source" Layer) - To be plugged in here
        if (config.enableAi) {
            const aiRisks = await AiService.analyzeWithAI(text, config.contractType);
            allRisks.push(...aiRisks);
        }

        // 3. Scoring
        const score = calculateScore(allRisks);

        const endTime = Date.now();

        return {
            contractType: config.contractType,
            score,
            risks: allRisks,
            summary: `Analyse terminée. ${allRisks.length} points d'attention détectés.`,
            processedAt: new Date(),
            processingTimeMs: endTime - startTime
        };
    }

    private static validateContractRelevance(text: string): { isValid: boolean, reason?: string } {
        const lowerText = text.toLowerCase();

        // List of strong indicators
        const legalKeywords = [
            'contrat', 'bail', 'convention', 'accord',
            'article', 'parties', 'signature', 'loi',
            'code civil', 'conditions générales', 'loyer',
            'prix', 'durée', 'résiliation', 'objet',
            'entre les soussignés'
        ];

        // Check for at least 3 keyword matches (to avoid false positives on random text containing 'prix')
        let matchCount = 0;
        for (const keyword of legalKeywords) {
            if (lowerText.includes(keyword)) {
                matchCount++;
            }
        }

        if (text.length < 50) {
            return { isValid: false, reason: "Le texte est trop court pour être analysé." };
        }

        if (matchCount < 2) {
            return { isValid: false, reason: "Aucun vocabulaire juridique détecté." };
        }

        return { isValid: true };
    }
}
