# Modèle Pay-Per-Contract - AvantDeSigner

## 🎯 Vue d'Ensemble

AvantDeSigner utilise un **modèle de paiement à l'acte avec packs prépayés**, sans abonnement récurrent.

### Principe
- Chaque analyse de contrat coûte **1,90€**
- Packs prépayés disponibles pour économiser
- Crédits valables **12 mois**
- **Aucun abonnement, aucun prélèvement automatique**

---

## 💰 Grille Tarifaire

| Type | Prix | Prix unitaire | Économie | Validité |
|------|------|---------------|----------|----------|
| **À l'acte** | 1,90€ | 1,90€/contrat | - | Immédiat |
| **Pack 10** | 15€ | 1,50€/contrat | 4€ (21%) | 12 mois |
| **Pack 25** | 35€ | 1,40€/contrat | 12,50€ (26%) | 12 mois |
| **Pack 50** | 60€ | 1,20€/contrat | 35€ (37%) | 12 mois |

### Ce qui est Inclus (Tous les Plans)
✅ Analyse complète du contrat  
✅ Détection de toutes les clauses à risque  
✅ Reformulations protectrices prêtes à négocier  
✅ Assistance contextuelle  
✅ Export PDF  
✅ Historique des analyses

---

## ✅ Avantages du Modèle

### Pour l'Utilisateur

**Simplicité** :
- Pas de surprise : prix fixe par contrat
- Pas d'engagement : aucun abonnement
- Pas de prélèvement automatique

**Flexibilité** :
- Payez uniquement ce que vous utilisez
- Achetez un pack si vous avez plusieurs contrats
- Pas de pression pour utiliser rapidement

**Transparence** :
- Validité claire (12 mois)
- Alertes avant expiration
- Pas de frais cachés

### Pour le Business

**Réglementation** :
- ✅ Pas d'abonnement récurrent → Simplifie la conformité
- ✅ Pas de gestion de résiliation
- ✅ Pas de prélèvement automatique → Moins de litiges
- ✅ Conditions claires (validité 12 mois)

**Fiscalité** :
- TVA applicable sur chaque achat
- Comptabilité simplifiée
- Pas de gestion de revenus récurrents

**Technique** :
- Stripe supporte parfaitement les crédits prépayés
- Pas de webhooks d'abonnement complexes
- Gestion simple en base de données

---

## 🗄️ Architecture Base de Données

### Schéma Prisma

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  credits   UserCredits[]
  analyses  Analysis[]
}

model UserCredits {
  id             String   @id @default(cuid())
  userId         String
  user           User     @relation(fields: [userId], references: [id])
  
  remainingCredits Int
  initialCredits   Int
  packType         PackType
  
  purchaseDate     DateTime @default(now())
  expirationDate   DateTime
  
  stripePaymentId  String?
  
  createdAt        DateTime @default(now())
  updatedAt        DateTime @updatedAt
  
  @@index([userId])
  @@index([expirationDate])
}

enum PackType {
  SINGLE      // 1 crédit
  PACK_10     // 10 crédits
  PACK_25     // 25 crédits
  PACK_50     // 50 crédits
}

model Analysis {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  
  contractText String   @db.Text
  results      Json     // Résultats de l'analyse
  
  creditUsed   Boolean  @default(false)
  creditsId    String?  // Référence au pack utilisé
  
  createdAt    DateTime @default(now())
  expiresAt    DateTime // Suppression auto après 24h
  
  @@index([userId])
  @@index([expiresAt])
}
```

---

## 🔄 Flux Utilisateur

### 1. Achat de Crédits

```typescript
// Utilisateur achète un pack
const purchase = await stripe.checkout.sessions.create({
  mode: 'payment',
  line_items: [{
    price: 'price_pack_10', // ID Stripe du Pack 10
    quantity: 1,
  }],
  success_url: `${process.env.NEXT_PUBLIC_APP_URL}/success`,
  cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
});

