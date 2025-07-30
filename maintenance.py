"""
Utilitaires de maintenance pour l'application Tourisme Castagniccia Casinca
"""

from database import DatabaseManager
import sqlite3
import pandas as pd
from datetime import datetime


class MaintenanceTools:
    def __init__(self):
        self.db = DatabaseManager()

    def export_all_data(self, filename=None):
        """Exporte toutes les données en CSV"""
        if not filename:
            filename = f"export_complet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Récupérer toutes les données des visiteurs
        visiteurs = self.db.get_visiteurs()
        if visiteurs:
            df = pd.DataFrame(
                visiteurs,
                columns=[
                    "ID",
                    "Type Visiteur",
                    "Temps Séjour",
                    "Tranche Âge",
                    "Centres d'intérêt",
                    "Date Visite",
                ],
            )
            df.to_csv(filename, index=False)
            print(f"Données exportées vers {filename}")
        else:
            print(" Aucune donnée à exporter")

    def reset_database(self):
        """Remet à zéro la base de données"""
        confirm = input(
            " Êtes-vous sûr de vouloir réinitialiser la base de données ? (oui/non): "
        )
        if confirm.lower() == "oui":
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Supprimer toutes les données
            cursor.execute("DELETE FROM visiteurs")
            cursor.execute("DELETE FROM vues_pages")
            cursor.execute("UPDATE vues_totales SET nombre_vues = 0")

            conn.commit()
            conn.close()
            print("Base de données réinitialisée")
        else:
            print(" Réinitialisation annulée")

    def get_database_stats(self):
        """Affiche les statistiques de la base de données"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Compter les visiteurs
        cursor.execute("SELECT COUNT(*) FROM visiteurs")
        nb_visiteurs = cursor.fetchone()[0]

        # Compter les pages
        cursor.execute("SELECT COUNT(*) FROM vues_pages")
        nb_pages = cursor.fetchone()[0]

        # Vues totales
        vues_totales = self.db.get_vues_totales()

        # Dernière visite
        cursor.execute("SELECT MAX(date_visite) FROM visiteurs")
        derniere_visite = cursor.fetchone()[0]

        conn.close()

        print("Statistiques de la base de données")
        print("=" * 40)
        print(f"Nombre de visiteurs: {nb_visiteurs}")
        print(f"Nombre de pages trackées: {nb_pages}")
        print(f" Vues totales du site: {vues_totales}")
        print(f"🕒 Dernière visite: {derniere_visite or 'Aucune'}")
        print("=" * 40)

    def backup_database(self, filename=None):
        """Sauvegarde la base de données"""
        if not filename:
            filename = f"backup_tourisme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

        try:
            import shutil

            shutil.copy("tourisme_data.db", filename)
            print(f"Sauvegarde créée: {filename}")
        except Exception as e:
            print(f" Erreur lors de la sauvegarde: {e}")

    def restore_database(self, backup_filename):
        """Restaure la base de données depuis une sauvegarde"""
        confirm = input(
            f" Êtes-vous sûr de vouloir restaurer depuis {backup_filename} ? (oui/non): "
        )
        if confirm.lower() == "oui":
            try:
                import shutil

                shutil.copy(backup_filename, "tourisme_data.db")
                print("Base de données restaurée")
            except Exception as e:
                print(f" Erreur lors de la restauration: {e}")
        else:
            print(" Restauration annulée")


def main():
    """Menu principal des outils de maintenance"""
    tools = MaintenanceTools()

    while True:
        print("\n🔧 Outils de Maintenance - Tourisme Castagniccia Casinca")
        print("=" * 50)
        print("1. Afficher les statistiques")
        print("2. Exporter toutes les données")
        print("3. Sauvegarder la base de données")
        print("4. Restaurer la base de données")
        print("5. Réinitialiser la base de données")
        print("0. Quitter")
        print("=" * 50)

        choix = input("Votre choix: ")

        if choix == "1":
            tools.get_database_stats()
        elif choix == "2":
            tools.export_all_data()
        elif choix == "3":
            tools.backup_database()
        elif choix == "4":
            filename = input("Nom du fichier de sauvegarde: ")
            tools.restore_database(filename)
        elif choix == "5":
            tools.reset_database()
        elif choix == "0":
            print("👋 Au revoir!")
            break
        else:
            print(" Choix invalide")


if __name__ == "__main__":
    main()
