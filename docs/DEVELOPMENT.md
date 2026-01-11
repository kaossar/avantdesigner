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

#### Phase 4 : Upload & Scan de Documents
- [ ] Interface d'upload multi-format
- [ ] Drag & drop
- [ ] Scanner caméra (mobile/desktop)
- [ ] Intégration Tesseract.js OCR
- [ ] Prévisualisation

#### Phase 5 : Backend & API
- [ ] API upload vers Vercel Blob
- [ ] Extraction PDF (PDF.js)
- [ ] Extraction DOCX (Mammoth.js)
- [ ] Pipeline OCR
- [ ] Normalisation texte

#### Phase 6 : Moteur d'Analyse
- [ ] Règles déterministes
- [ ] Détection clauses à risque
- [ ] Intégration IA (Hugging Face/Mistral)
- [ ] Système de scoring
- [ ] Génération reformulations

#### Phase 7 : Interface Résultats
- [ ] Page résultats avec score
- [ ] Liste des clauses
- [ ] Détails par clause
- [ ] Reformulations suggérées
- [ ] Export PDF

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

1. **Phase 4**: Créer l'interface d'upload avec scan caméra
2. **Phase 5**: Implémenter l'extraction de texte (PDF, DOCX, OCR)
3. **Phase 6**: Développer le moteur d'analyse avec règles + IA
4. **Phase 7**: Créer l'interface de résultats
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
