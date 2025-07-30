#!/bin/bash

# Script pour lancer l'API FastAPI - Office de Tourisme

echo "🚀 Démarrage de l'API Bureau d'Étude - Office de Tourisme"
echo "=================================================="

# Vérifier si l'environnement virtuel existe
if [ ! -d ".venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances API..."
pip install -r requirements_api.txt

# Vérifier que la base de données existe
if [ ! -f "tourisme_data.db" ]; then
    echo "Génération des données d'exemple..."
    python generate_sample_data.py
fi

echo "=================================================="
echo "🌐 L'API sera disponible sur :"
echo "   📡 API: http://localhost:8000"
echo "   📖 Documentation: http://localhost:8000/docs"
echo "   🧪 Test interactif: http://localhost:8000/redoc"
echo ""
echo "💡 Pour tester l'API, ouvrez test_api.html dans un navigateur"
echo "⚡ Interface Streamlit toujours accessible sur: http://localhost:8501"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'API"
echo "=================================================="

# Lancer l'API
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
