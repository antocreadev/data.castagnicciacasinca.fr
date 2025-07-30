# 🏖️ Système d'Analyse de Données Touristiques

## 📋 Présentation

Système complet d'analyse et de collecte de données pour bureau d'étude d'office de tourisme, avec interface de visualisation et API REST pour l'intégration web.

### ✨ Fonctionnalités principales

- 📊 **Dashboard interactif** avec Streamlit
- 🗃️ **Base de données SQLite** intégrée
- 🔄 **Système de sauvegarde** automatique
- 📡 **API REST** pour intégration web
- 📈 **Visualisations avancées** avec Plotly
- 🔐 **Gestion CRUD** sécurisée avec confirmations
- 📱 **Interface responsive** et moderne

### 💾 Système de Sauvegarde

## 🚀 Installation et Démarrage

### 1. Installation des dépendances

```bash
# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Génération des données d'exemple

```bash
python generate_sample_data.py
```

### 3. Lancement des services

#### Interface Streamlit (Port 8501)

```bash
streamlit run app.py
```

#### API REST (Port 8000)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

#### Scripts de démarrage automatique

```bash
./start_streamlit.sh  # Lance l'interface web
./start_api.sh        # Lance l'API REST
```

## 🎯 Utilisation

### 📊 Interface Streamlit

Accédez à http://localhost:8501 pour :

1. **📈 Dashboard** : Vue d'ensemble avec graphiques et KPIs
2. **👥 Gestion Visiteurs** : CRUD des profils visiteurs
3. **📄 Gestion Pages** : Suivi des pages et catégories
4. **📋 Rapports** : Analyse détaillée et exports
5. **💾 Sauvegarde** : Gestion des backups automatiques
6. **ℹ️ À Propos** : Informations système et aide

### 📡 API REST

Accédez à http://localhost:8000 pour :

- **Documentation interactive** : `/docs`
- **Health check** : `/health`
- **Endpoints principaux** :
  - `POST /visiteur` : Ajouter un visiteur
  - `POST /page-vue` : Enregistrer une vue de page
  - `POST /vue-totale` : Incrémenter les vues totales
  - `GET /stats` : Récupérer les statistiques

## 📁 Structure du Projet

```
data-castagniccia_casinca/
├── 📄 app.py                    # Interface Streamlit principale
├── 📄 api.py                    # API FastAPI
├── 📄 database.py               # Gestionnaire base de données
├── 📄 backup_manager.py         # Système de sauvegarde
├── 📄 generate_sample_data.py   # Générateur données test
├── 📄 test_app.py              # Tests automatisés
├── 📄 exemples_javascript.js    # Exemples intégration JS
├── 📄 test_api.html            # Page test API
├── 📁 backups/                 # Sauvegardes automatiques
├── 📄 requirements.txt         # Dépendances Python
├── 📄 requirements_api.txt     # Dépendances API spécifiques
├── 🚀 start_streamlit.sh       # Script démarrage Streamlit
├── 🚀 start_api.sh             # Script démarrage API
├── 📖 README.md                # Ce fichier
└── 📖 README_API.md            # Documentation API détaillée
```

## 🗄️ Modèle de Données

### Table `vues_totales`

- `id` : Identifiant unique
- `nombre_vues` : Compteur global
- `derniere_mise_a_jour` : Timestamp

### Table `vues_pages`

- `id` : Identifiant unique
- `nom_page` : Nom de la page
- `categorie` : Catégorie (Accueil, Activités, etc.)
- `nombre_vues` : Compteur de vues
- `derniere_visite` : Timestamp dernière visite

### Table `visiteurs`

- `id` : Identifiant unique
- `type_visiteur` : Couple, Famille, Solitaire
- `temps_sejour` : Durée du séjour
- `tranche_age` : Tranche d'âge
- `type_personna` : Type de persona touristique
- `date_creation` : Date d'ajout

## 🔧 Configuration

### Variables principales

Dans `database.py` :

```python
DATABASE_URL = "tourisme_data.db"  # Nom de la base de données
```

Dans `app.py` :

```python
BACKUP_INTERVAL_HOURS = 24  # Fréquence backup automatique
```

Dans `api.py` :

```python
# Configuration CORS pour production
allow_origins=["https://votre-site.com"]
```

### Catégories configurables

**Types de visiteurs** : Couple, Famille, Solitaire

**Temps de séjour** : Moins d'une semaine, 1-2 semaines, Plus d'un mois, Plus de 3 mois

**Tranches d'âge** : 18-25 ans, 26-35 ans, 36-45 ans, 46-55 ans, 56-65 ans, Plus de 65 ans

**Types de persona** : Culture/Patrimoine, Randonnée, Plage, Gastronomie, Sport, Détente

## 🌐 Intégration Web

### JavaScript simple

```javascript
// Auto-tracking des pages
fetch("http://localhost:8000/vue-totale", { method: "POST" });

