import { DetectedRisk, Severity } from '../types';

interface RuleDefinition {
    id: string;
    patterns: RegExp[];
    severity: Severity;
    title: string;
    description: string;
    recommendation: string;
}

const HOUSING_RULES: RuleDefinition[] = [
    {
        id: 'housing-refund-delay',
        patterns: [/restitution.*dépôt.*garantie.*(3|4|5|6).*mois/i, /remboursement.*caution.*(60|90).*jours/i],
        severity: 'high',
        title: 'Délai de restitution du dépôt de garantie excessif',
        description: "Le contrat mentionne un délai de restitution du dépôt de garantie supérieur à la légalité (maximum 1 mois si l'état des lieux est conforme, 2 mois sinon).",
        recommendation: "Exigez de ramener le délai à 1 mois conformément à la loi ALUR de 2014."
    },
    {
        id: 'housing-illegal-fees',
        patterns: [/frais.*dossier.*(rédaction|visite|état des lieux)/i, /chèque.*réservation/i],
        severity: 'critical',
        title: 'Frais potentiellement illégaux',
        description: "Certains frais de dossier ou de réservation exigés avant la signature ou hors agence sont strictement interdits.",
        recommendation: "Ne payez aucun frais avant la signature du bail. Vérifiez le barème légal des honoraires d'agence."
    },
    {
        id: 'housing-automatic-renewal',
        patterns: [/tacite.*reconduction.*(3|6|9|12).*ans/i],
        severity: 'medium',
        title: 'Durée de tacite reconduction à vérifier',
        description: "La tacite reconduction est standard, mais vérifiez les conditions de préavis pour le locataire (1 mois en zone tendue).",
        recommendation: "Assurez-vous que le préavis de départ est bien mentionné (1 ou 3 mois)."
    }
];

export function analyzeHousingRules(text: string): DetectedRisk[] {
    const findings: DetectedRisk[] = [];

    HOUSING_RULES.forEach(rule => {
        rule.patterns.forEach(pattern => {
            const match = pattern.exec(text);
            if (match) {
                findings.push({
                    id: rule.id,
                    severity: rule.severity,
                    title: rule.title,
                    description: rule.description,
                    recommendation: rule.recommendation,
                    clause: {
                        text: match[0],
                        startIndex: match.index,
                        endIndex: match.index + match[0].length
                    },
                    source: 'rule'
                });
            }
        });
    });

    return findings;
}
