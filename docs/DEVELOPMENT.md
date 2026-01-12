# AvantDeSigner - Guide de Développement

## 🚀 Démarrage Rapide

```bash
# Installation
npm install

# Développement
npm run dev

# Build de production
npm run build

# Lancer en production
npm start
```

## 📋 État d'Avancement du Projet

### ✅ Phases Complétées

#### Phase 1 : Initialisation & Configuration
- ✅ Projet Next.js 14+ avec TypeScript
- ✅ Structure de dossiers modulaire
- ✅ Toutes les dépendances installées
- ✅ Design system Tailwind configuré
- ✅ Variables d'environnement

#### Phase 2 : Design System & UI
- ✅ Design system complet (couleurs, typo, animations)
- ✅ Composants UI de base :
  - Button (6 variantes)
  - Card (avec sous-composants)
  - Badge (niveaux de risque)
  - Input (avec labels/erreurs)
  - Modal (avec animations)
- ✅ Header avec navigation
- ✅ Footer avec liens légaux
- ✅ Design responsive

#### Phase 3 : Page d'Accueil
- ✅ Hero section avec animations
- ✅ Section "Comment ça marche" (3 étapes)
- ✅ Types de contrats supportés
- ✅ FAQ avec accordéon
- ✅ SEO metadata optimisée

### 🚧 Phases Restantes

#### Phase 4 : Upload & Scan de Documents (Frontend ✅)
- ✅ Interface d'upload multi-format
- ✅ Drag & drop
- ✅ Scanner caméra (mobile/desktop)
- ✅ Intégration Tesseract.js OCR
- ✅ Prévisualisation

#### Phase 5 : Backend & API (Terminé ✅)
- ✅ API d'analyse `/api/analyze`
- ✅ Extraction PDF (pdf-parse)
- ✅ Extraction DOCX (mammoth)
- ✅ Vérification Crédits (Structure Mock en place)
- ✅ Routing API configuré (`src/app/api/...`)

#### Phase 6 : Moteur d'Analyse (Terminé ✅)
- ✅ Moteur Hybride : Règles Déterministes + IA
- ✅ Règles "Housing" codées (Regex pour frais, délais, etc.)
- ✅ Service IA via **Hugging Face Inference API**
    - Utilise le modèle **Mistral-7B-Instruct** (Open Source)
    - Analyse les subtilités et ambiguïtés
    - Fallback automatique sur les règles si l'IA échoue
- ✅ Système de Scoring (Trusted Score)

#### Phase 7 : Version Expert IA-First (En Cours 🔥)

**Objectif** : Transformer "Analyser mon contrat" en outil expert avec IA au cœur du produit

**Architecture** : Pipeline IA complet (OCR → Nettoyage → Chunking → Analyse Multi-Modèles → RAG → Export)

##### 7.1 Infrastructure IA (Sprint 1 - 3-4 jours) ✅
- [x] Service Python FastAPI (`python-ai/main.py`)
  - [x] API `/analyze` avec CORS pour Next.js
  - [x] Health check endpoint
  - [x] Gestion des erreurs
- [x] Pipeline IA complet (`python-ai/pipeline.py`)
  - [x] Nettoyage intelligent du texte (règles MVP)
  - [x] Chunking par clause (regex + paragraphes)
  - [x] Classification type de contrat (règles)
  - [x] NER juridique (extraction montants, dates, parties)
  - [x] Analyse clause par clause (règles MVP)
  - [x] Score de risque multi-axes
  - [x] Génération recommandations
- [x] Configuration modèles Hugging Face (version légère)
  - [ ] Mistral-7B-Instruct-v0.2 (LLM principal) - Sprint 3
  - [ ] CamemBERT (classification + NER) - Sprint 3
  - [ ] BARThez (résumé) - Sprint 3
  - [ ] Sentence-Transformers (RAG) - Sprint 3
- [x] Fichier `requirements.txt` complet
  - [x] fastapi, uvicorn
  - [x] pdfplumber (Sprint 2)
  - [ ] transformers, torch, accelerate - Sprint 3
  - [ ] langchain, sentence-transformers - Sprint 3
  - [ ] spacy, faiss-cpu - Sprint 3

##### 7.2 Pipeline Professionnel (Sprint 2 - Terminé ✅)
- [x] Validation fichiers (`utils/validator.py`)
  - [x] Vérification taille (50MB max)
  - [x] Vérification MIME type
  - [x] Extensions autorisées
