#!/bin/bash

# Script de démarrage pour l'application Bureau d'Étude - Office de Tourisme

echo "🏖️ Démarrage de l'application Bureau d'Étude - Office de Tourisme"
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
echo "Installation des dépendances..."
pip install -r requirements.txt

# Générer des données d'exemple si la base n'existe pas
if [ ! -f "tourisme_data.db" ]; then
    echo "Génération des données d'exemple..."
    python generate_sample_data.py
fi

# Lancer l'application
echo "Lancement de l'application Streamlit..."
echo "L'application sera disponible sur : http://localhost:8501"
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo "=================================================="

streamlit run app.py
