# Guide d'Utilisation - Bureau d'Étude Office de Tourisme 🏖️

## 🚀 Démarrage Rapide

### Première utilisation

1. **Lancez l'application** : `./start.sh` ou `streamlit run app.py`
2. **Accédez à l'interface** : http://localhost:8501
3. **Explorez les données d'exemple** déjà présentes

### Navigation principale

- **📈 Vue d'ensemble** : Tableau de bord avec métriques clés
- **👥 Gestion des Visiteurs** : CRUD complet des profils visiteurs
- **📄 Gestion des Pages** : CRUD complet des pages du site
- **📊 Analyses Détaillées** : Graphiques et analyses croisées
- **🗑️ Suppression en Masse** : Outils de nettoyage avancés
- **💾 Gestion des Sauvegardes** : Système de backup complet

## 👥 Gestion des Visiteurs

### Ajouter un visiteur

1. Dans l'onglet "👥 Gestion des Visiteurs"
2. Remplir le formulaire d'ajout (section dépliée par défaut)
3. Cliquer sur "Ajouter le visiteur"

### Modifier un visiteur

1. Dans la section "Liste des Visiteurs"
2. Sélectionner l'ID du visiteur dans la colonne de droite
3. Cliquer sur "✏️ Modifier"
4. Modifier les valeurs dans le formulaire
5. Cliquer sur "💾 Sauvegarder"

### Supprimer un visiteur

1. Sélectionner l'ID du visiteur
2. Cliquer sur "🗑️ Supprimer"
3. Confirmer la suppression (sauvegarde automatique créée)

## 📄 Gestion des Pages

### Enregistrer une vue de page

1. Dans l'onglet "📄 Gestion des Pages"
2. Saisir le nom de la page et sélectionner la catégorie
3. Cliquer sur "Enregistrer la vue"

### Modifier une page

1. Dans la section "Gestion des Pages"
2. Sélectionner la page dans la liste déroulante
3. Cliquer sur "✏️ Modifier"
4. Modifier les valeurs et sauvegarder

### Supprimer une page

1. Sélectionner la page à supprimer
2. Cliquer sur "🗑️ Supprimer"
3. Confirmer (sauvegarde automatique créée)

## 🗑️ Suppression en Masse

### ⚠️ Attention : Actions irréversibles !

Toutes les suppressions en masse créent automatiquement une sauvegarde.

### Supprimer des visiteurs par critères