// Webhook Stripe confirme le paiement
// → Créer UserCredits en base
await prisma.userCredits.create({
  data: {
    userId: user.id,
    remainingCredits: 10,
    initialCredits: 10,
    packType: 'PACK_10',
    purchaseDate: new Date(),
    expirationDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // +12 mois
    stripePaymentId: payment.id,
  },
});
```

### 2. Utilisation d'un Crédit

```typescript
// Utilisateur lance une analyse
async function analyzeContract(userId: string, contractText: string) {
  // 1. Vérifier les crédits disponibles
  const credits = await prisma.userCredits.findFirst({
    where: {
      userId,
      remainingCredits: { gt: 0 },
      expirationDate: { gt: new Date() },
    },
    orderBy: { expirationDate: 'asc' }, // Utiliser les plus anciens d'abord
  });
  
  if (!credits) {
    throw new Error('Aucun crédit disponible');
  }
  
  // 2. Décompter un crédit
  await prisma.userCredits.update({
    where: { id: credits.id },
    data: { remainingCredits: { decrement: 1 } },
  });
  
  // 3. Lancer l'analyse
  const results = await performAnalysis(contractText);
  
  // 4. Sauvegarder
  await prisma.analysis.create({
    data: {
      userId,
      contractText,
      results,
      creditUsed: true,
      creditsId: credits.id,
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // +24h
    },
  });
  
  return results;
}
```

### 3. Alertes d'Expiration

```typescript
// Cron job quotidien
async function sendExpirationAlerts() {
  const now = new Date();
  const in30Days = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
  const in7Days = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const in1Day = new Date(now.getTime() + 1 * 24 * 60 * 60 * 1000);
  
  // Crédits expirant dans 30 jours
  const expiringSoon = await prisma.userCredits.findMany({
    where: {
      remainingCredits: { gt: 0 },
      expirationDate: { gte: now, lte: in30Days },
      // Pas déjà alerté pour 30j
    },
    include: { user: true },
  });
  
  for (const credit of expiringSoon) {
    await sendEmail({
      to: credit.user.email,
      subject: `⏰ Vos ${credit.remainingCredits} crédits expirent dans 30 jours`,
      body: `Utilisez-les avant le ${credit.expirationDate.toLocaleDateString()}`,
    });
  }
  
  // Répéter pour 7j et 1j
}
```

### 4. Nettoyage des Crédits Expirés

```typescript
// Cron job quotidien
async function cleanupExpiredCredits() {
  const now = new Date();
  
  // Marquer comme expirés
  await prisma.userCredits.updateMany({
    where: {
      expirationDate: { lt: now },
      remainingCredits: { gt: 0 },
    },
    data: {
      remainingCredits: 0, // Mettre à 0 pour historique
    },
  });
}
```

---

## 🎨 Composants UI

### CreditTracker

Affiche les crédits de l'utilisateur :

```typescript
interface CreditTrackerProps {
  userId: string;
}

