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

##### 7.3 RAG Juridique (Sprint 3 - Terminé ✅)
- [x] Base de connaissances locale (`python-ai/knowledge_base/`)
  - [x] Code Civil (17 articles complets)
  - [x] Loi 89-462 (18 articles baux d'habitation)
  - [ ] Code du Travail (articles clés) - Phase 2
  - [ ] Modèles de clauses neutres - Phase 2
- [x] Index vectoriel FAISS (Sprint 3+)
  - [x] Embeddings multilingues (paraphrase-multilingual-mpnet-base-v2)
  - [x] Recherche sémantique (sentence-transformers)
  - [x] Top-K retrieval avec scoring
  - [x] Cache système (30s → <1s)
- [x] Intégration RAG dans pipeline
  - [x] Enrichissement des analyses
  - [x] Références légales automatiques (2.0 refs/clause)
  - [x] Fallback keyword/semantic
  - [x] Affichage frontend (ClauseByClauseView)

##### 7.3 Intégration Next.js (Sprint 2 - Terminé ✅)
- [x] Route API `/api/ai-analyze` (`src/app/api/ai-analyze/route.ts`)
  - [x] Communication avec service Python (`http://localhost:8000`)
  - [x] Gestion timeout (60s)
  - [x] Fallback en cas d'erreur
  - [x] Proxy vers `/analyze` Python
- [x] Variables d'environnement
  - [x] `AI_SERVICE_URL` (local/prod)
- [x] Tests d'intégration
  - [x] Upload → Analyse → Résultat (Testé via E2E)
  - [x] Gestion erreurs réseau

##### 7.4 Interface Résultats Expert (Sprint 4 - Terminé ✅)
- [x] Composant `ClauseByClauseView` (`src/components/analysis/ClauseByClauseView.tsx`)
  - [x] Affichage clause par clause
  - [x] Code couleur par niveau de risque (🟢🟡🔴)
  - [x] Sections : Résumé, Implications, Risques, Conformité, Recommandation
  - [x] Animations Framer Motion
  - [x] Références légales RAG (section purple)
- [x] Composant `ScoreCard` (`src/components/analysis/ScoreCard.tsx`)
  - [x] Score global avec jauge circulaire
  - [x] Scores détaillés (conformité, équilibre, clarté)
  - [x] Visualisation graphique
- [x] Composant `RiskSummary` (`src/components/analysis/RiskSummary.tsx`)
  - [x] Liste des risques détectés
  - [x] Filtrage par gravité
  - [ ] Actions recommandées
- [ ] Composant `ContractSummary` (`src/components/analysis/ContractSummary.tsx`)
  - [ ] Résumé exécutif IA
  - [ ] Entités extraites (montants, dates, parties)
  - [ ] Type de contrat détecté
- [ ] Page résultats (`src/app/analyser/results/page.tsx`)
  - [ ] Layout responsive
  - [ ] Navigation entre sections
  - [ ] Export PDF

##### 7.5 Export PDF Expert (Sprint 7 - Terminé ✅)
- [x] Service d'export (`python-ai/export/pdf_generator.py`)
  - [x] Génération PDF avec `pdfkit` + Jinja2
  - [x] Template HTML professionnel (`export/templates/report.html`)
  - [x] Sections : Cover, Score, Résumé, Risques, Clauses, Références légales, Annexes
  - [x] Mise en page professionnelle (A4, marges, styles)
  - [x] Références légales RAG incluses
- [x] Route API `/export-pdf` (`python-ai/main.py`)
  - [x] Génération à la demande
  - [x] Téléchargement direct (Content-Disposition)
  - [x] Gestion erreurs
- [ ] Bouton d'export dans l'interface frontend
  - [ ] Loading state
  - [ ] Appel API /export-pdf
  - [ ] Download automatique

##### 7.6 Docker & Déploiement (Sprint 6 - Terminé ✅)
- [x] Dockerfile Python (`python-ai/Dockerfile`)
  - [x] Base image Python 3.14-slim
  - [x] Installation dépendances système (wkhtmltopdf)
  - [x] Installation requirements.txt
  - [x] Cache directories (rag_cache, export/templates)
  - [x] Health check configuré
  - [x] CMD uvicorn
- [x] Docker Compose (`docker-compose.yml`)
  - [x] Service Next.js (web) :3000
  - [x] Service Python (ai-service) :8000
  - [x] Volumes persistants (ai-cache, rag-cache)
  - [x] Network configuration
  - [x] Environment variables
  - [x] Health checks
  - [x] Auto-restart policies
- [x] Documentation déploiement (`DOCKER.md`)
  - [x] Quick start guide
  - [x] Commandes développement
  - [x] Troubleshooting
  - [x] Production deployment
  - [x] Architecture diagram

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
- Backend IA : Python 3.14, FastAPI, Uvicorn
- LLM : Mistral-7B-Instruct-v0.2 (Hugging Face) - À intégrer
- NLP : spaCy (fr_core_news_md), CamemBERT, BARThez - À intégrer
- RAG : FAISS ✅, sentence-transformers ✅, paraphrase-multilingual-mpnet-base-v2 ✅
- Chunking : Smart chunker professionnel ✅
- Export : pdfkit ✅, Jinja2 ✅
- Déploiement : Docker, Docker Compose

---

#### Phase 8 : Expansion Types de Contrats (Vision Stratégique)

**Objectif** : Transformer AvantDeSigner d'un outil de niche (baux) en plateforme complète d'analyse contractuelle.

**État actuel** : ✅ Baux d'habitation (Loi 89-462 + Code Civil)

**Roadmap complète** : 9 catégories, 100+ types de contrats

##### 8.1 Contrats du Quotidien (Particuliers)

**🏠 Logement** (Priorité 1)
- [x] Bail d'habitation vide ✅
- [ ] Bail meublé
- [ ] Bail étudiant
- [ ] Bail mobilité
- [ ] État des lieux
- [ ] Acte de cautionnement
- [ ] Compromis de vente immobilière

**💳 Consommation** (Priorité 2)
- [ ] Contrat de crédit à la consommation
- [ ] Crédit renouvelable
- [ ] Prêt personnel
- [ ] Contrat de leasing / LOA / LLD
- [ ] CGV (Conditions Générales de Vente)
- [ ] CGU (Conditions Générales d'Utilisation)
- [ ] Abonnements (téléphonie, internet, streaming)

**🛡️ Assurances** (Priorité 1 - Forte valeur)
- [ ] Assurance habitation
- [ ] Assurance auto / moto
- [ ] Assurance santé / mutuelle
- [ ] Assurance prévoyance
- [ ] Assurance emprunteur

##### 8.2 Contrats Professionnels

**👨‍💻 Freelance / Indépendants** (Priorité 1 - Forte demande)
- [ ] Contrat de prestation de services
- [ ] Contrat de mission freelance
- [ ] Contrat de sous-traitance
- [ ] NDA / Accord de confidentialité
- [ ] Lettre de mission

**🧑‍💼 Travail Salarié** (Priorité 2)
- [ ] CDI
- [ ] CDD
- [ ] Contrat d'intérim
- [ ] Contrat d'apprentissage
- [ ] Rupture conventionnelle

##### 8.3 Contrats Business & Commercial

**🤝 Relations Commerciales** (Priorité 2)
- [ ] Contrat commercial général
- [ ] Contrat de partenariat
- [ ] Contrat de distribution
- [ ] Contrat de franchise
- [ ] Contrat de licence

**📦 Vente & Fournisseurs** (Priorité 2)
- [ ] Contrat de vente B2B
- [ ] Contrat fournisseur
- [ ] Contrat cadre
- [ ] SLA (Service Level Agreement)

##### 8.4 Numérique & SaaS (Stratégique)

**🌐 Tech** (Priorité 1)
- [ ] Contrat SaaS
- [ ] Contrat d'hébergement
- [ ] Contrat de maintenance informatique
- [ ] Contrat de développement logiciel
- [ ] Contrat de cybersécurité

**©️ Propriété Intellectuelle** (Priorité 2)
- [ ] Cession de droits d'auteur
- [ ] Licence de droits d'auteur
- [ ] Contrat d'édition
- [ ] Contrat de marque

##### 8.5 Immobilier Pro & Construction

- [ ] Bail commercial
- [ ] Bail professionnel
- [ ] CCMI (Contrat de Construction de Maison Individuelle)
- [ ] Contrat de maîtrise d'œuvre

##### 8.6 Contrats à Risque Élevé (Forte valeur ajoutée)

- [ ] Pacte d'associés
- [ ] Statuts de société (SAS, SARL)
- [ ] Contrat d'investissement
- [ ] Contrat de prêt entre particuliers
- [ ] Transaction amiable
- [ ] Convention de divorce

##### 8.7 Clauses Transversales (CRITIQUE)

**Indépendamment du type de contrat, AvantDeSigner DOIT reconnaître :**
- [x] Clauses abusives ✅
- [x] Clauses déséquilibrées ✅
- [x] Clauses de résiliation ✅
- [x] Clauses pénales ✅
- [ ] Clauses limitatives de responsabilité
- [ ] Clauses de reconduction tacite
- [ ] Clauses de compétence territoriale
- [ ] Clauses de force majeure
- [ ] Clauses RGPD
- [ ] Clauses de paiement / retard / pénalités

**Impact Stratégique** :
- ✅ Utile aux particuliers (logement, assurances, consommation)
- ✅ Indispensable aux freelances (prestations, NDA)
- ✅ Crédible pour les entreprises (commercial, SaaS, B2B)
- ✅ Différencié face aux simples outils d'analyse
- ✅ Monétisable en B2C + B2B + assurances + legaltech

**Architecture Technique pour Expansion** :
1. Base de connaissances modulaire par domaine juridique
2. Classification automatique du type de contrat
3. Sélection des règles applicables
4. RAG sémantique évolutif (index FAISS multi-domaines)
5. Pipeline modulaire avec analyseurs spécialisés

---

#### Phase 9 : Paiement Stripe

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

## 🧪 Stratégie de Tests

### Principe : Tests après chaque Sprint

**Règle d'or** : Chaque sprint doit inclure ses tests unitaires et d'intégration.

### Structure des Tests

#### Python (Backend IA)
```
python-ai/
├── tests/
│   ├── __init__.py
│   ├── test_validator.py     # Tests validation fichiers
│   ├── test_cleaner.py       # Tests nettoyage texte
│   ├── test_chunker.py       # Tests chunking
│   └── test_pipeline.py      # Tests intégration
├── pytest.ini                # Configuration pytest
├── requirements-test.txt     # Dépendances tests
└── TESTING.md               # Documentation tests
```

#### Commandes
```bash
# Installer dépendances tests
pip install -r requirements-test.txt

# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=. --cov-report=html

# Tests verbeux
pytest -v

# Tests spécifiques
pytest tests/test_validator.py
```

#### Couverture Cible
- **Minimum** : 70% de couverture
- **Objectif** : 85% de couverture
- **Critique** : 100% pour utils et preprocessing

### Tests par Sprint

#### Sprint 1 (Infrastructure IA)
- ✅ Tests pipeline de base
- ✅ Tests API endpoints (FastAPI)

#### Sprint 2 (Pipeline Professionnel)
- ✅ Tests validator (8 tests)
- ✅ Tests cleaner (9 tests)
- ✅ Tests chunker (11 tests)
- ✅ Tests intégration pipeline (6 tests)

#### Sprint 3+ (À venir)
- [ ] Tests NER (entity extraction)
- [ ] Tests LLM integration
- [ ] Tests RAG juridique
- [ ] Tests export PDF

### Next.js (Frontend)
```bash
# Tests unitaires
npm run test

# Tests en mode watch
npm run test:watch

# Tests E2E
npm run test:e2e
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
