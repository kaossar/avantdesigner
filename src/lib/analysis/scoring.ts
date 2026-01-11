import { DetectedRisk, AnalysisScore } from './types';

export function calculateScore(risks: DetectedRisk[]): AnalysisScore {
    let rawScore = 100;

    // Deduct points based on severity
    // Critical: -20, High: -10, Medium: -5, Low: -2
    risks.forEach(risk => {
        switch (risk.severity) {
            case 'critical': rawScore -= 20; break;
            case 'high': rawScore -= 10; break;
            case 'medium': rawScore -= 5; break;
            case 'low': rawScore -= 2; break;
        }
    });

    // Clamp score strictly between 0 and 100
    const finalScore = Math.max(0, Math.min(100, rawScore));

    // Determine Grade
    let grade: AnalysisScore['grade'] = 'F';
    if (finalScore >= 90) grade = 'A';
    else if (finalScore >= 80) grade = 'B';
    else if (finalScore >= 60) grade = 'C';
    else if (finalScore >= 40) grade = 'D';

    return {
        total: finalScore,
        grade,
        details: {
            // Mock sub-scores for now, can be refined based on Risk tags later
            legal: 0, // Todo
            financial: 0,
            clarity: 0
        }
    };
}