export function CreditTracker({ userId }: CreditTrackerProps) {
  const { data: credits } = useQuery({
    queryKey: ['credits', userId],
    queryFn: () => fetch(`/api/user/credits`).then(r => r.json()),
  });
  
  if (!credits || credits.remainingCredits === 0) {
    return (
      <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
        <p className="text-warning-900">Aucun crédit disponible</p>
        <Link href="/pricing">
          <Button variant="primary" size="sm">Acheter des crédits</Button>
        </Link>
      </div>
    );
  }
  
  const daysUntilExpiration = Math.floor(
    (new Date(credits.expirationDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
  );
  
  return (
    <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="font-semibold text-primary-900">
          {credits.remainingCredits} crédit{credits.remainingCredits > 1 ? 's' : ''} disponible{credits.remainingCredits > 1 ? 's' : ''}
        </span>
        <span className="text-sm text-primary-700">
          Expire dans {daysUntilExpiration} jours
        </span>
      </div>
      
      <div className="w-full bg-primary-200 rounded-full h-2">
        <div
          className="bg-primary-600 h-2 rounded-full transition-all"
          style={{
            width: `${(credits.remainingCredits / credits.initialCredits) * 100}%`,
          }}
        />
      </div>
      
      {daysUntilExpiration < 30 && (
        <p className="text-xs text-primary-700 mt-2">
          ⏰ Pensez à utiliser vos crédits avant expiration !
        </p>
      )}
    </div>
  );
}
```

---

## 📊 Métriques & Analytics

### KPIs à Suivre

**Acquisition** :
- Nombre d'achats par type (single, pack 10, 25, 50)
- Panier moyen
- Taux de conversion visiteur → acheteur

**Utilisation** :
- Taux d'utilisation des crédits (% utilisés avant expiration)
- Temps moyen entre achat et première utilisation
- Nombre moyen de contrats analysés par utilisateur

**Rétention** :
- Taux de réachat
- Délai entre deux achats
- Lifetime Value (LTV)

**Expiration** :
- % de crédits expirés non utilisés
- Efficacité des alertes (taux d'utilisation après alerte)

---

## 🚀 Roadmap

### Phase 1 (MVP)
- ✅ Paiement à l'acte (1,90€)
- ✅ Packs 10, 25, 50
- ✅ Gestion des crédits en base
- ✅ Expiration 12 mois

### Phase 2 (Amélioration)
- 🔄 Alertes email d'expiration
- 🔄 Dashboard utilisateur avec suivi crédits
- 🔄 Historique des achats
- 🔄 Cadeaux de crédits (parrainage)

### Phase 3 (Scale)
- 📅 Packs entreprise (100, 250, 500 contrats)
- 📅 API avec crédits dédiés
- 📅 Recharge automatique (opt-in)
- 📅 Crédits transférables

---

## ⚖️ Aspects Légaux

### CGU - Mentions Obligatoires

**Validité des packs** :
> "Les packs de crédits sont valables 12 mois à compter de la date d'achat. Les crédits non utilisés à l'expiration de cette période ne sont pas remboursables et ne peuvent être prolongés."

**Utilisation des crédits** :
> "Chaque analyse de contrat consomme 1 crédit. Les crédits sont décomptés automatiquement lors du lancement de l'analyse. Les crédits les plus anciens sont utilisés en premier."

**Pas de remboursement** :
> "Les crédits achetés ne sont pas remboursables, sauf en cas de défaut du service. En cas de problème technique empêchant l'analyse, le crédit est recrédité automatiquement."

**Données personnelles** :
> "Les analyses sont supprimées automatiquement après 24 heures. Seul l'historique (date, type de contrat) est conservé pour votre suivi."

### RGPD

- ✅ Données minimales collectées (email, analyses)
- ✅ Suppression auto des contrats (24h)
- ✅ Droit à l'oubli (suppression compte = suppression crédits)
- ✅ Export des données possible

---

## 💡 Conseils d'Implémentation

### Stripe Products

Créer 4 produits Stripe :
```bash
# Produit 1 : Contrat unique
stripe products create \
  --name "Analyse de contrat" \
  --description "Analyse complète d'un contrat avec reformulations"

stripe prices create \
  --product prod_xxx \
  --unit-amount 190 \
  --currency eur

# Produit 2 : Pack 10
stripe products create \
  --name "Pack 10 contrats" \
  --description "10 analyses de contrats valables 12 mois"

stripe prices create \
  --product prod_yyy \
  --unit-amount 1500 \
  --currency eur

# Répéter pour Pack 25 et Pack 50
```

### Webhooks Stripe

Écouter l'événement `checkout.session.completed` :

```typescript
export async function POST(req: Request) {
  const sig = req.headers.get('stripe-signature');
  const event = stripe.webhooks.constructEvent(
    await req.text(),
    sig,
    process.env.STRIPE_WEBHOOK_SECRET
  );
  
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    
    // Récupérer le produit acheté
    const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
    const productId = lineItems.data[0].price.product;
    
    // Mapper produit → crédits
    const creditsMap = {
      'prod_single': { credits: 1, packType: 'SINGLE' },
      'prod_pack10': { credits: 10, packType: 'PACK_10' },
      'prod_pack25': { credits: 25, packType: 'PACK_25' },
      'prod_pack50': { credits: 50, packType: 'PACK_50' },
    };
    
    const pack = creditsMap[productId];
    
    // Créer les crédits
    await prisma.userCredits.create({
      data: {
        userId: session.metadata.userId,
        remainingCredits: pack.credits,
        initialCredits: pack.credits,
        packType: pack.packType,
        purchaseDate: new Date(),
        expirationDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
        stripePaymentId: session.payment_intent,
      },
    });
  }
  
  return new Response(JSON.stringify({ received: true }), { status: 200 });
}
```

---

## 🎯 Conclusion

Le modèle pay-per-contract offre :

✅ **Simplicité** pour l'utilisateur  
✅ **Conformité réglementaire** facilitée  
✅ **Flexibilité** d'usage  
✅ **Transparence** totale  
✅ **Pas de friction** (abonnements, résiliations)

C'est le modèle idéal pour un service B2C accessible avec usage ponctuel ou régulier.
