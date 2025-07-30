# API REST - Bureau d'Étude Office de Tourisme 🏖️

## Vue d'ensemble

Cette API REST permet de collecter automatiquement les données de fréquentation et les profils visiteurs depuis n'importe quel site web via des appels HTTP simples.

### ✨ Fonctionnalités API

- 📊 **Comptage automatique** des vues totales du site
- 📄 **Tracking des pages** visitées avec catégorisation
- 👥 **Collecte des profils visiteurs** avec validation des données
- 📈 **Récupération des statistiques** en temps réel
- 🔄 **Envoi en lot** pour optimiser les performances
- 📖 **Documentation interactive** automatique

## 🚀 Démarrage Rapide

### 1. Lancement de l'API

```bash
# Méthode simple
./start_api.sh

# Ou manuellement
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 2. URLs importantes

- 📡 **API Base** : http://localhost:8000
- 📖 **Documentation Swagger** : http://localhost:8000/docs
- 🧪 **Documentation ReDoc** : http://localhost:8000/redoc
- ✅ **Health Check** : http://localhost:8000/health
- 📋 **Valeurs valides** : http://localhost:8000/valeurs-valides

### 3. Test rapide

```bash
# Test d'ajout visiteur
curl -X POST "http://localhost:8000/visiteur" \
     -H "Content-Type: application/json" \
     -d '{
       "type_visiteur": "Couple",
       "temps_sejour": "1-2 semaines",
       "tranche_age": "26-35 ans",
       "type_personna": "Culture/Patrimoine"
     }'

# Récupération des stats
curl -X GET "http://localhost:8000/stats"
```

## 📋 Endpoints API

### 🏠 Informations générales

#### `GET /`

Point d'entrée avec liste des endpoints disponibles

#### `GET /health`

Vérification de l'état de l'API et de la base de données

#### `GET /valeurs-valides`

Liste des valeurs acceptées pour créer des formulaires dynamiques

---

### 👥 Gestion des visiteurs

#### `POST /visiteur`

Ajoute un nouveau profil visiteur

**Paramètres requis :**

```json
{
  "type_visiteur": "Couple|Famille|Solitaire",
  "temps_sejour": "Moins d'une semaine|1-2 semaines|Plus d'un mois|Plus de 3 mois",
  "tranche_age": "18-25 ans|26-35 ans|36-45 ans|46-55 ans|56-65 ans|Plus de 65 ans",
  "type_personna": "Culture/Patrimoine|Randonnée|Plage|Gastronomie|Sport|Détente"
}
```

**Réponse :**

```json
{
  "success": true,
  "message": "Visiteur ajouté avec succès",
  "data": { ... }
}
```

#### `GET /visiteurs?limit=100`

Liste tous les visiteurs (limité par défaut à 100)

---

### 📄 Gestion des pages

#### `POST /page-vue`

Enregistre la visite d'une page

**Paramètres requis :**

```json
{
  "nom_page": "Nom de la page",
  "categorie": "Accueil|Activités|Hébergement|Restauration|Culture|Nature|Événements|Pratique"
}
```

#### `GET /pages`

Liste toutes les pages avec leurs statistiques

---

### 📊 Statistiques

#### `POST /vue-totale`

Incrémente le compteur global de vues du site

**Réponse :**

```json
{
  "success": true,
  "message": "Vue totale incrémentée",
  "vues_totales": 1234
}
```

#### `GET /stats`

Récupère les statistiques générales

**Réponse :**

```json
{
  "vues_totales": 1234,
  "nombre_visiteurs": 567,
  "nombre_pages": 89,
  "derniere_activite": "2024-07-30T15:30:00"
}
```

---

### 🚀 Tracking avancé

#### `POST /tracking/bulk`

Envoi de données en lot pour optimiser les performances

**Format :**

```json
{
  "visiteurs": [
    {
      "type_visiteur": "Couple",
      "temps_sejour": "1-2 semaines",
      "tranche_age": "26-35 ans",
      "type_personna": "Culture/Patrimoine"
    }
  ],
  "pages": [
    {
      "nom_page": "Accueil",
      "categorie": "Accueil"
    }
  ],
  "vues_totales": 2
}
```

## 🌐 Intégration Web

### JavaScript de base

```javascript
const API_BASE_URL = "http://localhost:8000";

// Auto-tracking à chaque page
document.addEventListener("DOMContentLoaded", async () => {
  // Incrémenter vues totales
  await fetch(`${API_BASE_URL}/vue-totale`, { method: "POST" });

  // Enregistrer la page courante
  await fetch(`${API_BASE_URL}/page-vue`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nom_page: document.title,
      categorie: "Accueil", // À adapter
    }),
  });
});
```

### Formulaire visiteur

```javascript
async function envoyerProfilVisiteur(donnees) {
  const response = await fetch(`${API_BASE_URL}/visiteur`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(donnees),
  });

  return response.ok;
}
```

### Récupération des stats

```javascript
async function afficherStats() {
  const response = await fetch(`${API_BASE_URL}/stats`);
  const stats = await response.json();

  document.getElementById("visiteurs-count").textContent = stats.vues_totales;
}
```

## 📁 Fichiers de référence

- **`exemples_javascript.js`** : Code JavaScript complet avec tous les exemples
- **`test_api.html`** : Page HTML de test interactive
- **`api.py`** : Code source de l'API FastAPI

## 🔒 Sécurité et Production

### Configuration CORS

En production, modifiez les origins autorisées dans `api.py` :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://votre-site.com"],  # Spécifiez vos domaines
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### HTTPS en production

Utilisez un reverse proxy (nginx) ou déployez avec des certificats SSL :

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --ssl-keyfile=/path/to/key.pem --ssl-certfile=/path/to/cert.pem
```

### Variables d'environnement

Pour la production, utilisez des variables d'environnement :

```python
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'tourisme_data.db')
```

## 🐛 Dépannage

### L'API ne démarre pas

```bash
# Vérifier les dépendances
pip install -r requirements_api.txt

# Vérifier le port
lsof -i :8000
```

### Erreurs CORS

- Vérifiez la configuration CORS dans `api.py`
- En développement, utilisez l'option `allow_origins=["*"]`

### Base de données

```bash
# Régénérer la base si nécessaire
python generate_sample_data.py
```

### Tests

```bash
# Tester l'API
python test_app.py
```

## 📈 Monitoring

### Logs

L'API utilise uvicorn qui affiche les logs en temps réel :

```
INFO:     127.0.0.1:54321 - "POST /visiteur HTTP/1.1" 200 OK
```

### Métriques

Utilisez le endpoint `/stats` pour monitorer l'activité

### Health Check

Le endpoint `/health` permet de vérifier l'état de l'API pour des outils de monitoring externes

## 🔄 Intégration avec Streamlit

L'API partage la même base de données que l'interface Streamlit :

- **Streamlit** : http://localhost:8501 (gestion et visualisation)
- **API** : http://localhost:8000 (collecte de données)

Les deux peuvent fonctionner en parallèle pour un système complet !

---

💡 **Conseil** : Consultez la documentation interactive sur http://localhost:8000/docs pour tester directement les endpoints
