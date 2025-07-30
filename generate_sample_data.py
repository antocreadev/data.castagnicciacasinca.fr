#!/usr/bin/env python3
"""
Script pour générer des données de démonstration pour l'application Office de Tourisme
"""

import random
from datetime import datetime, timedelta
from database import DatabaseManager


def generate_sample_data():
    """Génère des données d'exemple pour démonstration"""

    print("🏖️ Génération des données d'exemple pour l'Office de Tourisme...")

    # Initialiser la base de données
    db = DatabaseManager()

    # Données d'exemple pour les pages
    pages_data = [
        ("Accueil", "Accueil"),
        ("Randonnées GR20", "Activités"),
        ("Plages de Castagniccia", "Nature"),
        ("Hôtel des Montagnes", "Hébergement"),
        ("Restaurant U Castagnu", "Restauration"),
        ("Musée de la Châtaigne", "Culture"),
        ("Festival de la Châtaigne", "Événements"),
        ("Camping Les Pins", "Hébergement"),
        ("Sentier des Bergeries", "Activités"),
        ("Église San Pietro", "Culture"),
        ("Marché Local", "Pratique"),
        ("Centre Aquatique", "Activités"),
        ("Panorama Monte Padru", "Nature"),
        ("Gîte Rural Casinca", "Hébergement"),
        ("Pizzeria A Castagniccia", "Restauration"),
    ]

    # Ajouter des vues pour les pages (entre 5 et 50 vues par page)
    print("📄 Ajout des vues de pages...")
    for nom_page, categorie in pages_data:
        nombre_vues = random.randint(5, 50)
        for _ in range(nombre_vues):
            db.add_vue_page(nom_page, categorie)

    # Types de visiteurs avec leurs probabilités
    types_visiteurs = ["Couple", "Famille", "Solitaire"]
    temps_sejours = [
        "Moins d'une semaine",
        "1-2 semaines",
        "Plus d'un mois",
        "Plus de 3 mois",
    ]
    tranches_ages = [
        "18-25 ans",
        "26-35 ans",
        "36-45 ans",
        "46-55 ans",
        "56-65 ans",
        "Plus de 65 ans",
    ]
    types_personnas = [
        "Culture/Patrimoine",
        "Randonnée",
        "Plage",
        "Gastronomie",
        "Sport",
        "Détente",
    ]

    # Générer des visiteurs réalistes
    print("👥 Ajout des visiteurs...")
    nombre_visiteurs = random.randint(50, 100)

    for _ in range(nombre_visiteurs):
        # Logique pour rendre les données plus réalistes
        type_visiteur = random.choices(
            types_visiteurs, weights=[35, 45, 20]  # Plus de familles et couples
        )[0]

        # Les familles ont tendance à rester plus longtemps
        if type_visiteur == "Famille":
            temps_sejour = random.choices(temps_sejours, weights=[30, 40, 20, 10])[0]
        else:
            temps_sejour = random.choices(temps_sejours, weights=[40, 35, 15, 10])[0]

        # Distribution d'âge réaliste pour un office de tourisme
        tranche_age = random.choices(tranches_ages, weights=[15, 20, 25, 20, 15, 5])[0]

        # Centres d'intérêt avec des préférences régionales
        type_personna = random.choices(
            types_personnas,
            weights=[25, 30, 20, 15, 5, 5],  # Plus de culture et randonnée
        )[0]

        db.add_visiteur(type_visiteur, temps_sejour, tranche_age, type_personna)

    # Ajouter quelques vues totales supplémentaires
    for _ in range(random.randint(200, 500)):
        db.increment_vues_totales()

    print("✅ Données d'exemple générées avec succès!")
    print(f"📊 {len(pages_data)} types de pages créés")
    print(f"👥 {nombre_visiteurs} visiteurs ajoutés")
    print("🚀 Vous pouvez maintenant lancer l'application avec: streamlit run app.py")


if __name__ == "__main__":
    generate_sample_data()