1. Aller dans "🗑️ Suppression en Masse"
2. Déplier "👥 Suppression des Visiteurs"
3. Définir les filtres (type, séjour, âge, centres d'intérêt)
4. Prévisualiser les visiteurs correspondants
5. Confirmer la suppression

### Supprimer des pages par catégorie

1. Déplier "📄 Suppression des Pages"
2. Sélectionner les catégories à supprimer
3. Prévisualiser les pages concernées
4. Confirmer la suppression

### Remise à zéro complète 💥

1. Déplier "💥 Remise à Zéro Complète"
2. Lire attentivement les avertissements
3. Cliquer sur "💥 TOUT SUPPRIMER"
4. Taper exactement "SUPPRIMER TOUT"
5. Confirmer définitivement

## 💾 Sauvegardes

### Sauvegarde automatique

- **Déclenchement** : Avant chaque suppression
- **Nommage** : `auto_backup_AAAAMMJJ_HHMMSS.db`
- **Stockage** : Répertoire `backups/`

### Sauvegarde manuelle

1. Aller dans "💾 Gestion des Sauvegardes"
2. Optionnel : Saisir un nom personnalisé
3. Cliquer sur "💾 Créer une sauvegarde"

### Restaurer une sauvegarde

1. Dans "💾 Gestion des Sauvegardes"
2. Déplier la sauvegarde souhaitée
3. Cliquer sur "🔄 Restaurer"
4. Confirmer (remplace toutes les données actuelles)

### Nettoyer les anciennes sauvegardes

1. En bas de la page des sauvegardes
2. Cliquer sur "🧹 Nettoyer les anciennes sauvegardes"
3. Garde automatiquement les 10 plus récentes

## 📊 Export de données

### Export CSV des visiteurs

1. Dans "👥 Gestion des Visiteurs"
2. Cliquer sur "📥 Télécharger les données CSV"
3. Le fichier se nomme `visiteurs_AAAAMMJJ.csv`

### Export complet (maintenance)

```bash
python maintenance.py
# Choisir option 2 : Exporter toutes les données
```

## 🛠️ Maintenance

### Outils en ligne de commande

```bash
python maintenance.py
```

Options disponibles :

1. **Afficher les statistiques** : Vue d'ensemble de la base
2. **Exporter toutes les données** : CSV complet
3. **Sauvegarder la base** : Backup manuel
4. **Restaurer depuis un backup** : Récupération d'urgence
5. **Réinitialiser la base** : Remise à zéro totale

### Tests de fonctionnement

```bash
python test_app.py
```

Vérifie que toutes les fonctionnalités marchent correctement.

## 🔧 Dépannage

### L'application ne démarre pas

```bash
# Vérifier l'environnement Python
./start.sh

# Ou manuellement :
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Erreur de base de données

1. Vérifier que `tourisme_data.db` existe
2. Si corrompue, restaurer depuis une sauvegarde
3. En dernier recours : `python generate_sample_data.py`

### Données perdues

1. Aller dans "💾 Gestion des Sauvegardes"
2. Restaurer la sauvegarde la plus récente
3. Ou utiliser `python maintenance.py` > option 4

### Performances lentes

1. Nettoyer les anciennes sauvegardes
2. Exporter et archiver les anciennes données
3. Redémarrer l'application

## 📈 Bonnes Pratiques

### Utilisation quotidienne

- **Créer une sauvegarde manuelle** avant les grosses modifications
- **Nettoyer régulièrement** les anciennes sauvegardes
- **Exporter les données** périodiquement pour archivage

### Avant une suppression importante

1. Créer une sauvegarde nommée (ex: "avant_nettoyage_hiver")
2. Vérifier les filtres de suppression
3. Confirmer en ayant lu les aperçus de données

### Maintenance préventive

- **Hebdomadaire** : Vérifier l'espace disque des sauvegardes
- **Mensuel** : Exporter et archiver les données
- **Trimestriel** : Tester la restauration d'une sauvegarde

## 💡 Astuces

### Navigation rapide

- Utilisez les métriques de la vue d'ensemble pour surveiller l'activité
- Les graphiques sont interactifs (zoom, sélection)
- Les tableaux permettent le tri par colonne

### Analyses avancées

- Croisez les données dans "📊 Analyses Détaillées"
- Utilisez les heatmaps pour identifier les corrélations
- Exportez les données pour des analyses externes (Excel, R, Python)

### Gestion des données

- Utilisez des noms descriptifs pour vos sauvegardes importantes
- Profitez des filtres de suppression en masse pour nettoyer efficacement
- Les sauvegardes automatiques vous protègent des erreurs

---

🎯 **Support** : Consultez le README.md pour plus de détails techniques
🐛 **Problèmes** : Vérifiez d'abord les logs de l'application dans le terminal

---

## 🌐 Intégration API sur Site Web

### Démarrage de l'API

L'application dispose maintenant d'une **API REST FastAPI** pour collecter automatiquement les données depuis votre site web.

#### Lancer l'API

```bash
./start_api.sh
# ou manuellement :
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**URLs importantes :**

- 📡 **API** : http://localhost:8000
- 📖 **Documentation interactive** : http://localhost:8000/docs
- 🧪 **Documentation alternative** : http://localhost:8000/redoc
- 🧪 **Page de test** : ouvrir `test_api.html` dans un navigateur

### 🚀 Intégration rapide sur votre site

#### 1. Code JavaScript de base à inclure

```javascript
// Configuration
const API_BASE_URL = "http://localhost:8000";

// Comptage automatique des vues à chaque page
document.addEventListener("DOMContentLoaded", async () => {
  // Incrémenter les vues totales
  await fetch(`${API_BASE_URL}/vue-totale`, { method: "POST" });

  // Enregistrer la page spécifique
  await fetch(`${API_BASE_URL}/page-vue`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nom_page: document.title,
      categorie: "Accueil", // À adapter selon votre page
    }),
  });
});
```

#### 2. Formulaire de profil visiteur

```html
<form id="form-visiteur">
  <select name="type_visiteur" required>
    <option value="Couple">En couple</option>
    <option value="Famille">En famille</option>
    <option value="Solitaire">Seul(e)</option>
  </select>

  <select name="temps_sejour" required>
    <option value="Moins d'une semaine">Moins d'une semaine</option>
    <option value="1-2 semaines">1-2 semaines</option>
    <option value="Plus d'un mois">Plus d'un mois</option>
    <option value="Plus de 3 mois">Plus de 3 mois</option>
  </select>

  <select name="tranche_age" required>
    <option value="18-25 ans">18-25 ans</option>
    <option value="26-35 ans">26-35 ans</option>
    <option value="36-45 ans">36-45 ans</option>
    <option value="46-55 ans">46-55 ans</option>
    <option value="56-65 ans">56-65 ans</option>
    <option value="Plus de 65 ans">Plus de 65 ans</option>
  </select>

  <select name="type_personna" required>
    <option value="Culture/Patrimoine">Culture & Patrimoine</option>
    <option value="Randonnée">Randonnée</option>
    <option value="Plage">Plage</option>
    <option value="Gastronomie">Gastronomie</option>
    <option value="Sport">Sport</option>
    <option value="Détente">Détente</option>
  </select>

  <button type="submit">Envoyer</button>
</form>

<script>
  document
    .getElementById("form-visiteur")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);

      const response = await fetch(`${API_BASE_URL}/visiteur`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type_visiteur: formData.get("type_visiteur"),
          temps_sejour: formData.get("temps_sejour"),
          tranche_age: formData.get("tranche_age"),
          type_personna: formData.get("type_personna"),
        }),
      });

      if (response.ok) {
        alert("Merci pour vos informations !");
        e.target.reset();
      }
    });
</script>
```

### 📊 Endpoints API disponibles

#### POST `/visiteur`

Ajouter un profil visiteur

```javascript
await fetch(`${API_BASE_URL}/visiteur`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    type_visiteur: "Couple",
    temps_sejour: "1-2 semaines",
    tranche_age: "26-35 ans",
    type_personna: "Culture/Patrimoine",
  }),
});
```

#### POST `/page-vue`

Enregistrer une vue de page

```javascript
await fetch(`${API_BASE_URL}/page-vue`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    nom_page: "Randonnées GR20",
    categorie: "Activités",
  }),
});
```

#### POST `/vue-totale`

Incrémenter les vues totales

```javascript
await fetch(`${API_BASE_URL}/vue-totale`, { method: "POST" });
```

#### GET `/stats`

Récupérer les statistiques

```javascript
const response = await fetch(`${API_BASE_URL}/stats`);
const stats = await response.json();
console.log(`${stats.vues_totales} vues totales`);
```

### 🔧 Fichiers de référence

- **`exemples_javascript.js`** : Code complet avec tous les exemples
- **`test_api.html`** : Page de test interactive complète
- **Documentation API** : http://localhost:8000/docs

### 🛡️ Sécurité et Production

En production, remplacez `http://localhost:8000` par votre domaine et configurez CORS correctement dans `api.py`.
