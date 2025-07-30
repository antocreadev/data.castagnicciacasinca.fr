#!/bin/bash

# 🏖️ Système d'Analyse de Données Touristiques
# Script de démarrage de l'interface Streamlit

echo "🚀 Démarrage de l'interface Streamlit..."
echo "📊 Interface disponible sur : http://localhost:8501"
echo ""

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création en cours..."
    python -m venv .venv
    echo "✅ Environnement virtuel créé"
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier si les dépendances sont installées
if [ ! -f ".venv/pyvenv.cfg" ]; then
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt
    echo "✅ Dépendances installées"
fi

# Générer les données d'exemple si la base n'existe pas
if [ ! -f "tourisme_data.db" ]; then
    echo "🗄️ Génération des données d'exemple..."
    python generate_sample_data.py
    echo "✅ Base de données initialisée"
fi

echo ""
echo "🎯 Démarrage de l'application Streamlit..."
echo "💡 Conseil : Ouvrez http://localhost:8501 dans votre navigateur"
echo ""

# Lancer Streamlit
streamlit run app.py
