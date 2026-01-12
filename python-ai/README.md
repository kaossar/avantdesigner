# Python AI Service

Service d'analyse de contrats par IA utilisant FastAPI et Hugging Face.

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle spaCy français
python -m spacy download fr_core_news_md
```

## Démarrage

```bash
# Mode développement
python main.py

# Ou avec uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /health
```

### Analyze Contract
```
POST /analyze
Content-Type: application/json

{
  "text": "Contrat de bail...",
  "contract_type": "auto"
}
```

## Architecture

```
python-ai/
├── main.py           # FastAPI application
├── pipeline.py       # AI processing pipeline
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Pipeline Stages

1. **Text Cleaning** - Normalisation et nettoyage
2. **Smart Chunking** - Découpage par clause
3. **Classification** - Détection du type de contrat
4. **Entity Extraction** - Extraction montants, dates, etc.
5. **Clause Analysis** - Analyse IA clause par clause
6. **Risk Detection** - Détection des risques
7. **Score Calculation** - Calcul du score global
8. **Recommendations** - Génération de recommandations

## TODO - Sprint 2

- [ ] Intégrer Mistral 7B pour analyse LLM
- [ ] Ajouter CamemBERT pour classification
- [ ] Implémenter RAG juridique avec FAISS
- [ ] Ajouter BARThez pour résumé
- [ ] Tests unitaires