// Enregistrer une vue de page
fetch("http://localhost:8000/page-vue", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    nom_page: document.title,
    categorie: "Accueil",
  }),
});
```

### Formulaire visiteur

```javascript
// Envoyer profil visiteur
const donnees = {
  type_visiteur: "Couple",
  temps_sejour: "1-2 semaines",
  tranche_age: "26-35 ans",
  type_personna: "Culture/Patrimoine",
};

fetch("http://localhost:8000/visiteur", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(donnees),
});
```

## 🛡️ Sécurité et Sauvegardes

### Système de backup automatique

- 🔄 **Backup automatique** avant chaque suppression/modification
- 📅 **Backup quotidien** automatique
- 🗂️ **Conservation** des 10 derniers backups
- ♻️ **Nettoyage automatique** des anciens backups

### Protections intégrées

- ✅ **Confirmations** avant suppression
- 🔒 **Validation** des données d'entrée
- 📊 **Logs** des opérations critiques
- 🔐 **Encodage sécurisé** des données

## 🧪 Tests

### Tests automatisés

```bash
python test_app.py
```

### Tests API manuels

```bash
# Test santé API
curl http://localhost:8000/health

# Test ajout visiteur
curl -X POST "http://localhost:8000/visiteur" \
     -H "Content-Type: application/json" \
     -d '{"type_visiteur":"Couple","temps_sejour":"1-2 semaines","tranche_age":"26-35 ans","type_personna":"Culture/Patrimoine"}'

# Test stats
curl http://localhost:8000/stats
```

### Page de test interactive

Ouvrez `test_api.html` dans un navigateur pour tester l'API visuellement.

## 📊 Monitoring et Analytics

### Métriques disponibles

- 📈 **Vues totales** du site
- 👥 **Nombre de visiteurs** uniques
- 📄 **Pages les plus visitées**
- 🎯 **Répartition par persona**
- ⏱️ **Évolution temporelle**
- 📊 **Taux de conversion** par type

### Exports disponibles

- 📋 **CSV** : Données tabulaires
- 📊 **Excel** : Rapports formatés
- 📈 **PDF** : Rapports visuels
- 📡 **JSON** : Intégration API

## 🔧 Maintenance

### Nettoyage base de données

```bash
# Régénérer avec nouvelles données
python generate_sample_data.py --clean
```

### Gestion des logs

```bash
# Voir logs Streamlit
tail -f ~/.streamlit/logs/streamlit.log

# Voir logs API
# Les logs apparaissent dans le terminal uvicorn
```

### Mise à jour dépendances

```bash
pip install --upgrade -r requirements.txt
```

## 🚀 Déploiement Production

### 1. Configuration serveur

```bash
# Variables d'environnement
export DATABASE_URL=/path/to/production.db
export CORS_ORIGINS=https://votre-site.com
```

### 2. Services systemd (Linux)

Créer `/etc/systemd/system/tourisme-api.service` et `/etc/systemd/system/tourisme-streamlit.service`

### 3. Reverse proxy nginx

```nginx
location /api/ {
    proxy_pass http://localhost:8000/;
}

