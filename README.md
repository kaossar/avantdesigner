# AvantDeSigner

**Plateforme SaaS de vérification de contrats avant signature**

> AvantDeSigner – Vérifiez votre contrat.

## 🎯 Vision

AvantDeSigner permet de **vérifier un contrat avant signature**, d'identifier les **clauses à risque ou abusives**, et surtout de proposer des **reformulations concrètes et protectrices**, prêtes à négocier.

**La différence AvantDeSigner** :
- ❌ Autres outils : "Cette clause est risquée" (et vous êtes bloqué)
- ✅ AvantDeSigner : "Cette clause est risquée + voici comment la reformuler" (vous pouvez agir)

## 🚀 Stack Technique

- **Frontend**: Next.js 14+ (App Router) avec TypeScript
- **Styling**: Tailwind CSS avec design system personnalisé
- **Backend**: API Routes serverless (Next.js)
- **OCR**: Tesseract.js (gratuit, client-side)
- **IA d'analyse**: Hugging Face Inference API → Mistral AI
- **Reformulations**: IA générative + règles métier
- **Paiement**: Stripe (Checkout + Subscriptions)
- **Base de données**: Vercel Postgres + Prisma ORM
- **Stockage**: Vercel Blob Storage (suppression 24h)
- **Hébergement**: Vercel

## 📁 Structure du Projet

```
avantdesigner/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── page.tsx             # Page d'accueil
│   │   ├── analyser/            # Page d'analyse
│   │   ├── resultats/           # Pages de résultats
│   │   ├── dashboard/           # Tableau de bord utilisateur
│   │   ├── ville/               # Pages SEO locales
│   │   └── api/                 # API Routes
│   │       ├── upload/
│   │       ├── extract/
│   │       ├── analyze/
│   │       ├── stripe/
│   │       └── user/
│   ├── components/              # Composants React
│   │   ├── ui/                  # Composants UI de base
│   │   ├── layout/              # Header, Footer
│   │   ├── home/                # Composants page d'accueil
│   │   ├── upload/              # Upload & scan
│   │   ├── results/             # Résultats d'analyse
│   │   ├── payment/             # Paiement
│   │   ├── dashboard/           # Dashboard
│   │   └── legal/               # Composants légaux
│   ├── lib/                     # Logique métier
│   │   ├── analysis/            # Moteur d'analyse
│   │   ├── extractors/          # Extraction PDF/DOCX/OCR
│   │   ├── text-processing/     # Normalisation texte
│   │   ├── ocr/                 # OCR Tesseract
│   │   ├── stripe/              # Configuration Stripe
│   │   ├── seo/                 # Génération SEO
│   │   ├── db/                  # Client Prisma
│   │   └── auth/                # Sessions
│   ├── data/                    # Données statiques
│   │   └── cities/              # Communes françaises
│   └── styles/                  # Styles globaux
├── prisma/
│   └── schema.prisma            # Schéma de base de données
├── public/                      # Assets statiques
└── docs/                        # Documentation

```

## 🛠️ Installation

```bash
# Cloner le projet
cd d:\sources\avantdesigner

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.local.example .env.local
# Éditer .env.local avec vos clés API

# Initialiser la base de données
npx prisma generate
npx prisma db push

# Lancer le serveur de développement
npm run dev
```

Ouvrir [http://localhost:3000](http://localhost:3000)

## 📝 Scripts Disponibles

```bash
npm run dev          # Serveur de développement
npm run build        # Build de production
npm run start        # Serveur de production
npm run lint         # Linter ESLint
npm run format       # Formatter Prettier
npm run type-check   # Vérification TypeScript
```

## 🧪 Tests

```bash
npm run test         # Tests unitaires
npm run test:watch   # Tests en mode watch
npm run test:e2e     # Tests end-to-end
```

## 🏗️ Architecture Collaborative

### Conventions de Code

- **ESLint + Prettier** configurés pour cohérence
- **TypeScript strict** mode activé
- **Naming conventions**:
  - Composants: `PascalCase` (ex: `Button.tsx`)
  - Fonctions/variables: `camelCase`
  - Constantes: `UPPER_SNAKE_CASE`
  - Fichiers API: `route.ts`

### Git Workflow

- `main` → Production stable
- `develop` → Intégration continue
- `feature/nom-fonctionnalite` → Nouvelles fonctionnalités
- **Pull Request obligatoire** pour merge
- **Code review** requis avant merge

### Documentation

- README par module dans `/docs`
- Documentation API avec Swagger
- Guide onboarding pour nouveaux développeurs
- Commentaires JSDoc pour fonctions complexes

## 🔐 Sécurité & Conformité

- Chiffrement des données
- Suppression automatique après 24h
- Conformité RGPD
- Mentions légales et CGU
- Disclaimer juridique sur toutes les pages

## 📊 Modèle Économique

### Paiement à l'Acte
**1,90€ par contrat** - Analyse complète incluant :
- Détection de toutes les clauses à risque
- Reformulations protectrices prêtes à négocier
- Assistance contextuelle
- Export PDF

### Packs Prépayés (Valables 12 mois)
- **Pack 10 contrats : 15€** (1,50€/contrat) - Économie de 4€
- **Pack 25 contrats : 35€** (1,40€/contrat) - Économie de 12,50€
- **Pack 50 contrats : 60€** (1,20€/contrat) - Économie de 35€

> 💡 **Avantages** :
> - Aucun abonnement récurrent
> - Aucun prélèvement automatique
> - Packs valables 12 mois
> - Alertes avant expiration des crédits

## 🌍 SEO Local

- 36 000+ pages de villes françaises
- Pages ville × type de contrat
- Génération statique incrémentale (ISR)
- Balisage Schema.org
- Sitemaps segmentés

## 📞 Support

Pour toute question ou problème, consulter la documentation dans `/docs` ou contacter l'équipe de développement.

## 📄 Licence

Propriétaire - Tous droits réservés