- [x] Nettoyage professionnel (`preprocessing/cleaner.py`)
  - [x] Suppression headers/footers répétitifs
  - [x] Normalisation espaces et sauts de ligne
  - [x] Suppression numéros de page
  - [x] Métadonnées de nettoyage
- [x] Chunking intelligent (`preprocessing/chunker.py`)
  - [x] Détection articles/clauses
  - [x] Contexte ajouté à chaque chunk
  - [x] Détection type de clause (financial, termination, etc.)
  - [x] Limite 1000 caractères par chunk
- [x] Pipeline mis à jour avec composants professionnels

##### 7.3 RAG Juridique (Sprint 3 - À faire)
- [ ] Base de connaissances locale (`python-ai/rag_setup.py`)
  - [ ] Code Civil (articles pertinents)
  - [ ] Loi 89-462 (baux d'habitation)
  - [ ] Code du Travail (articles clés)
  - [ ] Modèles de clauses neutres
- [ ] Index vectoriel FAISS
  - [ ] Embeddings multilingues
  - [ ] Recherche sémantique
  - [ ] Top-K retrieval
- [ ] Intégration RAG dans pipeline
  - [ ] Enrichissement des analyses
  - [ ] Références légales automatiques
  - [ ] Prévention hallucinations

##### 7.3 Intégration Next.js (Sprint 2 - 1 jour)
- [ ] Route API `/api/ai-analyze` (`src/app/api/ai-analyze/route.ts`)
  - [ ] Communication avec service Python
  - [ ] Gestion timeout
  - [ ] Fallback en cas d'erreur
- [ ] Variables d'environnement
  - [ ] `AI_SERVICE_URL` (http://localhost:8000 ou Docker)
- [ ] Tests d'intégration
  - [ ] Upload → Analyse → Résultat
  - [ ] Gestion erreurs réseau

##### 7.4 Interface Résultats Expert (Sprint 3 - 3 jours)
- [ ] Composant `ClauseByClauseView` (`src/components/analysis/ClauseByClauseView.tsx`)
  - [ ] Affichage clause par clause
  - [ ] Code couleur par niveau de risque (🟢🟡🔴)
  - [ ] Sections : Résumé, Implications, Risques, Conformité, Recommandation
  - [ ] Animations Framer Motion
- [ ] Composant `ScoreCard` (`src/components/analysis/ScoreCard.tsx`)
  - [ ] Score global avec jauge
  - [ ] Scores détaillés (conformité, équilibre, clarté)
  - [ ] Visualisation graphique
- [ ] Composant `RiskSummary` (`src/components/analysis/RiskSummary.tsx`)
  - [ ] Liste des risques détectés
  - [ ] Filtrage par gravité
  - [ ] Actions recommandées
- [ ] Composant `ContractSummary` (`src/components/analysis/ContractSummary.tsx`)
  - [ ] Résumé exécutif IA
  - [ ] Entités extraites (montants, dates, parties)
  - [ ] Type de contrat détecté
- [ ] Page résultats (`src/app/analyser/results/page.tsx`)
  - [ ] Layout responsive
  - [ ] Navigation entre sections
  - [ ] Export PDF

##### 7.5 Export PDF Expert (Sprint 3 - 1 jour)
- [ ] Service d'export (`src/lib/export/pdf-expert.ts`)
  - [ ] Génération PDF avec `pdfkit`
  - [ ] Sections : Score, Résumé, Clauses, Risques, Recommandations
  - [ ] Mise en page professionnelle
  - [ ] Références légales
- [ ] Route API `/api/export-pdf`
  - [ ] Génération à la demande
  - [ ] Téléchargement direct
- [ ] Bouton d'export dans l'interface
  - [ ] Loading state
  - [ ] Gestion erreurs

##### 7.6 Docker & Déploiement (Sprint 4 - 2 jours)
- [ ] Dockerfile Python (`python-ai/Dockerfile`)
  - [ ] Base image Python 3.11
  - [ ] Installation dépendances système
  - [ ] Téléchargement modèles au build
  - [ ] Configuration GPU (optionnel)
- [ ] Docker Compose (`docker-compose.yml`)
  - [ ] Service Next.js (web)
  - [ ] Service Python (ai-service)
  - [ ] Volume pour cache modèles
  - [ ] Network configuration
- [ ] Scripts de déploiement
  - [ ] `docker-compose up -d`
  - [ ] Health checks
  - [ ] Logs monitoring
- [ ] Documentation déploiement
  - [ ] Prérequis système (RAM, GPU)
  - [ ] Variables d'environnement
  - [ ] Troubleshooting

##### 7.7 Tests & Validation (Sprint 4 - 1 jour)
- [ ] Tests unitaires Python
  - [ ] Pipeline IA
  - [ ] Chunking
  - [ ] Parsing réponses LLM
- [ ] Tests d'intégration
  - [ ] End-to-end (upload → analyse → résultat)
  - [ ] Performance (temps de réponse)
  - [ ] Qualité des analyses
- [ ] Tests UI
  - [ ] Affichage clauses
  - [ ] Interactions utilisateur
  - [ ] Responsive design

##### 7.8 Optimisations (Optionnel)
- [ ] Cache des modèles
  - [ ] Éviter rechargement à chaque requête
  - [ ] Singleton pattern
- [ ] Batch processing
  - [ ] Analyser plusieurs clauses en parallèle
- [ ] Monitoring
  - [ ] Logs structurés
  - [ ] Métriques (temps, erreurs)
  - [ ] Alertes

**Roadmap Totale** : 10-11 jours pour Version Expert IA-First complète

**Stack Technique** :
- Backend IA : Python 3.11, FastAPI, Uvicorn
- LLM : Mistral-7B-Instruct-v0.2 (Hugging Face)
- NLP : spaCy (fr_core_news_md), CamemBERT, BARThez
- RAG : FAISS, sentence-transformers
- Chunking : LangChain
- Export : pdfkit
- Déploiement : Docker, Docker Compose

#### Phase 8 : Paiement Stripe
- [ ] Intégration Stripe Checkout
- [ ] Gestion abonnements
- [ ] Webhooks
- [ ] Paywall UI

#### Phase 9 : SEO Local Massif
- [ ] Base données communes INSEE
- [ ] Génération pages villes (36 000+)
- [ ] Templates SEO intelligents
- [ ] Schema.org
- [ ] Sitemaps segmentés

#### Phase 10 : Fonctionnalités Utilisateur
- [ ] Authentification
- [ ] Dashboard utilisateur
- [ ] Historique analyses
- [ ] Statistiques

#### Phase 11 : Conformité & Légal
- [ ] Mentions légales
- [ ] Politique RGPD
- [ ] CGU
- [ ] Suppression auto 24h
- [ ] Disclaimers

#### Phase 12 : Base de Données
- [ ] Schéma Prisma
- [ ] Migrations
- [ ] Client DB

#### Phase 13 : Déploiement
- [ ] Configuration Vercel
- [ ] Variables d'environnement production
- [ ] Tests finaux
- [ ] Déploiement

## 📊 Modèle de Pricing

### Principe Simple

**1 contrat = 1,90€ (TOUT INCLUS)**

Ce prix inclut :
- ✅ Analyse complète du contrat
- ✅ Détection de toutes les clauses à risque
- ✅ Reformulations protectrices pour chaque clause
- ✅ Assistance contextuelle
- ✅ Export PDF

### Packs Prépayés (Valables 12 mois)

| Type | Prix | Prix unitaire | Économie |
|------|------|---------------|----------|
| À l'acte | 1,90€ | 1,90€/contrat | - |
| Pack 10 | 15€ | 1,50€/contrat | 4€ (21%) |
| Pack 25 | 35€ | 1,40€/contrat | 12,50€ (26%) |
| Pack 50 | 60€ | 1,20€/contrat | 35€ (37%) |

> 💡 **Note** : Les reformulations sont **incluses** dans le prix, pas payantes séparément.

## 🛠️ Stack Technique Utilisée

- **Frontend**: Next.js 14+ (App Router), React 18+, TypeScript
- **Styling**: Tailwind CSS, Framer Motion
- **UI Components**: Custom design system
- **Validation**: Zod
- **Forms**: React Hook Form
- **Utilities**: class-variance-authority, clsx, tailwind-merge

## 📦 Dépendances à Installer (Phases Futures)

```bash
# OCR & Document Processing
npm install tesseract.js pdfjs-dist mammoth

# Paiement
npm install stripe @stripe/stripe-js

# Base de données
npm install @prisma/client
npm install -D prisma

# IA (selon choix)
npm install @huggingface/inference
# OU
npm install @mistralai/mistralai
```

## 🏗️ Architecture des Composants

```
src/
├── components/
│   ├── ui/              ✅ Composants de base
│   ├── layout/          ✅ Header, Footer
│   ├── home/            ✅ Sections landing page
│   ├── upload/          🚧 À créer
│   ├── results/         🚧 À créer
│   ├── payment/         🚧 À créer
│   ├── dashboard/       🚧 À créer
│   └── legal/           🚧 À créer
├── lib/
│   ├── analysis/        🚧 Moteur d'analyse
│   ├── extractors/      🚧 PDF/DOCX/OCR
│   ├── text-processing/ 🚧 Normalisation
│   ├── ocr/             🚧 Tesseract
│   ├── stripe/          🚧 Paiement
│   ├── seo/             🚧 Génération SEO
│   ├── db/              🚧 Prisma client
│   └── auth/            🚧 Sessions
└── data/
    └── cities/          🚧 Communes françaises
```

## 🎨 Design System

### Couleurs

- **Primary**: Bleu professionnel (#3b82f6 → #1e40af)
- **Success**: Vert confiance (#22c55e → #15803d)
- **Warning**: Orange attention (#f97316 → #c2410c)
- **Danger**: Rouge alerte (#ef4444 → #b91c1c)
- **Neutral**: Gris slate (#f8fafc → #0f172a)

### Typographie

- **Sans**: Inter (corps de texte)
- **Display**: Lexend (titres)

### Animations

- `fadeIn`: Apparition douce
- `slideInUp`: Glissement vers le haut
- `scaleIn`: Zoom d'apparition
- `shimmer`: Effet de chargement

## 📝 Conventions de Code

### Naming

- Composants: `PascalCase` (ex: `Button.tsx`)
- Fonctions/variables: `camelCase`
- Constantes: `UPPER_SNAKE_CASE`
- Fichiers API: `route.ts`

### Structure des Composants

```typescript
'use client'; // Si nécessaire

import { ... } from '...';

export interface ComponentProps {
  // Props typées
}

export function Component({ ...props }: ComponentProps) {
  // Logique
  return (
    // JSX
  );
}
```

## 🧪 Tests (À Implémenter)

```bash
# Tests unitaires
npm run test

# Tests en mode watch
npm run test:watch

# Tests E2E
npm run test:e2e
```

## 📚 Documentation par Module

Chaque module majeur devrait avoir sa propre documentation dans `/docs`:

- `docs/upload.md` - Upload et scan de documents
- `docs/analysis.md` - Moteur d'analyse contractuelle
- `docs/seo.md` - Stratégie SEO locale
- `docs/payment.md` - Intégration Stripe
- `docs/deployment.md` - Guide de déploiement

## 🔐 Variables d'Environnement

Copier `.env.local.example` vers `.env.local` et remplir:

```bash
# Application
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Database
POSTGRES_URL=...
POSTGRES_PRISMA_URL=...

# Blob Storage
BLOB_READ_WRITE_TOKEN=...

# AI
HUGGINGFACE_API_KEY=...
MISTRAL_API_KEY=...

# Session
SESSION_SECRET=...
```

## 🚀 Prochaines Étapes Prioritaires

1. **Phase 6**: Développer le moteur d'analyse avec règles + IA
2. **Phase 7**: Créer l'interface de résultats
3. **Phase 7**: Créer l'interface de résultats
4. **Phase 8**: Intégrer Stripe pour les paiements
5. **Phase 8**: Intégrer Stripe pour les paiements

## 💡 Notes Importantes

- Le projet utilise Next.js 14+ avec App Router
- Tous les composants client doivent avoir `'use client'`
- Les API routes sont dans `app/api/`
- Le design system est dans `app/globals.css`
- Les composants sont dans `src/components/`
- La logique métier est dans `src/lib/`

## 🤝 Contribution

Pour contribuer au projet:

1. Créer une branche `feature/nom-fonctionnalite`
2. Développer la fonctionnalité
3. Tester localement
4. Créer une Pull Request
5. Code review obligatoire avant merge

## 📞 Support

Pour toute question, consulter la documentation ou contacter l'équipe de développement.
