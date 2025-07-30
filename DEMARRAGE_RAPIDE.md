# 🚀 Guide de Démarrage Rapide

## 📋 Commandes Essentielles

### 🎯 Démarrage Rapide (Recommandé)

```bash
# Interface Streamlit (Port 8501)
./start_streamlit.sh

# API REST (Port 8000) - Dans un autre terminal
./start_api.sh
```

### 🔧 Démarrage Manuel

```bash
# 1. Activer l'environnement virtuel
source .venv/bin/activate

# 2. Interface Streamlit
streamlit run app.py

# 3. API REST (nouveau terminal)
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 🗄️ Gestion Base de Données

```bash
# Générer données d'exemple
python generate_sample_data.py

# Tests automatisés
python test_app.py

# Maintenance base de données
python maintenance.py
```

## 🌐 URLs Importantes

- **Interface Streamlit** : http://localhost:8501
- **API Documentation** : http://localhost:8000/docs
- **API Health Check** : http://localhost:8000/health
- **Page Test API** : Ouvrir `test_api.html` dans un navigateur

## 📦 Installation Complète

```bash
# 1. Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Génerer données test
python generate_sample_data.py

# 4. Démarrer les services
./start_streamlit.sh  # Terminal 1
./start_api.sh        # Terminal 2
```

## 🧪 Tests Rapides

### Test API avec curl

```bash
# Santé de l'API
curl http://localhost:8000/health

# Ajouter un visiteur
curl -X POST "http://localhost:8000/visiteur" \
     -H "Content-Type: application/json" \
     -d '{
       "type_visiteur": "Couple",
       "temps_sejour": "1-2 semaines",
       "tranche_age": "26-35 ans",
       "type_personna": "Culture/Patrimoine"
     }'

# Récupérer les stats
curl http://localhost:8000/stats
```

### Test JavaScript (pour intégration web)

```javascript
// Tracking automatique d'une page
fetch("http://localhost:8000/vue-totale", { method: "POST" });

// Enregistrer vue de page
fetch("http://localhost:8000/page-vue", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    nom_page: document.title,
    categorie: "Accueil",
  }),
});
```

## 🔧 Dépannage Express

### Problèmes de Port

```bash
# Vérifier les ports utilisés
lsof -i :8501  # Streamlit
lsof -i :8000  # API

# Tuer un processus si nécessaire
kill -9 <PID>
```

### Problèmes de Base de Données

```bash
# Régénérer la base complètement
rm tourisme_data.db
python generate_sample_data.py
```

### Problèmes de Dépendances

```bash
# Réinstaller toutes les dépendances
pip install --force-reinstall -r requirements.txt
```

## 📊 Fonctionnalités Principales

### Interface Streamlit

- 📈 **Dashboard** avec graphiques interactifs
- 👥 **Gestion visiteurs** (CRUD complet)
- 📄 **Gestion pages** avec catégories
- 💾 **Système backup** automatique
- 📋 **Rapports** et exports

### API REST

- 📡 **POST /visiteur** : Ajouter profil
- 📊 **POST /page-vue** : Tracker page
- 🔢 **POST /vue-totale** : Incrémenter compteur
- 📈 **GET /stats** : Récupérer statistiques
- 🚀 **POST /tracking/bulk** : Envoi en lot

## 🎯 Cas d'Usage Typiques

### 1. Analytics de Site Web

- Intégrer le tracking JavaScript sur votre site
- Suivre les pages visitées automatiquement
- Collecter les profils visiteurs via formulaires

### 2. Tableau de Bord Office de Tourisme

- Visualiser les données de fréquentation
- Analyser les profils de visiteurs
- Générer des rapports pour les décideurs

### 3. API d'Intégration

- Connecter plusieurs sites/applications
- Centraliser les données touristiques
- Fournir des stats en temps réel

## 💡 Conseils d'Utilisation

- ✅ **Démarrez toujours l'API avant l'interface** pour les tests
- 📊 **Utilisez la documentation interactive** `/docs` pour tester l'API
- 💾 **Les backups sont automatiques** avant chaque suppression
- 🔄 **L'API supporte CORS** pour l'intégration web
- 📱 **L'interface est responsive** et fonctionne sur mobile

---

🎯 **Système prêt à l'emploi !**

- Interface de gestion complète
- API REST pour intégration web
- Système de backup intégré
- Documentation complète

💬 **Besoin d'aide ?** Consultez les fichiers README.md et README_API.md pour plus de détails.
