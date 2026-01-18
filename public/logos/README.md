# Logos AvantdeSigner

Ce dossier contient les options de logo pour AvantdeSigner.

## Fichiers

### Option 2 : Loupe Analytique 🔍
- `logo-option-2-magnifier.png` - Logo complet avec texte
- `icon-option-2.png` - Icône seule (favicon)

**Concept** : Loupe examinant un document avec analyse IA (ligne verte)  
**Couleurs** : Bleu foncé (#0f172a) + Vert émeraude (#10b981)  
**Style** : Professionnel, analytique, rassurant

### Option 3 : Checkpoint Innovant ✓
- `logo-option-3-checkpoint.png` - Logo complet avec texte
- `icon-option-3.png` - Icône seule (favicon)

**Concept** : Checkmark fusionné avec lettre "A"  
**Couleurs** : Gradient violet (#7c3aed) → cyan (#06b6d4)  
**Style** : Moderne, dynamique, innovant

## Recommandation

**Option 3 (Checkpoint)** est recommandée pour :
- Positionnement moderne et disruptif
- Mémorabilité et unicité
- Adaptation parfaite aux petites tailles
- Message clair : "Validation avant signature"

## Utilisation

Pour intégrer un logo dans l'application :

```tsx
import Image from 'next/image'

<Image 
  src="/logos/logo-option-3-checkpoint.png" 
  alt="AvantdeSigner" 
  width={200} 
  height={40}
/>
```

Pour le favicon :
```tsx
// app/layout.tsx
export const metadata = {
  icons: {
    icon: '/logos/icon-option-3.png',
  },
}
```
