import { AnalysisReport, AnalysisConfig, DetectedRisk } from './types';
import { calculateScore } from './scoring';
import { analyzeHousingRules } from './rules/housing';

import { AiService } from './ai-service';

export class AnalysisEngine {
    static async analyze(text: string, config: AnalysisConfig): Promise<AnalysisReport> {
        const startTime = Date.now();
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
}
