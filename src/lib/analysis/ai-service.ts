import { HfInference } from '@huggingface/inference';
import { DetectedRisk } from './types';

// Use environment variable or a default placeholder (User needs to set this)
const HF_TOKEN = process.env.HUGGINGFACE_API_KEY;

export class AiService {
    private static hf = new HfInference(HF_TOKEN);

    static async analyzeWithAI(text: string, contractType: string): Promise<DetectedRisk[]> {
        if (!HF_TOKEN) {
            console.warn("⚠️ HUGGINGFACE_API_KEY missing. AI analysis skipped.");
            return [];
        }

        console.log("🤖 Starting AI Analysis (Mistral-7B)...");

        // Truncate text to avoid token limits (approx 1500 words / 6000 chars for safety on free tier)
        const truncatedText = text.slice(0, 6000);

        const prompt = `
Tu es un avocat expert en droit des contrats français.
Analyse la clause ou le contrat suivant (Type: ${contractType}).
Identifie les risques juridiques majeurs, les clauses abusives ou les ambiguïtés.

Texte du contrat :
"""
${truncatedText}
"""

Format de réponse attendu (JSON uniquement, sans markdown) :
[
  {
    "title": "Titre court du risque",
    "description": "Explication juridique précise du problème",
    "severity": "high" | "medium" | "low",
    "recommendation": "Conseil pour corriger ou négocier",
    "quote": "Citation exacte du passage problématique"
  }
]
Si aucun risque n'est trouvé, renvoie [].
Réponds uniquement avec le JSON valide.
`;

        try {
            // Promise.race to enforce a 10s timeout for "Efficiency"
            const aiCall = this.hf.chatCompletion({
                model: "mistralai/Mistral-7B-Instruct-v0.2",
                messages: [
                    { role: "user", content: prompt }
                ],
                max_tokens: 1000,
                temperature: 0.1
            });

            const timeoutPromise = new Promise((_, reject) =>
                setTimeout(() => reject(new Error("AI Timeout")), 10000)
            );

            // Use type assertion to handle the race result
            const raceResult: any = await Promise.race([aiCall, timeoutPromise]);
            const content = raceResult.choices[0].message.content || "[]";

            // Cleanup formatting
            const cleanJson = content.replace(/```json/g, '').replace(/```/g, '').trim();
            const rawRisks = JSON.parse(cleanJson);

            // Map to DetectedRisk
            return rawRisks.map((r: any, index: number) => ({
                id: `ai-risk-${index}-${Date.now()}`,
                severity: r.severity || 'medium',
                title: r.title || 'Risque détecté par IA',
                description: r.description || '',
                recommendation: r.recommendation || '',
                clause: {
                    text: r.quote || 'Contexte global',
                    startIndex: 0,
                    endIndex: 0
                },
                source: 'ai'
            }));

        } catch (error) {
            console.error("❌ AI Analysis Failed or Timed Out:", error);
            // Non-blocking: return empty so Rules still work
            return [];
        }
    }
}