location / {
    proxy_pass http://localhost:8501/;
}
```

### 4. SSL/HTTPS

Utiliser certbot ou certificats existants

## 📞 Support

### Documentation complète

- 📖 **API** : Consultez `README_API.md`
- 📊 **Interface** : Documentation intégrée dans l'app
- 🧪 **Tests** : Exemples dans `test_api.html`

### Ressources

- 🌐 **Streamlit** : https://docs.streamlit.io/
- ⚡ **FastAPI** : https://fastapi.tiangolo.com/
- 📊 **Plotly** : https://plotly.com/python/

### Dépannage courant

**Port déjà utilisé** :

```bash
lsof -i :8501  # ou :8000
kill -9 <PID>
```

**Base corrompue** :

```bash
rm tourisme_data.db
python generate_sample_data.py
```

**Erreur dépendances** :

```bash
pip install --force-reinstall -r requirements.txt
```

---

🎯 **Système prêt pour la production !** Interface de gestion + API d'intégration + système de backup = Solution complète pour l'analyse de données touristiques.

💡 **Conseil** : Lancez d'abord l'API puis l'interface Streamlit pour une expérience optimale.
├── generate_sample_data.py # Générateur de données d'exemple
├── start.sh # Script de démarrage automatisé
├── requirements.txt # Dépendances Python
├── README.md # Documentation
├── .streamlit/config.toml # Configuration Streamlit
├── backups/ # Répertoire des sauvegardes (créé automatiquement)
└── tourisme_data.db # Base de données SQLite (créée automatiquement)

````

## Utilisation

### 📈 Vue d'ensemble

- Métriques principales en temps réel
- Graphiques de synthèse
- Top des pages visitées
- Répartition des profils visiteurs

### 👥 Gestion des Visiteurs

- Formulaire d'ajout de nouveaux visiteurs
- Liste complète des visiteurs enregistrés
- Export des données en CSV

### 📄 Gestion des Pages

- Enregistrement des vues par page
- Statistiques détaillées par catégorie
- Graphiques d'évolution temporelle

### 📊 Analyses Détaillées

- Graphiques détaillés par critère
- Analyses croisées (heatmaps)
- Corrélations entre les différents profils

## Catégories de Pages

- Accueil
- Activités
- Hébergement
- Restauration
- Culture
- Nature
- Événements
- Pratique

## Interface

L'application dispose d'une interface moderne et professionnelle avec :

- Design responsive
- Graphiques interactifs (Plotly)
- Navigation intuitive
- Métriques en temps réel
- Export de données
- **✏️ Modification des données** avec formulaires intuitifs
- **🗑️ Suppression sécurisée** avec confirmations multiples
- **💾 Système de sauvegarde** automatique et manuel
- **🛡️ Protection contre les pertes de données**

## Base de Données

La base de données SQLite comprend 3 tables principales :

1. **vues_totales** : Compteur global des visites
2. **vues_pages** : Suivi détaillé par page avec nom, catégorie et compteur
3. **visiteurs** : Profils complets des visiteurs avec tous les critères

Les données sont automatiquement persistées et mises à jour en temps réel.

## 🛡️ Sécurité et Sauvegardes

### Sauvegardes Automatiques

- **Avant chaque suppression** : Une sauvegarde est automatiquement créée
- **Nommage automatique** : `auto_backup_AAAAMMJJ_HHMMSS.db`
- **Stockage sécurisé** : Répertoire `backups/` dédié

### Confirmations de Sécurité

- **Suppression individuelle** : Confirmation simple avec aperçu des données
- **Suppression en masse** : Double confirmation avec compteur d'éléments
- **Remise à zéro complète** : Triple confirmation avec saisie manuelle "SUPPRIMER TOUT"

### Gestion des Sauvegardes

- **Visualisation** : Liste détaillée avec taille, date et chemin
- **Restauration** : Un clic pour restaurer n'importe quelle sauvegarde
- **Nettoyage** : Suppression automatique des anciennes sauvegardes (garde les 10 plus récentes)

### Récupération d'Urgence

En cas de problème, utilisez les outils de maintenance :

```bash
python maintenance.py
````

Options disponibles :

- Afficher les statistiques de la base
- Exporter toutes les données en CSV
- Sauvegarder manuellement la base
- Restaurer depuis une sauvegarde spécifique
