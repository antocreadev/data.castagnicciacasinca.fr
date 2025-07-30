#!/usr/bin/env python3
"""
Tests unitaires pour l'application Office de Tourisme
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from backup_manager import BackupManager


def test_database_operations():
    """Test des opérations de base de données"""
    print("🧪 Test des opérations de base de données...")

    # Créer une base de données temporaire
    temp_db = "test_tourisme.db"

    try:
        db = DatabaseManager(temp_db)

        # Test d'ajout de visiteur
        db.add_visiteur("Couple", "1-2 semaines", "26-35 ans", "Culture/Patrimoine")
        db.add_visiteur("Famille", "Moins d'une semaine", "36-45 ans", "Plage")

        visiteurs = db.get_visiteurs()
        assert len(visiteurs) == 2, f"Attendu 2 visiteurs, obtenu {len(visiteurs)}"
        print("✅ Ajout et récupération des visiteurs : OK")

        # Test de modification de visiteur
        visiteur_id = visiteurs[0][0]
        success = db.update_visiteur(
            visiteur_id, "Solitaire", "Plus d'un mois", "46-55 ans", "Randonnée"
        )
        assert success, "La modification du visiteur a échoué"

        # Vérifier la modification
        updated_visiteur = db.get_visiteur_by_id(visiteur_id)
        assert (
            updated_visiteur[1] == "Solitaire"
        ), f"Type visiteur non modifié: {updated_visiteur[1]}"
        print("✅ Modification des visiteurs : OK")

        # Test de suppression de visiteur
        success = db.delete_visiteur(visiteur_id)
        assert success, "La suppression du visiteur a échoué"

        visiteurs_after_delete = db.get_visiteurs()
        assert (
            len(visiteurs_after_delete) == 1
        ), f"Attendu 1 visiteur après suppression, obtenu {len(visiteurs_after_delete)}"
        print("✅ Suppression des visiteurs : OK")

        # Test des pages
        db.add_vue_page("Test Page", "Culture")
        db.add_vue_page("Test Page 2", "Activités")

        pages = db.get_vues_pages_with_id()
        assert len(pages) == 2, f"Attendu 2 pages, obtenu {len(pages)}"
        print("✅ Ajout et récupération des pages : OK")

        # Test de modification de page
        page_id = pages[0][0]
        success = db.update_page(page_id, "Page Modifiée", "Nature")
        assert success, "La modification de la page a échoué"

        updated_page = db.get_page_by_id(page_id)
        assert (
            updated_page[1] == "Page Modifiée"
        ), f"Nom de page non modifié: {updated_page[1]}"
        assert updated_page[2] == "Nature", f"Catégorie non modifiée: {updated_page[2]}"
        print("✅ Modification des pages : OK")

        # Test de suppression de page
        success = db.delete_page(page_id)
        assert success, "La suppression de la page a échoué"

        pages_after_delete = db.get_vues_pages_with_id()
        assert (
            len(pages_after_delete) == 1
        ), f"Attendu 1 page après suppression, obtenu {len(pages_after_delete)}"
        print("✅ Suppression des pages : OK")

        # Test des statistiques
        stats = db.get_stats_visiteurs()
        assert "type_visiteur" in stats, "Statistiques des visiteurs manquantes"
        print("✅ Statistiques des visiteurs : OK")

        # Test de remise à zéro
        db.reset_all_data()
        visiteurs_final = db.get_visiteurs()
        pages_final = db.get_vues_pages_with_id()
        vues_totales = db.get_vues_totales()

        assert (
            len(visiteurs_final) == 0
        ), f"Attendu 0 visiteurs après reset, obtenu {len(visiteurs_final)}"
        assert (
            len(pages_final) == 0
        ), f"Attendu 0 pages après reset, obtenu {len(pages_final)}"
        assert (
            vues_totales == 0
        ), f"Attendu 0 vues totales après reset, obtenu {vues_totales}"
        print("✅ Remise à zéro complète : OK")

    finally:
        # Nettoyer
        if os.path.exists(temp_db):
            os.remove(temp_db)


def test_backup_operations():
    """Test des opérations de sauvegarde"""
    print("🧪 Test des opérations de sauvegarde...")

    # Créer un répertoire temporaire pour les tests
    temp_dir = tempfile.mkdtemp()
    temp_db = os.path.join(temp_dir, "test_backup.db")

    try:
        # Créer une base de données avec des données
        db = DatabaseManager(temp_db)
        db.add_visiteur("Couple", "1-2 semaines", "26-35 ans", "Culture/Patrimoine")
        db.add_vue_page("Test Page", "Culture")

        # Tester le gestionnaire de sauvegarde
        backup_manager = BackupManager(temp_db)
        backup_manager.backup_dir = os.path.join(temp_dir, "backups")
        backup_manager.ensure_backup_dir()  # S'assurer que le répertoire existe

        # Test de création de sauvegarde
        backup_path = backup_manager.create_backup()
        assert backup_path is not None, "La création de sauvegarde a échoué"
        assert os.path.exists(
            backup_path
        ), f"Le fichier de sauvegarde n'existe pas: {backup_path}"
        print("✅ Création de sauvegarde : OK")

        # Test de liste des sauvegardes
        backups = backup_manager.list_backups()
        assert len(backups) == 1, f"Attendu 1 sauvegarde, obtenu {len(backups)}"
        print("✅ Liste des sauvegardes : OK")

        # Modifier la base de données
        db.add_visiteur("Famille", "Moins d'une semaine", "36-45 ans", "Plage")
        visiteurs_before_restore = db.get_visiteurs()
        assert len(visiteurs_before_restore) == 2, "Base modifiée incorrectement"

        # Test de restauration
        success = backup_manager.restore_backup(backup_path)
        assert success, "La restauration a échoué"

        # Vérifier que les données ont été restaurées
        visiteurs_after_restore = db.get_visiteurs()
        assert (
            len(visiteurs_after_restore) == 1
        ), f"Attendu 1 visiteur après restauration, obtenu {len(visiteurs_after_restore)}"
        print("✅ Restauration de sauvegarde : OK")

        # Test de suppression de sauvegarde
        success = backup_manager.delete_backup(backup_path)
        assert success, "La suppression de sauvegarde a échoué"
        assert not os.path.exists(backup_path), "Le fichier de sauvegarde existe encore"
        print("✅ Suppression de sauvegarde : OK")

    finally:
        # Nettoyer
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_all_tests():
    """Exécute tous les tests"""
    print("🚀 Démarrage des tests de l'application Office de Tourisme")
    print("=" * 60)

    try:
        test_database_operations()
        print()
        test_backup_operations()

        print()
        print("=" * 60)
        print("✅ Tous les tests sont passés avec succès !")
        print("🎉 L'application est prête à être utilisée en production.")

    except AssertionError as e:
        print(f"❌ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
